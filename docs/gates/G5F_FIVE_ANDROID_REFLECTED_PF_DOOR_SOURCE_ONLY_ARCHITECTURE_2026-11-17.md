# LET ME OUT! – MAIN VI: G5F fem androider + speglad spelplan + befintlig dörr (SOURCE ONLY)
**Datum:** 2026-11-17 · **Status:** `G5F_SOURCE_ONLY_ARCHITECTURE_REVIEW_COMPLETE_PHYSICAL_RENDERER_NOT_PROVEN`.
**Mandat:** Användarens "Ok, fortsätt" efter övervägande av **fem fiender**, svart bakgrund och en dörr vars svarta nyckelhål är en **del av samma dörrbild**. Denna källstudie är INTE en ny ROM-order, en ändring av historiska v0.18 R1/R2-acceptanskrav eller ett G6/F12-PASS.

## 1. Vad som faktiskt är låst, föreslaget och ännu okänt
- **Användarens uttryckta arbetsinriktning:** fem fiender **2 stora M + 1 stor F + 1 liten M + 1 liten F**, fortsatt normal Atari 2600/standard-F6 som researchmål; spelplanens fria bakgrund **svart**; vägg **brun**; player **gul**; android **vit**; key **guldgul**; endast högerdörr **orange med genomskinligt svart, utskuret nyckelhål i samma bitmap**.
- **Originalgrafik:** `design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, oförändrad. Ny femupplaga tar bort en stor kvinna men inte typidentiteterna. Fem-NPC är ett framtida design-/diagnostikspår. Historisk R1 C01/C04 kräver **SEX**, R2 C02 kräver **FEM + key** tills formellt reviderad; tidigare R1 = BLOCKED/NOT ACCEPTED.
- **Tidigare faktiskt uppnått:** R3 ensam C02-rum med verklig asymmetrisk PF, svart transparent hål i en orange **P1-dörrbitmap**, låst/öppet höger x39 y9–12, 600 × 262 NTSC, **DEVELOPER_LOCAL_PASS** för den *isolerade* R3-diagnosen, EJ integrerad R1/R2/E02. Källa fryst vid `000b6f2a579e4aa96995229b2174884fb7c565e2`, `rom/v018/experiments/r3_c02/TO_MAIN_R3.md`. Dörrhålet tar alltså **ingen separat sprite**; men **hela dörren förbrukar P1 under sina band**. Svart `COLUBK` avlastar ingen extra playerkanal jämfört med annan BK-färg.
- **Inte bevisat:** fem originalmask-NPC + gul player + exakt en aktiv M0/M1 på deras samma 9-radersband + bruna PF i en och samma ROM med numeriskt fri X/Y, frame/mask/färgkorrekt rendering. R1g har max **4** original NPC + player i förkompilerade lägen, M0 **ovanför** bandet. F11 fyra P1 numeriska X misslyckades på **G0 källpreflight**, ingen F11 ROM eller Stella.

## 2. Ny konkret observation från faktiska spelkartor: ALLA är symmetriska utom x39 D
**Källfil:** `design/PLANERADE_RUMSKARTOR_V011.json`, 40×22 tecken × A01/B01/C02/D01. MAIN:s nya deterministiska källaudit beräknade att för **alla fyra** rum skiljer `grid[y][x]` och `grid[y][39-x]` **ENDAST** vid **y=9,10,11,12 och (x=0, x=39)**. Vänster är `#`, höger `D`. Övriga **18/22 logiska rader** är bit-för-bit symmetriska.

| Rum | Normalt speglingsbara rader | Logiska rader med högerdörrsundantag | Antal vänsterhalva-radbyten mellan 22 rader | Distinkta 20-cellsvänsterhalvor |
|---|---:|---|---:|---:|
| A01 | 18/22 | 9–12 | 10 | 5 |
| B01 | 18/22 | 9–12 | 12 | 6 |
| C02 | 18/22 | 9–12 | 12 | 6 |
| D01 | 18/22 | 9–12 | 13 | 6 |

**Teknisk betydelse:** TIA:s `CTRLPF.REF` kan återanvända vänster 20-bitarsmönster för höger 20-bitarsdelen. Då är de **tre sena höger PF0/PF1/PF2-uppdateringarna** som den fulla R3-asymmetriska kerneln gjorde på **varje scanline** normalt inte behövliga. **Tre PF-register håller sina värden** tills de skrivs igen. För en 8-scanline-hög fysisk kartcellrad kan den speglade väggbilden teoretiskt ligga kvar på **sju efterföljande rader** utan någon ny PF-dataskrivning, och även mellan identiska logiska radmönster. Detta sparar eventfönster på många rader, inte bara ROM-bytes.

**Kritiskt undantag: dörrens y9–12.** Med `CTRLPF.REF=1` kommer x39 från samma vänster-PF0-bit som x0. För en **SVART genomsiktlig dörrhålsöppning** måste PF vid x39 vara **0** medan vänster ytterkant x0 är **1**. Teoretiskt kan man skriva **enbart PF0 en gång SENT efter att vänster-PF0 redan ritats men före höger-PF0:s sista pixlar**, återställa rätt vänster-PF0-värde på nästa rad, och låta PF1/PF2 speglas som vanligt. Original-R3 visade höger-PF0-skrivning c37 i sin kernel, men den **nyförkortade PF0-only+REF-schemat är INTE byggt eller cykelverifierat**. Det kräver pixel- och cycle-traps.

**Viktigt:** En svart `COLUBK` skapar inte automatiskt svart nyckelhål om PF vid hålpixlarna fortfarande är `1` och brun. Den orange P1-bitmapens "0"-pixlar kan bara se svarta ut där bakomliggande PF är släckt.

### Varför den här optimeringen är viktig men INTE en gratis full R1-kernel
Original-R3 loggade vänster PF0/PF1/PF2 **c7/c15/c22**, höger PF0/PF1/PF2 **c37/c45/c52**, dörrens `GRP1` **c62** och källestimerad yttersta avslutsrad **74/76**. Att ta bort två sena onödiga PF1/PF2-skrivningar i dörrbandet sparar **minst deras två trecykliga STA-instruktioner på papper (6 c)** om de verkligen kan avlägsnas; men registerhämtning, dataflöde, PF0-återställning, villkor och fysiska deadlines måste **totalräknas från scratch**, inte summeras med en fristående NPC-ROM. På normala symmetriska repetitioner kan betydligt fler PF-skrivningar utebli.
**Samtidighetsbarriären kvarstår:** en viss rad där fem NPC + player + M0 + dörr P1 + PF0-byte alla ska existera kan fortfarande kräva mer än 76 c eller ha oöverbryggbara START-/färgdeadlines. En optimering som bara gör 7/8 rasterrader lätta är INTE ett PASS om den åttonde feilerar.

## 3. Femdjursgrafiken, EXAKT originalmaskanalys, höjdrad 0–8
I ett justerat same-Y-provhöjdband där alla fem TOP-DOWN-8×9 börjar på samma y får tre stora (M/M/F) bitmapdata på samtliga nio rader; de två små (SM/SF) har två `00000000`-rader upptill och en tom rad längst ned.

| Relativ originalrad | Vita NPC med MINST en tänd originalpixel | M/M/F | SM/SF | Belastning inkl. gul spelare om dess bitmaprad är aktiv |
|---:|---:|---|---|---|
| 0 | 3 | JA | nollrad | minst 3 + player |
| 1 | 3 | JA | nollrad | minst 3 + player |
| 2 | **5** | JA | JA | **5 + player** |
| 3 | **5** | JA | JA | **5 + player** |
| 4 | **5** | JA | JA | **5 + player** |
| 5 | **5** | JA | JA | **5 + player** |
| 6 | **5** | JA | JA | **5 + player** |
| 7 | **5** | JA | JA | **5 + player** |
| 8 | 3 | JA | nollrad | minst 3 + player |

**Nytt källauditresultat:** **sex på varandra följande rader (2–7)** behöver alla fem olika vita aktörsobjekt samtidigt, alltså ytterligare gul spelare/skott/PF om scenen stressas korrekt. Det är ALLTSÅ **inte** som om minskningen till fem löste full same-Y-frihet i ett slag. Däremot har vi tagit bort en fullstor kvinna från ALLA 9 rader och från de sex kritiska raderna – fysisk rastervinst.

**Tänkbar men ej universell fördel:** två `large_male` har identiska pixelmasker; NUSIZ-copy kan spara grafik-/registerarbete bara vid särskilda faktiska avstånd. De ska ha fria individuella X/Y och får inte låsas vid 32/64 CC för att få "PASS". Vid generella oberoende X går denna besparing inte att räkna hem på worst-case.

## 4. Konkreta konkurrerande P0/P1-/missile-allokeringar
| Kandidat | P0 playertråd | P1 playertråd | Skott | Huvudrisk |
|---|---|---|---|---|
| **A – MINSTA P0-OMPOSITION** | gul spelare + **1** vit NPC (färg-/RESP-sorteras) | **4** vita NPC | M0 enligt G4, aktivt samma Y | Fryst F11:s fyra numeriska P1-positioner föll G0; en enda vit P0 kräver ändå gul/vit X-sort + skottfärg. PF-mirroring räcker inte automatiskt. |
| **B – MER P0-UTNYTTJANDE** | gul spelare + **2** vita NPC (3 olika X-start/färgfönster) | **3** vita NPC | M0 alt. M1 efter separat kompatibilitetstest | Minskar P1-slotkrav från fyra till tre men belastar P0-kernel, vilket kan krocka med M0-/COLUP0-färg och NUSIZ0. Ingen tidigare ROM bevisar 3 fria P0-start. |
| **C – ENDAST GUL P0** | gul spelare hela bandet | **5** vita NPC | M0 möjligt separat, men P1 tung | F10:s source-only optimistiska 5-P1-radsbudget utan PF/positionering/AI är inte en allmän plan. |
| **D – M1 SOM SKOTT (villkorad reserv)** | som A/B | P1 vita NPC | **M1**, om skottets form/färg och NUSIZ1-kopior tillåter | M1 delar `COLUP1` med vit P1; kan fungera om skottet får samma färg där och korrekt enda missil; konflikter med orange P1-dörr och låst skottvisual måste granskas. M1 är inte godkänt alternativ i historiskt G4 M0-mikro. |

Varken M1, ball eller PF är 8-bitars humanoidbitmap; de kan inte ersätta någon av de fyra låsta formerna utan ett verkligt nytt användarbeslut. `COLUP0` är gemensamt för P0/M0; gult skott över vit P0-pixel på samma colorclock är fysisk tvåfärgskonflikt i just A/B. `COLUP1` gemensamt för P1/M1; vit M1-skott på vit P1 kan eventuellt samägas, men missilkopior och dörr-orange ger andra konflikter. Inga fiktiva extra TIA-kanaler.

## 5. Föreslagna källtester på papper – inte ROM-test och inte G6-auktorisation
**Varje tänkbar framtida ROM ska först passera G0 med verkliga assembler-opcodes och fysiska START-/GRP-/PF-/COLU-deadlines på varje WORST-CASE rad, även rader där PF-tabell precis byts.** Inget råd om "sju lätta rader och en överlastad" får räknas som godkänt.

| ID | Ändamål / tillstånd | Förväntad falsifierbar risk |
|---|---|---|
| **P0: PF normal** | C02, en icke-dörr-cellrad med speglad vänster/vägg + black BK + fem NPC + player + en shot, alla same-Y | För många P0/P1-positioner trots speglad PF |
| **P1: PF radbyte** | samma men första av 8 linjer efter logisk väggradbytesövergång, verkligt nya PF0/PF1/PF2 | Cykelknapphet vid den enda svåra scanlinen |
| **P2: dörrband** | C02 y9–12: x0 solid vänstervägg, x39 PF=0 bakom svart nyckelhål, orange P1-dörr, white NPC och shot same-Y | P1 white→orange samma Y, PF0-right-write kontra GRP1 och M0 |
| **P3: numerisk X–ordning** | en enda källkernel läser 5 oberoende 8bitars X + player X och tillåter *både* NPC vänster/höger om player | Dolda hårdkodade X-lägen, F11 G0 och START latch |
| **P4: tät konflikt** | NPC X=[40,44,48,52,56], player nära, M0 same-Y | Spritebitmapöverlapp/START och obevisad visuell occlusion |
| **P5: NUSIZ copy/shot** | två samma-mask M får tillfälligt kompatibelt avstånd, annat läge godtyckligt och inkompatibelt, exakt EN shot | Otillåten kopieringsberoende renderingsväg eller spökskott |
| **P6: nyckel efter död** | en av fem NPC tas bort → **4 NPC + guldnyckel** + player + shot + brown PF, key kan passeras av NPC utan att dess logiska X/Y ändras | Saknat separat guld-/formband; O1 skymning/restoration |
| **P7: 600 NTSC frames** | efter eventuell separat ROM-auktorisation, 600 × 262, oförändrade 8×9 TOP-DOWN masker, vänster alltid stängd, högerlås/open | Inte källbevis, behöver oberoende VERIFICATION II. |

**P0/P1/P2 är olika *papperstestfall-ID*, inte TIA-register.** I en framtida riktig G0/G1-order ska identifierarna döpas entydigt så att de inte förväxlas med hardware-P0/P1.

## 6. Vad G5F har och inte har uppnått
**G5F SOURCE ONLY – GENOMFÖRT:** En verklig kart-audit för 4×22 rader, exakt 18 speglingsbara/4 dörr-undantag per rum, vänsterhalverings-radbyten A=10 B=12 C=12 D=13; exakta 8×9-källmask-nollrader 3/3/5/5/5/5/5/5/3 aktiva fiender; konkret PF-mirror/PF0-right-only/P1-mask-arkitektur och två alternativa NPC-kanalallokeringar.
**G5F INTE UPPNÅTT:** Källgenererad cykelexakt 6507-disassembly; en verifierad pixel-per-clock PF0-right-only-kernel; fem helt numeriskt fria NPC; riktig same-Y M0; final väl fungerande key; bevis på R1/R2/R3/R4 integration. Det finns **ingen ny ROM eller Stella-data** och ingen independent Verification.
**Falsifierande stoppspärr:** Om full physical G0 timeline inte ger varje obligatorisk normal, radbyte, dörr och same-Y scen en sammanhängande <=76 c med effektiva TIA-latchdeadlines och spel-/maskintegritet, STOP innan kodning och begär användaren välja explicit scope/visuell kompromiss. **G0 kan inte PASSeras med en ren billig PF/door-teorikalkyl.**

## 7. Rekommendation – en nästa beställning när användaren uttryckligen ger den
Fortsätt **på Atari 2600** och använd nu kartornas faktiska symmetri till att minska PF-kostnaden; **håll den fungerande P1-dörrens bitmap + utskuret svart hål som baslinje** i stället för att obestyrkt ersätta den med grovt PF-nyckelhål. Det nya PF0-only/speglingsspåret bör först göra en **ren SOURCE-ONLY G0-fas-/opcodetabell**, för allokering A och B och för verklig dörr/hard same-Y.
Detta är en arkitektur- och stopprekommendation till MAIN; **G6/F12/ROM DEVELOPMENT III får INTE implicit uppdrag** av denna fil. Separat uttrycklig startorder krävs för varje assembly-/Stella-ROM-mikro och för historiska testkriteriers ändring. Ingen automatisk ny canon/mapper/PR7/PAL/E02.

## 7A. Officiell Google Drive-kopia och versionshantering
- [Google Drive: G5F komplett source-only arkitekturanalys](https://docs.google.com/document/d/1PAELvVABaDAVuhZILC1Czo5kEIiRGQV2IaZ1bdtKRNw/edit), skapad som native Google Doc, flyttad till officiell projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u` och läst tillbaka med checks för 18/22, 3/3/5/5/5/5/5/5/3, PF0 och att ingen ROM byggts.
- Denna GitHub-fil är versionsstyrt original och projektets CURRENT_PROJECT_STATE samt G5 beslutsspärr pekar på båda. G5F tillåter bara research/planering, inte code-start.

## 8. Primärkällor
- [Exact 40×22 rooms](../../design/PLANERADE_RUMSKARTOR_V011.json).
- [Original 8×9 NPC masks](../../design/NPC_REFERENCE_8x9_masks.json).
- [C01/C02 and D01–D03 historical acceptance](../ROM_GATE_V018_ACCEPTANCE.md).
- [G3 full R1–R4 TIA contract](G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md); [G3 colorclock deadlines](G3_COLOR_CLOCK_DEADLINES_2026-11-17.csv).
- [G4 physical P0/M0 source hypothesis](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [G2 negative tests](G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md).
- [All 30 tricks reassessed per gameplay object](../MAIN_VI_30_TRICKS_CROSS_OBJECT_REASSESSMENT_2026-11-17.md).
- [User's black-background direction](../MAIN_VI_USER_VISUAL_DIRECTION_BLACK_BACKGROUND_2026-11-17.md).
- [R3 / C02 original developer evidence, historical pinned SHA](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md).
- [Stella programmer's guide: reflected PF, latched PF, four color registers, NUSIZ, 76c](https://www.atariage.com/2600/programming/2600_101/docs/stella.html).

**STATUSKVITTENS:** G5F_SOURCE_ONLY; 5-fiender är användarens föreslagna arbetsriktning, ingen retroaktiv ändring av sex-R1/R2. Slutlig fysisk kernel ännu INTE demonstrerad.
