"""Blind acceptance set A for isomorphism 0.2 (PERSON / ORG / ADDRESS).

Written without reading src/ or tests/cases.py, as a Swiss fiduciary office
would write. Everything is invented. Markup: ⟦KIND|value⟧.

Conventions used here (decisions where the task left room):
- A title/salutation directly in front belongs to the PERSON span
  (Herr, Frau, Hr., Mme, M., Me, Dr., avv., Fam., Familie, Notar).
- A bare first name or bare surname that refers to a client is marked
  (pattern class "first name alone" / "surname alone"); each occurrence.
- ORG without legal form (Baeckerei Luethi, Les P'tits Loups) is marked;
  expected to be a documented miss class, but a fiduciary writes it this way.
- Addresses on two lines (QR bill, signature block) are marked as two spans:
  street+number and PLZ+place. Noted at the text.
- "PLZ + place" alone as domicile ("7130 Ilanz") is marked as ADDRESS.
  Place alone, Gemeinde X, Kanton X, streets without number are NOT marked.
- Authorities (Steueramt, Gemeinde, Kanton, Ausgleichskasse, ESTV,
  Steuerverwaltung) are never marked.
- No dates of birth, UID, card or account numbers in the set, so those
  kinds cannot produce noise. AHV, IBAN, PHONE, EMAIL are marked where
  present; AHV and IBAN check digits are valid.
"""

RAW = [
    # 1 Client email, de: double names, CC line, move within the year
    (
        "email_steuererklaerung_de",
        "de",
        "Guten Tag ⟦PERSON|Frau Brunner⟧\n"
        "\n"
        "Anbei die Unterlagen für die Steuererklärung 2025 von meinem Mann ⟦PERSON|Reto Kälin⟧ und mir. "
        "Die Lohnausweise der ⟦ORG|Elektro Zumbühl AG⟧ und der ⟦ORG|Kita Sunnehof GmbH⟧ sind dabei, "
        "die Krankenkassenprämien schicke ich nach.\n"
        "Wir sind per 1. Oktober an den ⟦ADDRESS|Birkenweg 7b, 6210 Sursee⟧ gezogen. "
        "Die alte Adresse war ⟦ADDRESS|Rue de la Gare 15, 1700 Fribourg⟧. Müssen wir zwei Steuererklärungen machen?\n"
        "\n"
        "Freundliche Grüsse\n"
        "⟦PERSON|Nadine Kälin-Steiner⟧\n"
        "\n"
        "CC: ⟦PERSON|Reto Kälin⟧\n",
    ),
    # 2 Lohnausweis excerpt, de: Albanian name, initial, valid AHV
    (
        "lohnausweis_de",
        "de",
        "Lohnausweis 2025\n"
        "Arbeitgeber: ⟦ORG|Schreinerei Bürgi & Söhne AG⟧, ⟦ADDRESS|Industriestrasse 22, 4900 Langenthal⟧\n"
        "Arbeitnehmer: ⟦PERSON|Muharrem Gashi⟧\n"
        "AHV-Nr.: ⟦AHV|756.3418.7296.02⟧\n"
        "Adresse: ⟦ADDRESS|Dorfstrasse 3, 4912 Aarwangen⟧\n"
        "Lohnperiode: 1.1.2025 bis 31.12.2025\n"
        "1. Lohn: 78'450.00\n"
        "8. Bruttolohn total: 78'450.00\n"
        "9. Beiträge AHV/IV/EO/ALV/NBUV: 5'020.80\n"
        "11. Nettolohn: 71'214.20\n"
        "Ort und Datum: Langenthal, 20.01.2026\n"
        "Unterschrift: ⟦PERSON|B. Bürgi⟧, Personalabteilung\n",
    ),
    # 3 Quittance de loyer, fr: abbreviated streets (Rte de, Ch. des), initials with hyphen, valid IBAN
    (
        "quittance_loyer_fr",
        "fr",
        "Quittance de loyer\n"
        "Bailleur: ⟦ORG|Régie Chappuis & Cie SA⟧, ⟦ADDRESS|Rte de Lausanne 48, 1020 Renens⟧\n"
        "Locataire: ⟦PERSON|Mme Aurélie Dos Santos⟧\n"
        "Objet: appartement de 3.5 pièces, ⟦ADDRESS|Ch. des Vignes 12, 1009 Pully⟧\n"
        "Loyer mensuel net: CHF 1'850.00, acompte de charges: CHF 180.00\n"
        "Période: janvier à décembre 2025, total payé: CHF 24'360.00\n"
        "Payé par virement sur l'IBAN ⟦IBAN|CH40 0483 5001 1223 3445 A⟧\n"
        "Renens, le 12 janvier 2026\n"
        "⟦PERSON|J.-P. Chappuis⟧, gérant\n",
    ),
    # 4 Spendenbestaetigung, de: Verein as legal form, authority unmarked
    (
        "spendenbestaetigung_de",
        "de",
        "Spendenbestätigung für die Steuerbehörden\n"
        "\n"
        "Hiermit bestätigen wir, dass ⟦PERSON|Herr Bruno Frei⟧ und ⟦PERSON|Frau Anne-Marie Frei-Gisler⟧, "
        "⟦ADDRESS|Haldenstrasse 19, 8620 Wetzikon⟧, dem ⟦ORG|Verein Tierhilfe Zürcher Oberland⟧ im Jahr 2025 "
        "Spenden von insgesamt CHF 1'200.00 zukommen liessen.\n"
        "Der Verein ist gemäss Verfügung des Kantonalen Steueramts Zürich wegen Gemeinnützigkeit von der Steuerpflicht befreit.\n"
        "\n"
        "Wetzikon, 20. Januar 2026\n"
        "⟦PERSON|Silvia Odermatt⟧, Kassierin\n",
    ),
    # 5 Kontoauszug Buchungstexte, de: surname first, abbreviated street, ALL CAPS, Gemeinde unmarked, Dr.
    (
        "kontoauszug_buchungen_de",
        "de",
        "Kontoauszug CHF, Konto Geschäft, November 2025\n"
        "03.11. Gutschrift ⟦PERSON|Frischknecht Hans⟧, ⟦ADDRESS|Bahnhofstr. 3, 9500 Wil SG⟧, Rechnung 2025-118  2'340.00\n"
        "04.11. Lastschrift ⟦ORG|Netzwerk Thurtal GmbH⟧, Abo Oktober  -89.90\n"
        "05.11. E-Banking Auftrag ⟦PERSON|ANANTHAN SIVAKUMAR⟧ ⟦ADDRESS|WEIERSTRASSE 8 8603 SCHWERZENBACH⟧ LOHN OKTOBER  -5'210.00\n"
        "06.11. Gutschrift Gemeinde Wil, Rückerstattung Hundesteuer  120.00\n"
        "07.11. Gutschrift ⟦PERSON|Dr. Patrizia Caflisch⟧, Honorar Beratung  450.00\n"
        "10.11. Dauerauftrag Miete ⟦ORG|Immobilien Rhyner AG⟧  -1'650.00\n"
        "12.11. TWINT ⟦PERSON|Lea Bieri⟧, Rückzahlung Spesen  -35.00\n"
        "14.11. Steuern Kanton St. Gallen, Akontozahlung 2025  -4'500.00\n",
    ),
    # 6 Handwritten-style notes, de: Fam., first name alone, Hr., surname alone, von, ORG without legal form
    (
        "notizen_montag_de",
        "de",
        "Notizen Montag\n"
        "- Termin mit ⟦PERSON|Fam. Gashi⟧ 14:00 wegen Quellensteuer, Tochter ⟦PERSON|Blerta⟧ kommt mit (übersetzt)\n"
        "- ⟦PERSON|Hr. Vonlanthen⟧ zurückrufen, ⟦PHONE|079 412 88 31⟧\n"
        "- Unterlagen ⟦ORG|Carrosserie Schüpbach GmbH⟧ noch nicht da, mahnen\n"
        "- Belege ⟦PERSON|Wyss⟧ ans Steueramt Thurgau weiterleiten, Frist 15.11.\n"
        "- MWST-Abrechnung Q3 ⟦ORG|Bäckerei Lüthi⟧, Saldosteuersatz prüfen\n"
        "- ⟦PERSON|Frau von Arx⟧ will Termin verschieben, Dr. Tax Update vorher installieren\n",
    ),
    # 7 Client email, it: Signor, Sagl, V. abbreviation, avv. title, CC
    (
        "email_cliente_it",
        "it",
        "Gentile ⟦PERSON|Signor Bernasconi⟧\n"
        "\n"
        "Le invio la fattura della ⟦ORG|Impresa Edile Ferrari Sagl⟧ per i lavori di risanamento dello stabile in "
        "⟦ADDRESS|Via Cantonale 56, 6512 Giubiasco⟧. Mio marito ⟦PERSON|Luca Pedrazzini⟧ ha già pagato l'acconto a settembre. "
        "Può dirmi se la deduzione per la manutenzione è possibile per il 2025?\n"
        "Il nostro nuovo indirizzo dal 1° novembre: ⟦ADDRESS|V. Lugano 8, 6900 Massagno⟧.\n"
        "\n"
        "Cordiali saluti\n"
        "⟦PERSON|Chiara Pedrazzini-Rossi⟧\n"
        "\n"
        "Cc: ⟦PERSON|Luca Pedrazzini⟧, ⟦PERSON|avv. Marco Bianchi⟧\n",
    ),
    # 8 Expat email, en: first name alone, Tamil names, house number with letter
    (
        "expat_email_en",
        "en",
        "Hi ⟦PERSON|Sandra⟧,\n"
        "\n"
        "Quick question about my 2025 return. I moved from ⟦ADDRESS|Seefeldstrasse 112, 8008 Zürich⟧ to "
        "⟦ADDRESS|Zugerstrasse 5a, 6340 Baar⟧ in July. My employer, ⟦ORG|Helvetic Data Systems AG⟧, paid a relocation "
        "allowance of CHF 8,000 which shows up on the Lohnausweis. My wife ⟦PERSON|Priya Raghunathan⟧ started working for "
        "⟦ORG|Zuger Physio GmbH⟧ in September. Does she need a separate declaration, or is it one for both of us?\n"
        "\n"
        "Thanks,\n"
        "⟦PERSON|Arjun Raghunathan⟧\n"
        "Sent from my iPhone\n",
    ),
    # 9 Invoice, de: Postfach, Herrn, c/o, initial, ORG repeated, property address
    (
        "rechnung_treuhand_de",
        "de",
        "⟦ORG|Treuhand Bösch & Partner AG⟧\n"
        "⟦ADDRESS|Postfach 248, 9001 St. Gallen⟧\n"
        "\n"
        "Rechnung Nr. 2026-0042\n"
        "An: ⟦PERSON|Herrn Dieter Oberholzer⟧\n"
        "c/o ⟦ORG|Oberholzer Metallbau GmbH⟧\n"
        "⟦ADDRESS|Gewerbestrasse 14, 9230 Flawil⟧\n"
        "\n"
        "Leistung: Steuererklärung 2025 natürliche Person; Beratung Liegenschaft ⟦ADDRESS|Rosenbergstrasse 2, 9000 St. Gallen⟧\n"
        "Honorar: CHF 1'450.00\n"
        "MWST 8.1 %: CHF 117.45\n"
        "Total: CHF 1'567.45\n"
        "Zahlbar innert 30 Tagen auf IBAN ⟦IBAN|CH96 0023 0000 A109 2345 6⟧, lautend auf ⟦ORG|Treuhand Bösch & Partner AG⟧.\n"
        "Sachbearbeiterin: ⟦PERSON|M. Bösch⟧\n",
    ),
    # 10 Steuerrueckfrage from the tax office, de: surname-first pairs, authority unmarked, Art./§ references
    (
        "steuerrueckfrage_de",
        "de",
        "Kantonales Steueramt Zürich, Dienstabteilung Veranlagung\n"
        "\n"
        "Steuerpflichtige: ⟦PERSON|Gashi Fatmire⟧ und ⟦PERSON|Gashi Besnik⟧, ⟦ADDRESS|Im Grund 11, 8952 Schlieren⟧\n"
        "Steuerperiode 2024\n"
        "\n"
        "Sehr geehrte Damen und Herren\n"
        "Zur Prüfung der Steuererklärung bitten wir Sie um folgende Unterlagen:\n"
        "1. Mietvertrag für die Wohnung an der ⟦ADDRESS|Badenerstrasse 310, 8004 Zürich⟧ (Untervermietung)\n"
        "2. Belege zu den Unterhaltszahlungen an ⟦PERSON|Frau Lindita Berisha⟧, ⟦ADDRESS|Rue du Midi 7, 1003 Lausanne⟧\n"
        "3. Bestätigung der Ausgleichskasse des Kantons Zürich über die Beiträge als Nichterwerbstätiger\n"
        "4. Lohnausweis der ⟦ORG|Reinigung Blitzblank GmbH⟧\n"
        "Frist: 30 Tage gemäss Art. 126 DBG und § 135 StG.\n"
        "\n"
        "Freundliche Grüsse\n"
        "⟦PERSON|R. Hürlimann⟧, Steuerkommissär\n",
    ),
    # 11 WhatsApp-style message, de: all lowercase
    (
        "whatsapp_de",
        "de",
        "hoi ⟦PERSON|sandra⟧, hast du die belege von ⟦PERSON|reto kälin⟧ schon bekommen? er hat gesagt er schickt sie dir direkt. "
        "und ⟦PERSON|frau meier-huber⟧ fragt wegen dem termin am freitag. die adresse vom neuen mandanten ist "
        "⟦ADDRESS|hauptstrasse 44, 5000 aarau⟧. lg ⟦PERSON|dani⟧",
    ),
    # 12 Letter to the tax office, fr: M./Mme/Me, Sàrl, ORG without legal form, signature block with address on two lines
    #    (address of the signature marked as two spans: street+number, PLZ+place)
    (
        "lettre_justificatifs_fr",
        "fr",
        "Madame, Monsieur,\n"
        "\n"
        "Suite à votre courrier du 3 novembre, je vous transmets les justificatifs demandés pour "
        "⟦PERSON|M. Yannick Dubois-Mercier⟧ et ⟦PERSON|Mme Solange Dubois⟧, domiciliés ⟦ADDRESS|Avenue de Beaulieu 23, 1004 Lausanne⟧.\n"
        "Le certificat de salaire de ⟦ORG|Menuiserie Rochat Sàrl⟧ ainsi que l'attestation de ⟦ORG|Fiduciaire du Léman SA⟧ "
        "sont en annexe. Les frais de garde concernent la crèche ⟦ORG|Les P'tits Loups⟧ à Pully.\n"
        "\n"
        "Veuillez agréer, Madame, Monsieur, mes salutations distinguées.\n"
        "\n"
        "⟦PERSON|Céline Favre⟧\n"
        "⟦ORG|Fiduciaire du Léman SA⟧\n"
        "⟦ADDRESS|Rte de Genève 102⟧\n"
        "⟦ADDRESS|1226 Thônex⟧\n"
        "Tél. ⟦PHONE|022 348 71 90⟧\n"
        "\n"
        "Copie: ⟦PERSON|Me Olivier Grandjean⟧, avocat\n",
    ),
    # 13 QR bill payment part, de: ALL CAPS, addresses on two lines (two spans each), surname alone, valid IBAN
    (
        "qr_rechnung_zahlteil_de",
        "de",
        "Zahlteil\n"
        "Konto / Zahlbar an\n"
        "⟦IBAN|CH63 0900 0000 1340 2245 7⟧\n"
        "⟦ORG|HEIZUNG FORSTER AG⟧\n"
        "⟦ADDRESS|WERKSTRASSE 9⟧\n"
        "⟦ADDRESS|3600 THUN⟧\n"
        "\n"
        "Zahlbar durch\n"
        "⟦PERSON|HANS-PETER AEBERSOLD⟧\n"
        "⟦ADDRESS|ALPENBLICK 27⟧\n"
        "⟦ADDRESS|3612 STEFFISBURG⟧\n"
        "\n"
        "Währung CHF   Betrag 2'486.70\n"
        "Zusätzliche Informationen\n"
        "Rechnung 4711, Service Heizung ⟦PERSON|Aebersold⟧, Oktober 2025\n",
    ),
    # 14 Mietvertrag, de: Genossenschaft, Serbian names with diacritics, initials
    (
        "mietvertrag_de",
        "de",
        "Mietvertrag für Wohnräume\n"
        "\n"
        "Vermieterin: ⟦ORG|Wohnbaugenossenschaft Sonnenhalde⟧, vertreten durch ⟦ORG|Keller Immobilien AG⟧, ⟦ADDRESS|Marktgasse 18, 3011 Bern⟧\n"
        "Mieter: ⟦PERSON|Herr Dragan Jovanović⟧ und ⟦PERSON|Frau Milica Jovanović⟧\n"
        "Mietobjekt: 4-Zimmer-Wohnung im 2. OG, ⟦ADDRESS|Sonnenhaldenstrasse 31, 3098 Köniz⟧, inkl. Kellerabteil Nr. 12 und Parkplatz Nr. 4\n"
        "Mietbeginn: 1. April 2025\n"
        "Nettomietzins: CHF 1'920.00 pro Monat, Nebenkosten akonto CHF 230.00\n"
        "Mietzinsdepot: CHF 5'760.00 auf ein Sperrkonto, zinstragend\n"
        "Kündigungsfrist: 3 Monate auf Ende März, Juni und September\n"
        "\n"
        "Bern, 15. März 2025\n"
        "Die Vermieterin: ⟦PERSON|Th. Keller⟧    Die Mieter: ⟦PERSON|D. Jovanović⟧, ⟦PERSON|M. Jovanović⟧\n",
    ),
    # 15 Look-alikes only, de: nothing to mark
    (
        "lookalikes_de",
        "de",
        "Sitzungsnotiz Weiterbildung\n"
        "\n"
        "Am Kurs «Steuerrecht für Treuhänder» vom 12. März ging es um Art. 33 DBG und Ziff. 2.1 der Wegleitung. "
        "Die Gemeinde Wil und der Kanton St. Gallen haben die Einreichefristen bis Ende Mai verlängert, "
        "das Steueramt der Stadt Zürich bis Ende Juni. Das Update von Dr. Tax 2026 ist seit Montag verfügbar, "
        "ebenso die neue Version des Lohnprogramms.\n"
        "Herr der Lage war am Schluss niemand mehr: 4500 Franken Mehrkosten pro Mandat sind für kleine Büros nicht tragbar. "
        "Die Bahnhofstrasse in Zürich bleibt die teuerste Lage der Schweiz, auf dem Bundesplatz in Bern demonstrierten am Dienstag die Bauern.\n"
        "Nächste Kurstage: Januar, Februar und März in Olten, Winterthur und Chur. "
        "Referent war der Leiter der Abteilung Direkte Bundessteuer der ESTV. "
        "Der Kurs ist mit 8 Stunden an die Weiterbildungspflicht «Fachfrau Finanz- und Rechnungswesen mit eidg. Fachausweis» anrechenbar.\n"
        "Zur Erinnerung: Die Frau des Hauses heisst hier niemand, und Grüezi Frau und Herr sind keine Namen.\n",
    ),
    # 16 Look-alikes only, fr: nothing to mark
    (
        "lookalikes_fr",
        "fr",
        "Rappel aux collaborateurs\n"
        "\n"
        "La Commune de Vevey et le Canton de Vaud appliquent dès janvier le nouveau barème (art. 36 LIFD, ch. 3.2 de la circulaire). "
        "Le logiciel VaudTax 2025 est disponible depuis lundi. La Rue du Bourg à Lausanne est fermée pour travaux jusqu'en avril.\n"
        "Les cours «Comptabilité analytique» et «TVA pour PME» auront lieu en mars et avril à Yverdon-les-Bains; "
        "montant minimal de la déduction: 2'000 francs par an. Monsieur Tout-le-Monde ne lit pas la circulaire, "
        "mais l'Administration fédérale des contributions l'exige.\n"
        "Madame, Monsieur, merci de confirmer votre présence avant vendredi.\n",
    ),
    # 17 Mandate list with address changes, de: Dr. iur., von, Familie, Portuguese/Turkish/Romansh/Tamil names,
    #    c/o, house number with letter, Postfach, PLZ + place only, Notar, email
    (
        "adressaenderungen_de",
        "de",
        "Adressänderungen per 1.1.2026 (Mandantenliste)\n"
        "- ⟦PERSON|Dr. iur. Beat von Gunten⟧, neu: ⟦ADDRESS|Obere Zäune 8, 8001 Zürich⟧ (vorher Postfach)\n"
        "- ⟦PERSON|Familie Ferreira da Silva⟧, c/o ⟦PERSON|Maria Ferreira⟧, ⟦ADDRESS|Schulstrasse 6c, 8902 Urdorf⟧\n"
        "- ⟦ORG|Yilmaz Transporte GmbH⟧, neu ⟦ADDRESS|Postfach 1120, 8021 Zürich⟧; Geschäftsführer ⟦PERSON|Hr. Y. Yilmaz⟧\n"
        "- ⟦PERSON|Gion Antoni Caduff⟧ zieht nach ⟦ADDRESS|7130 Ilanz⟧ (genaue Adresse folgt)\n"
        "- ⟦PERSON|Thamilini Sivanesan⟧, Adresse unverändert, neue Mailadresse ⟦EMAIL|thamilini.s@example.ch⟧\n"
        "- ⟦PERSON|Ernst Anderegg-Zbinden⟧ verstorben am 3. Oktober, Nachlass läuft über ⟦PERSON|Notar Stefan Ruch⟧\n",
    ),
    # 18 Email from the office to a client, de: first names alone, Revisionsstelle, signature block, CC
    (
        "email_jahresabschluss_de",
        "de",
        "Betreff: Jahresabschluss 2025 ⟦ORG|Zimmerei Hürzeler GmbH⟧\n"
        "\n"
        "Lieber ⟦PERSON|Thomas⟧\n"
        "\n"
        "Der Entwurf ist fertig. Bitte prüfe die Abgrenzung der Rechnung an ⟦ORG|Baumann Bedachungen AG⟧ (CHF 12'400) "
        "und die Privatanteile für dich und ⟦PERSON|Karin⟧. Die Revisionsstelle ⟦ORG|Audit Nordwest AG⟧ will die Unterlagen "
        "bis Ende Monat; Ansprechpartner dort ist ⟦PERSON|Herr Pascal Niederhauser⟧.\n"
        "Den Termin bei der Steuerverwaltung des Kantons Solothurn habe ich auf den 9. Dezember gelegt.\n"
        "\n"
        "Herzliche Grüsse\n"
        "⟦PERSON|Sandra Wyss⟧\n"
        "Mandatsleiterin\n"
        "⟦ORG|Wyss Treuhand GmbH⟧\n"
        "⟦ADDRESS|Baslerstrasse 60, 4600 Olten⟧\n"
        "Tel. ⟦PHONE|062 205 44 10⟧\n"
        "\n"
        "CC: ⟦PERSON|Karin Hürzeler⟧, ⟦PERSON|Thomas Hürzeler⟧, ⟦PERSON|Pascal Niederhauser⟧\n",
    ),
]
