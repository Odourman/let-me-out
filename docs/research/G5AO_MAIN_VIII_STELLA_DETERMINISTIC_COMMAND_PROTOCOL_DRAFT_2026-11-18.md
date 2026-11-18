# LET ME OUT! – MAIN VIII G5AO: föreslagen deterministisk Stella 6.7.1-kommandotransport

**Datum:** 2026-11-18. **Klass:** `SOURCE_ONLY_PROTOCOL_DESIGN / NO IMPLEMENTATION`. Användaren har uttryckligen godkänt offline-förstudien genom "Låter bra, gör så", **inte** ett nytt ROM-/emulator-/Actions-implementationssteg. Denna specifikation är **rådgivande arkitekturforskning**, inte godkänd spelcanon eller färdig fungerande verktygskedja.

**Källgrund:** [G5AN – analys av Stella 6.7.1 `PromptWidget`, `DebuggerParser::run/exec`, `saveSes`, G5AL-runner](https://github.com/Odourman/let-me-out/blob/main/docs/research/MAIN_VIII_G5AN_G5AL_POST_RUN_PROMPT_SAVESES_TRANSPORT_SOURCE_ONLY_2026-11-18.md), fryst [G5AL specialistrapport](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/TO_MAIN_G5AL_F9_METHOD.md), samt [18 körda, helt syntetiska offlinetester på exakt fryst parser](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AO_MAIN_VIII_EXACT_FROZEN_G5AL_PARSER_OFFLINE_FIXTURE_RESULTS_2026-11-18.md). `G5AL_F9_TRAP_CONTROL_FAIL` och `G5_FORMAL_OPEN` förblir gällande.

## 1. Varför ett nytt protokoll behövs

G5AL:s `xdotool type` → `Return` → `sleep 0.40` garanterar inte att Stellas GUI accepterat färdig rad, utfört korrekt parserfunktion eller återställt prompten. Ett fönster med titel `Stella 6.7.1: Debugger mode` är inte sådan kvittens. `saveSes` kopierar den tidigare renderade promptbufferten till en fil; filen i sig ger ingen transaktions-ID, ingen atomic state-snapshot och inget bevis på ordning för alla avsända `print`. G5AL run 1 visar verkligt sammanfogad `print pcprint _fCount`/parserfel, run 2 visade efter nytt debuggerfönster ingen ny fungerande `saveSes`. **Inget tidigare A/B/C-PASS får därmed tillskrivas G5AL.**

Utöver transporten finns **två separata statiska auditfel**: `*_session.txt` mot `*_debugger_session.txt` och en för bred `endswith("HANDSHAKE")` som skuggar exakta återinträdes-PC-regler. [G5AO:s 18 offlinefixtures](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AO_MAIN_VIII_EXACT_FROZEN_G5AL_PARSER_OFFLINE_FIXTURE_RESULTS_2026-11-18.md) visar konkreta falska PASS/FAIL och en lokalt korrigerad kontrafaktisk variant. **Verifierad offlinekonsistens är en nödvändig förutsättning, inte emulatorbevis.**

## 2. Förslag: transaktionsbaserat, tvådelat protokoll

**Detta är ett kravförslag för en eventuell senare, separat auktoriserad teknisk adapter, inte en påstådd funktion i omodifierad Stella 6.7.1.** Använd en versionsbunden **single-thread-owned kommandokö** nära Stellas befintliga `Debugger::run`/`DebuggerParser::run` och state transition i `EventHandler`. All in/utdata ska vara entydig och maskinläsbar. CPU-/TIA-åtkomst får inte ske från en osynkron extern nätverkstråd.

### A. Kommando- och kvittenskontrakt

Varje transaktion ska bära:
- `protocol_version` och `session_id` för en ren emulatorkörning; `run_id`, `emulator_build_sha`, `ROM_SHA256`, `bank_scheme=F6`, `TV=NTSC` och korrekt tidskälla;
- strikt ökande `command_seq`, `stage=A|B|C`, exakt `command` och `expected_state`; **exakt en outstanding kontrolltransaktion**;
- `accepted` från emulatorns **verkliga kommandoväg**, `executed` från parserkörningen samt **parserns verkliga returvärde eller deterministiskt instrumenterat motsvarande**; `success` måste kontrolleras mot definierad grammatik, inte bara att en sträng skickades;
- `state_before`, `state_after`, `emulator_epoch` och `debugger_entry_seq` samt felklass (`INPUT_NOT_ACCEPTED`, `PARSER_ERROR`, `STATE_TRANSITION_UNEXPECTED`, `TIMEOUT`, `EVIDENCE_MISSING`);
- ett särskilt `snapshot`-objekt (om kommandot mäter state): atomiskt definierade `pc`, `frame`, `scanline`, `sCycles`, `bank`, TIA-REG-värden och snapshots-/transkriptfilens SHA och filstorlek.

**Nödvändig åtskillnad:** `command accepted` ≠ `parser executed` ≠ `state observed` ≠ `archive readback verified`. Arkivhash `PASS` får aldrig automatiskt uppfylla A/B/C. Ett internt `run`-svar kan vara tillståndsövergång, inte att nästa trap redan har inträffat.

### B. Zuståndsmodell och händelseordning

Tillåt endast explicita övergångar enligt denna modell:

```text
PROCESS_START
 -> DEBUGGER_READY(epoch=0, verified command-response)
 -> FRAME_ADVANCED(frame=136, same debugger epoch)
 -> TRAP_ARMED(verified parser ACK)
 -> RUNNING(run_command_seq, no further debug queries)
 -> DEBUGGER_REENTERED(new debugger_entry_seq, event reason=RESP1 trap)
 -> ATOMIC_STOP_SNAPSHOT(PC/frame/scan/cycles/bank/TIA)
 -> ARTIFACTS_FINALIZED(after Stella/Xvfb shutdown and wait)
 -> SEPARATE_ARCHIVE_READBACK
```

**`run` är en asynkron gräns:** [Stella `DebuggerParser::executeRun`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L1808-L1814) anropar `debugger.exit(false)`; [`EventHandler::leaveDebugMode`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/EventHandler.cxx#L2623-L2636) byter från debugger till emulering, medan [`Debugger::setQuitState`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/Debugger.cxx#L776-L787) dessutom kan exekvera **en CPU-instruktion** när debugläge lämnas. Nästa debuggerhändelse måste vara en **ny händelse från samma ROM-/processkörning**, med egen monotont ökande entry-ID och korrekt trap-/breakpointorsak. En tillfällig X11-titel och gamla numeriska värden får aldrig återanvändas.

En event-/command-logg ska skrivas append-only som **JSONL med ett objekt per händelse**, byggas färdigt och hash-signeras först efter process-stopp. Vid framtida CPU-/TIA-mätning krävs en dokumenterad mekanism för att samla alla state-fält atomiskt, så `PC` inte oavsiktligt avser en annan pauspunkt än `scanline`/TIA-register.

### C. Förslag på ren datastruktur (illustration, ej exekverat)

```json
{"schema":"lmo-debug-v0","session":"synthetic-example","seq":12,
 "kind":"DEBUGGER_REENTERED","entry_seq":2,"reason":"RESP1_WRITE_TRAP",
 "parent_run_seq":11,"emulator_state":"DEBUGGER","ROM_sha":"expected-F9-hash",
 "pc":"F1F0","frame":136,"scan":123,"sCycles":21,"bank":0,
 "evidence_class":"DESIGN_EXAMPLE_NOT_STELLA_OBSERVED"}
```

Denna exemplarstruktur **är inte en faktisk Stella-logg**; det är hur korrekt typade framtida bevis bör se ut.

## 3. Acceptanskriterier för en eventuell framtida F9-scopegrind (INTE AKTIV)

**Först** rätta och testa offline:
1. **Samma enda sessionspath** i writer, `--gate`, finalaudit och arkivmanifest. Exakt stage-name, `_debugger_session.txt`-suffix, ingen fallback till gammal/stale fil.
2. **Specifika stage-grindar före generiska**, med per-stage PC/frame/scan/bank/cycles och promptkvittens. Syntetiskt fel PC `$F000` måste **avvisas** i både A och B återinträde, och korrekta `$F1F0`/`$F1EE` godtas bara med rätt event/epoch.
3. Separat negativ-fixture-katalog: sammanfogade kommandon, saknat Enter, saknad `saveSes`, gammal session med giltiga PC men fel entry-ID, omkastad kommandosekvens, `bank=4`, fel frame/scan, dubblettkvittens, `break`-toggle som `cleared`, missad native-fil och arkiv-SHA som PASS trots metod-FAIL. För varje fel **fail closed**.
4. **Undvik att tolka ack från `saveSes` ensamt som ett oberoende kontrollprotokoll.** Om tillförlitlig returkanal saknas: `NOT_DETERMINABLE`, inte `PASS`.

**Därefter** kan en separat framtida A/B/C-kontroll definieras för **exakt fryst F9** SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, F6/NTSC. För A: faktiskt nytt RESP1-stopp `PC=$F1F0`, frame136, scan123, `_sCycles=21`, verkligt bank0–3 (F9:s fyra bankbilder byteidentiska), native 320×228 TIA; B: verkligt bankbundet `set` före `$F1EE` och bevisat event; C: en verklig `step` `$F1EE → $F1F0` med cykelbevis. **Detta är endast framtida kravförslag**, aldrig retroaktivt G5AJ/G5AL-PASS eller C0/colorclock-verifikation.

## 4. Teknisk avvägning mellan tillgängliga kandidater

| Metod | Varför/varför inte | Rekommendation |
| --- | --- | --- |
| Befintlig GUI-`xdotool` plus fler sekunder `sleep` | Ingen äkta kommandoack; G5AL:s längre väntan efter `run` gav ingen session | **Avråd** från ännu en testfamilj byggd på enbart timing |
| GUI-`saveSes` som efterhandskvittens | Export av tidigare promptbuffert; samma instabila inputtransport används för att utföra exporten; risk för stale eller falskt godkännande | Behåll endast som **sekundärt arkivbevis**, inte primär state-trafik |
| Native `exec`/autoexec.script | [Stella 6.7.1 `DebuggerParser::exec`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L135-L163) anropar parsern per rad men **kastar bort varje kommandos retursträng**; `run` byter dessutom GUI-state | Kan användas för statisk setup **men inte primärt numeriskt svarprotokoll** |
| Extern standard-TCP/CLI debugger i *omedifierad* Stella 6.7.1 | Ingen tillgänglig sådan verifierad av granskade originaldelar, och ingen bevisad stabil per-kommando-svarsport | **Inga nya antagna funktioner**; påstå inte att den existerar |
| **Separat C++-adapter i Stella 6.7.1:s egen kommandoväg**, med serialiserad intern event- och statejournal | [`Debugger::run`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/Debugger.cxx#L221-L224) har retursträng och state-händelser finns i [EventHandler](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/EventHandler.cxx#L2588-L2636). Potentiellt verkliga ACK och atomic stop-snapshots. Men kräver **separat auktoriserad emulatorfork/bygnad, API-design, kontroll mot stock Stella och oberoende verifiering** | **Mest lovande långsiktiga kandidat, EJ IMPLEMENTERAD/EJ AUKTORISERAD** |

### Bedömning av om intern adapter är värd arbetet

**Preliminärt JA, för en senare strikt avgränsad prototype – men bara efter offline-parserreparation och fryst protokollkontrakt.** De befintliga G5AF/G5AJ/G5AL-resultaten visar faktisk Atari-F9-rendering och fungerande första steg men upprepade **automationsmisslyckanden**. Att justera `xdotool` utan riktig state-/parserkvittens ger därför svag förväntad evidensnytta; en in-process serialiserad adapter skulle direkt kunna lösa den observerade klassen av brister. **Dock:** ingen kod är byggd, ingen integration är testad, Stella 6.7.1:s interna threading/eventmodell är inte här fullständigt bevisad och instrumentation kan förändra beteendet. Det krävs stock-vs-instrumented jämförelse och senare separat oberoende Verification II innan någon för hög status påstås.

**Minsta rimliga framtida arkitektur-PoC (INTE AUKTORISERAD):** få ett enda `print pc`-kommando med unik seq/ACK och korrekt PC, ett `run` som emitterar tillståndsskifte och sedan faktiskt *ny* trap-entry, och en atomisk snapshot från samma stopp, allt på en känt fryst F9-referens utan nya Atari-ROM-ändringar. Om det inte fungerar går man inte vidare till B/C, C0 eller pixelcolorclock.

## 5. Aktiva spärrar och ansvar

**G5AO är en MAIN-ledd, offline-källförstudie och syntetisk parser-egenkontroll**, inte ett genomfört programmeringsuppdrag åt ROM DEVELOPMENT III. RESEARCH II kan ge ytterligare rådgivande designanalys. ROM DEVELOPMENT III kan **endast** implementera ett separat, uttryckligen auktoriserat framtida scope; VERIFICATION II granskar först när självständig order finns. Ingen specialistchatt har automatiskt verkställt något genom detta dokument.

**Gällande:** `G5AL_F9_TRAP_CONTROL_FAIL`, 2/2 förbrukade, Issue #17 stängt. `G5AJ_F9_TRAP_CONTROL_FAIL` 2/2. G5AH ursprungligt hash-FAIL förblir historiskt. G5AF bounded F9-PASS är historiskt. **`G5_FORMAL_OPEN`.** Ingen ny emulator-/Actions-run, ingen C0- eller Atari-ROM, ingen B/C-mätning, inget PR-merge, ingen G6/S05 eller Verification II, ingen automatisk ny LM-D26. G5AO medför **ingen ersättning av Project Sources**.
