# LET ME OUT! – MAIN VII G5Q: G5-beslutsunderlag efter G5P

## MAIN VII tillägg 2026-11-17 – senare avgränsat användargodkännande

Efter detta beslutsutkast frågade MAIN VII uttryckligen om användaren godkände **G5Q A1+B1 som fortsatta designmål**. Användaren svarade **"Följ dina egna rekommendationer"**. Därmed är **A1 och B1 godkända som produkt-/kvalitetsmål** enligt [senare exakt beslutsregistrering LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) och [Drive-kopia](https://docs.google.com/document/d/1Yh5XfKZ8f9rm97sG7jY8tAjuGiV-0o9O-d9oy-BkP2s/edit). De ursprungliga `DRAFT`-/`USER_DECISION_PENDING`-formuleringarna nedan är historiskt utkast, **supersedade endast för A1+B1**, inte för C/D/E. Ingen ROM-implementation, renderingswaiver, R1/R2-cutover, poängändring, kartbyte, G5-PASS eller G6/F12-uppdrag följer.

**Datum:** 2026-11-17. **Status:** `G5Q_USER_DECISION_PACKAGE_DRAFT_NO_CANON_CHANGE`. **Inte:** användarbeslut, ny ROM-order, G0/G6/F12-auktorisation, grafikwaiver, PR-merge eller oberoende Verification.

## 1. Varför G5Q
G5P levererades av RESEARCH II på separat branch och MAIN VII reproducerade source-only resultaten. Det finns nu inget behov av att beställa samma AI-offlineutredning igen. Vi behöver i stället avgränsa vilka **produktmål** användaren vill hålla fast vid och vilka **eventuella kompromisser** som alls kan prövas senare.

**Källhierarki:** Originalets 57 beslut och Master Spec med senare uttryckliga supersessions är styrande. G5P är rådgivande forskning, inte spelcanon. [MAIN VII mottagningsrapport](G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md), [RESEARCH II original](https://github.com/Odourman/let-me-out/blob/research/g5p-adaptive-y-offline-20261117/docs/research/G5P_RESEARCH_II_FULL_REPORT_2026-11-17.md), [G5 formella spärr](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), [beslutsregister](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), [G4 teknisk förregistrering](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [G5M poäng/spawn](G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md). O1/LM-D06 godkänd endast vid faktisk key/NPC-pixelöverlappning.

## 2. Forskningsfynd som driver vägvalet, inte slutlig kernel
- v0.11 84 fall per policy: 2,869 unika hot-NPC strikt girig, 3,155 strikt adaptiv, 4,048 mjuk/fri logisk rörelse i deterministisk 2×2-modell; 30-ticks-stall 84/84 i båda hårda varianterna och 67/84 i mjuk/fri modell. `soft` och `free` har samma logiska AI i denna studie, inte två oberoende framgångar.
- En konservativ `soft`-kö bortprioriterade 498,6 av 900 NPC×tick-visningstillfällen i genomsnitt på v0.11, **inte** bevisad fysisk flicker/procent synliga sprites. Denna enkla modell är inte en acceptabel verifierad renderer.
- S05 player+vit NPC+guldkey+orange P1-dörr+M0+brun PF: originalmask med pixelöverlapp (13) kontra same-Y utan pixelöverlapp (0). O1 gäller endast faktiska överlappningen; nollöverlappande key får inte tas bort. Ingen komplett register-/CC-/timing-säker F6-kernel är visad.
- Resultaten är source-only offline. Ursprungliga F11 G0 FAIL och andra negativa tester består.

## 3. BESLUT A – fri logisk rörelse kontra bindande Y-lane
**MAIN rekommenderar A1 som produktmål, inte som redan visad implementation:**
- **A1:** Fem individuella NPC ska logiskt kunna röra sig fritt i både X och Y med ursprunglig fyrvägs-jakt, NPC/NPC-kollision och framkomlighet; renderingssystemet får använda situationellt val av kanaler som en *forskningskandidat* men får **inte** tyst förändra AI-rörelsen, frysa vissa NPC i permanenta Y-banor eller radera spelobjekt ur logiken. Låst dörr och nyckel bibehålls. Ingen särskild osynlighets-/flimmerwaiver beviljas av A1.
- **A2:** Acceptera uttrycklig begränsad Y-ordning med påvisad jakt- och spelbarhetskostnad; kräver separat, detaljerad rörelseregel och godkännande efter användardemonstration.
- **A3:** Inget nytt gameplaymål låses ännu; befintliga originalbeslut och senare uttryckligt fem-NPC-mål kvarstår, teknisk osäkerhet accepteras.

**Behov:** användarens uttryckliga val A1/A2/A3. Ett allmänt "fortsätt" är INTE ett designbeslut.

## 4. BESLUT B – visuell kvalitet, inte generell flickerlicens
**MAIN rekommenderar B1 som preliminär kvalitetsmålspecifikation, inte ett retroaktivt O1-tillägg:**
- Alla fem fiender ska förbli identifierbara som sina originala M/M/F/SM/SF-silhuetter, och farliga närbelägna fiender får inte systematiskt försvinna så att spelaren förlorar möjlighet att förutse kontakt.
- Guldnyckeln är synlig på rätt plats om ingen fiende faktiskt täcker dess pixlar, även om den delar **raster-Y** med fiende/dörr. O1 tillåter endast tillfällig skymning vid verklig pixelöverlappning. Dörrens svarta utskurna nyckelhål och orange färg är fortsatt mål.
- Varken 10Hz, generellt dold key vid same-Y eller ospecificerat regelbundet NPC-bortfall accepteras automatiskt; ett kvalitativt godkännande av "lite kort flimmer" är inte en ny global visningsregel.
- **Mätbara testmål** (framtida kontroll av faktisk 60Hz Stella-kernel): andel fullständigt synliga frames per NPC, längsta följd helt osynliga frames, närhet/fara, verkligt pixelöverlapp och synlighetsprofil under S05. Ingen godtycklig numerisk tolerans sätts här före faktisk visuell prototyp och ett separat användarbeslut.
- **B2:** Användaren väljer i framtiden ett specifikt kvantifierat, demonstrerat flimmeravsteg efter att ha sett konkreta situationer; kräver ny separat acceptans och får inte antas av detta dokument.

Det räcker nu med att välja **B1 som önskat kvalitetsmål**, inte en garanti att en teknisk lösning finns.

## 5. BESLUT C – fem-NPC-rebaseline och originalmasker
**MAIN rekommenderar C1 som ett framtida separat versionssatt produktmål:** fem vita NPC M,M,F,SM,SF, med alla fyra ursprungliga TOP-DOWN 8×9-masktyper oförvanskade och framtida diagnostik R1(fem), R2(fyra+key). **Historisk v0.18 R1(sex)/R2(fem+key) är fortfarande oförändrade frysta referenser och ingen ny acceptans är utförd.** Ny versionssatt R1/R2-acceptans skulle behöva godkännas uttryckligt; inga äldre ROM-bevis kan skrivas om. Fem är redan uttryckt som önskad spelriktning, men test-baslinjens formella revision återstår.

## 6. BESLUT D – femfienderspoäng, spawn och key
**MAIN rekommenderar D1 (endast framtida spelregel):** -30 per dödad NPC i stället för ursprungliga -25; övriga +50 pickup, +100 exit, +15 per överlevande, golv 0. Utan nollgolv påverkan: `225-45k` för k dödade av fem; all-kill k=5 ger netto 0 i stället för +25. Det följer originalets avsikt att all-kill inte ger hållbar highscore-tillväxt. **D1 kräver eget uttryckligt userbeslut och får inte implementeras av ett allmänt "fortsätt".** Alternativet D2 är att behålla -25 och öppet acceptera +25/rum vid all-kill eller välja ny regel senare.

**Spawn/key:** om framtida femfiendersversion godkänns måste fem distinkta, kollisions- och nåbarhetsprövade starter väljas ur beslutade kartor. Ett framtida uniformt 1/5-val av exakt en nyckelbärare är rimligt, men kräver beslut och verklig PRNG-/rums-/key-logik-test. G5N:s statiska och G5P:s dynamiska simuleringar är inte fullspelspass.

## 7. BESLUT E – kartbas
Luftiga rum LM-D04 är redan godkänd **designriktning**. Exakta v0.19 A/B/C/D_OPEN_01 är **kandidater**, inte ersättning för baslinjen A01/B01/C02/D01. MAIN rekommenderar att exakta kartbytet **avvaktas tills** användaren kan jämföra dem visuellt och G5-kernelkrav är klarare; under tiden bevaras v0.11 som källbas och v0.19 som jämförelsedata. Kartbyte kräver eget val.

## 8. G5-beslut får inte smygauktorisera G6
**Förberedda tekniska frågor, INTE arbetsorder:**
1. G4 H4-ONE är äldre source-only förregistrerad hypotes med både P0 gul/vit i två numeriska X-ordningar, M0 skott, brun PF och P1 vita NPC. G5P föreslår ännu snävare inledande P0-gul/vit+M0+PF-förprov. MAIN måste före någon framtida order välja en **exakt** G0-konfiguration och falsifierande X/CC-scenarier; de två underlagen kan inte oreflekterat utges som samma acceptans.
2. Stoppa redan vid G0 om 6507-cykler, RESP/GRP/START, färgregister, 128B RAM/stack eller F6-banklayout inte går ihop. Ingen ROM beställs utan en ytterligare, uttrycklig ROM-order.
3. S05 key+door+white+player+skott+PF är ett **eget framtida integrations-/hard-stop-villkor**. Ett isolerat 2-aktörers G0-PASS eller en historisk statisk R3-dörr ger inte 5-NPC fullspelspass.
4. ROM DEVELOPMENT III ansvarar för auktoriserad implementation, VERIFICATION II granskar separat. Researchbranch från G5P förblir separat från main; ingen merge följer av G5Q.

**Gate:** `G5Q_USER_DECISION_PENDING`; `G6_NOT_AUTHORIZED`; `NO_ROM`; `NO_CANON_CHANGE`.

## 9. Beslutsordning för minsta användararbete
- **Nu:** fråga endast om A1 och B1 som **designmål**, inte godkänd teknisk lösning. Användaren kan säga "Jag godkänner G5Q A1+B1 som designmål" om detta stämmer med deras vilja.
- **Därefter separat:** formell fem-R1/R2-rebaseline, -30 kontra -25, 1/5 nyckelbärare/fem-spawn, kartbas.
- **Mycket senare separat:** ett exakt förregistrerat G0/G6-scope före eventuell ROM. Inget automatiskt godkännande genom en G5-designmålstext.

**MAIN:s rekommendation:** bevara spelvisionen och undvik att lova en tekniskt obevisad renderer. Den faktiska genomförbarheten blir en ny gate först efter relevanta userbeslut och separat auktorisation.
