# Let Me Out! – MAIN:s mottagningsgranskning av ROM DEVELOPMENT v0.18

**Datum:** 2026-11-15  
**Status:** **BLOCKERAD / EJ GODKÄND** – utvecklarens egenkontroll, inte oberoende VERIFICATION.  
**Scope:** Enbart uttryckligen auktoriserad NTSC-diagnostik R1–R4, inte fullspelet.

## Fastställt källäge

- Projekt: `Odourman/let-me-out`.
- PR: https://github.com/Odourman/let-me-out/pull/7 – **öppen draft, ej mergad**.
- Baseline commit: `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` på `rom-dev/v018-ntsc-diagnostic`.
- Developer-rapport: `rom/v018/docs/STELLA_PREFLIGHT_REPORT_2026-11-15.md`.
- Developer-matris: `rom/v018/docs/TEST_RESULTS_16_STELLA.csv`.
- GitHub Actions senaste körning på baseline: run **43744070310**, `success`; tidigare Stella-evidens från run **43743513953**, samma ROM-kod (mellanliggande commit lade till rapport, testmatris och evidens).
- Uppladdad utvecklar-evidens ZIP: SHA-256 `7500dae4f4a63d27f765bad3b3872384bd2ccb842a7e807abb9e50a475df2dc4`; ZIP-test OK, samtliga **33** individuella SHA-poster korrekta.
- DASM-rebuilt 16 384-byte bin och original-bin som paketerats i utvecklarens ZIP är byte-identiska. SHA-256 för båda: `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`.
- GitHub Actions-loggen för senaste run innehåller `DASM_BUILD_BYTE_IDENTICAL=YES` med installerat DASM `2.20.15~20201109+really2.20.14.1-2` (praktiskt 2.20.14.1).

**Bevisgräns:** MAIN har granskat utvecklarens ZIP, manifest, inkluderad binär, bildmaterial, PR-status och CI-logg. MAIN har **inte** gjort en separat lokal DASM-ombyggnad eller en ny självständig Stella-körning. Alla påstådda Stella-PASS nedan är fortsatt utvecklarens egenkontroll. Detta dokument utgör inte oberoende VERIFICATION.

## Resultat från 16 fall enligt utvecklarens testmatris

- **PASS 5:** T05, T09, T10, T14, T16.
- **FAIL 5:** T02, T03, T04, T11, T12.
- **INCONCLUSIVE 5:** T01, T06, T07, T08, T13.
- **NOT_RUN 1:** T15 – oberoende VERIFICATION ännu inte utförd.

### Blockerande fel

**R1:** Det finns sex vita visuella enheter på samma rastersnitt plus gul spelare och skott, men PF-silhuetterna ser ut som **korta horisontella block** snarare än tydligt igenkännbara stora/små män och kvinnor. Detta är en **verklig grafikbrist**, inte ett skäl att ändra fiendeantal. C01/C03/C04 inte uppfyllda.

**R2:** O1-delprovet visar nyckel vid frame 625, skymd vid 715, åter synlig vid 835. Tre debuggerbilder stöder att RIOT `KEY_X=$1B`, `KEY_Y=$50`, `KEY_ALIVE=$01` behålls. Däremot är androidernas PF-grafik fortsatt otillräckligt läsbar. O1-delprov får **inte** bli godkännande av hela R2.

**R3:** Högerdörrens öppningsfunktion har punktvis stöd vid frame 1420 medan vänsterkanten är stängd; orange port är synlig i frame 1335. Svart nyckelhål har inte läsbar rund/kilform, och färgkod `$64` visas lila där en brun teknisk bas var avsedd. Den orange porten är inte tillräckligt för att godkänna nyckelhålsmålet.

**R4 / timing:** En faktisk Stella-bild från frame 1925 finns. Åtta separat tagna bilder visar enstaka föregående bildrutor med `262` scanlines, men inte **600 sammanhängande Stella-bildrutor per belastningsscen** eller komplett TIA-register-/CPU-cykeltrace. Utvecklarens tidigare CPU-modell är inte ett substitut för faktisk emulatormätning.

**Fångstteknik:** Minst ett fullständigt Stella-debuggerfönster visar varningar om saknade script/list/symbol-filer. Bildens frame- och bankuppgifter finns ändå; rätta gärna fångstkonfigurationen innan oberoende verifiering så att kommandon och symboler återfinns reproducerbart. Detta är inte i sig bevis för grafikfel.

## MAIN:s beslut – ingen scope-expansion

1. **Ingen merge av PR #7** och ingen release eller fullspelsutveckling. Ingen design-waiver ges.
2. **Prioritera nu en begränsad teknisk korrigering inom redan auktoriserade R1–R4:** undersök om P0/P1-spritegrafik och tidsdelning (med möjlig omfördelning av P0-spelare, P1-nyckel/dörr samt PF/M0/M1/BALL) kan återskapa de mänskliga 8×9-silhuetterna i det belastade rastersnittet. Börja med en dokumenterad 76-cykelsbudget och faktiskt Stella-förtest. **Denna lösning är inte verifierad** och får inte antas möjlig bara för att sprites är finare än playfield-bitar.
3. Om det visar sig omöjligt, dokumentera hindret och undersök **högst det andra redan redovisade alternativet**, en omskriven PF/TIA-kernel med tätare bitmappuppdatering. Gör ingen tyst förenkling av sex androider eller fyra utseenden.
4. Separera dörrens tre delar i rapportering: (a) rättsidig öppning, (b) orange dörrfärg/korrekt brun vägg, (c) svart igenkännbart nyckelhål. Ett PASS för (a) räcker inte för (c).
5. Komplettera framtida nykörning med kontinuerlig scanline- och cykelevidens och exakt reproducerbar scenstyrning. Enbart fler skärmbilder ersätter inte detta.
6. **VERIFICATION arbetar helt separat på fixerad commit och arkiv**, gör egen ombyggnad och bedömning. Ingen egenutvecklardom får uppgraderas till slutlig acceptans av MAIN.

Detta är en **prioriteringsinstruktion inom v0.18**, inte en ny implementeringsfas. Om verklig förbättring kräver ändrade spelregler, fler än R1–R4, PAL, full gameplay eller en visuell kompromiss måste MAIN inhämta ett **nytt uttryckligt användarbeslut**.

## Förväntad nästa leverans

- ROM DEVELOPMENT: minst en detaljerad genomförbarhetsanalys för spritebaserad multiplexning, kod-/tester enbart inom R1–R4, bilder/trace från riktig Stella, ny utvecklarmatris, exakt commit och SHA.
- VERIFICATION: separat verifieringsrapport på aktuell fixerad baseline innan en teknisk slutbedömning, med oberoende rebuild och redovisning av samtliga avvikelser.
- MAIN: sammanfatta evidensen och avgör om v0.18 nått PASS, FAIL eller INCONCLUSIVE. **Starta inte senare gameplay-uppdrag utan nytt explicit tillstånd.**

## Projektisolation

Alla hänvisningar och åtgärder gäller endast `Odourman/let-me-out` och den separata Let Me Out!-mappen i Google Drive. **The Cabin, I Love a Fish och Linear ska inte påverkas.**
