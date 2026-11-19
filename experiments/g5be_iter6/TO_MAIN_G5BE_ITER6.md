# TO_MAIN_G5BE_ITER6 · LM-D37 · ROM DEVELOPMENT IV → MAIN X

**G5BE_ITER6_FIRST_X_AND_FIVE_X_Y15_OBSERVED_BOUNDED.** Den första sorterade fienden flyttas från X19 till X22, X25 och X30 via RAM i samma körande F6-ROM, medan de fyra andra står stilla. En kombinerad ROM visar fem numeriskt ändrade X-positioner och 15 raders Y-spridning i samma bildruta. Alla fem originalmasker, den gula spelaren, skottet och väggarna är pixel- och RGB-exakta i de godkända lägena. Detta är utvecklarobserverad diagnostik i en begränsad koordinatdomän.

Underlag är [MAIN X:s arbetsorder](https://github.com/Odourman/let-me-out/issues/30#issuecomment-7001091216) och fryst ITER5 `d41398f6cd325cc0ca89149e4304b1635f082469`. Maskfilen matchar projektets `design/NPC_REFERENCE_8x9_masks.json` byte för byte.

## Första RESP1 kring HBLANK

Historisk X-vektor är [127,19,73,100,46] och Y=[73,72,73,71,72] i maskordningen M/M/F/SM/SF. Grundprovet ändrar bara andra byte i X-vektorn. Gopher läste tillbaka alla tio X/Y-byte vid varje sceninträde.

| RAM-X | Första RESP1 CL före→efter | Första GRP1 CL före→efter | Faktiskt mask-X | Tända vita X på Y76 | Resultat |
|---:|---|---|---:|---|---|
| 19 | −14→−2 | −2→7 | 19 | 22,23 | PASS, kontroll |
| 16 | −17→−5 | −5→4 | 19 | 22,23 | FAIL 19 saknade/19 extra |
| 22 | −8→1 | −44→−32 | 22 | 25,26 | PASS |
| 25 | −5→4 | −14→−5 | 25 | 28,29 | PASS |
| 28 | −2→7 | −14→−2 | 30 | 33,34 | FAIL 18/18 |
| 30 | −2→7 | −14→−2 | 30 | 33,34 | PASS |

X19/22/25/30 är **8/8 PASS per läge** i slutlig `direct.bin`, och de fyra lägena ingår i dess 600-körning. X16 och X28 mättes på tidigare byggda varianter och finns i råarkivet. Matchning mot X19 respektive X30 kontrollerades mot hela originalmasken, med oförändrade övriga individer och P0/M0/PF. Tabellen visar uppmätta instruktionsintervall, registrerade TIA-skrivningar och slutbildens faktiskt tända pixlar. RESP1 vid c21 respektive c22 gav samma synliga mask-X i de två mätta HBLANK-lägena. Exakt intern START-/latchförklaring är **INCONCLUSIVE**.

Som kontroll mättes den andra RESP1 i fryst ITER5 vid CL13→22, 16→25, 16→28 och 22→31 för andra X43, X46, X49 och X52. Samtliga fyra lägen gav 8/8 pixel-PASS. Bussloggen har faktiska CPU-register och läst P1-tillstånd. Ingen alternativ HMOVE-/NUSIZ-metod behövdes för att frigöra första X. Den alternativa metoden är **NOT_RUN**.

## Fem ändrade X, Y15 och lokal nära-X-gräns

| Prov | ROM | X och Y, i maskordningen M/M/F/SM/SF | Resultat |
|---|---|---|---|
| Fem ändrade X | combined | X=[133,22,76,103,49], historiskt Y | PASS |
| Fem ändrade X och Y7 | combined | Samma X, Y=[74,68,75,71,71] | PASS |
| Fem ändrade X och Y15 | combined | Samma X, Y=[74,68,83,71,76] | PASS |
| Historiska X och Y15 | combined | X=[127,19,73,100,46], samma Y15 | PASS |
| Omordning och Y7 | combined | X=[103,49,22,76,133], Y=[71,71,68,75,74] | PASS |
| Annan X-kombination | combined | X=[136,25,76,100,52], historiskt Y | PASS |
| Vänstra avstånd 16, same-Y | direct | X=[127,30,73,100,46], alla Y72 | PASS |
| Vänstra avstånd 13, same-Y | combined | X=[127,30,73,97,43], alla Y72 | FAIL, hela vänstra M:s 28 pixlar saknas |
| Vänstra avstånd 13, varierande Y | combined | Samma X, historiskt Y | FAIL, samma 28 saknas |
| Avstånd 3, vänster eller inre par | combined | X=[133,22,76,103,25] eller [127,19,49,100,46], alla Y72 | REJECTED före raster |

Vid avstånd 13 är `VALID=1`. Den första RESP1 exekveras vid CL−2→7. Andra RESP1-instruktionen stegas vid CL13→22; Gopher upprepade ingen separat bussrad för just denna skrivning, så den redovisas som faktiskt stegad instruktion i CPU-loggen. Den följande GRP1-skrivningen syns vid CL22→34. Första M syns inte alls. Det är en lokal rasterkonflikt i den prövade femstrobssekvensen. Intern START-/resetkausalitet är **INCONCLUSIVE**. Avvisade avstånd 3 har fysisk renderbarhet **NOT_RUN**.

- `direct` och `combined` gav vardera **600/600 sammanhängande PASS**, FR21–620, sex RAM-sceningångar per serie och exakt 262 scanlines. Combined-serien hade 100 historiska Y15 och 100 fem-X/Y15. I alla positiva bilder återgavs 136 NPC-, 32 P0-, 25 M0- och 3047 PF-pixlar på exakt referensposition med exakt RGB.
- En separat blandad serie i combined gav **48/48 ×262**, med 28 PASS, 8 fysiska FAIL och 12 REJECTED. Hela slutmatrisen inklusive referens- och negativprov gav **1652/1652 ×262**. Det betyder 1451 pixel-PASS, 48 fysiska pixel-FAIL och 153 REJECTED.
- Stock Stella **6.7.1** bekräftade X30 i 12/12 bilder. Både stock Stella **6.7.1 och 7.0** bekräftade fem ändrade X och Y15 i 12/12 bilder vardera. Dessa körningar startar från bootvärden. Stella live-POKE och egen mätning av bildrutelängd är **NOT_RUN**.
- Fryst ITER5 och ny direct-kontroll reproducerar X67/73/76 PASS samt fysiska tredje-X64/X82 FAIL. Frysta ITER5:s fyr-X/Y15 [133,19,76,103,49] klarar 4/4 igen på den frysta ROM:en. Samma vektor avvisas på combined, där första X19 väljer en annan fasbank. Fasdomänerna är olika. Historisk Y15 fungerar i båda. Av 20 äldre fixturer ger combined 2 PASS och 18 REJECTED, jämfört med fryst ITER5:s 3 PASS och 17 REJECTED.

## Tid, bankutrymme och livslängder

Första sorterade X väljer bank från en numerisk uppslagstabell. De andra X-byte styr maskordning, val av radkedja och kontrollerar att de finns i bankens begränsade fasfamilj. Maskdata och Y kommer från RAM/RIOT vid varje bildruta. Detta visar faktiskt numeriskt ändrade koordinater för alla fem i ett körbart test. Fasbankarna tillåter ett begränsat urval X-kombinationer.

`BANKSEL` får sitt värde när första sloten behandlas. Samma byte som i ITER5 används, utan att utöka RIOT. `ORDER` används för identitetsindex tills motsvarande poster har förbrukats. De två första byten återanvänds därefter för långbandets maskpekare, och först efter cachefyllnaden för kontrollflödets indirekta hopp. Varken de tre senare identitetsindexen eller de fem maskplanen skrivs över vid den återanvändningen.

| ROM | RIOT med stack | Aktivrader i binäraudit | Max CPU/rad | Minsta lediga svans före hotspots |
|---|---:|---:|---:|---:|
| direct | 92/128, SP=$FD | 220 | 76 | 157 byte |
| combined | 126/128, SP=$FF | 150 | 76 | 666 byte |

Varje ROM innehåller fyra banker om 4096 byte. Cykelrevisionen kontrollerar 370 aktiva radpaket och inga överhäng. RIOT-gränserna är verifierade från symboltabell och Gophers stackavläsning vid pekaruppbyggnadens högsta bruk. I combined upptar cachen $A2–$FD och stackfri pekaruppbyggnad lämnar $FE–$FF lediga. F6-hotspots vid $FFF6–$FFF9 används under VBLANK.

Den första combined-versionen gav **263 rader i Y15-lägena**. Fasloggen placerade den förlorade raden mellan tredje slotens två pekarfaser. När tredje sloten fick första jämförelsen i den segmenterade blankningsvägen återställdes 262. I det slutliga Y15-provet börjar de tätaste cache-WSYNC-instruktionerna senast CL148 (c72, plus tre CPU-cykler). Slutlig blankning mäts vid SL35 CL142 och avblankningsvägens början vid SL36 CL−47. Den sju rader långa delkedjan körs från SL121 CL−68 till SL128 CL−68 med overscan vid SL228 CL−56 i både historiska och ändrade X-läget.

Z3 4.15.4 ger 32 SAT och 3 UNSAT i den publicerade modellen. Solvern förutsäger instruktionernas skrivfaser. Den avläser varken fysisk pixelstart eller ihållande grafik i emulatorn. De två felkalibrerade X-proven och avstånd 13 finns bevarade som fysiska FAIL.

## Bygg och återkörning

- `direct.bin` SHA-256 `9802cbbcc029635f9493dbc3635a04c1a48d985e87554de69917ec246b17bd92`
- `combined.bin` SHA-256 `d68df8df29dcc53ecb11e92328b6cda44c5543404390d2d1a0537934ee23dcd7`

DASM 2.20.14.1 byggde F6. Gopher2600 v0.57.2 utförde POKE/PEEK, TIA-, CPU-, stack- och NTSC-mätning. Stock Stella 6.7.1/7.0 gav original-PNG. Python/Pillow jämförde individuella pixlar och RGB. `evidence/brief/tools.txt` innehåller verktygshashar. [G5AR](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [G5BB](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

Kör från `experiments/g5be_iter6`. `SHA256SUMS` täcker ASM, ROM, tester, originalbilder och råarkiv. `evidence/brief/matrix.tsv` ger individuell X/Y och resultat. Varje långkörnings 600 rad-/maskvisa scoreposter ligger delade i tolv direktläsbara filer.

```bash
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
out=$(mktemp -d)
python -m venv "$out/z3"
"$out/z3/bin/pip" install -r requirements.txt
"$out/z3/bin/python" schedule.py > "$out/solver.jsonl"
cmp solver.jsonl "$out/solver.jsonl"
python build.py
python build.py --name combined --rows 17 --unified --segmented
python audit.py | cmp - evidence/brief/cycles.jsonl
python banks.py | cmp - evidence/brief/banks.jsonl
python beam.py roms/direct.bin --first-domain 19 30 22 25 > "$out/direct-beam.jsonl"
python beam.py roms/combined.bin --stack-only > "$out/combined-stack.jsonl"
python beam.py roms/combined.bin --fixture close13-same-y --bank 1 > "$out/close13.jsonl"
python ram.py direct "$out/direct-beam.jsonl"
python ram.py combined "$out/combined-stack.jsonl"
python phase.py roms/combined.bin --fixture five-slots-y15 > "$out/phase.jsonl"
for spec in direct:first direct:third direct:close direct:first-soak \
            combined:unified combined:seg-soak combined:mixed-stress combined:legacy combined:prior-y15; do
    rom=${spec%:*}
    group=${spec#*:}
    tag="$rom-$group"
    python replay.py "roms/$rom.bin" "$out/$tag" --group "$group" > "$out/$tag.jsonl"
    python score.py "$out/$tag" evidence/reference/frozen-gopher-y76.png --ref-height 214 \
        --log "$out/$tag.jsonl" > "$out/$tag-score.jsonl"
done
python build.py --name combined-bootfar --rows 17 --unified --segmented --boot-far \
    --first 22 --second 49 --third 76 --fourth 103 --right 133
bash capture_stella.sh roms/combined-bootfar.bin "$out/stella671" 572
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash capture_stella.sh roms/combined-bootfar.bin "$out/stella70" 573
python score.py "$out/stella671/images" evidence/reference/stella-671-frozen.png \
    --first-x 22 --second-x 49 --boot-x 76 --fourth-x 103 --right-x 133 --far
python score.py "$out/stella70/images" evidence/reference/stella-70-frozen.png \
    --first-x 22 --second-x 49 --boot-x 76 --fourth-x 103 --right-x 133 --far
```

**Till MAIN X.** Bunden fem-X/Y15 är demonstrerad i samma körande ROM. Godtyckliga kombinationer och tät placering är fortfarande öppna. Nästa tekniska fråga är fasval och kopiebevarande mellan tidiga nära RESP1-strobes. **VERIFICATION II är NOT_RUN.** `G5_FORMAL_OPEN` kvarstår.
