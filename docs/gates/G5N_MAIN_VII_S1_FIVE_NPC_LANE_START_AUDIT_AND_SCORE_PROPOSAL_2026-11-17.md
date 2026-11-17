# LET ME OUT! — G5N / MAIN VII: fem NPC, Y-separering, kartstarter och poängförslag
**Datum:** 2026-11-17. **Klass:** `SOURCE_ONLY_DECISION_READINESS`; inte ny spelcanon, inte godkända rörelseregler, inte G5-PASS, inte G0/Stella/ROM-test och **inte G6/F12-auktorisation**.

## 1. Uppdrags- och auktorisationsgräns
MAIN VII har efter användarens "Ok, fortsätt. Följ dina egna rekommendationer. Redovisa sedan" fortsatt den redan förberedda G5-käll-/planeringsbedömningen. Detta är stöd för vägval, **inte ett uttryckligt godkännande** av en specifik Y-lane-rörelseregel, ändring av -25/kill, map cutover, kodorder eller PR-merge.

Aktuell prioritet: **G5-S1, Berzerk-inspirerad fiende-Y-separation, som huvudsaklig prövningskandidat**, inte som garanterad slutlig lösning. Alternativen G5-S0 (helt fri numerisk X/Y, olöst same-Y) och G5-S2 (kontrollerat flimmer, ej godkänd specifikation) är bevarade som jämförelsespår. O1 är redan **godkänt enbart vid faktisk android/nyckelöverlappning** (se senare LM-D06), inte generell same-Y-occlusion eller 10 Hz.

Källor:
- [A01/B01/C02/D01 v0.11, ursprunglig 40×22-kartstruktur](https://github.com/Odourman/let-me-out/blob/main/design/PLANERADE_RUMSKARTOR_V011.json).
- [Original fyra 8×9 TOP-DOWN-masker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json).
- [G5J Berzerk-originalkod och Y-separation](G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md), [G5K rasterägarhypotes](G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md), [G5L tio same-Y-stressfall](G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv), [G5M speldesign/score](G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md), [gällande G5-spärr](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).
- [O1 godkänt direkt i MAIN_STATUS_NEXT_10](../MAIN_STATUS_NEXT_10_2026-11-15.md), [LM-D06](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md).
- Analysens live källsnapshot innan skrivning: GitHub main HEAD `92f466a678735c43181dd90cc15576f67876a0e0`. **Endast proveniens**, kontrollera main på nytt före nästa beslut.

## 2. NY liten, reproducerbar SOURCE-ONLY kart-/spawnkontroll
Fråga: Finns åtminstone fem **inledande** NPC-startankare utan vertikal överlappning av 9 fysiska originalrader på historiska kartor? Detta hade tidigare inte systematiskt sammanfattats över alla fyra kartorna.

Algoritm direkt på `design/PLANERADE_RUMSKARTOR_V011.json`:
1. Läs varje `grid`, `candidate_positions` och `player_anchor`. Ett giltigt **offline**-ankare `(x,y)` kräver fyra öppna `.`-celler i `(x,y),(x+1,y),(x,y+1),(x+1,y+1)`. Det är v0.11:s **2×2-fotmodell**, inte faktisk 8×9-hitbox.
2. Gör en fyrgranne-BFS genom sådana ankare från spelarstart x2/y10 och behåll bara nåbara kandidatankare.
3. Räkna oordnade femmängder från dessa punkter där **alla** par uppfyller `abs(grid_y_i-grid_y_j) >= 2`. Varje gridrad representerar 8 visningslinjer; 8 pixlars avstånd skulle överlappa en 9-radersmask med 1 rad. Två gridrader ger 16 linjers startavstånd, alltså **minst 7 linjers mellanrum** mellan två 9-radersmaskers ritintervall. Detta gäller **enbart en antagen gemensam spriteskärm-Y-förankring** och startögonblicket.
4. Jämför också hur många av de gamla `example_six_positions` som kan behållas i en sådan parvis Y-separerad mängd.

| Historiskt rum | Ursprungliga kandidater | Nåbara enligt 2×2-BFS | Femparsmängder med separerade Y | Max direkt återanvändbara ur `example_six_positions` |
|---|---:|---:|---:|---:|
| **A01** | 20 | 20 | **2 208** | **4** |
| **B01** | 13 | 13 | **48** | **3** |
| **C02** | 18 | 18 | **1 248** | **4** |
| **D01** | 15 | 15 | **420** | **5** |

Exempel på giltiga **initiala, inte godkända spawnuppsättningar** (`[x,y]` i gridankare):
- A01: `[14,3], [9,6], [14,9], [9,12], [14,15]`
- B01: `[9,3], [14,9], [35,13], [9,15], [35,17]`
- C02: `[14,3], [9,6], [14,9], [14,15], [4,18]`
- D01: `[14,3], [9,6], [14,9], [9,12], [14,15]`

**Positivt under begränsade antaganden:** samtliga fyra v0.11-kartor har minst en parvis Y-separerad femstart. **Viktig ny konflikt:** de gamla exempel-sexstarterna kan inte i A/B/C omvandlas till fem icke överlappande Y-band endast genom att ta bort en NPC. En framtida S1-lösning behöver därför ett **nytt uttryckligt spawnval**; tyst användning av sex-starttestet är fel.

**Vad siffrorna INTE visar:** att fem fiender kan förflytta sig samtidigt utan Y-kollision, att de kan följa spelaren förbi varandra, att key från slumpad bärare kan nås, att verklig 8×9-grafik och 6×6-/kollisionsankare passar genom korridorer, att dessa startmängder har jämn sannolikhet eller att Atari 2600-hårdvara klarar full rasterbudget. De visar inte heller något om kandidaterna i v0.19 `*_OPEN_01`; den öppna rumskänslan är användargodkänd **riktning**, men de exakta v0.19-kartorna är ännu inte ersatta. Inga kartfiler har ändrats.

## 3. Y-policy: föreslå speltestvillkor, INTE en bestämd AI-regel
I G5-S1 får två fienders **ritintervall om 9 fysiska rasterrader inte överlappa i en frame** om vi vill hålla G5K:s P1-ägarmodell vid max en vit NPC per rad. **Att endast ordna startpositioner räcker inte; invarianten måste testas under all jakt, patrull och spawn**.

Svår gameplaykonsekvens: Om fem NPC alla vill nå spelaren på samma Y måste minst fyra begränsa sin vertikala förföljelse eller vänta. Vid ständigt bibehållen Y-ordning kan NPC inte passera varandra vertikalt. Detta är inte bara en prestandaoptimering utan en materiell regeländring för tidigare fri 4-vägs-AI. Ett system med adaptiv ordning och temporärt väntande i Y kan prövas source-only som **kandidat**, men får inte antas vara spelbart, rättvist eller bättre utan dynamiska tester och användarbedömning.

**Föreslagna framtida acceptansfrågor** före eventuell kod: (a) når fem AI-spawns faktiskt spelaren eller blockerar/kringgår honom på alla beslutade rum? (b) blir någon fiende permanent Y-låst bakom en annan? (c) nås guldnyckel, dörr och utgång trots lanes? (d) kan spelaren utnyttja systemet för säkra passager? (e) ser fem individers originalmasker rättvända och tydliga ut i 60 Hz? Inget tidigare sådant fullspelstest är godkänt.

## 4. S05 kvarstår även om S1 används
G5L:s stressfall **S05**: gul player + vit NPC + gold key + låst orange dörr på samma Y, plus M0-skott och brun PF. Med P1 låst av orange dörr och bara en P1 per rad behöver P0 i G5K:s enkla kanalmodell tre 8-bitars bitmaphändelser (gul + vit + key); **ingen generell fungerande 6507/TIA-kernel eller godkänd visningswaiver finns**. Godkänd O1 hjälper enbart när fienden faktiskt skymmer nyckeln med bildöverlappning. Varken key-drop under NPC, door-Y eller Ball/PF-konflikt får gömmas från ett framtida G0/fysiskt stresstest.

Tekniskt grundprov efter **separat G6-auktorisation** förblir G4 H4-ONE (P0 gul+vit i båda numeriska X-ordningar, M0 samma Y, brun PF, korrekt färg och registerdeadline). Även ett PASS där skulle inte räcka för R2/S05 och inget G6 är beställt.

## 5. Poängpolicy efter fem istället för sex – konkret REKOMMENDATION, inte beslut
Original: -25 per dödad NPC, +50 vid faktisk nyckelupptagning, +100 vid utgång, +15 för varje levande NPC, poänggolv 0, beslut 047 att all-kill inte ska bli långsiktigt lönsamt.

Med fem NPC och `k` dödade blir under antagandet att nollgolvet **inte** ingriper:
- **Gamla -25-regeln:** `delta = 225 - 40*k`, alltså **+185** för bara bärare (`k=1`) och **+25** för alla fem (`k=5`).
- **Förslag: -30 per dödad NPC**, övriga belopp oförändrade: `delta = 225 - 45*k`, alltså **+180** för bara bärare och **0** för alla fem.

**Motivering:** en enda enkel ändring från -25 till -30 skyddar gamla målet att all-kill inte ger återkommande highscore-tillväxt och undviker en specialregel om sista dödade NPC. Nollgolvet gör att ett första all-kill-rum med startpoäng 0 fortfarande kan ge +150 om alla kills föregår key pickup; det är ett **golv-/ordningsfenomen**, inte positiv steady-state-farming. Kontrollera händelseordning i separat future score-test. Kill-penalty -30 är en **ändring av användarens beslut 043 och kräver uttryckligt godkännande**, får inte implementeras automatiskt.

För en framtida femfiendersbas: välj exakt en slumpad key-bärare med **1/5 per NPC** och fem distinkta godkända startpositioner på vald **beslutad** kartuppsättning. Det är ett **rebaseline-/PRNG-/spawnförslag**, inte en beslutad regel. Testa varje bärare och nyckelplats för åtkomlighet och ingen sned viktning.

## 6. Rekommenderad ordning och saknade beslut
1. MAIN lägger fram **två separata beslutspaket** för användaren: **(A)** en preciserad, spelbar vertikal policy, helst med provbar AI- och nyckelåtkomst; **(B)** femfiendersscore `-30` eller ett annat medvetet godkänt alternativ, och femspawn/1/5-key-bärare. Kartornas exakta val har egen beslutspunkt.
2. När och endast när dessa är uttryckligen godkända: skriv versionssatt **framtida** R1 fem/R2 fyra+key acceptans och samma-Y-rastervillkor, utan att ändra historiska v0.18-data bakåt.
3. **G6 är en separat användarauktorisation.** Då kan MAIN beställa ett enda begränsat G0-cykel-/START-förprov; inget ROM innan det passerat enligt ny beställning. ROM DEVELOPMENT III gör utvecklarens egenkontroll, VERIFICATION II oberoende efter separat verifieringsorder. Ingen automatisk PR7 merge, G7–G10 eller gameplay-implementation.

**Status efter G5N:** en konkret **start-spawnfeasibility i offline 2×2-modell** har kunnat visas för v0.11-kartorna; Y-jakt, S05/KEY, score/spawn-beslut, fysisk G0 och G6 kvarstår uttryckligen öppna. **Ingen ROM, grafikcanon, spelregel, PR-merge eller oberoende verifiering ändrad.**
