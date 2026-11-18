# TO_MAIN_G5BB · LM-D34 · ROM DEVELOPMENT IV → MAIN IX

**`G5BB_PARTIAL_RENDERER_PROGRESS` · 18 november 2026 · DEVELOPER_OBSERVED**

Det historiska separerade fallet **X 19/46/73/100/127, same-Y** är reparerat. Det historiska omordnade fallet visar fyra av fem masker, med F-masken fortfarande borta. Två nya separerade/omordnade fixturer med lite mer utrymme mellan vissa slotar är pixelrätta. Samtliga fem positiva G5BA-fixturer är fortsatt pixelrätta. **G5_FORMAL_OPEN kvarstår.**

## Varför hela masker försvann

Den frysta G5BA-ROM:en (`793cb44d5a763e6f744c2dfacd8440eb39e2cea014127bd22399eec6345c9526`) kördes först. PEEK av ORDER gav 0/1/2/3/4 respektive 1/4/2/3/0. Båda scenerna begär RESP1 vid c22/31/40/49/58 men G5BA utförde c22/40/58 och GRP1 c25/43/61. `USED=2`, sista `TARGET=58`, `KT=61`. För den första bortplanerade sloten ger c31 minus föregående GRP1-slut c25 sex cykler. Ny indexerad LDA och nästa RESP1 kräver sju. Samma sak händer vid c49. Hela maskerna saknas därför redan i genererad RAM-kod. Det syns i dump, TIA-skrivspår och PNG.

`hybrid.bin` behåller G5BA:s cachekompaktering och inline-OR när dessa används. I en kortare separat rasterväg flyttas bandets sluttest till radens svans och nästa tätt följande mask förladdas i X när föregående slot har spelrum. Det klarar två separata 27-pixelsmellanrum i de nya fixturerna, där annan lucka ger förladdningstid. I den särskilda femslotvägen för det historiska same-Y-läget har de första två identiteterna samma M-mask och Y. Kärnan utelämnar en redundant GRP1-skrivning, förladdar den fjärde masken i X och lagrar femte maskens nästa radbyte i RIOT. Alla radvärden hämtas från de aktuella koordinaternas maskpekare. Den specialiserade strobsekvensen väljs enbart för exakt X 19/46/73/100/127 och samma Y för de två första M-aktörerna. Det omordnade historiska fallet saknar den redundansen och hoppar fortfarande över F vid c40. Ingen global 27-pixelgaranti.

## Pixelmatris och långtidsprofil

Varje kortfall kördes tre analyserade bilder. Tal anger saknade/extra vita pixlar per bild. Gopher använde POKE/PEEK på XP `$81–$85` och YP `$86–$8A` i samma binär och kontrolläste samtliga efter varje scen. PNG-oraklet jämför oförändrade M/M/F/SM/SF-masker, fysisk union och unika synliga pixlar per individ. Det nyttjar P0 som gemensam vertikal referens. Gul P0 och aktiv M0 mättes till 32 respektive 25 pixlar, och bruna PF-kanter syntes på båda sidor. Under ett första pipelineförsök sjönk M0 till 24 pixlar. En justerad avstängningsrad återställde den aktiva 25-pixelsmarkören vid oförändrat 262 scanlines. Det första försöket finns kvar i arkivet.

| Fryst historiskt fall | G5BA | G5BB `hybrid` | Utfall |
|---|---:|---:|---|
| Separerat X 19/46/73/100/127, Y 72 | 48/0 | **0/0** | PASS |
| Omordnat X 127/19/73/100/46, Y 73/72/73/71/72 | 42/0 | 38/0 | FAIL, F helt saknad |
| Close3 X 73/76/79/82/85 | 76/28 | 76/28 | FAIL |
| Close1 X 73/74/75/76/77 | 37/28 | 37/28 | FAIL |
| Same-X X 73/73/19/100/46 | 42/0 | 42/0 | FAIL |

| Långtest `hybrid.bin` | Positiva bilder | X, Y för nya fixturer |
|---|---:|---|
| Historiskt separerat | 100/100 | Enligt historisk matris |
| Separerat med omfördelad cykellucka | 100/100 | X 19/46/76/118/145, Y 72 |
| Omordnat med omfördelad cykellucka | 100/100 | X 145/19/76/118/46, Y 73/72/73/71/72 |
| G5BA nära 2 px, nära 1 px, reorder, same-X, två par | 300/300 | 60 per oförändrad G5BA-fixture |

Totalt **608 sammanhängande TV FRAME-avläsningar vid 262 scanlines**, varav 600 poängsatta råbilder och 8 övergångar utan PNG. Alla 600 bilder var pixelrätta, och varje NPC hade sina unika pixlar synliga i 600/600, max 0 poängsatta bilder helt frånvarande. PF-pixelantalet var 3047 i sju scener respektive 3046 i den nya omordnade fixturen. Den separata koordinatmatrisen matchade 48/50 (G5BA:s tidigare NPC0 X55→52 är kvarstående FAIL). X-rest 0/1/2 ingår i de logiska kompositkoordinaterna. Individuella P1-strobankare har fortfarande trepixlars upplösning; fri heltals-X över hela spelplanen är **NOT_RUN**.

## Verkliga alternativ och bussmätning

- **M1 FAIL.** M1 delar P1:s färg och NUSIZ. Provet slog på en vit 8-pixelsmissil bara på den saknade F-maskens hela armrad i den historiska omordningen. Efter 5 px positionskalibrering gick den scenen från 38/0 till **30/8**. Alla åtta avsedda bitar återkom på raden, men kopian gav åtta spökpixlar. TRACE visade NUSIZ1=`$31`, RESM1=`$40`, HMM1=`$40`, HMOVE=`$40` under blanking och ENAM1=`$02` på SL111, c68 inför nästa rad. P1 skrev RESP1 c22/31/49/58 och GRP1 c25/34/52/61. Stock Stella reproducerade 30/8. Detta prov återger en rad, utan ersättning för F:s 8×9-mask.
- **VDEL FAIL.** VDELP1=$01 med samma P1-schema gav 74/48 saknade/extra i historiskt separerat och 82/58 i historiskt omordnat, i båda emulatorerna. Den fördröjda latchen bevarar inte dessa täta GRP1-uppdateringar i den valda skrivordningen.
- **NUSIZ1=$00 FAIL.** Med oförändrade strobcykler förlorades alla 136 vita maskpixlar i båda historiska huvudfallen. Stock Stella bekräftade. `hybrid` använder uppmätt NUSIZ1=$01.
- **P1-timing.** I reparerat historiskt same-Y loggades RESP1 **22/31/40/49/58**, GRP1 **25/43/52/61** över alla 24 kritiska rader (SL100–123). Skrivningen på c34 behövs inte eftersom samma M-rad ligger kvar i latchen. Ny separerad fixture gav 22/31/41/55/64 respektive 25/34/44/58/67. Gopher `PLAYER 1` svar och fulla bussdata finns i arkivet. Timingen avser **CPU-skrivslut**, och intern TIA START är **INCONCLUSIVE**. De synliga pixlarna mättes separat i råbilderna.
- **Budget.** Granskaren `audit_kernel.py` avkodade faktiska 64-byte RAM-dumpar, kontrollerade att indexerade läsningar inte korsade sidor vid Y 0–23 och räknade 76 cykler inklusive WSYNC i reparerad same-Y och M1, 75 i nya separerade fallet, 69 i historiskt omordnat. Max observerad kodlängd var 55 byte. RIOT-reservationen är 1 bildräknare +10 koordinater +5 sortindex +16 arbetsbyte +24 cache +64 kod +8 stack = **128 byte**. Cachen delas mellan komposit och next-row-byte. Djupaste nästlade JSR använder 4 stackbyte. F6 har fyra identiska 4 KiB-banker. Största kod/markörregionen för hybrid är $0578 byte och för M1 $05D8 per unik bank, plus tabeller och vektorer.
- **Stella 6.7.1.** Tolv exakta historiskt separerade stickprov och tolv historiskt omordnade med 38/0. VDEL- och enkelkopie-ROM samt M1 har egna negativa serier. **Stella 7.0** gav dessutom 12/12 exakta same-Y-bilder. 600-bildersprofilen gäller Gopher. R2/S05 och fysisk hårdvara **NOT_RUN**.

## Verktyg som faktiskt användes

- G5AR ENV-01 användes för DASM 2.20.14.1, stock Stella 6.7.1, Gopher2600 v0.57.2 revision `2af86eb725739adbf3d9d45cea2ed69eea57da2a`, Xvfb och xdotool. Python 3.12.14, Pillow 13.0.0 och ImageMagick fanns i miljön. Bytehashar finns i `tool-inventory.txt`. Gopher-revision kommer från den faktiska PTY-körningen.
- **Ny sidoinstallation:** officiell Stella 7.0 amd64, extraherad med `dpkg-deb -x` i uppdragets privata arbetskatalog. Paketmetadata gav 7.0, och copyrightfilerna innehåller GPL-2+ för Stella. Paket-SHA-256 `1bc4a1ea57661c315db6035fb55bef8e7e0d0f1054b0db2b256888f3a9a871a9`, binär `afe0e4d91ecd2e57f7680c6e0ec01e8b5241a8034c56016199da5e123fc8040c`. GitHub-releasen saknade separat digest i metadata, så dessa är lokalt beräknade för de hämtade byten. Fryst Stella 6.7.1 användes också och ersattes aldrig. [Officiellt paket](https://github.com/stella-emu/stella/releases/download/7.0/stella_7.0_amd64.deb)
- Båda debuggerversionerna körde `exec`, registrerade `breakIf { pc == … && _bank == #0 }` och `trapWrite $11`, och nådde bandet på SL100 i bank 0. Stella 7.0 gjorde faktisk skrivfälla och stannade vid PC `$C9` efter första RESP1 på SL104. Timern mellan RAM `$BA→$B8` gav **73/73/73 cykler** (min/medel/max över tre träffar), plus tre cykler för WSYNC-instruktionen enligt käll-/emulatorkontroll. `listTimers` och `resetTimers` fungerade i 7.0, och gav `No such command` i 6.7.1. Rå `saveSes` finns i arkivet. [Stellas officiella debuggerhandbok](https://stella-emu.github.io/docs/debugger.html)
- Gopher v0.57.2:s faktiska `regress`-hjälp och isolerad Regression Database bekräftades. Två positiva poster, 30 frames vardera (fryst G5BA nära-par och reparerad G5BB same-Y), gav **2 success, 0 fail**. Databasens SHA matchade före/efter RUN. De historiska negativa fixturerna loggas i pixelmatrisen som förväntade FAIL. Ingen REDUX kördes. [Gopher Regression Database](https://github.com/JetSetIlly/Gopher2600-Docs/wiki/Regression-Database)
- Studerade dionoids build-script och exempel vid `f40ec34808a6fdafeb8ffa00a19ee379f4b4231d`. Metoden med DASM-listning/symboler och tidsbegränsad Xvfb-debuggersession tillämpades i egna projektskript. Repo-API gav ingen licensidentifierare. Ingen källkod kopierades och den modifierade emulatorn och `-dbg.logexec 1` användes inte. [Granskad verktygskälla](https://github.com/dionoid/atari2600-dev-skills/tree/f40ec34808a6fdafeb8ffa00a19ee379f4b4231d)

## Reproduktion

Kör från `experiments/g5bb` med G5AR ENV-01 tillgänglig. För fryst jämförelse behöver Git ha commit `c9df38692eb8807b515ddcc26e05c82e8f379509`.

```bash
set -e
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
n=260
for mode in hybrid vdel singlecopy missile; do
    python runtime_capture.py "$mode" "$out/$mode-png" > "$out/$mode.jsonl"
    python measure.py "$mode" "$out/$mode.jsonl" "$out/$mode-png" "$out/$mode-pixels.jsonl"
    timeout 25 bash capture_stella.sh "roms/$mode.bin" "$out/stella-$mode-select" "$n" select
    n=$((n+1))
done
timeout 25 bash capture_stella.sh roms/hybrid.bin "$out/stella-hybrid-boot" "$n"
python measure_stella.py "$out"/stella-* > "$out/stella-pixels.jsonl"
python runtime_capture.py hybrid "$out/soak-png" --soak > "$out/soak.jsonl"
python measure.py hybrid "$out/soak.jsonl" "$out/soak-png" "$out/soak-pixels.jsonl"
for item in bin sym; do
    git show "c9df38692eb8807b515ddcc26e05c82e8f379509:experiments/g5ba/roms/hybrid.$item" > "roms/baseline.$item"
done
for mode in baseline hybrid; do
    for fixture in historic-separated historic-reorder; do
        python trace_runtime.py "$mode" "$fixture" > "$out/trace-$mode-$fixture.jsonl"
    done
done
python trace_runtime.py missile historic-reorder > "$out/trace-missile.jsonl"
python audit_kernel.py "$out"/trace-*.jsonl
bash native_regress.sh roms/baseline.bin roms/hybrid.bin "$out/native"
bash stella_debug.sh roms/hybrid.bin "$out/stella67-debug" 270 /workspace/.g5ar-env01/bin/stella
curl -fL --max-time 50 -o "$out/stella_7.0_amd64.deb" https://github.com/stella-emu/stella/releases/download/7.0/stella_7.0_amd64.deb
printf '%s  %s\n' 1bc4a1ea57661c315db6035fb55bef8e7e0d0f1054b0db2b256888f3a9a871a9 "$out/stella_7.0_amd64.deb" | sha256sum -c -
dpkg-deb -x "$out/stella_7.0_amd64.deb" "$out/stella7"
bash stella_debug.sh roms/hybrid.bin "$out/stella70-debug" 271 "$out/stella7/usr/bin/stella"
```

Negativa ROM:ar, källsnapshots, orörda PNG, råa PTY-svar och mätningar ligger i arkivet. Status gäller egenkontroll. Ingen gameplay-integration påbörjades.
