# Offene Firmenfelder: Recherche vom 2026-10-08

87 zuvor offene Felder bei sieben Firmen wurden anhand öffentlicher Quellen
weiter geprüft. 22 Felder besitzen jetzt einen belegten Vorschlag; 65 bleiben
`NEEDS_RESEARCH` mit leerem Wert und `UNKNOWN`.

| Firma | Geprüft vorher | Geprüft jetzt | Neu belegt | Weiter offen |
| --- | ---: | ---: | ---: | ---: |
| P03 Upländer Bauernmolkerei | 6/15 | 8/15 | 2 | 7 |
| P10 Oskar Lehmann | 4/15 | 4/15 | 0 | 11 |
| P16 Sembach | 4/15 | 7/15 | 3 | 8 |
| P24 H&K Müller | 2/15 | 9/15 | 7 | 6 |
| P72 Hofbräuhaus Traunstein | 0/15 | 8/15 | 8 | 7 |
| P95 Winkler Bräu, Lengenfeld | 1/15 | 3/15 | 2 | 12 |
| P99 Kunststofftechnik Breitungen | 1/15 | 1/15 | 0 | 14 |

Über alle 100 Firmen steigt der Stand von 549 auf **571 geprüfte Felder**;
**929 von 1.500 Feldern** bleiben offen. Dies ist Quellenprüfung durch Codex,
keine unabhängige persönliche Freigabe und kein endgültiger SME-ETOI-Score.

## Belege und Grenzen

- Upländer: Der eigene historische Bericht bestätigt vorhandenes BHKW und PV.
  Brennstoffe, Inbetriebnahmedaten und Wärmespeicher bleiben offen. Der
  Rohmilchtank ist kein belegter thermischer Energiespeicher.
- Sembach: Die eigene Broschüre belegt CNC-Fertigung, Prozessüberwachung und
  Ofenabwärme für die Produktionsgebäude. Kundenanwendungen im Energiesektor
  sind keine eigenen Energieanlagen. Ofenbrennstoffe und Speicher bleiben offen.
- H&K Müller: Eigene PV, vollelektrische Maschinen, Einzelmaschinenmessung und
  Gebäudebeheizung mit Produktionsabwärme sind belegt. Die PV-Erweiterung war
  für Q4 2025 angekündigt; der vergangene Termin beweist keine Fertigstellung.
  Widersprüchliche Maschinenzahlen werden nicht zu einer sicheren Stückzahl.
- Hofbräuhaus Traunstein: Der datierte Bericht belegt zusätzliche installierte
  PV für Kühlung und E-Stapler; die Palettierung besitzt Roboter, Fördertechnik
  und Qualitätskontrolle. Flächenangaben sind keine kWp-Angaben. Eine gemeinsame
  Stromnutzung beweist keine übergeordnete Energiesteuerungssoftware. Der
  Läuterbottichbericht nennt laufende Bauarbeiten, keine fertige Inbetriebnahme.
- Winkler Bräu: Die vom Anlagenlieferanten verantwortete Veröffentlichung
  belegt eigene Würzekühlung, Pumpen, Abluft und automatisierte Kellersteuerung
  in Lengenfeld. Hotelanlagen und die andere Amberger Brauerei werden nicht
  übertragen. Veröffentlichung 2023 macht eine Anlage von 2017 nicht neu.
- Oskar Lehmann: Die aktuelle Nachrichtenübersicht schließt die fehlenden
  technischen Daten und den offenen KMU-Nachweis nicht.
- Kunststofftechnik Breitungen: Die eigene Maschinenliste nennt Arburg-Modelle.
  Eine allgemeine Herstellerbroschüre für andere bzw. neuere Modelle belegt
  nicht die elektrische Ausführung oder Ausstattung dieser eigenen Maschinen.

Konservativ abgeleitete elektrische Anker tragen Konfidenz C und benennen die
Grenze; spezifische Umrichter, Netzeffekte oder Software bleiben unbewiesen.
Die Investitionsperiode bleibt 2021-10-07 bis 2026-10-07. Geplante Arbeiten,
Veröffentlichungsdaten und Kapazitätsprojekte ohne Energiebeleg werden nicht
als abgeschlossene Energieinvestitionen gezählt. Fehlender öffentlicher Beleg
ist weder nachgewiesene Abwesenheit noch eine Vertriebschance.

## Prüfspur

`field_research_20261008.csv` erfasst alle 87 Feldversuche einschließlich
Ergebnis, gelesener Quellen und verbleibender Datenlücke. Die sieben
Firmendossiers erläutern die einzelnen Entscheidungen. Zwölf neue Quellen
sind im Register ergänzt; neun davon stützen neue Anker. Vier zusätzliche
Quellenkörper dokumentieren ausschließlich die ursprüngliche UNKNOWN-Prüfspur.
Insgesamt bestehen 529 Quellen, 563 URL-Audits und 282 Quellenkörperprüfungen
(279 abrufbar, drei historische Fehler weiterhin sichtbar).

Die unveränderten 554 ursprünglichen numerischen Prüfentscheidungen erhalten
22 zusätzliche `NEW_EVIDENCE`-Einträge. Die eingefrorene Ausgangstabelle bleibt
unverändert. Der Validator verlangt für neue Einträge einen ursprünglich
leeren UNKNOWN-Wert sowie die ursprüngliche Quellenverknüpfung; neue geprüfte
Anker benötigen gelesene, zuordenbare Quellenkörper.

Kanonische Scores, Anlagenflags, Zertifikate, KMU-Gates und unabhängige
Menschenfreigaben wurden nicht verändert. Es wurden keine privaten
Bayernwerk- oder CRM-Daten verwendet. Alle persönlichen Reviewerfelder bleiben
leer. Die Pipeline aktualisiert das Dashboard und die Arbeitslisten; drei
zusätzliche Dimensionsaufgaben wechseln von Recherche zu Geprüft.
