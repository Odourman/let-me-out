# TO_MAIN_G5AZ · LM-D32 · ROM DEVELOPMENT IV → MAIN IX

**G5AZ_PARTIAL_RUNTIME_OR_VISIBILITY_PROGRESS** · 18 november 2026

Fem individuella X/Y-par styr de ursprungliga maskerna M, M, F, SM, SF i en körbar NTSC F6-ROM. Alla 50 bilder från de 25 individuella kontrollägena var exakta. `union.bin` gav 600/600 pixelrätta bilder för fyra körda scener, inklusive två överlappande fiender med exakt samma X. De smalare och täta fall som MAIN efterfrågade fallerade. Full koordinatfrihet och samtidiga täta silhuetter återstår. **G5_FORMAL_OPEN kvarstår.**

## Runtime och mätmetod

- Enskild fiende först. Ursprunglig `one.bin` flyttade hela masken höger och vänster, men gav 9–27 extra vita pixlar. Efter VBLANK-positionering via RESP1/HMP1/HMOVE och kalibrering av ett uppmätt konstant −9 pixlars X-fel gav `single.bin` 33/33 exakta bilder vid X 19, 22, 25, 28, 31 och Y 71, 72, 73. Katalogen `early-hmove` i råarkivet bevarar den felkalibrerade versionen.
- `wide.bin` läser X i `$81–$85` och Y i `$86–$8A`. Stabil X-sortering körs varje bild. CPU:n genererar ett tidsatt scanlineprogram i RIOT-RAM, med fördröjning, RESP1/GRP1 och adress till raden i spelarens respektive fiendens mask. Maskerna är byte-identiska med datakällan i fryst G5AY. ROM:ens fyra banker är identiska och scenbytena kräver ingen ombyggnad.
- Gopher-debuggern skrev endast ändrade RAM-byte med POKE och kontrollerade alla tio med PEEK före och efter varje sekvens. För varje NPC-index 0–4 jämfördes bas mot X+3, X−3, Y+1, Y−1 med övriga nio byte oförändrade: 5/5 kontrollägen per index, 2/2 exakta rasterbilder per läge. `stimuli.py` anger varje koordinat och `wide.jsonl` har hela skriv- och läsprotokollet.
- Pixeloraklet jämför råbilder mot maskernas geometriska union och rapporterar synliga unika bitar per NPC. Y-registrering kommer från P0, samma referens för alla fiender. Varje positiv bild innehöll 32 gula P0-pixlar, 25 gula M0-pixlar och bruna PF-väggar. Skottet är kontinuerligt aktivt som rastermarkör. Väggarna är diagnostiska kanter, utan kartintegration.

## Rastermatris

X/Y-listor följer maskidentiteterna. Y72 betyder Y=72 för alla. Fel anges som saknade/extra vita pixlar per bild.

| Fall | X | Y | `union` |
|---|---|---|---|
| Same Y, brett | 19 52 85 118 151 | Y72 | 0/0 |
| Ny X-ordning | 151 19 85 118 52 | 73 72 73 71 72 | 0/0 |
| Ny X-ordning och blandat Y | 52 151 19 118 85 | 70 71 72 73 74 | 0/0 |
| Exakt samma X och överlapp | 79 79 19 112 49 | 75 74 73 72 71 | 0/0, utan OR 14/0 |
| Efterfrågat separerat | 19 46 73 100 127 | Y72 | 48/0, unika förluster 0 28 0 20 0 |
| Efterfrågat ordningsbyte | 127 19 73 100 46 | 73 72 73 71 72 | 42/0, unika förluster 0 0 0 20 22 |
| Tät 3 px | 73 76 79 82 85 | Y72 | 76/28, unika förluster 0 12 21 6 16 |
| Tät 1 px | 73 74 75 76 77 | Y72 | 37/28, unika förluster 0 2 5 2 5 |
| Efterfrågat samma X | 73 73 19 100 46 | 75 74 73 72 71 | 42/0, utan OR 56/0. OR återgav parets egna bitar, två andra NPC tappades. |

`union.bin` bygger en 24-byte OR-bitmap ur första parets aktuella Y-värden när deras X är exakt lika. Den jämförs direkt med fysisk pixelunion. Fler lika-X-aktörer och olika start-X på samma täta rad stöds inte av bitmapgrenen. Den återtriggade banan har X=3c−47 för cykel 22–66 (X=19…151 i trepixlars steg), kräver minst 10 cykler mellan aktiva slots, och har ett 24-raders fönster Y64–87 med hela niopixelsmasker vid Y64–79. Koordinater utanför det utrymmet har inget löfte om exakta bildpunkter. Kärnan registrerar överhopp i `$9C`. Det här är en begränsning i den testade kärnan.

`rotate.bin` använder en återtriggad mask åt gången och gav 20–38 extra vita pixlar per bild. `rotatefine.bin` minskar spökpixlarna via statisk NUSIZ1 och finpositionering. I 20 provbilder återgavs vald mask exakt i 20/20, med 4/20 bilder med synliga unika pixlar per NPC, längst fyra helt frånvarande bilder per NPC (20 % synlighet, ungefär 12 synliga bilder/s vid 60 Hz). Detta fallerar kravet på fem samtidiga läsbara fiender.

## Frame-, cykel- och minnesbudget

- **Gopher2600 v0.57.2.** En körning av `union.bin` med 604 sammanhängande TV FRAME-avläsningar vid 262 scanlines. De 600 poängsatta råbilderna fördelades 150/150/150/150 över matrisens första fyra scener. Fyra övergångsbilder avlästes utan PNG. Varje NPC hade sina unika pixlar synliga i 600/600 poängsatta bilder, längst 0 helt frånvarande. Tidiga 260-raders försök sparades och timerändringen verifierades på riktigt.
- **Stella 6.7.1.** Tolv råbilder vardera av fast grundscen och av samma-X-fixturen. Stella körde samma `wide.bin` och `union.bin`. I den senare hölls konsolens Select ned så att den interna teststyrningen skrev samma X/Y till RAM. 12/12 exakta per fixture. Stella-provet ger ingen motsvarande 600-bilders eller CPU-busstimingmätning.
- **TIA-register.** Gopher TRACE plus STEP INSTRUCTION och TV-ankare för samtliga 24 kritiska scanlines (TV SL100–123) i var och en av två scener. `wide` RESP1 på CPU-cykler 22/33/44/55/66, GRP1 25/36/47/58/69. Same-X `union` RESP1 22/32/42/53, GRP1 25/35/45/56. Loggen har även GRP0 och aktivering av ENAM0 före bandet. Cyklerna avser CPU-skrivslut, härledda från Gophers TV-klocka direkt efter skrivinstruktionen. Intern TIA START är omätt. I värsta positiva raster kommer sista GRP1 på c69, därefter JMP (3) och WSYNC (3) till c75 av 76. Kopieringsläge/NUSIZ, RESP1/GRP1, HMOVE och bildmultiplex provades. VDEL och linjeinterlace är **NOT_RUN**.
- **RIOT 128 byte.** 1 byte bildräknare, 10 koordinater, 5 ordningsindex, 16 arbetsbyte inklusive ett reserverat byte, 24 OR-bitmap, 64 RAM-kod inklusive avslutsväg och reserv, 8 stack. Djupaste JSR-nästling använder 4 stackbyte. Fyra 4 KiB-banker, 16 KiB per ROM, en 4 KiB unik bank. Största byggda kod/markörregion slutar exklusivt vid `$F2B8` (696 byte), X-tabellen tar 256 byte och maskregionerna 4 × 73 byte inklusive nollpadding. Vektorer 6 byte. Övrigt är bankutfyllnad.
- **R2 S05 NOT_RUN.** Den dynamiska R1-kärnan fallerar skilda fiender redan vid 27 px lucka. Fullt aktiva fem slots lämnar dessutom bara en CPU-cykel före linjegränsen efter synkronisering. Någon tillförlitlig samtidig R2-rendering med färgbyte och separat dörr-PF är därför inte visad. Tidigare R2-vänsterkantsavvikelse är omätt i denna leverans. Den tekniska nästa jämförelsen är olika täta X inom en gemensam bitmapruta jämfört med omplanerade P1-slots. Ingen slutsats om fysisk TIA-omöjlighet.

## Bygg och återskapa

Kör från `experiments/g5az` i Codex Cloud `let-me-out`. Använder pinnen i `/workspace/.g5ar-env01` (DASM 2.20.14.1, Stella 6.7.1, Gopher2600 v0.57.2 revision `2af86eb725739adbf3d9d45cea2ed69eea57da2a`) och Pillow 13.0.0. Fulla verktygshashar finns i `tools.sha256` i arkivet. ROM, källor och råarkiv har SHA-256 i `SHA256SUMS`.

```bash
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for mode in single one wide union rotate rotatefine; do
  python runtime_capture.py "$mode" "$out/$mode-png" > "$out/$mode.jsonl"
  python measure.py "$mode" "$out/$mode.jsonl" "$out/$mode-png" "$out/$mode-pixels.jsonl"
done
python runtime_capture.py union "$out/soak-png" --soak > "$out/soak.jsonl"
python measure.py union "$out/soak.jsonl" "$out/soak-png" "$out/soak-pixels.jsonl"
for mode in wide union; do
  python trace_runtime.py "$mode" > "$out/bus-$mode.jsonl"
done
timeout 30s bash capture_stella.sh roms/wide.bin "$out/stella-wide" 181
timeout 30s bash capture_stella.sh roms/union.bin "$out/stella-union" 182 select
```

Råarkivet innehåller orörda PNG, koordinater, SHA per bild, PTY TX/RX, CPU-klockankare, tidiga avvikelser och emulatorernas separata loggar. Avslutande signaler i PTY-loggarna är harnessens städning efter slutförd körning. De sex `.bin`-filerna är separata diagnostik-ROM:ar. Inga spelregler, kartor, huvudbranch, frysta leveranser eller PR:er har ändrats. Leveransen väntar på MAIN IX:s granskning.
