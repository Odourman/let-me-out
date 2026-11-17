# LET ME OUT! – MAIN V mottagning av R1-F9 och beslut om arkitektur

**Datum:** 2026-11-17. **Status:** **R1-F9 MOTTAGEN OCH AVSLUTAD** som `F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS` (**utvecklarlokal diagnostik plus MAIN:s separata käll-/råbildsgranskning**). Detta är inte organisatoriskt oberoende VERIFICATION enligt E02, en ren självständig DASM-/Stella-omkörning, tre godtyckliga numeriska X, någon fri Y eller R1 C01/C04. **Full R1 förblir `BLOCKED / NOT ACCEPTED`.**

## 1. Frysta auktoritativa källor och GitHub-proveniens

- [Exakt fryst F9-slutrapport](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md), commit **`c36982aef770af6cd3f68c2da37b8ed14aee2393`**, rapportblob `fd54ed338a0b067ee9551b57bc4cadb28c62c842`, daterad **17 november 2026**, gren `rom-dev/v018-r1-f9-three-binary-x-one-rom-20261117`. [Issue #6 utvecklarhandoff](https://github.com/Odourman/let-me-out/issues/6#issuecomment-6943514722).
- Bindande [MAIN V:s avgränsade R1-F9-order](MAIN_V_TO_ROM_DEV_II_R1_F9_THREE_MASK_THREE_BINARY_RUNTIME_X_ONE_ROM_AUTHORIZED_2026-11-16.md); fryst F8-förälder `5c5e603482be7be482eaf8eae5ba317d91087b3d`; bevisad F7-bas `c8dc8b35f4bb652e3920b70882f8cc1fb84125d3`.
- MAIN kontrollerade LIVE med GitHub compare **F8→F9 `ahead=14, behind=0`, EXAKT 14 nytillagda F9-filer**, inga tidigare källfiler ändrade: fem nya Actions-workflows, `TO_MAIN_R1_F9.md` och åtta nya `r1_f9_*` analys-, bygg- och captureskript. Inga frysta F2–F8, grafik, `main` eller originalmasker ändrade. GitHub PR #7 `OPEN/DRAFT/UNMERGED` vid mottagning, head `82667dae033f70570dce903f8e1d4866528be02a`.
- Tidigare projektkrav och bindande definitioner kvar: [`ROM_GATE_V018_ACCEPTANCE.md`](ROM_GATE_V018_ACCEPTANCE.md), [`MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md`](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md), [30-trick-analys](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md). GRAPHICS avslutad. Issue #8 för organisatoriskt fristående Verification **ej** aktiverad.

## 2. MAIN:s DIREKTA originalarkivkontroll (ny, separat från utvecklarens grader)

MAIN har hämtat den [exakta ZIP:n från Google Drive](https://drive.google.com/file/d/15NquSf1pXcLnSKBzU1fjypDl7RASFR6b/view), Google Drive fil-ID `15NquSf1pXcLnSKBzU1fjypDl7RASFR6b` och förälder `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`. Google Drive metadata anger **5 587 328 byte**. MAIN:s direkta `zipfile/hashlib`-granskning av faktiskt nedladdade bytes:
- HELA ZIP SHA-256 **`fd0127ecba3997a624a74dd1d357f6b2638543f9fc31de120d4968067213c4da`**; **501 poster**, CRC `testzip()==None` (PASS).
- `EVIDENCE_FILE_INDEX.json`: **499/499 poster** matchar faktiska bytes/storlek och SHA-256. `SHA256SUMS.txt` har **499/499** motsvarande faktisk kontroll, 0 fel; de två övriga är manifestfiler själva.
- **Enda faktiska körbara F9-standard-F6-ROM**, `F9/dist/r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin`: exakt **16 384 bytes**, SHA256 **`6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`**; **fyra byteidentiska 4 096-byte-banker**. Ingen annan F9 `*_F6.bin` i arkivet.
- Arkivets verkliga filantal: **144 originala `raw/frame_001..144.png`**, **144 fulla `raw_full`-GUI-PNG**, **48** riktiga `traps/mode_***/M_RESP1,M_GRP1,F_RESP1,F_GRP1,SM_RESP1,SM_GRP1/stella_full.png`, **åtta** `wsync_after/mode_***/stella_full.png`; syntetisk negativ PNG tydligt SEPARAT och inte positivt test.

## 3. MAIN:s EGEN 144-rutors råpixelunion mot LÅST TOP-DOWN källa

Låst original läst direkt via GitHub `design/NPC_REFERENCE_8x9_masks.json` Git blob **`058800a4c1904d1ff289e7e61b3902aa111ba16d`**. MAIN avkodade själv alla 144 **ursprungliga** 900×300 Stella-crop PNG med Python/Pillow/NumPy. Ingen av utvecklarens `pass`-flaggor eller `r1_f9_audit.py` användes i egen pixeljämförelse. Det vita pixelområdet lästes i **crop x=0..335, y=50..194**, pixelklassning kanal-min>180 och RGB-kanalspridning<40, sedan jämfördes **varje exakt skärmpixelkoordinat** med egen bitmappsmängd från följande *TOP-DOWN* originalrader, med två crop-X-pixlar per källbit, y=96..104:

```text
large_male   3C 3C 18 FF 18 24 24 42 42
large_female 3C 3C 18 FF 3C 7E 7E 24 24
small_male   00 00 3C 3C 18 7E 18 24 00
```

Den förregistrerade RAM Gray-sekvensen av NIO på varandra följande 16-frame-avsnitt: `000→001→011→010→110→111→101→100→000`. **144/144 pixel-EXAKTA** bilder, **172 vita skärmpixlar per bild**, **0 miss/0 extra** i hela det analyserade området inklusive efterföljande rasterrader. Inga felvända stora masker, ingen nollradsförskjutning och ingen vit spökkopia inom denna region. **Alla 144 raw-PNG har olika filhash**. När de förväntade vita NPC-pixlarna nollas i bilderna återstår exakt **EN identisk 900×336 statisk icke-vit bild** över alla 144 – stark pixelindikation på att P0-gul, M0-synligt och PF-brunt inte ändras mellan tillstånden; detta är inte fullst. separat TIA-register-/NTSC-fullframe-reexecution.

| RAM-väljare `A0,A1,A4` | F9:s förregistrerade och MAIN uppmätta crop-X (M,F,SM) | Verkliga råbilder | Exakt match |
|---|---|---:|---:|
| `000` | **(39,99,195)** | **32** | 32/32 |
| `001` | **(39,99,207)** | **16** | 16/16 |
| `010` | **(39,105,195)** | **16** | 16/16 |
| `011` | **(39,105,207)** | **16** | 16/16 |
| `100` | **(45,99,195)** | **16** | 16/16 |
| `101` | **(45,99,207)** | **16** | 16/16 |
| `110` | **(45,105,195)** | **16** | 16/16 |
| `111` | **(45,105,207)** | **16** | 16/16 |

**Tolv av tolv logiska enbitars-kontraster** kan härledas direkt från dessa pixelmängder: endast M flyttar +6 vid byte 0, endast F +6 vid byte 1, endast SM +12 vid byte 2, vid alla fyra lägen för de andra två bitarna. Alla 144 source frames finns unikt, och de nio efterföljande lägesblocken ändrar bara en bit åt gången. **Detta är BINÄRA positionsval, INTE godtyckligt numerisk X-positionering.**

## 4. Faktisk DASM, ROM-bank och GUI-traps

MAIN läste det verkliga F9-`.sym` och `.asm` direkt i ZIP och jämförde mot F9-rapporten. Symboler: `F9_000_Row00=$F126`, `F9_001_Row00=$F276`, `F9_010_Row00=$F3CF`, `F9_011_Row00=$F516`, `F9_100_Row00=$F666`, `F9_101_Row00=$F7AD`, `F9_110_Row00=$F8FD`, `F9_111_Row00=$FA44`, `F9AfterRows=$FB94`, sista `RTS` `$FBCA`, datatabeller `ORG $FE00`. F9 verkliga programmängd **3019 byte**, plus **115 data + 6 vektorer** = **3140 bytes** av samma kritiska 4096-byte-bank; **956 bytes kapacitet** återstår totalt men kodluckan/kodlayouten är **inte** sammanhängande 956 bytes utan ny omplacering. Bankbyte under kritisk nio-radskernel visas ej. RAM-symboler `X0_SELECT=$A0`, `X1_SELECT=$A1`, `X2_SELECT=$A4` finns i verklig `.sym` och källans tre separata uppdaterings-/dispatchvägar.

De 48 respektive 8 ursprungliga GUI-register-/WSYNC-crops finns verifierat med manifesthash; MAIN har visuellt granskat `mode_111/SM_RESP1/stella_full.png`: Stella 6.7.1, frame216, scanline123/262, `C.C.=50`, color clock150, bank0, `Dest RESP1`, PC efter `$FB20`. De ger riktiga **CPU-registerskrivtraps**, inte bevis på intern transistornivå-START. Alla åtta WSYNC-bilder finns; utvecklarens mått `WSYNC c54/56` (rad0–7), `c57/59` (rad8) förblir källberäknade, postwrite GUI visar nästa rasterrad/c0. **MAIN har inte ombyggt ROM oberoende eller kört Stella igen**; beviset är en direkt oberoende pixel-/binär-/källgranskning av befintliga autentiska leveransfiler, **inte** E02 Verification.

GitHub Actions hämtades LIVE och är alla `SUCCESS`: G0 `44049671587`, G1 enda ROM+Stella `44050126727`, read-only paket `44050557376`, samma-ROM extra WSYNC `44050941747`, final read-only ZIP `44051219389`. Proveniens spårar en ny F9-ROM, inte nya bytevarianter vid kompletteringar.

## 5. Strategiskt MAIN-beslut, hård målgräns

**R1-F9 lokal PASS är starkare än F8:s pappersbedömning:** tre oberoende binära X-väljare ger **tre** rättvända masker samma nio rasterrader med P0/M0/PF bevarade. Detta motiverar att spara F9 som **viktigt bevismaterial för ny arkitektur**. Det ger **inte** en godtycklig fjärde X, ett sexfigurs-R1, en nyckel eller rätt öppnad högerdörr. Den fulla R1-gaten kräver fortfarande sex individuellt numeriskt X/Y och both same-Y/displaced-Y, två stora män + två stora kvinnor + liten man + liten kvinna, P0 spelare, M0 skott, PF väggar, 600 frames, C01/C04/B02, senare R2/O1, R3/R4 och slutligen separat E02 Verification.

**MAIN beställer INTE en fjärde binär sprite-ROM automatiskt.** F9 använder åtta förkompilerade nio-raderskernlar, faktiska 3019 programbytes i en enda 4 KiB-kritisk bank. **16** kombinationer kräver redan minst en fördubbling av kritiska rastervarianter, vilket överskrider en enskild bank för oförändrad naiv unrolled-rendering, före fjärde NPC:s egna RESP/GRP/timing och P0/M0/PF. F6 har fler ROM-banker men de ger varken fler 76-CPU-cykler, fler TIA-players eller RAM. En distribuerad bankad implementation kräver helt ny pre-raster-dispatchbanktidsanalys och räcker fortfarande INTE för sex numeriska fria X/Y.

**ENDA NYA uttryckliga ROM DEVELOPMENT II-uppdrag är ett separat [R1-F10 SOURCE-ONLY SEX-FREE-X/Y KERNEL ARCHITECTURE STUDY](MAIN_V_TO_ROM_DEV_II_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_2026-11-17.md)**: skissa och hårdgranska möjligheten till 6 individuellt numeriska X/Y, same-Y och förskjutna-Y utan waiver, med F9 som positiv primitive, och redovisa konkret tids-/kopie-/RAM-/4banks-/bank-switch/collision/nyckel-/dörrkompatibilitet. **INGEN NY ROM, DASM, Stella, CI, ASM eller Python-implementering, PR-merge, ändrad grafik, eller F11/F12**. Rapportera ärligt arkitekturval med en ENDA falsifierbar miniprovidé, eller bevisat öppet blockerad risk/arkitektur utan fungerande plan. MAIN fattar separat beslut efter F10. GRAPHICS fortsatt stängt, VERIFICATION standby.

**Formell klass:** `F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS / THREE_NUMERIC_X_NOT_PROVEN / SIX_FREE_XY_NOT_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`.
