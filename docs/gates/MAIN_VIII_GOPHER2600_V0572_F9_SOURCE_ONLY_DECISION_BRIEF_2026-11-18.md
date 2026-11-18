# LET ME OUT! – MAIN VIII: Gopher2600 v0.57.2 F9 HEADLESS, source-only beslutsberedning

**Datum:** 2026-11-18. **Klassen:** `SOURCE_ONLY / DECISION_PREPARATION` (varken arbetsorder, ROM-bygge, emulatorkörning eller oberoende verifiering). **Formell G5-status:** `G5_FORMAL_OPEN`.

## 1. Varför denna granskning behövdes

- [G5AQ](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AQ_MAIN_VIII_G5AP_OFF01_OFFLINE_ONLY_PASS_SOURCE_RECEIPT_2026-11-18.md) godkände syntetisk G5AP-parserregression **98/98** (enbart `OFFLINE_SYNTHETIC`), inte verklig kommandotransport.
- [G5AL](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AM_MAIN_VIII_G5AL_LM_D25_F9_TRAP_CONTROL_FAIL_SOURCE_RECEIPT_2026-11-18.md) och G5AJ avslutades `F9_TRAP_CONTROL_FAIL`, **2/2 försök var förbrukade i respektive order**. G5AH:s ursprungliga hashavvikelse och C0 no-build kvarstår. [G5AF](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_VIII_G5AF_TO_NEXT_TIA_DECISION_BRIEF_SOURCE_ONLY_2026-11-17.md) ger endast begränsad instrumentation, inte pixel-fysik-pass.
- [Tidigare research](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AP_MAIN_VIII_WEB_VERIFIED_DEBUGGER_ALTERNATIVES_AND_NEXT_OFFLINE_GATE_2026-11-18.md) källgranskade Gopher2600 revision **`74c544203378c1448a33c29bc8b4586079b050f4`** som tänkbar efterföljare. ROM DEVELOPMENT IV har senare **rapporterat installerad officiell Gopher2600 v0.57.2, revision `2af86eb725739adbf3d9d45cea2ed69eea57da2a`** i Codex Cloud `let-me-out` [Issue #19](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310). Dess ny-task-persistens är **specialistrapporterad 8/8 SHA-PASS**; [MAIN:s G5AT](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_VIII_G5AT_G5AR_ENV01_FRESH_CLOUD_TASK_SPECIALIST_PASS_PENDING_RAW_EVIDENCE_2026-11-18.md) väntar ännu rå originalutskrift. **Inget verktyg har körts av MAIN i denna granskning.**
- GitHub-revisionjämförelsen mellan `74c5442...` och `2af86eb...` visade **diverged**: `2af86eb...` är **10 commits ahead och 137 behind** den tidigare forskningspinnen. Tre relevanta filblobbar har faktiskt olika SHA-1, bland annat `gopher2600.go`, `debugger/commands.go` och `debugger/terminal/plainterm/plainterm.go`; bara `headless/headless.go` var byteidentisk i detta fyra-filers stickprov. **Tidigare source-review på andra commit får inte utan vidare återanvändas som versionsbevis.**

## 2. Vad som FAKTISKT kan visas i koden för installerad v0.57.2

Detta är **källobservationer**, inte emulatortest.

| Påstående om `2af86eb...` | Direkta källor | Källbaserad konsekvens |
|---|---|---|
| Kommandot `HEADLESS` finns och väljs explicit | [gopher2600.go L239–275](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/gopher2600.go#L239-L275) | Kan vara kandidat för separat, senare headless ROM-försök |
| `headless()` kopplar debuggern till `PlainTerminal`, tar valfri ROM-sökväg, anropar `StartInDebugMode` och anger `pipe debugger commands to stdin` | [gopher2600.go L289–315](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/gopher2600.go#L289-L315) | Fil-/pipe-baserad transport finns i koden; **verifierat kommando-ACK framgår inte** |
| `PlainTerminal` öppnar `os.Stdin` och `os.Stdout`, läser med en **255-byte-buffer**, skriver inte terminalprompt i icke-TTY-läge och undertrycker input-echo | [plainterm.go L34–49](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/terminal/plainterm/plainterm.go#L34-L49), [L65–128](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/terminal/plainterm/plainterm.go#L65-L128) | **Hög risk:** en framgångsrik skrivning till stdin är *inte* kvitto på att debuggern konsumerat rätt kommando. Godtycklig pip-/batch-sträng måste inte motsvara ett `TermRead`-anrop/ett bekräftat resultat |
| `CPU`, `TV`, `TIA`, `LAST`, `STEP`, `RUN`, `BREAK` och `SCRIPT` har konkreta kommandogrenar | [debugger/commands.go L205–350](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/commands.go#L205-L350), [L945–1060](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/commands.go#L945-L1060), [L1267–1318](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/commands.go#L1267-L1318) | Källan stöder en **hypotes** om avläsning av CPU/TV/TIA/last-instruktion, men utskriftsfältens synkronisering och `same stop` är **ännu obevisade** |
| Icke-interaktivt `SCRIPT`/batch-läge kan underkänna kommandon med `batchUnsafeCommands` | [debugger/commands.go L113–133](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/commands.go#L113-L133), [L350–385](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/debugger/commands.go#L350-L385) | **Anta INTE** att `RUN` i `SCRIPT` är tillåtet eller har samma semantik som interaktiv stdin |
| HEADLESS har källkod för bildrendering/screenshot, inklusive pixelbuffert och framesignal | [headless/headless.go](https://github.com/JetSetIlly/Gopher2600/blob/2af86eb725739adbf3d9d45cea2ed69eea57da2a/headless/headless.go) | Möjlig framtida `GOPHER_OBSERVED` pixelväg; **inget screenshot-/TIA-bevis finns ännu** |

### Ännu olösta risker

1. **Kommandokvittens:** Inget synkront, entydigt protokoll för `command sent → command parsed → observed machine state` har demonstrerats för den installerade Gopher-versionen. Källan garanterar inte en echo-prompt i pip-läge, och ett externt loggskript som säger `sent` bevisar inget om debuggerns konsumtion.
2. **Stoppidentitet:** Även om `CPU`, `TV` och `TIA` kan anropas måste bank, PC, frame, scanline och CPU-cycle bevisligen vara från **samma pausade debugger-entry epoch**. Avläsningar från olika tillstånd, återspelad gammal output eller endast frontend-screenshot är otillräckliga.
3. **Batch/script:** `batchUnsafeCommands` och terminalläsningens 255-byte-buffer med en `Read` innebär att snabba kommando-burstar och felaktig newline-framing måste betraktas som risker. Använd inga antaganden om exakt en kommandorad per OS-läsning utan empiriskt kvitto.
4. **Versions-/fysikskillnader:** Gopher2600 `v0.57.2` och historiska Stella `6.7.1` är två olika emulatorkärnor. Kommandon/status, intern TIA START/latch/color-clock och pixeloutput måste separeras. `GOPHER_OBSERVED` får aldrig omklassificeras till `STELLA_OBSERVED`, `G5_FORMAL_PASS` eller VERIFICATION II.
5. **Proveniens:** Fryst original F9/F6-NTSC ROM, SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, måste kopieras från dess auktoritativa original och hashkontrolleras både före och efter eventuell framtida mätning. Ingen ny ROM behövs för F9-only. G5AR:s framtida verktygs-PASS är **inte** bevis på F9-funktion.

## 3. Rekommenderad FÖRSLAGEN framtida beslutskedja (INGEN ORDER)

**Först:** Slutför, om originalutskriften finns, endast [Issue #19 G5AR ENV-01](https://github.com/Odourman/let-me-out/issues/19) genom att arkivera den *redan genomförda* ny-task-inventeringens kommando, individuella 8/8 hashvärden, PATH/exitkod och ev. publiceringsrevision. Om underlaget är förlorat: skriv `NOT_AVAILABLE_TO_MAIN` och låtsas inte att det är fullständigt rågranskat.

**Om användaren sedan ger NY uttrycklig auktorisation:** MAIN kan skriva en **egen bindande, liten F9/RESP1-only Gopher2600 v0.57.2 HEADLESS-pilot**, exempelvis följande föreslagna krav:

- Exakt fryst Gopher-binär SHA och källrevision `2af86eb...` samt F9 SHA, originalkällor, separat isolerad specialistbranch och rålogg ska förregistreras.
- `G0` (source-only, **ingen emulator/ROM**) måste finna konduktivt och falsifierbart terminalprotokoll, fel-/timeoutstopp, samt acceptans som **inte** bygger på `stdin write succeeded`, temporära katalogfiler eller antagen prompt.
- Endast om G0 PASS **och** explicit pilotorder tillåter det: en *förhandstilldelad liten, absolut* run-kvot, med **noll ny ROM-byggen**, befintlig F9 oförändrad, hård timeout och STOPP vid första ovidimerade receipt, nytt entry eller inkonsekvent state. Exakt kvot och A/B-acceptans måste fastställas i den separata ordern, aldrig här.
- Kräv för varje observerat stopp: entydigt nytt debugger-entry, faktiska in-/utkommandon, status/kvittens, bank + PC + frame + scanline + CPU-cycle från samma epoch, transkript och alla negativa testutfall, original SHA före/efter. Vid osäker same-stop-kedja **`NOT_DETERMINABLE` eller FAIL**, inte PASS.
- Förklara explicit att en fungerande Gopher-transport bara är en **instrumenteringsmöjlighet**, inte bevis på TIA-kalibrering, intern START/latch, pixel-CC eller sammansatt femfienderspel.
- Skicka råbevis till MAIN; oberoende VERIFICATION II förblir separat framtida beslut. Ingen automatisk progression till C0/G6/S05/5 NPC eller PR-merge.

**MAIN VIII:s nästa rekommendation:** varken fler offline-parserupprepningar (G5AP är redan 98/98 inom scope) eller nya Stella-Actions-runs med samma problem. **Fysisk transport/proveniens är den första osäkra länken.** Gopher v0.57.2 HEADLESS är en rimlig *framtida* isolerad hypotes att pröva, men dess `PlainTerminal` har redan på källnivå konkreta semantiska risker. Ett misslyckat G0 ska stoppa piloten innan ny emulatorkörning och förhindra ytterligare felmärkta PASS.

## 4. Status och rollgräns

**INGET i detta dokument auktoriserar ROM DEVELOPMENT IV att starta ny task, använda F9 ROM, köra Gopher, Stella, DASM, debugger, GitHub Actions, C0, G6, S05, femfiendersimplementation eller PR-merge.** Ingen `AGENTS.md` eller annan permanent agentregel aktiveras. Research är rådgivande, MAIN förbereder beslut, ROM DEVELOPMENT implementerar bara formellt beställt scope och VERIFICATION II granskar separat.

**Slutklass:** `SOURCE_ONLY_DECISION_BRIEF` / `G5_FORMAL_OPEN` / `NO_NEW_TECHNICAL_RUN_AUTHORIZED`.
