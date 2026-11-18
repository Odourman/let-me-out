# TO_MAIN_G5BA · LM-D33 · ROM DEVELOPMENT IV → MAIN IX

**`G5BA_PARTIAL_DENSE_RUNTIME_PROGRESS` · 18 november 2026**

`hybrid.bin` återgav fem RAM-styrda originalmasker i samma bild med ett SM/SF-par på **1–2 pixlars olika X**, plus tre andra fiender, P0, aktivt M0 och båda PF-väggkanterna. Den återgav också två par samtidigt, ett nära SM/SF-par och två M-masker vid samma X med olika Y. **600/600 analyserade Gopher-bilder var pixelrätta vid 262 scanlines.** De fem historiska G5AZ-fallen fallerar fortfarande. **`G5_FORMAL_OPEN` kvarstår.**

## Två figurer och ΔX/ΔY

`pair.bin` sorterar SM/SF:s verkliga X, väljer en vänsterankare, flyttar originalradernas bitar och OR:ar dem i en 24-byte cache. En spillande tänd bit fäller den fasta ankarplanen. När hela planen avvisas behålls den vänstra masken. RESP1/HMP1/HMOVE under VBLANK ger fin-X och NUSIZ1=$00 ger en P1. En körning täckte ΔX 1–8 × ΔY 0–2 med två råbilder per läge. Tabellen anger **saknade pixlar** för ΔY 0/1/2, med **0 extra** i varje rad och två identiska mätresultat per läge. Noll i båda riktningarna är PASS.

| ΔX i pixlar | `pair.bin` | `rowprobe.bin` |
|---|---:|---:|
| 1 | 0 / 0 / 0 | 0 / 0 / 0 |
| 2 | 0 / 0 / 0 | 0 / 0 / 0 |
| 3 | 16 / 18 / 19 | 3 / 5 / 5 |
| 4 | 20 / 22 / 20 | 18 / 20 / 18 |
| 5 | 21 / 22 / 22 | 21 / 22 / 22 |
| 6 | 22 / 22 / 22 | 22 / 22 / 22 |
| 7 | 22 / 22 / 22 | 22 / 22 / 22 |
| 8 | 22 / 22 / 22 | 22 / 22 / 22 |

`rowprobe.bin` behåller det vänstra originalets rad när högra raden spiller och lägger annars till hela högra raden. Detta räddade 13–14 vita pixlar per bild vid ΔX=3. Det högra originalet förlorade ändå 3–5 unika pixlar i de lägena och syntes i 32/56 bilder över hela radmatrisen, max 24 helt frånvarande bilder i den poängsatta sekvensen. `pair.bin` hade 20/56 bilder med högra maskens unika pixlar, max 36 helt frånvarande i samma testordning. Båda gav 20/56 pixelrätta bilder, inklusive X-rest 0/1/2 och omvänt par. Alla 112 poängsatta bilder var 262 scanlines. Dessa är avgränsade diagnoser.

## Fem RAM-styrda fiender

`hybrid.bin` använder XP `$81–$85`, YP `$86–$8A` och stabil sortering per bild. Den bygger en kompakterad bitmap för första passande grannpar och genererar P1-programmet i RAM. Ett andra par med identiskt X får en tidsatt `ORA abs,Y` direkt i programmet, utan en andra radcache. Slotarna planeras om från aktuell RAM med RESP1/GRP1 på varje rad. De logiska identiteterna M, M, F, SM, SF förblir separata. PNG-oraklet jämför verkliga vita pixlar mot den geometriska unionen och mäter varje mask utanför faktisk pixelocklusion. P0 används som vertikal referens, gemensam för alla fiender. M0 är ett kontinuerligt aktivt diagnostiskt skott.

| Långtest, 120 poängsatta bilder vardera | X, i identitetsordning | Y | Rätt |
|---|---|---|---:|
| Nära 2 px, same-Y | 55 91 130 24 26 | 72 72 72 72 72 | 120/120 |
| Nära 1 px, förskjutet Y | 55 91 130 24 25 | 72 72 72 71 73 | 120/120 |
| Omordning och motrörelse | 91 130 55 26 24 | 73 72 70 72 74 | 120/120 |
| Exakt samma X | 55 91 130 24 24 | 72 72 72 71 73 | 120/120 |
| Två par | 70 70 130 24 26 | 71 73 72 71 73 | 120/120 |

Gopherloggarna visar **605 sammanhängande TV FRAME-avläsningar vid 262**, där 5 övergångsbilder efter koordinatskrivning loggades utan PNG. Varje fiende hade synliga unika pixlar i 600/600 poängsatta bilder, max 0 helt frånvarande. Varje poängsatt bild hade 32 gula P0-pixlar, 25 gula M0-pixlar och 3047 bruna PF-pixlar. PEEK kontrollerade alla 10 byte före och efter scenen. I separat matris var **48/50** isolerade kontrollbilder pixelrätta över 25 lägen. Alla fem Y±1 och båda små fienders X±1 gav korrekta bilder. Enda felet var NPC0 X55→52, där avståndet till kompositens X25 minskar från 30 till 27. Hela den första M-masken om 28 pixlar uteblev i båda bilderna.

| Fryst negativ fixture, återkörd oförändrad | Saknade / extra, varje bild | Saknade unika per NPC 0–4 |
|---|---:|---|
| Separerat X=19/46/73/100/127 | 48/0 | 0 / 28 / 0 / 20 / 0 |
| Omordnat X=127/19/73/100/46 | 42/0 | 0 / 0 / 0 / 20 / 22 |
| Close3 X=73/76/79/82/85 | 76/28 | 0 / 12 / 21 / 6 / 16 |
| Close1 X=73/74/75/76/77 | 37/28 | 0 / 2 / 5 / 2 / 5 |
| Same-X X=73/73/19/100/46 | 42/0 | 0 / 0 / 0 / 20 / 22 |

Varje rad är **FAIL**, tre bilder per läge, vid 262 scanlines. En tidig femfiendersprototyp med HMOVE bara under VBLANK följt av återtriggers för de andra fienderna tappade 32–37 pixlar redan i fyra senare positiva lägen och gav en 263-radersprofil i ett ordningsfall. Den aktiva P1-positionen behöver återställas på varje rad när samma register återanvänds. En andra tidig prototyp avvisade vissa par först efter radberäkning och gav 319/325 rader i close1/close3. Källans bredduppskattning före radloopen tog bort det uppmätta timeröverskridandet. Båda prototypernas ROM, källsnapshot, bilder och loggar finns i råarkivet.

## Faktisk timing, budget och Stella

Gopher2600 v0.57.2, revision `2af86eb725739adbf3d9d45cea2ed69eea57da2a`. TRACE/STEP/TV följde alla 24 aktiva rader (SL100–123) i var och en av sex kontrollscener. Cykler är CPU-skrivslut. Intern TIA START är **NOT_DETERMINABLE** med dessa mätningar. WSYNC återfanns vid följande rads CL −68. Källans längsta aktiva väg har sista GRP1 c69, JMP c72 och WSYNC c75 av 76. P0:s skrivning och M0:s aktivering finns i råspåret.

| Test | RESP1 inom aktiva raden | GRP1 inom aktiva raden |
|---|---|---|
| `pair` ΔX2, `rowprobe` ΔX3 | inga | 20 |
| Fem med nära par | 24 / 34 / 46 / 59 | 27 / 37 / 49 / 62 |
| Fem med två par | 24 / 39 / 59 | 27 / 42 / 62 |
| Historiskt close1 | 40 | 43 |
| Brett femslots-kontrolläge | 22 / 33 / 44 / 55 / 66 | 25 / 36 / 47 / 58 / 69 |

Vid HMOVE i `pair` respektive `rowprobe` observerades CL −68→−59 under VBLANK, på SL29 respektive SL24. NUSIZ1 initierades med uppmätt CPU-skrivning av `$00` i båda par-ROM:arna och `$01` i hybrid (TIA två kopior med kort avstånd). Timade enkla slots kräver minst 10 cykler mellan RESP1-skrivningar, motsvarande 30 pixlar. Inline-OR-paret behöver fyra ytterligare cykler före strobning. Hybridens ankare ligger kvar på X=19…151 i 3-pixelssteg, medan de logiska SM/SF-värdena kunde röra sig ±1 inuti bitmapen. Rasterbandet Y64–87 och hela originalmasker vid Y64–79 är källans intervall. Den verifierade geometrin är de dokumenterade fixturerna.

RIOT-reservationen är **128 byte**. `$80` bildräknare, `$81–8A` 10 koordinater, `$8B–8F` 5 sortindex, `$90–9F` 16 arbetsbyte, `$A0–B7` 24 radbytescache, `$B8–F7` 64 genererad kod, `$F8–FF` 8 stackbyte (max 4 använda i nästlade JSR). F6 omfattar fyra byteidentiska 4 KiB-banker per ROM. Den största kod/markörregionen är 952 byte, X-tabellen 256, maskregionerna 292 inklusive padding och vektorerna 6 byte per unik bank. Resten är utfyllnad.

**Stella 6.7.1** gav 12/12 pixelrätta positiva stickprov vardera för `pair`, `rowprobe` och `hybrid` (36 totalt). Tolv negativa bilder per ROM bekräftade ΔX8 = 22/0 saknade/extra i parvarianterna och close1 = 37/28 i hybrid. Stella använde uppstart och konsol-Select, medan Gopher matades med POKE/PEEK. Råbilderna sparades separat. Stella-resultatet är stickprov utan 600-bildersprofil eller CPU-trace.

**NOT_RUN** gäller VDEL, växlande spritekopielatch inom samma täta rad och R2/S05. VBLANK-HMOVE, radvis återtriggning, komplett bitmapunion och radvis förlustbegränsning är faktiskt provade. Ytterligare täta maskrader med fler än två nära aktörer har fortfarande pixel-FAIL. För nästa tekniska jämförelse är den praktiska frågan om en extra självständig pixelkälla kan rita överskjutande maskbitar där två P1-strobningar ligger för nära. Inga resultat här ger någon generell TIA-omöjlighet eller flimmerwaiver.

## Reproduktion

Från `experiments/g5ba` på specialistbranchen. Verktyg från `/workspace/.g5ar-env01` (DASM 2.20.14.1, stock Stella 6.7.1, Gopher2600 v0.57.2) och Pillow 13.0.0. Verktygshashar och fryst G5AZ-referenshash finns i råarkivet. `SHA256SUMS` täcker källor, de tre körbara ROM:arna, byggprodukter, exempelbilder och råarkiv.

```bash
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
export PYTHONDONTWRITEBYTECODE=1
out=$(mktemp -d)
n=184
for mode in pair rowprobe hybrid; do
  python runtime_capture.py "$mode" "$out/$mode-png" > "$out/$mode.jsonl"
  python measure.py "$mode" "$out/$mode.jsonl" "$out/$mode-png" "$out/$mode-pixels.jsonl"
  timeout 30s bash capture_stella.sh "roms/$mode.bin" "$out/stella-$mode-positive" "$n"
  n=$((n+1))
  timeout 30s bash capture_stella.sh "roms/$mode.bin" "$out/stella-$mode-negative" "$n" select
  n=$((n+1))
done
python measure_stella.py "$out" > "$out/stella-pixels.jsonl"
python runtime_capture.py hybrid "$out/soak-png" --soak > "$out/soak.jsonl"
python measure.py hybrid "$out/soak.jsonl" "$out/soak-png" "$out/soak-pixels.jsonl"
python trace_runtime.py pair dx2-dy0 > "$out/bus-pair.jsonl"
python trace_runtime.py rowprobe dx3-dy0 > "$out/bus-rowprobe.jsonl"
for fixture in close2 two-pairs historic-close1 wide-control; do
  python trace_runtime.py hybrid "$fixture" > "$out/bus-$fixture.jsonl"
done
```

PTY-loggarna innehåller kommandokvittens, rå TX/RX och processavslut. Avslutssignalerna kommer från harnessens städning. Råarkivet innehåller även parseromtag för WSYNC/HMOVE/NUSIZ och det separata utfallet för varje bild. Allt ovan är **utvecklarens egenkontroll**. Spelregler, godkända masker, fryst G5AZ, huvudbranch och PR:er är intakta. Uppdraget stannar här för MAIN IX:s mottagningsgranskning.
