# LET ME OUT! – MAIN VI: FEM ANDROIDER, BERZERK OCH VIDEO CHESS – RESEARCH CANDIDATE
**Datum:** 2026-11-17. **Status:** RECORDED_CANDIDATE_DIRECTION_NOT_CANON_NOT_IMPLEMENTATION_AUTHORIZATION.

## 1. Användarens egna förslag – arkiverade utan att omtolkas som godkänd canon
Användaren frågade varför *Let Me Out!* bedömts så mycket svårare än faktiska avancerade Atari 2600-spel såsom *Berzerk*, **utan Supercharger eller tilläggshårdvara**. Därefter föreslog användaren:
- **Fem androider i stället för sex**, exakt **två stora män, en stor kvinna, en liten man och en liten kvinna**. Alla fyra befintliga originaltyper kvarstår.
- **Undersök om nyckeln och dörren kan samsas via Video Chess/Venetian Blinds:** interleave varannan rasterrad när deras Y-band och TIA-register faktiskt konkurrerar. Tekniken skall jämföras med enklare återanvändning vid olika Y och med en möjlig playfield-/PF-dominerad dörr.
- Bedöm möjligheten till **Berzerk-liknande design av rasterkernel och spel-/objektrörelse tillsammans**, inte bara fler förkompilerade spriteprofiler.
Användaren sade därefter: "Ok, kom ihåg det här. Uppdatera till google drive och github."

**Tolkning:** användaren gav ett **uttryckligt bevarande- och dokumentationsuppdrag**, men sade inte uttryckligen "ändra vår canon nu till fem". Femandroidsversionen och en ny dörr/nyckelrendering är därför **prioriterade forskningskandidater**, **INTE** redan beslutade ändringar, ingångsvärden för framtida ROM eller en automatisk G6/F12-order.

## 2. Skillnad mellan fryst 6 och föreslagen 5

| Resurs / scen | Gällande sexandroidsversion | Kandidat om användaren senare godkänner fem |
|---|---|---|
| R1 vita NPC | 2 stora M, 2 stora F, 1 SM, 1 SF = **6** | 2 stora M, 1 stor F, 1 SM, 1 SF = **5** |
| Samtliga fulla 8-bitarsfigurer med gul spelare | **7** logiska figurer | **6** logiska figurer |
| Efter en nedskjuten nyckelbärare R2 | **5 NPC + guldnyckel** | **4 NPC + guldnyckel** |
| Minsta individuella numeriska NPC-X/Y-lagring | 12 byte | 10 byte |
| Acceptanskriterier C01/C02/C04 | Fortfarande **6 och 5+nyckel** | Skulle behöva separata uttryckliga ändringar; inga ändringar har gjorts |

**Bevara alla fyra låsta originalmasker** i design/NPC_REFERENCE_8x9_masks.json oförändrade. De är 8x9 TOP-DOWN; maskfilens Git-blob SHA1 är 058800a4c1904d1ff289e7e61b3902aa111ba16d.

### Kvalificerad teknisk nytta
Fem i stället för sex tar bort ett helt logiskt 8-bitarsobjekt ur den värsta samma-Y-situationen, kan minska positions-/grafikhändelser, frigöra minst 2 byte för X/Y och lämna färre fiender när nyckeln syns. Det är **en reell förbättring, ingen PASS**: TIA har fortfarande bara två 8-bitars playerströmmar; P0/M0 delar färg, NUSIZ0 kan också kopiera M0, 76 CPU-cykler gäller på varje rad, brown PF och key/door behöver egna deadlines.
F10:s tidigare villkorliga sex-P1-kopiors kostnad var 61/76 CPU-cykler utan många verkliga krav. Att subtrahera en illustration med 3 c RESP + 3 c GRP + 2 c omedelbar mask ger en modell 53/76; det är **inte ett fungerande femandroids-RAM-X/Y-schema** eller en timingmätning för vår P0/P1-kernel. R1g visade 4 original-NPC plus player med fyra förbyggda X-lägen för fjärde och M0 på en rad före NPC, inte 5 fria numeriska X/Y och aktiv M0 samma Y.

## 3. Vad Berzerk faktiskt styrker – och vad det inte styrker
Berzerk på ursprunglig Atari 2600 visar att labyrint, många logiska robotar, skott, spelare, jakt och poäng/liv kan göras som ett kommersiellt fungerande spel. **Det är relevant motbevis mot att spelets funktioner i allmänhet skulle vara för avancerade.**
Nyckeln till jämförelsen är **renderingens samspel med robotgrafik, spawn/rörelse och TIA-multiplexning**. Verifiera historiska uppgifter om *Berzerks* eventuella tvålinjers-, vertikala passerings-/sorterings- och flickerregler mot tekniska källor, ROM-observationer eller originaldisassembly innan någon detalj får användas som bindande spelarkitektur. **Det är inte bevisat** att Berzerk stödjer våra fyra nio-raders TOP-DOWN originalmasker, fem fritt numeriska X/Y, guldnyckel, en orange högerdörr och M0 med samtidiga överlapp på samma rasterrader.

## 4. Video Chess / Venetian Blinds som prövning för key + door
**Teknikprincip:** växla ritansvar mellan olika objekt på omväxlande vertikala rasterrader i samma höjdband, i stället för att kräva deras fullständiga grafik på varenda rad. Video Chess ger historisk referens för tekniken.

**Tre jämförbara tekniska kandidater:**
- **K1:** nyckel och dörr på olika vertikala höjder: återanvänd samma TIA-objekt på olika scanlines, utan Venetian Blinds.
- **K2:** verkligt samtidigt Y-band: dela rasterrader enligt Venetian Blinds för dörrdetaljen och nyckeln, mät färg/hål/läsbarhet. En 9-radersmask får bara 4 eller 5 egna rader om den delas jämt över en frame; risken för randighet och förlorad nyckel-/nyckelhålsform är konkret. Växlande frames har en annan flimmerrisk.
- **K3:** låt stationär högerdörr bäras mest av **PF** och nyckelhål/orange detalj av bara den minsta nödvändiga spritetiden. PF-vänsterkanten måste fortsatt vara stängd och PF brown; den historiskt isolerade R3-dörren använde P1 och bevisar inte en ny K3-layout.

**Viktiga gränser:** guldnyckeln kan ligga var som helst, inte bara vid dörren; O1 får skymma den logiskt stationära nyckeln under android men den skall återkomma exakt där; dörrens orange/svarta form är ett separat designmål. Att key och door kan dela P1 säger ingenting om hur fem vita NPC och player kommer dela P1 på samma Y. Tidigare negativa Venetian-blinds-/VDEL-prover T06/T07 för originalandroidmaskerna **bevisar inte** att K1–K3 är omöjliga för key/door, men markerar risken för maskförlust.

## 5. Ny rekommenderad researchprioritet – endast RÅDGIVANDE
1. Gör en **källbaserad Berzerk kontra Let Me Out! renderingsjämförelse**, skilj faktiskt verifierade register-/rastertekniker från forumpåståenden. Kopiera inte kommersiell Berzerk-ROM-kod till projektet.
2. Gör en **femandroids- 76c/TIA/colorclock/RAM/F6-matris** med verkliga originalmasker. Ta med full numerisk X/Y, samma Y och närliggande Y, player, M0 och brun PF. Redovisa varför det som fungerar i R1g är ett snävare bevis.
3. Gör en **K1/K2/K3 source-only kontrast** för guldkey och orange/svart dörr – definiera förlust av ursprungsrader, synliga nyckelhåls-/guldpixlar, PF-asymmetri och om P1-trafiken kan samexistera med NPC.
4. **Lägg fram en ny fråga till användaren** före varje förändring av sex→fem, visuella waivers eller acceptanskriterier. Håll Atari 2600 standard-F6 som levande researchkandidat, men utlovas inte som färdig produkt förrän verklig full scen kan visas.
5. Ingen ny G6/F12/ROM-, GRAPHICS-implementation eller oberoende E02-verification genom detta dokument.

## 6. Auktoritetsordning och källor
- Projektets aktuella [CURRENT_PROJECT_STATE](CURRENT_PROJECT_STATE_2026-11-15.md) och [G5 decision boundary](gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md) är fortfarande statuskällor.
- [ROM_GATE_V018_ACCEPTANCE](ROM_GATE_V018_ACCEPTANCE.md) C01–C04, [R1–R4 scope](ROM_GATE_V018_SCOPE.md) och [NPC originalmasker](../design/NPC_REFERENCE_8x9_masks.json) är **inte ändrade**.
- [Research: exakt 30 Atari-trick](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), #01 multiplex, #03 Venetian Blinds, #04 flimmer; historiska negativa prov och källor.
- [G2 raw audit](gates/G2_COMPLETION_RECEIPT_AND_FEASIBILITY_BOUNDARY_2026-11-17.md), [G3 resurskontrakt](gates/G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md), [G4 microhypotes](gates/G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md).
- Externa forskningsuppslag: https://forums.atariage.com/topic/182923-explain-sprite-theory-please/ ; https://forums.atariage.com/topic/272616-medium-spaced-6-sprites-with-color-graphics/ ; https://spectrum.ieee.org/atari-2600/atari-s-competition

**Klassning:** MAIN:s spårbara notering av användarens nya förslag. Projektcanon och implementation **PENDING uttryckligt senare beslut**. Memory ensam är inte projektauktoritet.
