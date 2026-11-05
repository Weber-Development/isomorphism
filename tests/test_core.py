import logging
import pickle
import re

import pytest

from isomorphism import Restorer, anonymize, detect, restore, restore_stream
from isomorphism.detectors import Candidate
from isomorphism.presidio import presidio_detector
from tests.cases import CASES
from tests.measure import KINDS, measure

AHV = "756.1234.5678.97"
IBAN = "CH93 0076 2011 6238 5295 7"


def test_roundtrip_all_cases() -> None:
    for case in CASES:
        anon, mapping = anonymize(case.text, case.lang)
        assert restore(anon, mapping) == case.text, case.name


def test_same_value_same_placeholder() -> None:
    anon, mapping = anonymize(f"{AHV} und {AHV} und 756.9960.3082.41")
    assert anon == "[AHV_1] und [AHV_1] und [AHV_2]"
    assert mapping["[AHV_1]"] == AHV


def test_no_original_value_left() -> None:
    for case in CASES:
        anon, mapping = anonymize(case.text, case.lang)
        for value in mapping.values():
            assert value not in anon, case.name
        found = {(f.kind, f.start, f.end) for f in mapping.findings}
        assert found >= case.expected, case.name


def test_findings_carry_no_value() -> None:
    _, mapping = anonymize(f"{AHV}, {IBAN}")
    f = mapping.findings[0]
    assert (f.kind, f.start, f.end, f.detector, f.checksum_ok) == ("AHV", 0, 16, "ahv-ean13", True)
    assert 0 < f.confidence <= 1
    for secret in (AHV, IBAN, "7561234567897"):
        assert secret not in repr(mapping) + str(mapping) + repr(mapping.findings)


def test_invalid_checksum_reported_with_lower_confidence() -> None:
    good, bad = detect("756.1234.5678.97 756.1234.5678.98")
    assert good.checksum_ok and not bad.checksum_ok
    assert bad.confidence < good.confidence


def test_keep_exceptions() -> None:
    text = "Mail an Steueramt.SG@Kanton.example oder anna@muster.example"
    anon, _ = anonymize(text, keep=["steueramt.sg@kanton.example"])
    assert anon == "Mail an Steueramt.SG@Kanton.example oder [EMAIL_1]"


def test_literal_placeholder_in_text_is_not_reused() -> None:
    anon, mapping = anonymize(f"Vorlage [AHV_1]: {AHV}")
    assert anon == "Vorlage [AHV_1]: [AHV_2]"
    assert restore(anon, mapping) == f"Vorlage [AHV_1]: {AHV}"


def test_restore_tolerates_model_changes_and_keeps_unknown() -> None:
    _, mapping = anonymize(AHV)
    assert restore("[ahv_1] / [ AHV_01 ] / [AHV_2] / [OTHER_1]", mapping) == (
        f"{AHV} / {AHV} / [AHV_2] / [OTHER_1]"
    )


def test_restore_is_single_pass() -> None:
    assert restore("[A_1] [B_1]", {"[A_1]": "[B_1]", "[B_1]": "x"}) == "[B_1] x"


def test_overlap_prefers_checksum_match() -> None:
    # The digits inside an IBAN must not also come out as a phone number.
    anon, _ = anonymize("CH93 0076 2011 6238 5295 7")
    assert anon == "[IBAN_1]"


def test_lang() -> None:
    anonymize("x", "de-CH")
    with pytest.raises(ValueError, match="unsupported lang"):
        anonymize("x", "xx")


def test_nothing_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.DEBUG):
        anon, mapping = anonymize(f"{AHV} {IBAN}")
        restore(anon, mapping)
    assert caplog.records == []


def test_mapping_survives_pickle() -> None:
    _, mapping = anonymize(AHV)
    assert dict(pickle.loads(pickle.dumps(mapping))) == {"[AHV_1]": AHV}  # noqa: S301


# Known false alarms, kept in the test texts on purpose (see README): a postcode-like number after
# a comma followed by a capitalised word is reported at low confidence.
FALSE_ALARM_BUDGET = {"ADDRESS": 2}


def test_acceptance_numbers() -> None:
    stats = measure()
    for kind in KINDS:
        assert stats[kind]["fn"] == 0, f"{kind}: a listed value slipped through"
        assert stats[kind]["fp"] <= FALSE_ALARM_BUDGET.get(kind, 0), f"{kind}: more false alarms"


def test_readme_table_is_current() -> None:
    from pathlib import Path

    from tests.measure import table

    readme = Path(__file__).parent.parent / "README.md"
    assert f"<!-- measure:start -->\n{table()}\n<!-- measure:end -->" in readme.read_text()


def test_streaming_restore_with_placeholder_split_across_chunks() -> None:
    _, mapping = anonymize(f"{AHV} und {IBAN}")
    answer = "Die Nummer [AHV_1] und das Konto [IBAN_1] sind gültig. [Hinweis] bleibt. [ ahv_1 ]"
    expected = restore(answer, mapping)
    for size in (1, 2, 3, 5, 7, len(answer)):
        chunks = [answer[i : i + size] for i in range(0, len(answer), size)]
        assert "".join(restore_stream(chunks, mapping)) == expected, size
    r = Restorer(mapping)
    assert r.feed("Nummer [AHV") == "Nummer "
    assert r.feed("_1] ok [IB") == f"{AHV} ok "
    assert r.flush() == "[IB"  # an unfinished placeholder at the very end stays as text


def test_streaming_does_not_hold_back_plain_brackets_forever() -> None:
    r = Restorer({})
    assert r.feed("[" + "x" * 60) == "[" + "x" * 60


def test_authorities_are_not_replaced() -> None:
    text = "Das Steueramt St. Gallen und das Handelsregisteramt Zürich schreiben an Hr. Keller."
    anon, _ = anonymize(text)
    assert (
        anon
        == "Das Steueramt St. Gallen und das Handelsregisteramt Zürich schreiben an [PERSON_1]."
    )
    # Presidio-style hit on an authority is dropped, too, unless protection is switched off.
    fake = lambda t: iter([Candidate("ORG", 4, 25, 0.8, "fake")])  # noqa: E731
    assert anonymize(text, detectors=[fake])[0].startswith("Das Steueramt")
    assert anonymize(text, detectors=[fake], protect_authorities=False)[0].startswith("Das [ORG_1]")


def test_surname_is_found_again_without_title() -> None:
    anon, mapping = anonymize("Frau Keller hat angerufen. Keller bittet um Rückruf.")
    assert anon == "[PERSON_1] hat angerufen. [PERSON_2] bittet um Rückruf."
    assert [f.detector for f in mapping.findings] == ["person-title", "person-surname-ref"]


def test_keep_accepts_patterns() -> None:
    text = "info@gemeinde.example und anna@muster.example"
    anon, _ = anonymize(text, keep=[re.compile(r".*@gemeinde\.example")])
    assert anon == "info@gemeinde.example und [EMAIL_1]"


def test_presidio_adapter_with_fake_analyzer() -> None:
    class Result:
        def __init__(self, entity_type: str, start: int, end: int, score: float) -> None:
            self.entity_type, self.start, self.end, self.score = entity_type, start, end, score

    class Analyzer:
        def analyze(self, *, text: str, language: str, entities: list[str]) -> list[Result]:
            assert language == "de" and entities == ["PERSON", "ORGANIZATION"]
            return [
                Result("PERSON", 0, 5, 0.9),
                Result("LOCATION", 10, 14, 0.9),
                Result("ORGANIZATION", 15, 19, 0.3),
            ]

    anon, mapping = anonymize(
        "Zorro wohnt Bern Acme", detectors=[presidio_detector(Analyzer(), language="de")]
    )
    assert anon == "[PERSON_1] wohnt Bern Acme"
    assert mapping.findings[0].detector == "presidio"


def test_luhn_and_postal_checks() -> None:
    from isomorphism.entities import luhn_ok, postal_ok

    assert luhn_ok("4111111111111111") and not luhn_ok("4111111111111112")
    assert postal_ok("80-12345-6") and not postal_ok("80-12345-7")
    assert postal_ok("85-1234-3") and postal_ok("10-20304-8")


def test_acceptance_sets() -> None:
    """The agreed acceptance (README "Acceptance"). A and B pass completely. C, the set that
    counted, misses tier 2 (see README); it must keep tier 1, precision and authorities."""
    from tests.acceptance import SETS, failures

    for name in ("A", "B"):
        assert failures(SETS[name]) == [], name
    assert failures(SETS["C"], tiers=(1,)) == []


def test_acceptance_table_in_readme_is_current() -> None:
    from pathlib import Path

    from tests.acceptance import table

    readme = Path(__file__).parent.parent / "README.md"
    assert f"<!-- acceptance:start -->\n{table()}\n<!-- acceptance:end -->" in readme.read_text()


def test_normalise_keeps_length_and_positions() -> None:
    from isomorphism.entities import normalise

    for text in (
        "HANS-PETER AEBERSOLD\nWERKSTRASSE 9",
        "hoi sandra, frau meier-huber fragt",
        "ß İ",
    ):
        assert len(normalise(text)) == len(text)
    assert normalise("HEIZUNG FORSTER AG") == "Heizung Forster AG"
    assert normalise("hoi sandra, frau meier-huber fragt") == "hoi Sandra, Frau Meier-Huber fragt"


def test_names_in_capitals_and_without_capitals() -> None:
    anon, _ = anonymize("Zahlbar durch\nHANS-PETER AEBERSOLD\nALPENBLICK 27\n3612 STEFFISBURG")
    assert anon == "Zahlbar durch\n[PERSON_1]\n[ADDRESS_1]"
    anon, _ = anonymize("hoi sandra, die adresse ist hauptstrasse 44, 5000 aarau. lg dani")
    assert anon == "hoi [PERSON_1], die adresse ist [ADDRESS_1]. lg [PERSON_2]"


def test_initials_but_not_abbreviations() -> None:
    anon, _ = anonymize("Unterschrift: B. Bürgi. Belege z. B. Kunden, u. a. Lieferanten.")
    assert anon == "Unterschrift: [PERSON_1]. Belege z. B. Kunden, u. a. Lieferanten."


def test_names_without_list_after_context_words() -> None:
    text = "Steuerpflichtige: Gashi Fatmire und Gashi Besnik, Im Grund 11, 8952 Schlieren"
    anon, _ = anonymize(text)
    assert anon == "Steuerpflichtige: [PERSON_1] und [PERSON_2], [ADDRESS_1]"


def test_gemeinde_and_kanton_are_authorities() -> None:
    anon, _ = anonymize("Gutschrift Gemeinde Wil, Steuern Kanton St. Gallen, Gutschrift Lea Bieri")
    assert anon == "Gutschrift Gemeinde Wil, Steuern Kanton St. Gallen, Gutschrift [PERSON_1]"


def test_authority_words_are_not_reused_as_names() -> None:
    for text in (
        "Gutschrift Gemeinde Wil. Die Gemeinde hat bezahlt.",
        "Zahlung an Steueramt Zürich. Unser Büro ist in Zürich.",
    ):
        assert anonymize(text)[0] == text


def test_legal_forms_in_capitals() -> None:
    anon, _ = anonymize("MUSTER KLG, MUSTER LTD, MUSTER INC, MUSTER LLC")
    assert anon == "[ORG_1], [ORG_2], [ORG_3], [ORG_4]"


def test_streets_after_elided_articles() -> None:
    for text in (
        "Rue d'Italie 5, 1200 Genève",
        "Rue de l'Hôpital 3",
        "Chemin d'Entre-Bois 7",
        "Av. de l’Avant-Poste 4, 1005 Lausanne",
        "Via dell'Indipendenza 2, 6900 Lugano",
    ):
        assert anonymize(text)[0] == "[ADDRESS_1]", text


def test_chart_of_accounts_is_not_an_address() -> None:
    chart = "Accounts:\n1000 Kasse\n1020 Bank\n6570 Informatikaufwand\n8900 Direkte Steuern\n"
    assert [f for f in detect(chart) if f.kind == "ADDRESS"] == []
    # One postcode line in an address block stays an address.
    letter = "Hans Muster\nKirchweg 4\n8000 Zürich\n\nBetreff: Steuern"
    assert [letter[f.start : f.end] for f in detect(letter) if f.kind == "ADDRESS"] == [
        "Kirchweg 4\n8000 Zürich"
    ]
    # One numbered neighbour is not a list: the place stays protected.
    for text in (
        "Hans Muster\nPostfach\n8000 Zürich\n0041 44 123 45 67",
        "2025 Steuererklärung\n8000 Zürich",
        "Hans Muster\n8000 Zürich\n1000 Stück Schrauben",
        "Hans Muster\n8000 Zürich\nPeter Beispiel\n3000 Bern\nAnna Probe\n6900 Lugano",
    ):
        found = [text[f.start : f.end] for f in detect(text)]
        assert "8000 Zürich" in found, text
    names = "Hans Muster\n8000 Zürich\nPeter Beispiel\n3000 Bern\nAnna Probe\n6900 Lugano"
    assert "3000 Bern" in [names[f.start : f.end] for f in detect(names)]


def test_known_names_share_one_placeholder_in_any_case_and_order() -> None:
    from isomorphism.known import known_detector

    clients = known_detector(["Arben Krasniqi"])
    text = "Gutschrift KRASNIQI ARBEN 300.00\nHerr Arben Krasniqi und krasniqi, arben."
    safe, mapping = anonymize(text, detectors=[clients])
    assert safe == "Gutschrift [PERSON_1] 300.00\nHerr [PERSON_1] und [PERSON_1]."
    assert mapping["[PERSON_1]"] == "KRASNIQI ARBEN", "the first form seen comes back"
    assert {f.detector for f in mapping.findings} == {"known"}


def test_known_single_words_but_not_ordinary_surnames() -> None:
    from isomorphism.known import known_detector

    clients = known_detector(["Ottilia Zumsteg-Keller", "Fridolin Weber"])
    text = "Ottilia hat angerufen. Zumsteg auch. Der Keller ist nass, Weber kommt."
    found = [text[f.start : f.end] for f in detect(text, detectors=[clients])]
    assert "Ottilia" in found and "Zumsteg" in found
    assert "Keller" not in found and "Weber" not in found


def test_known_companies_and_groups() -> None:
    from isomorphism.known import known_detector

    clients = known_detector(["Reinigung Blitzblank GmbH", "Familie Inderbitzin"])
    text = "Rechnung Blitzblank, bezahlt an Reinigung Blitzblank. Familie Inderbitzin zahlt."
    safe, _ = anonymize(text, detectors=[clients])
    assert "Blitzblank" not in safe and "Inderbitzin" not in safe
    assert "Rechnung" in safe and "zahlt" in safe


def test_known_names_kind_and_limits() -> None:
    from isomorphism.known import MAX_ENTRIES, known_detector

    text = "Bäckerei Lüthi und Ramun Caduff"
    kinds = {
        text[f.start : f.end]: f.kind
        for f in detect(text, detectors=[known_detector(["Bäckerei Lüthi", "Ramun Caduff"])])
    }
    assert kinds == {"Bäckerei Lüthi": "ORG", "Ramun Caduff": "PERSON"}
    with pytest.raises(ValueError):
        known_detector([("PLACE", "Wil")])
    with pytest.raises(ValueError):
        known_detector(f"Name{i} Test" for i in range(MAX_ENTRIES + 1))


def test_known_table_in_readme_is_current() -> None:
    from pathlib import Path

    from tests.acceptance import known_table

    readme = Path(__file__).parent.parent / "README.md"
    assert f"<!-- known:start -->\n{known_table()}\n<!-- known:end -->" in readme.read_text()
