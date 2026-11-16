# LET ME OUT! — MAIN III: kontroll av äldre externa kernelrekommendationer (1942 / Frantic / Three-Stream)

Datum: 2026-11-16. **READ-ONLY RESEARCH**. Ingen ROM-implementation, designwaiver eller independent verification.

## Bakgrund och statusankare

En äldre MAIN II-överlämning föreslog 1942:s `multisprite_kernel.asm` som huvudreferens för sex fria androider, samt Frantic och Three-Stream som inspirationskällor. Detta måste uppdateras efter R1h.

- Projektets `main`: `f6b3fc76c59161e04e583dc8c0787332d2f261c7` vid denna granskning.
- ROM DEVELOPMENT:s PR #7 fortfarande OPEN/DRAFT, head `82667dae033f70570dce903f8e1d4866528be02a`. VERIFICATION issue #8 fortfarande OPEN.
- R1h: faktisk 600-frame lokal PASS för fyra olika godkända NPC, en statisk gul testspelare, M0 på separat överliggande rad, BALL vänster x0, PF0 höger 32-raders öppning, fjärde NPC i fyra 24CC-spannlägen; Actions #43821560463, testad SHA `3e5b79fd0409a7ed9f9ae381ade6ac1e66d51b32`; full R1 fortfarande FAIL/BLOCKED.
- MAIN III:s R1i-A/B-studier: `docs/MAIN_III_R1I_STATIC_P1_WINDOW_AND_FIFTH_COPY_HYPOTHESES_2026-11-16.md`, **bara statisk forskning**.

## 1942 – öppnad faktisk källkod

Källa: https://github.com/Al-Nafuur/1942-bB/blob/main/src/multisprite_kernel.asm (GitHub blob `4490a30d814370fc72d96cfad65c4b5c6136246d`; 1200 rader).

- Källan beskriver `RepoKernel` som en **fyra-scanline** rutin för ompositionering av **P1**, inte sex oberoende åttabitarsmasker på samma scanline.
- Den Y-sorterade spritehanteringen och den mindre interfolierade kernelrutinen är intressanta för senare varierande Y och förberedning utanför kritiskt rasterband. Detta löser inte R1:s same-Y fem/sju bitmapresurser.
- Raderna cirka 32–40 definierar **`superchipRAM=$1000`** och `wCacheNewSpriteY` där. Standard-F6 har **inte** den RAM-funktionen. Mjukvarualgoritmen kan studeras, men koden är inte ett drop-in-bevis för vår standard-F6-ROM.
- `RepoKernel` använder explicit **`lax (PF2pointer),y`**, en **odokumenterad 6502-opkod**. Det är kompatibilitets-/portabilitetsrisk, som skulle behöva omskrivas eller testas separat. Detta gör kopiera-källkod-och-kör särskilt olämpligt.
- README anger dessutom PlusROM-funktioner i projektet. Det är inte bevis att just varje rasterfunktion beror på PlusROM, men är ännu ett skäl att inte jämställa hela 1942-implementationens hårdvarukontrakt med vårt.
- Källhuvudet säger CC0, men återanvändning av kod förutsätter separat licens-/proveniensgranskning; tekniska *principer* kan studeras utan kodimport.
- Utvecklarens egna förklaringar: https://forums.atariage.com/topic/347667-multi-sprite-kernel-strategies-or-examples/ (en player återanvänds, separat fyralinjers ompositioneringskernel) och https://forums.atariage.com/topic/362717-modifying-the-multisprite-kernel-its-complex-for-sure/ (pixel- och PF0-budgetkonflikt).

## Frantic – verifierat tidigare uppgivet DPC+

Källor: https://forums.atariage.com/topic/186560-frantic-2600/ samt https://forums.atariage.com/blogs/blog/148-spicewares-blog/57-frantic/.

- Det finns verklig publicerad Frantic-kod och en diagnostik som beskriver flimmernivåerna **30, 20, 15 Hz**.
- AtariAge beskriver Frantic som **DPC+**; ARM/kassettfunktionerna ligger utanför standard-F6. Frantic kan inspirera frameprioritering, konfliktdetektering och diagnostik men ger ingen ROM-kompatibel bekräftelse på sex same-Y originalmasker utan kompromisser.
- R1:s ursprungliga SEX_X_FREE-A med 100/600 frames per NPC (~10 Hz) var FAIL. Frantic:s högre frekvenser är en annan provpunkt, inte automatiskt godkänd flimmerwaiver.

## Three-Stream Versatile Kernel – nyttig dataplan, men inte direktersättning

Primärtext av Steven Hugg, publicerad 2025-10-13: https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html.

- Tre register-/datastreams per scanline (PF samt två spritekanaler). Beskriver displaylistor, temporära HMOVE-rörelser och resurssparande registerförberedelse.
- Texten är öppen med att kerneln normalt uppdaterar **upp till tre register per rasterrad**, ibland avstår uppdatering vid listbyte, RAM-kostnad ~**32 byte per displaylista**, och att tearing/krokigt playfield kan förekomma.
- I R1h är fyra P1/P0-maskbilder plus gul spelare och kritiska `GRP`, `COLUP`, `RESP`-strobningar redan tidsbegränsade till **74–75 av 76 CPU-cykler per rad**. En Three-Stream-displaylistlösning i samma band bevisar inte automatiskt att dessa fem fulla masker kan ritas, än mindre sju. Principen om **förberäknade registerhändelser** passar utanför rasterbandet.

## MAIN III:s slutsats och ordning

1. **R1i-A statiskt kartlagd, ännu ej körd:** omordna befintlig 3-cykels `STA RESP1` och 3-cykels `BIT FRAMELO` för att undersöka andra oberoende P1-X-axeln samtidigt med R1h:s fjärde P0-X. Kräver en egen uttrycklig test-/implementationsauktorisation innan ny exekverbar ROM skapas.
2. **R1i-B separat osäker hypotes:** ersätt en `BIT FRAMELO` med ytterligare `STA RESP1` för möjlig andra stora kvinnokopia. 18 CC är potentiellt TIA-fassensitivt; ingen femte NPC är ännu bevisad.
3. **1942** blir sekundär forskningsreferens för sortering, vertikal ompositionering och dataförberedelse, inte MAIN:s primära standard-F6 same-Y-implementationsplan.
4. **Frantic** blir jämförelse för flickerpolicy och DPC+-begränsningar, inte kartbyte eller gameplaybeslut.
5. **Three-Stream** blir rådgivande idé för blanking/precompute-/registerscheman, inte ett bevisat byte av R1h:s hårda rasterkernel.
6. Slutlig full R1, full R2 och separat VERIFICATION förblir blockerade. Ingen import/merge, ändring av originalmasker, specialcartridge eller kodorder skapas genom denna rapport.
