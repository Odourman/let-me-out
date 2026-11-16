# LET ME OUT! – ROM DEVELOPMENT II → MAIN V
## R1-F7: 2×2 BINARY RUNTIME X SELECTORS – FRYST SLUTRAPPORT

**Datum:** 2026-11-16  
**Slutklassning:** **`F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`** (begränsad, positiv DEVELOPER_LOCAL Stella 6.7.1-diagnostik, exakt två originalandroider).  
**Obligatoriska gränser:** **`ARBITRARY_TWO_X_NOT_PROVEN / SIX_FREE_XY_NOT_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`**. Ingen oberoende VERIFICATION. Ingen allmän fri numerisk X eller Y, ingen full sex-NPC-kernel och ingen full R1-acceptans.

## 1. Scope och frysta auktoritativa källor

**MAIN V:s bindande separata F7-order:** [MAIN_V_TO_ROM_DEV_II_R1_F7_TWO_MASK_TWO_RUNTIME_X_BITS_AUTHORIZED_2026-11-16.md](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F7_TWO_MASK_TWO_RUNTIME_X_BITS_AUTHORIZED_2026-11-16.md), blob `03b8ba55ae9e8dccb139b5486d61f83421793257`. Verifierad mot [MAIN:s F6-mottagning och F7-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F6_RECEIPT_INDEPENDENT_PIXEL_AUDIT_AND_F7_DECISION_2026-11-16.md) och [CURRENT_PROJECT_STATE](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md).

**Exakt fryst F6-bas:** `e45455e09e1d796e576b0012d96e5d817d6210c4`. Ny isolerad branch `rom-dev/v018-r1-f7-two-binary-runtime-selectors-20261116`; inga tidigare frysta filer får ändras. [F6-rapport](https://github.com/Odourman/let-me-out/blob/e45455e09e1d796e576b0012d96e5d817d6210c4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F6.md). Låst canon `design/NPC_REFERENCE_8x9_masks.json` på main, Git blob **`058800a4c1904d1ff289e7e61b3902aa111ba16d`**, bit-/byteidentisk redan fryst lokal `canon_masks.json`; varken deras bytes eller top-down-orientering ändras.

**Exakt två P1 originalmasker (uppifrån rad0–8):**
- Stor man: `3C 3C 18 FF 18 24 24 42 42`.
- Stor kvinna: `3C 3C 18 FF 3C 7E 7E 24 24`.

En enda och endast en **ny 16 384-byte F6/NTSC-ROM** får användas. Inga R1ba-orienteringsfixar, andra NPC, variabla Y, extra kopie-/NUSIZ-trick eller ännu en fas.

## 2. G0 SOURCE_ONLY innan någon ROM

Fristående [Actions G0 #43966545190](https://github.com/Odourman/let-me-out/actions/runs/43966545190) **GREEN** med källkontrollen [`r1_f7_preflight.py`](r1_f7_preflight.py), **ingen DASM eller Stella**. Förkontrollen är baserad på exakt låst F6/venetian-bildrutekälla och dess blobbhash `a25c92adb4ca5087eeace674e371be98b273ae5b`.

| Två tillåtna P1 RESP1 | GRP1 man / kvinna | Nästa WSYNC efter vanliga rad0–7, SOURCE_ONLY | Sista rad8 inkl. gemensam JMP+WSYNC, SOURCE_ONLY | Minsta CPU-marginal av 76 |
|---|---|---:|---:|---:|
| c21/c32 | c24/c35 | c38 | c41 | 35 |
| c23/c32 | c26/c35 | c38 | c41 | 35 |
| c21/c33 | c24/c36 | c39 | c42 | 34 |
| c23/c33 | c26/c36 | c39 | c42 | 34 |

**Exakt nio per-radsscheman för var och en av de fyra lägena** i G0 JSON. CPU-time/6502-opkod medför **ingen rad på eller över 76 CPU-cykler**, bankutrymme kontrollerat, fulla rättvända M/F-masker och oförändrad gul P0, M0-skott, speglade bruna PF-väggar och standard-NTSC-skelett. `STA RESP1,X` är fyracyklers zero-page-indexerad write till **samma** RESP1 ($11) med X=0 och förekommer **endast** i c23/c32. c33-varianterna använder separat förregistrerad NOP-pad till en **trecyklers** `STA RESP1`. Ingen självmodifierande ROM.

**Två separata faktiskt lagrade RIOT RAM-väljare:**

| RAM | Betydelse | 0 | 1 |
|---|---|---|---|
| `X0_SELECT=$A0` | Mans första P1-fas | c21 | c23 |
| `X1_SELECT=$A1` | Kvinnans andra P1-fas | c32 | c33 |
| `F7_SEQ_STEP=$A2` | Endast reproducerbar testordning | – | – |
| `F7_HOLDCOUNT=$A3` | Håll 16 bilder per sjulägessteg | – | – |

Enbart för diagnostiken: **`00 → 10 → 00 → 01 → 11 → 01 → 00`**, med 16 på varandra följande källbildrutor per steg. I **två av de 30 redan existerande VBLANK/WSYNC-scanlinepositionerna** uppdateras först håll-/steg-räknaren, därefter de två RAM-byten **var för sig via två olika CMP/STA**, och endast om just den byte faktiskt behöver ändras. Övriga 28 tidigare WSYNC-blankrader finns kvar. Precis innan det synliga nio-radersbandet läses **båda RAM-väljarna** för att hoppa till en av fyra i den **samma** ROM:en förberedda, unrolled nio-raderssekvenser. Ingen `FRAMELO`-formationstabell som i sig ersätter två fysiska RAM-väljare.

**Preregistrerade X-mål, OFÖRÄNDRADE:** 00=(39,99), 10=(45,99), 01=(39,105), 11=(45,105). För c33 var X1≈105 en ännu otestad forskningshypotes före den enda nya ROM:en; F7:s positiva X-response fick aldrig antas före riktiga Stella-PNG.

## 3. G1 – EN ny F6/NTSC-ROM och faktiskt fysisk 2×2-resultat

**Unika och ENDA nya ROM:en:**

`r1_f7_2x2_independent_RAM_X_ONE_ROM_F6.bin`  
**16 384 bytes**, 4 × **4 096 identiska bankbytes**, standard **F6/NTSC**, alla fyra rastersekvenser i samma bankkod.  
**ROM SHA-256: `ede93075c3c2c88b6cca226f52958fbbcb9117a068edca01d4d83ff30e4677df`**.

Enda faktiska DASM-kompileringen inträffade i [Actions #43966843507](https://github.com/Odourman/let-me-out/actions/runs/43966843507) efter G0. **Inga** andra ROM-kompileringsjobb, alternativa faser, bankmetoder eller NUSIZ-värden har exekverats. Alla senare Stella-bilder körde byteidentiskt **samma** ROM-hash. Byggskript [`r1_f7_build.py`](r1_f7_build.py), komplett assembler i arkivet tillsammans med den faktiska DASM-listningen `.lst` och symbollistan `.sym`.

**Faktiska 900×300 Stella-debuggercrop, exakt samma enskilda ROM:**

| RAM `X0,X1` | Prereg P1 RESP1 c | Prereg målpixels X M/F | Uppmätt fysisk X M/F | Antal genuina bilder, varav minst 16 i följd | Originalmask-/P0/M0/PF/262 |
|---|---|---|---|---:|---|
| **00** | c21/c32 | (39,99) | **(39,99)** | **70**, flera 16-block | **ALLA PASS** |
| **10** | c23/c32 | (45,99) | **(45,99)** | **32**, 16-block | **ALLA PASS** |
| **01** | c21/c33 | (39,105) | **(39,105)** | **42**, 16-block | **ALLA PASS** |
| **11** | c23/c33 | (45,105) | **(45,105)** | **16**, 16-block | **ALLA PASS** |

**160/160** verkliga föränderliga frameindex från samma ROM (debugger frame #11–#170), inte dubblade PNG. **160 originala 900×300 crops och 160 separata originala 1366×900 debuggerbilder**. **160/160** två originalmasker **rättvända** från canon rad0 till rad8, **0 saknade och 0 extra vita pixlar** inom hela testade white-band-unionen; **160/160** gul P0, ett aktivt statiskt M0, bruna speglade PF-väggar och debugger-HUD **262 NTSC** intakta enligt två oberoende kodade orienterings- och objektkontroller. Y-band i alla fall **y96–104**, ingen Y-rörelse. Inga spöken, dubbelsilhuetter eller inversioner.

Två kodmässigt oberoende auditer för positiva raw-PNG: (A) komplett canon-XY-mängd/union och (B) row-by-row 336-bitars bitfield-XOR från de top-down-matriserna. Den frysta F6-granskarens två olika algoritmer används som READ-ONLY underlagsmodul i den nya [`r1_f7_audit.py`](r1_f7_audit.py); dessutom gjordes **en extra lokalt fristående** rå-PNG-white-unionskontroll direkt från samma låsta maskbytes på **160/160** faktiska filer, inga extra/saknade. **En explicit märkt syntetisk NEGATIV ändring av EN riktig manpixel** lagras **separat**, förkastas av båda oraklen och ingår INTE bland de 160 autentiska positiva bildrutorna.

**Ortogonalitetsprövning – samtliga fyra källförregistrerade kontrasterna:**

| Variabel bit, andra låst | Ursprung och mål | M fysisk X | F fysisk X | Resultat |
|---|---|---|---|---|
| X0, X1=0 | 00→10 | **39→45 (+6)** | **99→99 (0)** | PASS |
| X0, X1=1 | 01→11 | **39→45 (+6)** | **105→105 (0)** | PASS |
| X1, X0=0 | 00→01 | **39→39 (0)** | **99→105 (+6)** | PASS |
| X1, X0=1 | 10→11 | **45→45 (0)** | **99→105 (+6)** | PASS |

Denna matris är ett verkligt, begränsat proof att **två skilda RAM-bitar oberoende kan välja TVÅ X-lägen vardera på två rättvända originalmasker** i en och samma ROM. **Inte** ett numeriskt godtyckligt X-reglage, två fria X för 6 NPC, eller fri X/Y.

## 4. Real TIA-registertraces, RAM-source och korrekt frameindex-proveniens

**16 äkta fulla debugger-GUI-registertraps:** fyra per varje RAM-läge, på oförändrad ROM, **frame 12/20/52/68**, **scanline123**, **bank0**, med riktig CPU cycle, färgklocka, ROM-PC och TIA-destination i bilderna.

| F7 RAM-läge / faktisk Stella frame | RAM $A0/$A1/$A2 i autentisk debugbild | P1 RESP1 första, CPU/CC, PC efter | RESP1 andra, CPU/CC, PC efter | GRP1 första / andra, CPU, verkliga separata GUI-traps |
|---|---|---|---|---|
| **00 / #12** | 00/00/00 | **c21/CC63, $F197** | **c32/CC96, $F19F** | **c24 / c35** |
| **10 / #20** | 01/00/01 | **c23/CC69, $F289** | **c32/CC96, $F28F** | **c26 / c35** |
| **01 / #52** | 00/01/03 | **c21/CC63, $F37A** | **c33/CC99, $F382** | **c24 / c36** |
| **11 / #68** | 01/01/04 | **c23/CC69, $F471** | **c33/CC99, $F478** | **c26 / c36** |

Färgklocka är här **verklig debugger CC** i trapbilder, inte bara tre gånger källcykel; destination `RESP1` eller `GRP1` visas samtidigt. Real STELLA-minnesraster visar **båda RAM-byte**, inte bara två källnamn. Original-TIA-trapbilderna ligger i full ZIP under `evidence/traps/mode_XX/...`. CPU-write och GRP1-registeruppdatering är fortfarande **inte** interna START/reset/latch-signalspår, så exakt TIA-intern orsak till HBLANK-fenomenet anses inte slutligt isolerad. `WSYNC`-slutc39/38 (och c42/41 på sista raden efter JMP) är **SOURCE_ONLY**; efter en faktisk WSYNC visas nästa scanline/c0.

**VIKTIG, explicit verifierad frameindex-korrigering, ej pixelprediktionsändring:** Stellas debugger "Frame #12" har under samma autentiska trap **`FRAMELO=$0B` (11)**, frame#20→`$13` (19), frame#52→`$33` (51), frame#68→`$43` (67). Alltså är **`Stella Frame = source RAM FRAMELO + 1`** i dessa faktiska körningar. Ursprungliga första read-only-auditorn använde felaktigt `floor(StellaFrame/16)` för lägesgränserna, vilket placerade en verklig övergångsframe i fel RAM-grupp. Den färdiga läsanalysen använder nu **`floor((StellaFrame-1)/16) % 7`**, exakt som belagda RAM-register, medan alla fyra **preregistrerade X-mål ligger kvar oförändrade**. Inga ROM-/ASM-/spritefiler eller bilder har ändrats vid denna rättelse. Fulla 160 originalbilder stämmer sedan med korrekt, source-/RAM-belagd mode-sekvens och fyra rena stabila X-par.

## 5. Evidens, exakta green/red CI, hash och reproducerbarhet

**Komplett verifierad ZIP i rätt Google Drive-projektmapp** [`LET_ME_OUT_R1_F7_FULL_SOURCE_160_REAL_STELLA_16_TRAPS_SHA256_2026-11-16.zip`](https://drive.google.com/file/d/116aehSuMbRltvLm0DI68xvtiBQ30SVXT/view), Drive-ID `116aehSuMbRltvLm0DI68xvtiBQ30SVXT`, parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.

**ZIP bytes 4 939 383** · **ZIP SHA256 `da6f4ef206e608dbf92749d65e053d27eed4aa2f512e13dc125369766fddb29f`** · **394 ZIP-poster, CRC PASS**, **392/392 poster** listade i `EVIDENCE_FILE_INDEX.json` med filstorlek och riktig SHA256 **utan en enda mismatch**; `SHA256SUMS.txt` verifierad. Resterande två poster är index-/summafilerna själva. Innehåller:
- den enda körbara F7-ROM:en (SHA `ede93075...`) med fyra identiska banker;
- ASM, faktisk DASM-listning, symbolfil, original källbyggare, båda G0/canon-pinnarna och Python-audit;
- 160 riktiga crop-PNG och 160 riktiga full-GUI-PNG med perbild SHA, ursprungliga capture-logs;
- 16 verkliga registertraps för fyra faktiska RAM-lägen, separata mode/breakpoint-skript;
- 160-raders fullständig sannings-/pixel-/RAM-/NTSC-JSON och fyra kontrastkontroller;
- syntetisk negativ mutant uttryckligen märkt **NOT REAL STELLA**, käll-G0 och checksummor;
- fryst summary med ROM-/Actions-identiteter, SHA256 och full R1-blockering.

**Exakta Action-runs, även misslyckanden:**

| Run | Status | Faktiskt arbete och begränsning |
|---|---|---|
| [#43966545190](https://github.com/Odourman/let-me-out/actions/runs/43966545190) | **GREEN** | Obligatorisk SOURCE_ONLY G0; ingen ROM |
| [#43966843507](https://github.com/Odourman/let-me-out/actions/runs/43966843507) | **RED, X11-infra efter verkligt ROM-bygge** | **ENDA 16 KiB ROM** faktiskt kompilerad, SHA `ede93075...`; **16/16 riktiga PC/TIA GUI-traps**. Första raw-capture missade på övergående `BadWindow`, **0 falskt godkända rawbilder** |
| [#43967287553](https://github.com/Odourman/let-me-out/actions/runs/43967287553) | **RED, GUI-ready falsk negativ** | Samma ROM hämtad/låst, ingen DASM; kontrollen misstog röd CPU-sifferruta för svart GUI, trots synlig riktig Stella, 0 rawbilder |
| [#43967693889](https://github.com/Odourman/let-me-out/actions/runs/43967693889) | **RED, audit-infra efter lyckad råinsamling** | **160/160 riktiga raw+full-GUI** insamlade och SHA-checkade från samma ROM; offline-audit stoppade p.g.a. saknad genererad G0 JSON, **inte verklig geometri-Fail** |
| [#43968120975](https://github.com/Odourman/let-me-out/actions/runs/43968120975) | **RED, read-only frameindex-/typfel** | Samma 160 originalrutor + gamla 16 traps verifierade; 160 top-down exakta, men käll-FRAMELO korrelerades fel till debugger Frame (ett steg) och analysen avbröts med ett felaktigt `bool`-typantagande. Inga nya ROM, inga Stella |
| [#43968481385](https://github.com/Odourman/let-me-out/actions/runs/43968481385) | **GREEN, SLUTGILTIG READ ONLY** | Fyra korrekta 2×2 RAM-/pixelpar, **160/160** P0/M0/PF/262 + top-down masker exakta; **4/4 ortogonalitetskontraster PASS**, separat syntetisk mutant båda orakel FAIL, **392/392 filhashar PASS**. Ingen DASM/ROM/Stella efter de ursprungliga körningarna |

De fyra tidigare röda körningarna **förblir red**; de är reproducerbart förklarade och **inte** omdöpta till gröna. Den definitiva PASS:en kommer från **samma frysta ROM + redan existerande genuine raw-GUI-bevis** med korrekt debugger-RAM-proveniens och självständig slutlig hashverifiering, inte en omkompilerad femte geometri.

**Reproduktionskommandon (källkod för framtida separat uppdrag, ingen auktorisation att fortsätta nu):**

`/usr/bin/python3 r1_f7_preflight.py` (ren G0 på rätt fryst repo/filer), därefter `/usr/bin/python3 r1_f7_build.py` (en enda standard-F6 4K×4, kontroll SHA ovan); `bash r1_f7_capture.sh` (160 authentiska Stella debuggerraw från `frame #10` till `frame #170`), `bash r1_f7_trace.sh` (16 autentiska TIA-traps) och `/usr/bin/python3 r1_f7_audit.py --raw evidence/r1_f7_one_rom/raw --out evidence/r1_f7_one_rom/TRUE_160_FRAMES_2x2_SOURCE_CANON_PIXEL_AUDIT.json --mutants evidence/r1_f7_one_rom/SYNTHETIC_MUTANTS_NOT_REAL_STELLA`. Verifiera de frysta GitHub Actions/ZIP-instruktionerna om miljö/GUI skiljer sig. **Utför INTE kommandona som ett nytt projektsteg utan separat uttrycklig MAIN V-order.**

## 6. Samlad teknisk slutsats och STOPP

**Positiv, falsifierbar testgrind uppfylld:** Två **olika RAM-byte**, deras en-bit-state-värden i fyra verkliga debuggertraps, **två individuellt selekterade positionsfaser i en och samma ROM**, fyra tillåtna tidsplaner, exakta två top-down original-M/F på nio rader och fulla P0/M0/PF/262, **fysisk +6 X per selekterat objekt med den andra X oförändrad** i båda kontrastparen. Därmed giltigt **`F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`**.

**Uttrycklig gräns:** endast **2×2 binär X-väljbarhet** för **två** originalmasker i en isolerad NTSC-testkernel, inte kontinuerliga/godtyckliga RAM-X, inte två godtyckligt fria X, inte sex självständigt valbara X/Y, inte en E02-oavhängigt verifierad R1-kernel. **`ARBITRARY_TWO_X_NOT_PROVEN / SIX_FREE_XY_NOT_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`**.

**Alla F7-åtgärder avslutas nu.** Ingen ny ROM, DASM, Stella eller ytterligare fassvep, ingen R1-F8, tredje NPC, variabel Y, R1ba-korrigering, R2/R3/R4, PAL, HUD/KEY/GAME OVER, grafikändring, fullspel, PR #7-merge, issue#8-VERIFICATION eller annan framtida implementation har auktoriserats eller utförts. MAIN V fattar separat beslut om varje möjlig fortsättning.

**Slut:** `F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS / ARBITRARY_TWO_X_NOT_PROVEN / SIX_FREE_XY_NOT_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`.
