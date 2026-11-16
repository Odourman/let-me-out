# Let Me Out! MAIN III R1o – skott från handen, fyra P0-lägen – partiellt lyckat men FAIL

**Datum:** 2026-11-16. **Forskningsstatus:** **FAIL** för samtliga fyra lilla-kvinnan-X-positioner. **Avgränsat fungerande delbevis:** 310/600 bildrutor från två av fyra P0-lägen. Ingen ändring i main/PR7/verification.

## Proveniens och reproduktion

- Separat forskningsgren `research/main-iii-r1o-single-arm-shot-14rows-20261116`.
- Första körningen [Actions #43836870885](https://github.com/Odourman/let-me-out/actions/runs/43836870885) `FAIL`: M0 vid handen, men extra gul M0-kopia och liten man försköts en rad. Även en trasig höger vägg-rad.
- Andra körningen [Actions #43837276975](https://github.com/Odourman/let-me-out/actions/runs/43837276975) `FAIL`, på testad commit **`b14055c0afcf47b4e437c8f470f03b60540a2cac`**.
- [Evidens artefakt #14211507102](https://github.com/Odourman/let-me-out/actions/runs/43837276975/artifacts/14211507102). Nedladdad ZIP SHA256 `587cfbfaf11f9b5a7549320040862e9eb086cc307edd7e757399dcf690ea9a3e`, CRC PASS, 600 riktiga Stella PNG, CSV och assemblerlisting.
- **16KiB NTSC F6-ROM** SHA256 `41a1b55a4d413cca88eccd690d29b6af1a041e4a354e0f4838a832f10fd6c44d`; exakt R1n14-bas ROM SHA `eb52e6baf37a396acbbf424a7ba937d78ef662cce7a47aff0cda9d9c6cf25558`.

## Tekniken

För att få en specialiserad **en-rads skottkernel** utan att förstöra de 14 visade maskeraderna delas figurbandet i fem topprader, en separat skottrad (GUI y167, Y=8 i 14-bytetabellerna) och åtta slutrader. Samtliga ursprungliga 8x9- och härledda 14-byte-sprite-tabeller är bit-för-bit oförändrade.

- På specialraden används `STA ENAM0` med `FemaleRows14,Y=$FF` (D1 satt) i stället för ursprungliga `BIT FRAMELO` (exakt tre CPU-cykler).
- `STY ENAM0` med `Y=8` (D1 rensad) körs tillräckligt tidigt för att stänga av den andra missilkopian.
- `STX.w GRP1` är en **tvingad absolut fyracyklers X-skrivning** till den lilla mannens GRP1; det ersätter `LDA SmallMaleRows14,Y; STA GRP1` (7 CPU-cykler). På just denna rad har båda små androidbitmaparna samma byte `$3C`; 3 sparade cykler väger exakt upp 3-cykels `STY ENAM0`. Se [DASM manual, force .w](https://github.com/dasm-assembler/dasm).
- M0 flyttas -4 TIA-färgklockor från förra x240 via `HMM0=$40` i blankning och `HMOVE`, till GUI **x232–233, y167**, ungefär en färgklocka utanför spelarhanden.
- 14 rader och **262 NTSC-linjer** bibehålls 600/600.

## Resultat (faktiska Stella-pixlar)

| Testfall | Antal | Resultat |
|---|---:|---|
| Lilla kvinnan på GUI-x330 (läge A), dörr öppen/låst | 150/600 | **PASS alla 150** |
| Lilla kvinnan på GUI-x348 (läge B), dörr öppen/låst | 160/600 | **PASS alla 160** |
| Lilla kvinnan på GUI-x360 (läge C) | 146/600 | **FAIL**: positionsstrobe skjuts på skottraden |
| Lilla kvinnan på GUI-x378 (läge D) | 144/600 | **FAIL**: positionsstrobe skjuts på skottraden och kan överlappa lilla mannen |

- **Totalt strikt pass: 310/600**, ej godkänt som fyra-X-prov.
- **Fem** fullständiga originella androidinstansmasker på samma höjd i **A/B**, utan extrasprites; en gul 14-raders testspelare; **ett enda gult M0-skott x232–233 på y167**, och inga M0-multipelkopior i A/B.
- C/D visar fortsatt fullständiga originalmasker för de andra fyra NPC:erna men en positionsskadad rad hos fjärde NPC. Detta orsakar **19720** vita extrabildpixlar totalt och `ambiguous_fourth_frames=290`.
- Stella verifierar **600/600** konsekutiva frame-ID, **600/600** 262 NTSC-rasterlinjer, **600/600** vänster BALL och rätt höger PF-dörrgeometry.
- En extra missilkopia i A/B efter STY-avstängningen **saknas** i faktiskt råbildsmaterial; inget photoshop eller spriteförenkling.

**Varför C/D brister:** Deras fjärde P0-position skapas genom en sent schemalagd `STA RESP0` på den rasterrad där även M0 behöver släckas före NUSIZ0:s automatiska kopia. Att lägga till den nya 3-cykelsskrivningen **före** denna reset flyttar endast den fjärde androidens kopia på skottraden. A/B:s `STA RESP0` är tidigare och förblir korrekt. För att inte dölja problemet bevaras dessa FAIL-evidenspaket och FULL R1 hålls blockerad.

## Nästa avgränsning

Skapa **R1p** med **endast** de fungerande två diskreta fjärde-P0-lägena (x330 och x348) och dörrens två tillstånd, för ett separat 600/600-giltigt positivt rasterbevis. R1p får inte utropas som löst fyra-X eller sex-NPC-problem. Därefter krävs en annan positionsarkitektur för C/D på samma skottlinje, riktig horisontellt rörlig kula, korrekta kollisionsregler, sjätte mask och all övrig R1/R2-grafik.

**Projektgrind:** R1o fullt FAIL. `main`, ROM DEVELOPMENT:s draft PR #7 och VERIFICATION issue #8 ändras inte.
