# LET ME OUT! – ROM DEVELOPMENT III → MAIN VIII
## G5AL / LM-D25 – SLUTRAPPORT: `G5AL_F9_TRAP_CONTROL_FAIL`

**Datum:** 2026-11-18. **Roll:** ROM DEVELOPMENT III, utvecklarens tekniska egenkontroll, **inte oberoende VERIFICATION II**. **Beslutsgrind:** `G5_FORMAL_OPEN`. **Körgräns:** exakt **2 av 2** nya tillåtna GitHub Actions-mätkörningar förbrukade. **HÅRT STOPP** – ingen tredje körning, ingen fortsättning till senare implementation.

**Bindande fullorder:** [G5AL / LM-D25](https://github.com/Odourman/let-me-out/blob/bef65b52556dab99d8eaac4270325704de81dbff/docs/gates/G5AL_MAIN_VIII_LM_D25_F9_STABLE_PROMPT_BANK_NEUTRAL_METHOD_AUTHORIZATION_2026-11-18.md), blob `e6c8ae80e723464b23393551a51eb0ecad602414`. [Issue #17](https://github.com/Odourman/let-me-out/issues/17). [MAIN VIII:s versionsbundna differential](https://github.com/Odourman/let-me-out/blob/bef65b52556dab99d8eaac4270325704de81dbff/docs/research/MAIN_VIII_G5AJ_F6_BANK_AND_DEBUGGER_LIFECYCLE_SOURCE_ONLY_2026-11-18.md) blob `27edbb3c3cb87a48c7b46b09b82033a82c95aba8`. Original huvud-HEAD vid branchskapandet: `bef65b52556dab99d8eaac4270325704de81dbff`.

## 1. Scope, original och pre-registration

**ENDA använd ROM:** historiskt byggd fryst standard-F6/NTSC F9 16 384 bytes, SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`. F9-originalet och `.asm/.lst/.sym` laddades read-only från original Actions run [44050126727](https://github.com/Odourman/let-me-out/actions/runs/44050126727) med artifact `LET_ME_OUT_R1_F9_ONE_ROM_AND_ACTUAL_STELLA_PARTIAL_OR_COMPLETE_G1`. **Inget nytt ROM/ASM/BIN/DASM-bygge eller produktionsändring.** Statiska originalkontroller PASS i båda körningarna: fyra identiska 4096-byte bankbilder, original `$F1EE 85 11 STA RESP1`, `$F1F0 85 1C STA GRP1`, originala nio TOP-DOWN M-maskrader `3C 3C 18 FF 18 24 24 42 42` och oförändrat SHA före/efter processavslut. Original `.lst` SHA `b47924e8bd3b4771b13bde05146f67591a994bcae45e2b8422f41f39dc0107f6`, original `.sym` SHA `bb0941c7278f58605c96a270eedb4a48fe703bf5717d6f5c848e1f62c12a12a7`.

**Förregistrering publicerad före första mätningen:** [PREREGISTERED_F9_METHOD.md](PREREGISTERED_F9_METHOD.md), först commit `3b85d94e0605b1b10a1307d6cf433f2869d65fae`. En enda ny G5AL-harnessfamilj; fryst B-strategi **fyra separata set-once bankbundna `break $f1ee #0`, `#1`, `#2`, `#3`**, aldrig bank-0-`dump`, aldrig `#255`. Nytt A-kriterium bankneutralt 0–3 ENDAST för denna nya G5AL, inte retroaktiv G5AJ.

**Metod:** Stella 6.7.1 med `-debug -dbg.logbreaks 0 -dev.settings 0 -dev.bankrandom 0 -plr.bankrandom 0 -bs F6 -format NTSC`, separata rena HOME/config per A och B. Initialt `autoexec.script` innehåller ENDAST `base #10`. Interaktiv `print pc`/`print _bank` och verklig `saveSes` måste fungera före interaktiv `frame #136`, trap/break, `run`. Efter `run` krävs faktiskt nytt debuggeråterinträde med numeriska kommandosvar, inte bara en titel. Native TIA ska vara original `saveSnap` 320x228, inte GUI-crop. Referens från [G5AF historisk PASS-run 44178247577](https://github.com/Odourman/let-me-out/actions/runs/44178247577). Endast faktisk `RESP1`-F9 surrogat testas; intern bus-writetid/colorclock och `RESP0` är **inte** uppmätta.

## 2. Försök 1 – verkligt stopp, men hårt A-FAIL

- [**GitHub Actions run 44203795042**](https://github.com/Odourman/let-me-out/actions/runs/44203795042), [capture-job 134464417668](https://github.com/Odourman/let-me-out/actions/runs/44203795042/job/134464417668) **FAIL**, [separat readback-job 134467449687](https://github.com/Odourman/let-me-out/actions/runs/44203795042/job/134467449687) **SUCCESS**.
- Initial **A_HANDSHAKE PASS**, session **833 bytes**, verkligt `PC=$F000`, bank **0**. `A_FRAME PASS`, session **1280 bytes**, faktisk frame **136**, `PC=$F063`, bank **0**. `A_TRAP_ACK PASS`, session **1620 bytes**, verklig Stella-kvittens **`added trap 0`**.
- Efter ett interaktivt `run` fick Stella åter debuggerläget med nytt fönster-ID. Rå `A_TRAP_debugger_session.txt` **2893 bytes** visar verklig `PC=$F1F0` (en korrekt posttrap-print), `_fCount=136`, `_scan=123` (två avläsningar), `_sCycles=21`, `_bank=0`, verklig `tia` inklusive `COLUxx/P0/P1/M0`. Native `A_TRAP_native_TIA.png` 320x228 RGB SHA **`078c9c1ce249cb8c9ef6a45dc322647db2e1a869b3f60635c9e27436f38c016a`**. Senare separat lokal pixeljämförelse mot G5AF M gav **0 avvikande pixlar**; nativ PNG SHA identisk med G5AF.
- **Avgörande negativa råbevis:** post-`run` transkriptet innehåller bokstavligen `> print pcprint _fCount` följt av Stellas `too many arguments`. Den tidigare begärda dubbla faktiska `print pc`-responsen vid samma stopp **saknas**. En senare `print pc` är riktig, men detta reparerar inte den föregående kommandokollisionen. **A STRICT FAIL** (inte A-PASS), B och C **NOT_RUN/NOT_DETERMINABLE**. Detta är ett observerat post-run prompt-/inmatningsrace, inte bevis för felaktigt ROM-innehåll.
- [Original GitHub Actions ZIP artifact 14382688726](https://github.com/Odourman/let-me-out/actions/runs/44203795042/artifacts/14382688726), **35 625 bytes**, exakt SHA-256 **`b2edf5609eefb051885bc5eaa5b7cfb8a20e4b9fdeb3e0c9f8df9f389c8d69f7`**, **45 arkivmedlemmar / 44 original SHA256SUMS-poster**. Separat readback-jobb PASS; dessutom lokalt från orört nedladdat ZIP omhashat **44/44 PASS**.
- [Oförändrad original-ZIP på officiella Drive](https://drive.google.com/file/d/1qwKIqIBlJ67mUP7b034J78KjgEJxQAQn/view).

## 3. Förhandsdokumenterad enda riktade ändring och försök 2

**Riktad korrigering registrerad FÖRE andra Actions-start:** [TARGETED_CORRECTION_BEFORE_SECOND_FINAL_RUN.md](TARGETED_CORRECTION_BEFORE_SECOND_FINAL_RUN.md), första källcommit `b3c4c4f999dd815570e0b5578204e931b44c6243`, [Issue #17 förhandskommentar](https://github.com/Odourman/let-me-out/issues/17#issuecomment-6964743654). Efter nytt debuggerfönster efter `run`: ge prompten två sekunder för att slutföra initiering, skicka ett separat `print pc` och kräv en verkligt sparad/parsad `A_REENTRY_HANDSHAKE`-session. Samma krav för B:s senare `run`, om A faktiskt passerat. **Ingen lättnad av kraven på två verkliga PC-avläsningar eller någon ROM/CPU/scan/STA-kondition**. Detta är enda korrigeringsfamiljen.

- [**GitHub Actions run 44204912620**](https://github.com/Odourman/let-me-out/actions/runs/44204912620), [capture-job 134468256971](https://github.com/Odourman/let-me-out/actions/runs/44204912620/job/134468256971) **FAIL**, [separat readback-job 134468721983](https://github.com/Odourman/let-me-out/actions/runs/44204912620/job/134468721983) **SUCCESS**. Detta är **ANDRA OCH SISTA** tillåtna mätkörning.
- Ny faktisk **A_HANDSHAKE PASS**, `PC=$F000`, bank0; ny **A_FRAME PASS**, frame136 och `PC=$F063`, bank0; ny **A_TRAP_ACK PASS** med `added trap 0`. Rå-GUI-logg visar nytt fönster med titeln `Stella 6.7.1: Debugger mode` efter `run`, men **fönstertiteln är inte svarskvittens**.
- `commands_sent.txt` visar att nytt `print pc` och `saveSes .../A_REENTRY_HANDSHAKE_debugger_session.txt` skickades efter två sekunders etablering; **ingen giltig ny session skapades**. Ursprungsfelet är `A_REENTRY_HANDSHAKE|saveSes did not create a live prompt session`. Den exakta interna orsaken till misslyckad återinträdesprompt är **inte fastställd**; varken verkligt post-run PC/bank/scan/cykelvärde eller native TIA kunde bekräftas i försök 2. **A STRICT FAIL; B/C INTE KÖRDA.** Ett skickat kommando eller titeln ensamt är inget exekveringsbevis.
- [Original GitHub Actions ZIP artifact 14383206943](https://github.com/Odourman/let-me-out/actions/runs/44204912620/artifacts/14383206943), **32 818 bytes**, exakt SHA-256 **`a937861dc55c674abee68146c8e12026bd732e4b36116d55c80aa3b1d39668fe`**, **40 arkivmedlemmar / 39 original SHA256SUMS-poster**. Separat readback-jobb PASS och dessutom lokalt omhashat original ZIP: **39/39 PASS**.
- [Oförändrad original-ZIP på officiella Drive](https://drive.google.com/file/d/1_dSFqTn_bIypBNrsmJiV5WPjgLORwetZ/view).

## 4. Kontrollmatris och tekniskt slutbeslut

| Kontroll | Försök 1 | Försök 2 | Slut |
| --- | --- | --- | --- |
| Ursprunglig F9-16KiB SHA/source/list/sym/mask | STATIC PASS | STATIC PASS | Endast source/ROM-original |
| A initial verklig Stella 6.7.1-prompt | PASS | PASS | Positiv fram till frame/trap |
| A interaktiv frame136 + `added trap` | PASS | PASS | Positiv förförberedelse |
| A faktisk komplett post-`run` stoppkedja | **FAIL**: en kolliderad `print` + en giltig PC | **FAIL**: ingen ny handshake-`saveSes` | **A FAIL** |
| A native TIA vs G5AF M | 320x228 RGB, **pixelidentisk** | INTE KÖRD | Ej komplett A PASS |
| B `break $F1EE` bankbundet `set` + nytt pre-STA stopp | NOT_RUN | NOT_RUN | NOT_DETERMINABLE |
| C exakt `step` med +3 cykler och pre/post-bilder | NOT_RUN | NOT_RUN | NOT_DETERMINABLE |
| D: post-shutdown SHA256SUMS och separat Actions original-readback | **PASS 44/44** | **PASS 39/39** | **D PASS endast arkivintegritet** |

**Slutstatus:** `G5AL_F9_TRAP_CONTROL_FAIL`. Originala capture-jobben är båda **FAIL**, båda D-jobben är **SUCCESS**. En arkiv-integritets-PASS gör inte metodens A till PASS. Resultatet är **mätinstrumenteringsblockering, inte bevis att F9-koden eller Atari 2600-konceptet är omöjligt**.

**STELLA_OBSERVED:** fungerande initial prompt, frame/trap/response, verklig enstaka F9 post-write-PC samt native RGB i försök 1, och faktiska negativa stopp. **SOURCE_INFERRED:** tre CPU-cykler för `STA RESP1` baserat på fryst opcode; ingen faktisk post-step, bus write-strobe eller TIA colorclock mätt. **NOT_DETERMINABLE:** hela B/C, verkligt post-run stopp i försök 2, alla C0/RESP0/X40/X104 och C1–C4/N1.

## 5. Fryst leverans och STOPP

**Specialistbranch:** [rom-dev-iii/g5al-lm-d25-f9-stable-bank-neutral-20261118](https://github.com/Odourman/let-me-out/tree/rom-dev-iii/g5al-lm-d25-f9-stable-bank-neutral-20261118). Källfiler: [förregistrering](PREREGISTERED_F9_METHOD.md), [riktad ändring](TARGETED_CORRECTION_BEFORE_SECOND_FINAL_RUN.md), [runner](run_g5al_f9.sh), [audit](audit_g5al.py), [originalkällkontroll](check_f9_frozen.py), [reproduktion](REPRODUCE_AND_EVIDENCE.md), [samlad bevis-CSV](G5AL_F9_METHOD_EVIDENCE.csv), [fryst manifest](MANIFEST.txt). Rå-zip, sessions, TIA och original-SHA finns både i ovan angivna Actions-artifact och för original-ZIP på Google Drive. Det sista oföränderliga GitHub-commit-ID:t dokumenteras i Issue #17-slutkommentar och kontrolleras via `compare_commits`.

**HISTORIK BEVARAD:** G5AJ/LM-D24 `G5AJ_F9_TRAP_CONTROL_FAIL` 2/2 utan omklassning; G5AH `C0_NO_BUILD_INSTRUMENTATION_BLOCKER` med historiskt ursprungligt readback FAIL; G5AF `G5AF_INSTRUMENTATION_READY_BOUNDED`; G5AD och G5Z negativhistorik oförändrad.

**STOPP:** Ny tredje G5AL Actions-körning, ny ROM/ASM/BIN/DASM, C0/X40/X104/C1–C4/N1, H4/G1/G6/F12, S05, fem NPC, spelgrafik/canon, emulatorpatch, PR-merge eller självständig VERIFICATION II **inte auktoriserat**. `G5_FORMAL_OPEN`. Detta är specialistens egenkontroll och fulla negativa överlämning, inte MAIN VIII:s mottagningsbeslut eller Verification II.
