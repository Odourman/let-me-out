# LET ME OUT! / G5AF LM-D22 – Reproduktion och råbevis
**Slutverdict:** `G5AF_INSTRUMENTATION_READY_BOUNDED` för **just de två F9-registerstoppen**.
**Auktoritet:** [Issue #14](https://github.com/Odourman/let-me-out/issues/14) och [G5AF bindande order](https://github.com/Odourman/let-me-out/blob/9063a5ad8f725093e57c1a6e5c6848e2a9d60518/docs/gates/G5AF_MAIN_VII_LM_D22_F9_INSTRUMENTATION_ONLY_REPAIR_RETEST_AUTHORIZED_2026-11-17.md).
**Projekt:** ingen ny ROM eller ASM; ingen DASM-kompilering, inga gameplay- eller TIA-C0–N1-test.

## 1. Frysning, versionskontroll och källa
- Standard-F6/NTSC, historisk F9 `r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin` = **16 384 byte**.
- Exakt historisk F9 SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`; verifierad i CI både före/efter med `sha256sum -c`. Binären kom oförändrad från Actions [44050126727](https://github.com/Odourman/let-me-out/actions/runs/44050126727), artifact `LET_ME_OUT_R1_F9_ONE_ROM_AND_ACTUAL_STELLA_PARTIAL_OR_COMPLETE_G1`.
- GitHub Ubuntu 24.04; `stella 6.7.1+dfsg-1build2` (Stella 6.7.1), Xvfb, xdotool, ImageMagick, PIL. Ingen Stella källkod har modifierats.
- Exakt två förregistrerade F9 registerstopp härleds ur det frysta [r1_f9_trace.sh](https://github.com/Odourman/let-me-out/blob/8145a50607942202315439477bd378ba92fbdba1/rom/v018/experiments/r1_free_xy/r1_f9_trace.sh): `frame #136`, `_scan == #123`, `RESP1` och timingband **19..23** respektive **30..34**, båda exklusiva. Den separata [PREREGISTERED_STOPS_AND_SCOPE.md](PREREGISTERED_STOPS_AND_SCOPE.md) publicerades **före båda Actions-mätningarna**.
- Reparationskod är `run_f9_instrument.sh`, `audit_evidence.py`, workflow `/.github/workflows/g5af_f9_instrument_retest.yml`. G5AD:s historiska `IndentationError` bevaras, rättning sker i ny egen verifierad Python-fil med `python3 -m py_compile`.

## 2. Endast utförda två nya CI-mätningar
1. [Första körning 44177844355](https://github.com/Odourman/let-me-out/actions/runs/44177844355), [capture job 134373876852](https://github.com/Odourman/let-me-out/actions/runs/44177844355/job/134373876852), **FAIL men råmaterial arkiverat**. `F9_000_M_RESP1` hann inte få synlig Stella-GUI inom blind väntan 6 s; `F9_000_F_RESP1` skapade **1707 byte** icke-tom native `saveSes` och **320×228** TIA PNG. Parsern läste fel `_scan=112` från **registeradressen `$70`** trots faktiskt konsolsvar `#123`. `G5AF_PARTIAL_INSTRUMENTATION_NOT_READY`, inte förkastade/dolda mätdata. [Original Actions-artifact 14369464567](https://github.com/Odourman/let-me-out/actions/runs/44177844355/artifacts/14369464567), SHA256 archive `d1e9b8a33b6fdebbde03ce26b4229883c83d948dbcf37f92670e8f7092a0da58`; dess 24 filer lästa lokalt och SHA256SUMS kontrollerad.
2. [Andra och sista körning 44178247577](https://github.com/Odourman/let-me-out/actions/runs/44178247577), [capture job 134375317996](https://github.com/Odourman/let-me-out/actions/runs/44178247577/job/134375317996), **PASS**. Riktade ändringar: väntar upp till 24 pollningar på **faktisk** synlig debugger-GUI (första ställdes synlig poll 8, andra poll 2); parsern väljer sista `#<decimal>` i Stella-kommandots utskrift i stället för tidigare registeradress; korrekt Python-indentering. **Endast samma två F9-stopp på samma binär**. [Original Actions-artifact 14370213586](https://github.com/Odourman/let-me-out/actions/runs/44178247577/artifacts/14370213586) och separat [verifieringsjobb 134376162352](https://github.com/Odourman/let-me-out/actions/runs/44178247577/job/134376162352), **PASS**. Artefakt ZIP SHA256 `a5d80efa75cc7948cf29fd8cd5ea21620176d0844d9db9e433ecd97298da3ad9`.

**Högst två körningar**: `44177844355` + `44178247577`; ingen tredje och ingen H4/G5AD-relaterad ROM. Det separata `verify-preserved-artifact`-jobbet i **samma andra Actions-run** kontrollerar arkivfilerna, det är inte en tredje emulatormätning.

## 3. Granska rådata utan ny emulator-körning
1. Öppna [Actions-artifact 14370213586](https://github.com/Odourman/let-me-out/actions/runs/44178247577/artifacts/14370213586) och ladda ned `G5AF_F9_ORIGINAL_READONLY_NATIVE_TIA_AND_DEBUGGER_EVIDENCE.zip`. Artifact är publicerad med **90 dagars** retention enligt workflow; länken kan upphöra efter lagringstiden.
2. Packa upp. Den innehåller **33 filer**; exakt **32 filer** ingår i `SHA256SUMS.txt` (självmanifestet är inte self-referential). Kör `sha256sum -c SHA256SUMS.txt` i arkivroten; samtliga 32 verifierades både i Actions andra kontrolljobb och separat efter nedladdning från GitHub.
3. Öppna `G5AF_INSTRUMENTATION_EVIDENCE.csv`. [Byteidentisk kopia i GitHub](G5AF_INSTRUMENTATION_EVIDENCE.csv) har Git blob `1ec5e145faf4fe3d84ff3f6c2df280bcf1709b6d`, samma blob som den på nytt beräknade lokala `git hash-object` för Actions-filen.
4. Varje case-katalog innehåller `debugger_session.txt`, `native_TIA_original.png`, `keyboard_commands.txt`, `autoexec.script`, `prompt_ready.txt`, `gui_ready_poll.txt`, `session_source_files.txt`, `native_source_files.txt` samt en separat hjälpskärmbild `debugger_GUI_1366x900.png`. **Endast** `native_TIA_original.png` är Stellas nativa råbild; GUI-skärmbilden är inte TIA-bevis. Se även `G5AF_PARSE_DIAGNOSTICS.json`, `ROM_SHA_PRE.txt`, `ROM_SHA_POST.txt`, `versions.txt`.
5. I `debugger_session.txt` visar Stellas verkliga prompt:
   ```text
   > print pc
   $f1f0 %1111000111110000 #61936
   > print _fCount
   ram_88(R/W): $88 %10001000 #136
   > print _scan
   INPT3|$70(R): $7b %01111011 #123
   ```
   Fallet F har PC `$f1f8 #61944`. Observera att `$70` är registeraddress, inte aktuellt `_scan`-värde; **`#123` är det numeriska utskriftsvärdet**.
6. Filnamn/case-ID, kända `trapWriteIf`-fönster, samma ROM-hash och frånvaron av `run/step` mellan `print pc; print _scan; tia; print pc; print _scan; saveSnap; saveSes` binder registertext till samma **frysta debuggerstopp**. Auditen kontrollerar att PC/scan förblir desamma före/efter TIA-avläsningen. Källnivå `RESP1`-fönster är stimulusevidens, **inte** full rå write-strobe-tidslinje.

## 4. Begränsningar / stoppspärr
- `saveSes` skrev 0 byte i G5AD **inne i autoexec**; det korrigerade `saveSes` exekverades **efter** GUI-promptinitiering och gav **1709/1707 byte**. Source-ordningsförklaringen är därmed empiriskt förenlig med utfallet, men ingen separat intern diagnostisk trace av `_promptStartPos` utfördes.
- `TIA`-text ger aktuell TIA-status, bl.a. `COLUxx`, P0/P1 GR/pos och M0 status. Stella `TIADebug::toString()` skriver **inte** de rena `RESP0/RESP1`-strobe-händelserna som råa register. Det är därför inte ett G5AD C1/START-latchbevis.
- Native TIA 320×228 och CPU-stoppon är från samma pausade emulatorprocess men bilderna är en frusen frame-buffer. Exakt synlig colorclock- eller interna TIA-latensangivelser per pixel **har inte härletts och får inte uppfinnas**. Dessa var inte mandatet i G5AF.
- `G5AF_INSTRUMENTATION_READY_BOUNDED` är **endast** två original-F9-kontroller i **Stella 6.7.1**, inte original-Atari-hårdvaruverifiering, full H4, G6/F12, S05, fem-NPC, G5_PASS eller tillstånd att fortsätta.
