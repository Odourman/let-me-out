# TO_MAIN_G5BE_ITER2 · LM-D37 · ROM DEVELOPMENT IV → MAIN IX

**G5BE_ITER2_MULTIROW_PIXEL_EXACT_OBSERVED_BOUNDED.** Alla fem ursprungliga 8×9-masker återges samtidigt vid sina rätta X/Y i den historiska omordningen. Y71–81 ritas fysiskt efter varandra i samma bildruta. Samma körbara RAM-ROM klarade ytterligare tre positionslägen och 600 sammanhängande bildrutor med 262 scanlines och 0 saknade, 0 extra vita pixlar. 19 av 20 äldre fixturer ligger utanför kärnans koordinatområde och ger FAIL för NPC-renderingen. Allt emulatorevidens är utvecklarens egenkontroll.

## ROM och testmatris

| ROM och körning | Bilder | NPC-resultat i samma bildruta | NTSC |
|---|---:|---|---|
| `chain.bin`, statiskt Y76–77 | 8 | PASS, 42/42 avsedda pixlar | 8/8 × 262 |
| `chain.bin`, statiskt Y74–78 | 4 | PASS, 94/94 avsedda pixlar | 4/4 × 262 |
| `chain.bin`, statiskt Y71–81 | 4 | PASS, 136/136 och alla fem fullständiga masker | 4/4 × 262 |
| `stream.bin`, RAM, historisk + två nya omordningar + separerat | 600 | PASS, 136/136 i varje bildruta | 600/600 × 262 |
| `stream.bin`, liveväxlingar med nära, överlappande och breda negativkontroller | 48 | PASS 28, FAIL 20 | 48/48 × 262 |
| `stream.bin`, 8 äldre familjer + 12 seedade fixturer | 60 | PASS 3 bilder i 1 fixtur, FAIL 57 i 19 | 60/60 × 262 |
| Stella stock 6.7.1, historisk helbild | 12 statiska + 11 RAM | PASS 23/23, exakt historisk geometri och RGB | NOT_RUN för radantal |
| Stella stock 7.0, historisk helbild | 12 statiska + 12 RAM | PASS 24/24, exakt historisk geometri och RGB | NOT_RUN för radantal |

De statiska deltesten begränsar avsiktligt antalet rader inom en bildruta. Hela bandet Y71–81 har förväntade vita pixelantal `[0,4,16,18,18,26,16,16,12,6,4]`. Historisk helbild har `[28,28,38,20,22]` pixlar i M, M, F, SM, SF. Alla dessa finns i Gopher och båda Stella-versionerna. Referensen är den frysta G5BE-iterationens fungerande Y76-fall, fäst vid den gula spelarens mask. Spelare, skott och väggar har exakt samma `(x,y,RGB)` som den frysta bilden inom varje emulator, med 32, 25 respektive 3047 pixlar. Gophers RGB är vit `255,255,254`, gul `255,255,41`, brun `199,107,33`. Båda Stella-versionerna gav vit `234,234,233`, gul `253,253,72`, brun `173,111,38`.

RAM-körningen verifierade samtliga tio ändrade RAM-byte med debugger-PEEK innan varje lägesblock. Bildrutorna är FR 5–604 utan avbrott. Blockordningen är historisk, vänsterförskjuten omordning, högerförskjuten omordning, vänsterförskjuten omordning igen, historisk igen och separerad. Pixelmatrisen verifierar varje bildruta, inklusive första bildrutan efter varje ändring.

| Läge | X, M/M/F/SM/SF | Y, M/M/F/SM/SF |
|---|---|---|
| Historisk | 127, 19, 73, 100, 46 | 73, 72, 73, 71, 72 |
| Vänsterförskjuten | 19, 127, 73, 46, 97 | 72, 73, 71, 72, 73 |
| Högerförskjuten | 103, 73, 46, 127, 19 | 71, 73, 72, 71, 72 |
| Separerad | 19, 46, 73, 100, 127 | 72, 72, 72, 72, 72 |

Stödd topologi i denna ROM har sorterade X `[19,46,73,97|100|103,127]` och oberoende Y i intervallet 71–73. Den tredje sorterade figuren ritas av P0:s andra kopia. För olika RAM-ordningar flyttas vilken originalmask som fyller varje slot. Inga specifika identitetspermutationer förkompileras i ROM. Utanför topologin avvisar diagnosen hela NPC-bandet. Den äldre separerade fixturen är PASS. Tätgrupper, delat X, två par, äldre omordningar utanför topologin och de tolv seedade scenerna är FAIL. Fri RAM-X/Y är därmed FAIL i regressionsmatrisen. Uttömmande test av den tillåtna topologin och 600-rutors timing i Stella är NOT_RUN.

## Timing, assembler och solver

Båda metoderna bygger standard F6, 16 KiB med fyra identiska banker. `chain` materialiserar radens maskoperander från det frysta c49-schemat i ROM. `stream` sorterar de fem RAM-X-koordinaterna, bygger fem maskpekare och fyller 55 byte RIOT-radcache på 11 VBLANK-rader. Därefter använder den raka radkedjor med `LDA/LDX zp`; en långsammare indexerad grafiklast körs aldrig inne i kedjan. Radcacheförberedelsen använder 57 cykler per rad som längst, inklusive synkroniseringsskrivningen. Originalmaskerna och all diagnostik finns i den isolerade katalogen.

Gopher mätte 262 scanlines i 724/724 bildrutor i de fyra matrisgrupperna, även när kommande koordinater ligger utanför kärnans topologi. En separat busskörning följde 12 live sceninträden i stressordningen, 12/12 × 262. VSYNC är tre rader. VBLANK-fördelningen ger 37 rader efter VSYNC, 192 synliga och 30 overscan. I Gophers TV-koordinater ligger avblankning runt SL36, bandinträde efter SL106, bandutgång SL118 vid CL−68 och overscan runt SL228. Hårdvaruspåret innehåller `VSYNC/VBLANK/WSYNC`, grafik, kopior, färg och RESP-skrivningar. Upprepade identiska WSYNC-skrivningar som samlas i samma svar reduceras i Gophers visning. JSON-fältet `wsync` räknar därför trace-rader, medan den faktiska bildrutans radantal mäts via `TV FRAME`. De okomprimerade kvittenserna finns under `evidence/brief/`.

Binära cykelrevisionen kontrollerar alla 18 statiska och 33 cachematade radpaket. Varje radpaket är 76 CPU-cykler inklusive avslutande hopp eller utfyllnad. Sista TIA-skrivningen slutar vid c70 eller c71. Färghändelserna i modellen anges i CPU-cykler, med tre TIA-färgklockor per cykel. `PlayerRows,Y` och VBLANK-maskläsningarna stannar på respektive sida. Dynamisk kärna använder 88 adresserade RIOT-byte under körning och högst två stackbyte vid maskpekardelen, totalt 90/128 inklusive den gemensamma initialiseringens MODE-byte. Statisk kärna har fem aktiva state-byte, ingen stack i renderern. Båda kärnorna nollställer RAM vid reset.

Z3 4.15.4 gav SAT med trecykels maskladdning för fjärde RESP1-stroben c48, c49 och c50. Fyrcykelslast gav UNSAT i alla tre fall under den här modellens fasta kopior, strobfönster, A/X-livslängder, `GRP0/GRP1`-skrivningar, CPU-budget och M0/COLUP0-fönster. Det är en begränsad modell med empiriskt kalibrerade fönster. VDEL används inte av de nya radkedjorna. RGB-, pixel- och timingresultaten kommer från separata emulatorobservationer.

### Bevarade negativa resultat

- Den första cachepipeline-ROM:en gav 12/12 ramar på 263 rader trots exakta NPC-pixlar. M0 hade 27 i stället för 25 pixlar och väggen 3062 i stället för 3047. Grenen före bandet flyttade ingångens WSYNC över radgränsen. En kortare led-in-fördröjning i den dynamiska vägen korrigerade felet.
- Efter timingkorrigeringen gav den separerade kontrollen fortfarande 0/136 NPC-pixlar. Y-temporären låg på samma RIOT-adress som giltighetsflaggan. Separat temporär på `$9C` behöll flaggans värde och åtgärdade det under den separerade kontrollen och den slutliga 600-körningen.
- Tidigare frysta rapporter och filer ligger på sina ursprungliga refar. Båda negativa kandidaterna med råloggar och bilder finns som `boundary-fail/` och `validity-fail/` i råarkivet.

## Bygg och bevis

- `chain.bin` SHA-256 `46e57148adee366b94d5dcc703538a23478e4a143d001e44280b131a91a2c50a`
- `stream.bin` SHA-256 `8b27a8d1fe8cf8a6e05cd5b185d6b6dc79753811c980f4c52be043f22d97c810`
- `SHA256SUMS` kontrollerar källor, ROM, bilder, budget, loggar och råarkiv. `evidence/examples/` har orörda PNG-filer. `evidence/brief/` har direktläsbara bildradsjämförelser, RGB, CPU-/TIA-händelser, NTSC-fasloggar och full regressionsmatris. `evidence/raw.tar.gz` har råa PTY-byte, samtliga emulatorbilder och negativa kandidater.

| Verktyg använt | Kommando | Direkt evidens |
|---|---|---|
| DASM 2.20.14.1, verifierat G5AR-prefix | `python build.py` | `roms/*.lst`, `roms/*.sym`, binärhasharna ovan |
| Gopher2600 v0.57.2, verifierat G5AR-prefix | `replay.py`, `timing.py` | `evidence/brief/soak-frames.jsonl`, `hardware-writes.jsonl`, rå PTY i arkivet |
| Stock Stella 6.7.1 och stock 7.0, G5AR och isolerad G5BB | `capture_stella.sh` | original-PNG, `evidence/brief/stella-*-score.jsonl` |
| Z3 4.15.4, pinnad `z3-solver==4.15.4.0` | `schedule.py` | `solver.jsonl` och `evidence/brief/solver.tsv` |
| Python/Pillow | `score.py` och `audit.py` | `evidence/brief/*-score.jsonl`, `cycles.jsonl` |

Dessa verktyg kördes mot de levererade kandidaterna. Verktygsversioner och binärhashar finns i [tools.txt](evidence/brief/tools.txt). Motsvarande filloggar och deras SHA-256 står i [SHA256SUMS](SHA256SUMS). [Issue #19](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [G5BB:s verktygsrapport](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

Kör från `experiments/g5be_iter2` med det publicerade verktygsprefixet och den isolerade stock Stella 7.0 från G5BB. `build.py` kör DASM 2.20.14.1 med `-DDYNAMIC=0` respektive `-DDYNAMIC=1`, `-f3` och separata bytekartor. Python och bibliotek måste finnas i aktiv miljö. Originalkommandon och verktygshashar finns i källan och `evidence/brief/tools.txt`.

```bash
sha256sum -c SHA256SUMS
python -m venv /tmp/g5be-iter2-z3
/tmp/g5be-iter2-z3/bin/pip install -r requirements.txt
/tmp/g5be-iter2-z3/bin/python schedule.py > /tmp/g5be-iter2-recomputed.jsonl
cmp solver.jsonl /tmp/g5be-iter2-recomputed.jsonl
python build.py
python audit.py | cmp - evidence/brief/cycles.jsonl

out=$(mktemp -d)
python replay.py roms/chain.bin "$out/chain" --frames 16 > "$out/chain.jsonl"
python replay.py roms/stream.bin "$out/stress" --dynamic --stress --frames 48 > "$out/stress.jsonl"
python replay.py roms/stream.bin "$out/legacy" --dynamic --legacy > "$out/legacy.jsonl"
python replay.py roms/stream.bin "$out/soak" --dynamic --frames 600 > "$out/soak.jsonl"
python timing.py roms/stream.bin > "$out/phases.jsonl"
for run in chain stress legacy soak; do
    python score.py "$out/$run" evidence/examples/frozen-gopher-y76.png \
        --ref-height 214 --log "$out/$run.jsonl" > "$out/$run-score.jsonl"
done

bash capture_stella.sh roms/chain.bin "$out/stella671-chain" 191
bash capture_stella.sh roms/stream.bin "$out/stella671-stream" 192
export STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella
bash capture_stella.sh roms/chain.bin "$out/stella70-chain" 193
bash capture_stella.sh roms/stream.bin "$out/stella70-stream" 194
for mode in chain stream; do
    python score.py "$out/stella671-$mode/images" evidence/examples/stella-671-frozen.png
    python score.py "$out/stella70-$mode/images" evidence/examples/stella-70-frozen.png
done
```

**Slutsats till MAIN IX:** Fysisk flerradskedja, historisk helbild och begränsad live-RAM-styrning är PASS. Generalisering över äldre fixturer är FAIL. Oberoende Verification är NOT_RUN. `G5_FORMAL_OPEN` kvarstår.
