# Eine 34-Umfärbungs-Schranke um eine veröffentlichte Schur-Partition von [1,536]

Fredricksen und Sweet veröffentlichten im Jahr 2000 eine summenfreie Zerlegung von [1,536] in sechs Farbklassen und bewiesen damit S(6) ≥ 536. Wir haben die sechs abgedruckten Listen positionsgenau mit der Originalarbeit abgeglichen und die daraus konstruierte Färbung rechnerisch geprüft: Alle 536 Zahlen erhalten genau eine Farbe, und keines der 71.824 möglichen Tripel x ≤ y mit x+y ≤ 536 ist einfarbig.

Für diese **konkrete, beschriftete** Färbung zeigen wir eine lokale Schranke. Jede gültige Sechsfärbung von [1,537] müsste gegenüber ihr mindestens 34 der ersten 536 Farben ändern. Für die Farbe von 537 erzwingen 32 disjunkte gleichfarbige Paare mindestens je eine Änderung; alle anderen Farben erzwingen mindestens 35. Falls höchstens 33 Änderungen erfolgen, bleibt außerhalb der 64 Paarendpunkte höchstens eine weitere Änderung möglich. Beim Paar (9,528) ergeben sich für jede mögliche Umfärbung eines Endpunkts zwei Tripelzeugen mit disjunkten übrigen Zahlen außerhalb dieser Endpunkte. Um beide zugleich zu beseitigen, wären dort mindestens zwei Änderungen nötig. Das beweist die Schranke 34.

Die Aussage betrifft ausschließlich den Abstand zu dieser beschrifteten Referenzfärbung. Sie liefert weder eine Färbung bis 537 noch einen neuen globalen Wert oder eine neue Schranke für S(6). Das englische Manuskript enthält die vollständige Tabelle mit 20 Tripeln; JSON-Daten und deterministische Python-Prüfprogramme liegen im Paket bei.

**Urheberangabe:** Beedbyte, School Scotty. **Datum:** 8. Oktober 2026. **Korrespondenz:** beedbyte@3g-projects.de.
