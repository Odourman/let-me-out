# LET ME OUT! – G5AL / LM-D25: ny separat F9-only instrumenteringsmetod med stabil debugger och bankneutral referens

**Datum:** 2026-11-18. **Beslutskälla:** Användarens direkta svar "Ok, Följ din rekommendation" på MAIN VIII:s uttryckliga rekommendation efter [slutförd source-only G5AJ-analys](https://github.com/Odourman/let-me-out/blob/main/docs/research/MAIN_VIII_G5AJ_F6_BANK_AND_DEBUGGER_LIFECYCLE_SOURCE_ONLY_2026-11-18.md): lås inte bankval via `dump` i debugger, verifiera verklig prompt innan `run`, kontrollera faktiska bankvärden och överväg ett **förhandsregistrerat bankneutralt F9-test**. Detta dokument är den **nya, specifika avgränsade användarauktorisationen**, inte en fortsättning av förbrukat LM-D24.

**Beslut:** `G5AL_F9_METHOD_ONLY_AUTHORIZED_NOT_EXECUTED`. **MAIN VIII** avgränsar och tar emot, **ROM DEVELOPMENT III** är ensam teknisk utförare efter faktisk specialistöverlämning. Detta är **inte** oberoende VERIFICATION II och inte C0-/spelimplementation.

## 1. Läges- och negativhistorik som aldrig får skrivas över

- [Bindande status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) och [G5AK mottagen G5AJ FAIL](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AK_MAIN_VIII_G5AJ_LM_D24_F9_TRAP_CONTROL_FAIL_RECEIPT_2026-11-18.md).
- [G5AJ fryst specialistcommit `b0cda0c55b05fa8ceb9763731363fbaada822f0b`](https://github.com/Odourman/let-me-out/blob/b0cda0c55b05fa8ceb9763731363fbaada822f0b/rom/g5aj_f9_method_2026-11-18/TO_MAIN_G5AJ_F9_METHOD.md) och [Issue #16 STÄNGD VID FAIL](https://github.com/Odourman/let-me-out/issues/16). [G5AJ run1](https://github.com/Odourman/let-me-out/actions/runs/44198377885) gav verklig `PC=$F1F0, frame136, scan123, _sCycles21, bank3` och originalbild men **A STRICT FAIL** eftersom gamla kravet var bank0. [G5AJ run2](https://github.com/Odourman/let-me-out/actions/runs/44199817228) förlorade debuggerprompten. B/C aldrig körda. LM-D24:s **2/2** körningar är **slutgiltigt förbrukade**; dess `FAIL` omklassas aldrig.
- Historisk [G5AF lyckad fryst F9-referens](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/run_f9_instrument.sh) har M `PC=$F1F0`, frame136, scan123, `_sCycles=21`, bank0; F `PC=$F1F8`, `_sCycles=32`. G5AF mäter bara F9 `RESP1`-surrogat. G5AH `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` med historiskt arkiv-hashfel; G5AD och G5Z negativa utfall kvar.
- [MAIN VIII källkontroll av Stella 6.7.1](https://github.com/Odourman/let-me-out/blob/main/docs/research/MAIN_VIII_G5AJ_F6_BANK_AND_DEBUGGER_LIFECYCLE_SOURCE_ONLY_2026-11-18.md): debuggern `lockHotspots`, så `dump $fff6 $fff6` i pausad debugger **är inte en giltig bank0-fixture**; `frame` låser upp bara under frammatning. `PromptWidget::loadConfig` kör autoexec under första promptvisning och `run` kan byta till spelläge, så en passerande fönstertitel är inte bevis på senare trap. Inget nytt tekniskt påstående har runtime-testats sedan G5AJ.

## 2. Exakt material och tillåtna kodförändringar

**Oföränderligt input:** Exakt befintlig 16 384-byte **F6/NTSC F9-ROM** SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, frysta original `.asm/.lst/.sym`, nio M-maskrader `3C 3C 18 FF 18 24 24 42 42`. Alla **fyra 4KiB-bankbilder är byteidentiska** i detta F9-original. `$F1EE: 85 11 = STA RESP1`; `$F1F0: 85 1C = STA GRP1`. Ingenting i den ursprungliga binären eller dess originalkällor får ändras, och inget nytt `.asm/.bin`/DASM-bygge får göras.

**Enda tillåtna nya tekniska familj:** `G5AL_F9_STABLE_PROMPT_BANK_NEUTRAL`, en isolerad ROM DEVELOPMENT III-branch, endast *nya* pre-registration, testscript, CI-workflow, parser/audit, råevidens/manifest/TO_MAIN. Inga ändringar av gamla G5AF/G5AH/G5AJ-filer, inga emulatorpatchar, inga gameplay-, sprite-, mask- eller speldesignändringar, ingen PR-merge.

**Hård högsta gräns:** **två (2) nya Actions-mätkörningar totalt under LM-D25**, initial + högst en **förhandsdokumenterad riktad harness-korrigering**. Readback-jobb i samma run räknas inte som ny emulatorkörning. **Ingen tredje körning** utan separat nytt användarbeslut. Begränsa till **en** F9 M/RESP1-positiv referens och sedan pre-STA-kontroll, inte fler testfamiljer eller C0.

## 3. NYA förregistrerade acceptanskriterier – A, B, C, D

### A: Stabil initial debugger, bankneutral F9-RESP1-referens

A1. Starta Stella **6.7.1** med `-debug`, `-dbg.logbreaks 0`, `-bs F6`, NTSC och fullständigt sparad effektiv CLI/versions-/settingsinformation (inklusive `dev.settings`, `dev.bankrandom`, `plr.bankrandom`, och `-startbank` om valt). Separera ren testinstans och configs; inga osedda sparade ROM-specifika autokommandon/breakpoints ska tillåtas. Autoexec för A:s **initiala öppning får ENBART innehålla `base #10`**. **Inget `frame`, `dump`, `trapWriteIf` eller `run` i initial autoexec.**
A2. Kontrollera aktivt Stella-fönster, process, exakta titeln `Stella 6.7.1: Debugger mode`, och *faktiskt fungerande* `print pc`, `print _bank` och `saveSes` med svar som går att parsa. Arkivera **ny session** före nästa steg. Spara window-ID/titel/tidsstämplar. Fönstertitel i sig är **inte** PASS.
A3. Skicka **separat interaktivt** `frame #136` från fungerande prompt, verifiera återkomst till verkligt debuggerläge och faktisk `_fCount`, `_bank`, `pc`; logga faktisk bank. **ALDRIG** `dump $fff6 $fff6` som bankfix. Därefter konfigurera **en enda förregistrerad** `trapWriteIf {_scan == #123 && _sCycles > #19 && _sCycles < #23} RESP1` med bevisbar parserkvittens innan **ett** `run`. Om `frame`-frammatning eller kommandot redan har lämnat debuggerläge: STOPP.
A4. Efter `run`: skilj initial prompt från verkligt **nytt** trap-återinträde. Kräv faktiskt nytt avläst `PC=$F1F0`, `_fCount=136`, `_scan=123`, `_sCycles=21`, `_bank` inom **0,1,2,3**, `RESP1`/TIA-registertext, `saveSes`-session och native **320×228** TIA PNG. Arkivera valda fönster, före-/efter-sessions och faktisk ny promptrespons. Kontrollera source/ROM/LST/SYM/mask+hash igen. **Ny förregistrerad bankneutral regel:** eftersom alla F9-bankbytes är identiska accepteras vilken faktiskt uppmätt bank 0–3 som helst **endast inom denna nya F9-kontroll**. Det är **inte** en retroaktiv godkännandeförklaring av G5AJ run1. Jämför även native TIA med fryst G5AF M-referens; en skillnad kräver explicit redovisning och kan inte döljas av bankneutraliteten. **A strikt FAIL vid saknad verklig återinträdes-/numerisk-/native evidens.**

### B: Bevisad kodbreakpoint före `STA RESP1` – endast efter A PASS

B1. Stäng och `wait` för A:s Stella-instans. Starta en **ny ren F9** Stella 6.7.1 utan alla typer av automatiska `run`/`frame`/breaks i autoexec, endast `base #10`. Samma faktiska ROM SHA, process-/fönster-/prompt-handshake som A1–A2. Interaktivt `frame #136` först efter bevisad prompt; verifiera verklig bank/PC/frame efter frammatning.
B2. Eftersom fyra F9-bankbytes är identiska och `break` är bankbunden/toggle kan metoden förregistrera **fyra separata en-gångs-kommandon** `break $f1ee #0`, `#1`, `#2`, `#3`, men bara i **ny, verifierat tom** breakpointkonfiguration och endast om varje kommando ger exakt riktig `set ... in bank #N`-kvittens. Alternativet är **en** bankbunden breakpoint för uppmätt aktuell bank, men då måste slutlig bank vid träff vara densamma. **Välj och frys en av dessa två strategier FÖRE första Actions-körningen; växla inte taktik i efterhand utan dokumenterad riktad korrigering inom 2-run-gränsen.** `break ... #255` ska inte användas (kvittens kan vara missvisande i Stella 6.7.1:s loop).
B3. **Först efter bevisat `set`:** interaktivt `run`; kräv faktiskt **nytt** debuggeråterinträde med `PC=$F1EE`, uppmätt bank som matchar en bevisat aktiverad bankbunden breakpoint, frame/scan/_sCycles, sparad native TIA och session. Inget annat CPU-stopp, andra fönster eller en bara utsänd `break`-sträng får klassas som PASS.

### C: exakt en CPU-instruktion – endast efter B PASS

Från bevisat `PC=$F1EE` vid körningens faktiska bank: spara *pre* `saveSes`/native, kör **ett** `step`, spara verifierat *post* `saveSes`/native, bekräfta verkligt `PC=$F1F0` och **+3 CPU-cykler** (från emulatorns faktiska `step`-kvittens och cykeldata), dokumentera frame/scan/bank före och efter. En source-härledd `STA`-bustid är **inte** en verkligt uppmätt raw TIA colorclock och får aldrig markeras `STELLA_OBSERVED` utan egen relevant mekanism. Kontrollera att `Debugger::setQuitState` kan exekvera en extra instruktion vid `run` – bevara faktisk före/efter PC, gissa inte.

### D: artifact integrity – efter emulatorns avslut

Efter alla lyckade eller misslyckade delar: avsluta och `wait` för samtliga Stella/Xvfb-processer, färdigställ loggar, **sedan** skapa `SHA256SUMS.txt`, upload oförändrat originalarkiv, **separat job i samma Actions-run** kontrollerar samtliga listade originalbytes och arkivmanifest. Bevara **även varje FAIL, rått command-response, frånvaro av sessioner, fönstertitlar, exakta exitstatus**, original ROM SHA, source/lst/sym/mask, syntax/versionsinfo och klassning per kontroll: `STELLA_OBSERVED`, `SOURCE_INFERRED`, `NOT_DETERMINABLE`. HASH-PASS får aldrig omklassas till emulator-/metod-PASS.

## 4. STOPP, slutstatus och nästa grind

**STOPP omedelbart** vid avvikande ROM SHA, saknad bevisad prompt, otillförlitlig statusövergång, annan PC/frame/scan/cykel än förregistrerat för A, utebliven genuin ny trap, saknad korrekt `set`-kvittens, bank utanför 0–3, oförklarad avvikelse i native TIA-referens, uteblivet B-återinträde, felaktig step eller bruten hashreadback. **B får aldrig köras om A inte har nått strikt PASS. C får aldrig köras om B inte nått strikt PASS.** Om testerna stannar: klassificera saknad information `NOT_RUN/NOT_DETERMINABLE`, inte "pass".

Endast utfallen `G5AL_F9_METHOD_READY_BOUNDED` (samtliga A–D pass enligt ny förregistrering), `G5AL_F9_METHOD_PARTIAL_NOT_DETERMINABLE`, `G5AL_F9_TRAP_CONTROL_FAIL`, eller `G5AL_F9_ARCHIVE_INTEGRITY_FAIL`. Ingen ny C0-ROM eller X40/X104; B/C-PASS gäller bara **fryst F9 RESP1-surrogat**, aldrig C0/RESP0, M0/NUSIZ/GRP, TIA-physical colorclock eller G5 formell PASS.

När ROM DEVELOPMENT III har gjort **högst två körningar**, fryser utföraren specialistbranch/commit/TO_MAIN/CSV/MANIFEST, länkar råa originalarkiv och originala Drive-kopior om tillgängligt, samt stoppar för MAIN VIII:s källmottagning. MAIN får inte ersätta oberoende VERIFICATION II.

**Förbjudet scope:** all ny `.asm/.bin` och DASM-build, C0–C4/N1, H4/G1/G6/F12, S05, femfienders-spelmotorn, spelcanon, grafiska tillgångar, emulatorpatch, PR-merge, oberoende Verification II, tredje Actions-körning och automatisk start av senare testfamilj/implementation. G5 förblir `G5_FORMAL_OPEN` även vid framtida F9-metod-PASS.

**Project Sources:** statiska V5/V6 får fortsätta vara navigeringshjälp; ingen ny V7/migration eller manuell ersättning behövs.
