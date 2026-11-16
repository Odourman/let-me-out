# Överlämning till MAIN – ny 26-trick-serie: #10, #08, #05 testade i verklig Stella

**2026-11-16. Scope:** enbart rådgivande, reproducerbara standard NTSC/F6-teknikexperiment. Ursprunglig numrering ur `main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md`; **27–30 är uteslutna** enligt användarbeslut. Inget nytt implementationssteg, fullspel eller oberoende VERIFICATION.

**Levande 26-poster-register:** [MAIN_II_26_F6_TRICKS_TEST_REGISTER_2026-11-16.md](MAIN_II_26_F6_TRICKS_TEST_REGISTER_2026-11-16.md).

## Tre nya praktiska DASM + Stella-resultat

| Nr | Trick | Faktisk körning | Utfall inom begränsat scope |
|---:|---|---|---|
| **10** | HMOVE Fine Positioning | [Actions #43813500872](https://github.com/Odourman/let-me-out/actions/runs/43813500872) | **PASS 4/4**: P0 och dess P0-wide-android förflyttas tillsammans 0/+1/+3/−3 TIA CC, andra tre P1-originalmasker och M0 statiska. 262 NTSC, alla originalbitar exakta. Fjärde NPC:s X förblir bunden till P0 med +64 CC |
| **08** | Two-Line Kernel | [Actions #43813868438](https://github.com/Odourman/let-me-out/actions/runs/43813868438) | **NEGATIV VARIANT:** 262 NTSC och 9 originalbitmaprader bevarade som data, men dessa upptar 18 fysiska rasterrader. 8×9-geometri och testad spelares ursprungliga 9-radersband FAIL |
| **05** | Dynamic Playfield Sprites | [Actions #43814436467](https://github.com/Odourman/let-me-out/actions/runs/43814436467) | **PASS 4/4 i separat höjdband:** brun PF1-figur flyttas i 4-CC-steg och genererar fast extra PF-kopia +80 CC, fyra original-8×9 androider och gul P0/M0 helt intakta på sina egna rasterrader |

### Bevis- och källsökvägar

- Trick 10: [mät- och SHA-rapport](MAIN_II_TRICK10_HMOVE_REAL_STELLA_LOCAL_PASS_2026-11-16.md); branch `research/main-ii-26-tricks-hmove10-20261116`. Artefakt **14201063902**, F6 16KB SHA256 `702c5c9534e5486881441a43c60dea85d0ca02093dae4d56d237202f7c6d2c18`. Tre TIA-originalmasker i P1 vid GUI-X 154/268/400; gul P0 vid 188/190/194/182 och vit P0-kopia vid 316/318/322/310. Samtliga fyra screenshot-faser PASS. Verkligt HMOVE PC-stop `$F07C` / scanline4 / CPU-cykel0 / bank0, före instruktionen.
- Trick 08: [negativt Stella-utfall](https://github.com/Odourman/let-me-out/blob/research/main-ii-trick08-two-line-20261116/docs/MAIN_II_TRICK08_TWO_LINE_REAL_STELLA_NEGATIVE_VARIANT_2026-11-16.md); branch `research/main-ii-trick08-two-line-20261116`. Artefakt **14201139080**, kontroll-ROM SHA `84083e1c01de7ab0347ac18e85bdf36f37a6a7a201dd060f1f5248020459e24a`, tvålinje-ROM SHA `f862edc97acbb5bf7f4f7d1442235ffa5138196bece82e16eec5b8c4c8f0bbac`. Kontroll 0 bitmapfel; tvålinje original 9-y-band 56/56/32/36 dubblerade GUI-pixelfel för fyra NPC och 64 för gul P0. Varannan fysisk rad ger 0 bitmönsterfel för de fyra NPC – alltså **källan ändras inte men höjden fördubblas**.
- Trick 05: [PF-resultat och rastergränser](https://github.com/Odourman/let-me-out/blob/research/main-ii-trick05-dynamic-pf-20261116/docs/MAIN_II_TRICK05_DYNAMIC_PF_STELLA_LOCAL_PASS_2026-11-16.md); branch `research/main-ii-trick05-dynamic-pf-20261116`. Artefakt **14201971767**, fyra 16KB F6-ROM:er; alla fyra PF1-förskjutningar och kopian på andra halvskärmen uppmätta i rå Stella 6.7.1-bild. 4/4 262 NTSC, fyra original-NPC 72/72 per mask, gul P0, M0 exakt, inga extra objektpixlar i NPC-bandet.

## Tekniska konsekvenser för Let Me Out!

1. HMOVE är användbart **för finförskjutning**, men skapar varken fler TIA-sprites eller oberoende P0-kopior. Ingen R1-uppgradering.
2. Enkel tvålinjers-interfoliering ger CPU-tid på bekostnad av ursprunglig fysisk 9-radershöjd; det är en negativ observation för den testade koden, inte alla VDEL-/two-line-arkitekturer.
3. PF kan producera extra grov form i separat höjdband, men konkurrerar med bruna väggar och högerdörr. Två PF-kopior med fast avstånd är inte två fria nya humanoider, och PF:s 4-CC-pixlar duger inte automatiskt som 8-bitars originalmasker.
4. Förutsättningen `R1e` fyra originalmasker **statiskt** 600/600 [Actions #43812461127](https://github.com/Odourman/let-me-out/actions/runs/43812461127) finns kvar med ursprunglig F6 SHA `84083e1c01de7ab0347ac18e85bdf36f37a6a7a201dd060f1f5248020459e24a`. Den fjärde androidens X är kopplad till gul P0 med +64 TIA-CC; det är fortfarande inte fritt fyra-X eller sex-X.

## Föreslagen fortsatt 26-trick-ordning, EJ här utförd

Nästa icke duplicerande försök: **07 Asymmetric Playfield** med vänster vägg och höger dörr i samma band, följt av **25 Stack-Based TIA Register Tricks** som säkerhetsavgränsat buss-/cykelexperiment; sedan **11 Late HMOVE** och **13 48px/HUD**. Behåll exakt originalmask, 76-cykelrad, 262 NTSC, P0/M0 och 600-frame-grind där det är relevant. För kommande tester som kräver en specialcart får 27–30 **inte** testas.

## Hård auktoritets- och scopegräns

Rapporten är **RESEARCH**, inte ROM DEVELOPMENT-implementation och **inte** oberoende VERIFICATION. Ingen ändring av spelregler, canon, karta, fullspel, PAL, cartridgeformat, `main`, draft PR #7 eller Issue #8. MAIN får besluta om prioritering/auktorisation separat. Full R1 med sex ursprungliga individuellt fritt placerade androider på samma Y och hela PF-/spelarbördan förblir **BLOCKED**.
