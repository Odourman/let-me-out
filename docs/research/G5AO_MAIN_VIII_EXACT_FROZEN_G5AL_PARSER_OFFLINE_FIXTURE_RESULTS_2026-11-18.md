# LET ME OUT! – MAIN VIII G5AO: reproducerade offline-fixtures mot exakt fryst G5AL-granskare

**Datum:** 2026-11-18. **Uppdragsmandat:** användarens "Låter bra, gör så" efter MAIN VIII:s [G5AN source-only granskning](https://github.com/Odourman/let-me-out/blob/main/docs/research/MAIN_VIII_G5AN_G5AL_POST_RUN_PROMPT_SAVESES_TRANSPORT_SOURCE_ONLY_2026-11-18.md), specifikt **offlinetester med syntetiska data och metod-/protokollspecifikation**. **Status: `G5AO_OFFLINE_FIXTURES_EXECUTED_18_OF_18_EXPECTATIONS`.** Detta är **inte** G5AL PASS, inte ny LM-D26-implementation, inte ROM DEVELOPMENT:s tekniska implementation och **inte oberoende VERIFICATION II**.

## Bevisad källa och metod

- Original fryst specialistcommit [`f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431`](https://github.com/Odourman/let-me-out/commit/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431), fil [`rom/g5al_f9_method_2026-11-18/audit_g5al.py`](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/audit_g5al.py).
- MAIN hämtade originaltext direkt via ansluten GitHub-koppling och återskapade den för **lokalt offline-bruk**. **Byteverifiering mot GitHub-original:** exakt **8426 byte**, Git-blob SHA-1 **`f159c1f8668c1f504fd9538a8d1ef17b2ddefafa`**, kontrollerad i lokal Python från `SHA1("blob 8426\\0" + exakt filinnehåll)`. **Samma blobhash som GitHub returnerade.** Det är samma fysiska parserkod som historisk G5AL, inte en omskriven tolkning.
- Den frysta Pythonfilen kördes via `subprocess.run([python, exact_parser, "--gate", stage, synthetic_session])` mot **syntetisk Stella-liknande text, ingen emulator**. Dess samlade finalaudit kördes i separat syntetisk katalog med författarfilnamn **`<STAGE>_debugger_session.txt`**, A-förutsättningsmarkör, fiktiv `OK`-SHA-fil och helt syntetisk gemensam 320×228 RGB-testbild. **Den fejkade SHA-/bildinformationen representerar INTE fysisk ROM eller verklig TIA.**
- En **separat lokal hypotetisk kontrafaktisk testkopia** gjordes med *endast* två statiska modifieringar: `stage.endswith("HANDSHAKE")` → `stage in ("A_HANDSHAKE", "B_HANDSHAKE")`; `p=parent/(n+"_session.txt")` → `p=parent/(n+"_debugger_session.txt")`. **Originalfil och specialistbranch ändrades inte.** Kopian avser ett *källmässigt experiment* i testmiljön, inte en granskat produktionsklar bugfix.

## Exakta offlinetestresultat

**Resultat: 18 av 18 testassertioner uppfyllde i förväg uttryckta förväntningar.** Det betyder INTE 18 lyckade Stella-kontroller. Några bekräftar just falsk PASS/falsk FAIL i det gamla verktyget.

| Syntetiskt prov | Fryst G5AL-parser, faktisk offline-avläsning | Kontrafaktisk två-radersvariant | Slutsats |
| --- | --- | --- | --- |
| `A_REENTRY_HANDSHAKE`, **fel `PC=$F000`** | **PASS (fel)** | **FAIL (rätt)** | För specialgrinden `PC=$F1F0` var generiskt `endswith("HANDSHAKE")` tidigare prioriterat |
| `B_REENTRY_HANDSHAKE`, **fel `PC=$F000`** | **PASS (fel)** | **FAIL (rätt)** | Kravet `PC=$F1EE` var oåtkomligt |
| A REENTRY, **korrekt `PC=$F1F0`** | PASS | PASS | Positiv kontroll |
| B REENTRY, **korrekt `PC=$F1EE`** | ej separat nödvändig för bugbevis | PASS | Positiv kontroll efter korrigerad dispatch |
| Initial handshake utan `_bank` | FAIL (rätt) | ej separat | Negativ kontroll |
| Sammanfogad `print pcprint _fCount`, utan giltigt PC | FAIL (rätt) | ej separat | Negativ kontroll |
| Fem individuella A-delsessioner (inklusive två PC och scan i syntetisk A-TRAP) | **5/5 positiva `--gate`** | indirekt i finalaudit | Data uppfyller stage-grindarna individuellt |
| A **slutaudit**, samma fem syntetiska sessioner i de filnamn G5AL-runnern faktiskt skriver | **A PASS = false**; alla fem steg visar `MISSING` | **A PASS = true** | Fullgranskaren läser fel namn `*_session.txt` jämfört med runnerns `*_debugger_session.txt` |
| Syntetiskt A-PASS utan B/C | `G5AL_F9_TRAP_CONTROL_FAIL` p.g.a. filnamnsmiss | `G5AL_F9_METHOD_PARTIAL_NOT_DETERMINABLE` | Även efter lokal korrigering förblir B/C **inte bevisade** |

18 enskilda assertions: (1–2) två fel-PC falskt godkända i originalet, (3–5) tre baseline positiv/negativ, (6–10) fem stage-gates, (11–12) slutgranskarens falskt negativa A + alla saknade blobar, (13–16) två fel-PC avvisade och två riktiga PC godkända i kontrafaktisk kopia, (17–18) syntetisk A godkänd men B/C fortfarande ej bedömbara i kontrafaktisk finalaudit. Alla förväntade utfall observerades i lokal Python 2026-11-18.

**Offline-testpaket i samma användarkonversation:** `LET_ME_OUT_G5AO_OFFLINE_FIXTURES_2026-11-18.zip`, SHA256 **`c519555a974199a2c19e07583c179a2af32819af69d2b42ccdb00c4ba1aad633`**, 8959 byte. Innehåller `audit_g5al_original.py` (exakt Git-blob-verifierad), reproducerande `run_g5ao_offline_fixtures.py`, `G5AO_OFFLINE_FIXTURE_RESULTS.json` (full maskinläsbar sammanställning), README. **ZIP är lokalt genererad i konversationen och har INTE i detta steg utgivits som officiellt Drive-/GitHub-originalarkiv.** Det är GitHub-rapporten och frysta originalscripten som ska användas som nuvarande auktoritetskällor tills separat arkivering sker.

## Varför detta inte ändrar historiska bedömningar

- Två källfel **bevisas** offlinemässigt. De innebär att G5AL:s auditverktyg hade både falsk-negativ och falsk-positiv risk.
- G5AL:s verkliga run1 missade fortfarande två separata post-`run`-PC-avläsningar; run2 saknade fortfarande ny giltig `saveSes`-session. **Dessa negativa originalhändelser ändras inte av något syntetiskt PASS**.
- B/C, verkliga bus-writes/colorclock, C0, X40/104, femfienders-implementation är **NOT_RUN/NOT_DETERMINABLE**. `G5AL_F9_TRAP_CONTROL_FAIL` och `G5_FORMAL_OPEN` kvarstår. Ingen ny Stella eller GitHub Actions, ingen ROM, inget PR-merge, ingen Verification II utförd.

**Rekommenderad order för eventuellt senare separat ROM DEVELOPMENT III *offline* bugfix:** gör `--gate` och finalaudit konsekventa, skriv deterministiska testfixtures med fel PC, fel bank, saknade/stale sessions och felaktigt format, säkerställ att ren finalaudit varken false-PASS eller false-FAIL och markera `OFFLINE_SYNTHETIC` separat från `STELLA_OBSERVED`. En sådan specialistreparation beställs **inte automatiskt** av detta G5AO-forskningsresultat.

**Parallell protokollspecifikation:** [G5AO – kommandotransport och tekniskt vägval](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AO_MAIN_VIII_STELLA_DETERMINISTIC_COMMAND_PROTOCOL_DRAFT_2026-11-18.md).
