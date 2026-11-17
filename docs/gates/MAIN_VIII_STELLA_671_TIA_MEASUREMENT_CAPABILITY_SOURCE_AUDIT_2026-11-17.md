# LET ME OUT! – MAIN VIII: Stella 6.7.1 TIA-mätbarhet, versionstroget source-audit

**Datum:** 2026-11-17. **Roll:** MAIN VIII. **Klass:** `SOURCE_ONLY_CAPABILITY_AUDIT`. **Auktorisationsläge:** `NEXT_TIA_EXPERIMENT_NOT_AUTHORIZED`.

Detta är en *ny granskning av den faktiskt använda Stella-versionens kommandon och TIA-källkod*, inte ny mätning, inte direkt emulatorkörning, inte oberoende VERIFICATION II och inte ett godkännande av full H4, S05, fem-NPC eller G6. Ändra inte historiska frysta källor/negativa resultat.

## 1. Aktuella projektoriginal / varför auditen behövs

- [Aktuellt statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) och [MAIN VIII:s tidigare G5AF→TIA beslutsbrief](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_VIII_G5AF_TO_NEXT_TIA_DECISION_BRIEF_SOURCE_ONLY_2026-11-17.md).
- [Fryst G5AF-källrapport](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md), [rå-CSV](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/G5AF_INSTRUMENTATION_EVIDENCE.csv) och [F9:s frysta trap-script](https://github.com/Odourman/let-me-out/blob/8145a50607942202315439477bd378ba92fbdba1/rom/v018/experiments/r1_free_xy/r1_f9_trace.sh).
- [LM-D21/G5AD frysta C0–C4/N1-matris](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv); utfallen är fortsatt `NOT_RUN_NO_NEW_ROM` efter [G5AE:s NO_BUILD](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md).
- Google Drive originalarkiv: [aktiv status](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit); [G5AF-arkivkopia](https://docs.google.com/document/d/1MvpvQEAwQRlPr_CH2VVy-gY5LYjebzkPxcUDh0Rk71g/edit). Sex [V5 Project Sources](https://github.com/Odourman/let-me-out/tree/main/docs/project_sources/CURRENT_V5) förblir en vägvisare, inte spelcanon.
- Källgranskningens *externa primärkälla* är **Stella-repositoryt i exakt tag `6.7.1`**, inte nuvarande webbmanual för Stella 7.0. Detta är **ingen** ny lokal DASM/Stella-runtime-test.

## 2. Källbelagda funktioner – finns respektive finns inte i exakt Stella 6.7.1

| Källställe | Direkt belagt | Slutsats för framtida testdesign |
|---|---|---|
| [DebuggerParser.cxx 6.7.1](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L3364-L3405), [implementation step/trace](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L2120-L2176) | `step` finns (exekverar en instruktion) och `trace` finns (stegar över subrutin); `disAsm` finns | De är **inte** en automatisk per-colorclock-logg av alla TIA-registerstrobes. Korrelera pre-/post-instruktions-PC, opcode, cykeltal och faktisk bild separat. |
| [DebuggerParser.cxx 6.7.1](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L3068-L3090) | `logBreaks` finns (breakpoint/trap-loggning). **Ingen `logTrace`-registrering finns i den granskade 6.7.1-parserkällan**. | Använd **inte** `logTrace` från [den nyare online-debuggermanualen](https://stella-emu.github.io/docs/debugger.html) som om kommandot vore bekräftat för 6.7.1. |
| [DebuggerParser.cxx trapWriteIf](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L2209-L2233) | En villkorad TIA-registerskrivtrap kan registreras | Ett pausat PC/`_sCycles`-värde ska inte utan ytterligare instruktionsanalys utges för *exakt* slutet av `STA RESPx`; G5AF markerar redan den här gränsen. |
| [TIA.cxx 6.7.1 `poke`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx#L529-L539) | `TIA::poke` uppdaterar emuleringen före registerswitch | CPU-tid, TIA-tid och när bildbufferten uppdateras måste hållas isär. |
| [TIA.cxx `RESP0/1`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx#L830-L843), [Player::resp](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx#L164-L172) | `RESPx` skickar den beräknade positionsräknaren till Player; Player har **ett särskilt villkor när en pixelgrupp redan håller på att renderas**. | En statisk X-formel räcker inte för C1:s båda ordningar; aktiv rendering/retrigger måste ingå i kontrollen. |
| [TIA.cxx `NUSIZ0`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx#L780-L788) | Samma `NUSIZ0`-skrivning når **både Missile0 och Player0** | C2/C3 måste räkna både P0- och M0-kopior, med båda objekten i samma Y. |
| [TIA.cxx `GRP0/1`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx#L806-L830), [`ENAM0`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx#L752-L757), [`TIA::cycle`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx#L1416-L1431) | `GRP` och `ENAM0` placeras i **DelayQueue**, som exekveras i TIA:s colorclock-loop | Värdet vid CPU-stopp och den visuella effekten kan avse **olika faser**. Ett CPU-registersnapshot ensamt mäter inte latch/latens. |
| [TIAConstants.hxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIAConstants.hxx#L30-L38) | 76 CPU-cykler/rad × 3 = 228 CC; 68 CC HBLANK, 160 synliga CC | Mät synliga X i **TIA-colorclocks**; 320 px bred native PNG är ett levererat bildformat, **inte** 320 oberoende TIA-colorclocks. Bekräfta bildkoordinat-, linje- och pixelparsmappning mot faktisk buffert före slutsats. |

Notera: genomgången verifierar **API och source-modell**. Den levererar inte bevis att någon automatisk komplett bus-event-tidslinje kan exporteras från omodifierad Stella 6.7.1. Det går alltså inte att budgetera ett nytt test som om `logTrace` eller raw-strobe-JSON redan fanns.

## 3. G5AF-data omvärderat – utan att skriva om G5AF

G5AF utförde exakt två Actions-mätförsök, varav andra blev `INSTRUMENTATION_READY_BOUNDED` för fryst F9. Rå-CSV anger två skilda `RESP1`-trap: PC `$F1F0` / `_sCycles=21`, respektive PC `$F1F8` / 32; frame 136, scanline 123, bank 0, sessioner 1709/1707 byte och nativa TIA-bilder 320×228. [Frozen CSV](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/G5AF_INSTRUMENTATION_EVIDENCE.csv). Bild och TIA-text är kopplade till ett fryst **debuggerstopp**, men det är inte en rå pixel-by-pixel skrivtidslogg. Inga C0–C4/N1 mättes.

`r1_f9_trace.sh` förregistrerade `trapWriteIf` och förväntade cykelband på just F9. Den **förutsåg** fönstren, men själva skriptets centervärden var inte nyuppmätt intern TIA-fas; G5AF:s separat sparade numeriska svar var riktiga **post-trap**-observationer. Skillnaden ska behållas.

## 4. Konkret source-only beslutskontroll före en ny auktorisation

**Mätkedjan består av separata påståenden.** Ett framtida specialistuppdrag skulle behöva bevisa följande i *den ordningen*, med varje osäker komponent märkt `NOT_DETERMINABLE`:

1. **CPU och kodposition:** fryst `lst/sym`/ROM-hash (vid eventuellt nytt bygge), faktisk bank, pre-/post-`STA`-PC och källinstruktion, löpande `_sCycles`/scanline. En trap stoppar vid instruktionens gräns; `_sCycles` får inte etiketteras som rå write-strobe utan separat underlag.
2. **TIA-fas / fördröjd effekt:** ange uttryckligen om en registerskrivning är direkt (`RESP`, med Player::resp-specifika villkor) eller köad (`GRP/ENAM`), och hur eventuell fördröjning kompenseras/observeras. Källmodell = `MODEL_INFERRED`, inte `STELLA_OBSERVED_RAW_WRITE`.
3. **Pixel-data:** frys samma Y/X och originalmask per kontrollpar; säkerställ frame/scanline→PNG-rad, 320-bildkolumn→0..159 synlig TIA-CC, startpunkt och tillåtna maskpixlar. Native bild ensam är inte bevis för write timing.
4. **Falsifierbar kontroll:** C0:s ensamma rättvända TOP-DOWN 8×9-bitmap med X=40/104 ska först ha uppmätt bild-X/CC och reproducerbar CPU-/TIA-korrelation. Utan den baslinjen går C1/C4-tolkningar inte att kalla bestämda. C2/C3 kräver M0 på samma aktiva Y; N1 är en negativ `COLUP0`-kontroll, inte universal-NO-GO.
5. **Resultatnivå:** `STELLA_OBSERVED` för faktiskt uppmätt emulatorbeteende; `SOURCE_MODEL_INFERRED` för källmodell; `NOT_DETERMINABLE` där ett steg saknas; separat framtida `VERIFICATION II` krävs för oberoende tekniskt mottagande.

**Konkret slutsats:** Före ett eventuellt nytt ROM-mandat bör MAIN kräva en *skriftligt falsifierbar metod* för mätning av pixel-CC och härledning av write-cykel, baserad på **de kommandon som faktiskt finns i 6.7.1**, inte generisk eller nyare Stella-manual. Alternativ med särskilt instrumenterad Stella, annan emulatorversion eller större harness vore en **annan teknisk metodfamilj** som inte redan är bevisad eller godkänd; föreslå den separat och utan att ändra originalemulator/historiska körningar i smyg.

## 5. Formell status / ingen ny order

`G5Z_G0_INCONCLUSIVE_NO_ROM`; `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`; `G5AF_INSTRUMENTATION_READY_BOUNDED`; `G5_FORMAL_OPEN`. Inga nya ROM/ASM/Stella/Actions, ingen aktiv G5AD/LM-D21 eller G5AF/LM-D22-order, ingen H4/G1/G6/F12/S05/fem-NPC-implementation, ingen ny oberoende Verification, ingen merge. PR #7 historiskt blockerad draft; Issue #8 uppskjuten. Fortsatt teknisk execution kräver ny **separat, precis användarauktorisation**.
