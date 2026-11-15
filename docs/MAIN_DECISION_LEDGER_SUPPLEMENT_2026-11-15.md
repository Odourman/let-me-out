# Let Me Out! – MAIN:s kompletterande beslutsregister och aktuell auktoritet

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
