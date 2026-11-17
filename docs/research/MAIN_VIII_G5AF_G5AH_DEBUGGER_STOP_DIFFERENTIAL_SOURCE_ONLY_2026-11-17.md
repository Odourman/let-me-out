# LET ME OUT! – MAIN VIII: G5AF ↔ G5AH, källbaserad analys av debuggerstopp

**Datum:** 2026-11-17. **Klass:** `SOURCE_ONLY_METHOD_DIAGNOSIS`, inte ny arbetsorder, ROM, emulator-/Actions-mätning eller oberoende Verification II.

## Status och original

[Aktuellt auktoritetsindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [MAIN VIII G5AI NO_BUILD-receipt](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AI_MAIN_VIII_G5AH_LM_D23_C0_NO_BUILD_SOURCE_RECEIPT_2026-11-17.md), [fryst G5AF-script](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/run_f9_instrument.sh), [fryst G5AH-script](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/preflight_f9.sh), [G5AH-rå-CSV](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/G5AH_C0_EVIDENCE.csv) och [officiell Drive-status](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit). Project Sources V5 i ChatGPT/V6 på GitHub används bara som navigering; ingen ändring eller manuell ersättning krävs.

**Oförändrat utfall:** G5AF `INSTRUMENTATION_READY_BOUNDED` på fryst F9; G5AH `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` efter EN verklig Actions-run; Issue #15 CLOSED. Ingen C0-ROM, inga X40/X104-mätvärden, G5 FORMAL OPEN.

## Versionsbunden källgranskning: Stella exakt 6.7.1

1. [DebuggerParser.cxx `executeBreak`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L817-L870) använder **`toggleBreakPoint(addr,bank)`**: `break $f1ee` är **inte idempotent**; samma kommando kan ge `set` eller `cleared`. Med ett enda addressargument väljs bank via `CartDebug::getBank(addr)`; en explicit bankparameter behövs för att undanröja oklarhet. F9:s gamla F6-bank 0 var observerad av G5AF, men G5AH:s val av breakpoint-bank dokumenterades inte som numeriskt runtime-bevis.
2. [DebuggerParser.cxx `executeFrame`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L1335-L1342) avancerar angivet antal frames; [`executeRun`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L1809-L1815) **lämnar debuggerläget**. Den observerade speltiteln i G5AH är förenlig med att återinträdet efter `run` inte hade verifierats. Den bevisar inte varför stoppet uteblev.
3. [M6502.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/M6502.cxx#L259-L281) testar faktisk `PC` och bank för breakpoints, men om `myLogBreaks` är på **loggas** breakpointen i stället för att sätta debuggerstopp. [Samma fil](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/M6502.cxx#L91-L102) läser `dbg.logbreaks` från inställningar; G5AH bevarade inte ett avgörande bevis för det värdet. Detta är en **källstödd möjlig förklaring, inte fastställd orsak**.
4. [Debugger::autoExec](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/Debugger.cxx#L175-L195) och [PromptWidget::loadConfig](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/gui/PromptWidget.cxx#L369-L414) visar att `autoexec.script` körs under promptinitieringen; [DebuggerParser::exec](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L135-L158) exekverar scriptkommandon men arkiverar inte automatiskt utskrifterna för `set`/ `cleared`. G5AH:s `commands_sent.txt` bevisar tangentsekvens, **inte** att korrekt debuggerläge fanns eller att breakpoint registrerades.
5. [executeSaveSes](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L2025-L2054) stödjer uttrycklig sökväg, men endast när kommandot faktiskt körs inifrån en fungerande prompt. Att filen saknades kan inte ensamt förklara varför stopptillståndet inte uppstod.

## Viktigaste faktiska skillnaderna

| Punkt | G5AF: fungerade som instrumentering | G5AH: misslyckades |
|---|---|---|
| Utlösare | `frame #136`; förregistrerad `trapWriteIf` på `RESP1`, cykel- och scanlinevillkor | `frame #136`; `break $f1ee` på **PC före** `STA RESP1` |
| Positivt efter stopp | Två numeriska debuggerstopp / native TIA-bilder dokumenterade efter förlängd initialisering | Bara ROM-spelfönster dokumenterat, inga pre/post-sessions- eller TIA-bilder |
| Fönsterberedskap | Väntade också på första synliga `Stella`-fönster: **inte en universell garanti**, men träffade trap i den lyckade körningen | Samma för svaga kontroll: första synliga `Stella`-fönster accepterades utan krav på `Debugger mode` innan `xdotool` skickade kommandon |
| Felsökningssignal | G5AF:s `trapWriteIf` gick att avläsa i session | G5AH sparade **ingen** `break`-kvittens, explicit bank- eller `dbg.logbreaks`-status före `run` |
| Arkivintegritet | G5AF:s lyckade readback enligt historisk leverans | G5AH:s original-SHA256SUMS fick ett shutdown-eftersläp i `stella_stdout.txt`: separat FAIL, inte belagd orsak till utebliven debugger |

**Källstödd men EJ avgjord felorsaksrangordning:** (A) bristfällig detektion/val av faktiskt debuggerfönster och prompt, (B) PC-breakpointens aktiverings-/bank-/persistensvillkor, (C) `dbg.logbreaks`-inställning; andra orsaker kan finnas. Ingen av dessa är verifierad genom ny runtime. `break` kontra `trapWriteIf` är inte i sig bevis att `break` är felaktig.

## Fördjupad MAIN VIII-källkontroll – bevisbar skillnad mellan standardinställning och G5AH-observation

Stellas [Settings.cxx 6.7.1](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/Settings.cxx#L208-L217) definierar `dbg.logbreaks = false` som **standard**. Samma [Settings.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/Settings.cxx#L694-L702) dokumenterar argumentet **`-dbg.logbreaks <1|0>`** för att uttryckligen sätta beteendet. Därför är hypotesen `LOG_ONLY` **mindre sannolik än de två övriga** om runnern var ny och standardinställningen gällde. Den är däremot inte utesluten, eftersom **det faktiska** G5AH-konfigurationsvärdet saknas. Detta nyanserar punkt 3 ovan; det ändrar inte historiskt verdict.

Den [interaktiva `logBreaks`-funktionen](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L1683-L1691) **växlar** också läge: kör inte kommandot blint för att försöka "stänga av" loggning, eftersom det kan slå *på* loggning i en ny runner. En eventuell framtida strikt metod bör använda explicit, värdesatt `-dbg.logbreaks 0` vid emulatorsstart **och arkivera faktisk konfigurering**, inte påstå att kommandots frånvaro bevisar inställningen.

Ytterligare två semantiska förgrindar är källbevisade:

- [`executeBreak`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L817-L870) returnerar **"set" eller "cleared"** och är bankmedvetet; ett enda inskickat `break`-kommando är *inte* bevis för ett aktivt PC-stopp. Om separat auktoriserad metod skulle användas, måste faktisk `set breakpoint at ... in bank #...`-kvittens läsas ur en redan aktiv prompt **före** ett separat, kontrollerat `run`. Om "cleared", avbryt och registrera det istället för att försöka reparera tyst genom fler kommandon.
- [`executeRun`](https://github.com/stella-emu/stella/blob/6.7.1/src/debugger/DebuggerParser.cxx#L1809-L1816) lämnar debuggerläge, medan [CPU:s breakpointcheck](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/M6502.cxx#L259-L281) endast kan åstadkomma nytt debuggerläge om *PC och bank faktiskt matchar*. I G5AH syntes spelfönstret och ingen interaktiv post-`run`-prompt verifierades. Det är ett **stopptillstånds- eller observationsfel**, inte ett belagt TIA-positionsfel.

**Konkret framtida acceptans utan ROM-/spelutveckling:** få först bevis för fungerande prompt i en helt frusen F9-körning; få därefter exakt bankbunden breakpoint-`set`-kvittens, ställ in `dbg.logbreaks=0` genom dokumenterad programflagga, `run` först efter kvittens, verifiera *återinträde i debugger*, PC/bank och bevarad session innan `step` och `saveSnap`. Avbryt direkt vid utebliven prompt. Slutligen döda och invänta Stella/Xvfb **före** SHA256SUMS och readback-jobb. Detta är **acceptanskriterier för ett möjligt nytt uppdrag**, inte att uppdraget redan exekverats.

## En möjlig framtida metodreparation – EJ BESTÄLLD

Detta är *beslutsunderlag*, inte kod som MAIN beställer:

1. **Frys exakt samma gamla F9-ROM och read-only .lst/.sym; ändra ingen ROM/ASM/bankmapper.** Reproducera, om separat godkänt, ett positivt debuggerstopp med den **redan fungerande `trapWriteIf`-metodens observationer**, inte som bevis för C0 utan som kontroll att GUI kan användas i den nya harnessmiljön.
2. För nästa PC-breakpointkontroll: **ta bort automatisk `run` ur initiala autoexec-scriptet**. Låt debuggerprompten först bli synligt och maskinellt **bekräftat aktiv**; bevara faktiskt debuggerfönster-ID, titel, `print pc`/bank, och **verkligt kommandosvar** på breakpointinställningen (särskilj `set` från `cleared`). Fastställ om `dbg.logbreaks` är på före påstått stopp. Endast då skicka `run`.
3. **Efter `run`: vänta på verifierat återinträde i debuggerläge** och jämför faktisk `PC=$F1EE`, bank, frame, scanline och cykelvärde, annars avbryt med `NO_STOP_OBSERVED` utan att skicka `step/saveSes/saveSnap` till spelfönstret. Stanna och skilj `BREAK_NOT_SET`, `BREAK_SET_NOT_HIT`, `BREAK_HIT_NOT_CAPTURED`, `LOG_ONLY` där faktisk evidens räcker.
4. Om verkligt pre-`STA`-stopp och session finns: prova **enbart en instruktion `step`** till `PC=$F1F0` och få en faktisk post-session och native snapshot i samma spår; källmodellens sista buscykel är **inte** direkt TIA-fasmätning.
5. **Stoppa Stella/Xvfb helt innan original `SHA256SUMS.txt` skrivs och råarkivet stängs.** `stella_stdout.txt` får inte skrivas vidare efter hashning. Readback måste få ett riktigt jobb-PASS eller bevara FAIL.

**Framtida mandat om användaren väljer detta:** en egen, mycket snäv **F9-instrumenteringsmetodreparation**, ingen ny C0-ROM, inga C1–C4/N1/H4, ingen PR-merge eller Verification II. Sätt separat maximalt antal körningar, strikt budget och hård NO_BUILD-grind. Även en tekniskt lyckad metodreparation ger bara **instrumentering redo**, aldrig C0/H4/G5-PASS. Det finns för närvarande **ingen auktoriserad ny Actions-körning**; det förbrukade G5AH/LM-D23 kan inte återstartas med allmänna "fortsätt".

**Rekommendation till MAIN:** begär *endast om det blir relevant* ett uttryckligt användarbeslut om denna smala metodreparation; ta inte ett nytt fullständigt C0-prov innan grundproblemet är isolerat och rättat.
