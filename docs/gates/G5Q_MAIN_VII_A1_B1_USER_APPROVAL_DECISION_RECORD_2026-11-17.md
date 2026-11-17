# LET ME OUT! – G5Q MAIN VII: användarbeslut A1 + B1 som fortsatta designmål
**Datum:** 2026-11-17. **Status:** `G5Q_A1_B1_USER_APPROVED_AS_DESIGN_TARGETS_ONLY`. **Beslutstyp:** avgränsat produkt-/kvalitetsmål, INTE rendering/kernel-PASS, flimmerwaiver, ändrad poängregel, R1/R2-cutover, G6/F12-auktorisation eller PR-merge.

## 1. Spårbar direkt användarvilja och exakt referent
MAIN VII hade omedelbart före svaret uttryckligen frågat:

> "Godkänner du G5Q:s rekommendation A1 + B1 som våra fortsatta designmål?"

Detta följdes av förklaringen att det **inte** startar G6, ändrar poäng eller accepterar någon given flimmernivå. Användarens direkta svar på denna precisa ja/nej-fråga var:

> "Följ dina egna rekommendationer"

**Tolkning strikt i samtalskontext:** användaren godkänner den uttryckligen hänvisade rekommendationen **A1 + B1 som designmål**, inte samtliga tidigare projektförslag, inte separat C/D/E och inte implementation. Detta är ett **positivt, avgränsat användarbeslut via direkt hänvisning**, skilt från ett generellt "fortsätt". Äldre råd och citat får inte tolkas som godkännande av nya detaljer.

Förslagets publicerade omfattning och ordalydelse: [G5Q beslutsklart underlag](G5Q_MAIN_VII_DECISION_READY_DESIGN_TARGET_AND_PRE_G6_BOUNDARY_2026-11-17.md), [Drive-original](https://docs.google.com/document/d/1_bB-F6pvwEehRP09F1jdfyYnUtKo4c6mie4QD3c9YGw/edit). Projektets tidigare bindande [LM-D01..D11](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) och originalets 57 beslut kvarstår där de inte berörs.

## 2. LM-D12 – G5Q A1 GODKÄNT, endast önskad spel-/AI-funktion
**De fem framtida vita fienderna M,M,F,SM,SF ska logiskt kunna röra sig individuellt i både X och Y och behålla trovärdig fyrvägs-jakt, individuella positioner, NPC/NPC-kollision och möjlighet att navigera runt väggar och mot spelaren.**

- Fienderna ska **inte genom en tyst implementation** permanent låsas i fem Y-banor, generellt förhindras att passera vertikalt eller få en annan spelmekanik som kompromiss för enkel multiplexning.
- Situationell grafisk kanal-/renderingsplanering får vara **kandidat för fortsatt utvärdering**, inte godkänd teknik, generellt same-Y-skylande eller licens att förlora spelobjekt i spellogiken.
- Ursprungliga fyra TOP-DOWN 8×9-masktyper samt nyckel, orange högerdörr och redan beslutade mekaniker bevaras som mål.
- Om faktisk hårdvara senare falsifierar målet krävs **nytt, uttryckligt användarbeslut** före någon rörelse-/AI-kompromiss. Detta beslut utgör ingen fysisk möjlighetssats.

## 3. LM-D13 – G5Q B1 GODKÄNT, endast önskad visuell kvalitet
**Fem individuella NPC-figurer ska vara igenkännbara och närbelägna farliga fiender får inte systematiskt försvinna eller bli så oläsliga att spelaren förlorar möjligheten att uppfatta och undvika hot.**

- Nyckeln förblir på rätt logisk plats och ska synas när den **inte faktiskt pixelöverlappas** av android, även vid samma raster-Y som fiende/dörr. **LM-D06/O1 är fortsatt godkänd endast för tillfällig faktisk nyckel/androidöverlappning**; kortvarigt mindre flimmer har tidigare accepterats **kvalitativt**, men inte kvantifierad tolerans/10Hz/varaktig osynlighet.
- Orange högerdörr med utskuret svart nyckelhål, gul spelare, bruna PF-väggar och svart bakgrund förblir visuella mål. Ingen ny rendering/ny maskskala beslutas.
- Utvärdera senare faktisk andel synliga frame per NPC, längst sammanhängande försvinnande under fara, individuella maskers riktighet och S05-nyckelsynlighet i en **framtida separat auktoriserad teknisk utvärdering**.
- **Inga numeriska flickertrösklar eller visningswaivers** har godkänts av detta beslut. Framtida B2 måste visas konkret för användaren och godkännas separat.

## 4. Fortfarande uttryckligen obeslutade G5-punkter
1. **C:** ny framtida versionerad R1 med fem NPC och R2 med fyra+key, samt exakt acceptance; historisk v0.18 R1 sex/R2 fem+key och deras PASS/FAIL bevaras.
2. **D:** original score `-25`/kill vs föreslagen `-30`/kill. `-30` är fortfarande endast ett förslag, ingen ändring av gamla 042–047. Fem spawnankare/1/5 uniform key-bärare kräver separat godkännande och riktig logik.
3. **E:** exakta v0.19 OPEN-rumskartor är fortfarande designkandidater, godkänd *luftig riktning* LM-D04 ger inte kartcutover.
4. **Fysisk G0-hypotes/G6:** G4 H4-ONE och G5P:s snävare probeutkast måste först preciseras i ett särskilt framtida beslutsdokument. **Ingen ROM/assembler/Stella eller ny verifieringsorder nu**.
5. **S05:** spelare + vit NPC + key + orange dörr + M0/PF på samma raster-Y, inklusive key utan verklig bitöverlapp, saknar fortfarande en bevisat korrekt TIA-kernel. O1 löser inte denna generella fysiska konflikt.

## 5. Slutlig grindstatus
`G5Q_A1_B1_DESIGN_TARGETS_APPROVED` men **`G5_FORMAL_STILL_OPEN`** och **`G6_NOT_AUTHORIZED`**. RESEARCH II G5P är avslutad source-only och har mottagningskontrollerats; originalresearchbranch hålls isolerad, PR #7 oförändrad draft. Ingen implementation, full G5-PASS, PR-merge eller Verification följer av detta dokument.
