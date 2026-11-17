# LET ME OUT! – MAIN VII G5Z: uttryckligt användargodkänd ENDAST G0 H4-ONE, SOURCE-ONLY arbetsorder till ROM DEVELOPMENT III
**Datum:** 2026-11-17
**Status:** `G5Z_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_NOT_YET_EXECUTED`
**Beställare:** MAIN VII. **Utförare:** ROM DEVELOPMENT III. **Beslutsfattare:** användaren. **Leveransmottagare:** MAIN VII.
**KATEGORISKT:** inga ROM-byggen, inga assembler-/spelimplementationsändringar, ingen Stella-debugging/körning, ingen G1/G6/F12, inga framtida steps, ingen PR-merge eller oberoende VERIFICATION II beordras här.

## 1. Spårbart särskilt användarmandat
MAIN VII avslutade sin uttryckliga rekommendation och kontrollfråga med:

> "Auktorisera enbart G0-källgranskningen av H4-ONE till ROM DEVELOPMENT III, med ovanstående tre utfall och hård stoppgräns."

Användaren svarade direkt:

> "Ok, fortsätt. Följ dina rekommendationer"

**Detta är ett uttryckligt jakande svar på precis den avgränsade rekommendationen**. Uppdraget **startar nu som separat auktoriserad source-only G0-arbetsorder**, inte som ett allmänt tillstånd för ROM-utveckling, eller för att starta G6. Det ändrar **inte** tidigare spelcanon och ger **inte** G0 PASS i förväg. Själva specialistchatten körs inte automatiskt enbart genom att MAIN skapar detta dokument eller GitHub-issue; ROM DEVELOPMENT III måste faktiskt öppna och genomföra arbetet och redovisa leveransen.

## 2. Primära källor och avstämning, läs live direkt
1. [G4 förregistrerad H4-ONE hypotes](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [G4 tidslinje med okända cykler](G4_REGISTER_TIMELINE_2026-11-17.csv) och [G4 GO/NO-GO](G4_ONE_EXPERIMENT_GO_NOGO_DECISION_2026-11-17.md). Den äldre [G4 framtida G6-ROM-order är fortfarande ENBART UTKAST](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md): detta är **INTE** dess utfärdande.
2. [G5Y beslutad testordning](G5Y_MAIN_VII_FALSIFIABLE_HARDWARE_TEST_PLAN_H4_ONE_S05_FIVE_NPC_NOT_AUTHORIZED_2026-11-17.md), [G5Y 17 förregistrerade testfall](G5Y_MAIN_VII_PREREGISTERED_TECHNICAL_TEST_MATRIX_NOT_AUTHORIZED_2026-11-17.csv). **Statusen för framtida G1/S05/5-NPC-testfall förblir NOT_RUN/NOT_AUTHORIZED**; G0 är nu enbart auktoriserad.
3. [G3 resurs-/cykel-/färgkontrakt](G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md), [G2 negativa tester och non-repeat](G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md), [F11 gamla källbaserade G0-FAIL](../MAIN_V_R1_F11_G0_FAIL_SOURCE_ONLY_RECEIPT_2026-11-17.md), [G5H full fem-NPC source-stress](G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md), [G5P forskning endast rådgivande](G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md).
4. [Original TOP-DOWN 8×9-masker](../../design/NPC_REFERENCE_8x9_masks.json) källblob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. [Fyra godkända framtida kartorna och exakta källhashar](G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json). De historiska R1/R2-testerna med sex/fem+key är frysta och får inte byta status.
5. [G5:s senaste bindande spel-/auktoritetsbeslut](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), [LM-D12/13 fri logisk X/Y och visuell kvalitet](G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D14–16 fem NPC, -30/kill och nyckelbärare](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D17–19 fyra exakta kartmål](G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md).
6. Läs även faktiska frysta tekniska original och ROM DEVELOPMENT II→III migrationsöverlämning via dess tidigare källpin `5d7551b50cbb67c659e0d4e4748812636a0dac77` om tillgänglig; om en fil saknas på `main`, redovisa detta, använd tillgängligt pinnat original och gissa inte dess innehåll. Bekräfta faktisk tillgång till GitHub, Drive och källor före slutsatser.

## 3. Exakt G0-H4-ONE-hypotes att förhandsgranska
**På NTSC standard F6 (16 KiB total, 4 KiB aktiv bank), med 128-byte RIOT inklusive stack och max 76 CPU-cykler/scanline**, ska en teoretiskt fullständig **enda datastyrd nio-raderskernel** kunna schemalägga:

- **P0:** en fullskalig **gul diagnostisk 8×9-spelare** och **en vit stor manlig M-originalmask 8×9**, på numeriskt separat X, med **BÅDA** X-identitetsordningar gul→vit OCH vit→gul.
- **P1:** två olika **vita originalmasker F och SM 8×9 TOP-DOWN** samtidigt i samma 9-radersband, numeriskt skilda RAM-X. SM:s alla nollrader och orientering bevaras; ingen originalmask ändras.
- **M0:** EXAKT EN aktiv synlig projektil **på samma aktiva nio-raders Y-band** där original-NPC syns, i positiva fall på en X-plats utan förbjuden vit/gul-pixelöverlapp. Inte endast skott på rasterraden före eller efter. `NUSIZ0` kan ge falska M0-kopior och måste ingå i tillstånds-/fasanalysen.
- **PF:** verklig källa-spårbar **brun** Playfield-vägg på vardera kanten i samma Y-zon, inga borttagna väggar eller PC-ritade overlays. Preload får bara antas där käll-PF faktiskt är statiskt över aktiva nio rader. **H4 provar inte hela nya fyrkartskompositionen**, och äldre C02-R3-registerfaser får inte påstås fungera för nya kartor.
- Ingen guldkey, orange dörr eller full femfiendersintegration ingår i H4; **S05 same-Y gold key+white NPC+orange P1-door+yellow player+M0+PF är ett SEPARAT senare problem**, som inte löses automatiskt genom H4.
- Alla aktörer har *separata numeriska RAM-X* och verklig datastyrd X-/aktörsordning, inte fyra förkompilerade fulla kernlar, framecounter-mode, enbart binära X-väljare eller förberedda konstgjorda statiska formationer. Två ytterligare möjliga numeriska X-par måste kunna matas efter eventuell framtida ROM-frysning inom förregistrerad domän.

### Föregående G4-stimulidata, synliga TIA CC-mål (inte CPU-STA-cykler)
| Fall | PLAYER_X | M_X | F_X | SM_X | SHOT_X | Krav |
|---|---:|---:|---:|---:|---:|---|
| G4-A1 | 40 | 104 | 68 | 132 | 24 | gul P0 till vänster, vit M till höger |
| G4-A2 | 48 | 96 | 72 | 128 | 24 | datastyrd positionsvariation |
| G4-B1 | 104 | 40 | 68 | 132 | 24 | **omvänd** vit M→gul spelare |
| G4-B2 | 96 | 48 | 72 | 128 | 24 | omvänd ordning med andra avstånd |
| G4-X1 | 104 | 40 | 68 | 132 | 43 | **negativ** samtidig vit M/gul M0 färg vid CC43, ursprungsrad 3 `FF` |
| G4-X2 | 44 | 40 | 68 | 132 | 24 | **negativ/svår** fyra-CC X-överlapp, P0 retrigger/risk för klippning |

**M1** prövar källmässigt bara ett enda M0 vid NUSIZ0-kopiering; **P1** kontrollerar båda F/SM-rätta originalmaskerna på alla nio rader. Inga faktiska ROM-bilder tas i G0.

## 4. Utför bara följande käll-/analysarbete
1. Upprätta en **per-aktiv-rad och per-fall** fullständig `6507 opcode / operand / varifrån data läses / CPU c start/slut / branchworst / pagecross / synlig CC-effekt / faktiskt förväntad START/GRP-latch-deadline / ägda färg- och objektregister`-matris. Lista okända tider som just **OKÄNDA**, inte som fysiskt uppmätta värden. HBLANK och CPU/CC-offset måste vara explicit, inte förenklat `x=3c`.
2. Redovisa VBLANK/F6-bank-presentation och relevanta loopförberedelser, `NUSIZ0/1, RESP0/1, GRP0/1, COLUP0/1, COLUPF, ENAM0/RESM0, PF0/1/2, WSYNC`, samt exakt förändringssekvens vid X-ordningsbyte. **Behandla NUSIZ0/M0-missilkopior och första P0-bitmapens interna START som särskilda risker.**
3. Gör *worst-case* instruktionskostnads-/branchanalys för **var och en av de nio maskraderna och båda ordningarna**, max 76 CPU-cykler/scanline. Redovisa 128-byte RIOT inklusive stack, per bank 4 KiB F6, datafetch och sortering före raster (utan att förutsätta obegränsad VBLANK) samt kritiska horisontella deadlines. Om teoretisk sekvens fallerar så redovisa första konkreta blockeraren och motsvarande register/CC/tidpunkt.
4. Skilj G4-A/B-positiva från G4-X1/X2 negativa och från M1/P1-kontroller. Följ källan: X1 kan **inte** ge två olika färger i samma pixel när P0/M0 delar `COLUP0`. Ett sådant väntat negativt resultat i en specifik allokering får inte omvandlas till ett globalt Atari-omöjlighetsbevis.
5. **N0 två-actor-variant** från G5P får endast användas som kort intern analytisk diagnos för en särskild mekanism. `N0_PLAUSIBLE` får aldrig ge `H4_G0_PLAUSIBLE`; H4 kräver även två P1-original och riktiga PF/M0-regler på samma rad. Gör ingen ny obegränsad 30-tricks-katalog eller repetitionsstudie av F9/F11.
6. Avsluta med en **kort källbunden konsekvensanalys** av vad som fortfarande krävs för slutmålet **5 vita NPC M,M,F,SM,SF + gul player + ett shot + fulla 40×22 kartors PF, plus S05 R2 gold key/orange right-door**. Identifiera hur H4-kärnan möjligen skalar eller var fysiskt resurskonflikt fortfarande finns. **Inte en andra forskningsomgång** och inga löften om fullspelsfeasibility.
7. Var transparent om källorna saknar exakta effektfaser. En fullständig plausibel G0-plan kan fortfarande behöva fysisk G1-kontroll som **inte är auktoriserad här**; om kritiska faser saknar källstöd ge `INCONCLUSIVE`, inte gissad `PASS`.

## 5. Tre tillåtna slututfall – en enda beslutscykel
- `G0_SOURCE_PLAUSIBLE`: En **sammanhängande och källstödd** register-/opcode-/colorclock-/minnesbudget för hela H4-ONE:s A1/A2/B1/B2 inklusive single M0 och PF finns. Det betyder **källmässigt rimligt**, inte TIA-fysiskt PASS och inte full fem-NPC.
- `G0_FAIL_NO_ROM`: En **falsifierande, konkret blockerare** inom den granskade H4-allokeringen (exempel >76c, ogiltig START, NUSIZ/M0-duplicering, RAM-/banköverskridande) kan visas trots den enda tillåtna sammanhängande preflight-genomgången. Redovisa gräns och vad den **inte** motbevisar. **Bygg ingen ROM.**
- `G0_INCONCLUSIVE_NO_ROM`: Avgörande registereffekt, START-/GRP-/NUSIZ-fas eller annan fysisk deadline kan **inte underbyggas** utifrån tillgängliga exakta källor. Redovisa vad som måste mätas senare för att skilja möjlig/omöjlig. **Bygg ingen ROM.**

**Oavsett utfall: STOPP efter leverans**. En `G0_SOURCE_PLAUSIBLE` är **inte** automatisk tillåtelse till ROM eller G1. En `G0_FAIL` är inte tillåtelse att hoppa till ny mapper, ny Y-policy eller förenklad rendering. Vid `INCONCLUSIVE` får en ny analys eller fysisk instrumentering bara ske genom **en ny separat användarauktorisation**.

## 6. Obligatorisk specialistleverans
- En originalkällbunden Markdown **`TO_MAIN_G5Z_G0_H4_ONE.md`** med exact verdict och rad-för-rad cycle/CC eventordning, alla antaganden och osäkra deadlines samt resultat på G4-A1/A2/B1/B2/X1/X2/M1/P1.
- Vid behov separat **CSV cycle/register/CC schedule** och liten ren källberäkningsfil **endast för analys** (ingen producerad `.asm`, `.bin`, `.lst`, `.sym`, Stella-screenshot eller nytillverkad spelkod).
- Ett dokument `G5Z_SOURCE_PROVENANCE.md` med käll-commit+Git-blob per faktiskt använd huvudkälla, metod och exakt beskrivna negativa historiska prover; den äldre F11 G0-FAIL ska vara kvar.
- Kort riskappendix `H4_TO_FIVE_NPC_AND_S05_REMAINING_GAPS.md` (högst fokuserad avstämning, inte ny researchomgång).
- Spara enbart **nya dokument/forskningsfiler** på separat ROM DEVELOPMENT III-branch under exempelvis `rom/g5z_g0_h4_one/`, aldrig ändra original-F11-källor, `main` ROM, `design` eller PR #7. Skapa gärna reproducerbar arkivkopia i officiell Drive, om verktyg tillåter, och ange exakta länkar/filhashar.
- Rapportera **ENDAST** till MAIN VII; MAIN tar emot och kontrollerar. ROM DEVELOPMENT III:s egenkontroll är **inte** oberoende VERIFICATION II. **Specialistchatten får inte starta G1/G6 eller besluta om en ny spelregel efter egen slutsats.**

## 7. Avslutsvillkor, giltighet
**`G5Z_G0_AUTHORIZED` är giltig arbetsorder. `G0_STATUS=AUTHORIZED_NOT_STARTED` vid skapande, inte `G0_PASS`.**
**`G5_FORMAL_OPEN` kvarstår. `G6/F12/G1/S05/FullROM/PRmerge/VERIFICATION=NOT_AUTHORIZED`.**
Nästa beslut efter leverans är MAIN VII:s mottagning av exakt källbevis, därefter separat användarbeslut om nästa tekniska steg (även om verdict `PLAUSIBLE`).

## 8. Beställningslänk
Den konkreta GitHub-issue som länkar till detta dokument får vara **en aktiverad specialistarbetsorder för G0 endast**, och får inte tolkas som automatisk körning av ROM DEVELOPMENT III-chatt.
