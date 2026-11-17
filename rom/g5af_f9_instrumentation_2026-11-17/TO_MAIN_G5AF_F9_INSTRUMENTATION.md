# LET ME OUT! – ROM DEVELOPMENT III → MAIN VII
## LM-D22 / G5AF: fryst F9, instrumenteringsreparation och exakt två mätkörningar

**Datum:** 2026-11-17 · **Roll:** ROM DEVELOPMENT III · **Globalt, tillåtet slututfall: `G5AF_INSTRUMENTATION_READY_BOUNDED`**.

**Mandat:** [GitHub Issue #14](https://github.com/Odourman/let-me-out/issues/14) och [G5AF bindande fullorder](https://github.com/Odourman/let-me-out/blob/9063a5ad8f725093e57c1a6e5c6848e2a9d60518/docs/gates/G5AF_MAIN_VII_LM_D22_F9_INSTRUMENTATION_ONLY_REPAIR_RETEST_AUTHORIZED_2026-11-17.md), original Git blob `a518648d7eaa820bce5983d84eeea22c732fa194`. Faktabakgrund: [MAIN VII G5AE receipt](https://github.com/Odourman/let-me-out/blob/9063a5ad8f725093e57c1a6e5c6848e2a9d60518/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) blob `e7f107a813f7ca8337b002e128b443c6ca4865c1`, [G5AD oförändrad blockerarrapport](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/rom/g5ad_tia_calibration_2026-11-17/TO_MAIN_G5AD_TIA_CALIBRATION.md).

**Scope:** endast testa reparerad debugger-/CI-instrumentering på en **redan existerande, exakt fryst** F9 ROM. **Inga** nya `.asm/.bin/.lst/.sym`, inga DASM-rebuilds, inga nya TIA-C0–C4/N1, ingen H4, G1/G6/F12/S05/fem NPC, ingen omritning, ingen merge, ingen oberoende Verification. All faktisk observation här är i **Stella 6.7.1**, inte Atari-originalhårdvara.

### A. Originalkällbunden root cause: autoexec-ordningen
1. Stellas [`PromptWidget::loadConfig` 6.7.1](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L369-L411), Git blob `ea5897160504e9f1308b46fcb10613b5eed4ac57`, anropar `debugger().autoExec(&history)` **innan** `_promptStartPos = _promptEndPos = _currentPos`.
2. [`Debugger::autoExec`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/Debugger.cxx#L175-L201), blob `1d943b0408fbce2b528e047a3552780ac90c30c5`, exekverar `autoexec.script`.
3. [`DebuggerParser::executeSaveSes`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L2027-L2057), blob `6dfa63dfaff70f803529a9be075617ed2784f805`, anropar `prompt().saveBuffer`, vars implementation i [`PromptWidget::saveBuffer`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L931-L957) bara itererar upp till `_promptStartPos`.
4. **Stark orsakshypotes:** G5AD:s `saveSes` låg **inne i initieringens autoexec**, varpå `_promptStartPos` ännu inte beskrivit färdiga prompt-rader. Verkligt gammalt [G5AD-jobb 134308674746](https://github.com/Odourman/let-me-out/actions/runs/44159356697/job/134308674746) dokumenterar `SESSION_FILE_BYTES=0`.
5. **Utförd ändring, utan Stella-patch:** `autoexec.script` sätter endast `base #10, frame #136, trapWriteIf ..., run`. Efter att `xdotool` har sett **faktiskt synlig debugger-GUI**, skickas två separata uppsättningar **interaktiva** `print pc; print _fCount; print _scan; print _sCycles; print _bank; tia; print pc; print _scan; saveSnap; saveSes`. Nya `saveSes` gav **1 709 och 1 707 byte med verkliga numeriska värden**. Resultatet bekräftar **reparerad utdata i denna setup** och är förenligt med källhypotesen. Den interna variabeln `_promptStartPos` loggades inte separat; hypotesens exakta interna tillstånd är inte direkttestat.
6. **Separat G5AD `IndentationError`:** gammal felindenterad `import shutil` efter `snapshots.append` är en separat objektivt observerad Python-bugg, inte bevis för Stellas promptfel. Ny modul `audit_evidence.py` skrivs med konsekvent indentering, `python3 -m py_compile` godkänd i båda G5AF-körningarna. Inga G5AD-frysta filer skrevs över.

### B. Kontrollerade försök, EXAKT två Actions-mätkörningar
| Försök | Faktiskt run/job | Observerat | Class |
|---|---|---|---|
| 1 | [44177844355](https://github.com/Odourman/let-me-out/actions/runs/44177844355), [134373876852](https://github.com/Odourman/let-me-out/actions/runs/44177844355/job/134373876852) | M-stopp saknade synligt promptfönster efter blinda 6 s, NOT_DETERMINABLE. F-stopp **gav faktisk 1707-byte session+320×228 native bild**, men CSV-parsern läste misstaget `$70` (112) före verkligt `#123` på `print _scan`-utskriften. 24 filer i bevarad artifact; CI FAIL. | `PARTIAL_NOT_READY` i första försöket |
| 2, sista | [44178247577](https://github.com/Odourman/let-me-out/actions/runs/44178247577), [134375317996](https://github.com/Odourman/let-me-out/actions/runs/44178247577/job/134375317996) | M GUI syntes vid poll **8**, F vid poll **2** efter max 24-poll-reparation. Parser tar nu det faktiskt avslutande Stella-`#dec`-värdet. Två icke-tomma, separata, läsbara Stella-sessioner och nativa bilder. ROM SHA före/efter godkänd, Python compile godkänd. Alla 2 testfall godkända. | **`G5AF_INSTRUMENTATION_READY_BOUNDED`** |

**Ingen tredje körning.** Separat [Actions-jobb `verify-preserved-artifact` 134376162352](https://github.com/Odourman/let-me-out/actions/runs/44178247577/job/134376162352), i **samma andra run**, laddade ned den redan uppladdade artefakten på en ny runner, kontrollerade alla ingående SHA256SUMS och exakt två sessioner/bilder med TIA-transkript och slutade `G5AF_ARCHIVE_READBACK_NUMERIC_TIA_AND_PNG_SHA256_PASS`. Det är en filbevarandekontroll, **inte** ett tredje emulatorprov.

### C. Exakt uppmätta CPU-/TIA-/scanlinevärden i Stella
*Båda: fryst F9 mode 000, NTSC/F6; originalets källprotokoll [`r1_f9_trace.sh`](https://github.com/Odourman/let-me-out/blob/8145a50607942202315439477bd378ba92fbdba1/rom/v018/experiments/r1_free_xy/r1_f9_trace.sh), Git blob `adfd24b2d0109ab665b5f65a594eec965886599b`; frame 136, scanline 123; `trapWriteIf` på `RESP1` efter registret. Filens gamla CPU-fönster är **förregistrerad source-stimulus**, inte uppmätta finalvärden.*

| Kontroll ID | CPU PC från `print pc` | `_fCount` | `_scan` | `_sCycles` | `_bank` | P1 `GR` / `pos` | Stellas faktiska sessionsstorlek |
|---|---:|---:|---:|---:|---:|---|---:|
| `F9_000_M_RESP1` | `$F1F0` = 61936 | 136 | 123 | 21 | 0 | `%00011000`, pos 3 | 1 709 byte |
| `F9_000_F_RESP1` | `$F1F8` = 61944 | 136 | 123 | 32 | 0 | `%00100100`, pos 33 | 1 707 byte |

Båda `tia`-utskrifterna innehåller `COLUxx: P0=$1e P1=$0e PF=$26 BK=$00`, `P0 GR=%00111100 pos=#129`, `M0 disabled pos=#158` samt fler register-/PF-statusfält. PC och `_scan` lästes **två gånger per stopp**, före och efter `tia`, och matchade; ingen emulator-`run/step` gjordes mellan. Det är faktiska promptsvar, **inte** CPU-source-estimat.

**Viktig källdetalj vid parserrevision:** Stellas uttryck `print _scan` ger `INPT3|$70(R): $7b %01111011 #123`; `$70` är symbolens registeradress; det numeriska värdet är **`#123`**. Motsvarande `print pc` visar `$f1f0 ... #61936`, `print _sCycles` ger `#21` resp `#32`. Andra parsern testades mot verklig sessionsfil och ställde in trailing decimal som värde.

**Kritiskt oförändrat:** `trapWriteIf` är inte en rå per-colorclock `STA RESP1`-write-eventlogg; `PC` vid paus ska inte utan extra källa betecknas exakt sista `STA`-cykel. Stella `TIADebug::toString` dokumenterar även `TODO: strobes? WSYNC RSYNC RESP0/1...` och skriver inte själv RESP-strobes. F9:s nedladdade artifact saknade extern käll-`.lst/.sym` vid denna ROM-path; sessionsfilen säger detta tydligt. Vi har PC+CPU-värden och TIA-state, men inga påståenden om exakt `STA`-slutlatens eller intern START.

### D. Verkligt bevarade native bild- och sessionsfiler (SHA-256)
**Rå slut-artefakt**: [GitHub Actions 44178247577 artifact 14370213586](https://github.com/Odourman/let-me-out/actions/runs/44178247577/artifacts/14370213586), **arkiv-ZIP SHA-256** `a5d80efa75cc7948cf29fd8cd5ea21620176d0844d9db9e433ecd97298da3ad9`.

| Kontroll | Bevarad Stella session, SHA-256 | Bevarad Stella-native TIA PNG 320×228 RGB, SHA-256 |
|---|---|---|
| M | `1ea943b27a58a218bb1215117a055cab45c98d8c099b97e9029726801c8a15f9` | `078c9c1ce249cb8c9ef6a45dc322647db2e1a869b3f60635c9e27436f38c016a` |
| F | `3b63819f04303f154cb54b72dd1cc25edcbffb3d2f5688e8612dca30da97e24f` | `1797454e84c23662ba35101ee479b435a792ac774f8ea089dffac8e286bcdc2d` |

Arkivet innehåller **33 filer**, 32 separat hashade i `SHA256SUMS.txt`, samtliga återlästa med SHA256-kontroll **i verifieringsjobbet och efter att den verkliga artifact-zippen laddats ned**. Nativa bilder är **faktiska** `saveSnap`-TIAsurfaces, inte Xvfb-GUI. Två bilder skiljer sig på **51 RGB-pixelpositioner** enligt separat offline `PIL/ImageChops`-jämförelse (bbox `(0, 100, 59, 103)`); detta är en **bildjämförelse**, inte ett tidsbevis för de enskilda TIA-colorclock-slotsen. Numeriska PC/frame/scan/cycles står endast i de två original-textevidenserna.

Arkivet innehåller `keyboard_commands.txt` och `autoexec.script` per kontroll med exakt inmatning, `prompt_ready.txt`, `gui_ready_poll.txt`, `stella_stdout.log`, `versions.txt`, `ROM_SHA_PRE/POST.txt`, `G5AF_PARSE_DIAGNOSTICS.json`, `G5AF_INSTRUMENTATION_EVIDENCE.csv` och en kontrollbar `SHA256SUMS.txt`. GitHub har även en **byteidentisk CSV-kopia** [G5AF_INSTRUMENTATION_EVIDENCE.csv](G5AF_INSTRUMENTATION_EVIDENCE.csv), blob `1ec5e145faf4fe3d84ff3f6c2df280bcf1709b6d`.

**Första negativa rå-artefakt:** [44177844355 artifact 14369464567](https://github.com/Odourman/let-me-out/actions/runs/44177844355/artifacts/14369464567), SHA-256 `d1e9b8a33b6fdebbde03ce26b4229883c83d948dbcf37f92670e8f7092a0da58`. Bevarad som negativ kunskap, inte överskriven av finalen.

### E. Verifierat och ej verifierat
- **Ja inom G5AF:** Efter-initialisering `saveSes` fungerar med faktiska numeriska värden. Två olika original F9 PC-/cykellokaler, identisk frame/scan/bank, registerstate `tia`, originalnative PNG, session- och bild-SHA, samma ROM-hash, två-stopp stabilitet och separat artefaktåterläsning. Python-kompilering och korrigerad decimalparsing fungerade.
- **Nej, inget PASS:** Full write-strobe-TIA-time series eller överföring av `RESP/GRP` till intern TIA-START/colorclock; originalhårdvara; G5AD sex C0–C4/N1; H4/G1/G6/F12/S05; femfienderskärna; varje annan ROM eller ändring av källcanon. Native snapshots är del av pausen men ger inte i sig skanningsposition för varje råpixel under skrivögonblicket.
- **Bedömning:** Arbetsordern efterfrågade en *instrumenteringsbenchmark*, inte en avgränsad ny ROM-mätserie. De två G5AF-stoppens korrelation och verifierbara arkivering uppfylls. Därför `G5AF_INSTRUMENTATION_READY_BOUNDED`, **inte** bredare `STELLA_HARDWARE_PASS`.

### F. Leverans och stopp
- **Branch:** `rom-dev-iii/g5af-lm-d22-f9-instrument-only-20261117`, start på `main` `9063a5ad8f725093e57c1a6e5c6848e2a9d60518`. Alla ändringar endast nya instrumentskript, dokument och workflow, inga originalfiler. Inga merges eller PR.
- **Källor att granska:** `run_f9_instrument.sh`, `audit_evidence.py`, [prereg](PREREGISTERED_STOPS_AND_SCOPE.md), [reproduktion](REPRODUCE_AND_RAW_EVIDENCE.md), [CSV](G5AF_INSTRUMENTATION_EVIDENCE.csv), `.github/workflows/g5af_f9_instrument_retest.yml` plus original GitHub Actions artifact ovan. Hela källproveniens i filmanifest.
- **STOPP:** Leverans av **en** avslutad LM-D22/G5AF instrumentreparation. `G5Z_G0=INCONCLUSIVE_NO_ROM` och `G5AD=NO_BUILD_INSTRUMENTATION_BLOCKER` lämnas oförändrade. `G5_FORMAL_OPEN`. **Ingen** fortsättning till ny G5AD-ROM, H4/G1/G6/F12/S05/fem-NPC, oberoende Verification eller merge utan separat uttrycklig användarauktorisation.
