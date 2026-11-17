# LET ME OUT! – ROM DEVELOPMENT III → MAIN VII
## G5AD / LM-D21 – EN TIA-kalibrerings-ROM: STOPP VID FÖRBYGGSGRIND

**Datum:** 2026-11-17. **Arbetsorder:** [Issue #13](https://github.com/Odourman/let-me-out/issues/13) och [G5AD ursprunglig auktorisation](https://github.com/Odourman/let-me-out/blob/aaaeef0522a746cf4f23faee9fcf2c49dd572d02/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md), Git blob `4480314a2f51cc5569a4d72d5d58ce9d7a910f62`. **Förregistrerad testmatris:** [C0–C4/N1](https://github.com/Odourman/let-me-out/blob/aaaeef0522a746cf4f23faee9fcf2c49dd572d02/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv), Git blob `ba56e95d1729afac0a0df2ce4993c2bfdaa996b2`.

**GLOBAL STATUS: `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`.** Arbetsorderns §5 STOPP har utlösts. Ingen G5AD-ROM, inget G5AD-ASM, inga G5AD-DASM-buildresultat, inga nya `.bin/.lst/.sym`, inga G5AD-C0–C4/N1 faktiska registereffektmätningar, ingen H4, G6, F12, S05, femfienders-implementation eller PR-merge. **Ett äldre fryst F9-ROM** kördes enbart som skrivskyddad kontroll av tillgänglig Stella-instrumentering före något G5AD-bygge.

### 1. Auktoritets- och reproduktionsankare
- Projektets `main` läst vid start: `aaaeef0522a746cf4f23faee9fcf2c49dd572d02`. Separat, ommergad specialistbranch: `rom-dev-iii/g5ad-tia-calibration-lm-d21-20261117` från exakt denna bas.
- Live läst [G5AD Issue #13](https://github.com/Odourman/let-me-out/issues/13), G5AD full originalorder och 6-radiga förregistrerings-CSV samt motsvarande **native Google Doc i officiella Drive**: [G5AD LM-D21](https://docs.google.com/document/d/163Xtt4ygxQD7eM4AfPwZgAN6JktF8DcEQjKK43JNF-g/edit). Äldre G5Z avslutades `G0_INCONCLUSIVE_NO_ROM` i [G5AA](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md); detta ändras inte.
- [NPC-original 8×9 TOP-DOWN](https://github.com/Odourman/let-me-out/blob/aaaeef0522a746cf4f23faee9fcf2c49dd572d02/design/NPC_REFERENCE_8x9_masks.json) Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, oförändrad. Ingen speldesign/kartändring.
- Läs [rå CI-jobblogg – sista förkontrollen](https://github.com/Odourman/let-me-out/actions/runs/44159356697/job/134308674746) före slutsats. Förkontrollen använder [versionsstyrd arbetsflödeskälla](https://github.com/Odourman/let-me-out/blob/rom-dev-iii/g5ad-tia-calibration-lm-d21-20261117/.github/workflows/g5ad_prebuild_instrument_check.yml), inte dold emulatormätning.

### 2. Förbyggsförsök – exakt negativ och positiv teknisk evidens
| Ordning | GitHub Actions run (UTC 2026-11-17) | Klasser / observerat | Vad det INTE är |
|---|---|---|---|
|1|[44158684786](https://github.com/Odourman/let-me-out/actions/runs/44158684786), job `134306268993`, **FAIL**|Installationen av DASM+Stella 6.7.1 lyckades; steg avslutades med `xdpyinfo: command not found`. Det visade saknat `x11-utils` i vår smoke-workflow, inte en TIA-mätning.|Inte ROM, inte Stella pixel-kalibrering|
|2|[44158817619](https://github.com/Odourman/let-me-out/actions/runs/44158817619), job `134306755038`, **SUCCESS**|Med `x11-utils` installerat: `dasm 2.20.15~20201109+really2.20.14.1-2`, `stella 6.7.1+dfsg-1build2`, Xvfb/X11, xdotool, PIL 10.2.0 och Stella-hjälp fungerade.|Verktygens *närvaro*, inte registertrace|
|3|[44159089329](https://github.com/Odourman/let-me-out/actions/runs/44159089329), job `134307740733`, **FAIL**|Laddade arkiverad 16KiB F9-ROM **utan DASM/rebuild**. Verifierad befintlig SHA-256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`. `stella -debug` skrev en native TIA-PNG på **320×228** och skapade en `session_...txt`. `saveSes`-filens innehåll gick inte att använda för maskinläsbar `_scan/_sCycles`-beviskedja (`G5AD_SAVED_DEBUGGER_SESSIONS []`).|Inte nytt G5AD-ROM, PNG är inte registertidslinje|
|4|[44159356697](https://github.com/Odourman/let-me-out/actions/runs/44159356697), job `134308674746`, **FAIL**|Samma äldre F9 SHA256 verifierad igen. Native TIA-PNG skapades åter och `saveSes`-session skapades, men **`SESSION_FILE_BYTES=0`**, explicit återläst ur exekverad jobblogg. Efter detta fick Python-hjälpkoden separat `IndentationError: unindent does not match any outer indentation level`; alltså är delar av den sista insamlingspostprocessen också felaktiga.|Python-felet ska INTE döljas och är inte ensamt förklaring till 0-byte-sessionen|

Alla fyra körningarna gällde **förkontroll, inte G5AD-bygg**. Den andra körningens resultat bevisar installationen, och tredje/fjärde visar att en skärmbild utan full återläsbar debuggersekvens inte räcker för G5AD:s explicita miniminivå. Det är inte styrkt varför `saveSes` blev tom: automatisk scriptsession kan vara en faktor, men det är **hypotes**, inte verifierad Stella-bugg.

**Rå evidens (Actions):** [första misslyckade paketkontrollen](https://github.com/Odourman/let-me-out/actions/runs/44158684786/artifacts/14361827778), [F9 read-only image + misslyckad sessionkontroll](https://github.com/Odourman/let-me-out/actions/runs/44159089329/artifacts/14361528784), [sista insamlingspaketet](https://github.com/Odourman/let-me-out/actions/runs/44159356697/artifacts/14362582337). GitHub jobbloggarna är primära för de exakta terminalvärdena; native Stella-snapshots under `/home/runner` **kopierades inte bevisligen in i leveransartefakten**. Får inte påstås bytebevarade där. Den sista CI-artefaktzippen har av Actions rapporterad SHA-256 `853d1887d108cd9fc1c5b895546558afe28e747c03e169ee007ee243f14f966a` (artefaktplattformens SHA, inte oberoende omräknad av ROM DEVELOPMENT III).

### 3. Exakt instrumenteringsblockerare enligt §5
G5AD kräver för varje fall **samtidigt och med en final ROM SHA**: (a) verkliga CPU-`PC` och instruktionens `STA`-slutcykel, (b) `_scan` och `_sCycles` vid avsedd registerskrivning, (c) `NUSIZ0/GRP0/1/RESP0/ENAM0/RESM0/COLUP0` före/efter samt (d) nativ råpixel-colorclock vid exakt samma Y och case.

Den redan existerande instrumentvägen kunde producera (en gammal) raw PNG och UI-screenshot, **men ingen icke-tom, hashbar och mätvärdesbärande register-/CPU-session**. Under sista kontrollen inträffade även ett faktiskt insamlingsskriptfel. Därför kan `PC → STA-write-cycle → intern TIA effekt → pixel X/CC` **inte återknytas till en och samma frysta mätning på ett reproducerbart sätt i denna utförandemiljö**. Att gissa på TIA-fördröjningen eller dra slutsatser från enbart 320×228 bilden bryter §2–5.

Vi använder därmed **arbetsorderns explicita NO-BUILD-utgång**, inte `G5AD_PARTIAL_NOT_DETERMINABLE` (den senare förutsätter en faktiskt byggd G5AD-ROM med mätningar). Det finns inga "misslyckade G5AD-pixeltest", för inget G5AD-case har körts; negativa utfall här är *förinstrumenteringens* tester.

### 4. Alla sex förregistrerade fall
| Case | Förregistrerat krav | G5AD per-case verdict | Faktiska G5AD STA/scanline/CC |
|---|---|---|---|
|`TIA-C0`|Två numeriska RAM-X P0-original M och korrekt 9-radig bitmap samt RESP0-fas|`NOT_DETERMINABLE`|**NOT_RUN_NO_NEW_ROM**|
|`TIA-C1`|Två P0-identitetsordningar + nära overlap; klipp/ghost/RESP0-write|`NOT_DETERMINABLE`|**NOT_RUN_NO_NEW_ROM**|
|`TIA-C2`|På samma 9-raders-Y: NUSIZ0=$00 vs $02 och P0/M0-kopior|`NOT_DETERMINABLE`|**NOT_RUN_NO_NEW_ROM**|
|`TIA-C3`|Samma C2 input men två ENAM0-gatefaser|`NOT_DETERMINABLE`|**NOT_RUN_NO_NEW_ROM**|
|`TIA-C4`|GRP0/GRP1 nära kontra före START och VDEL-fas|`NOT_DETERMINABLE`|**NOT_RUN_NO_NEW_ROM**|
|`TIA-N1`|P0 M rad3 FF + M0 visuellt X43; delat COLUP0-negativt scenario|`NOT_DETERMINABLE`|**NOT_RUN_NO_NEW_ROM**|

**Observerad hårdvarufysik för G5AD: noll nya mätvärden.** NTSC-källformel 228 TIA-colorclocks =76 CPU-cykler är generell referens, inte G5AD-mätt. Tidigare F9 har positiva **andra** originalbevis och får inte ersätta dessa sex kontroller.

### 5. Vad som skulle krävas för att häva *denna* tekniska blockerare senare – ingen ny order
Minimikravet är en fungerande reproducerbar debugger-inspelare som på en *redan befintlig* ROM kan frysa samma frame/bank/PC och logga efter-STA `_scan/_sCycles`/registertillstånd i en **icke-tom text/CSV** med tidsmässigt motsvarande **native, sparad** pixelbild. Därefter måste två olika kända registerstopps timing kunna kontrolleras mot samma källa, och postprocessens egna fel uteslutas. En möjlig interaktiv debuggerprompt eller kontrollerad extern instrumenterare är bara ett alternativ för ett **framtida separat beslut**, inte en åtgärd som utförs här.

**STOPP:** G5AD utförd **till grinden och stoppad före byggnad**. `G5_FORMAL=OPEN`, `FULL_H4/G1/G6/F12/S05/FIVE_NPC/INDEPENDENT_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`. Ingen egen ny testfamilj eller fortsättning föreslås som redan beställd. MAIN VII mottar denna blockerarrapport och avstämmer separat.
