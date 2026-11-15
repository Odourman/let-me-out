# MAIN v0.10 – Labyrint C01 kontra C02

**Status:** Offlineförstudie, inga nya kartbeslut, ingen ROM-implementation eller Stella-verifiering.

## Vad föreslås?
Rum C02 tar bort exakt åtta väggceller från C01, i två symmetriska öppningar:
- x 8–9 och x 30–31, y 10–11 i den föreslagna 40×22-kartans nollbaserade cellkoordinater.
- A01, B01 och D01 föreslås ligga kvar oförändrade. D02 har ingen tydlig vinst i tillgängliga tester.

## Geometriska mätvärden (2×2-objekt, 4-riktnings-BFS)
| Mått | C01 | C02 |
|---|---:|---:|
| Antal fria 2×2-fotfästen | 465 | 471 |
| Antal från start nåbara fotfästen | 465 | 471 |
| Kortaste väg från vänsterstart till högerdörrens insida (logiska steg) | 41 | 35 |
| Medelavstånd vänsterstart till 18 ursprungliga robotspawns (logiska steg) | 24,444 | 22,667 |
| Medelavstånd ursprungliga robotspawns till dörrinsidan (logiska steg) | 22,056 | 20,778 |

**Viktigt:** Alla mått använder en förenklad 2×2-gridmodell, utan verklig pixelgeometri, diagonalrörelse, skott, växelverkande androider, åtskilda animationer eller Atari TIA-timing.

## Tidigare v0.8 AI-prov
Sex androider patrullerade 36 abstrakta steg och jagade därefter en stillastående spelare nära utgången under 96 steg, 32 slumpstarter per kartvariant.
- **C01:** i genomsnitt 3,81 av 6 androider kom inom två logiska cellsteg från spelaren.
- **C02:** i genomsnitt 5,94 av 6 kom så nära.

Det gör C02 mer robust mot att enkel AI blir blockerad bakom hindren. Samtidigt kan C02 vara *svårare för spelaren*, eftersom fler jagande androider når fram. Det går inte att avgöra spelbalansen utifrån dessa offline-resultat.

## MAIN:s rekommendation
Ta **C02** vidare som primär *testkandidat*; lås inte C02 som slutlig karta utan senare uttryckligt beslut och spelbart test. Behåll **A01, B01 och D01** oförändrade som jämförelsegrund. ROM-kodningspausen gäller.

## För att reproducera
- [Drive-arkiv v0.10 (9 filer)](https://drive.google.com/file/d/13JHPwn11DtoCcPQupKlPMengz0hQQShE/view?usp=drivesdk) med exakt kart-JSON, geometrikontrollskript, CSV, logg, illustration och manifest.
- [Ursprungligt beslutsunderlag](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).

**Projektgräns:** detta gäller endast Let Me Out!. Linear används inte. The Cabin och I Love a Fish påverkas inte.
