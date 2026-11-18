# TO_MAIN_G5BC · LM-D35 · ROM DEVELOPMENT IV → MAIN IX

**`G5BC_PARTIAL_GENERALIZATION_PROGRESS` · 18 november 2026 · DEVELOPER_OBSERVED**

`hybrid.bin` ersätter G5BB:s jämförelse mot en exakt X-vektor med en runtime-plan byggd från sorterade RAM-koordinater och cykeldeadlines. Alla åtta positiva G5BB-scener förblev pixelrätta. **Tolv seedade separerade lägen klarade pixelkontrollen i samma binär. Fem av tolv fallerade i den frysta G5BB-ROM:en.** Den historiska omordningen är fortfarande FAIL. En separat tvåcache-ROM återgav hela den saknade F-masken, men offrade höger M. G5_FORMAL_OPEN kvarstår.

## F-blockeraren och två provade rasterplaner

Först kördes fryst G5BB `hybrid.bin` SHA-256 `7c77fcba29b460547f35c4667d637f1f0ff14e94be3b93290d1d4a8b85cacccd`. Vid X 127/19/73/100/46 och Y 73/72/73/71/72 var sortordningen 1/4/2/3/0. P1 skrev RESP1 på c22/31/49/58 och GRP1 c25/34/52/61, `USED=1`. Vid F:s c40 har den föregående GRP1-skrivningen slutat c34. Indexerad radläsning plus strob kräver sju cykler, medan sex återstår. F:s RESP1/GRP1 saknas därför i den genererade koden. Både Gopher och stock Stella ser 38 saknade F-pixlar.

- **`hybrid.bin`** behåller G5BB:s täta komposit och inline-OR. När de två vänstra instanserna är M med lika Y kan P1 återanvända sin skrivna mask vid andra stroben. Planen härleder alla fem måltider från RAM-värden, lägger in NOP/BIT eller lång strob, förladdar fjärde masken i X och strömmar femte maskens nästa radbyte genom nollsidans `$A0`. Ingen X-fixture väljer rasterkod. Boot/Select finns kvar för reproducerbar GUI-stimulering och ändrar bara de vanliga RAM-koordinaterna. Historiskt separerat fick RESP1 c22/31/40/49/58 och GRP1 c25/43/52/61. Den andra M-masken återanvände alltså c25-skrivningen. I historisk omordning kan vald plan inte dela den latchen, och F förblir borta.
- **`cacheprobe.bin`** prövar om F:s deadline kan mötas med kortare maskläsning. De två mellersta radvärdena laddas från `$A0` och `$A6` på tre cykler i stället för fyra. Refill av två byte tar 14 cykler efter sista GRP1. ROM:en reserverar bara fyra slots för att hålla raden kort nog. RESP1 blev c22/31/40/49, GRP1 c25/34/43/52, **74 cykler inklusive WSYNC**. Samtliga 38 F-pixlar återkom. Höger M:s 28 unika pixlar uteblev och inga spökpixlar tillkom. Stock Stella bekräftade. Kostnaden för att använda samma refill efter femte historiska skrivningen c61 skulle ge c61+14+8=83 cykler. Detta falsifierar den direkta förlängningen av just denna cacheplan. `cacheprobe` är ett negativt experiment.

## Pixel- och synlighetsmatris

| Historisk X-vektor | G5AZ saknade/extra | G5BB | G5BC hybrid |
|---|---:|---:|---:|
| 19/46/73/100/127, same-Y | 48/0 | 0/0 | **0/0 PASS** |
| 127/19/73/100/46, mixed-Y | 42/0 | 38/0 | **38/0 FAIL** |
| 73/76/79/82/85, close3 | 76/28 | 76/28 | **76/28 FAIL** |
| 73/74/75/76/77, close1 | 37/28 | 37/28 | **37/28 FAIL** |
| 73/73/19/100/46, same-X | 42/0 | 42/0 | **42/0 FAIL** |

Tre poängsatta bilder per kortfall, 262 scanlines i samtliga. Python jämförde råbilder med unionen av de oförändrade originella M/M/F/SM/SF-maskerna och rapporterade varje NPC:s unika pixlar. RAM POKE/PEEK verifierade alla tio koordinatbyte före/efter scenbyte. Individuella ändringar gav 48/50 pixelrätta bilder, samma tidigare miss vid NPC0 X55→52. Gul P0 hade 32 pixlar, det aktiva M0-skottet 25, och de båda PF-väggkanterna fanns med.

Seed `0x650735` gav 12 separerade fixturer, fyra verkligt täta och tre test av ett individuellt ankare. Testerna kördes i samma oförändrade binär. Seed 00–05 varierade sortordning för högerdelen och RAM-Y medan vänstra två M kunde dela en rad. Seed 06–11 permuterade alla identiteter med individuella Y.

| Seedad klass | Hybrid, 3 bilder per läge | Begränsning |
|---|---:|---|
| 00–05, RAM-räknad delad M-latch | **18/18 PASS**, fryst ROM 3/18 | Uppmätt X 19–127 i 3 px-steg, Y67–76, luckor ned till 24 px. |
| 06–11, separerade omordningar | **18/18 PASS**, fryst ROM 18/18 | Uppmätt X19–145, Y67–76, luckor 30–33 px. |
| Dense 0–3, luckor 1–6 px | **0/12 FAIL** | Saknade/extra 76/36, 98/39, 75/25, 84/45. |
| Individuellt ankare X19/20/21 | **3/9**, X19 PASS | X20 och X21 gav vardera 13/13. Off-grid-X kvarstår. |

Långkörning A gav **600/600 pixelrätta råbilder**, 608 konsekutiva TV FRAME-avläsningar vid 262 inklusive åtta övergångar. De åtta G5BB-familjerna var historiskt separerat och två slack-fixturer (100 vardera), plus G5BA:s nära 2 px, nära 1 px, reorder, same-X och två par (60 vardera). Långkörning B gav **600/600** över seed 00–11 (50 per läge) med 612 konsekutiva avläsningar vid 262 inklusive tolv övergångar. Samtliga fem NPC hade unika synliga pixlar i alla 1 200 poängsatta bilder, max 0 helt frånvarande i dessa positiva fixturer. Historisk omordning gav F 0/3 synlig och cacheprovet höger M 0/3.

## Budget och emulatorjämförelse

- **76 CPU-cykler max observerat i audit**, inklusive WSYNC, i historiskt separerat och seed-00. Seed-06 tog 74, normal historisk reorder 69, cacheprobe reorder 74, dense-0 48 och tvåparsscenen 68. Audit kontrollerade riktiga RIOT-byte, indexerad sidkorsning vid Y=0–23 och branch/jump tillbaka till radstart. TRACE gav 24 aktiva rader per tillstånd och bekräftade RESP1/GRP1 på CPU-skrivslut. Intern TIA START **INCONCLUSIVE**.
- RIOT `$80–FF` reserverar 1 bildräknare, 10 X/Y, 5 sortindex, 16 arbetsbyte, 24 delad komposit/cache, 64 kod och 8 stack = **128 B**. Största uppmätta genererade kod var 55 B. Tre nästlade JSR använder 6 stackbyte. Initiering av tvåcachevägen gör en separat push/pop. F6 innehåller fyra byteidentiska 4 KiB-banker (16 KiB per ROM). Hybridens kod/markörer upptar högst $05D8 och provets $06D8 före maskregioner, cykeltabell och vektorer.
- Källan tillåter den delade latchvägen inom c22–58 med tidströsklar för steg om 8/8/8/9 cykler. Offsetdomänen är på rastergittret 19…127, övriga vägar upp till 151. Full 8×9 inom bandet kräver Y64–79. Resultat här verifierar de listade geometrierna, inklusive 24 px mellan vissa strobpar. Exakta positiva kompositer är separata G5BA-fall inom bandet. Ingen generell minsta X-lucka för godtyckliga maskkombinationer har fastställts.
- **Stella 6.7.1** 12/12 exakta positiva bootbilder per ROM. Select reproducerade 38/0 för hybrid och 28/0 för cacheprobe, 12 bilder vardera. Stock Stella **7.0** reproducerade hybridens 38/0 i tolv bilder. R2/S05, fysisk Atari och fri heltals-X över hela spelplanen **NOT_RUN**.

## Reproduktion och direkta loggar

[TOOL_USAGE.md](TOOL_USAGE.md) har binärhashar, kommandon och små råloggar. Arbetsordern är Issue #28. Fryst utgångspunkt är `3bf873cc1473eff1f9e7474893a8ea2d02aacc6f`.

```bash
set -e
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for f in bin sym; do
  git show "3bf873cc1473eff1f9e7474893a8ea2d02aacc6f:experiments/g5bb/roms/hybrid.$f" > "roms/baseline.$f"
done
for mode in baseline hybrid cacheprobe; do
  python runtime_capture.py "$mode" "$out/$mode-png" > "$out/$mode.jsonl"
  python measure.py "$mode" "$out/$mode.jsonl" "$out/$mode-png" "$out/$mode-pixels.jsonl"
done
for mode in baseline hybrid; do
  python runtime_capture.py "$mode" "$out/$mode-seed-png" --seeded > "$out/$mode-seed.jsonl"
  python measure.py "$mode" "$out/$mode-seed.jsonl" "$out/$mode-seed-png" "$out/$mode-seed-pixels.jsonl"
done
for series in frozen seeded; do
  flags=(--soak)
  if [[ $series == seeded ]]; then flags+=(--seeded); fi
  python runtime_capture.py hybrid "$out/$series-png" "${flags[@]}" > "$out/$series.jsonl"
  python measure.py hybrid "$out/$series.jsonl" "$out/$series-png" "$out/$series-pixels.jsonl"
done
for mode in baseline hybrid cacheprobe; do
  python trace_runtime.py "$mode" historic-reorder > "$out/trace-$mode-reorder.jsonl"
done
for fixture in historic-separated seed-00 seed-06 seed-dense-0 two-pairs; do
  python trace_runtime.py hybrid "$fixture" > "$out/trace-$fixture.jsonl"
done
python audit_kernel.py "$out"/trace-*.jsonl
bash -x native_regress.sh roms/baseline.bin roms/hybrid.bin "$out/native"
for mode in hybrid cacheprobe; do
  timeout 25 bash capture_stella.sh "roms/$mode.bin" "$out/stella-$mode-select" 253 select
  timeout 25 bash capture_stella.sh "roms/$mode.bin" "$out/stella-$mode-boot" 254
done
python measure_stella.py "$out"/stella-* > "$out/stella-pixels.jsonl"
```

Regressionsdatabasen gav **2 success, 0 fail** och oförändrad databashash. Stella 7.0:s cykeltimer på det verkliga RAM-fallet gav **66/66/66** cykler över tre träffar från `$BA` till `$B8`, vilket tillsammans med WSYNC:s tre cykler matchar auditens 69. Båda Stella-versionerna stannade på den faktiska RESP1-fällan efter körning. Stock 6.7.1 saknade timerkommandon. Full rålogg, råbilder, mätmatriser, nya ROM:ar och källor levereras separat. Detta är utvecklarens egenkontroll och väntar på MAIN IX:s mottagningsgranskning.
