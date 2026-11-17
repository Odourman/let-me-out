# LET ME OUT! – G5O / MAIN VII: strikt S1-Y-separation ger blockerad jakt i förenklad dynamisk skärm
**Datum:** 2026-11-17. **Klass:** `MAIN_GATE_SOURCE_ONLY_EXPLORATORY_NEGATIVE_SCREEN`. **Inte** AI-implementation, officiell RESEARCH II-verifiering, kod-/ROM-prov, Stella/G0, spelcanon, G5-PASS, ny G6/F12-auktorisation eller PR-merge.

## 1. Syfte och källauktoritet
Efter [G5N:s statiska 5-startskontroll](G5N_MAIN_VII_S1_FIVE_NPC_LANE_START_AUDIT_AND_SCORE_PROPOSAL_2026-11-17.md) måste MAIN pröva den största kvarvarande gameplayrisken: **kan fem individuella fiender fortsätta jaga när deras 9-radersband aldrig får överlappa?** Denna G5O är en **förhands-/varningsscreen** för ett enda avsiktligt enkelt chasebeteende, inte ett optimerat Berzerk-/Let-Me-Out!-AI-alternativ.

Styrande original: [57 beslut, originalarkiv](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), särskilt 008 (lika AI/hastighet/kollision), 019–025 (dörr, nåbara nyckel-/NPC-platser, spawn/nyckelbärare), 032 (4 rörelseriktningar, söker spelaren), 033 (undviker väggar och varandra), 034 (litet slumpinslag), 043–047 (poäng). Originalmaskerna är [fyra TOP-DOWN 8×9](../design/NPC_REFERENCE_8x9_masks.json). 
Kartkälla: [v0.11 A01/B01/C02/D01, 40×22](../design/PLANERADE_RUMSKARTOR_V011.json). V0.19 exakta OPEN-kartor är fortfarande kandidater; deras gameplay har **inte** testats här.
Renderingsreferens: [G5K, 176-raders conditional S1](G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md), [G5L:s S05-same-Y key+NPC+door](G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv), [G5:s bindande gräns](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md). **O1 har senare godkänts endast för fysisk android/nyckelöverlappning**, enligt [LM-D06](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md); ingen generell same-Y-bortskymning eller 10Hz-flimmerwaiver.

## 2. Exakt avgränsad modell – inte riktig spel-AI
- En gridcell motsvarar offline-fotankare; ett NPC-/spelarfotankare kräver 2×2 helt öppna `.`-celler. Detta är en **approximation**, inte verklig 8×9-mask + 6×6-hitbox eller ROM-kollision.
- Fem förhandsvalda **test**-startuppsättningar tas ordagrant från G5N:s exempel:
  - A01: `[14,3];[9,6];[14,9];[9,12];[14,15]`.
  - B01: `[9,3];[14,9];[35,13];[9,15];[35,17]`.
  - C02: `[14,3];[9,6];[14,9];[14,15];[4,18]`.
  - D01: `[14,3];[9,6];[14,9];[9,12];[14,15]`.
- Spelaren hålls **avsiktligt stilla** vid tre öppna kartankare `(2,10)`, `(19,10)` och `(34,10)`. Detta testar efter-startad jakt mot olika sidor; **inte** riktig spelarcontroller eller spelmoment före första skott.
- Kör **180 modell-ticks**, varje tick ett uppdateringsförsök per NPC. Varje NPC föreslår något av fyra angränsande fotankare (ordning upp/ned/vänster/höger). Beräkna kortaste fyrgranne-BFS-avstånd till spelaren över 2×2-öppna ankarceller. Godta endast steg med **strikt lägre** BFS-avstånd; vid flera alternativ sortera på minst avstånd, sedan minst vertikalt avstånd till spelaren, sedan ursprunglig riktningsordning. Fiendeförsökens ordning roteras med `(j+tick) mod 5`.
- **S1-hård regel i varje mellanläge:** `abs(y_i-y_j) >= 2` för alla olika NPC. I G5N:s approximation betyder detta 16 scanlines mellan startankaren så två 9-radersmasker inte upptar samma pixelrad. Om inget av NPC:ns avståndsminskande grannsteg är tillåtet står den still. Ingen långvägsväntning, grupprörelse, slump, diagonaler, AI-omplanering eller byte av Y-ordning prövas.
- **Särskilt svaghet hos jämförelse utan S1:** om Y-spärren kopplas bort tillåter algoritmen **alla fem NPC på samma fotankare**. Den körningen är bara en matematisk referens för avståndsgradienten, inte en fungerande fri-AI som uppfyller NPC/NPC-kollision. Jämför alltså **inte** dess 5/5 som ett giltigt spelalternativ.
- Ett NPC räknas `near` om dess **BFS-avstånd till spelarens ankare är ≤1 efter tick 180**. Det är ett abstrakt mått, inte träff/angrepp/kollision eller spelardöd.

## 3. Resultat – tolv testfall och konkret negativ signal
Full maskinläsbar resultatmatris med samtliga NPC:s sluttider/slutpositioner, BFS-avstånd och antal blockerade gradientförsök:
[G5O 12-case CSV](G5O_HARD_LANE_GREEDY_CHASE_12_CASES_SOURCE_ONLY_2026-11-17.csv).

| Rum | Spelaren x2/y10 | Spelaren x19/y10 | Spelaren x34/y10 | Tolkning i denna modell |
|---|---:|---:|---:|---|
| A01 | **1 av 5 nära** | 1/5 | 1/5 | Fyra fiender stannar minst två/flera gridsteg bort |
| B01 | **0 av 5 nära** | 1/5 | 1/5 | En scenario med komplett misslyckad närförföljelse |
| C02 | 1/5 | 1/5 | 1/5 | Samma begränsningsmönster |
| D01 | 1/5 | 1/5 | 1/5 | Samma begränsningsmönster |

I **12/12** scenarier hamnar högst **1 av 5 NPC** på BFS-avstånd högst 1 från ett stillastående spelarmål; i **1/12** (B01, spelarankare 2,10) når **ingen** dit. Av totalt 9 126 möjliga **avståndsminskande stegförfrågningar** blockerades 8 513 av den hårda Y-avståndsregeln, ofta på samma slutposition under många upprepade ticks. **Detta är endast en räknare i denna naiva modell**, inte mätt spelprestanda eller förväntad blockeringsfrekvens med bra AI.

**Tolkningsgräns:** Resultatet bevisar inte att S1 i alla tänkbara implementations-/AI-varianter har samma problem. Mer sofistikerade regler, andra startuppsättningar, spelarrörelse, långvägsplanering och andra kompensationsmekaniker har **inte** testats. Det visar däremot med ett konkret motexempel att **statiskt Y-separerade startpositioner i G5N inte räcker för att legitimera en produktlösning med strikt Y-constraint och närjakt**. För fem fiender kan spelupplevelsen ändras avsevärt även om rasterägarmodellen blir enklare.

## 4. Beslutskonsekvens – S1 är fortsatt kandidat, inte acceptans
**MAIN-rekommendation efter negativ screening:** godkänn **inte** den enkla hårda S1-varianten som en tyst canonändring eller antagen G5-PASS. Innan användaren ombeds välja S1 bör RESEARCH II få ett avgränsat **rådgivande source-/offline-uppdrag** att jämföra (a) en förbättrad dynamisk Y-separation med ordnade grupper och aktiv omplanering, (b) temporär same-Y med uttrycklig kontrollerad renderings-/flickerstrategi som är **NY policy och EJ godkänd**, och (c) G5-S0 fritt X/Y som högriskkontroll. Redovisa vilka konkreta AI-/key-/door-krav 008/019–025/032–034 vardera bryter eller bevarar.

**S05 kvarstår:** 1 vit NPC + stilla gold key + låst orange högerdörr på samma Y, samt gul player/M0/PF, saknar verifierad integrerad kernel. Nyckel kan stanna på den dödade bärarens plats och får inte flyttas eller döljas godtyckligt av designen. O1:s **godkända skymning gäller bara faktisk pixeltäckning**.

**G5M poäng är separat:** MAIN:s -30 per kill-förslag är fortfarande **endast ett förslag**; originalet -25 gäller tills användaren uttryckligen godkänt ny poängpolicy. Fem slumpade spawn och 1/5 key-bärare är framtida beroenden, inte ändringar av originalbeslut eller historiska R1=6/R2=5+key.

## 5. Tydlig Research II-handoff, utan påstått utfört specialistarbete
**Föreslaget avgränsat uppdrag:** ny `G5O-R` rådgivande AI/source-only-studie som först reproducerar G5O:s 12 fall och testar fler startuppsättningar, rörligt spelarmål, och varierade chase-algoritmer för de fyra källvalda v0.11-rummen; utveckla dessutom en **förregistrerad kart-/spawnoberoende** testmatris för v0.19 OPEN-kandidater (utan att upphöja dem till canon). Varje motexempel ska visa: spelplan/version, start- och mål-X/Y, antagna 8×9 visuella Y-band, vägg-/NPC-kollision, om key/drop/door kan nås och exakt vilken regel som kompromissas. Separata R2/S05-key+door-stressfall, både med och utan faktisk pixelöverlappning. Beskriv kostnad för standard-F6/NTSC utan att bygga ROM. Researchresultat är rådgivande, MAIN tar framtida designbeslut **endast med användaren**.

Detta dokument **utfärdar inte någon G6/ROM-arbetsorder**, påstår inte att RESEARCH II redan har utfört G5O-R och ersätter inte separat auktorisation/acceptans. MAIN kan lämna detta som uppdragsunderlag till RESEARCH II.

## 6. Exakt stoppgräns och status
- **G1–G4:** tidigare avslutade source-only; historisk dokumentation orörd.
- **G5:** teknisk arkitekturforskning dokumenterad och G5O preliminär negativ dynamisk risk-screen; **formellt design-, poäng-/spawn-/kartval saknas**. Ingen G5-PASS.
- **G6/F12/G7–G10, ROM DEVELOPMENT, oberoende VERIFICATION, PR-merge:** **inte auktoriserade här**. Ingen .asm/.bin/Stella skapas av denna studie.

Denna screening ändrar **inte** dina spelregler, poängtal, NPC-masker, rumskartor, kod, original-57-beslut eller godkännanden.
