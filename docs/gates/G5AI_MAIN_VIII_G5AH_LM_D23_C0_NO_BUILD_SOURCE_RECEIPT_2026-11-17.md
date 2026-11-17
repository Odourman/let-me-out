# LET ME OUT! – MAIN VIII G5AI: mottagning av G5AH / LM-D23, NO_BUILD efter hård C0-förgrind

**Datum:** 2026-11-17. **Ansvar:** MAIN VIII. **Klass:** `SOURCE_REVIEW_RECEIPT_ONLY`. **Gällande tekniskt utfall:** `G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER`. **G5:** `G5_FORMAL_OPEN`. **Ingen ny implementation eller Verification II auktoriseras här.**

## 1. Kontrollerade originalkällor

- [G5AH uttryckliga C0-only arbetsorder (LM-D23)](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AH_MAIN_VIII_LM_D23_C0_ONLY_TIA_MEASUREMENT_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md), [Issue #15](https://github.com/Odourman/let-me-out/issues/15), [levande MAIN-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).
- **Specialistens immutabla slutcommit:** [`4e0f692cb782e9587407787d375b77684c43f14d`](https://github.com/Odourman/let-me-out/commit/4e0f692cb782e9587407787d375b77684c43f14d), [`TO_MAIN_G5AH_C0_ONLY.md`](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/TO_MAIN_G5AH_C0_ONLY.md), [rå-CSV](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/G5AH_C0_EVIDENCE.csv), [manifest](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/MANIFEST.txt), [`preflight_f9.sh`](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/preflight_f9.sh), [`audit_phase_a.py`](https://github.com/Odourman/let-me-out/blob/4e0f692cb782e9587407787d375b77684c43f14d/rom/g5ah_c0_only_2026-11-17/audit_phase_a.py).
- [En enda Actions-run 44193946233](https://github.com/Odourman/let-me-out/actions/runs/44193946233), med capture-job **134430286409 FAIL** och separat återläsningsjobb **134430694476 FAIL**. [Arkiv-ID 14378620744](https://github.com/Odourman/let-me-out/actions/runs/44193946233/artifacts/14378620744), 23 368 byte, GitHub Actions-reporterad SHA-256 `e9966c7cbdc17e62484cbc7775f9c8f031dc936c76f37e8c9c3cc4466306453e`.
- [Officiell Google Drive-arkivkopia](https://docs.google.com/document/d/11np9DbDxTMeaz58Z2DNalmPNlpB-_9Jgow_MvvMpC2U/edit), metadata bekräftar parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`. Native Google Docs är en textkopia, inte byteidentisk med rå ZIP eller GitHub-filer. Sex GitHub `CURRENT_V6` Project Sources kontrollerades som vägvisare och är inte teknisk auktoritet eller testresultat.

**GitHub compare:** från fryst bas `63ad3d43bd10e8a4bce644fedc949e0542c8c17a` till slutcommit: **ahead 10 / behind 0**, **exakt nio *tillagda* filer**, noll ändrade eller borttagna originalfiler; ingen merge. Nio filer omfattar en workflowfil plus åtta filer i `rom/g5ah_c0_only_2026-11-17/`. Specialistens manifest listar åtta ursprungliga nya filer och exkluderar sig självt som nionde – inte en brist.

## 2. Observerad och begränsad slutsats

| Kontroll | Resultat enligt fryst specialist-CSV, source och Actions |
|---|---|
| F9 historisk 16 384-byte F6/NTSC och dess original `.asm/.lst/.sym` | `SOURCE_STATIC_PASS`; hashad **gammal** F9; ingen ny C0-build |
| F9 9 TOP-DOWN M-maskrader | Käll-/binärmatchning `3C 3C 18 FF 18 24 24 42 42`; **inte** nio C0-rasterrader uppmätta |
| Planerat F9 pre-/post-`STA RESP1` vid PC `$F1EE` | `NOT_DETERMINABLE`; inga verkliga PC-/cykel-/bank-/scanlinepar från aktiv prompt |
| Interaktiv debuggerprompt | Ej påvisad; `gui_title.txt` var ROM-speltitel i stället för `Debugger mode`, GUI-bevisbild visade spel |
| `pre_step_debugger_session.txt`, `post_step_debugger_session.txt`, native TIA PNG | Saknades; `commands_sent.txt` bevisar inte att kommandon exekverades |
| C0 numeriska `X=40` och `X=104` | `NOT_BUILT_NOT_RUN` / `NOT_DETERMINABLE`; **ingen C0-ROM** |
| CI-integritet | **Readback-jobb FAIL** på historiskt original `SHA256SUMS.txt` för `stella_stdout.txt`; logg visar 16 OK och 1 FAILED; separat efterhands-rehash uppges i specialistens frysta rapport. Giltig original-FAIL **står kvar** |

Den ursprungliga `SHA256SUMS.txt` beräknade tomfilshash `e3b0c442...` för `stella_stdout.txt`; efter X11/shutdown innehöll filen ett meddelande och dess arkivhash var enligt rapporten `de0db306...`. Det är **en separat artefaktintegritetsbrist**, inte den påvisade orsaken till den saknade debuggerprompten och inte ett lyckat CI-readback-PASS. MAIN har inspekterat GitHub-kommentar, Actions-jobb och deras logg, CSV och manifest, **inte** själv kört Stella, läst alla binärbytes från nedladdad ZIP eller gjort oberoende Verification II. Specialistens återberäkning är dennes egenkontroll.

**Mottagning:** `G5AI_MAIN_VIII_G5AH_NO_BUILD_RECEIVED_SOURCE_REVIEWED` endast som korrekt begränsad specialistleverans och dokumenterat STOPP enligt LM-D23; **inte** C0-PASS, H4/G1-PASS eller extern hårdvaru-PASS.

## 3. Ny observation vid MAIN:s källjämförelse – specificera osäkerheten

Historiskt fungerande [G5AF `run_f9_instrument.sh`](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/run_f9_instrument.sh) startade `trapWriteIf {_scan == #123 && _sCycles ...} RESP1`, sedan `run`, och sparade numeriska sessionsfiler först **efter** GUI-initialisering och trap-stopp. G5AH:s nya `preflight_f9.sh` använde i stället `frame #136; break $f1ee; run` och väntade på ett **synligt fönster vars titel innehöll Stella**, inte specifikt på verifierad aktiv `Debugger mode`-prompt. Därefter sändes `xdotool`-kommandon till det funna fönstret. Ett synligt Stella-spelfönster är **inte bevis** för att källbreakpointen träffades.

Detta är en **konkret brist i hård förgrinds/GUI-beredskapsbeviset** och en skillnad i stoppsätt från G5AF. Det räcker **inte** för att fastställa varför `break $f1ee` inte nåddes eller för att kategoriskt döma ut Stellas debugger, emulatorns `RESP1`-funktion eller C0 på P0. CPU-källrad `STA RESP1` på F9 var endast en *surrogatkontroll* av instrumentering; ingen `STA RESP0`-latens mättes. Ingen källhypotes upphöjs till runtime-PASS.

## 4. Projektstatus och nästa beslutsgräns

- `G5Z_G0_INCONCLUSIVE_NO_ROM` historiskt; `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER` historiskt; `G5AF_INSTRUMENTATION_READY_BOUNDED` historiskt fryst. **Nytt** `G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER`. `G5_FORMAL_OPEN`.
- **LM-D23/G5AH är avslutat vid sin hårda grind.** Den andra outnyttjade Actions-mätmarginalen kan **inte** exekveras efter slutrapport utan nytt uttryckligt godkännande. Issue #15 stängs som **fullföljt avgränsat förgrindsuppdrag med negativt testresultat**. Stängning får inte märkas C0-lyckad.
- **Ny rekommendation, INTE auktoriserad:** först källbaserad jämförelse av exakt den fungerande G5AF-`trapWriteIf`-GUI-tillståndskedjan med G5AH:s `break`-val, och föreslå en enda separat hårt avgränsad **instrumenteringsmetodreparation**, inte en ny full C0/H4/fem-NPC-ROM-familj. En eventuell sådan åtgärd kräver nytt direkt uttryckligt användarbeslut, ny tydlig mätbarhetsgrind, separat run-tak och oförändrat bevarade negativa historiska utfall.
- Ingen C1–C4/N1, H4/G1, G6/F12, S05, fem-NPC, spelregler, oberoende Verification II eller PR-merge tillåts genom detta receipt. **Inget byte av Project Sources** begärs. Redan uppladdade Project Sources kan vara navigering; levande GitHub/Drive-original avgör.

**MAIN VIII:s ansvar:** status och receipt dokumenteras här, utan att agera ROM DEVELOPMENT III eller påstå att ett nytt specialistuppdrag är påbörjat.
