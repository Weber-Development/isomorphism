"""Acceptance set C: persons, companies and addresses, written blind by a third reviewer.

Written without reading the recognisers, the word lists or sets A and B, after those two sets had
been used to improve the recognisers. Set C decides whether the improvement generalises. The texts
are the kinds of paper a fiduciary office gets that are not the obvious ones: pension fund
statement, health insurance settlement, maintenance agreement, service charge statement, vehicle
registration data, club minutes, tradesman's quote, securities list, family allowance confirmation,
payment reminder, reference letters, hurried meeting notes, an email thread with quoted replies, a
dialect SMS, a pasted spreadsheet, a bank booking list, a French termination letter, an Italian
employment contract, and three texts with look-alikes only. Everything is invented.

Markup: ⟦KIND|value⟧ with KIND in PERSON, ORG, ADDRESS, IBAN, AHV, PHONE, EMAIL.
"""

RAW = [
    (
        "vorsorgeausweis",
        "de",
        "⟦ORG|Pensionskasse Bergbahnen Tschudi AG⟧\n"
        "Vorsorgeausweis per 1. Januar 2026\n"
        "\n"
        "Versicherte Person: ⟦PERSON|Frau Ottilia Zgraggen-Imboden⟧\n"
        "Geburtsdatum: 14.03.1971\n"
        "AHV-Nr.: ⟦AHV|756.4411.8723.40⟧\n"
        "Adresse: ⟦ADDRESS|Gotthardstrasse 12a, 6460 Altdorf⟧\n"
        "Arbeitgeber: ⟦ORG|Bergbahnen Tschudi AG⟧, ⟦ADDRESS|Bahnhofplatz 2, 6460 Altdorf⟧\n"
        "Eintritt: 01.08.2009\n"
        "Versicherter Jahreslohn: CHF 78'400\n"
        "Koordinationsabzug: CHF 26'460\n"
        "Sparguthaben per 31.12.2025: CHF 214'318.55\n"
        "davon BVG-Altersguthaben: CHF 142'910.20\n"
        "Altersrente bei 64 (Umwandlungssatz 5.4 %): CHF 18'900 pro Jahr\n"
        "Invalidenrente: CHF 47'040 pro Jahr\n"
        "Ehegattenrente: CHF 28'224 pro Jahr\n"
        "Kinderrente: CHF 9'408 pro Jahr und Kind\n"
        "Mögliche Einkaufssumme: CHF 61'200\n"
        "Vorbezug Wohneigentum möglich bis: CHF 107'159.25\n"
        "\n"
        "Bei Fragen wenden Sie sich an unsere Sachbearbeiterin, ⟦PERSON|Frau R. Caflisch⟧, "
        "Telefon ⟦PHONE|041 870 22 19⟧.\n",
    ),
    (
        "leistungsabrechnung",
        "de",
        "⟦ORG|Alpina Krankenversicherung AG⟧\n"
        "Leistungsabrechnung Nr. 2026-0417-88 vom 18.03.2026\n"
        "\n"
        "Versicherter: ⟦PERSON|Herr Fridolin Inderbitzin⟧, Versichertennummer 80756.4411\n"
        "Rechnungssteller: ⟦ORG|Physio am Bach⟧, ⟦ADDRESS|Dorfstr. 5 / 9000 St. Gallen⟧\n"
        "Behandlung: 9 Sitzungen Physiotherapie, 12.01.–27.02.2026\n"
        "Rechnungsbetrag: CHF 1'044.00\n"
        "Franchise (Rest 2026): CHF 300.00\n"
        "Selbstbehalt 10 %: CHF 74.40\n"
        "Unsere Leistung: CHF 669.60\n"
        "Ihr Anteil: CHF 374.40\n"
        "\n"
        "Weitere Rechnung: ⟦PERSON|Dr. med. Seraina Brunschwiler⟧, "
        "⟦ADDRESS|Rorschacherstr. 101, 9006 St. Gallen⟧\n"
        "Konsultation 03.03.2026: CHF 186.30, Selbstbehalt CHF 18.65\n"
        "\n"
        "Der Betrag von CHF 393.05 wird innert 10 Tagen auf Ihr Konto "
        "⟦IBAN|CH95 0839 0000 4442 2811 7⟧ überwiesen. Die Abrechnung gilt als Beleg für die "
        "Steuererklärung (Krankheitskosten).\n",
    ),
    (
        "alimentenvereinbarung",
        "de",
        "Vereinbarung über Kinderunterhalt\n"
        "\n"
        "zwischen\n"
        "⟦PERSON|Herrn Besnik Krasniqi⟧, ⟦ADDRESS|Weiherweg 3, 4600 Olten⟧ (nachfolgend Vater)\n"
        "und\n"
        "⟦PERSON|Frau Blerta Krasniqi-Gashi⟧, ⟦ADDRESS|Aarauerstrasse 88b, 4600 Olten⟧ "
        "(nachfolgend Mutter)\n"
        "\n"
        "betreffend die gemeinsamen Kinder ⟦PERSON|Arlind⟧ (geb. 2017) und ⟦PERSON|Dea⟧ "
        "(geb. 2020).\n"
        "\n"
        "1. Der Vater bezahlt der Mutter für ⟦PERSON|Arlind⟧ monatlich CHF 850 und für "
        "⟦PERSON|Dea⟧ monatlich CHF 750, zuzüglich allfälliger Kinderzulagen, zahlbar im Voraus "
        "auf das Konto der Mutter.\n"
        "2. Die Beiträge sind an den Landesindex der Konsumentenpreise gebunden (Stand Oktober "
        "2026) und werden jeweils per 1. Januar angepasst.\n"
        "3. Die Betreuung erfolgt alternierend; die Kinder besuchen die ⟦ORG|Kita Sunneschyn⟧ "
        "in Olten, die Kosten werden hälftig geteilt.\n"
        "4. Die Vereinbarung wurde der KESB Olten-Gösgen zur Genehmigung eingereicht.\n"
        "\n"
        "Olten, 20. Oktober 2026\n"
        "\n"
        "⟦PERSON|B. Krasniqi⟧            ⟦PERSON|B. Krasniqi-Gashi⟧\n",
    ),
    (
        "nebenkostenabrechnung",
        "de",
        "⟦ORG|Liegenschaftsverwaltung Imboden AG⟧\n"
        "⟦ADDRESS|Postfach 231, 7000 Chur⟧\n"
        "\n"
        "Heiz- und Nebenkostenabrechnung 01.07.2025 – 30.06.2026\n"
        "Liegenschaft: ⟦ADDRESS|Masanserstrasse 140-142, 7000 Chur⟧\n"
        "Mieter: ⟦PERSON|Fam. Radovanović⟧, Wohnung 3. OG links\n"
        "Verteilschlüssel: 4.5 Zimmer, 112 m2, Anteil 8.4 %\n"
        "\n"
        "Heizöl (Lieferung 14'200 Liter)        CHF 13'490.00\n"
        "Kaminfeger, Tankrevision                CHF    840.00\n"
        "Wasser / Abwasser                       CHF  4'115.60\n"
        "Hauswartung (⟦ORG|Reinigung Gashi⟧)             CHF  6'120.00\n"
        "Gartenpflege (⟦ORG|Gärtnerei da Silva⟧)         CHF  2'380.00\n"
        "Allgemeinstrom                          CHF  1'204.75\n"
        "Verwaltungshonorar 3 %                  CHF    844.50\n"
        "Total                                   CHF 28'994.85\n"
        "\n"
        "Ihr Anteil: CHF 2'214.70, Akontozahlungen CHF 2'400.00, Guthaben CHF 185.30.\n"
        "Das Guthaben überweisen wir auf das uns bekannte Konto von "
        "⟦PERSON|Herrn Milorad Radovanović⟧.\n"
        "Einsprachen innert 30 Tagen an die Verwaltung, z. H. "
        "⟦PERSON|Frau Ladina Caduff-Sprecher⟧.\n",
    ),
    (
        "fahrzeugausweis",
        "de",
        "Angaben aus dem Fahrzeugausweis (für die Buchhaltung, Geschäftsfahrzeuge)\n"
        "\n"
        "Halter: ⟦ORG|Garage Truffer⟧, Inhaber ⟦PERSON|Remigius Truffer⟧\n"
        "Adresse: ⟦ADDRESS|Kantonsstrasse 19, 3930 Visp⟧\n"
        "Kontrollschild: VS 184 227\n"
        "Marke/Typ: Skoda Octavia Combi 2.0 TDI\n"
        "Erste Inverkehrsetzung: 11.05.2022\n"
        "Stammnummer: 213.447.889\n"
        "Leergewicht: 1'512 kg, Gesamtgewicht 2'110 kg\n"
        "Kaufpreis: CHF 41'800 (Leasing, Restwert CHF 15'000)\n"
        "Privatanteil: 0.9 % vom Kaufpreis pro Monat, Fahrer ⟦PERSON|Hr. T. Zenhäusern⟧.\n"
        "\n"
        "Zweites Fahrzeug: Lieferwagen Ford Transit, VS 92 015, Erste Inverkehrsetzung "
        "02.02.2019, Leergewicht 2'045 kg. Wird von ⟦PERSON|Lourdes Ferreira dos Santos⟧ "
        "gefahren, kein Privatanteil (Fahrtenbuch vorhanden).\n",
    ),
    (
        "vereinsprotokoll",
        "de",
        "⟦ORG|Frauenchor Oberdorf⟧\n"
        "Protokoll der 47. Generalversammlung vom 12. März 2026, ⟦ORG|Restaurant Krone⟧, "
        "Oberdorf\n"
        "\n"
        "Anwesend: 23 Mitglieder\n"
        "Entschuldigt: ⟦PERSON|Theres Bieri⟧, ⟦PERSON|Alwina Hürlimann⟧, "
        "⟦PERSON|Rose-Marie Fankhauser⟧\n"
        "Vorsitz: Präsidentin ⟦PERSON|Ottilia Nussbaumer⟧\n"
        "Protokoll: ⟦PERSON|Flurina Caflisch⟧\n"
        "\n"
        "1. Begrüssung und Wahl der Stimmenzählerinnen.\n"
        "2. Jahresrechnung: Kassierin ⟦PERSON|Dragica Pavlović⟧ präsentiert die Rechnung 2025 "
        "mit einem Verlust von CHF 412.35; Vermögen per 31.12. CHF 9'877.10. Die Revisorinnen "
        "⟦PERSON|Gwendoline Rohrbasser⟧ und ⟦PERSON|Theres Bieri⟧ (schriftlich) beantragen "
        "Décharge. Einstimmig angenommen.\n"
        "3. Wahlen: Als neues Vorstandsmitglied wird ⟦PERSON|Seraina von Gunten⟧ vorgeschlagen "
        "und mit Applaus gewählt. ⟦PERSON|Urban Odermatt⟧ tritt als Dirigent zurück; der "
        "Vorstand dankt ihm für 14 Jahre. Nachfolgerin wird ⟦PERSON|Ilaria Fumagalli⟧ ab "
        "August.\n"
        "4. Vereinsadresse neu: c/o ⟦PERSON|Flurina Caflisch⟧, "
        "⟦ADDRESS|Lindenweg 4, 4515 Oberdorf⟧\n"
        "5. Mitgliederbeitrag bleibt bei 80 Franken, Passivmitglieder 40 Franken.\n"
        "6. Varia: Das Jubiläumskonzert findet am 7. November im Gemeindesaal statt. Die "
        "Gemeinde Oberdorf übernimmt die Saalmiete.\n"
        "\n"
        "Schluss der Versammlung: 21.40 Uhr.\n"
        "Die Protokollführerin: ⟦PERSON|F. Caflisch⟧\n",
    ),
    (
        "handwerkerofferte",
        "de",
        "⟦ORG|Sanitär Hürlimann & Söhne AG⟧\n"
        "⟦ADDRESS|Industriestr. 22, 8953 Dietikon⟧\n"
        "\n"
        "Offerte Nr. 26-0331 vom 29.10.2026\n"
        "An: ⟦ORG|Brunschwiler & Hossmann Architekten⟧\n"
        "z. H. ⟦PERSON|Herrn Konstantin Hossmann⟧\n"
        "⟦ADDRESS|Bahnhofstrasse 3\t8001 Zürich⟧\n"
        "\n"
        "Objekt: Umbau Bad, EFH ⟦PERSON|Wendelin Gisler⟧, ⟦ADDRESS|Im Rebberg 17, 8954 Geroldswil⟧\n"
        "\n"
        "Pos. 1  Demontage bestehende Sanitärapparate       CHF  1'280.00\n"
        "Pos. 2  Dusche bodeneben inkl. Rinne               CHF  4'960.00\n"
        "Pos. 3  WC wandhängend inkl. Spülkasten            CHF  1'740.00\n"
        "Pos. 4  Waschtisch mit Unterbau                    CHF  2'310.00\n"
        "Pos. 5  Leitungen, Anschlüsse, Dichtigkeitsprüfung CHF  3'850.00\n"
        "Pos. 6  Plattenarbeiten durch Drittfirma (⟦ORG|Fliesen Taddei⟧), separat offeriert\n"
        "Total exkl. MWST                                   CHF 14'140.00\n"
        "MWST 8.1 %                                         CHF  1'145.35\n"
        "Total inkl. MWST                                   CHF 15'285.35\n"
        "\n"
        "Gültig bis 30.11.2026. Ausführung Januar 2027, Dauer ca. 8 Arbeitstage. Die "
        "Koordination mit Schreiner ⟦PERSON|Bühler⟧ und ⟦ORG|Elektro Gisler + Co.⟧ erfolgt "
        "durch uns.\n"
        "\n"
        "Freundliche Grüsse\n"
        "⟦PERSON|Gallus Hürlimann⟧\n",
    ),
    (
        "wertschriftenverzeichnis",
        "de",
        "Wertschriftenverzeichnis 2025 – Beilage zur Steuererklärung\n"
        "Steuerpflichtige: ⟦PERSON|de Quervain Amédée⟧ und ⟦PERSON|de Quervain-Bovey Odile⟧\n"
        "Wohnsitz: ⟦ADDRESS|1700 Fribourg⟧\n"
        "\n"
        "Depot Nr. 441.228.7 bei der ⟦ORG|Privatbank Chevalley & Cie⟧\n"
        "Valor\tBezeichnung\tStück / Nominal\tSteuerwert 31.12.\tBruttoertrag\n"
        "1'102'334\tAnteile Fonds Obligationen CHF (thesaurierend)\t310\t34'720\t0\n"
        "2'998'017\tKassenobligation 1.5 % 2028\t50'000\t50'000\t750\n"
        "–\tAktien ⟦ORG|Druckerei Bieri AG⟧ (nicht kotiert)\t40\t28'000\t2'000\n"
        "4'411'089\tETF Aktien Welt\t85\t41'265\t612\n"
        "Sparkonto\t⟦IBAN|CH56 0483 5012 3456 7800 9⟧\t–\t18'044\t27\n"
        "\n"
        "Total Steuerwert: CHF 172'029\n"
        "Total Bruttoertrag: CHF 3'389, davon mit Verrechnungssteuer belastet: CHF 3'040\n"
        "Verrechnungssteuer: CHF 1'064.00, Rückforderung beantragt bei der Steuerverwaltung "
        "des Kantons Freiburg.\n"
        "\n"
        "Fribourg, 2. März 2026\n"
        "⟦PERSON|A. de Quervain⟧\n",
    ),
    (
        "kinderzulagen",
        "de",
        "Ausgleichskasse des Kantons Luzern\n"
        "Familienausgleichskasse\n"
        "\n"
        "Bestätigung Familienzulagen 2026\n"
        "\n"
        "⟦PERSON|Frau Sumithra Ravichandran⟧\n"
        "⟦ADDRESS|Gerliswilstr. 48⟧\n"
        "⟦ADDRESS|6020 Emmenbrücke⟧\n"
        "\n"
        "Arbeitgeber: ⟦ORG|Druckerei Bieri AG⟧, Luzern (Abrechnungsnummer 120.4471)\n"
        "\n"
        "Für folgende Kinder werden ab 1. Januar 2026 Zulagen ausgerichtet:\n"
        "- ⟦PERSON|Tharsan Ravichandran⟧, geb. 09.02.2012: Kinderzulage CHF 200 pro Monat\n"
        "- ⟦PERSON|Nila Ravichandran⟧, geb. 23.07.2016: Kinderzulage CHF 200 pro Monat\n"
        "- ⟦PERSON|Arjun Ravichandran⟧, geb. 30.11.2008: Ausbildungszulage CHF 250 pro Monat "
        "(Lehre bei ⟦ORG|Elektro Gisler + Co.⟧, Lehrvertrag bis 31.07.2027)\n"
        "\n"
        "Total CHF 650 pro Monat, Auszahlung mit dem Lohn durch den Arbeitgeber.\n"
        "Änderungen (Ausbildungsende, Wegzug, Wechsel des Arbeitgebers) sind innert 30 Tagen "
        "zu melden.\n"
        "\n"
        "Luzern, 15. Januar 2026\n"
        "Sachbearbeiter: ⟦PERSON|D. Zemp⟧\n",
    ),
    (
        "zahlungserinnerung",
        "de",
        "⟦ORG|Dachdeckerei Nussbaumer GmbH⟧, ⟦ADDRESS|Schlossweg 9, 3600 Thun⟧\n"
        "\n"
        "Herrn\n"
        "⟦PERSON|Pierre-Alain Dubosson⟧\n"
        "⟦ADDRESS|Ch. des Vignes 14⟧\n"
        "⟦ADDRESS|1806 St-Légier⟧\n"
        "\n"
        "Thun, 5. November 2026\n"
        "\n"
        "Zahlungserinnerung – Rechnung Nr. 4471 vom 2. September 2026\n"
        "\n"
        "Sehr geehrter ⟦PERSON|Herr Dubosson⟧\n"
        "\n"
        "Trotz unserer Rechnung für die Reparatur des Dachs an der ⟦ADDRESS|Rte de Blonay 27⟧ "
        "in St-Légier ist der Betrag von CHF 3'870.50 noch offen. Wir bitten Sie, den Betrag "
        "innert 10 Tagen auf unser Konto ⟦IBAN|CH95 0839 0000 4442 2811 7⟧ zu überweisen. "
        "Bleibt die Zahlung aus, müssen wir die Forderung dem Betreibungsamt übergeben und "
        "Verzugszins von 5 % verrechnen.\n"
        "\n"
        "Sollten Sie bereits bezahlt haben, betrachten Sie dieses Schreiben als "
        "gegenstandslos. Für Rückfragen steht Ihnen ⟦PERSON|Frau Jelena Pavlović⟧ "
        "(Buchhaltung) zur Verfügung.\n"
        "\n"
        "Freundliche Grüsse\n"
        "⟦ORG|Dachdeckerei Nussbaumer GmbH⟧\n"
        "⟦PERSON|Fridolin Nussbaumer⟧, Geschäftsführer\n",
    ),
    (
        "arbeitszeugnis",
        "de",
        "Arbeitszeugnis (Auszug)\n"
        "\n"
        "⟦PERSON|Herr Thabo Mwangi⟧, geboren am 3. Juni 1989, von Nairobi (Kenia), war vom "
        "1. Februar 2019 bis 31. Oktober 2026 als Sachbearbeiter Finanzen in unserer Firma "
        "tätig.\n"
        "\n"
        "Zu seinen Aufgaben gehörten die Debitoren- und Kreditorenbuchhaltung, das Mahnwesen, "
        "die MWST-Abrechnung sowie die Vorbereitung der Jahresabschlüsse für unsere "
        "Treuhänderin, die ⟦ORG|Treuhand Caflisch & Partner GmbH⟧.\n"
        "\n"
        "⟦PERSON|Herr Mwangi⟧ hat sich mit seinen fundierten Fachkenntnissen rasch "
        "eingearbeitet und die Aufgaben stets zu unserer vollen Zufriedenheit erledigt. Er "
        "arbeitete eng mit seiner Vorgesetzten, ⟦PERSON|Frau Ayşe Özdemir⟧, zusammen und wurde "
        "von Kundschaft und Lieferanten als zuvorkommend und zuverlässig geschätzt.\n"
        "\n"
        "⟦PERSON|Thabo⟧ verlässt uns auf eigenen Wunsch, um die Weiterbildung zum Fachmann "
        "Finanz- und Rechnungswesen mit eidgenössischem Fachausweis zu absolvieren. Wir danken "
        "ihm für seinen Einsatz und wünschen ihm alles Gute.\n"
        "\n"
        "Dietikon, 31. Oktober 2026\n"
        "⟦ORG|Sanitär Hürlimann & Söhne AG⟧\n"
        "\n"
        "⟦PERSON|Gallus Hürlimann⟧            ⟦PERSON|Ayşe Özdemir⟧\n"
        "Geschäftsleiter                       Leiterin Finanzen\n",
    ),
    (
        "besprechungsnotizen",
        "de",
        "Bespr. 28.10., 16h, Büro – Kunde: ⟦PERSON|GION CADUFF⟧ (übernimmt "
        "⟦ORG|Fahrschule Sprecher⟧ per 1.1.)\n"
        "- Übernahme von ⟦PERSON|Nicolin Sprecher⟧, Kaufpreis 180k, davon 40k Goodwill\n"
        "- neue Adresse Fahrschule: ⟦ADDRESS|Via Nova 8, 7130 Ilanz⟧ (bisher Glennerstr.)\n"
        "- Partnerin ⟦PERSON|Ladina⟧ (⟦PERSON|Caduff-Sprecher⟧?) soll 20% halten -> "
        "Gesellschaftsform? GmbH prüfen, Stammkapital 20k\n"
        "- Fahrzeuge: 2 Autos, 1 Töff, Leasing (frag ⟦PERSON|Hr. Vincenz⟧ von der "
        "⟦ORG|Garage Truffer⟧ wg. Vertragsübernahme)\n"
        "- MWST: ab Übernahme pflichtig, Umsatz > 100k, Saldosteuersatz?\n"
        "- Buchhaltung bisher Excel!! -> Angebot machen\n"
        "- Angestellter: ⟦PERSON|Placidus Derungs⟧, 60%, 3'900 brutto, bleibt\n"
        "- todo: Vollmacht, AHV-Anmeldung SVA GR, Handelsregister, Ausgleichskasse "
        "Familienzulagen\n"
        "- ⟦PERSON|Gion⟧ ruft mich Freitag an. Kopie an ⟦PERSON|Seraina⟧.\n",
    ),
    (
        "email_thread",
        "de",
        "Von: ⟦PERSON|Rose-Marie Fankhauser⟧ <⟦EMAIL|rm.fankhauser@hirschen-apotheke.example⟧>\n"
        "An: ⟦EMAIL|buchhaltung@treuhand-caflisch.example⟧\n"
        "Betreff: AW: AW: Belege Q3 ⟦ORG|Apotheke zum Hirschen⟧\n"
        "\n"
        "Guten Tag ⟦PERSON|Frau Caflisch⟧\n"
        "\n"
        "Danke, die fehlenden Belege habe ich jetzt im Portal hochgeladen. Die Rechnung von "
        "⟦ORG|Coiffure Blerta⟧ war privat, bitte ausbuchen.\n"
        "\n"
        "Freundliche Grüsse\n"
        "⟦PERSON|Rose-Marie Fankhauser⟧\n"
        "⟦ORG|Apotheke zum Hirschen⟧, ⟦ADDRESS|Hauptgasse 31, 4500 Solothurn⟧\n"
        "\n"
        "> Am 21.10.2026 um 09:12 schrieb ⟦PERSON|Flurina Caflisch⟧:\n"
        "> Liebe ⟦PERSON|Frau Fankhauser⟧\n"
        "> Für den Abschluss Q3 fehlen uns noch drei Belege (siehe Liste im Anhang). Zudem ist "
        "die Zahlung an ⟦PERSON|Herrn van der Meulen⟧ vom 14.9. (CHF 2'300) nicht zugeordnet "
        "– ist das die Miete für das Lager an der Weststrasse?\n"
        "> Freundliche Grüsse\n"
        "> ⟦PERSON|Flurina Caflisch⟧, ⟦ORG|Treuhand Caflisch & Partner GmbH⟧\n"
        ">\n"
        ">> Am 20.10.2026 um 17:48 schrieb ⟦PERSON|Rose-Marie Fankhauser⟧:\n"
        ">> Hallo ⟦PERSON|Flurina⟧, kannst du mir sagen, was noch fehlt? Die "
        "Lieferantenrechnung von ⟦ORG|Pharma Grosshandel Bovey SA⟧ bitte als Warenaufwand. "
        "Miete Lager: Vermieter ist ⟦PERSON|Jan van der Meulen⟧, "
        "⟦ADDRESS|Weststrasse 9, 4500 Solothurn⟧.\n"
        ">> Gruss, ⟦PERSON|Rose-Marie⟧\n",
    ),
    (
        "sms_dialekt",
        "de",
        "hoi ⟦PERSON|urban⟧, sorry bin spaat dra. d'⟦PERSON|frau zgraggen⟧ het aagrüefe wäge "
        "de ahv-abrächnig, chasch sie zrugglüte? ⟦PHONE|079 412 88 03⟧. und de ⟦PERSON|bühler⟧ "
        "vo de ⟦ORG|schriinerei bühler⟧ wott d'offerte bis fritig. adrässe vom neue lager isch "
        "⟦ADDRESS|lindenweg 4 4515 oberdorf⟧. merci, ⟦PERSON|ottilia⟧\n",
    ),
    (
        "mitgliederliste",
        "de",
        "Mitgliederliste Export (Stand 31.10.2026)\n"
        "Name;Vorname;Strasse;PLZ;Ort;Beitrag\n"
        "⟦PERSON|Inderbitzin⟧;⟦PERSON|Fridolin⟧;⟦ADDRESS|Gotthardstr. 12a;6460;Altdorf⟧;80\n"
        "⟦PERSON|von Gunten⟧;⟦PERSON|Seraina⟧;⟦ADDRESS|Alpenblick 3;3700;Spiez⟧;80\n"
        "⟦PERSON|dos Santos⟧;⟦PERSON|Edvaldo⟧;⟦ADDRESS|Rue de la Gare 15-17;1630;Bulle⟧;40\n"
        "⟦PERSON|Okafor⟧;⟦PERSON|Ngozi⟧;⟦ADDRESS|Via Cantonale 42;6900;Lugano⟧;80\n"
        "⟦PERSON|TSCHUDI⟧;⟦PERSON|URBAN⟧;⟦ADDRESS|Unterdorf 2;6460;Altdorf⟧;80\n"
        "⟦PERSON|da Silva Pereira⟧;⟦PERSON|Maria João⟧;⟦ADDRESS|Av. de la Harpe 9;1007;Lausanne⟧;80\n"
        "⟦PERSON|Hürlimann-Bieri⟧;⟦PERSON|Alwina⟧;⟦ADDRESS|Postfach 88;4800;Zofingen⟧;40\n"
        "Total;;;;;480\n",
    ),
    (
        "kontoauszug",
        "de",
        "Kontoauszug Kontokorrent ⟦IBAN|CH56 0483 5012 3456 7800 9⟧ – ⟦ORG|Druckerei Bieri AG⟧\n"
        "Periode 01.10.2026 – 31.10.2026, Währung CHF\n"
        "Datum|Valuta|Text|Belastung|Gutschrift|Saldo\n"
        "01.10.2026|01.10.2026|Gutschrift e-banking, Auftraggeber: "
        "⟦ORG|Brunschwiler & Hossmann Architekten⟧, Zürich, Mitteilung: RG 2026-311||4'320.00|"
        "58'112.40\n"
        "02.10.2026|02.10.2026|Dauerauftrag Miete Oktober, Begünstigter: "
        "⟦ORG|Liegenschaftsverwaltung Imboden AG⟧, Chur|3'150.00||54'962.40\n"
        "03.10.2026|03.10.2026|Lastschrift LSV ⟦ORG|Alpina Krankenversicherung AG⟧, Prämie "
        "Oktober|1'244.80||53'717.60\n"
        "06.10.2026|06.10.2026|Zahlung an ⟦PERSON|Theres Bieri⟧, Lohnvorschuss|1'500.00||"
        "52'217.60\n"
        "08.10.2026|07.10.2026|Gutschrift QR, Zahler: ⟦PERSON|Fam. Radovanović⟧, "
        "⟦ADDRESS|Masanserstrasse 140, 7000 Chur⟧, Ref. 00 00012 44718 00093 11022 "
        "07||186.50|52'404.10\n"
        "10.10.2026|10.10.2026|Kartenzahlung ⟦ORG|Restaurant Krone⟧ Oberdorf|142.00||52'262.10\n"
        "14.10.2026|14.10.2026|Zahlung an ⟦ORG|Fiduciaire Rossier Sàrl⟧, "
        "⟦ADDRESS|Rte de Fribourg 12, 1700 Fribourg⟧, Honorar Q3|2'700.00||49'562.10\n"
        "15.10.2026|15.10.2026|Gutschrift, Auftraggeber: ⟦PERSON|Okafor Ngozi⟧, Lugano, "
        "Mitteilung: Visitenkarten||260.00|49'822.10\n"
        "20.10.2026|20.10.2026|Zahlung Beiträge AHV/IV/EO Ausgleichskasse Luzern, Q3|"
        "4'871.35||44'950.75\n"
        "31.10.2026|31.10.2026|Kontoführungsgebühr|15.00||44'935.75\n",
    ),
    (
        "lettre_resiliation",
        "fr",
        "⟦PERSON|Me Firmin Pittet⟧\n"
        "⟦ORG|Étude Pittet & Chevalley⟧\n"
        "⟦ADDRESS|Pl. du Marché 6⟧\n"
        "⟦ADDRESS|1800 Vevey⟧\n"
        "\n"
        "Recommandé\n"
        "⟦PERSON|Mme Odile de Quervain-Bovey⟧\n"
        "⟦ADDRESS|Ch. de la Forêt 21b⟧\n"
        "⟦ADDRESS|1700 Fribourg⟧\n"
        "\n"
        "Vevey, le 3 novembre 2026\n"
        "\n"
        "Concerne : résiliation du mandat de gestion n° 2024-118\n"
        "\n"
        "Madame,\n"
        "\n"
        "Par la présente, nous résilions le mandat de gestion de votre portefeuille auprès de "
        "la ⟦ORG|Privatbank Chevalley & Cie⟧ pour le 31 décembre 2026, conformément à "
        "l'art. 404 CO. Les titres seront transférés à l'établissement de votre choix ; merci "
        "de nous communiquer les coordonnées avant le 15 décembre. Les honoraires du dernier "
        "trimestre (CHF 1'850.–) seront prélevés sur le compte de gestion.\n"
        "\n"
        "Le décompte final vous parviendra par ⟦PERSON|Mme Rose-Marie Dubosson⟧, notre "
        "comptable. Votre époux, ⟦PERSON|M. Amédée de Quervain⟧, en recevra une copie à "
        "l'adresse ci-dessus.\n"
        "\n"
        "Nous vous prions d'agréer, Madame, nos salutations distinguées.\n"
        "\n"
        "⟦PERSON|Firmin Pittet⟧, avocat\n",
    ),
    (
        "contratto_lavoro",
        "it",
        "Contratto di lavoro (estratto)\n"
        "\n"
        "tra ⟦ORG|Studio Legale Taddei & Bernasconi⟧, ⟦ADDRESS|V.le Stazione 4, 6500 Bellinzona⟧ "
        "(datore di lavoro)\n"
        "e la ⟦PERSON|Signora Ilaria Fumagalli⟧, nata il 2.9.1994, domiciliata a "
        "⟦ADDRESS|6512 Giubiasco⟧ (lavoratrice)\n"
        "\n"
        "Art. 1 Funzione: segretaria di studio, grado di occupazione 80 %.\n"
        "Art. 2 Inizio: 1° dicembre 2026. Periodo di prova: 3 mesi.\n"
        "Art. 3 Salario: CHF 4'480.– lordi mensili, tredicesima mensilità pro rata.\n"
        "Art. 4 Vacanze: 25 giorni lavorativi all'anno.\n"
        "Art. 5 Previdenza: la lavoratrice è assicurata presso la "
        "⟦ORG|Fondazione Collettiva Verbano⟧; i contributi sono ripartiti a metà.\n"
        "Art. 6 Superiore diretto: ⟦PERSON|avv. Tancredi Bernasconi⟧. In sua assenza, "
        "⟦PERSON|avv. Gioachino Taddei⟧.\n"
        "Art. 7 Disdetta: 1 mese durante il primo anno, poi 2 mesi per la fine di un mese.\n"
        "Art. 8 Foro: Bellinzona. Per il resto fa stato il CO.\n"
        "\n"
        "Bellinzona, 10 novembre 2026\n"
        "\n"
        "⟦PERSON|T. Bernasconi⟧                ⟦PERSON|I. Fumagalli⟧\n",
    ),
    (
        "reference_letter",
        "en",
        "⟦ORG|Fiduciaire Rossier Sàrl⟧\n"
        "⟦ADDRESS|Rte de Fribourg 12, 1700 Fribourg⟧\n"
        "\n"
        "To whom it may concern\n"
        "\n"
        "Reference for ⟦PERSON|Ms Ngozi Okafor⟧\n"
        "\n"
        "⟦PERSON|Ms Okafor⟧ joined our firm on 1 March 2021 as a junior accountant and left on "
        "30 September 2026 to relocate to Lugano. During her time with us she prepared VAT "
        "returns and annual accounts for small and medium-sized clients, among them "
        "⟦ORG|Café-Bar Il Portico⟧ and ⟦ORG|Garage Truffer⟧, and supported our partner, "
        "⟦PERSON|Mr Jean-Luc Rossier⟧, in audit assignments under the Swiss Code of "
        "Obligations.\n"
        "\n"
        "⟦PERSON|Ngozi⟧ is reliable, precise and calm under the pressure of the March and "
        "September deadlines. She communicates easily in French, English and Italian and is "
        "well liked by colleagues and clients alike. We regret her departure and wish her "
        "every success.\n"
        "\n"
        "Should you require further information, please contact me at the address above or "
        "⟦PERSON|Mrs Yolanda Rossier-Pittet⟧, Human Resources.\n"
        "\n"
        "Yours faithfully\n"
        "⟦PERSON|Jean-Luc Rossier⟧, Partner\n",
    ),
    (
        "seminar_lookalike",
        "de",
        "Einladung zum Herbstseminar 2026\n"
        "\n"
        "Liebe Mitglieder, sehr geehrte Damen und Herren\n"
        "\n"
        "Unser Verband lädt Sie zum Herbstseminar ein.\n"
        "Thema: Die neue Mehrwertsteuerverordnung und das revidierte Datenschutzgesetz (DSG) "
        "in der Praxis der Treuhänder\n"
        "Datum: Donnerstag, 26. November 2026, 13.30 bis 17.00 Uhr\n"
        "Ort: Kongresszentrum beim Bahnhof, Luzern\n"
        "\n"
        "Referate: Die Steuerverwaltung des Kantons Luzern stellt das neue Formular 2 für "
        "Wertschriften und das Wertschriftenverzeichnis vor. Die Eidgenössische "
        "Steuerverwaltung ESTV erläutert die Praxis zur Saldosteuersatzmethode nach Artikel 37 "
        "des Mehrwertsteuergesetzes. Die Ausgleichskasse zeigt die Änderungen bei der "
        "Lohnmeldung. Anschliessend Apéro und Erfahrungsaustausch.\n"
        "\n"
        "Kosten: 180 Franken für Mitglieder, 320 Franken für Nichtmitglieder, inklusive "
        "Unterlagen und Pausenverpflegung. Anmeldung bis 15. November über das Formular auf "
        "unserer Website. Die Anzahl Plätze ist auf 120 Personen beschränkt.\n"
        "\n"
        "Hinweis: Parkplätze sind beschränkt; der Bahnhof Luzern ist 400 Meter entfernt. Mit "
        "dem Auto erreichen Sie uns über die Seebrücke und die Pilatusstrasse, das Parkhaus "
        "kostet 4 Franken pro Stunde. Die Demonstrationen erfolgen in Excel und mit "
        "gängiger Buchhaltungssoftware; ein eigenes Notebook ist willkommen, aber nicht "
        "nötig.\n"
        "\n"
        "Wir freuen uns auf einen lehrreichen Nachmittag.\n"
        "Der Vorstand\n",
    ),
    (
        "rappel_lookalike",
        "fr",
        "Rappel des échéances fiscales 2027\n"
        "\n"
        "Chères collaboratrices, chers collaborateurs,\n"
        "\n"
        "La déclaration d'impôt 2026 des personnes physiques doit être déposée auprès de "
        "l'Administration cantonale des impôts avant le 31 mars 2027 ; une prolongation "
        "jusqu'au 30 juin peut être demandée en ligne. Le Canton de Vaud a publié les "
        "nouvelles Instructions générales ainsi que la Formule 2 et l'Annexe 01 pour les "
        "titres. La Commune de Lausanne a fixé son coefficient à 78.5 pour cent.\n"
        "\n"
        "Le Tribunal fédéral a rendu en octobre un arrêt sur la déduction des frais de "
        "formation ; la Loi fédérale sur l'harmonisation des impôts directs (LHID) et la Loi "
        "sur l'impôt fédéral direct (LIFD) restent déterminantes. Les montants forfaitaires "
        "passent à 3'500 francs pour les frais professionnels et à 12'000 francs pour la "
        "formation continue.\n"
        "\n"
        "En décembre, l'Avenue de la Gare et la Rue du Bourg seront fermées pour le Marché de "
        "Noël ; prévoyez le Métro ou le train. Les bureaux seront fermés du 24 décembre au "
        "2 janvier.\n"
        "\n"
        "Bonne fin d'année à toutes et à tous.\n"
        "La direction\n",
    ),
    (
        "circolare_lookalike",
        "it",
        "Circolare interna: chiusura annuale 2026\n"
        "\n"
        "Gentili Signore e Signori, cari Colleghi,\n"
        "\n"
        "con la presente ricordiamo le scadenze di fine anno. L'Ufficio delle imposte del "
        "Cantone Ticino accetta le dichiarazioni fino al 30 aprile 2027; il Comune di Lugano "
        "ha confermato il moltiplicatore al 77 per cento. La Legge federale sull'imposta sul "
        "valore aggiunto (LIVA) e l'Ordinanza sull'IVA sono state modificate dal Consiglio "
        "federale con effetto dal 1° gennaio 2027.\n"
        "\n"
        "Gli inventari devono essere consegnati entro il 15 gennaio; gli importi superiori a "
        "5'000 franchi vanno documentati con il contratto. Le fatture dei fornitori di "
        "dicembre vanno registrate nell'anno 2026, anche se pagate in gennaio.\n"
        "\n"
        "Durante il periodo natalizio Via Nassa e Viale Cattaneo saranno chiuse al traffico "
        "per il Mercatino di Natale; il Parcheggio Centrale resta aperto, la tariffa è di "
        "3 franchi all'ora. Gli uffici restano chiusi dal 24 dicembre al 3 gennaio.\n"
        "\n"
        "Buone Feste a tutte e a tutti.\n"
        "La Direzione\n",
    ),
]
