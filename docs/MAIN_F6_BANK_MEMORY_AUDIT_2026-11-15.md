# Let Me Out! – MAIN:s F6-bank- och minnesrevision
**Datum:** 2026-11-15. **Status:** statisk, reproducerbar käll-/symboltabellsanalys; rådgivande research. Ingen ny 6502-kod, ROM-byggning, Stella-körning, implementationsfas, design-waiver eller oberoende VERIFICATION genomförd av MAIN.

## 1. Inspekterade, faktiska projektkällor
- [Draft PR #7](https://github.com/Odourman/let-me-out/pull/7), HEAD vid granskning `82667dae033f70570dce903f8e1d4866528be02a`, fortfarande **DRAFT** och ej mergad.
- `rom/v018/tools/build.py` (genererar de fyra bankernas olika tabelldata), `rom/v018/src/bank0.asm` till `bank3.asm`, `rom/v018/dist/symbols.json` och `rom/v018/README.md`, allt från aktuell utvecklingsgren.
- Källtext inskickad av användaren: **Bank switching i Let Me Out! – nuläge och bästa användning**. Dess slutsats om mer kod- och databudget är korrekt i princip, men bytegränser och genomförbarhet måste skiljas från emulatorbevis.
- Externa arkitekturreferenser: [AtariAge: Bank switching, best practices](https://forums.atariage.com/topic/83915-bank-switching-best-practices/) och [Stella Debugger](https://stella-emu.github.io/docs/debugger.html). En bankväxling sker under samma CPU-adressfönster; korrekt fortsättningskod och resetvektor är centrala.

## 2. Verifierad ROM-organisation i *huvuddiagnostiken*
- F6: fyra banker på 4 096 byte, kartfönster `$F000-$FFFF`; hotspots `$FFF6-$FFF9`.
- `build.py` gör fyra versioner av **samma kernel**, men olika data. Den jämför uttryckligen alla bytes i `$F000-$F3FF` samt vektorerna, och felar om de skiljer sig. `src/bank0.asm`–`bank3.asm` har kontrollerats och kernelhuvuddelarna är identiska.
- Bank 0 = R1 (sex androids och testsymbolskott); bank 1 = R2 (fem NPC + nyckelskymning); bank 2 = R3 (dörr); bank 3 = R4 (rasterstress). Detta gäller **isolerad diagnostik**, inte en fungerande integrerad spelmotor.
- I VBLANK väljs `SCENE` och `STA $FFF6` / `STA $FFF7` / `STA $FFF8` / `STA $FFF9` utförs. Eftersom kerneln vid den följande programadressen för närvarande är identisk i alla banker fungerar det som en rimlig basdesign i det auktoriserade experimentet.
- `rom/v018/tools/build.py` använder en **egen minimal assembler** (`as6502.py`) för originaldiagnostikens genererade binär. Senare DASM-/Stella-kontroller måste redovisas separat; det är inte korrekt att kalla allt originalmaterial byggt med DASM enbart därför att senare experiment använder DASM.
- Senare `six_x_free` och `venetian_blinds` bygger var sin 4 KB-bankbild som upprepas fyra gånger till 16 KB. De använder därmed inte någon extra individuell kod- eller datakatalog ur F6-bankbytena.

## 3. Exakt statiskt ROM-adressutrymme i varje huvudbank
Kontrollerat mot `dist/symbols.json`: sista etiketten `Overscan=$F1D7`; återstående instruktioner `STA WSYNC` 2 byte, `DEX` 1, `BNE` 2, `STA WSYNC` 2, `JMP Frame` 3; koden slutar **före `$F1E1`**.

| Område | Byte/bank | Faktisk användning |
|---|---:|---|
| `$F000-$F1E0` | **481** | Identisk exekverbar kernel |
| `$F1E1-$F3FF` | **543** | Oallokerad plats efter koden |
| `$F400-$FBFF` | **2 048** | Åtta ROM-datatabeller ×256 byte; reserverade/använda |
| `$FC00-$FFF5` | **1 014** | Oallokerad plats före F6-hotspots |
| `$FFF6-$FFF9` | **4** | F6 bankväxlings-hotspots; **inte fri vanlig data-/kodplats** |
| `$FFFA-$FFFF` | **6** | Reservera för vektorer/systemslut |
| **Summa** | **4 096** | En fysisk ROM-bank |

**Praktiskt fritt utan att flytta befintliga tabeller:** `543+1014 = 1 557` byte per bank, **6 228 byte fysiskt över fyra banker**. Det är en ROM-utrymmesuppskattning, inte fyra samtidigt synliga databanker. Grov oallokerad rymd inklusive hotspot-/vektornärhet hade annars felaktigt uppgetts som `1 563` byte/bank.

### Gleshet i allokerade tabeller (källbyte, inte TIA-besparing)
| Bank / scen | Icke-nollbyte av 2 048 | Nollbyte | Unika kombinerade åttatabells-rastertupler av 256 |
|---|---:|---:|---:|
| 0 / R1 | 426 | 1 622 | 11 |
| 1 / R2 | 276 | 1 772 | 33 |
| 2 / R3 | 672 | 1 376 | 10 |
| 3 / R4 | 284 | 1 764 | 43 |

Detta pekar på möjlighet att packa rumsmönster och förberäkna bilddataströmmar på annat sätt i ROM. **Det är inte bevis för att tabellerna kan komprimeras utan mer avkodningsarbete**. Avkodning inne i den redan hårt belastade scanlinekerneln kan vara sämre än att läsa 256-byte-tabeller med direktindex. Töm inte heller de ursprungliga R1–R4-tabellerna utan spårbar regressionstest.

## 4. Konsekvenser för grafikproblemet

**Vad banker kan hjälpa med:**
1. Två **specialiserade men korrekt återhoppade** renderingsrutiner för diagnos R1 (sex NPC + P0 + M0) och R2 (fem NPC + nyckel + P0 + M0).
2. Fler statiskt förberedda bitmap-/mask-/rastertabeller än som ryms i ett enda 4 KB-kodpaket.
3. Flytta förarbete till VBLANK/overscan eller välja kernel vid bildrutegräns (med kostnaden och kodsambandet dokumenterade).
4. Ha gemensamma, korta bankväxlings-/resetstommar och olika scenimplementationer efter säkert inträde.

**Vad banker INTE löser:**
- `P0/P1` är fortfarande två fulla player-sprites; en aktiv bank i taget; 76 CPU-cykler/scanline och standard 128 byte RIOT-RAM.
- De fri positionerna hos sex samtidiga originalmasker på samma Y.
- Det tidigare misslyckade `RESP1`-läget; byteutrymme är inte en felrättad registerdeadline.
- Det framtida spelets **samtidiga** dörr/väggar + R1/R2-figurer. Att R3 finns i separat bank i diagnostiken innebär **inte** att dörren automatiskt kan ritas samtidigt med de sex androidernas spelbild. Full integration kräver senare separat godkännande och verkligt test.
- Sex dynamiska X-koordinater kan inte realistiskt lösas genom att på förhand lagra varje möjlig sexkombination av positioner i fyra ROM-banker.

## 5. Tekniskt säkra förändringshypoteser (ingen kodauktorisation)
1. **Behåll standard F6/NTSC.** F6SC/DPC+/F4 är andra format/arkitekturer och inte godkända i nuvarande diagnostik.
2. **Gemensam växlingsstub:** om bankkernlar görs olika måste den fortsättande instruktionen **efter** varje hotspot-access finnas på korrekt adress i den bank man just växlat till. Samma `$F000-$F3FF` kan inte längre förutsättas identisk i sin helhet när de specialiseras. Avgränsa identisk reset/transport/return-stub och bankvisa kodområden. Bevara stack, eventuella flaggberoenden, R1–R4-scenidentitet samt `SCENE` i RIOT-RAM.
3. **`STA` kontra `BIT` för bankväxling:** det befintliga `STA $FFF6` är inte bevisat fel. En alternativ `BIT $FFF6` är en etablerad läsbaserad variant, men påverkar N/V/Z och måste därför A/B-testas med återhopps-PC, banknummer, reset och cykelbudget innan byte. Ändra aldrig slentrianmässigt.
4. **Tabellkomprimering endast utanför rasterkritisk väg.** Mät VBLANK-förarbete, RAM-scratch och page-crossings. Varken mer RAM eller mer tid skapas av bytepackning i sig.
5. **Ingen ny fullbilds-kernel utan korrekt T07:** prioritera [RESP1-analysen](MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md); bevisa debuggerstopp vid `STA RESP1` med `break` + `run` eller `runToPc`, och verklig `_scan/_sCycles/_bank`, före försök med större F6-kernel.

## 6. Avgränsat, mätbart handoffförslag till ROM DEVELOPMENT
Detta är **rådgivande testordning**, inte nytt kodmandat:
- **F6-0** (offline): rapportera tabell- och kodbytebudget från respektive DASM-listning/ROM, bankhotspot-/vektorreservering, checksumma för varje 4 KB-segment och skillnader i data.
- **F6-1** (Stella, om inom befintligt uttryckligt R1–R4-mandat): under redan definierade scenväxlingar, logga `_bank`, PC, relevanta scen-/RAM-variabler och faktiskt frame/scanlineantal. Kontrollera uppstart från godtyckligt vald bank/reset och att byten aldrig sker inne i en kritisk synlig rasterrad.
- **F6-2** (Stella, först efter säker grund): jämför befintlig `STA`-växling med en **separat diagnostisk** `BIT`-variant. Mät samma skärmbild, banksekvens och flaggeffekter. Ändra inte produktionsbasen om inget fel motiverar det.
- **F6-3** (endast forskningsmodell): gör ett adressschema för en R1- och en R2-specifik kernel som fortfarande har plats för PF-väggar och framtida högerdörr. Räkna samman bytes och CPU, ingen påstådd visuell PASS.
- **F6-STOPP:** utan en fungerande, uppmätt två-NPC-positioneringsprob och godkänd silhuett kan bankomorganisationen inte redovisas som åtgärdad R1. Om testet skulle expandera v0.18-scope eller börja en ny utvecklingsfas måste separat användarbeslut inhämtas.

## 7. Status och verifieringsdisciplin
Vid denna MAIN-granskning är **R1 FAIL/BLOCKED**, R2–R4 ännu inte omtestade med senaste Venetian-kod, dess TIA-registertrace INCONCLUSIVE och [VERIFICATION #8](https://github.com/Odourman/let-me-out/issues/8) fryst vid tidigare `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`. [PR #7](https://github.com/Odourman/let-me-out/pull/7) ska vara DRAFT, inte mergas. Inga ändringar i The Cabin, I Love a Fish eller Linear.
