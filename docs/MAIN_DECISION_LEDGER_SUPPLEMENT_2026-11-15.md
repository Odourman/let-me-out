# Let Me Out! – MAIN:s kompletterande beslutsregister och aktuell auktoritet

## MAIN VII – LM-D17/LM-D18: exakt A/C/D-kartbeslut och G5V B-grafikuppdrag GODKÄNDA (2026-11-17)

**Direkt senare användarsvar:** MAIN frågade om användaren godkänner **exakt `A_OPEN_01`, `C_OPEN_01`, `D_OPEN_01` som framtida kartbaser** och ett **separat begränsat GRAPHICS II-uppdrag att förbättra B till `B_OPEN_02`**. Svaret var **"Ser bra ut"**, ett direkt avgränsat godkännande av dessa två delar. [Fullt G5V-beslutsprotokoll](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5V_MAIN_VII_A_C_D_EXACT_OPEN_MAPS_USER_APPROVAL_AND_B_OPEN_02_GRAPHICS_ORDER_2026-11-17.md) · [Drive](https://docs.google.com/document/d/11BAB8skxf1EJH7PFXo1mdlZ7MDGMevmRS_eDlhPYikw/edit) · [GRAPHICS II-uppdrag Issue #11](https://github.com/Odourman/let-me-out/issues/11).

| Beslut | Godkänd omfattning | Utesluter |
|---|---|---|
| **LM-D17** | De exakta 40×22-geometrierna för `A_OPEN_01`, `C_OPEN_01`, `D_OPEN_01` i original `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json` är godkända **framtida kartlayoutmål**. | Inte komplett fyra-rums-cutover; ingen käll-JSON-ändring, ROM/avläst Stella, spawn-/kollisions-/raster-PASS. `B_OPEN_01` är inte godkänd. |
| **LM-D18** | MAIN får ge GRAPHICS II ett separat, snävt **source-only-studieuppdrag** att skapa `B_OPEN_02` som luftig, mer varierad 40×22-kandidat. | Ingen B-karta ännu skapad eller godkänd, ingen ROM, G0/G6/F12, godkända spawns eller PR-merge. |

**A1/B1/C1/D1/E1 (LM-D12..D16)** är redan godkända inom tidigare exakt scope. Historiska v0.11-layout-/ROM-prover är frysta. All äldre text om att *alla fyra* v0.19 OPEN-kartor ännu är obeslutade är en historisk tidssnapshot **före LM-D17** och supersederas endast för A/C/D. **G5_FORMAL_OPEN, G6/F12_NOT_AUTHORIZED**.


## MAIN VII – LM-D14, LM-D15 och LM-D16: nya G5S-beslut GODKÄNDA (2026-11-17)

**Senare direkt användarsvar:** Efter MAIN:s uttryckliga fråga "Godkänner du uttryckligen C1, D1 och E1 som framtida spel- och testregler?" svarade användaren "Fortsätt Följ dina egna rekommendationer". I just detta sammanhang gäller **C1+D1+E1 som framtida krav**. [Fullständigt exakt beslutsprotokoll](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1UboARrqu3sFHQgeV1y5C0IWoRkSlvAY_6b6RMLWwbnE/edit). Äldre G5R-texter om "fortfarande endast förslag" beskriver tiden **före** detta användarsvar och supersederas endast för dessa tre rekommendationer.

| ID | Godkänt beslut | Exakt giltighet och gräns |
|---|---|---|
| **LM-D14 / G5R C1** | Framtida versionerat R1-mål med **5 NPC M,M,F,SM,SF**, R2 med **4 kvarvarande + synlig key** efter dödsanimation. | **Testmål godkänt, INTE ett nytt ROM-PASS.** Originalmasker bevaras och v0.18 R1=6/R2=5+key förblir historiskt frysta. Ingen omedelbar teknisk cutover/implementation. |
| **LM-D15 / G5R D1** | För **framtida fem-NPC-spelversion**: **-30 poäng per dödad NPC**, ursprunglig +50 pickup, +100 exit, +15 per överlevande, 0-golv per kill och extralivströsklar oförändrade. | **Framtida spelregel godkänd**; originalets sex-NPC/-25 historiskt oförändrad. För k=5 och ingen poänggolvseffekt blir netto 0 per rum. Ingen ROM-kod ändrad. |
| **LM-D16 / G5R E1** | **5 distinkta, förhandsvaliderade NPC-spawnpositioner** per framtida rum och **uniform sannolikhet 1/5 för key-bärare bland de fem individuella NPC**, inte fyra masktyper. | **Policy godkänd**, men inga specifika startkoordinater/kartor, PRNG-implementation eller faktiska tester godkända. Key faller efter dödsanimation på fysisk/logisk fallplats; K1/O1/E1 fortsatt styrande. |

**A1/B1 LM-D12/13 godkända sedan tidigare.** Fortfarande ÖPPET: exakt v0.19 kartbyte, framtida G0-S05/renderingskernel och uttrycklig G6/F12-arbetsorder. **G5 FORMAL OPEN, G6/F12 NOT AUTHORIZED, NO NEW ROM, NO VERIFICATION, NO PR MERGE.**


## MAIN VII – LM-D12 och LM-D13: godkända G5Q-designmål, 2026-11-17

**Direkt användargodkännande via uttrycklig hänvisning:** På MAIN VII:s omedelbara fråga "Godkänner du G5Q:s rekommendation A1 + B1 som våra fortsatta designmål?" svarade användaren **"Följ dina egna rekommendationer"**. I just denna samtalskontext innebär det godkännande av A1+B1 som **mål**, inte av övriga förslag. [Fullständig spårbar beslutsregistrering](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [Drive](https://docs.google.com/document/d/1Yh5XfKZ8f9rm97sG7jY8tAjuGiV-0o9O-d9oy-BkP2s/edit).

| ID | Senare giltigt användarbeslut | Avgränsning |
|---|---|---|
| **LM-D12 (G5Q A1)** | Fem framtida NPC M,M,F,SM,SF ska **logiskt kunna röra sig individuellt fritt i X/Y**, fyrvägs-jakt och NPC/NPC-kollision bevaras som spelmål. | **Designmål godkänt.** Ingen permanent tyst Y-lane, ingen accepterad renderer eller generell synlighets-/AI-waiver. Framtida v0.18 R1/R2-cutover fortfarande obeslutad. |
| **LM-D13 (G5Q B1)** | Fem fiender ska vara igenkännbara, farliga närliggande fiender får inte systematiskt försvinna; key ska synas när ingen NPC faktiskt pixelöverlappas. | **Kvalitetsmål godkänt.** Ingen numerisk flimmergräns, 10Hz-acceptans eller ny key-hide. **LM-D06/O1** fortsatt giltig enbart vid faktisk pixelöverlappning. |

**Läsordning och auktoritet:** LM-D12/13 gäller senare **designmål** för den framtida femfiendersinriktningen; den äldre LM-D01 med sex fiender och frysta historiska R1/R2-romtester ska inte raderas eller retroaktivt märkas om. Övriga 57 beslut, Master Spec, K1/E1, originalmasker och tillämpliga restriktioner kvarstår. **C/D/E (test-baslinje, poäng -30 kontra -25, 1/5 key-bärare/femspawn, exakta v0.19-kartor) inte godkända; G5 formellt ÖPPEN och G6/F12 inte auktoriserade.**


**Datum:** 2026-11-15  
**Projekt:** enbart `Odourman/let-me-out` / Google Drive-mappen `Atari 2600 - Let Me Out!`.  
**Syfte:** bevara nyare användarbeslut, precisera vad som *inte* är godkänt och ge nya MAIN-/ROM DEVELOPMENT-/VERIFICATION-chattar en entydig ingång.  
**Registerstatus:** komplement till den ursprungliga **57-posters beslutshistoriken** i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip`; ersätter eller skriver inte om det originalet. Konkreta användarbeslut gäller före rådgivande studier. Tidigare daterade dokument med formuleringen "ROM DEVELOPMENT pausad" beskriver sitt **historiska läge** och får inte användas för att upphäva det senare uttryckliga v0.18-tillståndet.

## 1. Aktuella direkta användarbeslut och visuella mål

| ID | Beslut eller preferens | Status och avgränsning | Auktoritativt underlag |
|---|---|---|---|
| LM-D01 | Sex vita, människoliknande androider: 2 stora män, 2 stora kvinnor, 1 liten man och 1 liten kvinna; fyra igenkännbara figurtyper. | **Fastställt spelupplägg.** Inga tysta förenklingar till block, färre NPC:er eller sammanlänkad rörelse. | Ursprunglig 57-beslutshandoff och [exakta ursprungsmasker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json). |
| LM-D02 | Gul spelare med hatt och vapen; **lika stor på skärmen som de stora androiderna**. De små är visuellt mindre. | **Godkänt visuellt mål.** Fortsätt utvärdera 8×9 för spelaren/stora och 8×9 matris med sex synliga rader för de små. Spelarens slutliga bitmap är inte låst. Användaren vill att figurerna ska kännas något mindre än Berzerks och inte dominera rummet; exakt jämförelseskala mot Berzerk är inte mätt. | [MAIN spelarskala](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md), originalmaskerna, användarens förtydligande i chatten. |
| LM-D03 | **Spelaren ska inte framstå som större än dörröppningen.** | **Visuellt/rumsligt mål**, inte nytt numeriskt kollisionsbeslut. Nuvarande skiss med högerdörr y9–12 ger 4×8 = 32 skärmlinjer hög öppning i offline-visualiseringen; faktisk TIA-rendering är inte färdig. | Användarens storleksförtydligande och [v0.19 kartstudie](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md). |
| LM-D04 | **Rummen ska vara luftiga**: få bruna väggpartier som antyder små rum eller avdelningar, men inte bildar en tät labyrint; stor fri mitt-/rörelseyta och breda öppningar. Inspirationskälla: Berzerks enkla rumsformationer, inte kopierade nivåer. | **Godkänd designriktning.** De fyra schematiska öppna rumstyperna har fått positivt användarsvar. Det betyder inte automatiskt att de exakt genererade 40×22-rutmatriserna har godkänts som ny slutgiltig canon. | Användarens direkta beskrivning och godkännande av skisserna; [v0.19-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md). |
| LM-D05 | Fyra rum, endast utgång på **högra** väggen. Stängd vänstervägg. Orange dörrmarkör med svart nyckelhål; guldgul nyckel med runt hål och kort tandat skaft. | **Beslutad spelmekanik/visuell riktning**; exakta TIA-färger, bitmapmasker och teknisk lösning inte verifierade. Dörren och nyckelhålet försvinner tillsammans vid upplåsning, verklig utgång krävs för bonus. | [Godkänt visuellt mål v0.13](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md). |
| LM-D06 | **O1:** android får visuellt skymma nyckeln tillfälligt men nyckelns logiska läge ändras inte; den blir synlig på samma plats efter skymning. | **Godkänt**. Lite, kortvarigt flimmer accepterat, men inte långvarigt oläsbara farliga figurer. | [MAIN-beslut O1](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md). |
| LM-D07 | **K1:** nyckel som skapas under stillastående spelare kan plockas tidigast nästa logiska uppdatering. **E1:** dödlig kontakt vid verklig högerutgång prioriteras före utgångsbonus, förutsatt överlevande android; skottträff på den androiden behandlas först. | **Godkända spelregler**, inte implementerade/verifierade i ROM. | [K1/E1-besluten](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md). |
| LM-D08 | Ingen separat startskärm; efter GAME OVER en Berzerk-inspirerad presentation i samma spelplan. **Endast konsolens RESET** startar om efter GAME OVER, med tre liv och noll poäng; FIRE startar inte om. | **Beslutat grundflöde.** Exakta färgeffekter och tidsintervall är öppna. | [Game Over/RESET-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md). |
| LM-D09 | **Kodauktorisation: endast Atari 2600 NTSC-diagnostik v0.18 R1–R4**, F6 16 KB om tekniskt motiverat, under ROM DEVELOPMENT och separat VERIFICATION. | **Uttryckligen godkänt.** Fullspel, PAL, senare ROM-faser, AI, poängkod, ljudkod, gameplaykartcutover m.m. är **inte** därmed auktoriserade. | [Issue #6](https://github.com/Odourman/let-me-out/issues/6), [autorisationsdokument](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md). |
| LM-D10 | **Omedelbar prioritet inom v0.18:** lös sex androiders individuella X-positionering och läsbarhet med fullstor gul spelare och testsymbolskott. | **Uppgiftsprioritering inom redan auktoriserad R1**, inte nytt fristående utvecklingssteg. Tvåsilhuettsprovet fungerade endast vid NUSIZ-fasta 32/64-avstånd; sex oberoende sprites har ännu inte klarat ROM-test. | [MAIN sex-X-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md), [PR #7](https://github.com/Odourman/let-me-out/pull/7). |
| LM-D11 | Let Me Out! hålls isolerat från **The Cabin** och **I Love a Fish**; **Linear används inte**. | **Projektregel.** Endast detta GitHub-repo och dess dedikerade Google Drive-mapp får ändras inom uppdraget. | Projektets aktuella MAIN-dokument och användarens tidigare direktiv. |

## 2. Fyra nya exakta kartor – resultat, men inte automatiskt godkänd ersättning

Användaren godkände den **öppna rummens designriktning**, och bad därefter MAIN skapa och kontrollera exakta 40×22-matriser. Det uppdraget är utfört som **v0.19 design-/offline-studie**. De exakta rutplaceringarna nedan är dock ännu **förslag**; det finns inget uttryckligt separat beslut som byter ut den tidigare, källvalda kartbasen **A01/B01/C02/D01** (inklusive det tidigare explicita valet av C02).

| Kandidat | Beskrivning | Nya innerväggar / 760 innerrutor | Reachable 2×2-ankare (offline) | Tidigare karta |
|---|---|---:|---:|---|
| `A_OPEN_01` | Fyra L-formade hörn, fri mittarena | 36 = 4,74 % | 623/623 | A01 |
| `B_OPEN_01` | Fyra dubbla väggstumpar, öppet mittparti | 48 = 6,32 % | 619/619 | B01 |
| `C_OPEN_01` | Hörn som antyder små rum, stora öppningar | 64 = 8,42 % | 579/579 | C02 |
| `D_OPEN_01` | Väggarmar och fri mittarena | 60 = 7,89 % | 591/591 | D01 |

**Gemensam bevarad geometri:** 40×22; inre väggar speglas; brun vägg, svart spelplan; vänster gräns stängd; dörr på **x39, y9–12**; spelarstartankare x2/y10. En kartcell är 4 horisontella TIA-färgklockor × 8 vertikala förhandsvisnings-scanlines i offline-skissen. Dessa pixel-/färgdetaljer är inte ännu godkänd ROM-rendering.

**Reproducerbara filer:** [v0.19 JSON](https://github.com/Odourman/let-me-out/blob/main/design/OPEN_ROOMS_V019_40x22_CANDIDATES.json), [MAIN-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md), [Drive ZIP](https://drive.google.com/file/d/1kO38zm26fFSwu0cAnwQYAZ56D52HrJvK/view), [mobilrapport](https://drive.google.com/file/d/197ssAX79Zqdmwl0V5W3xLhDVKMwgYYw3/view). **Historisk originalbas:** [v0.11](https://github.com/Odourman/let-me-out/blob/main/design/PLANERADE_RUMSKARTOR_V011.json).

**Offlinebevis och gränser:** Alla lagliga 2×2-fotankare i varje rum var nåbara, en öppen väg till högerdörren fanns och minst sex separata startankare fanns. Dessutom gjordes 100 deterministiska, förenklade dynamiska trafiktester per rum (400 totalt); spelaren nådde dörren inom 180 modellsteg i 400/400. Ingen faktisk P2/J2-jakt, 8×9-spritekollision, full diagonalförflyttning, 2600-ROM eller Stella-test ingick. Testerna bevisar **inte** att ingen någonsin fastnar i spel.

## 3. Öppna val – får inte omtolkas till beslut

- **Slutlig uppsättning kartor:** de exakta `A_OPEN_01`–`D_OPEN_01` är *kandidater*. Bevarade v0.11-kartor är tills vidare känt källval. Byte kräver användarens explicita val efter fortsatt granskning.
- **Kollisionsrektangel:** 6×6 för spelaren/androiderna har diskuterats som en **möjlig framtida testkandidat**, inte ett godkänt byte från existerande logik. Stor och liten android ska fortsatt ha **samma logiska kollisionsyta** enligt det gamla beslutet.
- **Diagonalt väggglid:** rekommendation för smidig spelkontroll, **inte** implementerat eller uttryckligt godkänt som konkret rörelseregel.
- **Minimala korridorbredder och väggtjocklekar:** tidigare MAIN-förslag (t.ex. 12 färgklockor fritt vågrätt, 16–24 scanlines vertikalt) är **riktvärden**, inte låsta dimensioner och inte testad hardware-acceptans.
- **Slutlig spelarbitmap, exakt Berzerk-skaljämförelse, guldnyckelmask och färgkoder** kräver speltest och/eller uttrycklig senare formbedömning. AI-genererade jämförelsebilder är *skisser*, inte Stella-skärmbilder.
- **S0/S1 spawnjusteringar, P2/J2 AI, hastighet C-1, HUD och fullspelsstart** är tidigare förstudier där annat inte uttryckligen har godkänts.

## 4. Oavslutad ROM-diagnostik och verifieringsspärr

- Utvecklargren `rom-dev/v018-ntsc-diagnostic`, [draft PR #7](https://github.com/Odourman/let-me-out/pull/7). Senast kontrollerad utvecklar-HEAD: `f5c06f352ba8653f3ce65bbc3e5e392c892beec5`; PR ska **inte** mergas innan oberoende verifiering och MAIN:s mottagning.
- Fryst originalbaseline: `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, med [separat VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8). Nya commits behöver egen oberoende bedömning, inte ärvd PASS.
- Faktiskt bevisat i Stella: 2 olika originalmasker (stor man/stor kvinna) med **fasta** NUSIZ-kopieavstånd 32/64 färgklockor, plus synlig gul spelarkandidat och skott. **Sex oberoende androider är fortfarande inte godkända**, och 600-frame scanlineloggar saknas. Allt nytt här ovan om kartor hör till **design/offline**, inte den redan godkända v0.18 ROM-implementationen.
- Ingen senare cutover, PAL, fullspel, nya AI-/poäng-/ljudimplementationer eller kartbyte får ske tyst eller bara genom att en ny rapport publiceras.

## 5. Vart nästa arbetschat ska börja

1. Läs denna beslutslogg och [aktuellt projektläge](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md). Kontrollera sedan originalbesluten i handoffen och senaste källor som är relevanta för uppgiften.
2. Skilj **GODKÄNT BESLUT**, **VISUELL RIKTNING**, **KANDIDAT**, **OFFLINE-MODELL**, **KÖRBAR STELLA/ROM** och **OBEROENDE VERIFICATION** i varje rapport.
3. Kontrollera alltid faktisk PR-head och Issue #8 i GitHub, och respektive källmaterial i Drive; anta inte att HEAD/hash aldrig ändras efter detta dokument.
4. Bevara historiska beslut och filer. Vid senare godkännande: lägg till ett **daterat delta eller uttrycklig supersession** i stället för att tyst radera äldre beslut. Ingen automatisk överflyttning från designspår till ROM-spår.

**Arkivering:** samma text lagras i GitHub och Google Drive. Detta register är ett tillägg, inte en ny generell rätt att implementera.
