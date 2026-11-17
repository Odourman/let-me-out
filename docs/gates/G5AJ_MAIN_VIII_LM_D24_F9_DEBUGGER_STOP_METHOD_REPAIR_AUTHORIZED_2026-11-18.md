# LET ME OUT! – G5AJ / LM-D24: F9-only reparation av debuggerstoppets mätkedja

**Datum:** 2026-11-18. **Beslut:** uttryckligt användarbesked i MAIN VIII-chatten efter G5AI:s analys. **Huvudansvar:** MAIN VIII. **Teknisk utförare:** ROM DEVELOPMENT III genom separat specialistöverlämning. **Klass:** `AUTHORIZED_BOUNDED_INSTRUMENTATION_ONLY` – inte ny spelimplementation. **Initialt läge:** `G5AJ_F9_METHOD_REPAIR_AUTHORIZED_NOT_EXECUTED`.

## 1. Exakt användarmandat och varför detta är nytt

MAIN VIII rekommenderade uttryckligen att nästa faktiska tekniska steg ska vara "en separat auktoriserad F9-instrumenteringskontroll med dessa acceptanskriterier", följt av en källgranskad definition: verklig debuggerprompt, sparad bankbunden breakpoint-`set`-kvittens, explicit `dbg.logbreaks=0`, verifierat debuggeråterinträde, stopp före felaktiga `step/saveSes/saveSnap`, SHA först efter avslutad emulatorprocess. Användaren svarade: **"Ok, fortsätt att jobba vidare själv. Om nuvarande steg inte är klart så gör det klart. Annars börja på nästa. Följ dina egna rekommendationer"**. Detta är en särskild hänvisning till ett **klart specificerat nästa tekniskt steg**, vilket MAIN VIII registrerar som ett **nytt** avgränsat användargodkännande, `LM-D24/G5AJ`.

Det gamla `LM-D23/G5AH` avslutades `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` och **återstartas inte**. [Aktuell MAIN-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [G5AI mottagen G5AH-FAIL](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AI_MAIN_VIII_G5AH_LM_D23_C0_NO_BUILD_SOURCE_RECEIPT_2026-11-17.md). Att det nu finns en **ny F9-only-verktygsorder** betyder inte tillstånd att återköra G5AH, skapa C0-ROM eller starta C1–C4/N1/H4/G6.

## 2. Frysta original som måste läsas

- [MAIN VIII:s Stella 6.7.1 G5AF/G5AH source-only differential](https://github.com/Odourman/let-me-out/blob/main/docs/research/MAIN_VIII_G5AF_G5AH_DEBUGGER_STOP_DIFFERENTIAL_SOURCE_ONLY_2026-11-17.md) – **tekniskt underlag**, inte verifiering.
- [Historiskt fungerande G5AF `run_f9_instrument.sh` fryst](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/run_f9_instrument.sh) och [G5AF fryst rå-metod](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/REPRODUCE_AND_RAW_EVIDENCE.md).
- [G5AH misslyckade `preflight_f9.sh` fryst](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/preflight_f9.sh), [negativa rapporten](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/TO_MAIN_G5AH_C0_ONLY.md), [fryst G5AH Actions-run 44193946233](https://github.com/Odourman/let-me-out/actions/runs/44193946233) och dess ursprungliga hash-FAIL.
- [Stella 6.7.1 `executeBreak`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L817-L870) är bankbunden `set/clear`-växling. [`executeRun`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L1809-L1816) lämnar debuggerläge. [M6502 breakpointcheck](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/M6502.cxx#L259-L281) kräver faktisk PC + bank; loggning kan ersätta stopp. [`dbg.logbreaks = false` default och `-dbg.logbreaks <1|0>` som CLI-flagga](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/Settings.cxx#L208-L217). [`PromptWidget::loadConfig` kör `autoExec`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L369-L414).
- [Originalmasker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json). De sex existerande Project Sources V5/V6 är bara navigering, inte teknisk auktoritet; inget nytt versionsbyte.

## 3. ENDA TILLÅTNA TEKNISKA OMFATTNING – verktygsmetod, inte spel

**Tillåten ROM som input:** exakt **befintlig**, fryst 16 384-byte standard-F6 NTSC F9 binär från historiska originalet, SHA-256
`6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`. Existerande `.asm/.lst/.sym` som read-only original; F9:s `$F1EE = 85 11 STA RESP1`, `$F1F0 = 85 1C STA GRP1`; ursprungliga nio M 8×9-maskrader `3C 3C 18 FF 18 24 24 42 42`.

**BARA EN NY TEST-HARNESSFAMILJ**, på isolerad ROM DEVELOPMENT III-branch utan merge, som får ändra nya **testscript/workflow/audit/evidensfiler** i G5AJ-katalogen. Ingen emulatorpatch, ingen historisk originalredigering, ingen ny `.asm/.bin`, inget DASM-bygge, ingen C0 ROM, ingen ingrepp i produktion, inga nya spelregler.

Följ pre-registrerad sekvens med verklig Stella **6.7.1** och read-only F9:

**Kontroll A – positiv metodreferens:** Reproducera **ett** tidigare bevisat `trapWriteIf`-stopp från G5AF på `RESP1` med fryst F9 och samma relevanta frame/scanline/cykelvillkor. Först när ett verkligt debuggerstopp med verifierad prompt, `PC/frame/scan/cycle/bank`, native TIA-snapshot och session har dokumenterats får nästa kontroll göras. Om detta misslyckas: **STOPP** med `G5AJ_F9_TRAP_CONTROL_FAIL`, identifiera felkälla om möjligt. Att C0 eller H4 fungerar får inte extrapoleras.

**Kontroll B – PC-breakpoint i två separata faser:** Initiera emulatorn i debuggerläge, **utan** `run` i autoexec före att GUI och prompt är verifierat aktiva. Spara fönster-ID, titel, processstatus, `PC` och bank. Ange `-dbg.logbreaks 0` explicit vid start och arkivera argument/versionsinformation; använd INTE det interaktiva `logBreaks` som blind avstängning eftersom det är en toggle. Välj exakt förregistrerad `$F1EE` och korrekt bank, skicka **ett** explicit bankbundet `break` endast från bevisat aktiv prompt. Spara och granska faktisk *`set breakpoint`*-kvittens – `cleared`, fel bank eller saknad kvittens = STOPP, inte tyst retry. Ange/styr frame på samma verifierbara sätt som fryst referens. **Först därefter `run`.** Bekräfta och arkivera faktiskt debugger-återinträde, `PC=$F1EE`, bank/scan/cycle/frame. Sätt aldrig `commands_sent.txt` eller en vanlig spelbild som bevis för exekverade kommandon.

**Kontroll C – en instruktion, BARA om B är positiv:** Spara verkliga före-stopp-sessions- och native TIA-filer. Kör exakt ett `step`, förvänta `PC=$F1F0` och 3 CPU-cykler, arkivera full post-session, native 320×228 TIA-bild och motsvarande frame/scan/bank från samma frysta SHA. Källhärledda "STA sista write clock" är **INTE** verklig busstid och får bara märkas `SOURCE_INFERRED`. Hela kontrollen är endast om F9:s **`RESP1`-surrogat**, aldrig en mätning av C0:s `RESP0`.

**Arkivkontroll D:** Stäng och **vänta in** Stella/Xvfb, säkerställ färdigskrivna `stella_stdout` och samtliga sessioner, **sedan** skapa original `SHA256SUMS.txt`, skapa rå Actions-arkiv och genomför separat oberoende fil-readback i samma Actions-run. Fail-closed vid avvikelse. G5AH:s ursprungliga hash-FAIL bevaras historiskt, får inte skrivas om till PASS. Arkivera rå commandsekvens, command-response, widget/session-TIA, pre/postvärden, ROM source/list/sym/hash, G5AJ-versionsmetadata, fönstertitlar, exitstatus, full logg och SHA-manifest.

## 3B. MAIN VIII:s efterföljande granskning av faktiska Actions-loggar (2026-11-18, INGEN ny mätning)

**Ny konkret råevidensgranskning av redan avslutade körningar:**

- [G5AF lyckad Actions-run 44178247577 / capture-job 134375317996](https://github.com/Odourman/let-me-out/actions/runs/44178247577/job/134375317996): första G5AF-kontrollen rapporterar `G5AF_STELLA_GUI_VISIBLE_AFTER_POLL ... poll=8` med fönstertitel **`Stella 6.7.1: Debugger mode`**; den andra rapporterar `poll=2`, också **`Debugger mode`**. Ursprunglig råaudit: F9 M `PC=61936 ($F1F0), frame=136, scan=123, _sCycles=21, bank=0`; F9 F `PC=61944 ($F1F8), frame=136, scan=123, _sCycles=32, bank=0`. Verkliga sessionsfiler och native `320×228` TIA PNGs finns i detta äldre G5AF-evidenspaket. [G5AF readback-job 134376162352](https://github.com/Odourman/let-me-out/actions/runs/44178247577/job/134376162352) rapporterar **PASS**. F9-stoppens PC är **efter RESP1-skrivning**, inte den före-stoppade `$F1EE` som den nya B-kontrollen avser.
- [G5AH misslyckad Actions-run 44193946233 / capture-job 134430286409](https://github.com/Odourman/let-me-out/actions/runs/44193946233/job/134430286409): `G5AH_GUI_POLL=3`, men sparad fönstertitel var **vanlig spel-ROM-titel**, inte `Debugger mode`. F9 original- och mask-check = **SOURCE PASS**, men inga debugger-sessionsfiler, verkliga före-/eftervärden eller native TIA-PNG. [G5AH readback-job 134430694476](https://github.com/Odourman/let-me-out/actions/runs/44193946233/job/134430694476) **FAIL**, inklusive den bevarade ursprungliga `stella_stdout.txt`-hashavvikelsen.

**Skärpt handskakningsregel som följer av loggarna och nu gäller inom redan godkänd G5AJ:**

1. Vänta inte bara på första fönster som heter "Stella"; det fönstret kan vara **spelvyn** som G5AH råkade skriva till. Pollningsantalet **8 kontra 3 är inte ett tidströskelkrav** (G5AF:s andra PASS hade poll 2). Kräv istället **den semantiska titeln `Stella 6.7.1: Debugger mode` och bekräftad riktig prompt**; arkivera hela sekvensen av fönster-ID, titel och tid/poll. Verifiera med faktisk response/session innan testet passerar promptgrinden. Sänd ALDRIG `print`, `break`, `step`, `saveSes` eller `saveSnap` till vanlig spelskärm.
2. För kontroll A räcker **en** verifierad förregistrerad `trapWriteIf RESP1`-händelse med relevanta `frame=136, scan=123, _sCycles=21, bank=0` och sparad native-TIA+session. Använd G5AF:s bekräftade värden som referens, men rapportera **enbart nytt observerade värden som nytt utfall**. Återanvändning av gamla PASS-filer räknas inte som en ny körning.
3. Kontroll B kräver påvisad **aktiv** prompt före explicit bankbunden `break`, verkligen sparad `set`-kvittens, och därefter `run` och **ny** validerad debuggerprompt/PC. Det faktum att `break` är en set/clear-toggle betyder att en utsänd sträng inte är ett kvitto. G5AF:s `PC=$F1F0` efter registertrap får **inte** felaktigt behandlas som en före-`STA`-PC vid `$F1EE`.
4. Om riktig prompt saknas: klassificera `GUI_GAME_VIEW_ONLY_OR_NO_DEBUGGER_PROMPT`; om prompt finns men kodbreakpoint inte bevisligen sätts: `BREAK_NOT_PROVEN_SET`; om `set` finns men återinträde inte sker: `BREAK_SET_BUT_STOP_NOT_OBSERVED`. Alla är hårda stopp, inga extra retry-runs utanför två tillåtna.
5. Skillnaden i fönstertitel är **starkt observationsbevis för en felaktig GUI-/prompt-grind**, **inte** en bevisad grundorsak till att kodbreakpointen uteblev. Inga C0- eller TIA-resultat får härledas ur denna loggjämförelse.

Detta är en **precision av befintlig G5AJ-mätbarhetsgrind**, inte ny auktorisation eller exekvering. Utvecklaren får inte tolka det som en extra tillåten mätkörning, nytt ROM-test eller nytt senare steg.

## 4. Exakta körgränser och STOPP

**Max två (2) nya Actions-mätkörningar TOTALT** för denna enda G5AJ-harnessfamilj (initial och högst en riktad **harness**-korrigering). Båda måste använda exakt samma frysta F9-ROM SHA. Stopp vid saknad prompt, uteblivet `trapWriteIf`, bankmissmatch, `cleared`, ej registrerat återinträde, saknad native TIA-/sessionpar, inkonsistenta värden, eller om hash-readback misslyckas. Ingen tredje körning under LM-D24, inget nytt testfamiljsbyte, inga oregistrerade "fixes" av emulator-/ROM-/spelkod.

**Slutstatus får endast vara:**
- `G5AJ_F9_METHOD_READY_BOUNDED` – positiv kontroll A+B+C+D, begränsat instrumenteringsresultat, aldrig C0/G5-PASS;
- `G5AJ_F9_METHOD_PARTIAL_NOT_DETERMINABLE` – begränsad faktisk evidens men ofullständig kedja; inga C0-siffror;
- `G5AJ_F9_METHOD_BLOCKER` eller `G5AJ_F9_TRAP_CONTROL_FAIL` – teststopp, negativa bevis kvar.

Varje kontroll redovisas separat i CSV med `STELLA_OBSERVED`, `SOURCE_INFERRED`, `NOT_DETERMINABLE` utan att blanda dem. Bevara även ALLA felkörningar inklusive den ursprungliga misslyckade hashkontrollen.

## 5. Avslut, roller och förbjudet fortsättningssteg

ROM DEVELOPMENT III utför **efter att ordern verkligen mottagits av specialistfunktionen**, levererar fryst branch/commit, full rå evidens och hashad reproduktion + `TO_MAIN` samt originalarkiv i officiell Drive-mapp om verktygsåtkomst tillåter. Stanna därefter. MAIN VIII får källgranska mottagningen men inte kalla sin egen granskning oberoende VERIFICATION II.

**EJ tillåtet genom LM-D24:** ny C0-ROM eller tester X40/104, C1–C4/N1, fem fiender, H4/G1/G6/F12, S05/dörr/nyckel, gameplay-/kart-/originalmaskändringar, ny full emulator/hårdvarutestfamilj, oberoende VERIFICATION II, PR-merge. `G5_FORMAL_OPEN`. Ett eventuellt positivt G5AJ-resultat kan leda till **separat** framtida begäran om C0-test, men inget sådant kan påbörjas automatiskt.

**Dokumenteringsprincip:** G5AJ är ett *nytt begränsat* mandat efter användarens specifika begäran att börja nästa rekommenderade steg; övriga äldre spärrar består. GitHub Issue/Google Drive startar inte tekniska specialisten eller Actions automatiskt.
