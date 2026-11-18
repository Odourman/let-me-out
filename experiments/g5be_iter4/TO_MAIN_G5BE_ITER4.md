# TO_MAIN_G5BE_ITER4 · LM-D37 · ROM DEVELOPMENT IV → MAIN X

**G5BE_ITER4_OUTER_X_DECOUPLED_BOUNDED.** Den femstrobs P1-kärnan klarar den högra fiendens X127→X130/X133/X136 via RAM i samma ROM, med de andra fyra stilla. En andra byggvariant klarar även fjärde sorterade X100→X97/X103 och kombinerad rörelse i tre slots. En tredje byggvariant breddar den uppmätta Y-spridningen från två till sju rader. Alla PASS nedan innebär fem fullständiga originalmasker med 0 saknade/0 extra pixlar samt oförändrade positioner och RGB för gul spelare, M0 och bruna väggar.

Utgångspunkt är [MAIN X:s order](https://github.com/Odourman/let-me-out/issues/30#issuecomment-6988885272) och fryst ITER3 `6107493e5d3ba49730ab4116e2ac518b193379e2`. Maskfilen jämfördes byte för byte med `design/NPC_REFERENCE_8x9_masks.json`.

## Fysisk positionering i det frysta kontrollprovet

Gopher2600 körde den frysta ROM:en med samma Y-vektor `[73,72,73,71,72]` och ändrade enbart F:s X i `[127,19,X,100,46]`. Alla 32 mätta bildrutor höll 262 scanlines. Bussen mättes genom att stega den faktiska 6507-koden på synlig Y76 och läsa TV:s färgklocka före och efter instruktionen samt Gophers P1-tillstånd.

| F:s RAM-X | Utfall | Tredje RESP1, CL före→efter | F:s GRP1, CL före→efter |
|---:|---|---|---|
| 64 | FAIL 12 saknade/18 extra, diff i SF | 34→43 | 43→52 |
| 67 | PASS 0/0 | 34→46 | 46→55 |
| 73 | PASS 0/0 | 43→52 | 52→64 |
| 76 | PASS 0/0 | 46→55 | 55→67 |
| 82 | FAIL 18/18. F-masken återges exakt vid X84 | 49→61 | 61→70 |

CL-intervallen anger instruktionens början och slut. Själva registerskrivningen syns i TIA-spåret. Vid X64 sker F:s grafikskrivning tidigare än i X67-kontrollen, samtidigt som strålen fortfarande går över SF:s X46–53. Y76-diffen visar att SF:s vita pixelmönster ändras medan F når sin avsedda position. Vid X82 börjar den helvita F-raden på observerat X84, och helbildens 18/18-diff blir 0/0 om oraklet jämför mot X84. Detta skiljer CPU-skrivning och synliga pixlar åt. Exakt internt TIA START-ögonblick och intern latch-orsak är **INCONCLUSIVE**.

## RAM-styrda yttre slots, omordningar och vertikal spridning

- **`outer.bin`, höger M:** X = `[130|133|136,19,73,100,46]` vid historiskt Y. De tre flyttade lägena och X127 gav vardera 8/8 PASS. Gopher loggade högra RESP1-instruktionen vid CL100→109, 103→112 och 106→115 för de tre nya lägena. De övriga fyra RESP1-intervallen var identiska i de tre körningarna.
- **`outer.bin`, kombinationer:** 24/24 PASS i sex lägen med tredjeslotten på X67 eller X76, höger M på ett ändrat X och tre RAM-omordningar där originalmaskerna följer sina respektive individer. X67/73/76 från ITER3 är återkontrollerade. X64 och X82 reproducerar tidigare fysiska FAIL.
- **`mixed.bin`, fjärde sorterade platsen:** X97 och X103 gav PASS med X127 kvar i femteslotten och övriga koordinater fasta. `[133,19,76,103,46]` klarade tre samtidiga X-ändringar från historiska scenen. Sex aktiva RAM-kombinationer gav 24/24 PASS.
- **`wide.bin`, Y:** X=`[133,19,76,100,46]`, Y=`[74,68,75,71,71]` gav PASS, en spridning på sju rader. Två tidigare flyttade band och de nya X-omordningarna klarades också. Y=`[74,68,83,71,76]` ger **REJECTED** eftersom cachen inte täcker spridningen. Det täta same-Y-provet och flyttproven för första/andra sorterade platsen ger också **REJECTED** före raster.
- **Äldre 20 fixturer på `outer.bin`:** historisk separerad PASS i 3/3 bilder, 19/20 fixturer REJECTED före raster, 60/60 ×262. Den faktiska TIA-renderbarheten för avvisade fixturer är **NOT_RUN**. Se individuell X/Y, PEEK/VALID och fältet `status` i matrisen och råloggarna.

Samtliga åtta tidigare positiva kontrollfixturer från ITER2 och ITER3 gav 32/32 PASS vid återkörning på `mixed.bin`, inklusive båda äldre fjärde-X-omordningarna och de två tidigare Y-banden. Totalt hade de färdiga Gopher-körningarna 2168/2168 bildrutor med 262 scanlines efter uppvärmning.

Över de tre utökade ROM:arna kördes tre separata serier om **600/600 PASS**. Varje serie är sammanhängande FR21–620 med sex RAM-sceningångar, exakt 262 scanlines, 136 korrekta NPC-pixlar, 32 P0-pixlar, 25 M0-pixlar och 3047 PF-pixlar. Stock Stella 6.7.1 visar X133 tillsammans med tredje X76 och stock 7.0 visar X136 tillsammans med tredje X67. Båda gav 12/12 pixel- och RGB-exakta bilder från bootvarianter som bara ändrar initiala X-byte. Stella live-POKE och egen radlängdsmätning är **NOT_RUN**.

### Hur kärnan väljer läge

Sorteringen och maskpekarnas X/Y-underlag kommer från RIOT. Efter sortering beräknar den RAM-lästa högra X-positionen bankindex i `outer` och `wide`; `mixed` väljer bank med fjärde och femte sorterade X. F6-bankbytet sker under VBLANK via `$FFF6,X`. Samma numeriska tredje X väljer sedan en radkedja inom den banken. Registerschemana är genererade i förväg för begränsade stödda fasalternativ. Varken hela scener, individordning eller maskrader är förkompilerade som koordinatfixerade helbilder. Första/andra sorterade X är fortfarande låsta till 19/46. Den bredare cachen kombinerar två jämförelser per VBLANK-rad efter initieringen, vilket frigör plats för ytterligare sex maskrader.

Det första F6-försöket gav **263 scanlines i 32/32 bildrutor**. Den längre initieringsvägen i VBLANK låg över radbudgeten; rak initiering av sorteringsindex återställde 262. Den negativa ROM:en, källan, bilderna och loggarna finns under `first-263-roms/` i råarkivet.

### Budget och modell

| ROM | RIOT inkl. stack | Reviderade paket | Max CPU-cykler per aktiv rad |
|---|---:|---:|---:|
| `outer.bin` | 92/128 | 220 | 76 |
| `mixed.bin` | 93/128 | 209 | 76 |
| `wide.bin` | 122/128 | 204 | 76 |

Debuggeravläsning för alla tre vid två stackpushar gav SP=$FD från $FF. Ingen av de uppmätta RIOT-allokeringarna överlappar stacken. DASM-binäraudit kontrollerar sidgränser, exekverade opkoder, TIA-skrivpositioner och sista hoppet i varje genererat radpaket. Gopher verifierade att på varandra följande spårade aktiva rader börjar vid CL−68. Z3-modellen gav 34/35 SAT, inklusive tidigare fysiskt negativa lägen. UNSAT för `[19,46,82,97,127]` gäller den valda modellen för skrivfönster och registerlivslängd. Fysisk TIA-renderbarhet för den kombinationen är **NOT_RUN**. Ingen alternativ HMOVE-/VDEL-metod behövdes för att uppnå den yttre X-milstolpen.

## Bygg och evidens

- `outer.bin` SHA-256 `1507414d5629dae634f73c4cef2353b6432060a244cf40e84cdf67599ab79912`
- `mixed.bin` SHA-256 `db576ddc3f50550de438e97d42100d74ff9140c27e5a42d1d08d99f12153730d`
- `wide.bin` SHA-256 `0c60bb6d53911e6c46789bed84c2cd6149252f95e440d757a3cccd3875cb2ec9`

DASM 2.20.14.1 byggde fyra 4 KiB-banker per standard-F6-ROM. Gopher2600 v0.57.2 körde RAM-matris, PTY/P1-bussmätning och tre obrutna långkörningar. Stock Stella 6.7.1/7.0 körde pixelkontrollen. Python/Pillow jämförde per mask och RGB mot den frysta referensen. Z3 4.15.4 körde instruktionsmodellen. Versioner, officiella byggreferenser från G5AR/G5BB och verktygens SHA-256 syns i `evidence/brief/tools.txt` och tidigare leveranser. [G5AR](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [G5BB](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

`SHA256SUMS` omfattar levererade källor, F6-ROM:ar, originalbilder, direktläsbara pixel-/buss-/RAM-/cykelloggar och råarkivet. `evidence/brief/matrix.tsv` innehåller samtliga X/Y-fixturer. Råarkivet innehåller ursprungliga PTY-byte och emulatorbilder. Kör från `experiments/g5be_iter4`.

```bash
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
out=$(mktemp -d)
python -m venv "$out/z3"
"$out/z3/bin/pip" install -r requirements.txt
"$out/z3/bin/python" schedule.py > "$out/model.jsonl"
cmp solver.jsonl "$out/model.jsonl"
python build.py
python build.py --name mixed --mixed
python build.py --name wide --rows 17
python audit.py | cmp - evidence/brief/cycles.jsonl
ref=evidence/reference
python beam.py "$ref/all-p1.bin" --frozen > "$out/frozen-beam.jsonl"
python beam.py roms/outer.bin > "$out/outer-beam.jsonl"
python beam.py roms/wide.bin --stack-only > "$out/wide-stack.jsonl"
python beam.py roms/mixed.bin --stack-only > "$out/mixed-stack.jsonl"
python ram.py outer "$out/outer-beam.jsonl"
python ram.py wide "$out/wide-stack.jsonl"
python ram.py mixed "$out/mixed-stack.jsonl"
for spec in outer:third outer:outer outer:combined outer:extended outer:legacy outer:soak \
            mixed:extended mixed:mixed mixed:prior mixed:mixed-soak \
            wide:extended wide:combined wide:wide-soak; do
    rom=${spec%:*}
    group=${spec#*:}
    tag="$rom-$group"
    python replay.py "roms/$rom.bin" "$out/$tag" --group "$group" > "$out/$tag.jsonl"
    python score.py "$out/$tag" "$ref/frozen-gopher-y76.png" --ref-height 214 \
        --log "$out/$tag.jsonl" > "$out/$tag-score.jsonl"
done
python build.py --name outer-boot133 --right 133 --third 76
python build.py --name outer-boot136 --right 136 --third 67
bash capture_stella.sh roms/outer-boot133.bin "$out/stella671" 558
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash capture_stella.sh roms/outer-boot136.bin "$out/stella70" 542
python score.py "$out/stella671/images" "$ref/stella-671-frozen.png" --boot-x 76 --right-x 133
python score.py "$out/stella70/images" "$ref/stella-70-frozen.png" --boot-x 67 --right-x 136
```

**Till MAIN X:** Nästa avgränsade teknikfråga är hur de första två sorterade RESP1-slotarna kan få fler giltiga X-faser och den vertikala cachen täcka större spridning. Generell fri X/Y är **FAIL som acceptanskrav**. Oberoende Verification II är **NOT_RUN**. `G5_FORMAL_OPEN` kvarstår.
