# MAIN II – R1b: near57 återvinner alla åtta X-lägen, 600/600 PASS

**Datum:** 2026-11-16. **Evidensklass:** EGENKONTROLL / forskningsdiagnostik, körbar DASM NTSC standard-F6 + Stella 6.7.1 i GitHub Actions. **Inte** slutlig R1, inte oberoende VERIFICATION, ingen ändrad canon.

## Slutligt reproducerbart Actions-prov

- **SUCCESS**: https://github.com/Odourman/let-me-out/actions/runs/43778989092
- Testad commit: `891aacf7a794b213723fe6ed4fa1377442a3ec78` (på `research/main-ii-r1b-near57-eight-x-600-20261116`)
- GitHub Actions artifact ID **14187885296**, `main-ii-r1b-near57-eight-x-600-frames` (624 filer).
- Körbar F6-ROM, exakt **16 384 byte**, SHA256 `56387a908ba6b77f4877febdda2c332594b0f9de940fd9f0e692d56e1031dd1b`.
- Fyra upprepade bankbilder på 4096 byte, byggd med DASM 2.20.14.1; testad Stella 6.7.1, Ubuntu 24.04.
- Artefakten nedladdad och `evidence_600/summary.json`, `frames_600.csv`, källor, `SHA256SUMS.txt` och 600 autentiska råa 900×300-X11-debuggerutskärningar kontrollerade.
- `summary.json`: **`LOCAL_PASS_600`**, tom `frame_errors`.

| Mätpunkt | Faktisk Stellamätning |
|---|---:|
| 600 efterföljande frame-ID (11–610) utan lucka | **600/600** |
| Stella-HUD 262 NTSC scanlines | **600/600** |
| Två samtidigt synliga, OLIKA kompletta originalmasker 8×9, exakt 72 bitpositioner vardera | **600/600** |
| Båda observerade X-positionerna korrekta mot åtta programstyrda varianter | **600/600** |
| Gul P0-spelarkandidat | **600/600** |
| Gult M0-projektiltest | **600/600** |
| Oförklarade vita GUI-pixlar utanför de två maskerna | **0 totalt** |
| Kontrollerade två-mask-/X-formationer | **8 olika** |

## Åtta faktiskt hållbara par

| A-delay | B-delay | Stor man, rå GUI-X | Stor kvinna, rå GUI-X |
|---:|---:|---:|---:|
| 1 | 1 | 196 | 310 |
| 2 | 1 | 226 | 340 |
| 3 | 1 | 256 | 370 |
| 1 | 2 | 196 | 340 |
| 2 | 2 | 226 | 370 |
| 3 | 2 | 256 | 400 |
| 1 | 3 | 196 | 370 |
| 2 | 3 | 226 | 400 |

GUI-X är 1366×900 Stellas råskärmbildkoordinater. Varje 30 GUI-pixels förflyttning här är 15 TIA color clocks. Samtliga åtta testkombinationer visades under upprepade bildrutor (64–80 i denna 600-rutorssekvens).

## Därför är detta en teknisk förbättring och inte en tillbakadragen FAIL

Ursprungliga 69-CC-kerneln med 6-cykels efter-RESP-väntan gav 270 rasterlinjer och förlorade masker/skott för fördröjningskombinationerna `(3,2)` och `(2,3)` vid 144/600 bildrutor. Det var ett **verkligt FAIL för den äldre ROM:en**; se separat rapport på `research/main-ii-r1b-xmatrix-600-20261116`.

Det efterföljande `near57`-experimentet tog bort fyra CPU-cykler genom att ersätta den sexcykels väntan med en **2-cykels NOP** innan `GRP1` laddar kvinnans rad. Stella-kontrollerat: vid `A=B=1` är första `STA RESP1` före-instruktionscykel 28, `STA GRP1` cykel 37, andra `STA RESP1` cykel 47, rasterrad 119, bank 0. Därmed är nominellt **57 TIA-färgklockor** mellan RESP1-skrivningarna.

Fyra separata råbilder bevisade att 57-CC-varianten i sig bevarar maskerna. 51-CC-varianten (helt borttagen mellanväntan) gjorde i stället att manlig första kopia fick kvinnans bitmap (18/72 fel) vid alla fyra placeringar; nära-51-provets FAIL är bevarat i `research/main-ii-r1b-near-copy-20261116`. Detta indikerar en verklig timing-/latchgräns för just detta kodschema, men ingen universell hårdvarugräns är påstådd.

Slutkörningen visar nu att **alla åtta** X-lägen fungerar över 600 faktiska bildrutor med det nya kodschemat. Att 57-CC-varianten löser ett problem betyder **inte** att den äldre 69-CC-variantens negativa observationer var felaktiga.

## Kända avgränsningar och MAIN-status

- Beviset gäller **2** olika originalmasker vid samma Y, en temporär gul P0, ett M0 och åtta **grova** X-par. Avståndet 57–87 färgklockor är inte näröverlappning eller godtyckligt fritt X.
- Inga tre till sex samtidigt renderade NPC:er, ingen PF-vägg-/rumbudget, ingen R2 fem NPC + nyckel/O1, ingen rättvis kollisions-AI/poäng/HUD, PAL eller riktig Atari-hårdvara.
- Originalets fyra masker är inte ersatta; användarens godkända gameplay får inte förenklas automatiskt.
- Ingen oberoende verifiering av en ny commit har gjorts. GitHub draft PR #7 och Issue #8 får inte ärva dessa tvåfigurspass.
- `main` och ursprunglig ROM-baslinje får inte ändras av denna forskningsleverans.

**MAIN II:** Detta är nu den bästa reproducerade lokala tvåmaskerskerneln. Nästa tekniska grind är att undersöka om fler än två originalsilhuetter kan existera utan att omtolka godtyckligt X eller godkända masker. En annan cart mapper är fortfarande utanför standard-F6-ramen. Inget 3→6-skalnings-PASS är fastställt.
