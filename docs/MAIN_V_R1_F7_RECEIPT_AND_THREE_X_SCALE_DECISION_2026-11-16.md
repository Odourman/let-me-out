# LET ME OUT! – MAIN V: R1-F7 mottagen, självständig evidenskontroll och nästa skalbarhetsgrind

**Datum:** 2026-11-16. **Beslut:** F7 **MOTTAGEN OCH AVSLUTAD** som `F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS` – exakt **två top-down originalandroider** med **två separata binära RAM-X-val** i samma standard-F6/NTSC ROM, fyra möjliga X-par. MAIN:s egen mottagningsgranskning är **inte** organisatorisk fristående VERIFICATION och ger **inte** godtyckliga numeriska två X, sex oberoende X/Y eller fullständigt R1.

## 1. Frysta GitHub-källor och arvsgrind

- [Fryst F7-rapport](https://github.com/Odourman/let-me-out/blob/c8dc8b35f4bb652e3920b70882f8cc1fb84125d3/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F7.md) på **`c8dc8b35f4bb652e3920b70882f8cc1fb84125d3`**, Git blob `b3afd8e1fae89f3612541ab7f966422c0ad126df`. Isolerad branch `rom-dev/v018-r1-f7-two-binary-runtime-selectors-20261116`, exakt bas fryst F6 `e45455e09e1d796e576b0012d96e5d817d6210c4`.
- Gällande auktorisation [R1-F7 TWO MASK TWO X BITS](MAIN_V_TO_ROM_DEV_II_R1_F7_TWO_MASK_TWO_RUNTIME_X_BITS_AUTHORIZED_2026-11-16.md), Git blob `03b8ba55ae9e8dccb139b5486d61f83421793257`. GitHub `compare_commits(F6,F7)`: **ahead=15, behind=0**, **10 ENDAST NYTILLAGDA filer** (4 workflows, 6 R1-F7 source/report/scripts), **inga ändringar i frysta F2–F6, maskerna, R1ba, main eller PR#7**.
- `main` projektstatus inspekterad; PR#7 **OPEN / DRAFT / UNMERGED**, head `82667dae033f70570dce903f8e1d4866528be02a`; Issue#8 / oberoende VERIFICATION fortsatt standby.
- Låsta rättvända NPC-referenser faktiskt återlästa via GitHub: `design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, stor man `3C 3C 18 FF 18 24 24 42 42`, stor kvinna `3C 3C 18 FF 3C 7E 7E 24 24`. Aldrig vertikal R1ba-mirroring.

## 2. Verklig original-EVIDENS i Google Drive – oberoende av utvecklarens ord

Hämtad direkt med ansluten Drive från exakt [`LET_ME_OUT_R1_F7_FULL_SOURCE_160_REAL_STELLA_16_TRAPS_SHA256_2026-11-16.zip`](https://drive.google.com/file/d/116aehSuMbRltvLm0DI68xvtiBQ30SVXT/view), Google Drive ID `116aehSuMbRltvLm0DI68xvtiBQ30SVXT`, projektsparent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.

- **4 939 383 byte**, helfil SHA256 **`da6f4ef206e608dbf92749d65e053d27eed4aa2f512e13dc125369766fddb29f`**, **394 ZIP-poster**, ZIP-CRC PASS.
- MAIN återberäknade direkt i faktisk ZIP **alla 392** `EVIDENCE_FILE_INDEX.json` entries: per entry faktisk filstorlek och **SHA256 392/392 PASS**; `SHA256SUMS.txt` verifierad **392/392 PASS**. Endast index och SUMS inte själva indexerade. 160 faktiska raw-crop PNG 900×300, 160 fulla debugger-GUI-PNG, 16 separata ursprungliga register-GUI-traps, en negativ märkt syntetisk bild (ej positiva bevis), asm/.lst/.sym, source-G0, GHA-historik och original-ROM.
- Den enda faktiska **16 384-byte F6 ROM** i arkivet är `dist/r1_f7_2x2_independent_RAM_X_ONE_ROM_F6.bin`, SHA256 **`ede93075c3c2c88b6cca226f52958fbbcb9117a068edca01d4d83ff30e4677df`**, fyra **byteidentiska 4KiB-banker**. Ingen ny ROM för de olika RAM-lägena.
- MAIN läste verkligt arkiverad F7-assembler **och** dess GitHub-original: två RAM-variabler `X0_SELECT=$A0`, `X1_SELECT=$A1`, faktiskt separata `CMP` och villkorade `STA` för respektive byte före synligt band, läser båda RAM-byte för dispatch till **fyra separata unrolled nio-radskernels i samma ROM**. Det är en scripted växling av två självständigt lagrade **1-bit-värden**, inte en algoritm som kan ta godtyckliga X-tal direkt och inte fyra olika förkompilerade ROM-byggen.

## 3. MAIN:s helt separata direkt-pixelgranskning, 160/160

MAIN skrev och körde en ny Python/Pillow/NumPy-råpixelsanalys av de **faktiska, arkiverade PNG-bilderna**, med original-8×9-TOP-DOWN från verifierad GitHub-maskkälla. Testad aktiva vita cropregion `x=0..335,y=50..194`, inga utvecklar-JSON-asserts som bevis. För varje frame måste pixelmängden vara **exakt** mängdunion av två originella 8×9-maskar, två croppixlar per originalpixel, på en unik uppmätt X-kombination, ingen extra eller saknad vit pixel. Alla **160/160** matchar exakt rättvända M/F med `y=96..104`, **132 vita screenshotpixlar per frame**. Inga R1ba-inverterade rader, inga `ghost` eller klipp.

Stella-frame till sparat råfilindex: `Stella frame = raw frame + 10`; spelvariabeln `FRAMELO = Stella frame - 1` enligt autentiska RAM-traps. Förkorrigering som tidigare read-only CI missade är därför source-läsregeln `floor((StellaFrame - 1)/16) % 7`, inte förändrad ROM eller efterhands-X-prediktion. MAIN:s source-kalkylerade mode för samtliga raw 001–160 och observerad pixelposition ger **0 avvikelser**:

| RAM-väljare `X0X1` | Ursprungligt mål / faktisk pixel-X (M,F) | Originala bildrutor | Status |
|---|---|---:|---|
| `00` | **(39,99)** | **70** | 70/70 pixel-exakt |
| `10` | **(45,99)** | **32** | 32/32 pixel-exakt |
| `01` | **(39,105)** | **42** | 42/42 pixel-exakt |
| `11` | **(45,105)** | **16** | 16/16 pixel-exakt |

Direkta avlästa **nio faktiska X-övergångar**, endast **en** figur flyttar i varje, inkluderar `00→10` och `10→00`, `00→01`, `01→11`, `11→01`, `01→00`. Härmed **fyra av fyra oberoende X-kontraster** (för varje RAM-bit, den andra biten fixerad vid 0 och vid 1) stödda direkt av source+originala rasterbytes.

De riktiga **16 register-GUI-traps** är faktiskt inkluderade, 4 per RAM-kombination, visar `RESP1/GRP1` c21/c23, c32/c33 och avlästa separata RAM-lägen i Stella GUI, med PC/bank/scanline. MAIN har inspekterat verkligt `mode_11/FIRST_RESP1/stella_full.png`: `PC` efter `$F471`, `RESP1` dest, `C. C=23`, `Color Clk=69`, `Scn Ln 123/262`, bank0, memory `A0=01/A1=01`. Men **16 riktade CPU-writetrapbilder ger inte intern TIA START-puls- eller RAM-X-random-access-bevis**. `WSYNC c38/c39` och rad8 c41/c42 är **källbudget**, inte skärmmätningar efter WSYNC.

Övrig P0 gul, M0 aktiv, PF brun och 262 NTSC beskrivs i utvecklarens två pixel-/HUD-auditer och faktiska GUI-bilder; MAIN:s nya fristående audit har själv redovisat endast **vit NPC-maskunion**, inte oberoende samtliga övriga färgade scenobjekts register-/full-frame-test.

**GitHub Actions lästes live:** G0 [#43966545190](https://github.com/Odourman/let-me-out/actions/runs/43966545190) success, [#43966843507](https://github.com/Odourman/let-me-out/actions/runs/43966843507) failure för X11 efter EN ROM kompilerats, [#43967693889](https://github.com/Odourman/let-me-out/actions/runs/43967693889) failure för audit-infra efter faktisk 160-rutors capture, [#43968120975](https://github.com/Odourman/let-me-out/actions/runs/43968120975) failure read-only fel frameindex, slutlig read-only [#43968481385](https://github.com/Odourman/let-me-out/actions/runs/43968481385) **SUCCESS** med samma låsta ROM och verkliga frame-artefakter; inget nytt byggt för slutgaten. Röda CI-runs redovisas som RED, inga omdöpta lyckade geometrier.

## 4. Slutsats och enda nästa beslut

**F7 STÄNGD OCH MOTTAGEN:** `F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS` betyder två oberoende **BINÄRA** positionsval per original-M/F i **EN** ROM, med exakt fyra bevisade punktlägen och påvisad dynamisk RAM-branch, **inte** godtyckliga numeriska X, Y-rörlighet, tredje/sjätte NPC, överlappande same-Y sex, hela R1/NTSC integration eller fristående E02 Verification. Fullt **R1 `BLOCKED / NOT ACCEPTED`**.

MAIN auktoriserar **ENDAST** [R1-F8: THREE-INDEPENDENT-X-SCALING SOURCE ONLY](MAIN_V_TO_ROM_DEV_II_R1_F8_THREE_INDEPENDENT_X_SCALE_SOURCE_ONLY_2026-11-16.md), en separat **READ ONLY SOURCE-/ARKITEKTURSTUDIE, INGEN ROM, DASM, Stella, CI, Python audit eller 3-sprite implementation**. Den ska leverera en källbaserad tid-/RAM-/banks-kostnad och en falsifierbar möjlighet att lägga till en **tredje originalmask med eget binärt X-val** på samma nio rader utan att bryta de två bevisade RAM-X-lägena, eller ett konkret `F8_NO_THREE_X_FEASIBLE_WITH_CURRENT_ROW`/architecture-stop. Inget F9 eller annan ombyggnad utan nytt uttryckligt MAIN-beslut. GRAPHICS stängt, VERIFICATION standby, PR#7 omergad.
