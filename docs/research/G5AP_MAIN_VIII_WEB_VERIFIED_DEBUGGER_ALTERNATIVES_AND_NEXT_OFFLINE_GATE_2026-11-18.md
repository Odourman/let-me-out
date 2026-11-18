# LET ME OUT! – MAIN VIII G5AP: webbkällkontrollerade debuggeralternativ och nästa offline-grind

**Datum:** 2026-11-18. **Klass:** `WEB_RESEARCH + CONNECTED_GITHUB_SOURCE_REVIEW + MAIN_DECISION_PREPARATION`. **Ingen Stella-, Gopher2600-, DASM-, ROM- eller GitHub Actions-körning i denna granskning.** Ingen implementerad patch. Ingen oberoende Verification II. **`G5_FORMAL_OPEN`.**

**Uppdragsgrund:** Användarens uttryckliga "Sök på internet efter lösningar på våra problem. Följ sedan din rekommendation" efter G5AO:s [faktiskt genomförda 18/18 offline-fixtures](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AO_MAIN_VIII_EXACT_FROZEN_G5AL_PARSER_OFFLINE_FIXTURE_RESULTS_2026-11-18.md) och [förslag till kommandoprotokoll](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AO_MAIN_VIII_STELLA_DETERMINISTIC_COMMAND_PROTOCOL_DRAFT_2026-11-18.md). Den rekommenderade **första** arbetsgrinden är en separat **ROM DEVELOPMENT III OFFLINE parser-/fixture-reparation**; användaren har *inte* med detta godkänt ett nytt Atari-ROM-steg, att ändra emulator, köra nya Stella/Gopher2600-mätningar eller automatiskt ta nästa G5-/G6-gate.

**Bindande aktuell nulägeskälla:** [G5AM MAIN VIII mottagen G5AL FAIL](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AM_MAIN_VIII_G5AL_LM_D25_F9_TRAP_CONTROL_FAIL_SOURCE_RECEIPT_2026-11-18.md), G5AL `G5AL_F9_TRAP_CONTROL_FAIL` 2/2, G5AJ `G5AJ_F9_TRAP_CONTROL_FAIL` 2/2, G5AH `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` med ursprungligt hash-Fail, G5AF enbart `G5AF_INSTRUMENTATION_READY_BOUNDED`. B och C för G5AL har aldrig körts. F9:s original F6/NTSC 16KiB SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, fryst [G5AL specialistcommit `f16e1e4`](https://github.com/Odourman/let-me-out/commit/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431) och gammal parserblob `f159c1f8668c1f504fd9538a8d1ef17b2ddefafa` får aldrig redigeras retroaktivt.

## 1. Nya verkliga källfynd från webbsökning

### A. `xdotool --window` använder en annan X11-sändväg än fokuserad input

**Primärkälla:** [xdotool-projektets officiella `xdotool.pod`, avsnitt SENDEVENT NOTES](https://github.com/jordansissel/xdotool/blob/main/xdotool.pod) och [maintainerns redogörelse i Issue #453, maj 2024](https://github.com/jordansissel/xdotool/issues/453).

Dokumentationen säger uttryckligen att `xdotool type --window <id>` skickar X11 `XSendEvent`, där `send_event`-flaggan kan göra att applikationer ignorerar kommandon; input till det **aktiva** fönstret går normalt via **XTEST**. Frys uppgiften att G5AL:s [`send()`](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/run_g5al_f9.sh#L140-L148) verkligen använder `xdotool type --window "$wid"` + `xdotool key --window "$wid" ... Return`. **Det är en mekaniskt möjlig felkälla av exakt relevant sort.**

**Inte bevisat:** Att Stella 6.7.1 alltid ignorerade dessa events, eller att det ensamt orsakade sammanslagningen `print pcprint _fCount` eller uteblivet `saveSes`. G5AL hade redan verkliga korrekta kommandosvar i samma miljö. Även XTEST via aktivt fönster garanterar inte promptredo, parserkvittens eller atomisk CPU/TIA-snapshot. **En ren XTEST-/sleeprättning får därför inte bli en ny körserie utan ytterligare protokollkontroll och separat auktorisation.**

### B. Gopher2600 har nu ett faktiskt **HEADLESS**-läge via stdin/stdout

**Externa webbkällor:** [Gopher2600:s officiella repository](https://github.com/JetSetIlly/Gopher2600) och [releasenotes v0.55.0](https://github.com/JetSetIlly/Gopher2600/releases), som beskriver `gopher2600 headless roms/Pitfall.bin` för pipad input/output. Senaste publicerade release verifierad **v0.57.2, 2026-08-13**; källans `master` vid granskning **`74c544203378c1448a33c29bc8b4586079b050f4`, 2026-11-16**. Kräv versionspinning; välj inte automatiskt en senare version.

**Direkt läst primärkälla via ansluten GitHub (starkare än marknadsbeskrivning):**
- [`gopher2600.go` vid pin `74c5442`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/gopher2600.go#L289-L318): `HEADLESS` finns, hjälptexten lyder **"pipe debugger commands to stdin"**, debuggerstart utan GUI, `PlainTerminal`.
- [`debugger/terminal/plainterm/plainterm.go`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/debugger/terminal/plainterm/plainterm.go#L41-L100): läser hela kommandorader från `os.Stdin` genom `bufio.Reader.ReadString('\n')`, avvisar ofullständiga rader vid fel, och skriver/flushar svar mot `os.Stdout`. Det är **verifierad källa för en direkt stream-transaktionskanal utan X11-tangentautomation**. Notera: terminalen utelämnar `StyleEcho` och garanterar inte egna kommandosekvens-ID:n; klienten måste korrelera rader till konkreta svar/händelser.
- [`debugger/commands_template.go`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/debugger/commands_template.go#L30-L104): `RUN`, `STEP`, `HALT`, `SCRIPT`, `GOTO`, `ONHALT`, `CPU`, `TIA`, `TV`, `BREAK`, `TRAP`, `SCREENSHOT`.
- [`debugger/commands_help.go`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/debugger/commands_help.go#L30-L100): `QUANTUM` stöd för **INSTRUCTION, CYCLE, CLOCK (tre färgklockor per CPU-cykel)**; `GOTO` kan sikta på frame/scanline/clock. **Viktig begränsning:** `SCRIPT` får **inte** innehålla `RUN`. Använd `HEADLESS` med separata stdin-kommando-/svartransaktioner, inte antagande om script-run.
- [`headless/headless.go`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/headless/headless.go#L31-L115): screenshot är möjlig även utan GUI. Gopher-screenshot är **inte automatiskt samma native 320×228 Stella-TIA-bild**, kan vara crop/scaled.
- [`hardware/memory/cartridge/cartridge.go`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/hardware/memory/cartridge/cartridge.go#L287-L311) stödjer **F6** med `newAtari16k`; [`mapper_atari.go` [52–56]](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/hardware/memory/cartridge/mapper_atari.go#L52-L56) beskriver `$1FF6..$1FF9`.
- [`macro/doc.go`](https://github.com/JetSetIlly/Gopher2600/blob/74c544203378c1448a33c29bc8b4586079b050f4/macro/doc.go#L16-L67) har en frame-`WAIT` och `SCREENSHOT` för automatisering, men är **inte** ett substitut för per-registerkommandon eller ett `RUN` till specifik trap i debugger.

**Teknisk slutsats:** Gopher2600 HEADLESS är nu en **källstyrkt, låg-I/O-risk-kandidat för en senare, oberoende F9-CPU/TIA-testväg**, mer attraktiv än att direkt skriva en Stella C++-patch. **Men den är en annan emulator**: numeriska TIA-/colorclock-resultat måste jämföras separat med Stella 6.7.1 och kan **inte** retroaktivt uppfylla specifika `STELLA_OBSERVED`-grindar. Inget live HEADLESS-F9-test har körts av MAIN.

### C. Äldre `stella-lua` finns, men är inte en aktuell Stella 6.7.1-lösning

[`tcr/stella-lua`](https://github.com/tcr/stella-lua) visar en inbäddad Lua-debuggermodell med CPU-register och `peek`. GitHub-repo metadata kontrollerad: default `release/5.1`, senaste push **2019-06-12**. **Ingen visad kompatibilitet med exakt Stella 6.7.1**, ingen stabil integration/underhållsbevisning. **AVRÅDS från att importera som standardlösning** utan separat revisions-/sårbarhets-/licenskontroll.

## 2. Teknikval och ordningsföljd (skilj stöd och utförande)

| Kandidat | Källkontroll | Risk kvar | Beslut |
| --- | --- | --- | --- |
| **Offline reparation av G5AL-parserns felaktiga sessionsnamn och skuggade PC-grindar** | Båda falska PASS/FAIL reproducerade i G5AO **18/18 syntetiska fixture-assertioner** | Förblir offline och kan inte visa debugger-/ROM-beteende | **GÖR FÖRST via separat snäv ROM DEVELOPMENT III-order** |
| **Gopher2600 HEADLESS stdin/stdout** | Faktiskt stöd för F6, direkta kommandorader, CPU/TIA/klocksteg och skärmdump | Annan emulator; okänd exakta F9 trap-/register-/bildkontrakt tills separat körning | **FÖRSTA tekniska runtime-kandidat för framtida *oberoende jämförelse*, EJ KÖRD/AUKTORISERAD** |
| **Stock Stella 6.7.1 XTEST + serialiserade kvittenser** | Officiell xdotool-dokumentation visar skickskillnad | Inget robust emulator-ACK, risk för missad GUI-readiness; G5AL negativt | **ENDAST möjlig senare jämförelsemetod, inget nytt försök nu** |
| **Separat in-process Stella C++ adapter** | `DebuggerParser::run` har intern retursträng, Stellas state machine är tillgänglig | Kräver egen patch/bygnad, synkronisering, instrumenteringsbias, stock-vs-patched-validering | **RESERVPLAN, efter Gopher-analys och offline-PASS**, EJ IMPLEMENTERAD |
| **Gamla Stella-Lua-forken** | Existerar, men push 2019, annan releasegren | Ålderdomlig kod och versionsrisk | **Inte förstahandsval** |

**Beslutsmotivering:** Felen i parsern är **bevisade utan emulering**. En ny emulatorprovrunda innan parser/fixtures har genomgått offline-regression riskerar att slösa ytterligare felklassificerade experiment. Först därefter görs en separat explicit ny G5-instrumenteringsauthorization om användaren så beslutar, med en *ny* tids-/körgräns – aldrig återanvänd G5AJ/G5AL 2/2.

## 3. MAIN:s nya SNÄVA nästa offline-uppdrag

**Godkänt av användarens "Följ sedan din rekommendation", i detta skede ENDAST som ny offline-parserreparation och regressionskontroll av ROM DEVELOPMENT III.** Utföraren måste få verklig handoff; det här dok kan i sig inte starta en annan specialistchatt.

**Scope:**
1. Ny isolerad branch med **ny kopia** av G5AL:s frysta `audit_g5al.py` (originalblobs får inte ändras), en kanonisk per-stage `<STAGE>_debugger_session.txt`-path och gemensam pathresolution för `--gate` och finalaudit.
2. Prioritera **exakta** A/B-`REENTRY_HANDSHAKE` (PC `$F1F0`/`$F1EE`) **före generiska** A/B initial-handshake; bind varje parsed PC till faktiskt `print pc` i relevant transaktion, acceptera inte återanvänd gammal `Stella 6.7.1`-header som färskt entrybevis. Stoppa på bank `0..3` utanför, felaktigt frame/scan, för gammal fil, stängd/cleared `break`, `print pcprint _fCount`, saknad native TIA, staging/manifest-skillnad och positiv archive-hash trots A/B/C-FAIL.
3. **Inga fabricerade emulator-PASS.** Fixture-data ska vara markerade `OFFLINE_SYNTHETIC`; tidigare 18 G5AO-assertioner blir minimala baseline, komplettera med negativa/stale/ordreferens-/session-ID-scenarier. Frys fixturehashar, kör locally offline och publicera maskinläsbar PASS/FAIL-matris samt reproducerbar instruktion.
4. Kontrollera att en **ny** syntetisk fullaudit med korrekt A men saknat B/C klassas `PARTIAL_NOT_DETERMINABLE` och att A-strikt-fel blir FAIL. Testkoden får inte tyst försvaga G5AL:s verkliga A/B/C-krav eller reparera historiska resultat.
5. Leverera ny `TO_MAIN`, frozen commit, exakt testlogg, `MANIFEST` och ev. oföränderlig Drive-arkivkopia. **Inga gamla G5AO/G5AL-filer ändras**.

**Stopp:** Detta är **OFFLINE_PARSER_FIX_ONLY**. Ingen ny Stella/Gopher2600-instans, ingen GitHub Actions-run, ingen ROM/DASM/ASM/BIN, inget emulatorfork-bygge, ingen F9/C0-spelmätning, ingen PR-merge, ingen oberoende Verification II, ingen automatisk C0/G6/5NPC-/S05-implementation. En senare extern emulator-kontroll eller egen C++-adapter kräver ett **nytt, separat, uttryckligt användarbeslut** med specificerat scope och stop limits. **`G5_FORMAL_OPEN`**.

**Project Sources:** V6 är navigering; inga nya manuella källfilsbyten krävs för denna research/ordern.
