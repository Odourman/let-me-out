# LET ME OUT! – MAIN V → ROM DEVELOPMENT II
## R1-F8: THIRD ORIGINAL NPC + THIRD INDEPENDENT BINARY X – SOURCE ONLY SCALING GATE

**Datum:** 2026-11-16. **AUTORISERAT:** EN separat, snävt avgränsad **READ-ONLY käll- och TIA-arkitekturanalys** inom användarens godkända standard F6/NTSC v0.18 R1-tekniska scope. **INGEN ny ROM, assembler, DASM, Stella, screenshot, CI-run, automatiskt kodbygge, ändring av source-/originalmasker, ny grafik, R1ba-fix eller PR-merge.** Lägg bara **EN** analysrapport till en NY isolerad branch från frysta F7 `c8dc8b35f4bb652e3920b70882f8cc1fb84125d3`. ROM DEVELOPMENT II ska STOPPA efter rapporten även om en genomförbar idé hittas. Det är inte F8-implementation.

### 1. Varför F8 och vad som verkligen är löst

Se [MAIN V:s egna F7-evidensgranskning](MAIN_V_R1_F7_RECEIPT_AND_THREE_X_SCALE_DECISION_2026-11-16.md), den frysta [R1-F7 rapporten](https://github.com/Odourman/let-me-out/blob/c8dc8b35f4bb652e3920b70882f8cc1fb84125d3/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F7.md), [bindande R1-originalmasker](../design/NPC_REFERENCE_8x9_masks.json) blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, [FULL R1 kriterier](ROM_GATE_V018_ACCEPTANCE.md), [6 independent-X krav](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md), PR #7 omergad, original `main` STATE och tidigare [R1ba-orienteringsmotbevis](MAIN_V_R1_F5_RECEIPT_R1BA_VERTICAL_ORIENTATION_INDEPENDENT_AUDIT_2026-11-16.md).

F7 ger **EN** standard-F6/NTSC-ROM med **TVÅ** rättvända original 8×9: man/female; separata `X0_SELECT=$A0`, `X1_SELECT=$A1`; **FYRA** i äkta Stella verifierade par `(39,99),(45,99),(39,105),(45,105)`; 160/160 samma ROM och 4/4 ortogonala kontraster. De väljs av **FYRA FÖRKOMPILERADE nio-raderskernlar** efter RAM-branch; det ger inte godtyckliga numeriska X, fri Y, tre figurer eller full R1.

**F8:s ENDA fråga:** Finns en realistisk **tredje fysiskt separat P1-utritad original-NPC i exakt samma nio-radersband**, med **en TREDJE egen RAM-bit `X2_SELECT`** som kan välja två X-lägen utan att flytta de första två eller skada originalmaskerna, medan `P0` gul spelare, `M0` statiskt skott, brun `PF`, `NUSIZ1=$01`, 262 NTSC och en 76-CPU-cykelrad bevaras? Påvisa **full sanningsmatris på papper 2×2×2=8**, eller visa ärligt att detta inte kan ske inom nuvarande sekvens.

**Avgränsad tredje mask för kalkylen:** Använd `small_male` från låst original `00 00 3C 3C 18 7E 18 24 00` i sina NIO topp-till-botten-rader – den ska pröva nollledande rader och byteväxling. Mannen/female F7 är oförändrade; ingen maskorientering får vändas och `X2` får ej ersättas av en annan hårdvarukopias samma bundna X. Detta är en diagnosfråga, **inte** ett beslut om slutlig NPC-ordning i spelet.

### 2. Måste göras utan ny körbar kod: exakt källtidslinje och fysiska villkor

Gör en source-only tabell för **varenda nio synliga bitmaprader och alla 8 RAM-bitkombinationer**:
- F7:s två befintliga `RESP1`-faser `(c21/c23)` och `(c32/c33)`, `GRP1` c24/c26 och c35/c36, inklusive exakt **när GRP1-kvinnan latched / sista pixel**. F7 row0–7 `WSYNC` c38/c39 och slutrad c41/c42 är historiskt **STATIC**; tredje maskens `RESP1` och `GRP1` får **inte** bara läggas ovanpå innan den föregående kopian hunnit visa hela 8pixlar (16 screenshotpx). Räkna TIA färgklockor, 6502 cykler och databeroenden inklusive `NUSIZ1=$01` close-copy, GRP-latch och nästa `RESP1`-startsignal.
- Registrera **två** hypotetiska `X2`-faser innan någon framtida ROM, och förutsäg två fysiska X-lägen med **oförändrade** M/F-positioner i var och en av de fyra gamla lägena. Om inget par av tredje-kopiestarter kan uppfylla maskpixel-/copy-start-/register-/timingvillkoren, skriv explicit `NO_X2_START_FOUND`, INGEN spekulativ värdetabell.
- Deklarera verklig tredje RIOT RAM-bit och **OBEROENDE** update-väg utan att inkräkta på `$A0/$A1`, befintliga 30 blank-/TopBlank-scanlines och tidigare P0/M0/PF/HMOVE-data. Källgranska F7:s `r1_f7_build.py`, faktiska arkiverade `r1_f7_2x2...asm`, `.lst/.sym` och skärmbilder (READ ONLY), inte bara utvecklartext.
- Räkna **faktisk värstafalls-kodstorlek** och branch-/entry-kostnad för de 8 förberedda fulla nio-radersvarianterna jämfört med tillgänglig standard-F6 **4 KiB per bank** och F6-bankbytestiming (bankning ger ROM-datayta, **inte** fler TIA-register/CPU-cykler). Alla 8 lägen måste kunna nås från samma exekverbara ROM utan flyttat NTSC-frame/hårdvarumasker. Redovisa även 4:e–6:e NPC:s asymptotiska källkodskostnad `2^n` om samma rena unrolled-väljarmetod skalas vidare; **ingen** spekulativ sex-X/Y-acceptans.
- Bedöm källmässigt om detta kräver **ny kernelarkitektur** snarare än en enkel utvidgning, med explicit alternativ (exempelvis delad rutindata/efter-HBLANK rastermultiplex eller NUSIZ-kopiegrupper) och deras bevislägen. Äldre R1ba `NUSIZ1=$03` är endast rådgivande: den visar fyra inverterade stor-NPC-rader i historisk research och positioner i fasta grupper, **inte** frikopplade X.

### 3. Obligatorisk falsifierbar slutsats, inga nya builds

Lämna exakt en av dessa slutsatser, med redovisad källa per tekniskt antagande:
1. `F8_THIRD_BINARY_X_SOURCE_FEASIBLE_WITH_PRE_REGISTERED_EIGHT_STATES`: åtta källbaserat cykel- och 4KiB-kontrollerade kombinationer + två specifika X2-hypoteser, **inte Stella-PASS**, och **ingen framtida ROM tillåten utan nytt separat MAIN-beslut**;
2. `F8_THIRD_X_REQUIRES_NEW_ARCHITECTURE`: dagens F7-unrolled-linje räcker ej, redovisa exakt första falsifierade grind och **ett** källgrundat alternativ som kräver användarens/MAIN:s nytt arkitekturscope;
3. `F8_SOURCE_INCONCLUSIVE`: går inte att belägga när faktisk latch/counter/GRP-start sker, rekommendera en minimal källstödd framtida verifieringsgrind, men **bygg inget nu**.

Kostnadsredovisa skillnaden mellan **tre separata binära RAM-väljare**, **tre godtyckliga X**, **sex godtyckliga X/Y** och riktig **R1 C01/C04/P0/M0/PF/R3**. Fortsatta TIA-sweeps, produktionskod, nya 600-frame körningar, tredje ROM, 6-NPC-cellkärna eller PAL kan inte motiveras av F7:s tvåmaskers-PASS ensamt.

### 4. Leverans och hård STOPP

Endast **en ny Markdown-rapport** med källkonservativ tabell och motbevis till MAIN V på ny branch från fryst F7, sökväg `docs/ROM_DEV_R1_F8_THIRD_BINARY_X_SCALING_SOURCE_ONLY_TO_MAIN_2026-11-16.md`; efter handoff i GitHub Issue #6 STOPP. **Ingen ny DASM, Stella, 6502/ASM, Python-audit, PNG, ZIP, CI, R1-F9, R2–R4, sexgodkännande, R1ba-ändring, PR #7-merge eller Issue #8 VERIFICATION** i F8. R1 fortfarande **`BLOCKED / NOT ACCEPTED`**, GRAPHICS fortsatt avslutat. Överträdelser av kopie-/mask-/RAM-/bankbudget ska redovisas som blockering, aldrig kringgås med nytt mapperformat eller användar-waiver antagen utan beslut.
