import logging
import pickle

import pytest

from isomorphism import anonymize, detect, restore
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
        assert len(mapping.findings) == len(case.expected), case.name


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


def test_acceptance_numbers() -> None:
    stats = measure()
    for kind in KINDS:
        assert stats[kind]["fn"] == 0, f"{kind}: a listed value slipped through"
        assert stats[kind]["fp"] == 0, f"{kind}: false alarm"


def test_readme_table_is_current() -> None:
    from pathlib import Path

    from tests.measure import table

    readme = Path(__file__).parent.parent / "README.md"
    assert f"<!-- measure:start -->\n{table()}\n<!-- measure:end -->" in readme.read_text()
