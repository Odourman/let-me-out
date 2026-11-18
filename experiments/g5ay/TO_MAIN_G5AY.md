# TO_MAIN_G5AY · LM-D31

**ROM DEVELOPMENT IV → MAIN IX · G5AY_PARTIAL_RASTER_PROGRESS · G5_FORMAL_OPEN**

Fem vita M,M,F,SM,SF kan i verklig rasterutmatning visas samtidigt i samma nioradersband tillsammans med gul P0, ett synligt M0-skott och bruna PF-väggar. Korrigerad NTSC/F6-kandidat `clean1` gav **600/600 sammanhängande 262-radersframes** i stock Gopher2600. Tre separerade scener gav **456/456 pixel-exakta** bilder. Det avsiktliga X-överlappningsprovet gav **0/144 exakta**. Stock Stella bekräftade samma utfall i 12 separata råbilder. Fri numerisk placering av godtyckliga koordinater i runtime är fortfarande olöst. Diagnostiken använder specialiserade scheman per ROM-bank eller bank/slot, valda med en framecounter. Ingen spelkod eller tidigare leverans ändrades. [Arbetsorder](https://github.com/Odourman/let-me-out/issues/24)

## Testmatris

| Test | Faktiskt utfall | Avgränsning |
|---|---|---|
| F9-primitiv med fem RESP1 och NUSIZ1=0 | `direct` 68 × 263 scanlines. Ingen NPC-mask i separerade samma-Y-rutan, enstaka vita fragment i övriga scener. | Negativ kontroll för denna timing. |
| NUSIZ1=1 med första tidsplanen | `copies` 68 × 263 scanlines. Fem figurer i samma-Y, men fel framelängd och sämre övriga positioner. | VBLANK:s RESM0-positioneringsrad gick statiskt till c79 före WSYNC. |
| Förkortad VBLANK-positionering | `fixedcopies`, därefter `packedcopies`, vardera 68 × 262. Den senare flyttade spelare till vänster och RESP1-strobeplanen för att lämna utrymme åt höger för M0. Ytterligare 600 × 262 på `packedcopies` visade precis en återkommande extra vit pixel i staggered-scenen. | Negativ pixel bevarad i råarkivet. |
| GRP1 fördröjt vid NPC 0 på synlig rad 71 | `clean1` och `clean2` med +1/+2 CPU-cykler gav vardera 68 × 262; 16/16 staggered pixel-exakta i båda. Valde det mindre ingreppet `clean1` för 600-frame-test. | RESP1-tid oförändrad. TIA START-tid mättes inte. |
| Samma Y, separerat X | `clean1`, 159/159 Gopher frames pixel-exakta. Två av 12 Stella-bilder tillhörde scenen, båda pixel-exakta. | Alla fem renderade i en enda frame, inga växlande grupper. |
| Numerisk omordning och tätare spridning | `clean1`, 153/153 Gopher frames exakta. Fyra av fyra Stella-bilder exakta. | Styrningen är förkompilerad per identitet. Ingen allmän runtime-sortering eller placering. |
| Intilliggande Y-start/slut | `clean1`, 144/144 Gopher frames exakta. Fyra av fyra Stella-bilder exakta. | Fem intilliggande startlinjer med P0/M0/PF aktivt. |
| Samma X, överlappande Y | `clean1`, 144/144 Gopher frames saknar 10 väntade unika vita pixlar för NPC 1 och har 2 extra pixlar. Två av två Stella-bilder visar samma fel. | Schemat markerar explicit tappade strobes när två begär samma slot eller tidsavståndet är för kort. Det är en negativ renderingstest, ingen tillåten gameplay-prioritet. |
| En koordinat i taget | `contrasts`: 68 × 262, 63/68 totalt exakta. För samtliga fem matchade +1 CPU-strobe-cykel (+3 pixlar) och +1 Y-rad per identitet, med en extra pixel i en NPC1 Y+-bild. Fyra av fem −X-kontraster var exakta. NPC0 c21 gav avvikande maskplacering i 4/4. | Tre förkompilerade timingpunkter per NPC och två Y-värden. Övriga fyra maskpositioner ändras inte när en koordinat manipuleras i dessa kontraster. Ingen fri kombination utanför schemat. |
| Frame-alternation | `alternate` utan NUSIZ-kopiering misslyckades. Reviderad `splitcopies` med 3+2-maskers frame-alternation gav 68 × 262 men varje fiende syntes bara **34/68** med högst en följande osynlig frame. | Negativ farosynlighetsjämförelse. Ingen flimmerwaiver. |
| R2 samvisning | `r2probe` 16 × 262, guldfärg spillde över på 15 NPC-pixlar när COLUP1 bytte för nära fjärde spriten. `r2probe2` flyttade de fyra NPC tidigare. **16/16 Gopher + 12/12 Stella** råbilder gav 114/114 vita NPC-pixlar, 17/17 guldnyckelpixlar, 32 P0-pixlar och 10 M0-pixlar samt en orange högerdörr med svart 4×3 öppning. | Ett fast, icke-överlappande testläge. PF0-hålet smalnar även vänster testvägg på några rader och skottet hålls aktivt genom hela testbandet. Ingen kartintegration, ingen gameplay och inget bevis för nyckelns olika överlappsfall. |

Identitetsordning i tabellen är M₀,M₁,F,SM,SF. X anges i fysiska 160-pixelskoordinater som maskens vänsterkant. Y är synlig kodscanline. Raderna för de två M i överlappningsprovet är avsedda koordinater, även om andra maskens pixlar delvis uteblir.

| `clean1`-scen | X | Y |
|---|---|---|
| Samma Y | 19, 46, 73, 100, 127 | 72, 72, 72, 72, 72 |
| Omordning | 130, 19, 73, 103, 46 | 73, 72, 73, 71, 72 |
| Intilliggande Y | 46, 127, 19, 100, 73 | 70, 71, 72, 73, 74 |
| Avsiktlig X-överlapp | 73, 73, 19, 100, 46 | 75, 74, 73, 72, 71 |

Alla fem hade minst en egen synlig vit pixel i 600/600 `clean1`-frames, längsta följd helt utan egna pixlar **0**. NPC1 hade full mask i 456/600 frames. De övriga fyra hade alla sina förväntade bitar i 600/600. Den överlappande scenen ska bedömas som fel trots delvis synliga masker. Varje `clean1`-frame visar 32 gula P0-pixlar, 2 gula M0-pixlar och 3072 bruna PF-pixlar på det normaliserade pixelgittret.

## Register, budget och begränsning

Gopher_TRACE vid frame **20**, scanline **112** i `clean1` bank 1 gav följande faktiska CPU-skrivningar, tidsatta med `TV` direkt efter respektive instruktion. Cykelvärdet är instruktionens observerade slutgräns härledd från beam, inte TIA intern START.

| Register | Observerade CPU-cykelgränser inom raden |
|---|---|
| GRP0 | 5, värde 1E |
| ENAM0 | 10, värde 02 |
| RESP1 | 22, 31, 40, 50, 59 |
| GRP1, nollning följd av masker | 15, 25, 34, 43, 53, 62 |

Kompletterande Gopher-trace på `packedcopies` registrerade faktisk `PF0 ← $30` vid uppstart och 5 × RESP1/5 × mask-GRP1 per aktiv rad i provet. En första scanline-trace stannade korrekt vid tomt WSYNC-intervall; det råutfallet finns kvar, följt av den korrigerade mätningen. Kandidatens källräknade radslut för värsta aktiva rad är c65 inklusive WSYNC, mot 76. Max för `clean1` är c74 på VBLANK-raden som sätter M0. `r2probe2` pressar aktiv rad till c73 för sista PF-färgskrivning och c76 inklusive WSYNC; alla 16 uppmätta frames var 262.

Den direkta sekvensen för en ny mask kräver minst **8 CPU-cykler** med omedelbar bitmap-load, RESP1 och GRP1. Tre klockor per cykel ger cirka 24 pixlars minsta spacing i det bevisade kopieringsläget. Den mätta omordningsscenen har minst 27 pixlar mellan maskursprungen. Tätare och samma-X-fall kan därför inte översättas till valfria strobetider med denna sekvens. Överlappningsprovet visar den faktiska förlusten när två aktörer konkurrerar om samma slot. Detta är en begränsning för testkärnan, ej en generell omöjlighet för TIA eller en ändring av spelmålet.

**Minne:** Varje ROM är 16 384 byte med fyra 4096-byte-banker och 6 vektorbytes per bank. `clean1` bankspecifikt sammanhängande innehåll från $F000 till `EndKernel` exklusive vektorer är 692, 742, 758 och 696 byte. `contrasts` använder som mest 2463 sammanhängande byte plus 6 vektorbytes. `clean1` använder 1 byte arbetstillstånd i RIOT-RAM ($80 framecounter). `contrasts` använder 3 ($80–$82, två dispatchpekare). Init nollställer 128 byte och de synliga kärnorna har inga subrutinanrop eller stackdata. Koordinaterna kodas i bankernas schema och lagras inte som en komplett dynamisk NPC-motor i RAM.

## Reproduktion och råbevis

Git-bas `ced1ce3efc5c14f29ced4034f8d59c61edab2ad7`. Ursprungliga F9 används som orörd teknisk referens (commit `c36982aef770af6cd3f68c2da37b8ed14aee2393`). Källmasker är den byteidentiska kopian `masks.json` av `design/NPC_REFERENCE_8x9_masks.json`. Skärmen är en testfixtur med PF-sidoväggar, utan rumscanon eller spelregler. [F9-baskvitto](https://github.com/Odourman/let-me-out/blob/ced1ce3efc5c14f29ced4034f8d59c61edab2ad7/docs/MAIN_V_R1_F9_RECEIPT_INDEPENDENT_EVIDENCE_AUDIT_AND_ARCHITECTURE_DECISION_2026-11-17.md) · [Masker](https://github.com/Odourman/let-me-out/blob/ced1ce3efc5c14f29ced4034f8d59c61edab2ad7/design/NPC_REFERENCE_8x9_masks.json)

- Kör från denna katalog. `python3 build.py clean1` genererar fyra ASM-källor, kör DASM **2.20.14.1** per bank med `-f3 -o<bank>.bin -l<bank>.lst -s<bank>.sym`, kontrollerar gemensamma bytes fram till bankbytet och sammanfogar bankarna i F6-ordning. Samtliga 11 kandidater återbyggdes byteidentiskt i en tom katalog. Se `evidence/rebuild.stdout`.
- Gopher **v0.57.2**, rev `2af86eb725739adbf3d9d45cea2ed69eea57da2a`. `timeout -k 2s 90s python3 -B capture.py clean1/g5ay_clean1_F6.bin /workspace/work/g5ay/images-clean600 600 --all-images > clean600.raw.jsonl` ger canonical PTY/VEOF, versions- och F6-kvitto, `STEP FRAME`, `TV`, `TV FRAME`, en oförändrad HEADLESS PNG per frame. De två första frame-stegen skippas. Faktiskt räknade frames **3–602**. Gopher HEADLESS PNG är emulatorns egen skalade bild och sparades med oförändrade bytes. Analysen skalar tillbaka pixlar offline utifrån emulatorns rapporterade crop.
- TIA-busstrace `timeout -k 2s 25s python3 -B trace_cycles.py` på `clean1`. `trace_row.py` ger den kompletterande PF-/rastertracen på `packedcopies`. Varken instruktionens beamgräns eller PNG belägger fysisk intern TIA START.
- Stella **6.7.1**, `timeout -k 2s 18s bash capture_stella.sh clean1/g5ay_clean1_F6.bin /workspace/work/g5ay/stella-clean 60`. Stock GUI, NTSC/F6, Xvfb och F12 i 1× TIA-läge. Uppmätta 320×228 PNG är separata **STELLA_OBSERVED**-bildstickprov. De är inte en Stella-600-frame-serie. Gopher-600 är **GOPHER_OBSERVED**. Stella kan skriva ALSA-varning i miljön; snapshotter skapades. Gopher-processerna behövde SIGKILL efter färdig insamling, exit −9 i child-logg och exit 0 för godkända capture-harness, se rådata.
- Offline `python3 -B pixels.py clean600.raw.jsonl images-clean600 clean1/schedule.json clean600-pixels.jsonl` (filer finns i råarkivet). `crosscheck.py` granskar oförändrade Stella- och R2-PNG. `evidence/raw-evidence.tar.gz` innehåller alla ursprungliga PNG, TX/RX, stderr, fallerat traceprov, per-frame pixelstatus, Stella- och rebuildloggar. `SHA256SUMS.txt` pinnar kapsel, analyser, ROM och källor. Under `evidence/examples/` finns omodifierade bildexempel.
- Bästa R1 ROM `2922849393aaccf59aeab811ebdb75743eb465aef9f9c7a35517c3a4fec80ee0`. Bästa R2-probe `3ef3aca20fd66e0e2ee8a62bc7c3cf26ac67fa0d01b9ef0c398d0e44fe16e727`. Gopher-binär `cca432ce75589d806b4d52ae48b76501e74dd4db0259ffe2b94c01853b0b3148`, Stella-binär `e1f89b28a26528214f4288498811e1356459ad55498e1e0e00925e876515cee0`, DASM-binär `c177b2fcd4405dc65ef0be1a7b80d7900c1597bac63ba0f4f37bdc7e8fcd6f50`.

**NOT_RUN i denna order:** generell runtime-X/Y över alla kombinationer, produktionskartor/komplett S05, TIA intern START-tid, PAL, AI/kollision/poäng eller annan gameplay samt oberoende Verification II. R1- och R2-ledtrådarna stödjer en fortsatt test-only undersökning av runtime-schemaläggning och tät geometri. Detta avslutar G5AY och lämnar nästa order till MAIN IX.
