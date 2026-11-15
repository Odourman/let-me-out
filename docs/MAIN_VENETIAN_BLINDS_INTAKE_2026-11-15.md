# MAIN – mottagningsgranskning av Venetian Blinds, v0.18 (2026-11-15)

**Omfattning:** Atari 2600 *Let Me Out!*; enbart tidigare auktoriserad NTSC-diagnostik R1–R4. **Status: tekniskt FAIL/BLOCKED för testade implementationer; INTE ett generellt bevis för att Venetian Blinds är omöjligt.** Detta dokument är MAIN:s evidensmottagning och källkodsläsning, inte oberoende VERIFICATION eller nytt implementationstillstånd.

## Proveniens och leverans

- Aktiv draft [PR #7](https://github.com/Odourman/let-me-out/pull/7), vid kontroll HEAD `82667dae033f70570dce903f8e1d4866528be02a`, **inte mergad**.
- [ROM DEVELOPMENT:s fullständiga rapport](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/TO_MAIN_VENETIAN_BLINDS_2026-11-15.md), [T01–T16](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/TEST_MATRIX_V018_VENETIAN_DELTA.csv), [Actions-run](https://github.com/Odourman/let-me-out/actions/runs/43770158692) (ROM-kod på `e06c253629f9fe26bfe3879dc98f7527b59bbf32`).
- [Komplett ZIP i projektets Google Drive](https://drive.google.com/file/d/1toh8XDyCBk2LckDwrm4oAQHJ_E4RSEfP/view). **355 517 byte**, SHA-256 **`b8141a874ad1e10de1ec958d1af36f46c51cc7a548181370ccfe6714dcfda271`**. MAIN hämtade den faktiska ZIP-filen, kontrollerade ZIP-integriteten och **94/94** angivna inre manifestposter utan avvikelse.
- Tre 16 KB F6-ROM enligt rapporten: `vb_9_interleave`, `vb_18_doubled` (ej godkänd dubbelskala) och korrigerad `vb_9_vdel`. Full .asm, .lst, .sym, buildskript, råa Stella-bilder och mätunderlag finns i arkivet.
- Originalbaslinjen för [oberoende VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8) är fortfarande den **historiska** committen `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`. Den gäller inte automatiskt ny Venetian-commit.

## Utvecklarens faktiska resultat – ej oberoende PASS

- **9 interleaved:** en komplett andra originalandroid på oberoende X saknas; 5 observerade vita rader i fångade bilder.
- **18 doubled:** andra oberoende figurpositionen saknas; skalan är enbart diagnostisk och får inte ersätta den godkända.
- **9 VDEL1:** fragment vid separerade X, men inte två hela människofigurer. VDEL1 skapar ingen extra TIA-spelarsprite.
- Den gula P0-spelaren och M0-skottet syns. **Endast sex valda råa Stella-bilder** för dessa nya ROM:er, alla med synligt 262-scanline-HUD enligt utvecklaren. **Inget 600-frame-test** genomfört för Venetian, då redan tvåfigurs-deltestet misslyckades.
- Ny delmatris: **LOCAL_PASS 2 / FAIL 2 / INCONCLUSIVE 2 / NOT_RUN 10**. R1 full grafik = FAIL. R2–R4 saknar ny lyckad körning.
- **Individuell TIA-/CPU-write-timing är inte uppmätt.** `logTrace`, `trapWriteIf` och PC-breakpointförsök gav inte användbara registerspår. De 43/48/63/68 cykeltalen är **statiska uppskattningar**, inte Stella-bevis.

## MAIN:s egen källkodsobservation – hypotes, ej bevisad rotorsak

MAIN läste `rom/v018/experiments/venetian_blinds/vb_9_interleave.asm` och `vb_9_vdel.asm`:

1. Varje rad börjar med `STA WSYNC`, skriver därefter `GRP1` tidigt och utför först **senare på samma rad** `STA RESP1` efter en variabel delay-loop. TIA-ompositionering är tidsberoende. En rimlig hypotes är att X-reset/GRP1-schemat kommer för sent eller till fel rad jämfört med när den avsedda pixelgruppen ska visas. **Detta är ännu inte bevisat med giltig Stella registertrace**.
2. `MALE_REQ_X` / `FEMALE_REQ_X` uppdateras i VBLANK från två tabeller, men under de nio synliga raderna används i stället `MALE_DELAY` / `FEMALE_DELAY`. En oberoende nominell X-tabell är **inte** i sig bevis för två faktiskt fria, korrekt renderade X. Avläs och jämför P1:s verkliga bildposition för båda.
3. Förslaget att dela 9 rasterrader varannan linje med två personer ger **ofrånkomlig radförlust i den diagnosmodellen** även om ompositioneringen rättas: 5/9 och 4/9 synliga radplatser innan kompletterande teknik. Därför är den inte en full acceptanslösning för intakta originalmasker.

**Viktig konsekvens:** Ett misslyckat prov med ovalid registertrace räcker för att underkänna de faktiska ROM:erna, men **inte** för att isolera varför `RESP1` misslyckas eller slutligt avfärda alla videochessliknande tekniker. En ny 600-frame-körning på samma misslyckade skärmbild är inte nästa rätta felsökningsåtgärd.

## MAIN:s fortsatta arbetsgrind och rekommendation

1. **Behåll R1 FAIL/BLOCKED och draft PR #7.** Ingen merge, ingen fullspel-, PAL- eller kartcutover; inget tyst avsteg från sex androids, fyra originalsilhuetter, fullstor gul spelare och skott.
2. **Första prioritet är teknisk rotorsak, inte fler stora experiment:** fastställ på verklig ROM/instruktionsnivå var `RESP1` träffar TIA i förhållande till `GRP1`, pixelklocka och `WSYNC`. Få en giltig breakpoint/step-trace vid den faktiska `STA RESP1`-instruktionen, alternativt en reproducerbar minimal positionsprob där observerat X går att kontrollera i Stella.
3. **Bara om den minimala positioneringsproben fungerar**: pröva ett korrekt 2-NPC-originalmaskprov inom en liten teknisk uppgift; bedöm radförlust på 9 linjer före uppskalning, och reservera resurser för R2 med nyckeln.
4. Utvecklarens rapport anger avslutat STOPP; om ytterligare kodförsök inte längre täcks av den konkreta avgränsningen, **begär separat uttrycklig MAIN/användarauktorisation för fortsatt tekniskt scope**. Det här MAIN-dokumentet är inte en sådan auktorisation.
5. Be oberoende VERIFICATION granska den relevanta nya committen under eget specificerat uppdrag. Issue #8:s frysta historiska baslinje ändras inte automatiskt.
6. Om åtgärden visar en hårdvarugräns: rapportera exakt varför och redovisa avvägningar **som förslag**, utan att införa visuella eller spelmekaniska kompromisser.

**Källordning:** Denna mottagningsgranskning registrerar resultaten. Den förändrar inte ursprungliga användarbeslut, auktorisationsdokument eller oberoende verifieringsutfall. *The Cabin* / *I Love a Fish* / Linear lämnas orörda.
