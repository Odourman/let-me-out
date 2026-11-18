# G5AL / LM-D25 – FÖRHANDSREGISTRERAD RIKTAD KORRIGERING, FÖRE ANDRA SISTA KÖRNINGEN

**Originalkörning #1:** [Actions 44203795042](https://github.com/Odourman/let-me-out/actions/runs/44203795042), capture-job `134464417668` FAIL, originalartifact [14382688726](https://github.com/Odourman/let-me-out/actions/runs/44203795042/artifacts/14382688726), ZIP 35 625 bytes, SHA256 `b2edf5609eefb051885bc5eaa5b7cfb8a20e4b9fdeb3e0c9f8df9f389c8d69f7`, kontrolljobb `134467449687` SUCCESS. Nedladdat original och alla **44/44** ursprungliga manifestposter lokalt efterräknade utan avvikelse. Officiellt Drive-original: https://drive.google.com/file/d/1qwKIqIBlJ67mUP7b034J78KjgEJxQAQn/view .

## Direkt i originalsessionen observerat (inte gissning)

- `A_HANDSHAKE`, `A_FRAME` och `A_TRAP_ACK` passerade med verkliga Stella-kommandosvar; `frame=136`, faktiska banken 0 och `added trap 0`. Nytt debuggerfönster efter `run` registrerades med annat window-ID.
- I den faktiska originalfilen `A_TRAP/A_TRAP_debugger_session.txt` efter `run` står **`> print pcprint _fCount`** följt av Stellas feltext **`too many arguments`**. Därför har endast den senare `print pc` ett korrekt avläst `PC=$F1F0 / #61936`, och den avsiktligt strikta grinden med två faktiska posttrap-PC-svar **FAIL**. Detta är en verkligt observerad command/prompt-race, inte enbart ett regexfel.
- Andra faktiska nya avläsningar vid samma pause: `_scan=123` två gånger, `_sCycles=21`, `_bank=0`; riktig `tia`-text. Native `A_TRAP_native_TIA.png` 320x228 med exakt SHA `078c9c1ce249cb8c9ef6a45dc322647db2e1a869b3f60635c9e27436f38c016a`, samma som G5AF M, **0 avvikande pixlar**.
- **Strikt A=FAIL i försök 1**, eftersom hela PC-kedjan inte bevisades enligt förregistrering. B/C **NOT_RUN**, inte pass. D originalarkiv **PASS 44/44**, inte ett metod-PASS.

## EN RIKTAD KORRIGERING (samma F9, bankneutralitet och grindar)

Korrigera **enbart Stella GUI-prompt-synkronisering vid NYTT återinträde efter `run`**:

1. Efter `find_debugger ... AFTER_RUN`, ge det verifierade debuggerfönstret tid att slutföra `PromptWidget::loadConfig`. Skicka sedan **ett** separat `print pc`, följt av `saveSes`, och avvisa om den nya sessionen inte innehåller ett verkligt avläst PC-värde för förväntat stopp (`$F1F0` i A och `$F1EE` i B), med aktivt verifierat debuggerfönster. Ingen blind omkörning/retry om handskakningen misslyckas.
2. Därefter kör oförändrat `record_cpu` och de strikt registrerade `A_TRAP`/`B_PRE`-grindarna; **ingen försvagning av kravet på två faktiska PC- och scan-avläsningar**. Anteckna ny `A_REENTRY_HANDSHAKE` och `B_REENTRY_HANDSHAKE` i audit/CSV.
3. Ingen ändring av ursprunglig ROM, masker, source/list/sym, A:s bankneutralitet, B:s fyra en-gångs `break $f1ee #N`, C:s enda `step`, D:s fullständiga hash-efter-shutdown eller original G5AJ/G5AH-fel. Inga extra Actions-runs utanför denna **andra och sista** G5AL-körning.

**Detta dokument sparas före andra workflowstarten.** Försök 1:s ursprungliga filbytes, CI-FAIL och lokalt verifierade manifest får aldrig omklassas. Körning 2 utvärderas från sina EGNA nya faktiska sessioner och native TIA och stoppar vid varje avvikelse.
