# Let Me Out! – MAIN: sex individuella X-positioner inom ROM-diagnostik v0.18

**Datum:** 2026-11-15  
**Status:** faktisk offline-granskning + avgränsat tekniskt utvecklingsuppdrag. **Ingen ny ROM byggd i denna studie; inga Stella-test utförda här.**  
**Repository:** `Odourman/let-me-out`; befintlig utvecklingsgren `rom-dev/v018-ntsc-diagnostic`, draft PR #7, senaste kontrollerade HEAD `f5c06f352ba8653f3ce65bbc3e5e392c892beec5`. Separat VERIFICATION Issue #8 avser fortfarande den frysta committen `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`.

## 1. Ny kontrollerad geometrisk evidens

Den riktiga Stella-diagnostiken visade två olika, fullständiga 8×9-originalsilhuetter genom NUSIZ1-kopior med **fasta X-avstånd 32 och 64 färgklockor**. Det fungerar som delbevis för två figurer men ger inte sex individuella X-positioner.

Jag har därför tagit **exakt kartdata** från `design/PLANERADE_RUMSKARTOR_V011.json`, kartset A01/B01/C02/D01, de tidigare S0-kandidatpoolerna, och kontrollerat alla sexkombinationer. Varje kartcell är **4 TIA-färgklockor** bred i denna *abstrakta kartprojektion*. För par med en av tidigare Stella-testade NUSIZ-separationerna måste skillnaden i kart-X därför vara **8 eller 16 celler**. Detta är ett geometriskt villkor, inte en TIA-implementation.

| Rum | Antal möjliga sexval | Sexval utan ett enda par på 32/64 färgklockors X-avstånd | Andel |
|---|---:|---:|---:|
| A01 | 38 760 | 25 935 | 66,9 % |
| B01 | 1 716 | 413 | 24,1 % |
| C02 | 18 564 | 14 378 | 77,5 % |
| D01 | 5 005 | 3 465 | 69,2 % |
| **Totalt** | **64 045** | **44 191** | **69,0 %** |

Att även lägga till den hypotetiska *16 färgklockors* NUSIZ-kopieseparationen ger **samma totalsiffra i just dessa originalspawnpooler**, eftersom ingen av deras unika X-positioner ligger exakt fyra kartceller isär. Det är **inte** ett bevis att en 16-färgklockorsvariant saknar värde efter rörelse.

**Viktig tolkning:** 69,0 % är andelen av **kombinationerna över alla fyra S0-pooler**, inte den faktiska risken vid slumpmässigt vald karta eller en förutsägelse om spelbarhet. Ursprungskandidaterna har olika Y, medan grafikkerneln måste klara ännu hårdare **samma-Y-stressfall**. En existerande NUSIZ-parrelation är heller inte i sig tillräcklig för att rendera sex samtidigt.

**Slutsats:** Begränsning till 32/64-färgklockors avstånd skulle innebära att vi artificiellt kopplar ihop fiendernas X-rörelser. Det strider mot det avsedda sexfiendeupplägget. De godkända individuella positionerna ska inte ändras för att passa NUSIZ.

## 2. Direkt tekniskt startuppdrag till ROM DEVELOPMENT (R1, befintlig auktorisation)

1. **Sex logiskt separata X-positioner:** Behåll minst sex individuella `x[0..5]` (eller motsvarande byte-/fixed-pointpositioner) som kan uppdateras *oberoende* och nå olika X-värden. Representera även NPC-typ: `large_male, large_male, large_female, large_female, small_male, small_female`. Behåll spelarens egen X-position och projektilens position separat. Ingen automatisk NUSIZ-koppling, samma-hastighet-rörelse på grund av renderer eller koordinatsammanslagning.
2. **Testfall SEX_X_FREE:** På gemensamt rasterhöjdband välj exempelvis TIA-färgklockors X-startvärden `[16,36,56,76,96,116]` (20 färgklockor mellan grannar). Inget par har avstånd 16, 32 eller 64 färgklockor. Detta är **tekniska stresstestvärden**, inte nya godkända spawnpunkter. Följ de sex av varandra oberoende X-spåren under **600 sammanhängande bildrutor** och låt varje X kunna förändras separat, med plats för alla nio pixelrader och fullstor gul spelare. Spara de sex *begärda* X-positionerna och vilka spritebilder som faktiskt visas i varje bildruta.
3. **Två implementeringsvägar, högst:** (A) kontrollerad bildrute-tidsmultiplexning och (B) sprite/playfield/TIA-hybrid enligt tidigare MAIN-dokument. Visa faktiskt använd TIA-objektplan med P0/P1, M0/M1, BL/PF, NUSIZ/RESP/GRP/HMOVE per belastad scanline. Testa inte bara att `x[0..5]` kan uppdateras i RAM – kravet gäller även **synliga, läsbara** androider.
4. **Synlighetslogg i extern Stella-instrumentering:** per bildruta: frame-ID, scanlineantal, scen, sex individuella X-värden, faktiskt synliga bitar för var och en av sex androider (`visible_mask`, 6 bitar), vilken spritekanal de använder och relevanta TIA-write-cykler. Räkna per android (i) antal visuellt uppträdande frames, (ii) max sammanhängande osynlighetsperiod, (iii) synlighetsandel. **Spara 600 poster externt**, inte i RIOT-RAM (128 byte). Ingen ersättning av mätning med Pythonmodell.
5. **Slutlig R1-stress:** sex originalandroids (två stora män, två stora kvinnor, två små av olika typ), fullstor gul spelare och ett aktivt testskott samtidigt på samma höjdband. Visst kortvarigt flimmer tillåts, men ingen tyst maskförenkling, kopplade X-positioner, borttagna fiender eller inlånade designwaivers. Om tekniken bara visar en av sex per bildruta blir en enkel sexfascykel cirka **10 synliga uppdateringar per android och sekund vid 60 Hz**; det är en **teoretisk varningssignal**, inte ett accepterat resultat eller uppmätt Stella-frekvens.
6. **R2-resurskonflikt redan i schemat:** Nyckeln kan behöva använda P1 när fem androider, spelaren och skottet ska visas. Dokumentera hur tekniken i så fall fungerar, utan att ändra O1 eller den godkända nyckel- och dörrdesignen.
7. **Stoppregel:** Om både A och B misslyckas i faktisk Stella, lämna öppet FAIL/BLOCKED med loggar till MAIN. Ingen ny implementation, PAL, fullspel, förändrad spawner, ändrade hitboxar eller antalsreduktion på eget initiativ.

## 3. Bevisgräns och nästa leverans

**MAIN:s nuvarande mätning:** 64 045/64 045 kombinationer enumererade, 44 191 saknar provad NUSIZ-parrelation. Script och data är reproducerbara. **Ingen RAM-rutin, ingen sex-NPC ROM eller 600-Stella-trace har skapats här.**

**ROM DEVELOPMENT måste leverera:** ny diagnosbinär (eller explicit teknik-Fail), källa, byggrecept, commit och ROM-SHA256, verkliga Stella-bilder och 600-posterloggar per stresscen, cykelspår, X-/synlighetsstatistik och uppdaterad egenkontroll per 16 test-ID. Allt på befintlig utvecklingsgren och draft PR #7.

**VERIFICATION:** Issue #8 gäller fryst historisk baseline. En ny fungerande commit kräver en senare separat oberoende kontroll. MAIN:s offline-geometri får aldrig användas som oberoende slutverifiering.

**Projektgräns:** endast Let Me Out!, ingen Linear, inga ändringar i The Cabin eller I Love a Fish.
