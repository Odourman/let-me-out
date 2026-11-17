# LET ME OUT! – G5P: MAIN VII:s avgränsade uppdrag till RESEARCH II
**Datum:** 2026-11-17. **Status:** `AUTHORIZED_G5_ADVISORY_RESEARCH_ORDER`. **Ägare:** RESEARCH II (rådgivande), mottagande projektledning MAIN VII. **INTE G6/F12, ROM-kod, spelcanon, ny verifiering, PR-merge eller godkännande av någon grafisk waiver.**

## Uppdrag och utgångspunkt
Användaren har begärt att vi fortsätter nästa steg efter G5O. MAIN VII får samordna **rådgivande forskning inom den pågående G5-bedömningen**, men får inte godkänna nya spelregler eller starta ett senare ROM-implementationssteg genom ett allmänt "fortsätt". RESEARCH II ska därför **självständigt granska** den negativa G5O-skärmen och jämföra konkreta tekniska spelbara alternativ, utan att ta över ROM DEVELOPMENT III, GRAPHICS II eller VERIFICATION II.

Källor som MÅSTE återöppnas live innan slutsatser:
- [G5O – tidigare begränsad dynamisk testmetod och negativt fall](../gates/G5O_MAIN_VII_STRICT_S1_Y_LANE_DYNAMIC_CHASE_NEGATIVE_SCREEN_2026-11-17.md), [dess tolv råfall](../gates/G5O_HARD_LANE_GREEDY_CHASE_12_CASES_SOURCE_ONLY_2026-11-17.csv).
- [G5N – fem separerade startankare på v0.11](../gates/G5N_MAIN_VII_S1_FIVE_NPC_LANE_START_AUDIT_AND_SCORE_PROPOSAL_2026-11-17.md), [ursprunglig v0.11 JSON](../../design/PLANERADE_RUMSKARTOR_V011.json).
- [v0.19 fyra OPEN-kandidater](../../design/OPEN_ROOMS_V019_40x22_CANDIDATES.json) **endast parallell förstudie**, inte ändrad officiell karta.
- [G5K P0/P1+door-kanalhypotes](../gates/G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md), [G5L/S05 same-Y-stress](../gates/G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv), [G5-godkännandespärr](../gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), [G5M score/spawn](../gates/G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md).
- [Fyra oförändrade 8×9 masktyper](../../design/NPC_REFERENCE_8x9_masks.json), [kompletterande direkta användarbeslut LM-D04/LM-D06](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), och [originalarkivet med 57 beslut](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view).
- [Historisk Berzerk-disassembly pinnad på commit 480a528](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm), [AtariAge flicker-metoder](https://forums.atariage.com/topic/347643-flickering-sprites-is-there-more-than-one-way-to-do-this/), [AtariAge multisprite-kernel och rotationssortering](https://forums.atariage.com/topic/347667-multi-sprite-kernel-strategies-or-examples/), samt [historiskt citat om flicker kontra vertikal separation/Venetian Blinds](https://www.atariage.com/2600/archives/design_case.html). Forum och historiska källor är rådgivande, inte vår ROM-beviskedja.

## 1. MYCKET VIKTIG METODRÄTTELSE – var inte vilseledd av G5O:s 1/5-siffra
G5O prövade endast ett **girigt BFS-kortaste-väg-steg med strikt minskat avstånd** till en STILLASTÅENDE spelare, förenklad 2×2-fotmodell och fem fixerade starter per karta. Dess jämförelse med "fri" rörelse tillät dessutom fem fiender på exakt samma fotankare och var därför ingen kollisionskorrekt spelvariant.

**Geometrisk begränsning före AI:** om parvis NPC-vertikalt avstånd alltid måste vara minst 2 gridrader och `near` betyder BFS-avstånd ≤1 från en fixerad punkt, är högst **två** NPC geometriskt möjliga nära samtidigt, i gränsfallet på spelarens y−1 och y+1. Den observerade siffran 1/5 (eller 0/5 i B01) kan därför **inte ensam** skilja en bra S1-AI från en dålig eller säga att spelet är tråkigt. Den reflekterar även det avsiktliga grafiska utrymmeskontraktet. Att 8 513 av 9 126 upprepade avståndsminskande försök blockerades är en **tickräknare med samma återkommande stopp**, inte en oberoende procent av verkliga spelmöten.

**Begär därför en uttrycklig omtolkning av G5O**: bevara dess rådata och negativa B01-stallfall, men klassificera 1/5-måttet som starkt strukturellt begränsat och underkänn en kollisionsfri 5/5-jämförelse som produktbaslinje. Redovisa ALLA ändringar som ny analys; skriv inte om historiska G5O-CSV som om äldre mätningar aldrig funnits.

## 2. Forskningsfrågor (rådgivande, inte ny designcanon)
Jämför minst följande:
- **G5-S1a – strikt visuell Y-separation men adaptiv jakt:** tillåt planerade sidosteg eller tillfälliga BFS-ökningar, tidsmässig prioritet och ny bedömning av lokala mål, men behåll alltid minst 9 fysiska originalmaskrader utan vertikal överlappning. Redovisa om vertikal NPC-ordning måste förbli fixerad; om så, hur detta påverkar jakt och blockering av spelaren.
- **G5-S1b – mjuk/dynamisk Y-separation:** full logisk frihet eller temporär same-Y när fiender passerar och dokumenterad potentiell visningskonflikt; **ingen tyst bortskymning**. Kan föreslås som framtida policyval med separat användargodkännande.
- **G5-S2 – kontrollerad flimmer-/multiplexstrategi som reserv:** välj synlighetsprioritet per rasterrad/frame och visa vilka fem fiender eller key som faktiskt skulle saknas under belastning. **O1 är redan godkänd endast för faktisk android/key-pixelöverlappning**; inte generell same-Y-dold key, inte 10 Hz som accepterad frekvens.
- **G5-S0 – fri X/Y-kontroll:** ger bevarad originalrörelse men same-Y P0/P1/GRP/M0/door-problemet finns kvar. Använd denna endast som *ärlig jämförelse för spelbarhet*, inte som redan bevisad hårdvarulösning.

För alla kandidater: ange exakt vilka ursprungliga 57-beslut som förblir intakta och vilka som skulle behöva nytt, uttryckligt godkännande. Använd **fem NPC M,M,F,SM,SF** som senare angivet mål utan att retroaktivt ändra gamla R1=6/R2=5+key-test.

## 3. Reproducerbar minimimatris
1. Reproducera samtliga **12 G5O-fall**, samma version av start, kartor, fixerade mål och tidssteg. Förvalidera att startankarna har 2×2 åtkomst men markera att detta inte är 8×9-kollisionsbevis.
2. Utöka med **rörlig spelare**, både vertikala och horisontella banor, skydd bakom PF-vägg, flykt mot högerdörr, fem NPC som jagar i fyra riktningar. Ange exakta, reproducerbara player paths och NPC-uppdateringsordning; minst två extra startuppsättningar per rum för att undvika att anekdotisk spawn avgör utfallet.
3. **Rättvis jämförelse:** vid alla varianter ska NPC/NPC-kollision respektive eventuell visuell överlappning redovisas. Jämförelsen får inte ge fri X/Y möjligheten att fem NPC står på samma fotankare medan S1 nekas det, utan att det särskilt flaggas som en artificiell kontroll.
4. Mät inte bara samtidig närhet utan **antal unika fiender som någonsin hotar spelaren**, tid till första hot, antal låsningar över minst 30 ticks, framkomlig väg för spelaren till dörr, fiender som blockerar ingången, om olika spawns fungerar, kartbetingad ojämlikhet och eventuella permanenta luckor som spelaren kan exploatera. Redovisa råa sekvenser; ingen vilseledande sammanslagen "PASS" om flera spelkrav ej uppfylls.
5. Två separata key-/door-situationer: (A) en död key-bärare på dörrens raster-Y medan en annan vit NPC passerar nyckelns Y, med **verklig pixelöverlappning**; (B) samma raster-Y men **inget pixelöverlapp**. I B får godkänd O1 **inte** dölja nyckeln. Kontrollera logisk key fallplats, K1-pickup och att nyckelbäraren slumpas bland fem. S05 återstår en separat fysisk G0-fråga.
6. Översätt grundmodellen till ett tydligt **renderingskontrakt** med fulla 9 originalrader, P0 gul+vit/M0-färg, P1 orange dörr med svart negativt hål, PF brown, BK black, utan att kalla en 2×2-simulering ett cykel-/colorclock-provat TIA-schema. Använd 76 CPU-cykler/scanline, 128B RAM, standard F6 endast som **källkrav**, inte som ett löst "PASS".

## 4. Redovisning/acceptans från RESEARCH II
Leverera en versionssatt, rådatastödd **source-only** forskningsrapport till MAIN VII i GitHub och kopia i officiella Drive-mappen:
- Exakt testmodell, källversion/commit, körparametrar, eventuellt reproducerbart OFFLINE-skript/CSV med antaganden, resultat för alla scenarier och viktiga motexempel.
- Bedömning per kandidat: AI-/spelbarhetseffekt, synlighets-/flickerkostnad, konsekvens för originalbeslut, teknisk TIA-risk, kvarvarande key/door-S05 och vilka tester som vore falsifierande.
- Egen uttrycklig kritik av G5O:s nära-mått, av de kollisionsfria jämförelserna och av eventuell obalanserad validering.
- Avslutning med MAIN:s kommande **användarbeslutsfrågor**, inte en ny implementerad regel; rekommendera om och varför eventuell S1-/S2-policy bör visas i illustration/studie före bindande beslut.

**Avsluta vid rådgivande leverans.** Får **inte** skapa .asm/.bin, starta G0/G6, redigera canon-/beslutsregister, slå ihop PR, ändra befintliga originalmasker/kartor, godkänna ROM/Verification eller hävda att Work/ROM DEVELOPMENT/GRAPHICS/VERIFICATION redan gjort någonting.

## 5. Stoppgräns i G1–G10-planen
G1–G4 source-only redan klara. G5 teknisk granskning fortsätter genom **G5P rådgivande specialistuppdrag** inom samma grind. **Formell G5-acceptans kräver senare uttryckliga användarbeslut** om vertikal/rendervisible policy och separat score/spawn/kartval. G6/F12 och G7–G10 står fortsatt spärrade tills särskilt tillstånd ges.
