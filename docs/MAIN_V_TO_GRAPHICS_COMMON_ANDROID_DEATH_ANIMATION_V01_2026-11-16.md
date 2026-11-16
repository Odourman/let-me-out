# LET ME OUT! – MAIN V till GRAPHICS
## COMMON ANDROID DEATH ANIMATION v0.1 – gemensam visuell sekvens och nyckel-timing

**Datum:** 2026-11-16. **Status:** ENDA NYA GRAPHICS-DESIGNUPPDRAGET. **Designkandidater enbart**; inte ROM- eller teknisk integrationsauktorisation.

### 1. Källa, mandat och det enda visuella målet

Du är dedikerad GRAPHICS-chatt. Läs din gällande [rollinstruktion](MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md), [aktuell projektstatus](CURRENT_PROJECT_STATE_2026-11-15.md), [MAIN:s gångbildsmottagning](MAIN_V_ANDROID_WALK_FRAME_B_V01_RECEIPT_2026-11-16.md) och den ursprungliga 57-beslutshandoff i [Google Drive](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view). I handoffens `02_MASTER_SPEC.md`, `03_DECISIONS.csv` och `07_DECISION_HISTORY.md` är följande fastställt:
- Exakt **en GEMENSAM dödsanimationsprincip/sekvens** för alla sex androidinstanser (fyra grundtyper).
- När en android förstörs används dess faktiska fallposition och den tas bort efter den gemensamma animationen.
- Om den var den förutbestämda nyckelbäraren syns **guldnyckeln först när animationen är helt färdig**, på samma lagrade position. Om den inte bar nyckeln visas **ingen nyckel**.
- Androiderna är vitfärgade och människoliknande; **de fyra ursprungliga 8×9 A-maskerna är låsta** i `design/NPC_REFERENCE_8x9_masks.json`, blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Stora är 9 synliga bitmaprader, små bara 6 (rader 2–7). Det är **inte godkänt** att rita uppenbara robotdelar eller ändra fiendeantalet.

Grafisk huvudfråga: Hur kan samtliga sex androidfigurer visuellt dö/neutraliseras med **en tydlig, kort, konsekvent grafisk effekt**, utan att den lilla varianten plötsligt blir större eller att nyckeln förväxlas med själva animationen?

### 2. Högst TVÅ avgränsade 8×9-koncept, inte fler

**Koncept D1 – Gemensam upplösningsregel:** Utgå från respektive originalmask i den första synliga rutan. Applicera SAMMA deterministiskt specificerade stegvisa pixelborttagnings-/fragmenteringsregel för alla fyra typer på exakt samma källrader. Resultatet kan ge olika niobytesmasker per typ men ska vara **EN gemensam transformationsmetod, samma fasantal, ingen ny typunik animation eller timing**. Undvik explosion som breddar silhuetten, och särskilt att de små fylls ut på rader 0/1/8.

**Koncept D2 – Alternativ universell slutsekvens:** Pröva en mer visuell geometrisk kort sekvens som ALLA typer kan dela, till exempel kort kollaps/dissolve med få bärande pixlar, men håll ursprungligt 8×9-bildområde och de små figurernas egen sexradsbegränsning i de frames där de fortfarande syns. Om det är omöjligt att göra samma bytesekvens läsbar utan att de små växer eller identiteten förloras, skriv tydligt `UNIVERSAL_BYTES_VISUAL_FAIL`. Högst två sådana alternativ – ingen designserie av olika effekter för varje android.

För båda koncepten:
- Håll dig inom **ursprungsrenderingens 8 bitar × 9 rader, vitt mot mörkt**, helst endast originalmask + **högst två** mellanliggande **unika** animationsbilder + avslutande osynligt/tomt tillstånd. Det är en **grafisk budgetmålsättning**, inte en redan implementerad 6502-framestatemaskin. Om den fysiska formen kräver ett extra frame måste det markeras `FUTURE DESIGN REQUEST`, inte smygas in.
- Ingen stor vit helskärmsblixt, ändrad hudfärg, andra Atari-TIA-objekt, explosioner som skymmer andra figurer eller användning av M0/P0/PF. En gemensam lokalffekt får inte bli "en saknad fiende" som går upp i ingenting utan en igenkännbar träfffeedback.
- **Ingen flicker-waiver** och inga dolda extra GRP1-cykler. De sex fiendernas pixeldata/pointertiming är ännu inte allmänt fungerande i runtime. Detta är bara visuell simulering.
- Bevara originalpositionen fram till att dödssekvensen slutar. Ingen reell collision-/hitbox-/nyckelspawnlogik implementeras. Om du vill illustrera en teoretisk kollisionsfrysning måste den märkas som scenario, inte ny spelregel.
- Testa sexfigursvisning med **en** döende android och andra fem kvar i Frame A, inklusive fall där en **liten** är den döende. Visa två avslut för samma sekvens: (A) icke-bärare → tom plats, (B) nyckelbärare → **guldnyckel först EFTER den sista animationsbilden**, på ursprunglig plats. Inga nyckelpixlar visas under själva dödsanimationen. Förvarad nyckelform är v0.13:s visuella mål, K09/K11 endast **ej godkända** bitmapförslag.
- Ställ den statiska gula spelarprototypen bredvid endast som tydlig skala-/färgreferens med etiketten `V03_B UNAPPROVED COMPARISON ONLY`. Välj inte ny P0, ändra inte orange dörr eller bakgrundsfärger.
- Vid önskad GIF: enstaka offline 1× och närmaste-granne 4×/20× med GIF-varaktighet explicit `ILLUSTRATIVE ONLY`. **Inga tidsintervall i ms låses till spelet.**

### 3. Jämförbar fil- och grafikleverans

Leverera **EN** `ANDROID_DEATH_ANIMATION_V01_TO_MAIN.md` med:
1. Exakt de fyra ursprungliga Frame A-maskerna med källhash, och för båda D1/D2 de nya råbitmönstren (rader uppifrån ned, hex, pixlar, position och variantnotation). För ett delat regelbaserat förlopp, specificera regeln så att den går att återge från valfri A-mask, inte en handviftning om "pixlar försvinner".
2. Tydliga animation-stills med märkning `ORIGINAL → HIT → DISSOLVE → EMPTY`; visa sedan **key after death** i eget separat bildsteg. Gör också ett scenario utan nyckel. För alla fyra typer visa minst 1×, 4×, 20× i en liten jämförelsetabell och en sexfigursscen där exakt en dödas.
3. **Källren visning:** Data-/PNG-/GIF-filer måste faktiskt överensstämma med genererade bytes; antal poster, verklig ZIP CRC, SHA-256 för hel ZIP och alla övriga poster i `SHA256SUMS.txt`; ZIP får inte innehålla ROM, obehörig Berzerk-disassembly eller kommersiell tredjepartsbild.
4. Är D1 eller D2 grafiskt begriplig i verklig 1×? Markera själv vilka som är `GRAPHICS CONCEPT ONLY`, `VISUALLY PLAUSIBLE`, `UNREADABLE` eller `INCONCLUSIVE`. **Ingen** simulation är en äkta Stella- eller CPU-timingmätning. Visa om en liten kvinnas kropp eller nyckelposition blir otydlig.
5. Separat **TIA-kostnadsrisktabell**: råa nybytes, extra niobytesrader, frågan om egen fas-RAM, P1/GRP1-timing, att fem andra fortfarande ska kunna visas, samt konflikter när dödsobjektet delar rasterhöjd med spelaren, M0 och brun PF. Alla sådana kostnader är **TEKNISKA HYPOTESER**, inte färdig implementation eller rätt till fler sprites.
6. Skapa ett **verkligt uppladdat ZIP** samt länkar till fullständig handoff, JSON-maskdata, jämförelsebild/GIF i just projektets dedikerade [Google Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Visa filstorlek, antal poster, full SHA256 och riktig föräldermapp; eller lämna verifierbara sandboxfiler. Ingen "ladda ned" utan faktisk länk.

### 4. Stopp och beslutsklass

Avsluta efter **D1 och D2**. Du ska inte godkänna final death sprite, ljud, nyckelspawner, R2, collision eller gameplayteknik. Ge **EN** rekommendation till MAIN om vilken visuell effekt som bör väljas som framtida kandidat – eller **`DEATH_ANIMATION_VISUAL_FAIL`** om båda är för svaga vid 1×.

Status för allt nytt: **`GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`**. Alla tidigare godkända original 8×9-bitmappar, nuvarande P0, kartor, PR#7 och ROM DEVELOPMENT:s frysta grenar lämnas orörda. Ingen separat teknik-/kodauktorisation, ingen ny mapper/bank och ingen oberoende VERIFICATION för detta designscope. Inga ändringar i The Cabin, I Love a Fish eller Linear.

**Målet är ett enda begripligt grafiskt dödsförlopp och ett korrekt VISUELLT tidsförhållande till nyckelns uppdykande, inte ännu en omgång med onödigt komplicerad TIA-grafik.**
