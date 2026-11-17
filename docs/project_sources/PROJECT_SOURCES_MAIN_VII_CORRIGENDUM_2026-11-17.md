# Let Me Out! – MAIN VII korrigering av Project Sources, 2026-11-17

## MAIN VII – SLUTLIG PROJECT SOURCES-VERSION, 2026-11-17

**ENDA REKOMMENDERADE VERSION FÖR NY UPPLADDNING:** [LET_ME_OUT_PROJECT_SOURCES_MAIN_VII_FINAL_2026-11-17.zip](https://drive.google.com/file/d/1mLSqMZZx_j7g8ha6Mje4PyBsjiwZ6V6F/view), SHA256 `2c20ea7a5dbc9ae6809d2731fecfbc12acd6be279acb2d9255ba49d723fd792d`, 9 individuella källfiler, 35 spårbara källreferenser. Den nedladdade Drive-kopian har bytejämförts med originalet; ZIP CRC och alla 8 SHA256-filposter kontrollerades utan avvikelse.

Denna slutgranskning rättar en saknad direkt källregisterpost till G5M samt bevarar två kartauktoritetsnivåer: luftiga rum är godkänd riktning (LM-D04), men v0.19:s exakta `*_OPEN_01`-kartor är fortfarande förslag, medan `A01/B01/C02/D01` fortsatt är källvald äldre baseline. O1:s tidigare dokumenterade begränsade godkännande bevaras. Inga spelregler, originalmasker eller tidigare ROM-/Stella-evidens har ändrats.

**Tidigare paket är nu historiska, inte parallella Project Sources:** `LET_ME_OUT_PROJECT_SOURCES_2026-11-17.zip` (MAIN VI) och `LET_ME_OUT_PROJECT_SOURCES_MAIN_VII_CORRECTED_2026-11-17.zip` (första MAIN VII-rättelsen). Det som följer i äldre text beskriver sina respektive historiska revisionsögonblick. **G5:s formella användarbeslut återstår och G6/F12 är inte auktoriserat.**


Status: SOURCE ONLY. Inte ny game canon, G5 PASS eller G6-kodauktorisation.

## Kontrollerad migration
MAIN VII efterträder MAIN VI. GitHub main vid mottagningskontroll: 61bb44f39d6f6f3f2ceb8bfb4b134b7834e87db4 (151 poster, inte trunkerat). Ursprungligt masterarkiv från Google Drive verifierades på nytt: 21 filer, 57 beslutsrader, ZIP CRC OK, SHA256 f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4.

Det historiska, äldre Project Sources-paketet LET_ME_OUT_PROJECT_SOURCES_2026-11-17.zip har SHA256 5d4b4749c5db710eda29642c4918bfcf7d8032acf2e73cdd6a809f1f1f0986e7. **Ladda inte upp detta parallellt med korrigerade paketet.**

Det korrigerade niofilspaketet som MAIN VII levererar i sin chatt heter LET_ME_OUT_PROJECT_SOURCES_MAIN_VII_CORRECTED_2026-11-17.zip, SHA256 1d749df02d74b8fa1c41f8160e5ca2ae15d41eff32bdb3fac6be895915653cb0. Det har 29 källreferenser, verifierad ZIP CRC och SHA256 per fil. Den gamla ZIP:en i Google Drive bevaras som historik; den är inte den rekommenderade uppladdningsversionen.

**Ny, verifierad officiell Drive-kopia av det rättade paketet:** https://drive.google.com/file/d/1fxexRLz9fE8egW9bFnA1zA3x3j7f9AYj/view (28 001 byte, SHA256 1d749df02d74b8fa1c41f8160e5ca2ae15d41eff32bdb3fac6be895915653cb0). Detta är versionen att lägga till i Project Sources; den äldre Drive-ZIP:en ska bevaras enbart som historik.

## Konflikt 1: O1 var redan godkänt
Den äldre studien docs/KEY_OCCLUSION_LOGIC_V015.md kallar O1 preliminär. Men docs/MAIN_STATUS_NEXT_10_2026-11-15.md återger det efterföljande direkta användarsvaret "Lite flimmer i spelet är ok. Men följ din rekommendation", och gör O1 till ett godkänt beslut. Docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md bekräftar detta uttryckligen under LM-D06.

Godkänt scope: en android får kortvarigt skymma guldnyckeln vid faktisk överlappning; nyckeln ligger kvar logiskt, behåller upptagningsbarhet och återkommer på samma koordinater. Lite, kortvarigt flimmer är kvalitativt godkänt, men ingen siffra/frekvens och ingen systematisk same-Y- eller långvarig objektosynlighet.

Senare G5L/G5M och vissa G5-sammanfattningar felklassar O1 som preliminär. De formuleringarna bör läsas med denna rättelse, eftersom en senare rådgivande text inte återkallar ett uttryckligt användarbeslut. Rättelsen är inte ny spelcanon och rättfärdigar inte att gömma en key som inte faktiskt överlappar en android.

## Konflikt 2: identifierarkrockar
- K1 är en godkänd spelregel om nyckelupptagning tidigast nästa logiska uppdatering. Paketets fem forskningskombinationer har nu egna etiketter TK01–TK05.
- S0/S1 förekommer i äldre v0.11 som start-/spawnfilter; G5-renderingsalternativ heter nu G5-S0/G5-S1/G5-S2 så de inte kan blandas ihop.

## Övriga korrigeringar
- MAIN VI angiven som historisk roll; MAIN VII tar över.
- G5F–G5M omfattar också nyare G5M score/spawn, inte bara G5F–G5L.
- Fem fiender och svart bakgrund är användaruttryckta mål, men historiska v0.18 R1=sex/R2=fem+key ändras inte retroaktivt.
- Fem fienders all-kill kan under tillräckligt saldo ge +25 per rum mot beslut 047. Separata framtida beslut om poäng, 1/5 nyckelbärare och fem validerade spawnpositioner väntar. Ingen ny regel kodas.

## Oförändrad teknisk spärr
G1–G4 read-only/source-only klara. G5:s tekniska underlag klart, formell Y-/synlighets- och score/spawn-ombaslinjering återstår. G6/F12 och G7–G10 inte auktoriserade. PR #7 är äldre draft; Issue #8 historisk oberoende verifiering. Ingen ROM/Stella tillkom vid denna rättelse.

Primära länkar:
- https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md
- https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md
- https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md
- https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md
