# LET ME OUT! – UTKAST ENBART – FÖRESLAGEN FRAMTIDA G6 MIKROPROV-ORDER TILL ROM DEVELOPMENT III
**Status:** `DRAFT_NOT_ISSUED_NOT_AUTHORIZED`. **Skapad av MAIN VI:** 2026-11-17 inom den SOURCE-ONLY-auktoriserade **G4**, för att spara det föreslagna handoffunderlaget. **INGEN IMPLEMENTATION ÄR BESTÄLLD.** Denna fil, en GitHub-länk, en Drive-kopia eller en "fortsätt"-formulering om G4 får **inte** läsas som att ROM DEVELOPMENT III får börja arbeta med detta koduppdrag. Först ett framtida **nytt uttryckligt användarbeslut** med exakt scope och fryst baslinje får lyfta utkastet till en faktisk arbetsorder.

## 1. Bakgrund och gräns
G1 källcanon godkänd som dokumentation, G2 historiska råbevis kontrollerade, G3 CPU/64-färgkopplings-/RAM/F6-kontrakt sammanställt, G4 `G4_SOURCE_ONLY_COMPLETE_CONDITIONAL_GO_ONE_MICROPROBE_NOT_ORDERED`.
**Syftet med senare separat beordrat G6 är EN enda minsta faktisk hardware-falsifiering**, inte ny hela R1-forskning, inget fullspel, inte tre generella NPC fria X, ingen v0.19 kart- eller sprite-omdesign, ingen PR #7-merge, ingen självsignerad E02 och ingen F12 på eget initiativ.

Frysta referenser:
- [G4 SOURCE-HYPOTES](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [G4 GO/NO-GO](G4_ONE_EXPERIMENT_GO_NOGO_DECISION_2026-11-17.md), [G4 TIA-schema](G4_REGISTER_TIMELINE_2026-11-17.csv), [G3 budget](G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md).
- [F9 fryst `c36982a...`](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md) som separata binära P1-maskbevis.
- [R1f original `552a085...`](https://github.com/Odourman/let-me-out/blob/552a085d0c1ce0ec47d4f3342173658a25fd0e87/rom/v018/experiments/main_ii_r1f_resp0/build.py) och [R1g `d1d1675...`](https://github.com/Odourman/let-me-out/blob/d1d16758c549ecd657aba3b0aa4d6d7559e19264/rom/v018/experiments/main_ii_r1g_dynamic/build_dynamic.py), tillgängliga som både frysta källor och G2 ZIP.
- [8×9 TOP-DOWN-maskar](../../design/NPC_REFERENCE_8x9_masks.json), Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. P0 vit **M**, P1 vita **F** och **SM**. Gul P0-spelare temporär fullstor diagnostikbitmap – inte godkänd slutgiltig spelarbitmap.

## 2. Leveransformat om senare separat användarauktoriserat
**ETT** dedikerat 6507/DASM/standard-F6/NTSC-diagnostikexperiment, i ny isolerad branch och ny experimentsubdir. Ingen ändring av frysta F9/F10/F11, R1f/R1g original, PR7, Issue #8-baslinjen eller `main` ROM. Ingen PAL, SC/ARM/DPC/CDF, inget gameplay eller ny mask. Fullt källa, binärens SHA256, `DASM .lst/.sym`, dokumenterade Stella 6.7.1-inputs, råa 9-raders PNG/GUI/video, TIA-write traps, PC, bank, scanline och exakta 76 CPU-cycle worst-case per rad. Behåll **även negativa fall**.

### Gate G0 – SOURCE/PREFLIGHT före ett enda binärbygge
En käll- och opcodetraceplan visar `RESP0/GRP0/COLUP0` i båda sortordningarna, `RESP1/GRP1` för två rättvända original F/SM, `ENAM0/RESM0/NUSIZ0` som ger **en** M0-skottsilhuett **på SAMMA aktiva Y**, source-korrekt brunt PF på båda gränserna, numeriskt RAM-X, `WSYNC` och max `76c/scanline` (inklusive worst-case branches/page crossings). Integriteten för 128B RIOT/stack och aktiv 4096B F6-bank skall redovisas. För varje av A1/A2/B1/B2 och 9 rader: ritningens effektiva fysisk START/GRP-deadline är medvetet prövbart, ej hemligt antaget från X≈3c. **Om G0 saknar en sammanhängande plausibel mekanism: markera G0 FAIL, STOPPA UTAN ROM och leverera blockerarrapport.** Inte återstarta ny ROM-variant på chans.

### Gate G1 – faktiskt enda mikrofysik-ROM om G0 PASS
- Ett enda ROM-läge läser RAM `PLAYER_X`, `NPC0_X`, `P1_F_X`, `P1_SM_X`, `SHOT_X` som numeriska heltal, INTE precompiled 2-/4-mode code profiler. Byt x för endast spelaren respektive NPC för att falsifiera koppling.
- Förregistrera **A1** (40,104,68,132,24), **A2** (48,96,72,128,24), **B1** (104,40,68,132,24), **B2** (96,48,72,128,24). Fälten ordning `player,npc,P1_F,P1_SM,shot` i synliga TIA-CC mål. En annan numerisk X för en figur skall **bara** flytta den figuren (undantag explicit dokumenterad overlap/occlusion).
- Vid y99 och varje berörd rad: **M0 EN SAMMA SCANLINE** som vita original och gul player, icke-overlap X24 i positiva fall, inte före bandet. **Exakt ett** synligt M0 (NUSIZ0=$02 kan skapa extra missilcopy). Bara äkta source-PF bruna väggpixlar, inte nollad PF.
- Rättvända nio originalrader, de små maskernas 0-rader behållna. Kolla reella GUI-färgpixlar, crop↔TIA-CC koordinatkalibrering och 262 NTSC-linjer när lämpligt. Registrera cykler och faser vid varje `STA RESP0`, `GRP0`, `COLUP0`, `ENAM0`, `NUSIZ0`, `RESP1`, `GRP1`, `PF0/1/2`, `WSYNC`. Kör 600 sammanhängande frames för ett positivt relevansfall, om godkänd uppdragsram kräver detta.
- **Negativ X1:** M0 X43 överlappar vit M originalrad3 X40..47; framställ inte två distinkta skott/androidfärger på exakt samma slutpixel som PASS för standard-P0/M0. Det negativa utfallet dokumenterar känd registerfärgkoppling, men avgör inte slutspels-kollisionsreglerna.
- **Negativ X2:** P0 vit X40 + gul X44, med risk att RESET klipper bitmap; dokumentera FAIL/INCONCLUSIVE och ingen designwaiver. Det är inte samma sak som om A1–B2 passerar.
- Varje test har PASS/FAIL/INCONCLUSIVE, alla negativa originalmask- och M0-kontroller bevaras. En observerad avvikelse i A/B-fysikscen => stoppa, återgå till MAIN med exakt source/Cycle/CC-fel. **Inga oändliga sweep- eller profilsökningar.**

## 3. Ej tillåtna falska genvägar
- Inget "M0 är aktiv" om M0 endast finns på en rasterrad **före eller efter** original 9-radersbandet.
- Ingen `FRAMELO & $30` som ensam väljer ett av fyra hårdkodade X-värden och sedan kallar dem NUMERIC X.
- Inga vertikalt vända M/F/SM/SF (R1ba falskt auto-PASS), inga reducerade 5/4 fiender eller designenligt oförklarad interleaved flicker.
- Ingen hardcoded room cutover, ingen fake PF, inget R3-keyhole/port eller R2-key som marknadsförs PASS genom denna begränsade P0/P1-primitiv.
- Ingen "G6 PASS" om färg- och kopie-WorstCase inte säkrats via riktig Stella och separat efterföljande MAIN-evidensgenomgång. Ingen ersättning av oberoende VERIFICATION II E02 vid senare G9.

## 4. Framtida utvärdering och möjligt stopp
**Efter EN godkänd mikroprov**, MAIN ska återläsa ROM-hash, faktisk source och raw pixels och avgöra `MICRO_PASS_BOUNDED`, `FAIL`, `INCONCLUSIVE`. Endast efter specifikt nytt användaruppdrag kan nästa G7 sex numeriskt fria X/Y utredas. **G5** aktiveras endast vid reell userdesignkonflikt och kräver uttryckligt beslut om kompromiss. Inga ändringar av canonical originalmål av MAIN/ROM på eget mandat.

### Särskild varning
**Detta är ett UTKAST**, publicerat för att framtida arbetsordrar inte skall behöva rekonstruera G4-resonemanget. Det är inte en skickad, utfärdad eller auktoriserad implementeringsinstruktion. MAIN VI stannar vid G4; ROM DEVELOPMENT III och VERIFICATION II arbetar inte utifrån utkastet utan separat tilldelning.
