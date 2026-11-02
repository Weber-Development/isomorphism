"""Invented Swiss texts with the expected hits marked inline as ⟦KIND|value⟧.

Everything here is made up. Names, street addresses and companies appear in the texts but are not
marked yet: those kinds arrive with the next version. Numbers with a wrong check digit are marked
too, because they must be found as well.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_MARK = re.compile(r"⟦([A-Z]+)\|([^⟧]*)⟧")


@dataclass(frozen=True)
class Case:
    name: str
    lang: str
    text: str  # without markup
    expected: frozenset[tuple[str, int, int]]  # kind, start, end


def _parse(name: str, lang: str, marked: str) -> Case:
    out, expected, pos = [], set(), 0
    for m in _MARK.finditer(marked):
        out.append(marked[pos : m.start()])
        start = sum(len(p) for p in out)
        out.append(m[2])
        expected.add((m[1], start, start + len(m[2])))
        pos = m.end()
    out.append(marked[pos:])
    return Case(name, lang, "".join(out), frozenset(expected))


_RAW = [
    (
        "lohnausweis",
        "de",
        """\
Lohnausweis 2025 (Auszug)
Arbeitnehmerin: ⟦PERSON|Anna Muster⟧, ⟦ADDRESS|Musterstrasse 12, 9000 St. Gallen⟧
Geburtsdatum: ⟦DOB|03.04.1981⟧, AHV-Nr.: ⟦AHV|756.5260.1815.91⟧
Arbeitgeberin: ⟦ORG|Beispiel Treuhand AG⟧, ⟦UID|CHE-937.865.795⟧ MWST
Bruttolohn 78'450.00, Nettolohn 66'918.40, Auszahlung auf ⟦IBAN|CH10 7971 1471 0497 4650 7⟧.
Rückfragen: Lohnbuchhaltung, ⟦PHONE|071 123 45 67⟧, ⟦EMAIL|lohn@beispiel-treuhand.example⟧
""",
    ),
    (
        "mandanten-mail",
        "de",
        """\
Grüezi ⟦PERSON|Frau Keller⟧

Wir haben die Unterlagen für die Steuererklärung erhalten. Meine Mobilnummer ist
⟦PHONE|+41 79 123 45 67⟧, erreichbar bin ich auch unter ⟦PHONE|079 123 45 67⟧.
Die Rückzahlung bitte auf ⟦IBAN|CH21 5291 7034 2366 7127 6⟧ überweisen.
Meine AHV-Nummer: ⟦AHV|756.0830.1661.38⟧ (die Nummer meines Mannes: ⟦AHV|756.1860.9139.07⟧).
Ich wohne seit 2020 an der ⟦ADDRESS|Bahnhofstrasse 5a, 8400 Winterthur⟧.
Freundliche Grüsse
⟦PERSON|Hans Muster⟧, ⟦EMAIL|hans.muster@mail.example⟧
""",
    ),
    (
        "beleg",
        "de",
        """\
Beleg 2025-0417, Rechnung Nr. 20250417, Referenz 21 00000 00003 13947 14300 09017
Lieferant: ⟦ORG|Muster Garage GmbH⟧, ⟦UID|CHE-754.323.198⟧ HR, ⟦UID|CHE-487.574.914⟧ MWST
Betrag CHF 1'234.50 inkl. 8.1% MWST, fällig am 30.11.2026
Zahlbar an ⟦IBAN|CH19 8426 8465 6321 2233 0⟧ (keine Barzahlung), Tel. ⟦PHONE|+41 (0)71 987 65 43⟧
Bezahlt mit Karte ⟦CARD|4111 1111 1111 1111⟧, PC-Konto ⟦ACCOUNT|80-12345-6⟧.
""",
    ),
    (
        "steuerrueckfrage",
        "de",
        """\
Betreff: Steuerrückfrage Veranlagung 2025
Das Steueramt St. Gallen fragt nach dem Beleg zu Kontonummer ⟦IBAN|CH67 7924 4026 8599 5289 0⟧.
Sehr geehrte ⟦PERSON|Frau Doktor Müller⟧, das Kantonale Steueramt Thurgau und das Handelsregisteramt Zürich erhalten eine Kopie.
Bitte melden Sie sich unter ⟦PHONE|058 123 45 67⟧ oder per Mail an ⟦EMAIL|steueramt.anfrage@kanton.example⟧.
Die AHV-Nummer ⟦AHV|756.9960.3082.41⟧ von ⟦PERSON|Herr Meier⟧ stimmt nicht mit den Unterlagen überein.
Sein Konto: ⟦ACCOUNT|1234 567890⟧. ⟦PERSON|Meier⟧ wohnt an der ⟦ADDRESS|Dorfstrasse 3⟧.
""",
    ),
    (
        "courrier",
        "fr",
        """\
Madame, Monsieur,
Veuillez trouver ci-joint le décompte pour ⟦PERSON|M. Jean Dupont⟧, n° AVS ⟦AHV|756.6281.9482.17⟧,
né le ⟦DOB|12 mars 1975⟧, domicilié ⟦ADDRESS|Rue de Lausanne 12, 1003 Lausanne⟧.
Le montant est à verser sur ⟦IBAN|CH35 7866 6617 6031 3721 5⟧. Numéro IDE: ⟦UID|CHE-186.252.760⟧ TVA.
Contact: ⟦PHONE|+41 21 123 45 67⟧ ou ⟦PHONE|021 123 45 67⟧, ⟦EMAIL|contact@fiduciaire.example⟧
Société: ⟦ORG|Dupont & Fils SA⟧. L'Administration fiscale cantonale a été informée.
""",
    ),
    (
        "lettera",
        "it",
        """\
Gentile ⟦PERSON|signora Bianchi⟧,
il suo numero AVS è ⟦AHV|756.9935.1819.09⟧, nata il ⟦DOB|15/06/1990⟧. Il pagamento va fatto sul conto ⟦IBAN|LI27 9010 9281 5901 3962 4⟧.
Numero IDI: ⟦UID|CHE-018.955.594⟧ IVA. Può chiamarci al ⟦PHONE|0041 91 123 45 67⟧ oppure scrivere a ⟦EMAIL|info@studio-fiduciario.example⟧.
Lo studio si trova in ⟦ADDRESS|Via Nassa 8, 6900 Lugano⟧. Il Ufficio imposte Ticino riceve una copia.
""",
    ),
    (
        "mail-en",
        "en",
        """\
Hi ⟦PERSON|Anna⟧,
please transfer the refund to ⟦IBAN|CH93 0076 2011 6238 5295 7⟧ (I cannot find my ⟦AHV|756.1234.5678.97⟧ card).
Our company is ⟦UID|CHE-123.456.788⟧; reach me on ⟦PHONE|+41 71 123 45 67⟧ or ⟦EMAIL|anna.muster@example.ch⟧.
My date of birth is ⟦DOB|1981-04-03⟧ and I live at ⟦ADDRESS|12 Baker Street⟧.
Card on file: ⟦CARD|5500 0000 0000 0004⟧, American Express ⟦CARD|3782 822463 10005⟧.
Regards, ⟦PERSON|Mr. Smith⟧ of ⟦ORG|Smith & Partners Ltd⟧
""",
    ),
    (
        "formate",
        "de",
        """\
Schreibweisen: ⟦AHV|7561234567897⟧, ⟦AHV|756 1234 5678 97⟧, ⟦IBAN|CH9300762011623852957⟧, ⟦IBAN|ch93 0076 2011 6238 5295 7⟧,
⟦UID|CHE123456788⟧, ⟦UID|CHE-123.456.788⟧, ⟦PHONE|0711234567⟧, ⟦PHONE|071/123 45 67⟧, ⟦PHONE|(071) 123 45 67⟧,
⟦PHONE|+41711234567⟧, ⟦PHONE|0041 71 123 45 67⟧, ⟦PHONE|071.123.45.67⟧
Karten: ⟦CARD|4111-1111-1111-1111⟧, ⟦CARD|4111111111111111⟧. Geburtstag: ⟦DOB|3. April 1981⟧, geb. ⟦DOB|3.4.81⟧.
Adresse mit Postleitzahl: ⟦ADDRESS|CH-9000 St. Gallen⟧
⟦ADDRESS|8400 Winterthur⟧
Firma in ⟦ADDRESS|6003 Luzern⟧
""",
    ),
    (
        "falsche-pruefziffer",
        "de",
        """\
Tippfehler müssen trotzdem gefunden werden:
AHV ⟦AHV|756.1234.5678.98⟧, IBAN ⟦IBAN|CH93 0076 2011 6238 5295 8⟧, UID ⟦UID|CHE-123.456.789⟧,
Karte ⟦CARD|4111 1111 1111 1112⟧, PC-Konto ⟦ACCOUNT|80-12345-7⟧.
""",
    ),
    (
        "keine-treffer",
        "de",
        """\
Rechnung 2026-1102, Kunde 756-20, Artikel 0711234, Menge 12 Stk. zu CHF 1'290.00.
Datum 03.04.1981, Zeit 08.30 Uhr, Seite 4 von 12, Version 3.13.1.
Tarif 5.2.0, Konto 1020, Debitoren 1100, Kreditoren 2000, Anzahl 12345678901.
Referenz 21 00000 00003 13947 14300 09017, Kontakt: siehe Impressum, Kapital 100'000.
Im Jahr 2025 Zahlungen erfasst. Ernte 2024 Weizen. Die Rechnung wurde bezahlt.
Das Steueramt St. Gallen und das Bundesamt für Statistik haben geantwortet.
Mit freundlichen Grüssen, Ihre Treuhand und die Verwaltung. Kapitel 3 Abschnitt 4.
Total 3000 Franken netto, 1200 Meter Kabel, 4500 Euro. Das ist ein Roman. Die Firma Meier und Söhne.
Nr. 8000 Zürich, 08:30 Uhr 9000 Besucher, Kapital 1000 Aktien.
""",
    ),
]

CASES = [_parse(*row) for row in _RAW]
