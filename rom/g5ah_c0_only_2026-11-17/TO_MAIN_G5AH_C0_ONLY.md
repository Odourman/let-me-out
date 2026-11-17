# LET ME OUT! – ROM DEVELOPMENT III → MAIN VIII
## LM-D23 / G5AH C0 ONLY – STOPP EFTER HÅRD FÖRGRIND; INGEN C0-ROM

**Datum:** 2026-11-17. **Bindande status:** `G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER`.
**Ingen C0-ROM, ASM, DASM-build, C0-X40/104 Stella-rendering, fysisk C0 colorclock-kalibrering eller ROM SHA** har skapats eller mätts. **Endast en av högst två tillåtna nya Actions-mätkörningar** utfördes; efter misslyckad förgrind STOPP enligt arbetsorderns §3, ingen korrigerings-/tredjekörning.

### 1. Precis auktorisation och källor, live granskade
- [G5AH LM-D23 bindande fullorder](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/docs/gates/G5AH_MAIN_VIII_LM_D23_C0_ONLY_TIA_MEASUREMENT_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md), Git blob `878809fed7228d36cd0e746bd4ca8f9443726b48`; [Issue #15](https://github.com/Odourman/let-me-out/issues/15); [statusindex](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), Git blob `d4207ba790df192466c1716c18ba74b1ae07d9ba`.
- [MAIN VIII Stella 6.7.1 källaudit](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/docs/gates/MAIN_VIII_STELLA_671_TIA_MEASUREMENT_CAPABILITY_SOURCE_AUDIT_2026-11-17.md), blob `d33d86d35e732ab91994ed631a54d34f33c528ba`; [MAIN VIII G5AF→TIA brief](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/docs/gates/MAIN_VIII_G5AF_TO_NEXT_TIA_DECISION_BRIEF_SOURCE_ONLY_2026-11-17.md), blob `435fd1c7a195938a4533cfbfc807cf60b9cabf28`.
- [C0-only original sixfallsmatris](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv), Git blob `ba56e95d1729afac0a0df2ce4993c2bfdaa996b2` – bara `TIA-C0` användes som möjligt kommande experiment; övriga förblev historiskt NOT_RUN. [Frysta TOP-DOWN originalmaskerna](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/design/NPC_REFERENCE_8x9_masks.json), oförändrade.
- **Alla sex GitHub Project Sources `CURRENT_V6`** + [V6 blobmanifest](https://github.com/Odourman/let-me-out/blob/63ad3d43bd10e8a4bce644fedc949e0542c8c17a/docs/project_sources/CURRENT_V6/GIT_BLOB_SHAS.txt) kontrollerade; uppladdade V5 i ChatGPT är historiska och supersederas av V6. **Officiell Drive-status** [här](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit) och [V6-guiden](https://docs.google.com/document/d/1ixFG1C4ky5c1cFj0U7B9V5UmMal627IqsxTUpcyktf0/edit) lästes direkt. Det är navigering, inte implementationsauktoritet.
- Historisk [G5AF LM-D22 F9 RAW metod](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/REPRODUCE_AND_RAW_EVIDENCE.md) återläst och **inte** körd igen under dess förbrukade mandat.

### 2. Fryst prebuild-stimulus och faktiskt utfall
**Ny separat branch:** `rom-dev-iii/g5ah-lm-d23-c0-only-20261117`, från exakt `main=63ad3d43bd10e8a4bce644fedc949e0542c8c17a`; endast G5AH-dokument, förgrindsharness/workflow. Ingen merge, inget gameplay, ingen ny .asm/.bin/.lst/.sym producerad. F9 `.lst/.sym` kopierades under samma ROM-stem inne i Actions runner **för att möjliggöra originaldebuggerns källkorrelation**; detta är read-only originalmetadata i runner, inte nytt byggt program.

**Den enda nya Actions-körningen:** [run 44193946233](https://github.com/Odourman/let-me-out/actions/runs/44193946233), [capture-job 134430286409](https://github.com/Odourman/let-me-out/actions/runs/44193946233/job/134430286409) **FAIL**, [readback-job 134430694476](https://github.com/Odourman/let-me-out/actions/runs/44193946233/job/134430694476) **FAIL**. Readback-jobbet är **ingen andra ROM-/emulatormätkörning**. Inga fler Actions-mätkörningar har startats.

**Reproducerad strikt positiv KÄLLkontroll, inte runtime-kalibrering:**
- Arkiverad **F9 F6 NTSC 16 384 byte**, hash före/efter `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, original Actions [44050126727](https://github.com/Odourman/let-me-out/actions/runs/44050126727), bevarade ursprungliga `.asm/.lst/.sym/.4k.bin` i arkivet.
- F9 4 KiB-banken upprepas byteexakt fyra gånger, och registerinstruktionerna `$F1EE = 85 11 = STA RESP1`, `$F1F0 = 85 1C = STA GRP1`, `$F1F6 = 85 11 = STA RESP1`, `$F1F8 = 85 1C = STA GRP1` matchade det F9 frysta list-/binärpaketet.
- Alla nio **original M 8×9 TOP-DOWN**-maskrader i F9:s källkod verifierades i rätt ordning `3C 3C 18 FF 18 24 24 42 42` mot nuvarande originalmaskdata. Komplett numerisk råkälla: `F9_SOURCE_LIST_SYM_MASK_STATIC_CHECK.json` i det faktiska Actions-arkivet. Detta bekräftar **F9:s källkod**, inte en C0-ROM eller ens ett emulerat C0-maskutfall.
- [Stella 6.7.1 `TiaOutputWidget.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/TiaOutputWidget.cxx) `drawWidget()` duplicerar 160 TIA-indexpixlar till 320 skärmpixlar och ritar en **3×3 electron-beam-markör** på bilden; `saveSnapshot` beskär till `width*2`. [`TIAConstants.hxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIAConstants.hxx) anger 160 synliga CC och 68 hblank. Detta är **SOURCE_MODEL_INFERRED**; det finns inte en ny nativ pixelbild att validera C0:s synliga X mot.

**Förregistrerat tänkt verkligt debuggerstopp:**
```text
base #10
frame #136
break $f1ee
run
```
Vid första synliga Stellafönster (poll 3) skickades `print pc/_fCount/_scan/_sCycles/_bank/X0_SELECT`, `disAsm $f1ee #4`, `tia`, `saveSnap`, `saveSes`, `step`, därefter samma kontroll efter instruktionen. Källhypotesen var `$F1EE STA RESP1` → `$F1F0` efter 3 CPU-cykler med separerade `SOURCE_INFERRED`-busstid och `STELLA_OBSERVED`-tid. Men **denna hypotes verifierades ALDRIG i körningen**.

**Faktiskt runtime-NEGATIVT:**
- `gui_title.txt` innehåller `Stella 6.7.1: "r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6"`, **inte** `Stella 6.7.1: Debugger mode` som vid fungerande G5AF. Sparad `DEBUGGER_GUI_HELP_ONLY.png` visar **vanlig spelbild**, inte aktiv debuggerprompt. Detta styrker att preflight-harnessens `break $f1ee`/`run` **inte gav det avsedda synliga stoppet före insamling**. Varför break inte nåddes är **inte fastställt**, och får inte tillskrivas en generellt trasig Stella-debugger.
- `commands_sent.txt` visar **vad xdotool försökte skriva**, inte att debuggern exekverade det. Varken `pre_step_debugger_session.txt`, `post_step_debugger_session.txt` eller `pre_step_native_TIA.png`, `post_step_native_TIA.png` skapades/bevarades. `PHASE_A_ACTUAL_AUDIT.json` markerar alla faktiska CPU-/scanline-/register-/RAM-X/PNG-värden **MISSING**. `PHASE_A_VERDICT.txt = FAIL_HARD_NO_BUILD`. Därmed saknas förgrindens återläsbara `PC, STA, _sCycles, frame, scan, bank` ihop med native 160-CC pixlar.
- Inga `STA RESP0`-tidsvärden, inga C0 numerisk RAM-X=40 eller 104, inga C0 maskpixlar observerades. *G5AF:s andra historiska F9-PASS ändras inte av det nya testets snävare negativa mätning.*

### 3. Råartifact, negativa hashkontroller och efterhandsräddning
- [Exakt sparad original Actions-artifact 14378620744](https://github.com/Odourman/let-me-out/actions/runs/44193946233/artifacts/14378620744), **23 368 byte ZIP**, dess verkliga självberäknade SHA256 samt Actions-reporterade digest: `e9966c7cbdc17e62484cbc7775f9c8f031dc936c76f37e8c9c3cc4466306453e`. 18 arkivposter; original SHA256SUMS.txt listade 17.
- **Viktigt separat negativt problem, ej dolt:** Actions `readback-hashes`-jobb **FAIL** därför att original `SHA256SUMS.txt` angav SHA256 för en **tom** `stella_stdout.txt` medan filen efter emulatorns shutdown innehöll `X connection to :157 broken (explicit kill or server shutdown).`. Filens verkliga SHA256 vid arkivering var `de0db306e362a36d1b20e1a92dd88116e4e9d3b993b04064f1da07adb6e9cb1e` i stället för tomfilens `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Förändringen skedde **efter** att originalmanifestet skrevs, när cleanup-stoppet stängde X11.
- Vi har därefter **faktiskt laddat ned original ZIP-artefakten och separat kontrollerat alla 17 FILERNAS SHA-256 över de arkiverade, oförändrade bytesen**. Den återberäknade separata filen [RECOVERED_ACTUAL_ARTIFACT_SHA256SUMS.txt](RECOVERED_ACTUAL_ARTIFACT_SHA256SUMS.txt) är en **postmortem-verifiering**, inte det ursprungliga lyckade Actions-jobbet. Originalets FAIL och felaktiga hash är kvar; original ZIP är inte omskriven. **Detta ändrar inte förgrindens FAIL.**

### 4. Stopp enligt bindande order, inte universell teknikdom
**SLUTVERDICT = `G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER`.** Orsaken är att den enda utförda förgrinden **inte** kunde påvisa en faktisk, stabil debuggerinstruktionssekvens och pixelevidens, trots positiv käll- och 2×bildmappinggranskning. Ett fel i just detta script motbevisar **inte** Stellas allmänna funktionalitet, C0-konceptets möjliga implementerbarhet eller Atari 2600-spelvisionen.

**Inget C0-bygge har påbörjats.** Både C0-mode `X=40` och `X=104` = `NOT_DETERMINABLE; NOT_RUN_NO_ROM`. Ej godkända C1–C4/N1, H4/G1/G6/F12, S05, fem-NPC, nya regler/mapper, oberoende Verification eller merge har inte påbörjats. `G5_FORMAL_OPEN`; äldre `G5Z_G0_INCONCLUSIVE_NO_ROM`, `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`, `G5AF_INSTRUMENTATION_READY_BOUNDED` kvarstår oförändrade.

**Efter denna slutrapport: STOPP.** MAIN VIII mottar och kan bedöma annan separat uttryckligt godkänd framtida metod. Det krävs en **ny auktorisation** för vidare exekvering; använd inte oanvänd andra Actions-försöksmarginal som automatisk tillåtelse efter hård NO_BUILD-grind.
