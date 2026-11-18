# TO_MAIN_G5BD · LM-D36 · ROM DEVELOPMENT IV → MAIN IX

**`G5BD_PARTIAL_FIVE_SLOT_PROGRESS` · 18 november 2026 · DEVELOPER_OBSERVED**

I den historiska omordningen återgav `phaseprobe.bin` **F:s alla 38 unika pixlar samtidigt med 27 av höger M:s 28**. Alla fem fiender hade synliga unika pixlar i samma bild. Scenen är fortfarande **FAIL**. Den saknade en M-pixel och fyra SF-pixlar och hade 20 extra vita pixlar runt SF. Resultatet upprepades på Gopher2600 och stock Stella 6.7.1/7.0. **G5_FORMAL_OPEN kvarstår.**

## Det faktiska femslotsprovet

Den frysta G5BC-hybriden kördes först från commit `1365025ff58ea36dce432c0213ce532c14fbf817` och hash `0f1c83bab54f4a1089461f7ac721d8c6e46f59f3a984938939a223af5083cd14`. Den aktuella byggkatalogens `hybrid.bin` är byte-identisk. I X **127/19/73/100/46**, Y **73/72/73/71/72**, sorterade ID **1/4/2/3/0**, visade kontrollen åter de fyra RESP1-skrivningarna c22/31/49/58 och `USED=1`. Efter SF:s GRP1-slut c34 återstår sex cykler till F:s c40. En indexerad maskläsning och strob kräver sju. G5BC:s cacheprobe löste den lokala deadlinen genom att stryka höger M.

G5BD:s nya väg förladdar nästa rads första mask till X över radgränsen. Den skriver två GRP1-värden före respektive RESP1, och läser höger M efter dess strob. En initial WSYNC låser bandet. Därefter går den återkommande loopen på exakt 76 cykler utan ny WSYNC. 6507-koden emitterar instruktioner och pad från sorterade RAM-X och hämtar varje maskrad från RAM-Y. Admissionsvillkoren är tidsgränser och minsta strobavstånd **8/9/8/8 cykler**, första strob tidigast c22, sista senast c58, och ingen aktiv G5BC-komposit. Varken en specifik X-vektor eller NPC-identitet används för denna väg. G5BC:s latchdelning och inkompatibla geometrifall går via tidigare vägar.

| Historisk omordning | Synliga F / 38 | Synliga höger M / 28 | Saknade / extra vita | Utfall |
|---|---:|---:|---:|---|
| Fryst G5BC hybrid | 0 | 28 | 38/0 | FAIL |
| Fryst G5BC cacheprobe, mottaget resultat | 38 | 0 | 28/0 | FAIL |
| G5BD `phaseprobe` | **38** | **27** | **5/20** | FAIL, fem synliga |
| G5BD `phasevdel`, fördröjd P1-latch bara under provvägen | 18 | 14 | 64/68 | FAIL |

`phaseprobe` loggade RESP1 c22/31/40/49/58. Gopher rapporterade GRP1 c15/34/52/65. Den extra **STX GRP1** vid c37 är verifierad genom maskinkoden, Gophers klockade steg från `$D1` till `$D3` och Stellas faktiska `trapWrite $1c` efter samma instruktion. Gophers TRACE skrev inget separat registermeddelande i det steget. SF-felen låg vid X46–53, där F-data blev synliga i den tidigare kopian. Höger M förlorade den vänstra pixeln på den breda raden. Den sena GRP1-skrivningen c65 sammanfaller med den avvikelsen. VDEL-testet förvärrade båda felen och behölls som separat negativ ROM. Intern TIA START och den fullständiga serializer-/latchkedjan är **NOT_DETERMINABLE** från dessa skrivspår.

## Testmatris

| Historiskt G5AZ-fall | G5BD phaseprobe saknade/extra | Klass |
|---|---:|---|
| Separerat X19/46/73/100/127 | 0/0 | PASS |
| Omordnat X127/19/73/100/46 | 5/20 | FAIL |
| Close3 X73/76/79/82/85 | 76/28 | FAIL |
| Close1 X73/74/75/76/77 | 37/28 | FAIL |
| Mixed same-X X73/73/19/100/46 | 42/0 | FAIL |

- **Tidigare positiva** Samtliga åtta G5BB-familjer och tolv G5BC-seedlägen förblev pixelrätta. De tolv seedlägena gav 36/36. Seedade täta stresslägen gav fortsatt 0/12. Ankarproven för X19/20/21 gav 0/0, 13/13 och 13/13 (saknade/extra). Individuella positionskontroller gav fortsatt 48/50.
- **Tolv nya omordningar**, seed `0x650736`, gav 9/36 pixelrätta bilder i tre lägen (03, 07, 11, med 30-pixelspacing). Övriga nio lägen gav pixelavvikelser. Sju av de nio negativa lägena strobade alla fem men hade kopie-/bitmapfel. Två hade en planerad miss. Exakta X/Y, unika fel per NPC och varje fall finns i `evidence/brief/reorders-coordinates.jsonl` och `reorders.txt`. En planerat emitterad strob räknas aldrig som pixel-PASS.
- **Långtest A** 600/600 exakta Gopher-PNG i de åtta positiva familjerna. 608 sammanhängande 262-scanlineavläsningar inklusive åtta övergångar.
- **Långtest B** 600 poängsatta bilder i fem familjer (120 vardera). Historisk omordning gav 0/120 exakta och 5/20 i varje bild. Historiskt separerat, tvåpar, seed-04 och seed-06 gav 480/480 exakta tillsammans. 605 sammanhängande avläsningar, alla 262. Alla fem NPC hade unika synliga pixlar i samtliga 600 poängsatta bilder, med max 0 helt osynliga. I omordningen sågs F 38/38 och M 27/28 i varje analyserad bild.
- **P0/M0/PF** I huvudsakliga omordningen mättes 32 gula P0-pixlar, 25 gula M0-pixlar, 3047 bruna PF-pixlar och båda väggkanterna. Samma originalmaskfil jämfördes byte för byte mot `design/NPC_REFERENCE_8x9_masks.json`. POKE/PEEK kontrollerade alla tio värden före och efter varje scen. Pixeloraklet räknade fysisk union och unika maskpixlar.
- **Stock Stella** 12/12 stickprov per version för `phaseprobe` återgav samma FAIL 5/20, och `phasevdel` gav 64/68 i 12/12 per version. Stellas bevis omfattar dessa stickprov. R2/S05, fysisk maskin och hel fri X/Y är **NOT_RUN**.

## Cykler, minne och verktyg

DASM 2.20.14.1 byggde två nya körbara NTSC/F6-varianter, fyra byteidentiska 4 KiB-banker per ROM. Kodområdet före tabeller slutade vid `$F718` (1816 byte) i båda. Faktisk dump av RIOT-koden visar **55/64 kodbyte** och ingen indexerad sidkorsning vid Y0–23. Auditens max var **76 cykler** inklusive den tagna loopbranchen (fasprovet) eller inklusive WSYNC (G5BC:s positiva femslotsväg). Fasprovets initiala WSYNC ingår bara före bandloopen. RIOT-budget **128 B** = 1 bildräknare + 10 X/Y + 5 sortindex + 16 arbetsbyte + 24 delad cache/komposit + 64 kod + 8 stack. Längsta nästling tre JSR, 6 stackbyte. I fasprovet återanvänds den tomma kompositcachens arbetsbyte. Provade band och strobintervall innebär ingen generell helskärmslösning.

- **Stella 7.0** befintlig isolerad version från G5BB, här faktiskt exekverad. På omordningen mätte `timer $ba $b8` tre gånger 66 cykler för G5BC-beteendet (69 inklusive WSYNC). `timer $ba $ec` mätte tre gånger 73 för fasloopen fram till branchens opcode (76 efter tagen BNE). `trapWrite $11`, `trapWrite $1c`, `listTimers` och `resetTimers` finns i rå session. Stock 6.7.1 reproducerade fällorna men saknade timerkommandon. [Stellas officiella handbok](https://stella-emu.github.io/docs/debugger.html)
- **Gopher2600 v0.57.2** revision `2af86eb725739adbf3d9d45cea2ed69eea57da2a`. Regression Database gav 2 success/0 fail för två positiva 30-frame bootbaslinjer, oförändrad databashash. Separat live POKE/pixelregression mätte resultatet ovan. Oförändrade kommandon/resultat och verktygshashar finns direkt under `evidence/brief`. [Gopher Regression Database](https://github.com/JetSetIlly/Gopher2600-Docs/wiki/Regression-Database)
- **Python 3.12.14 och Pillow 13.0.0** exekverade maskoraklet och 6507-auditen. Gopher-spåren visar CPU-skrivslut och originalbilderna synliga pixlar. VDEL-förklaringar utöver observerad skillnad i bilderna är **SOURCE_ONLY**.

## Bygg och omkörning

Från `experiments/g5bd` med G5AR ENV-01 och Stella 7.0 sidobinären från G5BB. Inga nya paket installerades.

```bash
set -e
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for f in bin sym; do
    git show "1365025ff58ea36dce432c0213ce532c14fbf817:experiments/g5bc/roms/hybrid.$f" > "roms/baseline.$f"
done
for mode in hybrid phaseprobe phasevdel; do
    python runtime_capture.py "$mode" "$out/$mode-png" > "$out/$mode.jsonl"
    python measure.py "$mode" "$out/$mode.jsonl" "$out/$mode-png" "$out/$mode-pixels.jsonl"
    python trace_runtime.py "$mode" historic-reorder > "$out/trace-$mode.jsonl"
done
for series in seeded reorders soak stress; do
    flags=("--$series")
    if [[ $series == stress ]]; then flags+=(--soak); fi
    python runtime_capture.py phaseprobe "$out/$series-png" "${flags[@]}" > "$out/$series.jsonl"
    python measure.py phaseprobe "$out/$series.jsonl" "$out/$series-png" "$out/$series-pixels.jsonl"
done
python audit_kernel.py "$out"/trace-*.jsonl
bash -x native_regress.sh roms/baseline.bin roms/phaseprobe.bin "$out/native"
stella7=/workspace/work/g5bb/stella7/usr/bin/stella
bash stella_debug.sh roms/hybrid.bin "$out/stella7-baseline" 291 "$stella7"
bash stella_debug.sh roms/phaseprobe.bin "$out/stella7-phase" 292 "$stella7" '$ec' '$d1'
bash stella_debug.sh roms/phaseprobe.bin "$out/stella67-phase" 293 /workspace/.g5ar-env01/bin/stella '$ec' '$d1'
for mode in phaseprobe phasevdel; do
    timeout 25 bash capture_stella.sh "roms/$mode.bin" "$out/stella-671-$mode-select" 294 select
    STELLA_BIN="$stella7" timeout 25 bash capture_stella.sh "roms/$mode.bin" "$out/stella-70-$mode-select" 295 select
done
python measure_stella.py "$out"/stella-*select > "$out/stella-pixels.jsonl"
```

Specialistleveransen väntar på MAIN IX:s mottagningsgranskning. Ingen implementeringsetapp påbörjades.
