"""Blind acceptance set B: persons, companies and addresses, written by a second reviewer.

Written after set A had been used to improve the recognisers, without reading the recognisers
or the changes, to see whether the improvement generalises. Different kinds of text than an
obvious first set: a Betreibungsauszug, a dentist's invoice, a daycare receipt, a bank's tax
certificate (3a and mortgage), an estate inventory, a lease termination, a payslip with child
allowances, an all-caps bank statement, a lowercase WhatsApp exchange, a phone note, a meeting
protocol, a mail with names in running text and a signature, an Italian invoice, a French
procuration, an association's annual report, an English letter, an all-caps payment slip, and
three texts with look-alikes only (nothing to mark).

Everything is invented: no real persons, no real companies. Postcodes and places are real.
Markup: ⟦KIND|value⟧ with KIND in PERSON, ORG, ADDRESS, IBAN, AHV, PHONE, EMAIL.

Conventions (as in set A): a person's name as written, with a salutation or title directly in
front of it; every occurrence separately, also a bare first name or surname. A company with its
legal form when it has one; a shop, Verein, Kita, Praxis or Notariat without legal form is marked
too. Street with number plus postcode and place as one span when on one line, two spans on two
lines; postcode plus place alone as somebody's domicile is marked; a place alone, a street without
number, Gemeinde X and Kanton X are not. Authorities are never marked.
"""

RAW = [
    (
        "betreibungsauszug",
        "de",
        """Betreibungsamt Olten-Gösgen
Auszug aus dem Betreibungsregister

Betreffend: ⟦PERSON|Krasniqi Arben⟧, geb. 14.03.1981
Wohnhaft: ⟦ADDRESS|Aarburgerstrasse 44b, 4600 Olten⟧
Auskunft verlangt von: ⟦ORG|Treuhand Niederamt AG⟧ (mit Vollmacht vom 02.10.2026)

Betreibungen der letzten fünf Jahre:

Nr. 2024/01877  Gläubiger: ⟦ORG|Sanavita Krankenversicherung AG⟧, ⟦ADDRESS|Postfach 1240, 6002 Luzern⟧
  Forderung CHF 1'842.60, Zahlungsbefehl zugestellt 12.02.2024, Rechtsvorschlag: nein, bezahlt am 03.04.2024
Nr. 2023/00412  Gläubiger: ⟦ORG|Garage Wyss & Söhne⟧, ⟦ADDRESS|Industriestrasse 9, 4663 Aarburg⟧
  Forderung CHF 3'120.00, Rechtsvorschlag erhoben am 21.06.2023, Fortsetzung nicht verlangt
Nr. 2022/03391  Gläubiger: Steuerverwaltung des Kantons Solothurn
  Forderung CHF 4'578.35, Verlustschein ausgestellt 19.09.2022, zurückgekauft am 28.11.2023

Keine hängigen Betreibungen. Ausgestellt in Olten, 21.10.2026.
Der Betreibungsbeamte: ⟦PERSON|R. Studer⟧
""",
    ),
    (
        "zahnarztrechnung",
        "de",
        """⟦ORG|Zahnarztpraxis am Marktplatz⟧
⟦PERSON|Dr. med. dent. Luisa Camenzind⟧
⟦ADDRESS|Marktgasse 5⟧
⟦ADDRESS|8200 Schaffhausen⟧
Tel. ⟦PHONE|052 625 18 40⟧

Patientin: ⟦PERSON|Fr. Nirmala Sivakumar⟧, geb. 02.07.1988
Vers.-Nr. ⟦AHV|756.4180.7319.09⟧
Rechnungsadresse: ⟦PERSON|Nirmala Sivakumar⟧, ⟦ADDRESS|Bachstrasse 17, 8240 Thayngen⟧

Rechnung Nr. 26-0831 vom 30.09.2026
Behandlungen vom 12.09.2026 und 19.09.2026

Pos.  Tarif  Leistung                              Anz.   TP      Betrag
4000  DT     Konsultation und Befundaufnahme        1    1.00     58.00
4055  DT     Zahnsteinentfernung, pro Quadrant      4    1.00    172.00
4160  DT     Füllung Komposit, 2-flächig            1    1.00    186.00
4910  DT     Röntgen, Einzelbild                    2    1.00     54.00
Total CHF                                                         470.00

Behandelnde Zahnärztin: ⟦PERSON|L. Camenzind⟧
Dentalhygiene: ⟦PERSON|Frau Mirela Jovanović⟧

Zahlbar innert 30 Tagen auf IBAN ⟦IBAN|CH55 0070 0790 0001 1223⟧, lautend auf ⟦ORG|Zahnarztpraxis am Marktplatz⟧.
Bitte reichen Sie die Rechnung selbst bei Ihrer Krankenkasse ein (Zusatzversicherung).
""",
    ),
    (
        "kita_beleg",
        "de",
        """⟦ORG|Kita Sunnewirbel⟧
⟦ADDRESS|Lindenweg 3, 8604 Volketswil⟧

Bestätigung der Betreuungskosten 2025 für die Steuererklärung

Kind: ⟦PERSON|Elina Pereira Gonçalves⟧, geb. 11.05.2021
Erziehungsberechtigte: ⟦PERSON|Herr Carlos Pereira⟧ und ⟦PERSON|Frau Joana Gonçalves Pereira⟧
Wohnadresse: ⟦ADDRESS|Zentralstrasse 88, 8604 Volketswil⟧

Betreuung: Montag, Dienstag und Donnerstag, ganze Tage, Januar bis Dezember 2025
In Rechnung gestellt (Vollkosten)          CHF 19'440.00
Subvention Gemeinde Volketswil             CHF  6'120.00
Von den Eltern bezahlt                     CHF 13'320.00
Davon Verpflegung (nicht abzugsfähig)      CHF  1'560.00
Abzugsfähige Betreuungskosten              CHF 11'760.00

Alle Rechnungen 2025 sind bezahlt. Diese Bestätigung ersetzt die Einzelrechnungen.

Volketswil, 15.01.2026
⟦PERSON|Sandra Egli⟧, Kitaleitung
""",
    ),
    (
        "bank_steuerbescheinigung",
        "de",
        """⟦ORG|Spar- und Leihkasse Oberaargau AG⟧
⟦ADDRESS|Bahnhofpl. 2⟧
⟦ADDRESS|4900 Langenthal⟧

Herrn
⟦PERSON|Luca Bianchi-Keller⟧
⟦ADDRESS|Mühleweg 12a⟧
⟦ADDRESS|3360 Herzogenbuchsee⟧

Langenthal, 12. Januar 2026

Steuerbescheinigung per 31. Dezember 2025

Sehr geehrter ⟦PERSON|Herr Bianchi-Keller⟧

Für Ihre Steuererklärung 2025 bestätigen wir Ihnen folgende Werte:

Vorsorgekonto 3a Nr. 3a-0412.7788
Einzahlungen 2025 (BVG-Maximum)                 CHF   7'258.00
Saldo per 31.12.2025 inkl. Zins                 CHF  61'904.35
Die Einzahlungen sind gemäss Art. 7 BVV 3 vom steuerbaren Einkommen abziehbar.

Festhypothek Nr. 51.207.339-4
Pfandobjekt: ⟦ADDRESS|Mühleweg 12a, 3360 Herzogenbuchsee⟧
Mitschuldnerin: ⟦PERSON|Frau Seraina Bianchi-Keller⟧
Schuldzinsen 2025 (1.45 %)                      CHF   9'412.50
Schuld per 31.12.2025                           CHF 620'000.00

Privatkonto ⟦IBAN|CH76 8080 8123 4567 8901⟧
Saldo per 31.12.2025                            CHF  14'220.80
Zinsertrag 2025 brutto                          CHF      31.40
Verrechnungssteuer 35 %                         CHF       0.00 (Freigrenze)

Für Fragen steht Ihnen Ihr Kundenberater ⟦PERSON|Thomas Aebi⟧ unter ⟦PHONE|062 919 30 11⟧ gerne zur Verfügung.
""",
    ),
    (
        "erbschaftsinventar",
        "de",
        """Inventar über den Nachlass von ⟦PERSON|Margrit Hürlimann-Vogt⟧, geb. 03.08.1941, gest. 22.06.2026, zuletzt wohnhaft ⟦ADDRESS|Alte Landstrasse 101, 8800 Thalwil⟧, verwitwet seit 2019 (Ehemann ⟦PERSON|Walter Hürlimann⟧), Bürgerin von Thalwil ZH und Küssnacht SZ.

Erben:
1. ⟦PERSON|Beatrice Hürlimann⟧, Tochter, ⟦ADDRESS|Seestrasse 230, 8810 Horgen⟧
2. ⟦PERSON|Daniel Hürlimann⟧, Sohn, ⟦ADDRESS|Rua das Flores 18, 2750-312 Cascais, Portugal⟧
3. ⟦PERSON|Nadja van der Meer-Hürlimann⟧, Enkelin, an Stelle des vorverstorbenen Sohnes ⟦PERSON|Peter Hürlimann⟧, ⟦ADDRESS|Chemin des Vignes 7, 1009 Pully⟧

Willensvollstrecker: ⟦PERSON|Notar Dr. Beat Zumstein⟧, ⟦ORG|Notariat Zumstein & Partner⟧, ⟦ADDRESS|Bahnhofstrasse 40, 8001 Zürich⟧

Aktiven per Todestag
- Liegenschaft ⟦ADDRESS|Alte Landstrasse 101, 8800 Thalwil⟧, Kat.-Nr. 4471, Steuerwert CHF 1'180'000.00
- Sparkonto ⟦ORG|Zürcher Landbank AG⟧, ⟦IBAN|CH28 0900 0000 4511 2233⟧, Saldo CHF 212'338.15
- Wertschriftendepot ⟦ORG|Bank Seeblick AG⟧, Depot Nr. 77-123.456, Kurswert CHF 388'900.00
- Guthaben Krankenkasse (Rückerstattung Prämien) CHF 412.30
- Hausrat und Schmuck, geschätzt CHF 15'000.00

Passiven
- Todesfallkosten ⟦ORG|Bestattungen Frei⟧ CHF 8'940.00
- Steuern 2026 (Gemeinde Thalwil und Kanton Zürich, provisorisch) CHF 14'200.00
- Offene Rechnung Spitex September CHF 1'180.00

Reinnachlass CHF 1'792'330.45. Die Teilung erfolgt zu je einem Drittel nach Art. 457 ZGB; ein Testament liegt nicht vor.

Inventaraufnahme am 15.09.2026 in Thalwil, in Anwesenheit von ⟦PERSON|B. Hürlimann⟧ und ⟦PERSON|Dr. Zumstein⟧.
""",
    ),
    (
        "kuendigung_miete",
        "de",
        """⟦ORG|Immoverwaltung Bützberg AG⟧
z. H. ⟦PERSON|Frau Petra Lüscher⟧
⟦ADDRESS|Postfach 311⟧
⟦ADDRESS|4922 Bützberg⟧

Einschreiben

Burgdorf, 28. September 2026

Kündigung des Mietvertrags: 3.5-Zimmer-Wohnung, ⟦ADDRESS|Kirchbergstrasse 56, 3400 Burgdorf⟧, 2. OG links

Sehr geehrte ⟦PERSON|Frau Lüscher⟧

Hiermit kündigen wir den oben genannten Mietvertrag auf den 31. März 2027 (ordentlicher Kündigungstermin, Art. 266c OR). Die Wohnung übergeben wir Ihnen gereinigt; wir bitten um einen Vorschlag für den Abgabetermin.

Unsere Adresse ab 1. April 2027: c/o ⟦PERSON|Familie Ndiaye⟧, ⟦ADDRESS|Lyssstrasse 14, 3270 Aarberg⟧.

Das Mietzinsdepot von CHF 4'500.00 bei der ⟦ORG|Bank Emmental⟧ bitten wir nach der Wohnungsabgabe auf unser Konto ⟦IBAN|CH43 0835 1234 5678 0001⟧ freizugeben.

Freundliche Grüsse

⟦PERSON|Aminata Ndiaye⟧          ⟦PERSON|Ousmane Ndiaye⟧
(beide Mieter unterzeichnen)
""",
    ),
    (
        "lohnabrechnung",
        "de",
        """⟦ORG|Metallbau Hänni GmbH⟧ · ⟦ADDRESS|Werkstrasse 21, 3250 Lyss⟧
Lohnabrechnung Oktober 2026

Mitarbeiter: ⟦PERSON|Shkelzen Berisha⟧, Pers.-Nr. 0147
AHV-Nr. ⟦AHV|756.9203.3144.73⟧, Eintritt 01.02.2019, verheiratet, 2 Kinder
Adresse: ⟦ADDRESS|Hirschenweg 6, 3292 Busswil BE⟧

Grundlohn (Monatslohn)                              5'850.00
Kinderzulage ⟦PERSON|Ardit⟧ (geb. 2016)                           250.00
Kinderzulage ⟦PERSON|Leonora⟧ (geb. 2020)                         250.00
Bruttolohn                                          6'350.00

AHV/IV/EO 5.3 %                                      -336.55
ALV 1.1 %                                             -69.85
BVG Sparbeitrag                                      -312.40
NBU 1.2 %                                             -76.20
Quellensteuer                                           0.00
Nettolohn                                           5'555.00

Auszahlung am 25.10.2026 auf ⟦IBAN|CH81 3199 9123 0008 8901⟧ (⟦ORG|Regiobank Seeland AG⟧)
Familienzulagen gemäss Verfügung der Ausgleichskasse des Kantons Bern vom 03.03.2020.
Lohnbuchhaltung: ⟦PERSON|E. Hänni⟧
""",
    ),
    (
        "kontoauszug_caps",
        "de",
        """KONTOAUSZUG PER 30.09.2026   KONTO CHF 0835-1234567.8   ⟦ORG|SCHREINEREI ZAUGG GMBH⟧

DATUM     BUCHUNGSTEXT                                                        BELASTUNG   GUTSCHRIFT
01.09.26  SALDOVORTRAG                                                                     38'412.70
02.09.26  ZAHLUNGSEINGANG VON ⟦ORG|MUELLER TRANSPORT AG⟧ ⟦ADDRESS|8953 DIETIKON⟧ RG 2026-144               4'860.00
03.09.26  SEPA UEBERWEISUNG AN ⟦PERSON|ANDRZEJ WOJCIK⟧ DE VERWENDUNGSZWECK MONTAGE SEPT   2'300.00
05.09.26  LASTSCHRIFT LSV ⟦ORG|SANAVITA KRANKENVERSICHERUNG AG⟧ PRAEMIE 10/2026             612.40
08.09.26  E-BANKING AUFTRAG ⟦ORG|HOLZ IMPORT BUCHS AG⟧ RG 7781                            9'115.20
10.09.26  TWINT ZAHLUNG ⟦ORG|BAECKEREI KUENZLI⟧ WINTERTHUR                                   38.50
12.09.26  DAUERAUFTRAG MIETE WERKSTATT ⟦ORG|LIEGENSCHAFTEN THURTAL AG⟧                    2'450.00
15.09.26  ZAHLUNGSEINGANG ⟦PERSON|FAM. OEZDEMIR⟧ RG 2026-139 KUECHE                                  12'400.00
18.09.26  BEZUG BANCOMAT WINTERTHUR HAUPTBAHNHOF                                   500.00
22.09.26  LOHNZAHLUNG SEPT ⟦PERSON|D. ZAUGG⟧                                             6'200.00
22.09.26  LOHNZAHLUNG SEPT ⟦PERSON|F. ROSSI-BAUMANN⟧                                     5'400.00
25.09.26  STEUERN AKONTO STEUERAMT WINTERTHUR                                    3'000.00
28.09.26  ZAHLUNGSEINGANG VON ⟦PERSON|KELLER HANS⟧ ⟦ADDRESS|8405 WINTERTHUR⟧ RG 2026-150               1'975.00
30.09.26  SPESEN UND GEBUEHREN                                                      12.00
30.09.26  SALDO NEU                                                                        28'019.70
""",
    ),
    (
        "whatsapp",
        "de",
        """[04.11.26, 09:12] ⟦PERSON|Sandra Keller⟧: hoi ⟦PERSON|reto⟧, hesch du d rechnig vo de ⟦ORG|garage brunner⟧ scho verbuecht? de ⟦PERSON|herr aliu⟧ fragt
[04.11.26, 09:15] ⟦PERSON|Reto Gisler⟧: no nid, isch das die vom ⟦PERSON|aliu⟧ sim transporter?
[04.11.26, 09:15] ⟦PERSON|Sandra Keller⟧: ja genau, 1'240.– vom 12.10.
[04.11.26, 09:20] ⟦PERSON|Reto Gisler⟧: ok mach ich hüt no. und d ⟦PERSON|frau morina⟧ het aglütet wäge em lohnuswiis vo ihrem maa ⟦PERSON|besnik⟧
[04.11.26, 09:21] ⟦PERSON|Sandra Keller⟧: schick ihr s pdf a ⟦EMAIL|l.morina@example.ch⟧ – aber nid a die alt adresse ⟦ADDRESS|bergstr. 4, 6010 kriens⟧, die sind umzoge
[04.11.26, 09:22] ⟦PERSON|Reto Gisler⟧: 👍 neui adresse?
[04.11.26, 09:24] ⟦PERSON|Sandra Keller⟧: ⟦ADDRESS|obernauerstrasse 19, 6010 kriens⟧
[04.11.26, 09:24] ⟦PERSON|Reto Gisler⟧: merci, passt
""",
    ),
    (
        "telefonnotiz",
        "de",
        """Telefonnotiz 03.11.2026, 14:35
Anrufer: ⟦PERSON|Hr. Gashi⟧ (⟦ORG|Gashi Gipserei⟧), ⟦PHONE|079 412 33 18⟧
Betrifft: MWST-Abrechnung Q3/2026

- hat Mahnung der ESTV erhalten, Frist 15.11.
- Belege liegen noch bei ⟦PERSON|Fr. Steiner-Huber⟧ (seine Buchhalterin bis Juni), sie wohnt jetzt in ⟦ADDRESS|8853 Lachen⟧
- wünscht Termin nächste Woche, Di oder Do, nicht vor 17 Uhr
- Rückruf bitte an ⟦PERSON|Valon⟧ (Sohn, macht die Administration), ⟦PHONE|076 880 21 09⟧

Erledigt: Termin Do 12.11., 17:30 bei uns. Fristverlängerung bei der ESTV online beantragt.
""",
    ),
    (
        "sitzungsprotokoll",
        "de",
        """Protokoll der Teamsitzung vom 27.10.2026, 16:00–17:15, Sitzungszimmer 2

Anwesend: ⟦PERSON|J. Frischknecht⟧ (Vorsitz), ⟦PERSON|A. de Oliveira⟧, ⟦PERSON|K. Vuković⟧, ⟦PERSON|S. Rüegg-Baumann⟧, ⟦PERSON|T. Balasingham⟧ (Protokoll)
Entschuldigt: ⟦PERSON|P. Tanner⟧
Gast zu Traktandum 3: ⟦PERSON|Herr Yves Chevalley⟧, ⟦ORG|Chevalley Revision SA⟧

1. Protokoll der letzten Sitzung: genehmigt.

2. Mandat ⟦ORG|Bäckerei Konditorei Zumbühl⟧: ⟦PERSON|Frischknecht⟧ berichtet, dass die Inhaberin ⟦PERSON|Frau Zumbühl⟧ den Betrieb per Ende Jahr an ihren Neffen ⟦PERSON|Fabio Zumbühl⟧ übergibt. ⟦PERSON|de Oliveira⟧ klärt die steuerlichen Folgen der Übertragung (Art. 18 DBG, Steueraufschub) bis Ende November.

3. Revision ⟦ORG|Alpenblick Immobilien AG⟧: ⟦PERSON|Chevalley⟧ erläutert die Befunde der Zwischenrevision. Offen ist die Bewertung der Liegenschaft ⟦ADDRESS|Dorfstrasse 2, 3818 Grindelwald⟧. ⟦PERSON|Vuković⟧ bereitet die Stellungnahme vor; Frist 15.11.

4. Personelles: ⟦PERSON|Rüegg-Baumann⟧ reduziert ab 1.1.2027 auf 60 %. Die freie Kapazität wird im Dezember ausgeschrieben.

5. Varia: Die Weihnachtsfeier findet am 18.12. statt; ⟦PERSON|Balasingham⟧ reserviert.

Nächste Sitzung: 24.11.2026.
Für das Protokoll: ⟦PERSON|T. Balasingham⟧
""",
    ),
    (
        "mail_ohne_titel",
        "de",
        """Betreff: Übergabe Mandate per Ende Jahr

Hallo ⟦PERSON|Nadine⟧

Gestern hat ⟦PERSON|Priya Nadarajah⟧ angerufen. Sie übernimmt ab Januar die Buchhaltungen von ⟦PERSON|Tomislav Horvat⟧, weil er pensioniert wird. Die Unterlagen von ⟦PERSON|Horvat⟧ liegen noch bei ⟦PERSON|Beatrix Wenger⟧ im Archiv; ⟦PERSON|Beatrix⟧ ist bis Freitag in den Ferien. Kannst du ⟦PERSON|Priya⟧ die Zugänge einrichten und ⟦PERSON|Marco Delacroix⟧ vom Kundenteam informieren? ⟦PERSON|Marco⟧ kennt die Kunden von ⟦PERSON|Tomislav⟧ am besten, vor allem ⟦PERSON|Gianluca Ferrari⟧ und die beiden Schwestern ⟦PERSON|Imhof⟧, die immer erst im Dezember ihre Belege bringen.

Die Übergabe soll bis am 19. Dezember erledigt sein, damit im Januar niemand ohne Ansprechperson ist.

Danke und Gruss
⟦PERSON|Oliver⟧

--
⟦PERSON|Oliver Brändli⟧
Mandatsleiter, dipl. Treuhandexperte
⟦ORG|Brändli & Co. Treuhand AG⟧
⟦ADDRESS|Zürcherstrasse 101 | 8500 Frauenfeld⟧
T ⟦PHONE|+41 52 721 44 10⟧ | M ⟦PHONE|+41 79 334 56 78⟧
⟦EMAIL|oliver.braendli@example-treuhand.ch⟧ | www.example-treuhand.ch
""",
    ),
    (
        "fattura",
        "it",
        """⟦ORG|Elettro Pedrazzini Sagl⟧
⟦ADDRESS|Via S. Gottardo 14⟧
⟦ADDRESS|6500 Bellinzona⟧
IDI CHE-123.456.789 IVA

Spett.le
⟦ORG|Fiduciaria Ceresio SA⟧
all'att. della ⟦PERSON|Signora Chiara Bernasconi⟧
⟦ADDRESS|Piazza Indipendenza 3⟧
⟦ADDRESS|6900 Lugano⟧

Fattura n. 2026-0412 del 15.10.2026
Cantiere: casa unifamiliare ⟦PERSON|Sig. Alessandro Ghiringhelli⟧, ⟦ADDRESS|Via ai Ronchi 9, 6512 Giubiasco⟧

Descrizione                                       Quantità   Prezzo     Importo
Sostituzione quadro elettrico                        1      1'850.00   1'850.00
Ore di lavoro elettricista (⟦PERSON|D. Pedrazzini⟧)      14.5       98.00   1'421.00
Materiale (cavi, interruttori, prese)                1        612.40     612.40
Trasferta cantiere                                   3         45.00     135.00
Totale netto                                                            4'018.40
IVA 8.1 %                                                                 325.49
Totale CHF                                                              4'343.89

Pagamento entro 30 giorni sul conto ⟦IBAN|CH55 0070 0790 0001 1223⟧, intestato a ⟦ORG|Elettro Pedrazzini Sagl⟧.
Per domande: ⟦PERSON|Signor Davide Pedrazzini⟧, ⟦PHONE|091 825 44 12⟧.
""",
    ),
    (
        "procuration",
        "fr",
        """PROCURATION

Je soussigné, ⟦PERSON|Monsieur Yannick de Preux⟧, né le 09.04.1972, domicilié ⟦ADDRESS|Pl. de la Gare 3, 1003 Lausanne⟧, donne par la présente procuration à ⟦ORG|Fiduciaire du Léman Sàrl⟧, ⟦ADDRESS|Avenue de Rumine 22, 1005 Lausanne⟧, représentée par ⟦PERSON|Me Isabelle Rochat⟧ ou ⟦PERSON|Mme Aurélie Dos Santos⟧, pour me représenter auprès de l'Administration cantonale des impôts du Canton de Vaud et de la Commune de Lausanne dans toutes les affaires relatives à ma déclaration d'impôt 2025, y compris pour recevoir toute correspondance, demander des délais et déposer des réclamations.

La présente procuration s'étend également à ma société ⟦ORG|DP Conseils SA⟧, dont je suis l'administrateur unique, et à mon épouse ⟦PERSON|Madame Carole de Preux-Nussbaumer⟧ pour notre déclaration commune.

Elle est valable jusqu'à révocation écrite.

Lausanne, le 20 octobre 2026

⟦PERSON|Y. de Preux⟧

Procuration acceptée le 22 octobre 2026: ⟦PERSON|I. Rochat⟧, ⟦ORG|Fiduciaire du Léman Sàrl⟧
""",
    ),
    (
        "vereinsbericht",
        "de",
        """⟦ORG|Quartierverein Breitenrain-Lorraine⟧
Jahresbericht 2025

Liebe Mitglieder

Das Vereinsjahr 2025 war geprägt vom Quartierfest im Juni und von der Neuausrichtung der Ferienbetreuung für Kinder. Der Vorstand hat sich zu acht Sitzungen getroffen.

Vorstand 2025
Präsidentin: ⟦PERSON|Hanna Gfeller⟧
Vizepräsident: ⟦PERSON|Mehmet Kaya⟧
Kassierin: ⟦PERSON|Ruth von Allmen⟧
Aktuar: ⟦PERSON|Jérôme Favre-Bulle⟧
Beisitz: ⟦PERSON|Tesfalem Ghebremariam⟧, ⟦PERSON|Ana Lucía Ruiz Ortega⟧
Revisoren: ⟦PERSON|Urs Bieri⟧ und ⟦PERSON|Claudia Spörri⟧

Finanzen: Die Jahresrechnung schliesst mit einem Gewinn von 2'340.15 Franken. Der grösste Posten waren die Kosten für das Quartierfest (11'800 Franken), gedeckt durch einen Beitrag der Stadt Bern und das Sponsoring der ⟦ORG|Metzgerei Hofer⟧ und der ⟦ORG|Lorraine Apotheke AG⟧. Die Mitgliederzahl stieg von 212 auf 238.

Mutationen: Aus dem Vorstand zurückgetreten ist ⟦PERSON|Kaya⟧ per Ende Jahr; als Nachfolgerin schlägt der Vorstand ⟦PERSON|Frau Leyla Demir⟧ vor. Wir danken ⟦PERSON|Mehmet⟧ herzlich für sechs Jahre Engagement.

Generalversammlung: Donnerstag, 19. März 2026, 19:30 Uhr, Pfarreisaal. Traktanden und Jahresrechnung folgen mit der Einladung.

Für den Vorstand: ⟦PERSON|H. Gfeller⟧
""",
    ),
    (
        "english_letter",
        "en",
        """Dear ⟦PERSON|Mr Okonkwo⟧

Thank you for sending us the documents for your 2025 Swiss tax return. As discussed with my colleague ⟦PERSON|Ms Vera Hug⟧, we have registered you with the tax office of the Canton of Zug as a resident taxpayer from 1 March 2025.

We still need the following:
- the salary certificate (Lohnausweis) from ⟦ORG|Nexora Systems AG⟧ for March to December 2025;
- the statement of your pension fund contributions from ⟦ORG|Pensionskasse Nexora⟧;
- the rental contract for ⟦ADDRESS|Zugerbergstrasse 15, 6300 Zug⟧ and the receipts for your relocation costs;
- the UK P60 from your former employer ⟦ORG|Hartley & Finch Ltd⟧ for the months before your move;
- confirmation whether your wife ⟦PERSON|Mrs Adaeze Okonkwo⟧ had any income in 2025, and whether your children ⟦PERSON|Chidi⟧ and ⟦PERSON|Amara⟧ attended a daycare (childcare costs are deductible up to CHF 25,000 per child).

Please upload everything to the client portal or send it to ⟦EMAIL|tax@example-treuhand.ch⟧. The filing deadline has been extended to 30 June 2027.

Kind regards
⟦PERSON|Dominik Stalder⟧
⟦ORG|Stalder Treuhand GmbH⟧, ⟦ADDRESS|Baarerstrasse 77, 6300 Zug⟧
""",
    ),
    (
        "einzahlungsschein",
        "de",
        """EMPFANGSSCHEIN / ZAHLTEIL

KONTO / ZAHLBAR AN
⟦IBAN|CH81 3199 9123 0008 8901⟧
⟦ORG|BAUMGARTNER HAUSTECHNIK GMBH⟧
⟦ADDRESS|GEWERBESTRASSE 11⟧
⟦ADDRESS|5035 UNTERENTFELDEN⟧

REFERENZ
21 00000 00003 13947 14300 09017

ZUSAETZLICHE INFORMATIONEN
RECHNUNG 2026-0587 HEIZUNGSSERVICE OKTOBER

ZAHLBAR DURCH
⟦PERSON|SELAMAWIT TESFAY⟧
⟦ADDRESS|WEINBERGSTR. 7A⟧
⟦ADDRESS|8006 ZUERICH⟧

WAEHRUNG CHF      BETRAG 486.75
ANNAHMESTELLE
""",
    ),
    (
        "lookalike_seminar",
        "de",
        """Einladung zum Fachseminar «Neues Rechnungslegungsrecht und Mehrwertsteuer 2027»

Datum: Dienstag, 20. Januar 2027, 13:30 bis 17:00 Uhr
Ort: Kongresszentrum, St. Gallen (der Saal wird im Dezember bekannt gegeben)
Kosten: 480 Franken pro Person, für Mitglieder 320 Franken

Themen:
- Die Revision des Rechnungslegungsrechts (Art. 957 ff. OR) und ihre Folgen für KMU
- Säule 3a und Einkauf in die Pensionskasse: Was gilt neu nach Art. 79b BVG?
- Mehrwertsteuer: Saldosteuersatz, Plattformbesteuerung und die Praxis der ESTV
- Erfahrungsbericht: Umstellung von Excel auf eine Buchhaltungssoftware (Buchwerk Pro, Finanzbogen Cloud)
- Podium: Künstliche Intelligenz im Treuhandbüro – Chancen und Grenzen

Die Referentinnen und Referenten werden auf der Website bekannt gegeben. Anmeldung bis 10. Januar über das Formular; die Teilnehmerzahl ist auf 80 Personen beschränkt. Der Anlass findet in deutscher Sprache statt, die Unterlagen sind auch auf Französisch erhältlich.

Anreise: Der Veranstaltungsort liegt fünf Gehminuten vom Bahnhof St. Gallen entfernt, Parkplätze gibt es im Parkhaus Bahnhof. Mit dem Zug ab Zürich dauert die Fahrt rund eine Stunde, ab Chur und Winterthur weniger.
""",
    ),
    (
        "lookalike_prosa",
        "de",
        """Notiz zur Ablage und zum Vorgehen bei Mahnungen

Bei Mahnungen und Betreibungen gilt: Zuerst die Rechnung und Mahnung prüfen, dann den Kontoauszug und die Buchung vergleichen. Wenn Zahlung und Rechnung nicht übereinstimmen, z. B. bei Skonto, Teilzahlung oder Rundungsdifferenz, ist u. a. das Datum der Valuta zu beachten. Erst nach der zweiten Mahnung, frühestens im März oder April nach dem Rechnungsjahr, geht die Forderung ans Betreibungsamt.

Die Unterlagen gehören in den Ordner «Debitoren und Kreditoren», getrennt nach Januar bis Juni und Juli bis Dezember. Dauerbelege wie Mietvertrag und Versicherungspolice kommen in den Ordner «Verträge und Policen». Für die Kinder gilt: Kinderzulagen, Betreuungskosten und Alimente in den Ordner «Familie und Vorsorge».

Für den Kaffee im Pausenraum: Wer die letzte Kapsel nimmt, bestellt neue. Die Marke «Dr. Bohne» ist aufgebraucht; die Kollegen bevorzugen ohnehin «Frau Holle Schoggi» aus dem Dorfladen, auch wenn der «Herr der Ringe»-Marathon am Freitag mehr Zucker braucht. Zwischen Weihnachten und Neujahr sind Büro und Sekretariat geschlossen; am Berchtoldstag wird gearbeitet.
""",
    ),
    (
        "lookalike_memo_fr",
        "fr",
        """Mémo interne: délais et procédures pour la période fiscale 2026

Les déclarations d'impôt des personnes physiques du Canton de Vaud doivent être déposées jusqu'au 15 mars; une prolongation jusqu'au 30 juin est possible en ligne. Pour le Canton de Genève, le délai est le 31 mars, et l'Administration fiscale cantonale accorde une prolongation jusqu'au 30 septembre. Dans le Canton de Fribourg et le Canton du Valais, la Commune ne joue aucun rôle dans la procédure; tout passe par le Service cantonal des contributions.

Rappel: les frais de garde sont déductibles jusqu'à 25'000 francs par enfant en impôt fédéral direct (art. 33 al. 3 LIFD). Les rachats dans la caisse de pension restent déductibles, sous réserve du délai de blocage de trois ans de l'art. 79b LPP.

Les bureaux de la Rue du Simplon et de l'Avenue de la Gare seront fermés entre Noël et Nouvel An. Le parking de la Place de la Riponne est réservé aux clients en janvier et février. Le logiciel de saisie passe de la version Printemps à la version Automne en novembre; la formation a lieu en décembre, en français et en allemand.
""",
    ),
]
