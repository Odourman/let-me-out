# LET ME OUT! – G5: bindande beslutsspärr och framtida scope (ingen canon-ändring)

## MAIN VII G5Q – uttryckligt G5-designmål krävs; förslag är inte canon (2026-11-17)

[G5Q-beslutsförslag](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_DECISION_READY_DESIGN_TARGET_AND_PRE_G6_BOUNDARY_2026-11-17.md) · [officiell Drive-kopia](https://docs.google.com/document/d/1_bB-F6pvwEehRP09F1jdfyYnUtKo4c6mie4QD3c9YGw/edit). **G5Q är en användarbeslutsberedning, inget nytt godkännande.** MAIN rekommenderar A1 (fri logisk NPC-X/Y med ursprunglig jakt och utan hård permanent Y-lane) och B1 (kvalitetsmål: fem ursprungliga NPC läsbara, farliga NPC ej systematiskt dolda, key aldrig dold enbart för same-Y utan faktisk bitpixelöverlapp). G5P:s mjuka/fri-modellers ~498,6/900 bortprioritering är **syntetisk köbelastning, inte fysisk flicker** och ger ingen generell waiver. O1/LM-D06 redan godkänt men begränsat. Separata userbeslut återstår om formell fem-NPC R1/R2-bas, -30 kontra -25, 1/5 bärare/femspawn och exakta v0.19-kartor. G4 H4-ONE och G5P:s snävare G0-proposal är ännu inte samma definierade testorder. **Ingen G5-PASS, inga ändrade spelregler, ingen G6/F12/ROM/VERIFICATION/PR-merge.**


## MAIN VII G5P-mottagning – source-only reproduktion PASS, formell G5 ÖPPEN (2026-11-17)

[MAIN VII:s mottagnings-/reproduktionsrapport](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1HzRq0wJlX8iZPZsxeDRWpQenMI5eveAr9lIgfTNICSA/edit) · [RESEARCH II:s underlag](https://github.com/Odourman/let-me-out/blob/research/g5p-adaptive-y-offline-20261117/docs/research/G5P_RESEARCH_II_FULL_REPORT_2026-11-17.md). Råfiler 672 huvudfall + 168 globalfall + 12 historiska replay verifierades; Pythonkörning gav **sex byteidentiska CSV** och ZIP-manifest/CRC PASS. Källkartornas grid 8/8 matchar live GitHub. **Detta accepterar endast reproducerbarheten hos rådgivande offlineforskning, INTE en TIA-kernel eller oberoende Verification.** G5P visar fortsatt svagheter med hård Y-lane, och mjuk Y ger förbättrad AI men stor syntetisk same-Y-synlighetsbelastning. Fri logisk X/Y med situationsberoende visuell planering är en **kandidat**, inte godkänd policy. S05 och kvantifierade synlighetsgarantier olösta; O1 endast godkänt vid faktisk NPC/key-pixelöverlapp. `-30`/kill, 1/5-key/spawn, framtida R1/R2-bas och exakta v0.19-kartor fortfarande användarägda beslut. **G5 formal ej avslutad; G6/F12/ROM, oberoende Verification och PR-merge ej auktoriserade.**


## MAIN VII G5P – source-only RESEARCH II-order, formell G5 fortsatt spärrad (2026-11-17)

[Preciserad G5P-instruktion](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5P_MAIN_VII_TO_RESEARCH_II_ADAPTIVE_Y_POLICY_STUDY_ORDER_2026-11-17.md) · [öppen specialistuppgift #9](https://github.com/Odourman/let-me-out/issues/9) · [Drive](https://docs.google.com/document/d/1NHYV4EVnJyce19DCyFHFA_bEk5UMKHlN9okugkeyDxc/edit). MAIN har **bara** beställt en rådgivande jämförelse, inte fått RESEARCH II:s rapport. Nya testmått kräver kollisionskorrekt jämförelse; G5O:s <=1 av 5 nära spelarankare är delvis inneboende i en två-gridraders Y-separation och ingen självständig design-NO-GO. Bevara faktiskt negativa B01-stallfall och rådata. Inga nya rendering-/Y-/AI-/flickerregler, score -30, femspawn, R1/R2-rebaseline, kartbyte, G0/G6/F12 eller ROM får antas från denna order. O1 begränsat godkänt, S05 kvarstår tekniskt olöst. **G5 formell användargrind fortfarande ÖPPEN.**


## MAIN VII G5O – negativt source-only-strikt-lane-dynamikprov (2026-11-17)

[G5O/MAIN:s 12-scenariers test](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5O_MAIN_VII_STRICT_S1_Y_LANE_DYNAMIC_CHASE_NEGATIVE_SCREEN_2026-11-17.md) · [CSV](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5O_HARD_LANE_GREEDY_CHASE_12_CASES_SOURCE_ONLY_2026-11-17.csv) · [Drive](https://docs.google.com/document/d/12RG0YNpimCiY64gVTFYpaPzrjTYDXnLMfUONPYjLDqQ/edit). Den hårda S1-regeln `abs(grid_y_i-grid_y_j)>=2` för fem 9-raders NPC ger vid en enkel 2×2/BFS-girig modell högst en nära stillastående spelaren efter 180 ticks i 12/12 v0.11-kart-/målscenarier, B01 startspelarankare 0/5. **Det är en negativ MODEL SCREEN, inte allmängiltig S1-NO-GO, inte spelets riktiga AI/ROM/Stella.** En stabil femstart (G5N) räcker inte för spelbar jakt. MAIN rekommenderar att ingen hård S1-Y-restriktion canoniseras förrän RESEARCH II rådgivande bedömt adaptiv Y-planering och/eller synligt specificerad temporär multiplex/flimmer. Originalbeslut 008/019–025/032–034 får inte tyst ändras. **Formell G5 och score/spawn kvar; G6/F12 ej auktoriserade.**


## MAIN VII G5N – nya initiala start-/spelsystemfynd, utan auktorisation (2026-11-17)

[Full G5N source-only-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5N_MAIN_VII_S1_FIVE_NPC_LANE_START_AUDIT_AND_SCORE_PROPOSAL_2026-11-17.md) · [Drive-kopia](https://docs.google.com/document/d/1oVeMuwiwUrvzQrNBBd-aMUVHxnj5HiGgDWBPesy1CTQ/edit). **G5-S1 prövas som rekommenderad huvudkandidat**, inte som beslutad Y-lane gameplay. En deterministisk 2×2-grid-/BFS-enumerering av *endast v0.11:s historiska A01/B01/C02/D01* visar 2 208/48/1 248/420 möjligheter till fem startpunkter med parvis skilda 9-raders grafikband. Ingen dynamisk jakt, nyckelåtkomst, 8×9-hårdvarugeometri eller 2600-kernel är därmed verifierad. G5N föreslår -30 per kill för att undvika framtida +25 all-kill-farming, och fem validerade spawns/1/5 key-bärare; allt väntar på särskilt användarbeslut. **O1:s godkända faktiska överlappningsscope och alla G5/G6-spärrar oförändrade.**


## MAIN VII RÄTTELSE TILL G5:s O1-FORMULERINGAR, 2026-11-17

**Det senare uttryckliga användarbeslutet O1 är redan giltigt**, trots att några nedanstående MAIN VI/G5L-avsnitt felaktigt benämner det preliminärt. Se [O1-beslutet med ordagrant användarsvar](../MAIN_STATUS_NEXT_10_2026-11-15.md), [LM-D06 GODKÄNT](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) och [korrigendum](../project_sources/PROJECT_SOURCES_MAIN_VII_CORRIGENDUM_2026-11-17.md).

O1 tillåter tillfällig skymning av nyckel **vid verkligt android/nyckelöverlapp** utan ändrad logisk position/upptagning. Mindre, tillfälligt flimmer är acceptabelt kvalitativt; **inte** kvantifierad 10Hz, systematisk same-Y-occlusion eller dold nyckel när ingen verklig överlappning finns. Godkänd O1 får **inte** användas som ersättning för den fortfarande olösta G5-S0/G5-S1/G5-S2-kernelpolicyn.

**Övriga G5-spärrar fortsätter oförändrat:** formellt val av Y-rörelse/synlighetsgarantier utöver O1 och femfiendersscore/spawn saknas. Ingen G6/F12/ROM/ny verifiering/PR-merge är auktoriserad av denna rättelse.

**2026-11-17 · MAIN VI. Status: `G5_USER_DECISION_PENDING_NO_CANON_CHANGE`.**

Detta är en styrning av vad *inte* får påbörjas till följd av teknisk feasibility-granskning. [Fullständiga käll-/risk- och vägvalsbedömningen](G5_CANDID_FEASIBILITY_ASSESSMENT_AND_DECISION_BRIEF_2026-11-17.md) är separat och normativ som **MAIN:s rekommendation**, men **inte ett nytt användarbeslut**.

## 0H. G5M ny fem-fienders följdkonsekvens: score och nyckelbärarslump kräver eget uttryckligt beslut

[**G5M full källbaserad analys av 57 beslutsrader**](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md) · [Project Sources-revisionspaket index](https://github.com/Odourman/let-me-out/blob/main/docs/project_sources/PROJECT_SOURCES_REVIEW_PACK_2026-11-17.md) · [officiell Drive ZIP](https://drive.google.com/file/d/1Pv0TUKoN3QVu-Yy8UZFOhlv7OgoGOQit/view). Efter uttryckt arbetsmål **5** i stället för originalets **6** visar originalpoängreglerna 042–047 en **ny potentiellt blockerande spelbalansändring**: normalt långsiktigt all-kill `-25*6 + 50+100=0`; fem blir `-25*5 +50+100=+25` per rum om nollgolv inte ingriper. Beslut 047 hade avsikten att all-kill inte gav långsiktig highscore-tillväxt. Vid första rum/nyckelupptagning före sista kills gäller nollgolv och händelseordning, inte dessa nettoformler automatiskt. Original 021 sex slumpade prevalidated spawn och 022 1/6 uniform bärare behöver framtida, **inte tyst gjord**, omprövning till fem positioner och 1/5 uniform sannolikhet.

**G5 FORMAL** har nu TVÅ separata användarägda beslutsklasser: (i) Y-/synlighets-/grafik-kernelpolicy (G5L), (ii) fem-NPC-poängbalans, bärar- och spawn-revision (G5M). Båda måste senare skrivas in i nytt versionerat scope/acceptance om användaren godkänner dem. **Inget av dem följer av "fortsätt"**, och ingen G6/F12-kodorder, ny VERIFICATION eller PR-merge får utges. Sourcepaket är navigation-only.

## 0G. G5L TEKNISKT EXIT-PAKET – sista kvarvarande USER-valet, INTE nästa G6 (2026-11-17)

[GitHub: avslutande G5L source-only 30 tricks/3 arkitekturer/10 nyckel-dörr stressfall](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md) · [fullständig Drive-kopia i officiella projektmappen](https://docs.google.com/document/d/1zbusyasMrLlO4zIp3iq8iplr8cvjvlAvbcgkDATOi38/edit) · [10-scene CSV](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv). **G5 technical source-only research COMPLETE, G5 formal decision PENDING**. Ingen ny generell five-NPC same-Y+key/door G0 kernel. Berzerk Y-lane och vår P0/P1 door-hybrid är lovande *enbart som villkorad designförändring*; när key och vit robot är på samma door-Y fordras P0=player+robot+key om P1=door och den föreslagna fasta 1-P1-policyn upprätthålls. Även O1 nyckelskymning är dokumenterad som **preliminär MAIN-policy, inte användarcanon**, så kan inte användas för att dölja icke-pixelöverlappande key.

**En enda återstående G5-designfråga:** tillåter användaren Y-arbitrering så att fem fienders 9-fysiska-radersband inte överlappar, med konsekvenser för rörelse/AI; eller skall de kunna röra sig helt fritt i Y utan automatisk flicker? Det finns ingen implicit waiver. **G6/ROM DEVELOPMENT III/independent VERIFICATION II behöver separata explicita arbetsorder oberoende av detta val.**

## 0F. G5J/G5K verklig Berzerk-källa och förberedd dynamisk kanal-arkitektur, Y-policy EJ GODKÄND

[Den kommenterade historiska källan analyserad, G5J](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md) · [dynamisk P0 player/robot ↔ P1 orange door, G5K](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md). Berzerks 8 robotar använder Y-start med gap och rörelsekontroller, inte 8 same-Y 8bitars originalsprites. En **fram­tida** möjlig Atari 2600-renderer kan ha fem logiska NPC i Y-lanes, och per dörrband låta P0 hålla player+vit NPC medan P1 förblir R3-orange/black-hole. Offline 176 scanlines max P0 två/P1 ett, men **inte** ROM-pass. En sådan *Y-begränsning* av fienders frihet/AI är en uttrycklig användarägd canonändring; VARKEN den, key-O1, flimmer-/occlusionpolicy eller G6/F12 har blivit godkända genom användarens "fortsätt". Historiska v0.18 six-R1/5+key-R2 oförändrade. **Slutsats:** G5 källforskning konkret förbättrad och avslutad inom nytt G5J/K scope; FORMAL G5 fortfarande PENDING, G6 spärrad.

## 0E. G5I plan-/auktoritetsavstämning – felaktigt G5→G6 förhindrat (2026-11-17)

[Versionsstyrd G5I avstämning och framtida femfienders R1/R2 acceptance-delta](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5I_PLAN_RECONCILIATION_FIVE_NPC_DECISION_READY_NOT_G6_2026-11-17.md) · [fullständig officiell Google Drive-kopia](https://docs.google.com/document/d/1Zc-n5K-RHRZ5YriInxyQBqmb99siXl44547cVteT1YI/edit). G1–G4 avslutade som read-only/source-only underlag, G5:s tekniska feasibility-analys och G5F/G5G/G5H-delstudier utförda och dokumenterade. **G5 FORMELLT beslut om testkrav/visuell policy och eventuell 6→5 cutover fortfarande PENDING**; gammal R1 sex / R2 fem+nyckel gäller tills en riktig userauktoriserad rebaseline. Användaren har redan uttryckt Atari 2600, fem (M,M,F,SM,SF), svart bakgrund och nyckelhål som del av orange port – fråga inte om dessa preferenser på nytt. Utan explicit waiver för flicker/occlusion skall gamla synlighetskrav inte försämras i smyg. **"Fortsätt om klar" är villkorat, inte en separat specificerad G6 ROM-uppdragsorder.** Inga G6/F12/Gameplay/Verification eller nya masker inledda.

## 0D. G5H 24/36 ordningar, gräns för direkt-GRP/RESP-kernel (2026-11-17)

[GitHub G5H käll-/registeranalys](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md) · [Google Drive fulltext plus CSV](https://docs.google.com/document/d/1rsRlR4BOjXnY9Wtsp1N3Oq_02yGVMiAKD6Z3UhFa4Q4/edit). Vid fem fiender med originalmasker och orange P1-port räcker source-only direkt `GRP/RESP`-sekvens inte i fria worst-case-X: originalrad6 A 79/76 i alla 24 P1-ordningar, B bästa 74/76 bara om samma M-M intill, B 79/76 när player mellan två M, upp till 89/76 i uttryckligt hypotetiskt gult M0-stressfall. Ingen fysisk G0/ROM-pass, inga ROM-ändringar. Varken tidigare R1 sex, R2 fem + key eller G5 användarens slutliga designval har reviderats. Ytterligare experiment/implementation G6/F12 kräver separat uttrycklig auktorisation; RESEARCH II kan enligt MAIN studera NY kernelfamilj source-only.

## 0C. G5G ny teknikforskningskandidat; källmässigt naiv 6507-direktsekvens FAIL

[GitHub hela G5G-rapporten](../gates/G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md) · [maskinläsbar 9-scenario CSV](../gates/G5G_DIRECT_EVENT_CPU_CYCLE_CENSUS_2026-11-17.csv) · [Google Drive-kopia i projektmappen](https://docs.google.com/document/d/14sNkAi8gdLqz2wo6OtR9jrpTggrcXB0cv-BCO3onaWY/edit). Teknik: reflektions-PF plus `Ball` 4CC i brunt vid x0 **endast på dörrbandet** när PF0=0, P1 samma orange bitmask med negativt svart keyhole, COLUBK svart. PF+BL 3520/3520 logiska kartceller PASS **endast offline**; BL-positionering, door P1+vit NPC same-Y, M0 och X/Y START-tider INTE mätta.

A/B:s enkla direkta 6507-instruktionsmodell på stadig dörrrad **79/76** (PF0-right toggle tidigare **89/76**); själva Ball/PF-radövergången ökar modellen till **89/76**. **NAIVE PLAN FAIL**, inte 2600 hardware NO-GO; full fysisk G0 ej godkänd och ROM IMPLEMENTATION EJ AUKTORISERAD. Befintlig användarcanon för historiska R1/R2 testantal samt övriga G5-val förblir spärrad i avvaktan på separat explicit användarbeslut.

## 0B. G5F source-only fem-NPC/REF PF baserad på faktisk källanalys, INTE en kodorder

Efter användarens "Ok, fortsätt" färdigställde MAIN VI [G5F source-only arkitekturrevision](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5F_FIVE_ANDROID_REFLECTED_PF_DOOR_SOURCE_ONLY_ARCHITECTURE_2026-11-17.md) och [Drive fullständigt underlag](https://docs.google.com/document/d/1PAELvVABaDAVuhZILC1Czo5kEIiRGQV2IaZ1bdtKRNw/edit). Alla fyra kartor speglar vänsterhalvan på 18/22 rader, endast dörr x39/y9–12 avviker. Förslaget är `CTRLPF.REF`, latched återbruk av väggdata, eventuellt PF0-only högersidig override på dörrlinjerna samt befintligt P1-dörrmotiv med svart utskuret nyckelhål. 5-NPC-maskradlast 3/3/5/5/5/5/5/5/3; F11 och P0/M0-färgkonflikter kvarstår. **Ingen G6/ROM-implementationsorder, ändrad v0.18-acceptans eller ny teknisk PASS följer av denna dokumentation.** Formellt G5-beslut, fem-NPC cutover av historisk R1/R2 och eventuella visuella waivers är fortfarande användarägt.

## 0A. Ny användarinitierad fem-NPC- och Video Chess-forskningskandidat (2026-11-17)

[GitHub dokument med användarens femandroidsförslag, Berzerk-jämförelse, och Video Chess/Venetian Blinds för guldnyckel + högerdörr](../MAIN_VI_FIVE_ANDROID_BERZERK_VIDEO_CHESS_RESEARCH_DIRECTION_2026-11-17.md) · [arkiverad Google Drive-kopia](https://docs.google.com/document/d/1Iv9XrYt3CvkPNhiCGxSgEQSe0M91SHa4CHIjqP6YAA8/edit). Exakt kandidat: **2 large M + 1 large F + 1 small M + 1 small F = 5** (mot frysta 2M+2F+SM+SF=6). R2 blir hypotetiskt 4 kvarvarande NPC + nyckel om antalet ändras. Kandidat för nyckel/dörr: pröva omväxlande scanlines NÄR de ligger på samma höjd; jämför först med enkel Y-separerad spriteåteranvändning och PF-buren dörr. Tidigare android-Venetian-negativfall är inte automatiskt key/door-negativfall.

**Auktoritet:** användaren bad att minnas och arkivera förslagen, **INTE** uttryckligen att fastställa ny canon eller utfärda kodorder. Originalantal 6, R1/R2 acceptans, fyra 8×9 TOP-DOWN-masker och G5 PENDING USER kvarstår. Varken G6 eller någon annan implementation är beslutad.

## 1. De två möjliga framtida produktbesluten
**A – Atari 2600, ny visuell renderingspolicy.** Behåll sex logiska individuell X/Y NPC, fyra typers originalidentiteter, gul spelare, en projektil, fyra rum, högernyckeldörr, O1/K1/E1, poäng, liv, RESET-only och spelkänsla **som mål**. Användaren måste *se och uttryckligen godkänna* den föreslagna policyn för hur många NPC som får saknas/flickra/occluderas på överbelastad same-Y-rad och exakt vad original8×9-krav ska betyda för en överlagrad grafisk framställning. Varken ändrade exakta rumsrutor, begränsad NPC Y-mobilitet, annan dörrfärg eller reducerat antal NPC följer automatiskt.

**B – originalambition bibehålls, plattformsbyte till Atari 7800/MARIA.** Användaren behöver uttryckligen bestämma att Atari 2600-målmaskinen överges som leveransplattform. Exakta originalmasker, sex fria X/Y, fullfärgsguldkey och orange/black dörr blir då vidareförda designmål; 7800-renderingen och ROM/gameplay måste nyutvecklas separat och är inte verifierad ännu. Standard-F6-DASM/2600 TIA-resultat är forskningshistoria, **inte** en färdig 7800 implementation.

Den tidigare G4-"villkorad GO" för EN mikrofysik-uppgift är en **alternativ forskningsmetod om användaren önskar testa originalspecen lite till**, inte ett tredje automatiskt produktbeslut. Ett lyckat mikroprov har INTE visat sex NPC eller guldkey/door samtidigt; inte heller ska ett misslyckande automatiskt ändra canon.

## 2. Frågor som kräver uttrycklig framtida användarformulering
- Vilket är absolut viktigast: **Atari 2600 som hårdvara** eller **alla nuvarande samtidiga originalgrafikregler**?
- Om A väljs: exakt **flicker-/occlusion-policy** och vilken minsta läsbarhet som krävs, särskilt sex same-Y och gameplay-/collision-invariant, baserat på synliga testklipp innan godkännande.
- Om B väljs: uttryckligt målmaskins- och scopebyte; nytt ROM- och oberoende verification-upplägg.
- Om användaren vill fortsätta exakt 2600-forskning: explicit separat mikro-G6-order enligt [G4 DRAFT_NOT_AUTHORIZED](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md), med **G0 före bygg**, bounded exit och ett förhandsgodkänt kostnadsstopp.

**Nej till tysta antaganden** om "lite flimmer" = 10 Hz för en NPC, F6SC/ARM löser sprites, ändring 6→4 NPC, att nyckeln får vara brun eller att den vänstra väggen får öppnas.

## 3. Aktuell auktorisation och tekniskt tillstånd efter G5-analysen
| Del | Nuvarande faktiska status |
|---|---|
| **G1–G4** | Dokumentation/evidens/source-only analyser färdiga, ej ROM-PASS |
| **G5 feasibility-analys** | COMPLETE – ärlig 2600 produktplan bedöms **NO_GO med samtliga exakta krav samtidigt** (ingen universell omöjlighetssats) |
| **G5 val av canon/teknisk väg** | **PENDING USER DECISION** – inte godkänt/inte färdigt |
| **G6 nytt ROM-mikroprov/F12** | **NOT AUTHORIZED / NOT ORDERED** |
| **Full R1 och R2–R4** | BLOCKED / NOT ACCEPTED |
| **PR #7** | DRAFT, UNMERGED |
| **Issue #8** | Oberoende äldre fryst E02-baslinje, ej ny G5/future-ROM |
| **Andra projekt eller annan cartridge-mapper/PAL/fullspel** | INTE auktoriserade inom detta steg |

## 4. MAIN:s styrrekommendation
**Gör inget flerförgrenat F9–F12-probe-svep.** Pausa ytterligare grafikkernel-forskning tills användaren har valt vilken kompromiss de föredrar, eller har uttryckligen avgränsat att de vill lägga **EN sista** forskningsmikro på bevisning trots att det inte garanterar ett spel. Inga fullspelsfunktioner skall byggas i förtid mot en oföränderlig icke bevisad spritekernel.

**Bevara hela originalet.** Originalets 57 beslut och skisser, senare LM-D/Issue6, alla frysta ROMs, G1–G4 underlag och G5-bedömningen kvarstår oförändrade. Ingen gamla positiva/negativa bevis raderas. Huvudchattens nästa verkliga uppgift efter ett användarbeslut är ny, uttryckligen begränsad roadmap och separat rollordrade prov.

*Dokumentattest: MAIN VI, rådgivande produkt-/feasibility- och authority-gräns, inte användarsignerad canon.*
