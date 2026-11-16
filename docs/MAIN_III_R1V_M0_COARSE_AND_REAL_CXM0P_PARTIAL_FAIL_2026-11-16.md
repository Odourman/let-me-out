# LET ME OUT! MAIN III R1v – grövre M0-positionsbyte och verklig CXM0P-överlappning

**Datum 2026-11-16. FULL R1v RESEARCH-RESULTAT: FAIL (456/600 PASS).** Det finns ett separat positivt underresultat för verklig TIA-hårdvarukollision. Ingen produktionsintegration eller oberoende VERIFICATION.

## Teknik och testat oförändrat scope

- Research branch `research/main-iii-r1v-resm0-coarse-overlap-20261116`.
- [**GitHub Actions #43845730545**](https://github.com/Odourman/let-me-out/actions/runs/43845730545) på tested commit `9ba05d5614b650caf083f447cee92a77f564b09a`: **FAIL**, trots att DASM byggt 16KiB F6 och Stella spelat in 600 löpande frames; själva pixelgranskningen rapporterar nedanstående faktiska begränsning. Äldre [#43845669937](https://github.com/Odourman/let-me-out/actions/runs/43845669937) fångade samma bilder, men audit stoppade på en Python-variabel som beräknades i fel ordning; detta åtgärdades innan den fullständiga granskningen.
- [**Fullständigt råevidenspaket #14215955286**](https://github.com/Odourman/let-me-out/actions/runs/43845730545/artifacts/14215955286), 623 ZIP-poster inklusive 600 råa Stella-PNG, ROM och `summary.json`; ZIP SHA256 `8d10885523b83a2e77f45d219eca400730761f39395796c935e29f540e6e59df`, CRC PASS.
- Byggd utifrån exakt R1u SHA256 `ba06c63fd2247a4dfd47b5baa5619271c3ac851859c3ba3ca516bd4c227fc2e7`.
- R1v-ROM 16 384 byte vanlig F6 NTSC, SHA256 **`0110ae7cdf33aee5af75b008c2cdd091bffc3abce85dc3b43a0bcc3f07c3ffe3`**.
- Tre CPU-cykler `BIT FRAMELO` införs **utanför synlig kernel**, just före blankningens `STA RESM0`; detta flyttar missilens grova grundposition **9 TIA color-clocks = 18 GUI-pixlar**, utan att ändra andra sprites, deras tabeller eller fyra rasterlägen. `HMM0` ger som tidigare ytterligare åtta finpositioner, nu GUI-x250,252,254,256,258,260,262,264 på GUI-y167.
- TIA:s verkliga `CXM0P` (read register $00) maskeras med bit7 `#$80`; det avlästa värdet skrivs enbart till diagnostisk bakgrund `COLUBK` **efter NPC-bandet**, och `CXCLR` nollställer collision-latchen för nästa frame. Den markerade efterföljande skärmregionen är **blå vid kollision**, annars **svart**. Detta är instrumentering, inte godkänd gameplay-kollisionskod.

## Faktiskt Stella-resultat, fail-closed

| Test | Resultat |
|---|---:|
| 600 sammanhängande autentiska Stella 6.7.1 frame-ID | 600/600 |
| NTSC 262 scanlines | 600/600 |
| Fem ursprungliga 8×9-NPC-maskinstanser utsträckta till 14 visningsrader, 4 fjärde-P0-X | 600/600, med bullet-överlagrade pixlar undantagna endast vid exakta bulletpositioner |
| Vänster BALL-vägg, höger PF0-dörrs 32 scanlines, två dörrlägen | 600/600 |
| Kula korrekt ensam vid GUI-y167 på förväntat X, utan extrakopior och extra pixlar | **456/600** |
| Kula osynlig på förväntad X på grund av för tidig `STY ENAM0` i vissa rasterlägen | **144/600 FAIL** |
| Totalt extra vita/gula spökpixlar | 0 / 0 |
| Hårdvarudiagnos `CXM0P` D7 när synlig M0 överlappar första kvinnliga P1 vid x250–262 | **417 autentiska frames** med blå kontaktindikator |
| Ingen aktiv kontakt vid sista X x264 eller då skottet uteblir | **183 frames**, svart indikator |

**Väsentlig ny teknisk kunskap:** M0 och den första kvinnliga P1:s originalmask sammanfaller på rasterrad GUI-y167 när den aktuella projektilen syns inom x248–263. Även om den gula pixeln visas över vit P1 fungerar TIA:s faktiska hårdvarukollisionslatch. `CXM0P` D7 skilde korrekt på kontakt (RGB `0,0,138`) och frånvaro av kontakt (RGB `0,0,0`) i de 600 verkliga bilderna. **Inget bevis för identifierad enskild android som gameplay-hit:** multiplexad P1 kan vara andra logiska NPC i senare fall.

**Varför full R1v underkänns:** När M0 flyttas till de senare positionerna i det grövre fönstret släcks M0 i de sena fjärde-P0-lägena C och D innan skottets position har nåtts. Vissa faser visar därmed ingen projektil alls. Resultatet visar en verklig cykelgräns, inte ett testskripts koordinatfel.

## Nästa försök R1w (forskningshypotes, ingen PASS-claim)

Retima skottraden **utan att ändra antal cykler**, så M0 avaktiveras senare, men innan `NUSIZ0` kan skapa en extra kopia. Samtidigt ska de viktiga `RESP0`-strobefönstren C=c53 och D=c56 hållas intakta med hjälp av att bitmapen `GRP0` kan skickas tidigare/senare. Kandidat OFF-tider A/B=c56, C=c56, D=c53 ska testas strikt med 600 Stella-bilder och **alla 64 kombinationer**. Tidigare R1q demonstrerade att för sen avstängning kan skapa gula/vita missilkopior. Om R1w misslyckas är det ett legitimt resultat; ändra inte acceptanskraven.

**Gräns:** Hittills inte ett fullskärmsskott, inte eldknapp, inte skottlogik eller validerat ID på träffad android; fem (inte sex) NPC, endast fyra diskreta fjärde-P0-X. Full R1 FAIL/BLOCKED. `main`, ROM DEVELOPMENT:s draft PR #7 och fristående VERIFICATION issue #8 är orörda.
