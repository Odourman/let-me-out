# LET ME OUT! – MAIN VII G5R: fem-NPC-rebaseline, poängbalans, nyckelbärare och startpositioner
**Datum:** 2026-11-17. **Klass:** `G5R_SOURCE_ONLY_DECISION_READINESS_NOT_APPROVED`.
**Gräns:** Ingen ny spelcanon, testacceptans, ändrad gameplay-/poängkod, kartcutover, G0/G6/F12/ROM, PR-merge eller oberoende VERIFICATION. Äldre G5Q A1+B1 är redan avgränsat användargodkända designmål; den nya användartexten "Fortsätt Följ dina egna rekommendationer" auktoriserar fortsatt **förberedelse**, men är inte ett entydigt, separat uttryckligt numeriskt beslut om originalets -25-poäng eller ny R1/R2-bas.

## 1. Proveniens och auktoritet
- Originalfilerna har **denna gång lästs direkt från officiella Google Drive-arkivet** [LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view). ZIP SHA256 `f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4`, 21 filer, ZIP-CRC godkänd. Relevant primärdata: `03_DECISIONS.csv`, `02_MASTER_SPEC.md`, `04_SCORE_AND_TEST_CASES.md`, `analysis/score_model.py`. Originalbeslut 005–008, 019–025, 032–034, 042–047. Den äldre sexfiendersmodellen är **fryst historisk auktoritet** där den inte uttryckligen ersatts.
- Senare användarbeslut [LM-D12/A1 och LM-D13/B1](G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) fastställer **fem fritt logiskt rörliga individer** och **rättvist synliga fiender** som kvalitetsmål, **inte** ändrad ROM-testbas eller poäng.
- [G5M tidigare följdanalys](G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md), [G5N startstudie](G5N_MAIN_VII_S1_FIVE_NPC_LANE_START_AUDIT_AND_SCORE_PROPOSAL_2026-11-17.md), [G5P forskningsmottagning](G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md), [G5Q förslag och stoppspärr](G5Q_MAIN_VII_DECISION_READY_DESIGN_TARGET_AND_PRE_G6_BOUNDARY_2026-11-17.md).
- Kartkällor: `design/PLANERADE_RUMSKARTOR_V011.json` (historiskt A01/B01/C02/D01); `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json` (uttryckligen **icke godkända exakta kartor**). Det godkända LM-D04 är **luftig rumskänsla**, inte v0.19-matrisbeslut.

## 2. Originalets verkliga poängsemantik – avgörande för fem NPC
**Master Spec och `04_SCORE_AND_TEST_CASES.md`** beskriver, för sex NPC, en sammanhängande poängmodell:
1. Startpoäng 0 och vid varje dödad NPC: `score=max(0, score-kill_penalty)` **direkt efter varje sådan händelse**, aldrig en dold negativ skuld.
2. Vid verklig nyckelupptagning: `score += 50`; **inte** vid död av key-bärare.
3. Vid **faktisk utgång**, endast en gång: `score += 100 + 15*surviving_NPCs`.
4. Missat skott 0, död före utgång ger ingen ej intjänad rumsbonus; extraliv 500, 1500, 2500 … endast en gång per tröskel.
5. Ursprunglig avsikt 047: "Skjut alla" får återställa från låg poäng vid låg risk men **inte** vara repeterbar highscore-farming. Specen betonar att detta nollgolv är *avsiktligt* och att ändringar inte får göras slentrianmässigt.

Med framtida **N=5** och **k** förstörda, under antagandet att ingen nollklampning behövs:
- Originalstraff `p=25`: `delta=225 - 40*k`; k=1 ger **+185**, k=5 ger **+25/rum**. Repeterbar farming.
- Föreslaget `p=30`: `delta=225 - 45*k`; k=1 ger **+180**, k=5 ger **0/rum**. Originaltanken återställs utan någon ny specialregel för sista fienden.

Vid **ingångspoäng 0**, om alla k dödas *före* key pickup: varje minus stannar på 0 och rumsutfallet är `225 - 15*k`. För k=1..5: **210,195,180,165,150**, **identiskt för -25 och -30**, eftersom minusgolvet klampar. Vid hög poäng och nyckelbäraren uniformt bland fem, om spelaren skjuter tills rätt bärare dödas och lämnar direkt, är medelvärdet av k=1..5: **+105** för -25; **+90** för -30. Det är ett aritmetiskt antagande om slumpad kill-ordning, inte speltest eller faktiskt PRNG-bevis.

### Första fem rum – spelaren skjuter alla fem före nyckel och går ut
Startpoäng `S=0`:
- p=25: **150 → 175 → 200 → 225 → 250**.
- p=30: **150 → 150 → 150 → 150 → 150**.

Slutvärde för varje rum med fullständigt all-kill **före key pickup**:
- p=25: `S_next=max(0,S-125)+150`, vilket för S≥125 är S+25.
- p=30: `S_next=max(0,S-150)+150=max(S,150)`. Detta är **samma önskade no-farming-profil** som ursprungligen bevisades för **sex × -25**, utan att upphäva godkänd golvseffekt vid låg poäng.

**Händelseordningen spelar fortfarande roll**: skjut nyckelbärare → plocka key +50 → skjut övriga fyra → exit kan ge lägre rumsutfall än att skjuta alla fem innan key pickup. Denna taktiska skillnad är *avsiktlig* i originalspecen.

## 3. Nytt reproducerbart source-only poängprov
[Full G5R CSV – 210 händelseordnade utfall](G5R_FIVE_NPC_SCORE_FLOOR_210_CASES_SOURCE_ONLY_2026-11-17.csv).
Detta är en liten ren aritmetikkontroll, **inte en spel-ROM**. Samtliga `2` straff (25,30) × `7` startpoäng (0,40,100,149,150,500,1000) × `15` möjliga kombinationer (kills före key 1..5, kills efter key 0..5-before) = **210 distinkta fall**. Kalkylen applicerar nollgolv **på varje kill** samt +50 vid pickup, +100+15×levande vid exit. När fullt avdrag är möjligt har en oberoende sluten-formel `S + 225 - (p+15)*k` kontrollräknats mot varje eventbaserat utfall. 77 av 210 har ett scenario där det enkla no-floor-formelvillkoret inte är säkert och måste räknas händelsevis.

**Explicit kvarvarande tekniska regressioner efter separat framtida implementationstillstånd:** poäng vid verklig död före exit, olika ordning av shot/hit/death/drop/pickup, K1 nyckel under spelare, E1 exit-vs-kontakt, ett-skott-per-press, miss = 0, alla fem bärare, fem-rums highscorefarming, 500/1500 monotona extralivströsklar och overflow/BCD-score om tillämpligt. Ingen sådan framtida ROM-körning skedde här.

## 4. G5R-C: rekommenderad formell fem-NPC-testbas – ännu inte godkänd
**Föreslagen framtida version, måste få egen versionssatt användaracceptans:**
- R1-fem: **M,M,F,SM,SF**, fem individuella vita NPC med **alla fyra historiska originalmasktyper oförändrade**, korrekt orientering, individuellt logiskt X/Y, original AI/kollision och bestämd NTSC/standard-F6-målmiljö.
- R2-fyra-plus-key: när en av de fem dödas efter nyckelholder-val, **fyra kvarvarande NPC + en fysisk guldkey** efter avslutad dödsanimation. Key-logisk position låst, K1/O1/E1 och andra gällande beslut följs.
- Status för äldre tester förblir uttryckligen **historisk v0.18 R1-sex och R2-fem+key**, inklusive deras PASS/FAIL och filhashar. Ny R1/R2-kandidat kräver separata framtida acceptansscenarier och riktig ROM/Stella. Ingen "renaming" eller retroaktivt PASS.
- Varken G5R eller en kommande rebaseline bevisar fysisk rasterförmåga; S05 same-Y player+white+key+orange P1-door+M0+PF är fortfarande öppen och kan blockera spelets fulla leverans.

## 5. G5R-D: rekommenderad framtida poängpolicy – ännu inte godkänd
**Förslag D1:** -30 per dödad NPC med fem istället för ursprunglig -25 med sex. +50 vid verklig nyckelupptagning, +100 verklig utgång, +15 per överlevande, nollgolv per event, existerande extralivströsklar och originalets taktiska konsekvenser **helt oförändrade**. Användaren måste uttryckligen godkänna just denna **ändring av originalbeslut 043** innan den förs in i designcanon eller kodorder.
**Alternativ:** behåll -25 med fem och acceptera +25/rum för all-kill eller besluta om separat all-kill-specialavdrag; båda kräver egen konsekvensbedömning. MAIN rekommenderar D1 för minimal ändring och starkast bevarad avsikt.

## 6. G5R-E: 5-spawn och 1/5 key-bärare – ännu inte godkänd
**Förslag:**
- För varje framtida beslutad rumskarta, välj exakt fem olika startpositioner ur **rummets förhandsvaliderade pool**, där varje start är gångbar och kan nås enligt **riktig framtida** hitbox, där ingen NPC/NPC-startkollision föreligger och spelaren/key/dörr förblir nåbara. Kartor och kandidater kan inte väljas bara med förenklad 2×2-offline-BFS.
- Alla fem individer M,M,F,SM,SF har **exakt 1/5 sannolikhet** att bära key, **oberoende av masktyp** och utan att låta de två stora männen få en otillåten sammanlagd omräkning som en NPC-typ. Välj bland de **fem instanserna**, inte bland fyra spriteformer.
- Vid 3-bitars slumptal (0..7) är naiv `r % 5` **snedfördelad** (utfall 0..2 har 2/8 var, 3..4 har 1/8 var). Använd t.ex. avvisning av värdena 5..7 på **oberoende uniforma** 3-bitars kandidater, eller annan matematiskt likvärdig metod. Hur faktiskt PRNG-seed/mönster fungerar på 6507 är en **framtida implementationsfråga**, inte här bevisat.
- Nyckel visas **först efter** key-holderns dödsanimation på dennes faktiska fallplats, ligger kvar, robotar kan passera över utan att flytta den, spelaren tar upp den genom kontakt. Godkänt O1 gäller bara faktisk pixelöverlapp.
- Testa future key carriers 1..5, flera initiala startkombinationer, byte av rum utan direkt repetition, dynamisk dörrblockering, oblocked key-åtkomst, spawns nära player, R2/S05 i framtida **separat** auktoriserad ROM-/speltestomgång.
- v0.11 A01/B01/C02/D01 har historiska pooler **20/13/18/15** enligt käll-JSON. V0.19 OPEN-exakta kartor fortsatt förslag. G5N:s strikta Y-separerade femspawnexempel kan INTE tyst införas efter A1:s godkända fria rörelsemål; om de senare övervägs är de bara startstudier, inte låsta Y-lanes.

## 7. G5R-F: kartval avvaktar separat designvisning
LM-D04 redan godkänd: **luftig** rumskänsla. Varken detta dokument eller det ursprungliga tillståndet om fyra rum gör de fyra specifika **v0.19 OPEN** kartmatriserna till canon. Behåll v0.11 som historisk källbas och v0.19 som separat kandidat, tills användaren fått en riktig jämförelse och uttryckligt valt eller delegerat exakt karturval inom ett versionssatt mandat.

## 8. Föreslaget användarbeslut och formell stoppgräns
**A1/B1 (LM-D12/13) är redan godkända; fråga inte igen.** MAIN rekommenderar följande **separata, uttryckligen ännu icke accepterade** val:
- **C1:** Godkänn en framtida *versionerad* testbas R1=fem M,M,F,SM,SF och R2=fyra kvarvarande + key, med historiska v0.18-resultat arkiverade, inte ersatta.
- **D1:** Godkänn `-30` per dödad NPC för just fem-NPC-spelversionen, med alla andra poängregler kvar.
- **E1:** Godkänn fem distinkta validerade starter från vald karta och uniform `1/5` key-bärare per NPC-instans, utan tysta kart-, AI- eller keydrop-ändringar.
- **F:** Exakta v0.19-kartor avgörs **senare separat**; ingen kartcutover genom C1/D1/E1.

**G5 FORMAL:** Kvarstår **öppen** tills C/D/E-vägval har uttryckligt användargodkännande och hårdvarans fortsatta S05-/visningsrisk hanteras i senare särskilt beställda prov. **G6/F12/ROM/ny oberoende Verification/PR-merge EJ auktoriserade** av denna G5R-studie.

**Användarens "Fortsätt Följ dina egna rekommendationer" i detta sammanhang** har här fullföljts genom source-only beredning och verifierad poängmatris, utan att implicit ändra originalets -25/regeln.
