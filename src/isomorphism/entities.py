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

_UP = "A-ZÄÖÜÉÈÀÂÊÎÔÛÇÑÁÍÓÚÝĆČŠŽĐŁŃŚŹŻŐŰĂŞŢĞİËÏŸŒÆÅØÃÕ"
_LO = "a-zäöüéèàâêîôûçñßøáíóúýćčšžđłńśźżőűăşţğıëïÿœæåãõ"
# One capitalised word, also hyphenated or with an apostrophe (Müller-Keller, D'Angelo, P'tits).
# Never starts inside a hyphen or apostrophe chain, so "Aa-Aa-Aa-…" is scanned once, not once
# per hyphen.
_WORD_CORE = rf"[{_UP}](?:[{_LO}]+|['’][{_UP}]?[{_LO}]+)(?:[-'’][{_UP}]?[{_LO}]+)*"
_WORD = rf"(?<![\w'’-]){_WORD_CORE}"
_PARTICLE = r"(?i:von der|van der|von|van|de la|de|di|da|del|della|dos|zu|le|la|ten|ter)"
_SURNAME = rf"(?:{_PARTICLE}[ ])?{_WORD}"
# An initial: "B.", "Th.", "J.-P."; not "St." (St. Gallen) or "Nr.".
_INITIAL = rf"(?<!z\. )(?<!z\.)(?<!u\. )(?<!d\. )(?!St\.|Nr\.|Ch\.)[{_UP}][{_LO}]?\.(?:-[{_UP}]\.)?"


# --- text written in capitals or without any ------------------------------------------------

_LETTERS = re.compile(rf"[{_UP}{_LO}]+(?:[-'’][{_UP}{_LO}]+)*")
_KEEP_UPPER = frozenset("AG SA KG KLG SNC GMBH SARL SAGL LTD INC LLC OHG CH FL".split())
_TITLES_LOWER = frozenset("frau herr herrn hr fr dr mme monsieur madame signora signor".split())
_TRADES_LOWER = re.compile(
    r"(?:garage|bäckerei|baeckerei|metzgerei|schreinerei|carrosserie|praxis)$"
)
# Lower-case words that are also first names, left alone in lower-case text ("max. 20").
_LOWER_NOT_NAMES = frozenset("max tom jan eva".split())
# A line counts as capitals (bank bookings, payment slips) or as lower case (chats).
_CAPS_SHARE = 0.6
_LOWER_SHARE = 0.8
_CHAT_PREFIX = re.compile(r"^\[[^\]\n]{1,30}\][^:\n]{1,40}:")
_LOWER_ADDRESS = re.compile(
    r"(?<![\w])(?P<street>[a-zäöüéèà]+(?:strasse|str\.|weg|gasse|platz))[ ]\d{1,4}[a-z]?,?[ ]+"
    r"[1-9]\d{3}[ ]+(?P<place>[a-zäöüéèà]+)"
)


def _capitalised(word: str) -> str:
    """Same length: lower case, then upper case at the start and after - or '."""
    out = []
    for i, c in enumerate(word):
        up = i == 0 or word[i - 1] in "-'’"
        x = c.upper() if up else c.lower()
        out.append(x if len(x) == 1 else c)
    return "".join(out)


def _is_name(word: str) -> bool:
    return all(_capitalised(part) in FIRST_NAMES for part in word.split("-"))


def _is_caps(words: list[re.Match[str]]) -> bool:
    upper = [m for m in words if m[0].isupper()]
    return (
        bool(words)
        and len(upper) / len(words) >= _CAPS_SHARE
        and any(len(m[0]) >= 4 for m in upper)
    )


def normalise(text: str) -> str:
    """The text with the case a recogniser expects, same length and positions.

    A line mostly in capitals ("HANS-PETER AEBERSOLD", "WERKSTRASSE 9") is written as a name
    would be ("Hans-Peter Aebersold"); legal forms stay as they are. In a line mostly in lower
    case ("hoi sandra, frau meier-huber fragt ..."), titles, known first names, trades and the
    word right after one of them get a capital; a chat line is judged after its sender. A street
    with number, postcode and place in lower case gets capitals in any line.
    """
    out = list(text)
    pos = 0
    for line in text.split("\n"):
        words = [m for m in _LETTERS.finditer(line) if len(m[0]) >= 2]
        if _is_caps(words):
            for m in words:
                if m[0].isupper() and m[0] not in _KEEP_UPPER:
                    out[pos + m.start() : pos + m.end()] = _capitalised(m[0])
            pos += len(line) + 1
            continue
        for m in _LOWER_ADDRESS.finditer(line):
            for g in ("street", "place"):
                out[pos + m.start(g) : pos + m.end(g)] = _capitalised(m[g])
        prefix = _CHAT_PREFIX.match(line)
        words = [m for m in words if not prefix or m.start() >= prefix.end()]
        lower = [m for m in words if m[0].islower()]
        if len(words) >= 4 and len(lower) / len(words) >= _LOWER_SHARE:
            mark_next = False
            for i, m in enumerate(words):
                w = m[0]
                if not w.islower() or w in _LOWER_NOT_NAMES:
                    mark_next = False
                    continue
                gap = line[words[i - 1].end() : m.start()] if i else ""
                follows = mark_next and gap.strip() in ("", ".")
                if w in _TITLES_LOWER or _is_name(w) or _TRADES_LOWER.match(w):
                    mark_next = True
                elif follows:
                    mark_next = False
                else:
                    mark_next = False
                    continue
                out[pos + m.start() : pos + m.end()] = _capitalised(w)
        pos += len(line) + 1
    return "".join(out)


def caps_lines(text: str) -> bytearray:
    """1 for every character in a line that normalise() reads as capitals."""
    mask, pos = bytearray(len(text)), 0
    for line in text.split("\n"):
        if _is_caps([m for m in _LETTERS.finditer(line) if len(m[0]) >= 2]):
            mask[pos : pos + len(line)] = b"\x01" * len(line)
        pos += len(line) + 1
    return mask


# --- persons -------------------------------------------------------------------------------

_TITLE = (
    r"(?:Hr\.|Herr|Herrn|Frau|Fr\.|Fräulein|"
    r"Dr\.(?: (?:med|iur|phil|oec|dent|vet|sc|rer\. nat|h\.c)\.)*|"
    r"Prof\.(?: Dr\.)?|lic\. iur\.|Mme|Madame|Mlle|Mademoiselle|Monsieur|Me|Doktor|Professor|"
    r"M\.|Mr\.?|Mrs\.?|Ms\.?|Miss|Dott\.(?:ssa)?|Ing\.|Notar(?:in)?|Fam\.|Familie|Famille|"
    r"(?i:signor|signora|signorina|sig\.ra|sig\.|avv\.))"
)
_FIRST1 = "(?:" + "|".join(sorted(FIRST_NAMES, key=len, reverse=True)) + ")"
# A double first name needs one known half: "Anne-Marie", "Rose-Marie", "Pierre-Alain".
_FIRST = rf"(?:{_FIRST1}(?:-[{_UP}][{_LO}]+)?|[{_UP}][{_LO}]+-{_FIRST1})(?![\w-])"
# Up to two name words (particles do not count): "Dos Santos", "Ferreira da Silva".
_NAME2 = rf"(?:{_INITIAL}[ ]?)*{_SURNAME}(?:[ ]+{_SURNAME})?"
_TITLED = re.compile(
    rf"(?<![\w.])(?:{_TITLE}[ ]+)+(?:{_FIRST}[ ]+{_SURNAME}[ ]+{_SURNAME}|{_NAME2})(?![\w])"
)
# Surname and first name without comma, at the end of an entry: "Krasniqi Arben, geb. ...".
_SURNAME_FIRST_BARE = re.compile(rf"(?<![\w]){_WORD}[ ]+{_FIRST}(?=[ ]*(?:[,;:\n]|$))")
# A second surname only right before punctuation or "und": "Elina Pereira Gonçalves (2021)".
_FULL = re.compile(
    rf"(?<![\w]){_FIRST}(?:[ ]+{_FIRST})?[ ]+{_SURNAME}"
    rf"(?:[ ]+{_SURNAME}(?=[ ]*(?:[,.;:()\n]|$|[ ](?:und|et|e|and)[ ])))?(?![\w])"
)
_SURNAME_FIRST = re.compile(rf"(?<![\w]){_SURNAME},[ ]+{_FIRST}")
_INITIALS = re.compile(rf"(?<![\w.]){_INITIAL}[ ]?{_SURNAME}(?![\w])")
_BARE_FIRST = re.compile(rf"(?<![\w-]){_FIRST}")

# Words after which a name follows: labels on forms and bank bookings, relations, greetings.
_CONTEXT = (
    r"(?:(?i:arbeitnehmer(?:in)?|mitarbeiter(?:in)?|vermieter(?:in)?|mieter(?:in)?|locataire|"
    r"bailleur|steuerpflichtige[r]?|contribuable|contribuente|zahlbar durch|payable par|"
    r"pagabile da|auftraggeber(?:in)?|begünstigte[r]?|empfänger(?:in)?|kontoinhaber(?:in)?|"
    r"inhaber(?:in)?|unterschrift|sachbearbeiter(?:in)?|ansprechpartner(?:in)?|ansprechperson|"
    r"kontaktperson|gutschrift(?: von)?|lastschrift|zahlung (?:an|von)|"
    r"(?:sepa )?(?:ü|ue)berweisung (?:an|von)|zahlungseingang(?: von)?|"
    r"einzahlung von|e-banking auftrag|twint|"
    r"c/o|name|vorname|nom|prénom|nome|cognome|tochter|sohn|ehemann|ehefrau|gattin|gatte|"
    r"lebenspartner(?:in)?|mein mann|meine frau|my wife|my husband|mon mari|ma femme|"
    r"mio marito|mia moglie|figlia|figlio|fille|fils|daughter|son|erbe|erbin|liebe[r]?|hallo|"
    r"hoi|sali|salü|grüezi|guten tag|hi|hello|dear|cher|chère|bonjour|salut|caro|cara|ciao|"
    r"gentile|lg|betreffend|betrifft)(?:[ ]*:[ ]*|[ ]+|[ ]*\n))"
)
_IN_CONTEXT = re.compile(rf"(?<![\w]){_CONTEXT}(?P<n>{_NAME2})(?![\w])")
# The name under a closing formula, on its own line.
_SIGNED = re.compile(
    r"(?i:grüsse|grüße|gruss|grüessli|saluti|salutations distinguées|regards|thanks|best|"
    r"cheers|merci|danke|cordialement|sincerely)[ ,.!]*\n(?:[ ]*\n)*"
    rf"(?P<n>{_NAME2})[ ]*(?=\n|,|$)"
)
_COPY = re.compile(r"(?m)^(?:CC|Cc|cc|Kopie(?: an)?|Copie|Copia|Verteiler)[ ]*:[ ]*(?P<rest>.*)$")
_COPY_ITEM = re.compile(rf"(?:^|,[ ]*)(?P<n>(?:{_TITLE}[ ]+)*{_NAME2})(?=[ ]*(?:,|$|[ ]{_WORD}?))")
# Two name words, a title, or a known first name: "und Buchhalterin" is not a name.
_AND = re.compile(
    rf"[ ]+(?:und|et|e|and|&)[ ]+(?P<n>(?:{_TITLE}[ ]+)+{_NAME2}|{_FIRST}|"
    rf"(?:{_INITIAL}[ ]?)*{_SURNAME}[ ]+{_SURNAME})(?![\w])"
)

# Capitalised words that are not surnames, so "Hans Anna" style false hits stay rare.
_NOT_SURNAME = frozenset(
    """
    Die Der Das Den Dem Des Ein Eine Und Oder Mit Von Für Bei Aus Auf An In Am Im Zu Zum Zur
    Le La Les Un Une Et Ou De Du Il Lo Gli Una The And Or For Of To At By AG GmbH SA Sàrl Sagl
    Tax Tout-le-Monde Jedermann Zusammen Alle Team Damen Herren Mesdames Messieurs Signori
    Everyone All Sir Madam Kunde Kundin Mandant Mandantin Liebe Lieber Mitglieder Kolleginnen
    Kollegen Freunde Eltern Kunden Kundinnen Mitarbeitende Anwesende Teilnehmende Gäste Leser
    Leserinnen Sie Ihr Ihre Ihrer Ihrem Ihren Zahlung Bezug Miete Rechnung Lohn Spesen Akonto
    Januar Februar März April Juni Juli September Oktober November Dezember
    """.split()
)


def _words(value: str) -> list[str]:
    return value.split(" ")


def persons(text: str) -> Iterator[Candidate]:
    text = normalise(text)
    found: list[tuple[int, int]] = []
    reusable: list[tuple[int, int]] = []
    covered = bytearray(len(text))  # 1 where a person was found, for O(1) lookups
    # Words of an authority ("Gemeinde Wil") are reported (core drops them) but never reused.
    official = bytearray(len(text))
    for a in AUTHORITY.finditer(text):
        official[a.start() : a.end()] = b"\x01" * (a.end() - a.start())

    def hit(start: int, end: int, confidence: float, detector: str) -> Candidate | None:
        # Cut at the first word that is not a name ("Frau Meier Die ...", "Dr. Tax Update").
        words = _words(text[start:end])
        cut = next((i for i, w in enumerate(words) if w in _NOT_SURNAME), len(words))
        value = " ".join(words[:cut])
        # At least one word that is neither a title nor an initial ("Nouvel An." is not a name).
        if not any(
            len(w) > 1 and not w.endswith(".") and not re.fullmatch(_TITLE, w)
            for w in value.split(" ")
        ):
            return None
        end = start + len(value)
        found.append((start, end))
        covered[start:end] = b"\x01" * (end - start)
        if confidence >= 0.65 and not any(official[start:end]):
            reusable.append((start, end))
        return Candidate("PERSON", start, end, confidence, detector)

    for pattern, confidence, detector in (
        (_TITLED, 0.9, "person-title"),
        (_FULL, 0.8, "person-firstname-surname"),
        (_SURNAME_FIRST, 0.7, "person-surname-firstname"),
        (_INITIALS, 0.7, "person-initial"),
        (_SURNAME_FIRST_BARE, 0.6, "person-surname-firstname"),
    ):
        for m in pattern.finditer(text):
            if c := hit(m.start(), m.end(), confidence, detector):
                yield c
    for pattern, detector in ((_IN_CONTEXT, "person-context"), (_SIGNED, "person-signature")):
        for m in pattern.finditer(text):
            if c := hit(*m.span("n"), 0.65, detector):
                yield c
    for m in _COPY.finditer(text):
        for item in _COPY_ITEM.finditer(m["rest"]):
            if c := hit(
                m.start("rest") + item.start("n"),
                m.start("rest") + item.end("n"),
                0.65,
                "person-copy",
            ):
                yield c
    # "Gashi Fatmire und Gashi Besnik": the name after "und" next to a name.
    for _, e in list(found):
        if (nxt := _AND.match(text, e)) and (c := hit(*nxt.span("n"), 0.6, "person-and")):
            yield c

    # Every name word of a person found above, again on its own later ("Horvat", "Priya"), also
    # with a particle in front ("de Oliveira").
    # shortcut: every capitalised occurrence counts, even when the word is a noun elsewhere; the
    # confidence is low so you can filter it.
    names = set()
    for s, e in reusable:
        for w in re.split(r"[ ,]+", text[s:e]):
            if (
                len(w) > 2
                and not w.endswith(".")
                and w not in _NOT_SURNAME
                and not re.fullmatch(_TITLE, w)
                and not re.fullmatch(_PARTICLE, w)
            ):
                names.add(w)
    if names:
        words = "|".join(map(re.escape, sorted(names, key=len, reverse=True)))
        pattern = re.compile(rf"(?<![\w-])(?:{_PARTICLE}[ ])?(?:{words})(?![\w-])")
        for m in pattern.finditer(text):
            if not covered[m.start()] and not any(official[m.start() : m.end()]):
                yield Candidate("PERSON", m.start(), m.end(), 0.6, "person-surname-ref")
    for m in _BARE_FIRST.finditer(text):
        if not covered[m.start()]:
            yield Candidate("PERSON", m.start(), m.end(), 0.45, "person-firstname")


# --- companies -----------------------------------------------------------------------------

_LEGAL = (
    r"(?:AG|GmbH|GMBH|SA|SARL|Sàrl|S\.à r\.l\.|Sagl|SAGL|KlG|KIG|KLG|SNC|KG|OHG|Ltd\.?|LTD|"
    r"Inc\.?|INC|LLC|"
    r"Genossenschaft|Stiftung|& Cie\.?(?: (?:AG|SA))?)"
)
_ORG_WORD = rf"(?:{_WORD}-?|[A-ZÄÖÜ]{{2,}}|&|Co\.|und|et|e|and|du|de|des|della|di|del|dei|von)"
_ORG = re.compile(rf"(?<![\w])(?:{_ORG_WORD}[ ]+){{0,4}}?{_ORG_WORD}[ ]+{_LEGAL}(?![\w])")
# Legal form in front: "Verein Tierhilfe Zürcher Oberland", "Wohnbaugenossenschaft Sonnenhalde".
_ORG_FIRST = re.compile(
    rf"(?<![\w])(?:Verein|Genossenschaft|Stiftung|Association|Fondation|Coopérative|"
    rf"Associazione|Fondazione|Cooperativa|{_WORD}(?:genossenschaft|verein|stiftung))"
    rf"(?:[ ]+(?:{_WORD}|für|de|du|des|di|per)){{1,3}}(?<![ ])(?![\w])"
)
# A trade or institution and a name: "Bäckerei Lüthi", "la crèche Les P'tits Loups",
# "Zahnarztpraxis am Marktplatz", "Notariat Zumstein & Partner", "Bank Emmental".
_TRADE = (
    r"(?i:b(?:ä|ae)ckerei|metzgerei|schreinerei|zimmerei|malerei|g(?:ä|ae)rtnerei|druckerei|"
    r"carrosserie|garage|restaurant|ristorante|pizzeria|hotel|café|coiffeur|coiffure|kita|"
    r"krippe|crèche|apotheke|pharmacie|farmacia|boulangerie|atelier|kiosk|notariat|advokatur|"
    r"kanzlei|bestattungen|bank|banque|banca|versicherung(?:en)?|pensionskasse|krankenkasse|"
    r"caisse|cassa|treuhand(?:büro)?|fiduciaire|fiduciaria|architekturbüro|ingenieurbüro|"
    r"fahrschule|physiotherapie|reinigung|transporte|"
    rf"[{_UP}][{_LO}]+(?:praxis|erei|kasse|bank))"
)
_PARTNERS = rf"(?:[ ]+&[ ]+(?:{_WORD}|Co\.|Cie\.?))?"
_ORG_TRADE = re.compile(
    rf"(?<![\w]){_TRADE}"
    rf"(?:[ ]+(?:Les|Le|La|Il|Da|Zum|Zur|am|im|zum|zur|an der)(?:[ ]+{_WORD}){{1,2}}|[ ]+{_WORD})"
    rf"{_PARTNERS}(?![\w])"
)
_ARTICLES = frozenset("Les Le La Il Da Zum Zur".split())
# The name first: "Gashi Gipserei", "Müller Schreinerei".
_ORG_TRADE_AFTER = re.compile(rf"(?<![\w]){_WORD}[ ]+[{_UP}][{_LO}]+erei(?![\w])")
_LEADING = frozenset(
    """
    Die Der Das Den Dem Des Ein Eine Und Oder Mit Von Für Bei Aus Auf An In Am Im Zu Zum Zur
    Le La Les Un Une Et Ou De Du Il Lo Gli Una The And Or For Of To At By Wir Ihre Ihr Unsere
    Rechnung Lieferant Firma Beleg Kunde Betreff Arbeitgeberin Arbeitgeber Mandant Mandantin
    Fournisseur Société Entreprise Fattura Fornitore Ditta Company Supplier Invoice
    """.split()
)


def organisations(text: str) -> Iterator[Candidate]:
    text = normalise(text)
    for m in _ORG.finditer(text):
        words = m[0].split(" ")
        skip = 0
        while skip < len(words) - 2 and (
            words[skip] in _LEADING
            or words[skip] in "& und et e and du de des della di del dei von"
        ):
            skip += 1
        # Drop a leading word that ends a sentence or a label ("Arbeitgeberin:" cannot match).
        value = " ".join(words[skip:])
        if len(value.split(" ")) < 2:
            continue
        start = m.end() - len(value)
        yield Candidate("ORG", start, m.end(), 0.85, "org-legal-form")
    for pattern, confidence, detector in (
        (_ORG_FIRST, 0.75, "org-legal-form-first"),
        (_ORG_TRADE, 0.6, "org-trade"),
        (_ORG_TRADE_AFTER, 0.6, "org-trade"),
    ):
        for m in pattern.finditer(text):
            words = m[0].split(" ")
            if pattern is _ORG_TRADE_AFTER and (
                words[0] in _NOT_SURNAME or re.fullmatch(_TRADE, words[0])
            ):
                continue
            if not any(w in _NOT_SURNAME and w not in _ARTICLES for w in words[1:]):
                yield Candidate("ORG", m.start(), m.end(), confidence, detector)


# --- addresses -----------------------------------------------------------------------------

_STREET_DE = (
    rf"{_WORD}(?:strasse|straße|str\.|weg|gasse|platz|allee|rain|hof|ring|quai|promenade|"
    rf"steig|matte|halde|egg|acker|graben|bühl|pl\.)"
)
_STREET_ROMANCE = (
    rf"(?:Rue|Avenue|Av\.|Chemin|Ch\.|Route|Rte|Place|Pl\.|Boulevard|Bd|Quai|Impasse|Via|V\.|"
    rf"Viale|V\.le|Piazza|P\.za|Corso|Vicolo|Strada|Salita)[ ]+"
    rf"(?:(?:du|de la|de|des|à la|au|aux|della|dei|degli|delle|del|dal|ai|al|alla|alle|agli|"
    rf"sul|sulla)[ ]|(?:de l|d|dell|dall|all|sull|nell)['’])?(?:[{_UP}]\.[ ])?"
    # After an elided article the word follows the apostrophe: "Rue d'Italie", "de l'Hôpital".
    rf"(?:(?<=['’]){_WORD_CORE}|{_WORD})(?:[ ]{_WORD})?"
)
_NUMBER = r"[ ]{1,2}\d{1,4}(?:-\d{1,4})?[ ]?[a-zA-Z]?(?![\w])"
_STREET = rf"(?:(?:{_WORD}[ ])?{_STREET_DE}|{_STREET_ROMANCE}){_NUMBER}"
_STREET_EN = rf"\b\d{{1,4}}[ ]+{_WORD}[ ]+(?:Street|Road|Avenue|Lane|Square)\b"
_POBOX = r"(?:Postfach|Case postale|Casella postale|PO Box|P\.O\. Box)[ ]+\d{1,6}(?!\d)"
# Any words and a number, but only with postcode and place after it: "Im Grund 11, 8952 Schlieren".
_STREET_ANY = rf"(?:{_WORD}[ ]){{0,2}}{_WORD}{_NUMBER}"
_CANTON = (
    r"(?:AG|AI|AR|BE|BL|BS|FR|GE|GL|GR|JU|LU|NE|NW|OW|SG|SH|SO|SZ|TG|TI|UR|VD|VS|ZG|ZH)(?![\w])"
)
_PLACE = (
    rf"(?:(?:St\.|Ste\.|Sankt|Saint|Sainte|Le|La|Les|Bad)[ ]+)?{_WORD}(?:/{_WORD})?"
    rf"(?:[ ]+{_CANTON})?"
)
_PLZ = rf"(?:(?:CH|FL)[- ])?(?<![\d.])[1-9]\d{{3}}(?!\d)[ ]+{_PLACE}"
# Between street and postcode: comma, "|", "/", ";", tab or line break.
_SEP = r"(?:[ \t]*[,|/;][ \t]*\n?[ \t]*|[ \t]*\n[ \t]*|[ \t]+)"
_ADDRESS = re.compile(
    rf"(?:{_STREET}|{_STREET_EN}|{_POBOX})(?:{_SEP}{_PLZ})?|{_STREET_ANY}{_SEP}{_PLZ}"
)
_PLZ_ONLY = re.compile(_PLZ)
_ADDRESS_LEAD = re.compile(
    r"(?:^|\n|[,;|/\t]\s*|\b(?:in|nach|bei|aus|von|à|a|de|wohnhaft|domiziliert)\s+|"
    r"\b(?i:wohnsitz|domizil|wohnort|adresse|domicile|domicilio|indirizzo)[ ]*:[ ]*|"
    r"\b(?:AG|GmbH|GMBH|SA|Sàrl|Sagl)\s+)$"
)
_PLZ_NUM = re.compile(r"(?<![\d.])[1-9]\d{3}(?!\d)")
# A line that starts with a number of four or more digits and a word, as in a chart of accounts
# ("1000 Kasse"). A phone number ("0041 44 ...") is not such a line.
_NUMBERED_LINE = re.compile(r"[ \t]*\d{4,}[ \t]+[^\W\d_]")


def _in_numbered_list(text: str, line_start: int) -> bool:
    """True when the line at `line_start` sits in a chart of accounts or a price list: the line
    directly before or after it starts with a number and a word, and so does at least one more of
    the two lines before and the two after. An address block has at most one such neighbour, and
    a list of names with a place line each never has a numbered line next to the place."""
    before: list[int] = []
    i = line_start
    for _ in range(2):
        if i == 0:
            break
        i = text.rfind("\n", 0, i - 1) + 1
        before.append(i)
    after: list[int] = []
    i = line_start
    for _ in range(2):
        i = text.find("\n", i)
        if i == -1:
            break
        i += 1
        after.append(i)
    numbered = [bool(_NUMBERED_LINE.match(text, j)) for j in (*before, *after)]
    adjacent = (before and numbered[0]) or (after and numbered[len(before)])
    return bool(adjacent) and sum(numbered) >= 2


def addresses(text: str) -> Iterator[Candidate]:
    capitals = caps_lines(text)
    text = normalise(text)
    taken = bytearray(len(text))
    for m in _ADDRESS.finditer(text):
        taken[m.start() : m.end()] = b"\x01" * (m.end() - m.start())
        full = bool(_PLZ_ONLY.search(m[0]))
        yield Candidate("ADDRESS", m.start(), m.end(), 0.95 if full else 0.8, "address-street")
    for m in _PLZ_ONLY.finditer(text):
        if taken[m.start()]:
            continue
        num = int(_PLZ_NUM.search(m[0])[0])  # type: ignore[index]
        # Years look like postcodes: without "CH-" or "PLZ" before it, 1900-2099 is not trusted.
        before = text[max(0, m.start() - 12) : m.start()]
        marked = m[0].startswith(("CH", "FL")) or re.search(r"PLZ[: ]*$", before)
        # Without a marker the postcode must stand where an address would: start of a line, after
        # a comma or after a preposition. "3000 Franken" and "1200 Meter" are not places.
        # In a booking line in capitals the postcode follows the name:
        # "KELLER HANS 8405 WINTERTHUR".
        in_caps = bool(capitals[m.start()])
        if not marked and not in_caps and not _ADDRESS_LEAD.search(before):
            continue
        i = m.start()
        while i and text[i - 1] in " \t":
            i -= 1
        if not marked and (i == 0 or text[i - 1] == "\n") and _in_numbered_list(text, i):
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
    rf"(?<![\w])(?:(?:Gemeinde|Stadt|Kanton|Commune|Ville|Canton|Comune|Città|Cantone)"
    rf"(?:[ ]+(?:de|di|du|des|of))?[ ]+{_PLACE}|"
    rf"(?:Kantonales?|Gemeinde|Eidgenössische[s]?|Bundes|Kantons)?[ ]?"
    rf"(?:Steueramt|Steuerverwaltung|Handelsregisteramt|Betreibungsamt|Konkursamt|Grundbuchamt|"
    rf"Zivilstandsamt|Strassenverkehrsamt|Migrationsamt|Ausgleichskasse|Sozialversicherungsanstalt|"
    rf"Bundesamt|Amt|Gemeindeverwaltung|Stadtverwaltung|Stadtkanzlei|Staatskanzlei|Obergericht|"
    rf"Bezirksgericht|Regionalgericht|Kantonsgericht|Bundesgericht|Verwaltungsgericht|"
    rf"Administration fiscale|Office des poursuites|Registre du commerce|Caisse de compensation|"
    rf"Ufficio imposte|Ufficio del registro|Cassa di compensazione|Tax Office|Tax Administration|"
    rf"Commercial Register)"
    rf"(?:[ ]+(?:(?:für|des|der|de|du|di|del|of)[ ]+)?{_PLACE}(?:[ ]+{_WORD})?)?)"
)
