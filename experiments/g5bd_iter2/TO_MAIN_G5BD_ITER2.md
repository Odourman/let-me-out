# TO_MAIN_G5BD_ITER2 · LM-D36 · ROM DEVELOPMENT IV → MAIN IX

**`G5BD_ITER2_LOCAL_TIA_CONFLICT_OBSERVED` · 18 november 2026 · DEVELOPER_OBSERVED**

Den historiska omordningen är fortsatt **FAIL**. En kontroll som enbart ersätter c37-skrivningen tar bort **alla 20 extra pixlar vid SF** och återställer SF:s fyra saknade pixlar, men F förlorar 20 pixlar. Ett riktat GRP1-new → GRP0 → GRP1-old-prov återger **SF, F och höger M pixelrätt samtidigt** och utelämnar öppet de övriga två maskerna. Den frysta fas-ROM:en är fortfarande bästa femslotsreferens med 5 saknade/20 extra. **G5_FORMAL_OPEN kvarstår.**

## Avgörande mätningar i historisk omordning

X **127/19/73/100/46**, Y **73/72/73/71/72**. Endast XP/YP och sortordningen bestämmer planens maskadresser och strobtider. Proverna använder samma M, M, F, SM, SF-maskfil, bytejämförd med originalet. Gopher POKE/PEEK kvitterade samtliga tio byte.

| ROM / åtgärd | Unika pixlar per NPC i ID-ordning M/M/F/SM/SF, av 28/28/38/20/22 | Saknade/extra | Cykler per aktiv rad |
|---|---|---:|---:|
| Fryst `phaseprobe`, SHA `16301cd20952d1a101c4ea876d6a63a0ae147399f4342d386454ebf230c631da` | 27/28/38/20/18 | 5/20 | 76 |
| `mute37`, ersätt en STX med lika lång BIT-zp | 27/28/18/20/22 | 21/4 | 76 |
| `tailindex`, flytta INY till radslut och håll F i X över radgränsen | 27/12/38/20/22 | 17/10 | 76 |
| `earlyright`, läs höger M före strob och skriv tidigare | 28/12/20/20/22 | 34/10 | 76 |
| `resetminus`, flytta bara SF:s RESP från c31 till c30 | 27/28/38/20/8 | 15/29 | 76 |
| `shadow`, riktade GRP0-överföringar och tre av fem strobar | 28/0/38/0/22 | 48/0 | 66 inklusive WSYNC |

Samtliga huvudrader är **FAIL** för hela scenen. Varje Gopher-variant gav tre identiska kortprover vid 262 scanlines. Gul P0 32 pixlar, aktivt M0 25 och båda PF-väggar (3047 bruna pixlar) mättes i huvudscenen. Femslotsvarianterna har fortfarande synliga unika pixlar för samtliga fem i varje kortprov.

### SF→F, P1 reset och höger M

- **Isolerad c37-effekt.** `mute37` använder samma strob- och cykelschema som fasreferensen. Endast instruktionen STX GRP1 ersattes av BIT på ett arbetsvärde i nollsidans RAM. I X46–53 gick extra pixlar från **20→0** och SF:s unika bitar från **18→22**. De fyra kvarvarande extra pixlarna var utanför SF-fönstret. Den klockade ursprungsinstruktionen är `$D1→$D3`. Stella 7.0 kvitterade faktisk `trapWrite $1c` vid `$D3`. Radloggen har förväntade/observerade maskbyte och exakta X för varje fel.
- **Reset-fas.** `resetminus` ändrar SF-strob c31→c30 och använder en längre STA-adressering så GRP1-skrivsluten behåller sina ursprungliga cykler. Gopher `PLAYER 1` på SL112 rapporterade andra kopian vid px7 på c37 i motprovet. Den frysta var vid en annan ScanCounter-fas i samma klockpunkt. Bilden blev sämre, 15/29 i stället för 5/20. En förskjuten strob räknas som negativt prov eftersom önskade RAM-koordinater är oförändrade. **Intern TIA START är NOT_DETERMINABLE**. CPU-busspunkter, emulatorns ScanCounter-ögonblick och faktiskt synlig PNG-pixel hålls isär.
- **Höger M, raster-Y76.** Referensens armrad är `FF`, synligt `7F`, med endast X127 saknad där. `earlyright` flyttar dess GRP1 från **c65→c61**, med RESP1 kvar på c58. Masken blir **FF, 28/28**. Förladdningen ändrar andra GRP1-faser och ger större fel i vänster M och F. `tailindex` skjuter F:s skrivning till c43 och återger hela SF och F, men den tidigare SF-uppdateringen skadar vänster M. Inget av proven räcker för hela femmaskraden.
- **Riktad VDEL.** `shadow` sätter VDELP1 på c14, skriver SF-new c21, överför det genom spelarens eget byte till GRP0 c24, buffrar F-new c34 och överför det genom GRP0 c43. VDEL släcks c48 och höger M skrivs c55 före sin c58-strob. Gopher registrerade de riktade skrivningarna och samtliga tre maskfönster är bitexakta utan extra pixlar. P0:s faktiska maskbyte hölls i X för triggern. Vid den kontrollerade scenen finns 10 fria cykler i 76-budgeten, otillräckligt för att lägga in två ordinära oberoende maskslotar i denna plan. Det är en lokal deadline, utan generell TIA-omöjlighet. Metoden lånar GRP0-triggern och registerförladdningen från 48-pixeltekniken, utan att använda en fast 48-pixelsbild. Fryst blanket-VDEL 64/68 är oförändrad. [48-pixelkernel](https://bumbershootsoft.wordpress.com/2018/09/24/atari-2600-a-48px-kernel/) · [TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php)

## Regression och budget

Alla fem nya ROM:ar återkörde den historiska matrisen, **8/8 gamla positiva G5BB-familjer**, **12/12 gamla seedade positiva**, samtliga tolv nya G5BD-omordningar (3/12 PASS per variant), täta seedfall (0/4) och X-resterna. De historiska fallen separated/close3/close1/mixed-same-X förblev respektive **0/0, 76/28, 37/28, 42/0**. X19 PASS, X20 och X21 vardera 13/13. Individuell positionsmatris 48/50. Alla resultat per koordinat, inklusive `USED` och unik synlighet, finns i kortmatriserna i `evidence/brief`.

`tailindex` gav **600/600 exakta bilder på de åtta positiva familjerna**, 608 sammanhängande Gopher-avläsningar inklusive 8 övergångar, samtliga 262 scanlines och max 0 helt frånvarande NPC i detta positiva prov. Det finns ingen 600-bilders PASS för den historiska omordningen. Stock Stella 6.7.1/7.0 bekräftade kortmatrisen, 12 bilder per serie. En bild i första 6.7.1-serien för `mute37` gav 46/46 (`INCONCLUSIVE` avvikelse i GUI/Select-serie). En separat omkörning gav 12/12 med det stabila 21/4-resultatet. Bägge serierna är sparade.

DASM 2.20.14.1 byggde fem nya 16 KiB F6-ROM:ar med fyra byteidentiska banker. Faktisk 6507-audit fann **50–56 byte** emitterad kod under 64-byte-reserven, och ingen indexerad sidkorsning vid Y0–23. De friroterande schemana tar 76 inklusive den tagna BNE, med en initial WSYNC före loopen. RIOT-reservation **128 B** = 1 bildräknare +10 X/Y +5 sortindex +16 arbetsbyte +24 cache/komposit +64 emitterad kod +8 stack. Max 6 stackbyte i de nya emitterarvägarnas tre JSR-nivåer. Full originalmask ligger fortsatt inom bandets Y64–79.

**Stella 7.0** mätte fryst `$BA→$EC` **73×3** (76 inklusive BNE), respektive `shadow $BA→$B8` **63×3** (66 inklusive WSYNC). Rå `trapWrite $11/$1c`, timer och reset finns direkt i leveransen. **Gopher2600 v0.57.2** gav 2 success/0 fail på de positiva 30-frame bootbaslinjerna med oförändrad databashash. Live POKE/pixeldata är separat. Verktygsbinärerna är hashade i `tool-versions.txt`. Inga nya emulatorpaket installerades. Fysisk maskin, helt fri X/Y och R2/S05 **NOT_RUN**.

## Reproduktion

Från `experiments/g5bd_iter2` med G5AR ENV-01 och stock Stella 7.0 sidobinär från G5BB.

```bash
set -e
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for f in bin sym; do
  git show "fa0b6c869d16d2aaf190c452e0d9aadc159af05a:experiments/g5bd/roms/phaseprobe.$f" > "roms/baseline.$f"
done
for m in baseline mute37 tailindex earlyright resetminus shadow; do
  python runtime_capture.py "$m" "$out/$m-png" --fixture historic-reorder > "$out/$m.jsonl"
  python measure.py "$m" "$out/$m.jsonl" "$out/$m-png" "$out/$m-pixels.jsonl"
  python row_diff.py "$out/$m-pixels.jsonl" "$out/$m-png" > "$out/row-$m.jsonl"
  python trace_runtime.py "$m" historic-reorder > "$out/trace-$m.jsonl"
done
for m in mute37 tailindex earlyright resetminus shadow; do
  for series in cases seeded reorders; do
    flags=()
    if [[ $series != cases ]]; then flags+=("--$series"); fi
    python runtime_capture.py "$m" "$out/$m-$series-png" "${flags[@]}" > "$out/$m-$series.jsonl"
    python measure.py "$m" "$out/$m-$series.jsonl" "$out/$m-$series-png" "$out/$m-$series-pixels.jsonl"
  done
done
python runtime_capture.py tailindex "$out/soak-png" --soak > "$out/soak.jsonl"
python measure.py tailindex "$out/soak.jsonl" "$out/soak-png" "$out/soak-pixels.jsonl"
python audit_kernel.py "$out"/trace-*.jsonl
bash -x native_regress.sh roms/baseline.bin roms/tailindex.bin "$out/native"
stella7=/workspace/work/g5bb/stella7/usr/bin/stella
bash stella_debug.sh roms/baseline.bin "$out/stella7-baseline" 331 "$stella7" '$ec' '$d1'
bash stella_debug.sh roms/shadow.bin "$out/stella7-shadow" 332 "$stella7"
for m in baseline mute37 tailindex earlyright resetminus shadow; do
  timeout 25 bash capture_stella.sh "roms/$m.bin" "$out/stella-671-$m-select" 333 select
  STELLA_BIN="$stella7" timeout 25 bash capture_stella.sh "roms/$m.bin" "$out/stella-70-$m-select" 334 select
done
python measure_stella.py "$out"/stella-*select > "$out/stella-pixels.jsonl"
```

Utvecklarens egenkontroll lämnas till MAIN IX. Ingen gameplay-etapp påbörjades.
