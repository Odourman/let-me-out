# LET ME OUT! – GRAPHICS II / G5V: B_OPEN_02

**Datum:** 2026-11-17  
**Status:** `G5V_GRAPHICS_SOURCE_ONLY_DELIVERED / B_OPEN_02_NOT_APPROVED / NOT_STELLA / NO_ROM`.  
**Beställare:** MAIN VII, [Issue #11](https://github.com/Odourman/let-me-out/issues/11).  
**Utförare:** GRAPHICS II.

## 1. Auktoritet och originalkällor

- MAIN VII G5V användarbeslut: [`G5V_MAIN_VII_A_C_D_EXACT_OPEN_MAPS_USER_APPROVAL_AND_B_OPEN_02_GRAPHICS_ORDER_2026-11-17.md`](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5V_MAIN_VII_A_C_D_EXACT_OPEN_MAPS_USER_APPROVAL_AND_B_OPEN_02_GRAPHICS_ORDER_2026-11-17.md) och samma beslut i officiella [Drive](https://docs.google.com/document/d/11BAB8skxf1EJH7PFXo1mdlZ7MDGMevmRS_eDlhPYikw/edit).
- Källans `main` HEAD vid studieutgång: `80bf072ee0e8a9a84905a29d70771a7cc6be7820`.
- Historisk källa: `design/PLANERADE_RUMSKARTOR_V011.json` blob `820a74e5fb77c818ffb1286c5b23698d4374e771`. `B01` är historisk referens.
- Tidigare öppen kandidat: `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json` blob `0e449f97f87bd9b403476fd1435398042eaee285`. `B_OPEN_01` är EJ godkänd.
- MAIN:s G5U-mottagning av G5T och beslutsgräns G5 kontrollerade, liksom v0.11:s och v0.19:s faktiska B-matriser och `candidate_positions`/`reusable_old_S0_candidates_for_geometry_only`.
- Senare användarbeslut LM-D17: `A_OPEN_01`, `C_OPEN_01` och `D_OPEN_01` är **godkända exakta framtida kartmål**, men ännu inte ROM-implementerade; de ändras INTE här. LM-D18 ger endast en B-studie, inte ett B-kartgodkännande.

## 2. Det nya exakt definierade förslaget

`B_OPEN_02.json` är en ny, fristående 40×22-kandidat med 880 faktiska celler. Svart bakgrund `.`, brun vägg `#`, och orange **kartmarkering** `D` på endast högerkanten x=39, y=9..12. Stängd vänsterkant x=0 och övre/nedre kant. Origo övre vänstra hörnet; x åt höger, y ned. Spelarens gamla 2×2-modellankare kvar på (2,10).

Utgångspunkt i B_OPEN_01:s övergripande luftiga, fyra-väggdelade princip, men de tidigare raka pelarna **ritas om till korta, tvåsidigt speglade, övre och nedre väggarmar**. Väggarna skiljer sig mellan övre och nedre delen för variation. Två små centrala hinder finns utanför mittkorridoren. Rader y=9..12 är helt öppna från x=1 till x=38, så att utgångspassagen inte stryps. Det är ingen tät labyrint.

Designändring i exakt kartdata jämfört med B_OPEN_01: **48 celler tillagda som vägg; 24 tidigare väggceller blir öppna; 4 D-celler orörda.** B_OPEN_02 har **72 innerväggceller av 760** och **90.53% fri yta**.

## 3. Kvantitativ jämförelse, samma offline modell

| Karta | Innerväggar / 760 | Öppen interiör | 2×2: tillåtna / nåbara | B01-ankare återanvändbara / 13 | Spelare till högersidans dörrnärhet, 4-vägs steg |
|---|---:|---:|---:|---:|---:|
| B01          | 156 | 79.47% | 439 / 439 | 13 | 40 |
| B_OPEN_01    | 48 | 93.68% | 619 / 619 | 9 | 35 |
| B_OPEN_02    | 72 | 90.53% | 565 / 565 | 13 | 35 |

B02 har **565 av 565 2×2-ankare nåbara** från spelare (2,10) i denna modell, **0** otillgängliga 2×2-ankare och **0** artikulationspunkter i ankargrannskapsgrafen. Det betyder att bortfall av ett enda *2×2-ankar-läge* inte delar upp den grafen i två delar, men kan inte ersätta rörelsetest med olika aktiva fiendekroppar. Sista dörrposition x=39 antas vara ett kartmarkerat låst hinder, inte en automatiskt passabel cell. Testad dörrnärhet är (37,9),(37,10),(37,11), varav den kortaste nås på **35** steg; faktisk övergång genom en upplåst dörr är **inte** testad.

**Återanvändning av gamla kandidater:** B01:s `13` av `13` gamla `candidate_positions` klarar geometriskt 2×2-test i B02. Det är en förbättring mot B_OPEN_01:s 9/13, inte fem spelvaliderade spawns. Som tydligt markerat icke-beslutat *illustrativt femtal*: `[[9, 3], [29, 3], [19, 9], [9, 15], [29, 15]]`, varje 2×2 kvadrat separat och minst 10 rutors Chebyshev-ankarseparation. Spelaren (2,10) och alla fem kandidatankare är i samma BFS-komponent. Ingen likformig spawnslump eller faktisk 8×9-kollision har prövats.

## 4. Begränsad grafisk riskgranskning

- **B01** har egen pelarhallsidentitet men 156 innerväggar och känsla av tät hinderbana.
- **B_OPEN_01** är tydligt öppet och enkelt, men fyra nästan identiska pelare kan ge för lite variation och triviala raka vägar.
- **B_OPEN_02** har 72 innerväggar, stegvisa väggarmar och små centrala hinder, med en sammanhängande mittarena och breda öppningar. Det är min rekommenderade **grafikkandidat för ett separat B-val**. Spegelbar innervägg, inte spegelbar högerdörr. Den är inte nödvändigtvis taktiskt bäst i verklig fiendejakt.
- **Kontrollbehov:** även om 2×2-grafen inte har artikulationspunkter kan faktiskt aktiv NPC/NPC-blockering, fler hinder i siktlinjen, 8×9 collision/feet scale, jakt-AI och nyckelfall ändra framkomlighet. Den öppna mittkorridoren kan också göra spelarens flykt alltför enkel. Varken detta eller väggarnas NTSC/TIA/PF/BL-fysiska implementerbarhet kan bedömas definitivt från offlinegrafiken.

## 5. Exakthetskontroll och reproduktion

Reproduktionsskriptet `build_g5v.py` läser två särskilt märkta **B-excerpter** i `source_snapshots/`, och kan i en repo-checkout köras med `--repo-root` så att de **exakta original-JSON-filerna** läses. Scriptet jämför båda källkartorna med låsta **FNV-1a 32-bit-värden** `B01=d94133dd`, `B_OPEN_01=7746b1c9` och konstruerar sedan B02 genom uttryckligt listade symmetriska rektangeloperationer, utan att skriva i originalet. Fryst B02-checkvärde: `c9e29f45` (FNV32), SHA256 över dess 22 rader plus avslutande newline: `7ac4ce94398c098e5f1922afd8aa59d115fa33fac2e86ddc9c885f6a4c82995a`.

Alla tre separata rena PNG-kartor verifierades mot respektive 880-cellsmatris genom att varje runcellcentrums RGB lästes tillbaka ur filen; **2640/2640**, noll fel. Även alla **2640/2640** cellcentrum i den horisontella 3-kartorsbilden kontrollerades. Jämförelsebilderna är deterministiska offlinebilder, **inte** faktiska Atari 2600- eller Stella-skärmbilder. Dörrens svarta nyckelhål tillhör ett separat ännu tekniskt obevisat visuellt mål och har inte modifierat den enda D-kartkolumnen.

Bilagor: `B_OPEN_02.json` (ny B-matris), `B_OPEN_02.grid.txt`, råa PNG/SVG för B01/B_OPEN_01/B_OPEN_02, `G5V_B_TRIPTYCH.png`, `G5V_B02_START_ANCHORS.png`, `G5V_B01_TO_B02_DELTA.png`, `VALIDATION.json`, `build_g5v.py`, `source_snapshots/`, `SHA256SUMS.txt`.

## 6. Förslag till MAIN VII:s explicita nästa användarfråga

**"Vill du godkänna den exakta nya 40×22-kartan B_OPEN_02 som planerat framtida rum B, tillsammans med redan godkända A_OPEN_01, C_OPEN_01 och D_OPEN_01?"**

Betona att detta är ett *beslut om framtida exakt kartgeometri*, inte ett genomfört ROM-kartbyte. Den nya B-layouten har en bättre visuell variation än B_OPEN_01, men behöver senare oberoende tekniska tester, fem faktiska förhandsvaliderade spawns och en separat authorization gate. Ett nej får behålla B01-historiken och öppna för ytterligare B-kandidat, **inte** retroaktivt låsa B_OPEN_01.

**Stopp:** GRAPHICS II levererar en rådgivande kandidatkarta. Ingen ändring av A/C/D, canon, AI, originalmasker, spelregler, ROM-kod, G0/G6/F12, PR-merge eller oberoende Verification.


## GitHub-renderer

GitHub tillhandahåller också `render_g5v.mjs`, en oberoende source-pinnad Node.js-generator som regenererar SVG, B_OPEN_02.json och BFS-kontroller. Lokalt `build_g5v.py` samt reproducerbara PNG finns i Drive ZIP: https://drive.google.com/file/d/15-krJ-7Ga_Lyd_LrwEJnao_-637LCYP_/view
