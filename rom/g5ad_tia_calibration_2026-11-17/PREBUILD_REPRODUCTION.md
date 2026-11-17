# G5AD – PREBUILD_README / TEST_PROTOCOL (NO NEW ROM)
**Utförare:** ROM DEVELOPMENT III · **Datum:** 2026-11-17 · **Status:** `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`.

**Avsikt:** Detta reproducerar **enbart den utförda instrumentkontrollen**. Det är **inte** en PLAYTEST för G5AD (ingen G5AD-ROM finns), inte en ny G1 eller framtida testauktorisation.

## Källor
- [Issue #13](https://github.com/Odourman/let-me-out/issues/13) auktoriserar en **villkorad** exakt en-ROM-kalibrering; §5 kräver stopp före bygg om reella register- och råpixeltider inte kan styrkas.
- [G5AD order på granskat main-commit](https://github.com/Odourman/let-me-out/blob/aaaeef0522a746cf4f23faee9fcf2c49dd572d02/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md).
- [Fryst sexscenmatris](https://github.com/Odourman/let-me-out/blob/aaaeef0522a746cf4f23faee9fcf2c49dd572d02/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv).
- [Stella Debugger officiellt](https://stella-emu.github.io/docs/debugger.html), med `saveSes`, `saveSnap`, `runToPc`, `print`, `_scan`, `_sCycles`, `trapWriteIf` och `autoexec.script`. Det är funktioner som manualen beskriver, men deras **samverkande funktion i vår automatiserade CI-session har inte verifierats**.
- [G5AD isolerad CI-kontroll-workflow](../../.github/workflows/g5ad_prebuild_instrument_check.yml) på branch `rom-dev-iii/g5ad-tia-calibration-lm-d21-20261117`. Ingen annan workflow eller ROM-source skapades.

## Reproduktion av faktiskt utförda steg (historik, ingen uppmaning att köra ny mätning)
1. GitHub Actions `ubuntu-24.04`, `sudo apt-get install -y dasm stella xvfb xdotool x11-utils imagemagick python3-pil`. På [success run 44158817619](https://github.com/Odourman/let-me-out/actions/runs/44158817619): paket `dasm 2.20.15~20201109+really2.20.14.1-2`, `stella 6.7.1+dfsg-1build2`, `python3-pil 10.2.0`, Xvfb 1366×900×24, `DISPLAY=:152`. Första [run 44158684786](https://github.com/Odourman/let-me-out/actions/runs/44158684786) saknade `xdpyinfo` och klassificerades **INFRA FAIL**, innan ROM.
2. För **sista två** förkontrollerna laddades en **redan existerande, fryst** F9-binära från GitHub Actions original `44050126727` med `actions/download-artifact@v4` och namnet `LET_ME_OUT_R1_F9_ONE_ROM_AND_ACTUAL_STELLA_PARTIAL_OR_COMPLETE_G1`. Exakt 16 384 bytes; `sha256sum` gav den redan frysta SHA256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`. Detta var **inte** ett G5AD-bygge.
3. Script i `$HOME/.config/stella/autoexec.script` innehöll:
   ```text
   base #10
   frame #3
   print _fCount
   print _scan
   print _sCycles
   print _bank
   tia
   saveSes
   saveSnap
   ```
   Utförd emulatorkommandorad:
   ```sh
   stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$readonly_rom"
   ```
   I en separat Xvfb-session med `DISPLAY=:153`, `SDL_AUDIODRIVER=dummy`, `SDL_VIDEODRIVER=x11`. Resultatet gick att kontrollera mot `/home/runner/session_*.txt` och `/home/runner/*_dbg_*.png`.
4. [Run 44159089329](https://github.com/Odourman/let-me-out/actions/runs/44159089329), [job 134307740733](https://github.com/Odourman/let-me-out/actions/runs/44159089329/job/134307740733), visade att native PNG skapats `320×228 RGB`, men **inga** `_scan/_sCycles`-strängar i sessionsfilen. Provets kontrolldom: `NO_MACHINE_READABLE_DEBUGGER_AND_NATIVE_PIXELS; STOP_NO_ROM`.
5. [Run 44159356697](https://github.com/Odourman/let-me-out/actions/runs/44159356697), [job 134308674746](https://github.com/Odourman/let-me-out/actions/runs/44159356697/job/134308674746), skrev uttryckligen `SESSION_FILE_BYTES=0`. Efter detta följde `IndentationError` i vår egna Python-postprocess; felaktig indentering medgavs och **bevaras** som separat negativt testresultat, inte bortförklarat. Native PNG skapad igen på runner men **ej bevisat sparad i leveranspaket**. Inga färg-/CC-pixlar eller registertider för G5AD påstås.
6. Proveniens och paketen ligger i Actions ovan. [Sista råa workflow artifact](https://github.com/Odourman/let-me-out/actions/runs/44159356697/artifacts/14362582337), och maskinläsbart [case-disposition CSV](G5AD_CASE_DISPOSITION.csv) anger alla sex `NOT_DETERMINABLE`. Utfört test stoppade **före G5AD-genererad .asm eller .bin**.

## Tydlig mätgräns
- `DASM/STELLA_AVAILABLE` är **observerad och loggad**.
- `F9_EXISTING_ROM_SHA_MATCH` är **observerad och loggad**.
- `F9_NATIVE_TIA_PNG_CREATED` är **observerad och loggad**.
- `G5AD_DEBUGGER_CPU_WRITE_POSTSTATE_CSV`, `G5AD_FROZEN_ROM_SHA`, `G5AD_C0_C4_N1_ACTUAL_CC` är **NOT_OBTAINED/NOT_RUN**. Tolka inte tidigare F9 source-test som en ny kalibrering.
- `G5AD_ROM_BYTES=0` (inte en nollbyte-ROM utan **ingen ROM-fil**), `G5AD_ASM=ABSENT`, `DASM_BUILD_G5AD=NOT_RUN`, `STELLA_RUN_G5AD=NOT_RUN`. En användare ska inte försöka välja scener i ett spel eller köra `PLAYTEST` från detta paket.
- Efter stoppet finns inget tillstånd att starta ytterligare automation, bygga en G5AD-ROM på egen hand, återuppta H4 eller G6.

**Slutlig specialiststatus:** `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`. Detaljer i [TO_MAIN](TO_MAIN_G5AD_TIA_CALIBRATION.md).
