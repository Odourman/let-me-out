# LET ME OUT! – MAIN V till ROM DEVELOPMENT II
## R1-F6: TWO-MASK HBLANK → VISIBLE COPY START DIAGNOSTIC

**Auktoriserad 2026-11-16 av MAIN V som en NY, separat, extremt smal v0.18 NTSC R1-diagnostikorder** inom användarens befintliga NTSC/F6/R1–R4-undersökningsscope [Issue #6](https://github.com/Odourman/let-me-out/issues/6). **Detta är INTE tillstånd till ny full sexandroidskernel, återaktivering av R1ba, spritefixar, spelprogrammering eller annan implementeringsfas.**

### 0. Läs bindande källor och kontrollera commit

1. [MAIN V F5-mottagning + oberoende R1ba orienteringsmotbevis](MAIN_V_R1_F5_RECEIPT_R1BA_VERTICAL_ORIENTATION_INDEPENDENT_AUDIT_2026-11-16.md), [F5 fryst `953c6c5`](https://github.com/Odourman/let-me-out/blob/953c6c5ef20e83d93474de4c094de784761da257/docs/ROM_DEV_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_TO_MAIN_2026-11-16.md) §7, F4 `2218e583`, F2:s enda rörliga index2 och NUSIZ1=$01.
2. [Låsta original-NPC-masker](../design/NPC_REFERENCE_8x9_masks.json), blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. **RITNINGEN MÅSTE SYNAS TOP-DOWN I EXAKT SIN REFERENSORDNING.** Den historiska R1ba-kerneln hade **fyra STORA omvända** masker; dess green 600/600 är inte pixel-PASS mot canon och **får inte** användas som fixture eller utvärderingsoracle. M/F bitmapbyte får aldrig "korrigeras" i originalkällan.
3. [F5-HBLANK/R1ba 30 trick READ-ONLY](MAIN_V_F5_SOURCE_ONLY_CROSSCHECK_HBLANK_R1BA_AND_30_TRICKS_2026-11-16.md); Andrew Towers TIA Hardware Notes och Stella 6.7.1 TIA/Player/DrawCounterDecodes med **CPU-STA**, intern reset och START/GRP-latch strikt åtskilda.
4. [R1-kriterierna](ROM_GATE_V018_ACCEPTANCE.md) inklusive A/B/C/E, [gällande MAIN state](CURRENT_PROJECT_STATE_2026-11-15.md). Sex-NPC C01/C04 förblir blockerade oavsett F6:s tvåmaskersutfall.
5. Säkerställ att **PR #7 fortfarande draft/omerget**, Issue #8 standby. Ingen ändring av dem.

### 1. EN enda testbar teknisk fråga

I samma korta **nio synliga rasterrader**, och **en enda** P1 med `NUSIZ1=$01`, kan **första** av två skilda originalmasker (stor MAN och stor KVINNA) förflyttas på faktisk X genom att flytta dess `RESP1` från tidig **c21** (HBLANK) till **c23** (efter HBLANK) **medan den andra `RESP1` förblir vid c32 och andra maskens synliga X förblir oförändrad**?

F5:s **kalibrerade, ännu inte oberoende bevisade** screenshot-prediktioner: `(X0,X1)=(43,99)` för c21/c32, respektive `(45,99)` för c23/c32 i 900×300 Stella-debuggercrop. **Fysisk huvudgrind** är dock faktisk x0-förflyttning med oförändrad X1 och två helt rättvända originalmasker i alla 9 rader; ett litet avsteg från kalibrerad X45 får förklaras, inte godkännas genom efterhandsanpassad mål-X. Även full positiv tvåmaskersgeometri är bara `F6_TWO_MASK_HBLANK_PHASE_LOCAL_PASS`, **inte** två fritt kontrollerbara runtime-X, och aldrig full R1.

### 2. G0: obligatorisk SOURCE-ONLY, ny bygge först om faktiskt möjligt

Ny **isolera forsknings-/ROM-diagnosbranch** från frysta F5 `953c6c5ef20e83d93474de4c094de784761da257`, inget röra F5/F4/F3/F2-filer. Endast `r1_f6_*` källor/skript och rapport `rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F6.md`. Använd originella per-rad M/F-maskrader från top-down canon. Få till exakt två nio-radersmasker, utan clipping, inversion, blandning, spökobjekt, korrupt P0/M0/PF eller fler 8×9-varianter.

**Före första ROM-bygget**, räkna verkliga 6502-cykler rad0–8 för **två** registerplaner `RESP1[0]=c21 / RESP1[1]=c32` och `RESP1[0]=c23 / RESP1[1]=c32`, inkludera `GRP1`, `NUSIZ1`, `WSYNC`, `HMOVE`/HBLANK, föregående/nästa rad, player P0, static missile M0 om de kan bevaras, PF och minst **76-cykels** faktisk safety. Om ena planar har noll eller negativ cykelmarginal eller kräver annan game/layout/mask waiver: **STOPP: `F6_SOURCE_ONLY_INFEASIBLE`**, inga kompilerade nya ROM. F6 får använda mindre antal NPC än sex endast därför att testet är isolerad *hårdvaruorsaksdiagnostik*, inte ett ersättningsspel eller C01-test.

### 3. G1: som mest TVÅ faktiska, frysta och körbara standard-F6/NTSC ROM

1. Bygg först **c21/c32 baslinje** från den förregistrerade källplanen.
2. Bygg sedan **c23/c32 variant** endast om baslinjen visar **båda korrekt rättvända, fullt separata 8×9 originalmasker på samma nio rasterrader**, korrekt programmerad `RESP1/GRP1`, ursprunglig X enligt baseline eller dokumenterad avvikelse som fortfarande medger diskriminerande prediktion, P0/M0/PF om användaren redan kan se dem, inga ghostpixlar och stabila **262 NTSC rasterrader**. **STOPP** om baseline mask-/TIA-/scanline-korrupt. Sammanlagt **högst två binärer** och inga alternativa c22/c24/c25/c28/c30-svep, NUSIZ-varianter eller R1ba-ombuild.
3. Kräv **16 konsekutiva autentiska Stella 6.7.1-raw-bilder per faktisk byggd ROM** efter stabil init och minst en faktisk GUI-debugger-trap per `RESP1` och `GRP1` i kritisk rad med verkliga scanline/cycle/PC/TIA-colorclock/bank. Undvik att kalla någon beräknad cykel för `MEASURED`. Fulla 900×300-crops och uncropped debuggerbild, 262-NTSC-HUD, perbild-SHA256, körbar ROM/SHA, ASM, DASM .lst/.sym och byggkommandon.
4. Kontrollera båda maskernas **TOP-DOWN** `M=3C 3C 18 FF 18 24 24 42 42`, `F=3C 3C 18 FF 3C 7E 7E 24 24`. P1 masking måste stämma mot **aktuell låst GitHub-sprite** direkt, **aldrig** inverterat `[::-1]`. Både ett råpixelunionstest från source-canon och ett sekundärt oberoende maskcheck samt minst EN märkt syntetisk negativ mutant behövs. `white_missing=0`/`white_extra=0` per bild i **båda** lägena.
5. Få fram en sanningstabell `requested first X`, `measured first X`, `requested second X`, `measured second X`, med förregistrerade prediktioner. Särskilj `NO_RESPONSE`, `FIRST_MASK_LOST`, `SECOND_MOVED`, `PIXEL_ORIENTATION_FAIL`, `NTSC_TIMING_FAIL`, `SOURCE_ONLY_INFEASIBLE` och `LOCAL_PASS`.

**HÅRD STOPPGRIND:** om första/mellersta felaktiga mask, försvunnen stor figur, spökpixel, flyttad andra X, korrupt scanline eller förlorad P0/M0/PF i en omfattning som ingick i G0-stipulation, sluta omedelbart, inga fler variant-/felfixar utanför max TVÅ; sammanfatta vilka signaler som kan ha fallerat. Även vid PASS stannar F6: inget kombinerat runtime-X, ingen sex-NPC-ROM, ingen R1ba-rättning, inget F7.

### 4. Leverera och STOPP

Leverera **en** fryst `TO_MAIN_R1_F6.md` på isolerad branch med testade exakt två registerplaner, explicit source-only förkontroll, båda binärernas SHA256/size/bankkopior, 16 per ROM autentiska Stella och TIA-trap-bevis, all PNG-hash/manifest/ZIP-CRC, verklig evidens-ZIP i korrekt Google Drive-projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`, exakta GitHub Actions-ID (röda/gröna) och en sammanfattning om vilken START-modell som blivit falsifierad. **Ingen efterhandskorrigering av teoriprediktionen eller av top-down-canon**.

Rapportera endast `F6_TWO_MASK_HBLANK_PHASE_LOCAL_PASS`, `F6_TWO_MASK_PHASE_LOCAL_FAIL`, `F6_SOURCE_ONLY_INFEASIBLE` eller `F6_INCONCLUSIVE`, samt uttryckligen `F6_TWO_INDEPENDENT_RUNTIME_X_NOT_RUN / SIX_INDEPENDENT_XY_NOT_RUN / FULL_R1_BLOCKED`.

**Inga R2/R3/R4, GAME OVER, KEY, HUD, PAL, mapper-F6SC/ARM, nya originalmasker, GRAPHICS, fullspel, PR #7 merge, äldre Verification Issue #8-godkännande eller fortsatt ROM-implementation.** R1-F6 är en **enstaka förregistrerad hypotesdiagnos**, inte en accepterad teknisk arkitektur. MAIN måste separat besluta om något efteråt.
