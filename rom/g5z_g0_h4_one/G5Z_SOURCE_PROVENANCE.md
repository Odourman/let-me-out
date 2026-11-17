# G5Z SOURCE PROVENANCE – ROM DEVELOPMENT III / 2026-11-17

**Avgränsning:** G5Z Issue #12, endast full H4-ONE source-only preflight. **Utfall:** `G0_INCONCLUSIVE_NO_ROM`; ingen kod, DASM, Stella, CI, G1/G6/F12, eller oberoende Verification.

## 1. Faktiska förstahandskontroller
- GitHub-anslutningen hämtade [Issue #12](https://github.com/Odourman/let-me-out/issues/12), dess fullständiga body och kommentarer (0 vid start); GitHub `main` frystes för denna analyssnapshot till commit **`2421aa9eb49a10a618f030ef282f1bebc268eac0`** (main HEAD 2026-11-17 18:19:50Z). En isolerad `rom-dev-iii/g5z-g0-h4-one-source-only-20261117` branch skapades **från exakt detta commit**; inga äldre käll- eller grafikfiler modifierades.
- Google Drive-anslutningen listade officiella projektmappen [Let Me Out! Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) live och läste G5Z originalets native Google Doc, [länk](https://docs.google.com/document/d/15cWPUaLAzo-LP131WjTNCmHNsCrOWY9Ii9EAZ2hbmz0/edit), med samma G5Z-title, mandat/status och hela dokumentets 62 stycken. Detta är en readback av arbetsordern, inte en ny auktorisation.
- Alla beräkningar är manuell/deterministisk **text- och kostnadskalkyl** av publika assembleropcodes och maskbytes. Inga operativa ROM-/emulator- eller CI-mätvärden har producerats.

## 2. Projektets primära GitHub-källor (repo `Odourman/let-me-out`)
Alla nedan för G5Z/G4/G3/G5H/G5Y/G5X/masker är lästa på den exakta tidigare `main`-snapshotten `2421aa9eb49a10a618f030ef282f1bebc268eac0`; **sha är Git blob SHA-1, inte påstådd ROM SHA-256**.

| Källa | Faktiskt uppmätt Git blob SHA-1 | Funktion |
|---|---|---|
|[G5Z bindande order](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md)|`09f5d823e42cfe195af81845ab313006237a4a88`|Scope, uppdragsgränser, tre slututfall|
|[G4 H4-ONE prereg](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md)|`10fd29a5facf47bda6ff22237a2137398c433189`|A1/A2/B1/B2/X1/X2/M1/P1, Y och maskregler|
|[G4 event-timeline](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G4_REGISTER_TIMELINE_2026-11-17.csv)|`abf12a03dd964ee9d7394e782e3064f98a0a54c2`|Explicit okända CPU-/START-effektfaser|
|[G4 GO/NO-GO](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G4_ONE_EXPERIMENT_GO_NOGO_DECISION_2026-11-17.md)|`584396af3229a33c992de4bb750e1fc595177003`|En enda fysikhypotes, ej ROM-order|
|[G5Y testplan](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5Y_MAIN_VII_FALSIFIABLE_HARDWARE_TEST_PLAN_H4_ONE_S05_FIVE_NPC_NOT_AUTHORIZED_2026-11-17.md)|`ce1a46e66a846d3cf09e06c0e9509827a91f8eee`|Separerar H4/N0, S05, fem NPC|
|[G5Y 17 testfall](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5Y_MAIN_VII_PREREGISTERED_TECHNICAL_TEST_MATRIX_NOT_AUTHORIZED_2026-11-17.csv)|`a3e809d751b62708b9a828ee811614100c5c1a81`|Förregistrerade input och historisk NOT_RUN|
|[G3 resurskontrakt](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md)|`77cc6550c66db50f611f42220e1230ffeb2b5f69`|F6/RIOT/CC/color/PF-påståenden|
|[G3 CC-deadlines](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G3_COLOR_CLOCK_DEADLINES_2026-11-17.csv)|**läst**, blob ej separat pinad här|Historiska F9/R3 c-värden, ej H4-traces|
|[G2 negativa och non-repeat](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md)|`8a92d30043e898688dc27d950b14154e8c0dbf73`|R1ba, R1f/R1g, F9, F11 begränsningar|
|[G5H fem-NPC stress](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md)|**läst**, blob ej separat pinad här|79/76 och 74/76 gäller annan direktallokering|
|[G5P rådgivande analys](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md)|`01ac6550089eb6be3d7e17e21555f1a2cc556d45`|N0 reducerad, ej H4|
|[F11 MAIN-mottagning](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/MAIN_V_R1_F11_G0_FAIL_SOURCE_ONLY_RECEIPT_2026-11-17.md)|`48120508cd8d88c84e8bb2c4be24fe5ba6529cb2`|F11 `SOURCE_ONLY_INFEASIBLE`, G1 NOT RUN, 0 ROM|
|[fyra originalmasker](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/design/NPC_REFERENCE_8x9_masks.json)|`058800a4c1904d1ff289e7e61b3902aa111ba16d`|Exakt M/F/SM/SF TOP-DOWN original|
|[G5X godkänt fyrkartsmanifest](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json)|`bc97d2c49131ef698cf0aebd96ba5592f61412be`|Källa/commit och exakta 40x22 kartval|
|[G5Q fem fri X/Y + kvalitetsmål](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md)|`4870234258f073143f8701d9f9f5861b9278926e`|LM-D12/13 design, inget ROM-PASS|
|[G5S fem/score/spawn](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md)|`8763554640e0a4b146e6a91208093b60599206ae`|LM-D14/15/16: fem, −30, 1/5|
|[G5X exakta kartbeslut](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md)|`e422b800ce985466c2fe096d3f8a9f93407cab57`|LM-D17/19, framtida kartmål|
|[G5-auktoritetsdelta](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md)|`79f428d495fca2ca28737915550e1dd83d897c2d`|Nyaste G5Z gäller framför äldre "G0 ej auktoriserat" i historiska avsnitt|

## 3. Frysta tekniska primärkällor på exakt historisk commit
| Repo/ref + full originalfil | Git blob SHA-1 | Vad den faktiskt stöder |
|---|---|---|
|[R1e käll-ASM, commit `552a085…`](https://github.com/Odourman/let-me-out/blob/552a085d0c1ce0ec47d4f3342173658a25fd0e87/rom/v018/experiments/main_ii_p0_four/r1e_four_originals.asm)|`531fae4477a903d87c5bb5d395e110b6e26cac01`|P0 diagnostisk `PlayerRows` och M0 på föregående rad; PF tom i historisk loop|
|[R1f build.py, samma commit](https://github.com/Odourman/let-me-out/blob/552a085d0c1ce0ec47d4f3342173658a25fd0e87/rom/v018/experiments/main_ii_r1f_resp0/build.py)|`97edcc3632286e212bddffc4b1855271d6d792c9`|Byter till `NUSIZ0=$02`, två `RESP0`, fasta 2 ROM-varianter|
|[R1g bygggenerator, commit `d1d167…`](https://github.com/Odourman/let-me-out/blob/d1d16758c549ecd657aba3b0aa4d6d7559e19264/rom/v018/experiments/main_ii_r1g_four_positions/build.py)|`7f7e3606a37ff2778cc383f692ca5178c40f4527`|Fyra varianters 11c omordning av P0-grp/color/RESP|
|[R1g 1 ROM / 4 profillägen, samma commit](https://github.com/Odourman/let-me-out/blob/d1d16758c549ecd657aba3b0aa4d6d7559e19264/rom/v018/experiments/main_ii_r1g_dynamic/build_dynamic.py)|`eadee75fbdabd2f719539495a28640c6b179ed26`|Pre-raster `FRAMELO & $30` väljer fulla fasta rutiner; inget numeriskt allmänt X|
|[F9 diagnostic report, commit `c36982…`](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md)|`fd54ed338a0b067ee9551b57bc4cadb28c62c842`|Tre separata binära P1-val, 144 autentiska historiska Stella-bilder (ärvda bevis)|
|[F11 original report, commit `dfe21c…`](https://github.com/Odourman/let-me-out/blob/dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md)|`a9c67b0ed3822dc218e435d76719f8f431c37de1`|G0 hard stop / G1 NOT RUN, inga nya F11-ROM|

## 4. Exakt versionspinnad Stella-hårdvarukällkod
Git-repo `stella-emu/stella`, tag **`6.7.1`**, läst via GitHub-anslutning (källkod som text, **inte körd**).

| Source | Git blob SHA-1 | Viktiga effekter |
|---|---|---|
|[Player.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx)|`af6978b9f517692b7cbeff7560466cbfd7455bf5`|`resp` vid aktiv rendering, `nusiz` decode-fas, `grp` graphic byte|
|[Missile.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Missile.cxx)|`cd66ec22c930a0014b1d23995061c7c40a034e20`|`enam`, `resm`, `nusiz`, one-shot enable and copy risk|
|[TIA.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx)|`4c61e197fa2a4dc37c307327120319698fb41ab6`|`NUSIZ0` writes Player0+Missile0; `GRP` and `ENAM` delay queues; `RESP` separate|
|[DrawCounterDecodes.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx)|`e0b89c7c167be6c9f405b448c12b3d4b22a960b5`|NUSIZ medium +32CC, close +16CC, far +64CC, player/missile decoder|

Detta är **en emulators källmodell**, inte nya observerade färgklockspulser på en fysisk Atari.

## 5. Source-pinnad aktuell kartgeometri, endast PF-kontroll
[G5X-manifestet](https://github.com/Odourman/let-me-out/blob/2421aa9eb49a10a618f030ef282f1bebc268eac0/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) anger:
- A_OPEN_01, C_OPEN_01, D_OPEN_01 från commit `80bf072ee0e8a9a84905a29d70771a7cc6be7820`, fil `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json`, blob `0e449f97f87bd9b403476fd1435398042eaee285`.
- B_OPEN_02 från commit `2991a94a4d92a0ee75a5de8e8c5302d549734e1e`, fil `studies/graphics/G5V_B_OPEN_02_2026-11-17/B_OPEN_02.json`, blob `c32fc656fb5c60d16a5b73e4cea75f86df3e9621`.
- I **alla fyra** lästa JSON-grid-original är både room-relativa gridrad 1 och 2 exakt `#......................................#` (40 tecken). **Ett möjligt statiskt PF-kantband för ett avgränsat H4-prov**; inte full fyrkarts- eller rasterimplementation.
- G4:s illustrativa y96..104 (om 8 scanlines/cell utan room-offset) korsar grid-rad12/13, där högra dörrtecknet går från `D` till `#`. Behåll källskillnaden, påstå aldrig PF-statiskt där utan ytterligare avgränsning eller byte av fysisk bandplacering efter separat beslut.

## 6. Metod, historiska negativa utfall och leveranskedja
1. Läste exakt Issue #12, G5Z-kopiorna, G4/G3/G5Y/G5H/G2/F11/R1f/R1g/F9/8x9-källorna och 6.7.1 TIA-källfilerna via aktiva anslutningar.
2. Skilde registerskrivning `STA` (CPU 3CC-gitter) från intern decode, pixelstart och `GRP`-fördröjning. All aritmetik märkts som **NOMINELL, KÄLLBERÄKNAD**; inga G5Z TIA-traps eller screenshots finns.
3. Räknade källradsmasker och nominell worst-case opioidcykelkostnad för **8 förregistrerade fall × 9 rader = 72** poster i G5Z:s nya CSV. Beräkningsmallen har explicit okända CPU start/slut för en faktisk körtidsplan.
4. Bevarade **R1ba felvända stora masker**, äldre `F11_SOURCE_ONLY_INFEASIBLE` utan ROM och `G5H 79/76/74/76` för annan allokering som **olika negativa/gränsade** fakta; inga av dem omdöpta till nya PASS eller universell Atari-omöjlighet.
5. **G5Z enda utfall:** `G0_INCONCLUSIVE_NO_ROM`. MAIN VII ska granska originalen och denna frysta source-only-specialistleverans självständigt. Ingen beställning om ny testvariant, ROM, G1/G6/F12, verifiering eller cutover ges här.
