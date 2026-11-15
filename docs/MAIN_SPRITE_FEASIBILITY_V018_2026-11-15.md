# Let Me Out! – MAIN:s spritegenomförbarhet och delprov för v0.18

**Datum:** 2026-11-15  
**Roll:** MAIN / teknisk förstudie och uppgiftsavgränsning, **inte** ROM DEVELOPMENT eller oberoende VERIFICATION.  
**Projekt:** endast `Odourman/let-me-out`, inget Linear, inga ändringar i The Cabin eller I Love a Fish.  
**Utvecklarbaseline:** commit `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` i draft PR #7.  
**Auktoriserat scope:** endast NTSC/R1–R4 enligt Issue #6; ingen senare fas, inget fullspel, ingen PAL.

## 1. Utgångsläge (faktiska källor)

- `rom/v018/src/bank0.asm` på den fixerade committen och de motsvarande bankerna har enligt MAIN:s tidigare **statiska** kontroll två synliga loopar (`FullLoop` och `BandLoop`) med cirka **74 av 76 CPU-cykler** per normalt taget loopvarv. Båda återladdar sex playfield-registervärden per rasterlinje och P0/P1-data. Detta är **inte** en Stella-mätning eller en garanti att läs-/skrivtiming ligger på rätt del av bilden.
- R1 använder **PF** för sex vita androidkroppar, P0 för spelaren och PF för testsymbolskott. R2 använder PF för fem androidkroppar, P0 för spelaren och P1 för nyckeln. R3 använder P1 för dörrmarkören. `M0`, `M1` och `BALL` används inte av den frysta versionen.
- Utvecklarens Stella-bilder visar **grova korta block** i stället för de fyra godkända 8×9-människosilhuetterna. R1/R2 full bildacceptans fallerar. Nyckelns O1-försvinnande/återkomst och högeröppning har punktvisa bevis.
- Rapporten redovisar **5 utvecklar-PASS / 5 FAIL / 5 INCONCLUSIVE / 1 NOT_RUN**. Den rapporten får inte omtolkas som oberoende godkännande.

## 2. Varför upprepade P0/P1-sprites inte automatiskt löser sex androider

Atari TIA har två egentliga 8-bitars Player-sprites (`P0`, `P1`), två enbitsmissiler, en ball och grovkornigt playfield. `NUSIZ0`/`NUSIZ1` kan visa 2–3 kopior av samma sprite med **fasta relativa avstånd**. Funktionerna ger alltså inte automatiskt sex **oberoende placerade** humanoider med **fyra olika** silhuetter. Samtidig närvaro av spelare (P0) och nyckel (P1) förvärrar konflikten i R2.

Det går att studera om ompositionering, flera bildrutefaser, spelarspriteresurs och förenklade statiska väggar kan delas på annat sätt. **Genomförbarheten är ännu okänd**, och ett teoretiskt NUSIZ-exempel får inte räknas som godkänd lösning.

**Hårdvarureferenser:**
- https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-17.html (PF = 4 color clocks per bit, asymmetrisk PF och 76-cykelgränsen)
- https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html (svårighet att uppdatera två sprites och PF per rasterlinje)
- https://chrisaacson69.github.io/Vault/research/atari-2600/tia-reference.html (TIA:s objektresurser och NUSIZ-kopior)

## 3. MAIN:s nästa avgränsade teknikprov – enbart inom redan godkända v0.18

### DELPROV A – resursbevis före komplett R1

Uppdrag till ROM DEVELOPMENT: bygg eller analysera en **minimal teknikdel** som samtidigt har (a) gul spelare, (b) två vita androider med **olika** av originalets 8×9-masker, (c) ett testsymbolskott, med **gemensamt rasterhöjdband** och separata horisontella placeringar. Delprovet ingår som intern förundersökning till R1; **det är uttryckligen inte R1 PASS**, eftersom alla sex fortfarande krävs i R1.

Redovisa för varje kritisk scanline:
1. Vilket TIA-objekt ritar varje av de fyra visuella enheterna och vilka bitmaps används.
2. Exakta 6502-instruktioner med cykelposition, inklusive TIA-skrivningar, horisontell placering och eventuell ompositionering inom samma rasterlinje.
3. Vad som händer när de två androidernas X-avstånd varierar (inte enbart NUSIZ:s fasta avstånd); testa ett fall med närliggande objekt och ett med större avstånd.
4. Om tekniken kräver tvålinjeskernel, delade playfield-bakgrunder eller tidsmultiplexning mellan bildrutor: redovisa faktisk effekt på grafisk läsbarhet och flimmer. **Litet tillfälligt flimmer** är tillåtet, inte försvunna faror.
5. Om A inte kan visa *två olika* silhuetter plus spelare och skott i samma rasterband: **stoppa och dokumentera**, skala inte blint till sex.

### DELPROV B – skala till de redan beslutade R1/R2

Endast om A visar verklig teknisk potential: testa exakt **sex** androider, spelare och skott i R1 och exakt **fem** androider, spelare, nyckel och skott i R2. Bevara fyra igenkännbara humanoidtyper och O1. Variera X-positionerna; samtidiga höjdband ska fortfarande prövas. Använd inte två-androider-provet som ursäkt att sänka slutkravet.

### DELPROV C – mätningen

Innan nya PASS: fixa Stella-script/listing/symbolsökvägar och kontrollera att de laddas utan fel. Redovisa **600 sammanhängande** riktiga Stella-frames per R1/R2/R4, antalet scanlines och relevanta belastade TIA-skrivningar med cykelposition. Separera detta från offline-6502-modell. Bevara ursprungliga fullständiga debuggerbilder; märk beskärningar.

### DELPROV D – R3 oförändrad design

Behåll planerade C02-högeröppningen, bruna väggar, smal orange port och svart nyckelhål som visuella mål. Koden `$64` gav lila testvägg i Stella, och svart nyckelhål gick inte att urskilja. Redovisa dessa fel separat, utan att införa designwaiver eller ersätta låssymbolen tyst.

## 4. Utvecklarens två tillåtna tekniska kandidater

**Kandidat 1: sprite-/PF-hybrid med noggrant planerad 1- eller 2-linjers rasterkernel.** Först visa två olika riktiga silhuetter med gul spelare på samma höjd, sedan all R1/R2-belastning. `NUSIZ` kan bara användas där dess kopieavstånd och identiska bitmap faktiskt matchar scenen; det får inte tyst ersätta varierande spawns.

**Kandidat 2: omarbetad PF/TIA-kernel med annan register-/dataplanering.** Rapportera redan i teorifasen att PF:s 4-color-clock-bredd begränsar horisontell silhuettdetalj. Enbart mer ROM, borttagning av fyra NOP eller extra grafiktabeller innebär inte automatiskt att de 8×9-silhuetterna blir synliga eller att PF-skrivningarna hamnar rätt.

**Stopp om båda fallerar:** Rapportera tekniskt blockerande begränsning till MAIN. Det är INTE auktoriserat att minska antalet androider, göra om deras fyra silhuetter, frångå den guldgula nyckeln eller börja en annan utvecklingsfas.

## 5. Bevis- och beslutsgräns

- Allt tekniskt arbete under detta dokument omfattas endast av redan uttryckligen godkända **R1–R4 i v0.18**.
- Ändringar får endast ske på befintlig `rom-dev/v018-ntsc-diagnostic` och redovisas som nya commits på **draft PR #7**, inte sammanslås till `main` utan korrekt process.
- **Oberoende VERIFICATION Issue #8** avser fryst baseline `561d3b...`; nya commits behöver ny verifieringsomgång och kan inte ärva en tidigare godkänd bedömning.
- **MAIN har inte implementerat någon ROM eller själv utfört oberoende verifiering i denna studie.**
- Praktisk acceptans styrs av `docs/ROM_GATE_V018_ACCEPTANCE.md` och 16-ID-testmatrisen, inte av denna studie.
