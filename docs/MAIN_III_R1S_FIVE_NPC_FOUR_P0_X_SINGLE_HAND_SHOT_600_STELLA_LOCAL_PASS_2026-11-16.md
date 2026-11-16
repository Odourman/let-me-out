# LET ME OUT! – MAIN III R1s: FEM originalandroider + fyra P0-X + en ensam handprojektil

**Datum 2026-11-16. Status: `LOCAL_PASS_R1S_FOUR_P0_X_SINGLE_HAND_SHOT_600` (endast isolerat forskningsprov). Full R1 fortfarande FAIL/BLOCKED.** Inget nytt steg i ROM DEVELOPMENT har auktoriserats. Ingen oberoende VERIFICATION har utfärdats.

## 1. Exakt testat och körbart utfall

**GitHub Actions [#43839484192](https://github.com/Odourman/let-me-out/actions/runs/43839484192) = SUCCESS**, commit **`3b0640c2545417feb917c2fe8b28d484badca60d`**, research branch `research/main-iii-r1s-early-m0-off-delayed-grp0-4x-20261116`. Fullt byggbar Python-generator, DASM-listing och Stella 6.7.1/X11-evidens finns i [Actions-artefakt #14212826623](https://github.com/Odourman/let-me-out/actions/runs/43839484192/artifacts/14212826623).

| Evidensparameter | Exakt värde |
|---|---|
| ROM | **16384 byte, standard F6, NTSC**; fyra identiska 4096-byte-banker |
| Exakt ROM SHA256 | **`33ab04b95ca6f649593e50082bf17275b605caea282e6e044aeb49abf93d1d85`** |
| Nedladdad full evidens-ZIP SHA256 | **`f4db03f4acc72d488977c2805668622367f642bcd5f4c0de346ea305e823206e`** |
| ZIP | 623 arkivposter, därav 600 **råa** frame-PNG från verklig Stella-debugger, + initial/final X11-bilder; ZIP CRC PASS |
| Verkliga Stella-frame-ID | **600/600 i obruten sekvens** |
| NTSC 262 rasterlinjer | **600/600** |
| **Fem** 14-radersvisade oförändrade originalandroid-instansmasker | **600/600** |
| En gul, 14-radersvisad temporär spelare | **600/600** |
| **Exakt en** gul M0-projektil, GUI **x232–233, y167**, intill handen | **600/600** |
| Förra felaktiga M0-raden y160 | **0 pixlar, 600/600** |
| Automatisk M0-spökkopia vid GUI x296 | **0 pixlar, 600/600** |
| Yttervägg vänster via BALL + asymmetrisk PF0-högervägg och rätt 32-raders dörröppning | **600/600** |
| Fyra olika fjärde-P0 GUI-X | **x330, 348, 360, 378; alla godkända** |
| Samtliga P0-X × dörr öppen/stängd-kombinationer | **8/8** |
| Totalt extra vita och gula pixlar | **0/0** |
| Strikt underkända Stella-bildrutor | **0** |

Exakta fördelningar:
- x330: **150** frames; x348: **160**; x360: **146**; x378: **144**.
- P0-X × dörr: `pre_mask_locked=70`, `pre_mask_open=80`, `post_mask_locked=80`, `post_mask_open=80`, `post_lda_locked=80`, `post_lda_open=66`, `post_color_locked=80`, `post_color_open=64`.

## 2. Varför R1s lyckas där R1o och R1q misslyckas

Samma fem-NPC-kernel på samma 14 fysiska rasterrader, samma 8×9 originalmask-tabeller och samma genererade 14-byte visningstabeller. **Alla tidigare originalgrafikbytes är oförändrade**, liksom A/B:s avfyrningsrutiner. R1s ändrar bara **ordningen på redan befintliga CPU-skrivningar för de två sena fjärde-P0-X-lägena C och D**.

R1o [Actions #43837276975](https://github.com/Odourman/let-me-out/actions/runs/43837276975) hade M0 avstängd tidigt, men `STY ENAM0` lades **före** de sena `STA RESP0` och flyttade då en vit maskrad åt höger i C/D. Det gav bara **310/600** godkända frames.

R1q [Actions #43838985789](https://github.com/Odourman/let-me-out/actions/runs/43838985789) flyttade i stället `STY ENAM0` **efter** sena `RESP0`. Då var **samtliga 600** fem-NPC-masker korrekta och alla fyra P0-X fanns, men M0 hann automatiskt dupliceras via `NUSIZ0=$02`:
- C (146 frames): 2 extra **gula** pixlar per frame = **292** gula spökpixlar.
- D (144 frames): 2 extra **vita** pixlar per frame = **288** vita spökpixlar.
- R1q total strikta PASS: **310/600**, alltså inte acceptabelt.

**R1s löste konflikten med följande cykelneutrala omordning efter kvinnans andra P1-`RESP1` vid CPU c45:**

| Cykel efter `WSYNC` | C: GUI-x360 | D: GUI-x378 |
|---|---|---|
| **c48** | `STY ENAM0`: avaktivera extra M0 | `STY ENAM0`: avaktivera extra M0 |
| c50 | `LDA #$0E` | `LDA #$0E` |
| **c53** | `STA RESP0` (oförändrad C-position) | `STA COLUP0` |
| **c56** | `STX GRP0` (flyttad senare) | `STA RESP0` (oförändrad D-position) |
| c59 | `STA COLUP0` | `STX GRP0` (flyttad senare) |
| c63 | `STX.w GRP1` (liten mans originalbitmap) | `STX.w GRP1` |
| c66 | `STA RESP1` (liten mans P1-position) | `STA RESP1` |

**Varför:** TIA behöver `RESP0` på exakt rätt cykel för fjärde P0-positionen men behöver inte dess aktuella `GRP0`-bitmap **förrän de riktiga spritepixlarna ska visas**. För C startar den lilla kvinnan senare än c56; för D ännu senare än c59. M0:s ursprungliga projektil vid x232 har redan hunnit ritas innan c48, men dess automatiska 32-CC-senare kopia har inte hunnit börja och stängs därför av säkert. Alla P1-dubbelkvinnor, P0-gulspelaren, fjärde P0-lilla kvinnan och tredje P1-lilla mannen bevaras.

Inga extra CPU-instruktioner eller specialmapper, DPC+, extra RAM, ARM, flicker eller visuellt maskbyte infördes. C/D:s **totala cykelantal och viktiga reset-faser är oförändrade**; endast registerskrivningarnas ordning har ändrats.

## 3. Separat lokal återanalys av nedladdad evidens

MAIN III laddade ned exakt Actions ZIP och kontrollerade:
1. SHA256 och ZIP CRC. ROM lästes ut ur ZIP och SHA256 matchade `33ab04b95...`; 16 384 byte.
2. Samtliga **600 verkliga rå-PNG** är i förväntat 900×300-format.
3. Samtliga **600 CSV-rader är `local_pass=True`**, shot-exakt-2-GUI-pixlar på x232–233/y167, inget gammalt y160-skott, ingen extra missile x296.
4. Spelytan i varje Stella-bild bildhashades byte för byte. **Exakt 8 olika, stabila bildhashar för 8 P0-X/dörrkombinationer**, **en** stabil scenhash per kombination och ingen hash delades mellan två tillstånd.

Detta är en tekniskt oberoende **omkontroll av levererade data**, men **inte** organisatoriskt oberoende VERIFICATION. Den skärmbild som visas för MAIN är från riktig Stella-ROM (visad med korrigerad NTSC 4:3-aspekt, pixelperfekt närmsta granne); inga figurer eller skott har bildgenererats.

## 4. Exakta begränsningar och authority gates

**DET SOM NU ÄR LÖST I ISOLERAD FORSKNING:** fem hela tidigare bevisade originalandroidinstanser, 14-radersvisualisering, fyra diskreta P0-X-lägen, en ensam avsiktlig M0-punkt direkt vid spelarhanden, 32-raders högerdörr, vänster BALL-vägg, 262 NTSC, alla åtta kombinationer.

**DET SOM INTE ÄR LÖST:**
- Fortfarande **fem, inte sex**, NPC:er: andra stora mannen saknas.
- Fjärde P0 har **fyra diskreta X** – inte full fri rörlighet över 160CC. De två stora kvinnorna har fast nära P1-fas / är inte oberoende från varandra.
- Skottet är **STATISKT** i detta prov. Eldknapp, projektilens X-förflyttning, projektilhastighet och riktning, fler skotthöjder, NPC-rörelse under eld samt **kollisionslatchar/inga falska träffar** är **inte** testade. Att inga extra pixlar syns räcker inte för att fullgodkänna kollisioner.
- 14-raders upprepad representation av godkända ursprungliga 8×9-byte-masker är bara estetiskt forskningsprov; ingen designcanon har ändrats.
- Endast brun högerdörröppning (öppen/stängd), inte komplett orange låst port/svart nyckelhål; ingen full 40×22-karta, nyckel eller PAL.
- **Full R1, R2–R4 och oberoende VERIFICATION kvarstår FAIL/BLOCKED.**

**Integritet:** `main` och ROM DEVELOPMENT:s draft PR #7 är oförändrade; separat VERIFICATION issue #8 påverkas inte. Inget arbete i senare implementation scope har påbörjats med hänvisning till detta forskningstest.

## 5. Rekommenderad nästa forskningsgrind

**Separat R1t (ännu inte testad):** prova en faktiskt rörlig kula som börjar vid x232–233/y167 och skjuts horisontellt medan fem originalandroider och fyra diskreta P0-positioner rör sig inom aktuella begränsningar. För att testa en dynamisk missile måste `HMM0`, `HMOVE` och M0-positioneringen analyseras noggrant i VBLANK, utan att modifiera de kritiska P0/P1-strobefaserna. Utveckla särskilt oberoende collision-latch-test via `CXM0P` och synliga falska kopior under positionsstress, innan något accepteras som spelmekanik.

**Användarkrav:** ingen skjutpose eller animation behövs. Skottet måste komma i höjd med spelarens hand, inte huvudet, med exakt en projektil.
