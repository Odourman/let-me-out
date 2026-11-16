# LET ME OUT! – MAIN V: R1-F4 mottagning och nästa tekniska beslut

**Datum:** 2026-11-16. **Klassning:** fryst **DEVELOPER_LOCAL** R1-F4 mottaget och genomgånget med MAIN:s separata ZIP-/PNG-/ROM-kontroll. **Inte** extern VERIFICATION, R1-PASS, spelimplementation eller designwaiver.

## 1. Bindande källa, branch och integritet

- ROM DEVELOPMENT II fryst rapportcommit: **`2218e583f4a6f9c60adc3e4bb850b05a7176f1b4`**, branch `rom-dev/v018-r1-f4-early-copy-phase-20261116`, [TO_MAIN_R1_F4.md](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md), [utvecklarens överlämning Issue #6](https://github.com/Odourman/let-me-out/issues/6#issuecomment-6929356599).
- [F4 MAIN-order](MAIN_V_TO_ROM_DEV_II_R1_F4_EARLY_COPY_PHASE_GEOMETRY_AUTHORIZED_2026-11-16.md); förälder/den frysta F3 `65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190`. GitHub compare F3→F4 visar **23 commits** och **11 ENBART nytillagda F4-filer** (F4-rapport, skript och Actions-workflows), **0 ändringar av frysta F2/F3/R1/R3/originalmasker**.
- PR #7 bekräftad GitHub `open/draft/unmerged`, head `82667dae033f70570dce903f8e1d4866528be02a`. Issue #8 fortsatt oberoende viloläge. Main har ingen F4-ROM eller R1-branch-merge.
- Tre riktiga ZIP från samma projekt-Drive-mapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u` hämtade direkt och analyserade separat:
  1. [Kombinerad F4-evidens](https://drive.google.com/file/d/1ELlpy5rlXrgtW-flmKT7sUpZXKGj3LMJ/view), **1 306 370 byte**, ZIP SHA256 **`c8585485eeb78cf3fb7c17dd1dbddbc77d17118485232161d9b1c16736dd8c50`**, CRC PASS, **149 ZIP-poster**, **147/147** filer i `EVIDENCE_FILE_INDEX.json` oberoende SHA-256-/filstorlekskontrollerade.
  2. [c18 råpaket](https://drive.google.com/file/d/19ymcYUpqPSGh79x7u3iR1I9DKQWdAxsF/view), **638 459 byte**, SHA256 **`740f2dee7fcf0f5483ed98b8b59d6b01a98e87480287c8335f28015b5ee3ec46`**, 70 poster, CRC PASS.
  3. [c21 råpaket](https://drive.google.com/file/d/1UVQxKxuPN3NrlSYOA1mX_tgyHyoXO0gb/view), **635 922 byte**, SHA256 **`642043a96e1940ec1e286e1b465f2f789874388c886a75ec7ad5e4ceecf9bb8c`**, 70 poster, CRC PASS.

## 2. MAIN:s självständiga bild- och binärkontroll

MAIN har själv skrivit och kört en **separat Python/Pillow-audit**, utan att använda F4:s egen exakthetsflagga. Källans sex maskmönster har lästs från aktuellt GitHub `design/NPC_REFERENCE_8x9_masks.json`, Git blob **`058800a4c1904d1ff289e7e61b3902aa111ba16d`**, indexordning stor man, stor man, stor kvinna, stor kvinna, liten man, liten kvinna. Råkroppen i Stella-debuggercrop använder 2 horisontella pixlar per originalmaskbit, nio rasterrader, y0=96.

- **c18:** samtliga **16 riktiga 900×300 Stella-crop-PNG** har hela exakta vitt-pixelunionen av de sex canonical bitmapparna vid `x=[43,75,129,183,243,303]`, **348 vita skärmpixlar**, **inga avvikande extra eller saknade pixlar**, 16 kompletta debuggerbilder och 6 separata trapbilder i arkivet. **Hypotetiskt begärt x0=37**, verkligt **43**.
- **c21:** oberoende samma bildberäkning **16/16** crop PNG, exakt **348 vita skärmpixlar** vid samma sex X, **inga avvikande pixlar**. **Hypotetiskt begärt x0=55**, verkligt **43**. Även här 16 fulla debuggerbilder och 6 trapbilder.
- Två faktiska 16 384 byte F6-binärer hämtade **ur** ZIP:
  - `r1_f4_6B_I0_C18_I2_FIXED_F6.bin` SHA256 **`d06fa761ddcc4756fbb2b9b2d72bbe49cc4ec5146a04c8e5e4ff8483dfd9f15d`**
  - `r1_f4_6B_I0_C21_I2_FIXED_F6.bin` SHA256 **`fc3e3622e155c3faded0d91e12f2889c24d0c9eb16822bbef58a4d7cdd6d704f`**
  Varje binär är **4×4096 byte byteidentiska bankkopior**. Det finns inga F4 tvåindividers-runtime-byggen i de levererade källpaketen.
- MAIN öppnade verkliga GUI-trapbilder för första `RESP1`: c18: bank0, frame12, scan123, `Dest RESP1`, `C. C=18`, `Color Clk=54`, PC efter **`$F1C3`**; c21: `C. C=21`, `Color Clk=63`, PC efter **`$F1BF`**. Övriga register-traps, enligt utvecklarens rapport, index1 c28, index2 c37, sista GRP1 c69, WSYNC efter write scan124/c0; MAIN:s egen bildgranskning kan inte ersätta fristående Stella-rerun. Cykel c72 vid WSYNC är **endast källberäknad**, inte en skärmtext som faktiskt visar c72 efter skrivningen.

## 3. Beslutet: negativa tester får inte felklassas

**`F4_INDEX0_PHASE_GEOMETRY_LOCAL_FAIL`** för de **exakt två** auktoriserade proberna c18 och c21. Varken den ena eller den andra flyttade index0; x0=43 i alla **32/32** verkliga råbilder. De övriga fem källmaskerna är byte-/pixelkorrekta, gul P0, aktiv M0, bruna PF och 262 NTSC visas enligt F4:s riktade käll-/GUI-kontroller. Dessa verkliga pixel-**PASS** för maskkvalitet är **positions-FAIL**.

Redan fryst F1 c19 och F3 c20 gav också x43; därmed finns **fyra olika första-P1-RESP1-tider c18/19/20/21 med samma första synliga X** under det undersökta 6B/NUSIZ1=$01 och oförändrad index1-RESP1-c28. Detta gäller **det här tidsschemat**, inte en bevisad universell TIA-begränsning.

**`F4_TWO_INDEPENDENT_RUNTIME_X=NOT_RUN`**, eftersom ingen sådan F4-ROM var tillåten/byggd; tidigare F2:s enda index2 runtime-X `129↔135` kvar DEVELOPER_LOCAL_PARTIAL_PASS. **Fullt R1: BLOCKED / NOT ACCEPTED**, och R1+R3, R2/R4, 600 dynamiska sexbilder, varierande Y, kärna+HUD, PAL/fullspel, independent VERIFICATION fortfarande ej utförda/godkända. Källanalysens teoretiska x37/x55 är **inte** fysiskt uppnådda pixel-X.

## 4. Nästa huvudbeslut: orsaksförståelse, inte blind offset-sweep

MAIN stänger **R1-F4 i sitt scope** och auktoriserar **endast en separat, källbaserad, läsande teknisk undersökning** [R1-F5 P1 COPY PROVENANCE – SOURCE ONLY](MAIN_V_TO_ROM_DEV_II_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_2026-11-16.md). Detta är **inte en F5 ny geometristest-ROM** och får **inte** producera ny ROM, Stella-trap, CI-svep, ny branch/assembly-familj eller integration. Studera vad som genererar första faktiska kopian när `NUSIZ1=$01` och sex `RESP1/GRP1` per rasterrad föreligger; rita register-/kopietidslinje för minst två källrader samt jämför varför mitten `index2` i F2 faktiskt svarar på c37↔c38 medan index0 inte svarar c18↔21.

Syfte: **en enda konkret falsifierbar framtida hypotes** eller ärligt `CAUSE_NOT_ISOLATED`/stopprekommendation, inte ännu en obestämd optimeringsloop. Separat och uttrycklig framtida ROM-order krävs om någon ny diagnostik motiveras. Ingen designwaiver, R1-canon, grafik, main/PR#7 eller oberoende VERIFICATION ändras.
