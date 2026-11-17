# LET ME OUT! – MAIN VI G5K: BERZERK-Y-BAND + DYNAMISK P0/P1-ÄGARFÖRDELNING VID HÖGERDÖRREN
**Datum:** 2026-11-17. **Status:** `G5K_SOURCE_ONLY_176_LINE_CHANNEL_ASSIGNMENT_PASS_CONDITIONAL_Y_POLICY_G0_NOT_PASSED_G6_NOT_AUTHORIZED`.
**Syfte:** Fortsätta G5 efter att G5J funnit original-Berz​erks faktiska Y-arbitrering. Detta är en **ny, positivt formul­erad arkitekturhypotes** som kombinerar Berzerk idén, vår tidigare frysta **G4 H4-ONE P0 player+white**-mikrofysikfråga, isolerad **R3 orange P1 door med samma svart utskurna keyhole**, och G5G **speglad PF+Ball vänstervägg**. Utför endast källanalys och deterministiskt offline-registerägarprov. **Ingen användare har godkänt begränsad Y-rörlighet, key O1-avsteg, skottfärgskompromiss eller G6/ROM-kodorder.** Därför blir detta inte v0.18 ny canon och INTE G0-pass.

## 1. Källkedja och ny syntes
- [Berzerk original 2600 dissasembly, pinned `480a528...`](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm), **`MAX_ROBOTS=8`** (L214), **`H_ROBOT=9`** (L199), init Y=75,65,...5 (L1826..1839 och 2093..2109), en aktiv P1-robot per vertikal kernel-sektion (L401..524), rörelselås vid närhet till grannar (L1323..1367). Detta är källbevis för en annan verklig speldesign än fem fullständigt Y-fria NPC; source lästes men inte omkompilerades eller kördes.
- [G4:s H4-ONE och konditionell GO, source only](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md): kritiskt obevist är `P0 gul player + vit original-NPC` i båda X-ordningar, `M0` samma aktiva Y och bruna PF.
- [R3 isolerad rätt högerdörr med orange P1 och svart inmaskat nyckelhål](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md): **P1 door när låst**, öppnar endast höger och tar bort nyckelhålet samtidigt; R3 är DEVELOPER_LOCAL_PASS separat, inte fullspelspass.
- [G5G spegel-PF + Ball x0](G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md): 3520/3520 offline väggceller; fysisk BL-position/kollisionsbeteende ännu oprövad.
- [G5J källanalys med Berzerk](G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md): riktig Y-lane måste ändra fri Y och Berzerks 2LK får inte okritiskt dubbla vår oförändrade 8×9-höjd.

**Ny arkitektur H5K (ej godkänd spelregel):**
- **Utanför y för dörr:** P0 reserverad åt **gul spelare**, P1 återanvänds för **högst EN** vit original-android på samma scanline. M0 fortsatt EN aktiv projektil, PF brunt, BK svart.
- **I 32-raders dörrbandet när dörren är låst:** P1 reserverad åt den **orange P1-dörren** (svart genomskinligt nyckelhål som del av bitmapen), som i R3. Om en vit robot behöver synas samtidigt används **P0** för roboten och spelaren (både X-ordningar måste stödjas). Detta byter **P0 registerägarschema vid Y-bandsgränsen** i stället för att tvinga P1 till white→orange varje scanline.
- **Efter nyckelbärarens död** (R2-kandidat fyra kvar + gold key): i det dödade objektets tidigare Y-band kan guldnyckel teoretiskt ta samma gfxslot, om ingen annan aktör samtidigt vill använda den. I dörrbandet blir P0=player+key, P1=door, men gold/yellow-växling och M0 ger ytterligare färgrisk.
- **Ball x0** brunt och speglade PF0/1/2 antas hålla dörrens bakgrund enligt tidigare 3520-cellsmodellen. BL upptaget som vänstervägg och kan **inte** samtidigt användas för key i samma Y-band.

**Sammantaget:** P1 behöver aldrig på SAMMA rasterrad generera både white robot och orange door i den **icke överlappande lanemodellens R1-fall**. Detta är ett större tekniskt framsteg som source-only arkitekturförslag än tidigare G5H:s försök att få P1 att rita 3–4 robotar PLUS dörr.

## 2. Reproducerbar 176-raders offline-rasterägarrevision
[**G5K – alla 176 rumsscanlines med P0/P1-owner för R1 och ett villkorligt R2-nyckelfall (CSV)**](G5K_LANE_DOOR_DYNAMIC_CHANNEL_R1_R2_176_ROW_OFFLINE_ASSIGNMENT_2026-11-17.csv).

**UTTRYCKLIGT ICKE-CANON-testfall**: fem NPC med originalmaskfysiskt höjdband 9 rader och rumsrelativa Y-start `[20,44,68,92,116]` (M1,M2,F,SM,SF), historisk C02 32-door-band y80..111, gul player antas grafiskt kunna täcka varje Y. Scenario efter slumpad nyckelbärardöd: den fjärde figuren (SM i denna exempelindexordning) har försvunnit och lämnar en guldkey med samma `Y=92..100`; de fyra andra NPC behåller sina X/Y. Detta är enbart en syntetisk **bevismodell för kanalägande**, inte ett löfte om slumpad bäraridentitet, korrekt key-bitmapp eller full O1.

| Reproducerbar modellparameter | Offline-observation |
|---|---|
| Rumsdel 22×8 | **176** analyserade scanlines |
| Fem 9-raders original mask-band | **Max 1** vit NPC-samtidighet per scanline, **0** rader med två vita bandsöverlapp |
| Dörr 32 rader y80..111, NPC 4 y92..100 | **9** rader med **NPC och dörr samtidigt**; falsifierar alla påståenden att deras Y alltid skiljer |
| R1 när dörren låst: P0 bitmapowners | Max **2** (player + 1 robot), i det villkorade demo-Y-bandet |
| R1 när dörren låst: P1 bitmapowners | Max **1** (door eller 1 robot) |
| R2 död NPC4 → 4 NPC + guldkey på Y92..100, utan övriga NPC i samma Y | Max **2** 8bits P0-owner (player + key), max **1** 8bits P1-owner (door eller en NPC/key), endast **för detta syntetiska fall** |
| Dörr ↔ guldkey på samma Y | **9 rader**; detta är den verkliga motsatsen till att nyckeln och dörren aldrig skulle behöva dela rasterhöjd |

**Vad AUDIT PASS betyder:** Alla 176 rader följer de just införda TESTANTAGANDENA, med max två 8bitars P0 och ett P1. Det validerar endast en **logisk kanaltilldelning efter beslutade Y-gränser**, inte att TIA faktiskt kan rita 2 P0 på fri numerisk X med korrekt Y, färg och M0; inte att vi får begränsa NPC:s Y. Det är alltså *source-only ASSIGNMENT PASS*, inte G5 användardesignbeslut/G0-pass/G6-ROM-pass.

### 2.1 Cykelkostnad i minimal direktinstruktionsmodell, EJ fysisk G0
Oförändrade jämförelseantaganden från G5G/H: en synlig 8bitarsaktör med `LDA #imm`2 + `STA GRP`3 + `STA RESP`3 = **8c**. `COLUPx` färgpair `LDA#;STA`=5c. `WSYNC`=3c. Tabellen är **inte** komplett runtimeberäkning och **inkluderar ej** giltig SRC X/START/latch, masktabell, M0-ENAM, PF register-delays, Ball x0 och nuvarande gameplay/collision.

| Scenario | Teoretiska opcodes | Modellcykler / 76 | Status |
|---|---|---:|---|
| Utanför door: P0 player, P1 en vit NPC, oförändrad PF | 2×8 + 3 | **19/76** | Stor återstående aritmetisk budget, G0 fysisk ej visad |
| Inom door: P0 player + 1 vit NPC, P1 orange-door, P0 färg två växlingar | 3×8 + 2×5 + 3 | **37/76** | Passar tidigare G4 P0 korsning som fortfarande ej validerats |
| Door/BL bandgräns: dessutom PF0 samt ENABL aktiveras / återställs | 37 + 2×5 | **47/76** | Ej inkluderad BL-positionering |
| Svår enskild PF-map-change-rad med tre nya PF-byte | 47 + 3×5 | **62/76** | Bara 14c kvar för all verklig ytterligare hårdvaru-/datakostnad |

**Det avgörande är inte 37c i sig, utan att **P1:s originalpositionerade orange port kan behållas där den redan är demonstrerad**, utan samma-Y vit P1 om vi Y-lane-placerar roboten på P0 under dörren. Den nya risk som tar dess plats är **P0 gul/vit/gul-färgretriggning och M0 samtidigt**, dvs precis G4:s öppna grundprimitiv, vilket knyter forskning till förberedda steg.

## 3. Fysiska stoppvillkor och design-/O1-problem som aldrig får gömmas
1. **Fri Y vs Y-lane:** Våra ursprungliga logiska NPC är individuellt Y-rörliga. Berzerk-liknande **hård avståndsregel om minst 9 rasterrader** betyder att vissa NPC inte får följa spelaren eller gå förbi varandra vertikalt. Det kan ändra patrull, jakt, kartpassage och spelkänsla. **Kräver uttryckligt userbeslut** före ändrad canon/implementation. Kan inte antas av "fortsätt".
2. **Spelar-korsning:** P0 player och vit NPC måste kunna byta X-ordning i båda riktningar; G4 H4-ONE är bara villkorat SOURCE-ONLY, ingen faktisk fungerande numeric-X P0-mekanik bevisad. M0 delar COLUP0; om skottet skall vara gult och NPC vit på **samma färgklocka** kan båda färgerna inte visas med samma register. Nya hidden X vid ROM-merge och fysiska TIA counter START måste förregistreras.
3. **Enkelt dörr-P1 betyder inte integrerad R3-pass:** Vid byte av P1-owner mellan Y-zoner måste P1 återpositioneras till rätt white-X eller door-X utan glömd GRP0/GRP1/VDEL, med `RESP1/HMOVE` under verkliga blankings/deadlines och P1-door x~152 på samma originalrader. R3 ROM visade statisk port, **inte** denna runtime Y-bankväxling.
4. **Guldnyckeln och dörren kan vara på samma Y:** Original O1 anger att nyckeln finns kvar på den dödade bärarens plats när den blir tillgänglig. Om bäraren dör i dörrbandet måste guldnyckeln också kunna visas där. G5K's synthetic killed NPC4 demonstrerar **9 rader door+key**, och väljer P0 key+player, men gul/guld färg och aktiv M0 är ny risk.
5. **R2/O1 KEY OCCLUSION kan bryta slot-antagandet:** Om en annan robot senare skymmer nyckeln med korrekt O1 måste båda vara logiskt kvar och ritregeln hantera skymning; global Y-lane som också förbjuder fiender att korsa KEY:s y skulle göra det omöjligt att spela upp O1:s avsedda occlusion-situation. **Inget O1 PASS**, och en sådan tyst policy är förbjuden.
6. **Ball dörrvägg x0:** BL är upptagen som vänster gräns i dörrband, bitmodell 3520/3520 men fysisk `RESBL` och kollisionslatchar ännu ej testade. Villkorad.
7. **Aktiv mapper:** standard F6 fyra 4K aktiva bankkoder, 128-byte RIOT, 76c varje NTSC-linje, original 8×9 höjdrader på *en* rasterrad var. Berzerks tvålinjekernel är **en annan visuell höjd**, måste inte följa med.
8. **No flicker waiver:** Endast om användaren senare godkänner separata regler kan displaylista/flicker få tjäna som reserv; ingen 10Hz "visning" får utges för all 5 NPC simultant originalrättvänt.

## 4. Hur detta relaterar till den verkliga G1–G10-planen
- **G1–G4** redan färdiga i dokumentation; G4 villkorad H4-ONE går på **P0 player+white + M0 same Y + PF**. Den mikroförberedelsen är nu konkret relevant som **grundmekanik just i den låsta dörrens Y**. G5K:s ett-robot-per-Y-spår kräver inte att man *startar* G6 eller återanvänder ett oauktoriserat gammalt G6-orderutkast. Original-G4 mikro med två P1 vita utanför dörr är visserligen starkare på P1 än vårt en-robot lane-läge, men det kan inte ersätta ett oberoende 5-NPC game-PASS.
- **G5**: Ny *redovisningsbar positiv kompromisskandidat* med explicit TECH-vinst och explicit Y-mobilitetskostnad. Vår **formella G5-designcutover är fortfarande PENDING USER**, inte ett avslag på användarens fem-/svart-/nyckelhålsval.
- **G6**: När användaren senare uttryckligen godkänner en tillräckligt precis ROM-mikroorder och dess Y-policy, är första fysiska preflight **P0 gul ↔ vit same-Y X-order + en M0 och äkta brun PF**, och separat P1 statisk låst orange-door mellan band, före full kombination; **ingen ny G6 beställd nu**.
- **G7–G10**: Senare, *separata* rättningar av ursprunglig sex-NPC-grind till formellt auktoriserad femfiendersversion, R2 key/O1, R3 door, R4/E02 och gameplay. Research II rådgivande; ROM DEVELOPMENT III endast authorized coding; VERIFICATION II oberoende på fryst commit.

## 4A. Officiellt arkiv och fullständig rad-/kanalbilaga
- [Google Drive – G5K, full text och 176-raders R1/R2-kanal-CSV](https://docs.google.com/document/d/1OuqluwyUycObf-tB27SoN-kKaqvwVUWbdmUal7oqB60/edit), lagrad i officiell projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u` och läst tillbaka; kontrollerat 37/76, 62/76, key+door 9 rader och sista rad 175. GitHub originalkälla är versionsstyrd och inte en implementationsorder.

## 5. Källa, leverans och stopp
- [G5K logisk 176-scanline/6-fält-ägarlista](G5K_LANE_DOOR_DYNAMIC_CHANNEL_R1_R2_176_ROW_OFFLINE_ASSIGNMENT_2026-11-17.csv).
- [G5J Berzerk primärkälla/24+36 vs lane](G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md), [G5H direkt-test FAIL](G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md), [G5I kanonisk planavstämning](G5I_PLAN_RECONCILIATION_FIVE_NPC_DECISION_READY_NOT_G6_2026-11-17.md).
- [Original Berzerk pinned external code](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm).
- [Original isolated R3 fixed P1 door](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md), [G4 H4-ONE](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md).

**Slutklassning G5K:** `SOURCE_ONLY_CHANNEL_ASSIGNMENT_PASS_FOR_DECLARED_SYNTHETIC_Y_BANDS`; **G5_FORMAL_ACCEPTANCE_PENDING**, **G0_RUNTIME_SOURCE_TIMING_NOT_PASSED**, **G6_NOT_AUTHORIZED**, **NO NEW ROM**, **NO E02**. Den underliggande speldesignen med individuellt fri Y har INTE bevisats möjlig under detta schema; kandidatens stora vinst kräver separat synligt användarbeslut om vertikal rörelsepolicy.
