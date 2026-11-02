"""Recognisers for names, companies, addresses, dates of birth, cards and accounts.

These are heuristics (patterns, a first-name list, context words), not language models. They
find less certain things than the checksum recognisers, so their confidence is lower. All four
languages are always active, because Swiss texts mix them.
"""

from __future__ import annotations

import re
from collections.abc import Iterator

from ._names import FIRST_NAMES
from .detectors import Candidate

_UP = "A-ZÄÖÜÉÈÀÂÊÎÔÛÇ"
_LO = "a-zäöüéèàâêîôûçñßø"
# One capitalised word, also hyphenated or with an apostrophe (Müller-Keller, D'Angelo, O'Brien).
_WORD = rf"[{_UP}][{_LO}]+(?:[-'’][{_UP}]?[{_LO}]+)*"
_PARTICLE = r"(?:von der|van der|von|van|de la|de|di|da|del|della|zu|le|la)"
_SURNAME = rf"(?:{_PARTICLE}[ ])?{_WORD}"


# --- persons -------------------------------------------------------------------------------

_TITLE = (
    r"(?:Hr\.|Herr|Herrn|Frau|Fr\.|Fräulein|Dr\.(?: med\.| iur\.| phil\.)?|Prof\.(?: Dr\.)?|"
    r"Mme|Madame|Mlle|Mademoiselle|Monsieur|Doktor|Professor|M\.|Mr\.?|Mrs\.?|Ms\.?|Miss|Dott\.|Avv\.|"
    r"(?i:signor|signora|signorina|sig\.ra|sig\.))"
)
_FIRST = "(?:" + "|".join(sorted(FIRST_NAMES, key=len, reverse=True)) + ")"
_TITLED = re.compile(rf"(?<![\w.])(?:{_TITLE}[ ]+)+(?:{_FIRST}[ ]+)?{_SURNAME}(?![\w])")
_FULL = re.compile(rf"(?<![\w]){_FIRST}(?:[ ]+{_FIRST})?[ ]+{_SURNAME}(?![\w])")
_SURNAME_FIRST = re.compile(rf"(?<![\w]){_SURNAME},[ ]+{_FIRST}(?![\w])")
_BARE_FIRST = re.compile(rf"(?<![\w]){_FIRST}(?![\w])")

# Capitalised words that are not surnames, so "Hans Anna" style false hits stay rare.
_NOT_SURNAME = frozenset(
    """
    Die Der Das Den Dem Des Ein Eine Und Oder Mit Von Für Bei Aus Auf An In Am Im Zu Zum Zur
    Le La Les Un Une Et Ou De Du Il Lo Gli Una The And Or For Of To At By AG GmbH SA Sàrl Sagl
    """.split()
)


def _last_word(text: str) -> str:
    return text.rsplit(" ", 1)[-1]


def persons(text: str) -> Iterator[Candidate]:
    found: list[tuple[int, int]] = []

    def hit(m: re.Match[str], confidence: float, detector: str) -> Candidate | None:
        if _last_word(m[0]) in _NOT_SURNAME:
            return None
        found.append(m.span())
        return Candidate("PERSON", m.start(), m.end(), confidence, detector)

    for pattern, confidence, detector in (
        (_TITLED, 0.9, "person-title"),
        (_FULL, 0.8, "person-firstname-surname"),
        (_SURNAME_FIRST, 0.7, "person-surname-firstname"),
    ):
        for m in pattern.finditer(text):
            if c := hit(m, confidence, detector):
                yield c

    # The same surname again without title or first name, and first names on their own.
    # shortcut: every later capitalised occurrence of a known surname counts, even when it is a
    # noun elsewhere; the confidence is low so you can filter it.
    surnames = {_last_word(text[s:e]) for s, e in found if "," not in text[s:e]}
    surnames |= {text[s:e].split(",")[0].split(" ")[-1] for s, e in found if "," in text[s:e]}
    if surnames:
        pattern = re.compile(rf"(?<![\w-])(?:{'|'.join(map(re.escape, surnames))})(?![\w-])")
        for m in pattern.finditer(text):
            if not any(s <= m.start() < e for s, e in found):
                yield Candidate("PERSON", m.start(), m.end(), 0.6, "person-surname-ref")
    for m in _BARE_FIRST.finditer(text):
        if not any(s <= m.start() < e for s, e in found):
            yield Candidate("PERSON", m.start(), m.end(), 0.45, "person-firstname")


# --- companies -----------------------------------------------------------------------------

_LEGAL = (
    r"(?:AG|GmbH|SA|SARL|Sàrl|S\.à r\.l\.|Sagl|KlG|KIG|SNC|KG|OHG|Ltd\.?|Inc\.?|LLC|"
    r"Genossenschaft|Stiftung)"
)
_ORG_WORD = rf"(?:{_WORD}|[A-ZÄÖÜ]{{2,}}|&|und|et|e|and)"
_ORG = re.compile(rf"(?<![\w])(?:{_ORG_WORD}[ ]+){{0,4}}?{_ORG_WORD}[ ]+{_LEGAL}(?![\w])")
_LEADING = frozenset(
    """
    Die Der Das Den Dem Des Ein Eine Und Oder Mit Von Für Bei Aus Auf An In Am Im Zu Zum Zur
    Le La Les Un Une Et Ou De Du Il Lo Gli Una The And Or For Of To At By Wir Ihre Ihr Unsere
    Rechnung Lieferant Firma Beleg Kunde Betreff Arbeitgeberin Arbeitgeber Mandant Mandantin
    Fournisseur Société Entreprise Fattura Fornitore Ditta Company Supplier Invoice
    """.split()
)


def organisations(text: str) -> Iterator[Candidate]:
    for m in _ORG.finditer(text):
        words = m[0].split(" ")
        skip = 0
        while skip < len(words) - 2 and (words[skip] in _LEADING or words[skip] in "&und et e and"):
            skip += 1
        # Drop a leading word that ends a sentence or a label ("Arbeitgeberin:" cannot match).
        value = " ".join(words[skip:])
        if len(value.split(" ")) < 2:
            continue
        start = m.end() - len(value)
        yield Candidate("ORG", start, m.end(), 0.85, "org-legal-form")


# --- addresses -----------------------------------------------------------------------------

_STREET_DE = (
    rf"{_WORD}(?:strasse|straße|str\.|weg|gasse|platz|allee|rain|hof|ring|quai|promenade|"
    rf"steig|matte|halde|egg|acker|graben|bühl)"
)
_STREET_ROMANCE = (
    rf"(?:Rue|Avenue|Av\.|Chemin|Ch\.|Route|Rte|Place|Boulevard|Bd|Quai|Impasse|Via|Viale|"
    rf"Piazza|Corso|Vicolo|Strada)[ ]+(?:(?:du|de la|de|des|della|dei|del|d')[ ]?)?{_WORD}"
    rf"(?:[ ]{_WORD})?"
)
_STREET = rf"(?:(?:{_WORD}[ ])?{_STREET_DE}|{_STREET_ROMANCE})[ ]+\d{{1,4}}[ ]?[a-zA-Z]?(?![\w])"
_STREET_EN = rf"\b\d{{1,4}}[ ]+{_WORD}[ ]+(?:Street|Road|Avenue|Lane|Square)\b"
_PLACE = rf"(?:(?:St\.|Ste\.|Sankt|Saint|Sainte|Le|La|Les|Bad)[ ]+)?{_WORD}(?:/{_WORD})?"
_PLZ = rf"(?:(?:CH|FL)[- ])?(?<![\d.])[1-9]\d{{3}}(?!\d)[ ]+{_PLACE}"
_ADDRESS = re.compile(rf"(?:{_STREET}|{_STREET_EN})(?:[,\n ]+{_PLZ})?")
_PLZ_ONLY = re.compile(_PLZ)
_ADDRESS_LEAD = re.compile(
    r"(?:^|\n|[,;]\s*|\b(?:in|nach|bei|aus|von|à|a|de|wohnhaft|domiziliert)\s+)$"
)
_PLZ_NUM = re.compile(r"(?<![\d.])[1-9]\d{3}(?!\d)")


def addresses(text: str) -> Iterator[Candidate]:
    taken: list[tuple[int, int]] = []
    for m in _ADDRESS.finditer(text):
        taken.append(m.span())
        full = bool(_PLZ_ONLY.search(m[0]))
        yield Candidate("ADDRESS", m.start(), m.end(), 0.95 if full else 0.8, "address-street")
    for m in _PLZ_ONLY.finditer(text):
        if any(s <= m.start() < e for s, e in taken):
            continue
        num = int(_PLZ_NUM.search(m[0])[0])  # type: ignore[index]
        # Years look like postcodes: without "CH-" or "PLZ" before it, 1900-2099 is not trusted.
        before = text[max(0, m.start() - 12) : m.start()]
        marked = m[0].startswith(("CH", "FL")) or re.search(r"PLZ[: ]*$", before)
        # Without a marker the postcode must stand where an address would: start of a line, after
        # a comma or after a preposition. "3000 Franken" and "1200 Meter" are not places.
        if not marked and not _ADDRESS_LEAD.search(before):
            continue
        if 1900 <= num <= 2099 and not marked:
            continue
        yield Candidate("ADDRESS", m.start(), m.end(), 0.75 if marked else 0.55, "address-postcode")


# --- dates of birth ------------------------------------------------------------------------

_MONTHS = (
    r"(?:Jan(?:uar|uary)?|Feb(?:ruar|ruary)?|März|Mär|Mar(?:ch)?|Apr(?:il)?|Mai|May|Jun[ie]?|Juli?|"
    r"Aug(?:ust)?|Sep(?:t|tember)?|Okt(?:ober)?|Oct(?:ober)?|Nov(?:ember|embre)?|Dez(?:ember)?|"
    r"Dec(?:ember)?|janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|"
    r"novembre|décembre|gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|"
    r"ottobre|dicembre)"
)
_DATE = (
    rf"(?:\d{{1,2}}[./-]\d{{1,2}}[./-](?:\d{{4}}|\d{{2}})(?!\d)|\d{{4}}-\d{{2}}-\d{{2}}|"
    rf"\d{{1,2}}\.?[ ]+{_MONTHS}\.?[ ]+\d{{4}})"
)
_DOB_CONTEXT = (
    r"(?:geb\.|geb\.-?datum|geboren|geburtsdatum|geburtstag|geburtsdat\.|né(?:e)?|née|"
    r"date de naissance|naissance|nato|nata|data di nascita|nascita|born|date of birth|birthday|"
    r"birth date|dob|d\.o\.b\.)"
)
_DOB = re.compile(
    rf"(?<![\w]){_DOB_CONTEXT}[ ]*(?:am|le|il|on|ist|is|est|è|:)?[ :]*(?P<d>{_DATE})", re.IGNORECASE
)


def birthdates(text: str) -> Iterator[Candidate]:
    for m in _DOB.finditer(text):
        yield Candidate("DOB", *m.span("d"), 0.9, "dob-context")


# --- cards and accounts --------------------------------------------------------------------


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, c in enumerate(reversed(digits)):
        n = int(c) * (2 if i % 2 else 1)
        total += n - 9 if n > 9 else n
    return total % 10 == 0


_CARD = re.compile(
    r"(?<!\d)(?<!\d )(?:\d{4}([ -]?)\d{4}\1\d{4}\1\d{4}(?:\1\d{3})?|\d{4}([ -])\d{6}\2\d{5})(?!\d)"
)


def cards(text: str) -> Iterator[Candidate]:
    for m in _CARD.finditer(text):
        digits = re.sub(r"\D", "", m[0])
        ok = luhn_ok(digits)
        yield Candidate("CARD", *m.span(), 0.95 if ok else 0.5, "card-luhn", ok)


_POSTAL = re.compile(r"(?<![\d-])\d{2}-\d{3,6}-\d(?![\d-])")
_TABLE = (0, 9, 4, 6, 8, 2, 7, 1, 3, 5)


def postal_ok(account: str) -> bool:
    """PostFinance account number: modulo 10 recursive over the zero-padded digits."""
    a, b, check = account.split("-")
    carry = 0
    for c in a + b.zfill(6):
        carry = _TABLE[(carry + int(c)) % 10]
    return (10 - carry) % 10 == int(check)


_ACCOUNT_CONTEXT = (
    r"(?:konto(?:nummer|-?nr\.?|nr\.?)?|kto\.?(?:-?nr\.?)?|compte(?:[ ]n°|[ ]no\.?)?|"
    r"conto(?:[ ]n\.|[ ]nr\.)?|account(?:[ ](?:no\.?|number|nr\.?))?)"
)
_ACCOUNT = re.compile(
    rf"(?<![\w]){_ACCOUNT_CONTEXT}[ ]*[:]?[ ]*(?P<n>\d[\d .\-/]{{4,22}}\d)(?![\d])", re.IGNORECASE
)


def accounts(text: str) -> Iterator[Candidate]:
    for m in _POSTAL.finditer(text):
        ok = postal_ok(m[0])
        yield Candidate("ACCOUNT", *m.span(), 0.9 if ok else 0.4, "account-postal-mod10", ok)
    for m in _ACCOUNT.finditer(text):
        yield Candidate("ACCOUNT", *m.span("n"), 0.8, "account-context")


DETECTORS = (persons, organisations, addresses, birthdates, cards, accounts)

# --- authorities (never replaced) ----------------------------------------------------------

AUTHORITY = re.compile(
    rf"(?<![\w])(?:(?:Kantonales?|Gemeinde|Eidgenössische[s]?|Bundes|Kantons)?[ ]?"
    rf"(?:Steueramt|Steuerverwaltung|Handelsregisteramt|Betreibungsamt|Konkursamt|Grundbuchamt|"
    rf"Zivilstandsamt|Strassenverkehrsamt|Migrationsamt|Ausgleichskasse|Sozialversicherungsanstalt|"
    rf"Bundesamt|Amt|Gemeindeverwaltung|Stadtverwaltung|Stadtkanzlei|Staatskanzlei|Obergericht|"
    rf"Bezirksgericht|Regionalgericht|Kantonsgericht|Bundesgericht|Verwaltungsgericht|"
    rf"Administration fiscale|Office des poursuites|Registre du commerce|Caisse de compensation|"
    rf"Ufficio imposte|Ufficio del registro|Cassa di compensazione|Tax Office|Tax Administration|"
    rf"Commercial Register)"
    rf"(?:[ ]+(?:(?:für|des|der|de|du|di|del|of)[ ]+)?{_PLACE}(?:[ ]+{_WORD})?)?)"
)
