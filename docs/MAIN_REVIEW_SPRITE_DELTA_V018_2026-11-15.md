# LET ME OUT! – MAIN:s granskning av tvåsilhuettsprovet, v0.18

**Datum:** 2026-11-15  
**Roll:** MAIN, mottagnings- och teknisk källgranskning. Inte oberoende VERIFICATION.  
**Scope:** Enbart redan godkänd NTSC-diagnostik v0.18, R1–R4. Ingen fullspelsutveckling, PAL, senare implementation eller designändring.

## 1. Exakt leverans och källor

- Utvecklingsgren: `rom-dev/v018-ntsc-diagnostic`.
- [Draft PR #7](https://github.com/Odourman/let-me-out/pull/7) är **öppen, inte mergad**.
- Ny PR-head/utvecklarcommit: `f5c06f352ba8653f3ce65bbc3e5e392c892beec5`.
- Ursprunglig fryst baseline för [oberoende VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8): `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, fortfarande separat och orörd.
- [Utvecklarens rapport](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/two_silhouettes/TO_MAIN_2026-11-15.md), [källkod](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/two_silhouettes/proof_nusiz.asm).
- Utvecklarens ZIP: `LetMeOut_v018_SpriteFeasibility_Delta_2026-11-15(1).zip`, **53 arkivposter, SHA-256** `675bfcf17343bccdd2bf2d5843dcf77738d9d0521fa5e9ae606bd52eabbf03b6`.
- Paketet innehåller tre separata 16 384-byte F6-binärer och en inbäddad historisk baseline, inte en uppdaterad full R1–R4-ROM.

## 2. MAIN:s faktisk kontroll av artefakter

- ZIP-strukturen testad: **inga fel**. Samtliga **52 av 52** interna SHA-256-poster i `SHA256_MANIFEST.txt` kontrollerades mot extraherade bytes med oberoende hashberäkning.
- NUSIZ-provet har ROM SHA-256 `a945ab5a0b91df9c6583d46aeebc717a3b5b13232b3fa606fc15412727b26fe5`.
- Pixelprov från **råa, obeskurna Stella Debugger-bilder** `evidence/stella_original/nusiz/near|far/stella_debugger_full.png`. MAIN läste åtta pixelkolumner × nio rasterrader vid rapporterade koordinater med två visningspixlar per TIA-färgklocka. **Alla fyra observationer** (stor man/stor kvinna × 32/64 färgklockor) motsvarar exakt de 8×9-masker som ligger i `design/NPC_REFERENCE_8x9_masks.json`: **72/72 bitar per figur och testläge**. De två stora silhuetterna går att skilja åt i originalbilden.
- Gul spelarkandidat och testskott är synliga; spelarens *slutgiltiga* bitmap/hatt/vapen är inte separat godkända. Ingen pixelmaskregel eller hitbox är ändrad.
- GitHub Actions [run 43752235843](https://github.com/Odourman/let-me-out/actions/runs/43752235843) är genomförd med **SUCCESS**, på kodcommit `324e1261c7872b54c2bc25e759c86f969c3274aa`. Efterföljande HEAD `f5c06f3...` lägger till **endast rapport/ZIP/manifest/testsammanfattning, inga ändringar i assemblerkällkoden** enligt GitHub commit-jämförelse. CI-grönt betyder inte R1 PASS.
- Varken DASM eller Stella har körts *på nytt av MAIN lokalt* i denna granskning; råa skärmbilder och utvecklar-CI har kontrollerats. Oberoende VERIFICATION återstår.

## 3. Resultat utan sammanblandning av testnivåer

| Prov | Utfall | Vad det faktiskt bevisar / inte bevisar |
|---|---|---|
| A1: P1-ompositionering två gånger per scanline | FAIL | Inga vita androider syns; bevisar **inte** att all sådan teknik är omöjlig. |
| A2: NUSIZ med separata GRP1-bitmaps | **LOKALT DELPROV PASS** | Exakta stora man/kvinna-bitmapper i två fasta X-konfigurationer (32/64 färgklockor), med gul nio-raders spelare och testsymbolskott. |
| A3: alternativ RESP1-ompositionering | FAIL | Två vita androidsilhuetter saknas även i detta schema. |
| 600 konsekutiva Stella `frame #1`-kommandon | INCONCLUSIVE | Slutbild visar frame 610 och senast 262 scanlines; `saveSes` gav **0 byte**, så 600 individuella scanlinevärden är inte bevarade. |
| Fullt R1, sex självständiga androider | **BLOCKERAD** | Inte implementerat eller visuellt verifierat med de nya 8×9-silhuetterna. |
| R2/R3/R4 efter ny delimplementation | INTE OMTESTADE | Teknikprovet är separat från gamla v0.18-baslinjens diagnos. |

**R1 är inte godkänt, och PR #7 får inte mergas.** Att originalmaskerna nu går att rita på samma höjd är en verklig delvinst men ingen lösning på de sex oberoende X-positionerna. Särskilt i R2 behövs P1 även för nyckeln eller en annan fullt fungerande resursplan.

## 4. MAIN:s nästa avgränsade tekniska uppdrag till ROM DEVELOPMENT

**Beslut:** Gå vidare **inom samma auktoriserade v0.18** med en kort, mätbar undersökning av **individuell horisontell placering för sex logiska androider**, inte ännu fler demonstrationer med endast fasta NUSIZ-avstånd. Skapa ingen ny fullspelsskiva och ändra inga spelregler.

1. **Resursschema och stoppkalkyl först.** För R1 visa hur sex unika X-värden, två stora manmasker, två stora kvinnomasker, liten man och liten kvinna plus P0 fullstor gul spelare och M0-testskott får plats i respektive bildruta. För R2 redovisa också P1/nyckelkonflikten. Ange exakt TIA-kanal, bildrutefas, scanline, 6502-cykel, GRP/RESP/PF-write och eventuellt kopieavstånd. 76 cykler får inte överskridas.
2. **Prova högst två tidigare diskuterade vägar:** (A) kontrollerad **tidsmultiplexning mellan verkliga bildrutor**, med bibehållna sex logiska androider och olika fristående X-positioner; eller (B) en **PF/TIA-hybrid**. Ett tidsmultiplexat experiment är inte automatiskt en visuellt tillåten designkompromiss. Behåll originalmaskerna där de faktiskt tecknas. Om originalens exakta pixelmönster inte går att visa i hybriden är det en avvikelse, inte ett tyst PASS.
3. **Mät synlighetskvalitet:** över minst 600 följande Stella-bildrutor per kritisk testscen, dokumentera **per android** hur många bildrutor den är synlig, längsta obrutna osynlighetstid, hur tydligt den kan identifieras och faktisk samlingsbild/film. Bevisa att X-värden inte bara är NUSIZ-kopiegitter. Förväxla inte "lite flimmer tolereras" med godkänt att farliga androider försvinner längre stunder.
4. **Mät verklig rasterstabilitet:** rätta `saveSes`-problemet genom att skriva verifierbart 600-raders frame/scanline-/kritiska registerloggar. CI ska underkänna en tom, avkortad eller felaktigt indexerad mätfil. Den tidigare statiska 74/76-uppskattningen och nya beräknade 55/65 cykler är inte samma sak som en verklig skrivtrace.
5. **Beslutsgrind:** Om inga av de två arkitekturerna kan visa sex självständigt placerade och tillräckligt läsbara androidfigurer med spelare och skott på samma rasterhöjd: **stanna och redovisa teknikblockerare till MAIN**. Föreslå då eventuella användarbeslut separat, men ändra inte antal androider, masker, hitboxar, R2/O1, dörr eller ljud på egen hand.
6. Om metoden i stället har verkligt stöd för hela R1: fortsätt sedan med R2, R3, R4 och uppdaterad egenkontroll av de 16 testfallen inom v0.18. Tidigare PASS är inte överförbara; oberoende VERIFICATION granskar senare varje reviderad commit separat.

## 5. Projektgränser och status

- [PR #7](https://github.com/Odourman/let-me-out/pull/7): fortsatt **DRAFT, ej merge**.
- [Issue #8](https://github.com/Odourman/let-me-out/issues/8): fortsatt fryst ursprunglig baseline `561d3ba...` för oberoende verifiering. Den nya NUSIZ-koden `f5c06f...` har **inte** oberoende verifierats och behöver eget verifieringsunderlag när den blir kandidat.
- Endast `[Odourman/let-me-out](https://github.com/Odourman/let-me-out)` och dess egen Drive-mapp. **Ingen Linear, inga ändringar i The Cabin eller I Love a Fish**.
- **Ingen separat auktorisation för senare ROM-steg, PAL eller fullspelet.**
