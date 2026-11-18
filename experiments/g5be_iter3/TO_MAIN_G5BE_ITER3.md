# TO_MAIN_G5BE_ITER3 · LM-D37 · ROM DEVELOPMENT IV → MAIN IX

**G5BE_ITER3_THIRD_X_DECOUPLED_BOUNDED.** Den tredje sorterade fienden flyttas från X73 till **X67 och X76** genom RAM-skrivningar i samma körande `all-p1.bin`. De andra fyra X/Y-paren hålls fasta. Alla fem ursprungliga masker visas fullständigt i samma NTSC-bildruta med exakt P0, M0 och PF. X64 och X82 är fysiskt testade FAIL. Fri X/Y är fortfarande FAIL. Statusen bygger på utvecklarens emulatorobservationer.

Arbetet följer [MAIN IX:s fortsättningsorder](https://github.com/Odourman/let-me-out/issues/30#issuecomment-6987687323) och utgår från fryst ITER2 `aa789b39aca3c7b27a434f1fa28c34bf43db33f3`. Maskfilen är byteidentisk. Referensbilderna och den frysta kontroll-ROM:en finns i `evidence/reference/`.

## Tredje X i samma bildruta

Alla fem maskers start-Y i tabellen är `[73,72,73,71,72]` i ordningen M/M/F/SM/SF. Bara F:s X ändras i `[127,19,X,100,46]`. Samtliga X/Y-värden lästes tillbaka med PEEK före bildtagning. Alla 32 mätta bildrutor per ROM höll 262 scanlines, inklusive övergångarna. Varje tabellcell för respektive X gäller samtliga bildrutor i det läget. Saknade/extra avser vita NPC-pixlar.

| X | Fryst ITER2-kontroll | A · `late-p0` | B · `all-p1` |
|---:|---|---|---|
| 73, 8 bilder | PASS, 0/0 | FAIL, 42/0 och hela gula P0 saknas | PASS, 0/0 |
| 67, 8 bilder | FAIL, 136/0 | FAIL, 46/0 och hela gula P0 saknas | PASS, 0/0 |
| 76, 8 bilder | FAIL, 136/0 | FAIL, 52/15 och hela gula P0 saknas | PASS, 0/0 |
| 82, 4 bilder | FAIL, 136/0 | FAIL, avvisat läge utan schema | FAIL, 18/18 i F |
| 64, 4 bilder | FAIL, 136/0 | FAIL, 45/0 och hela gula P0 saknas | FAIL, 12/18 i SF |

**A – sen RESP0.** VBLANK förbereder samma fem maskplan. Fyra fiender nyttjar P1. På varje aktiv rad försöker en tidig RESP0 kring c24 återställa den gula spelaren och en andra RESP0 flytta F med NUSIZ0 i enkelkopieläge. För att få plats flyttades vänstra P1-stroben från c22 till c21. Den tidiga och sena RESP0-skrivningen syns fysiskt i Gophers Y76-busspår. Spelaren och F försvinner i de schemalagda lägena trots att grafiksvaren och båda färgskrivningarna når TIA. M0 och PF är pixel-/RGB-exakta. X82 saknar schema under de provade fönstren, så där mättes avvisningsvägen och den sena RESP0-mekanismen för just det X-värdet är NOT_RUN. Stock Stella bekräftar X67-felet. Den lokala begränsningen är att två faktiska RESP0-strobes inom de här tidfönstren inte återger de två avsedda P0-grafikinstanserna.

**B – fem P1-strobes.** Varje NPC har en separat RESP1-strobe och GRP1-maskläsning. P0 visas på sin basposition med NUSIZ0=0 och spelarfärgen orörd under bandet. M0 och väggen behåller samma `(x,y,RGB)`. VBLANK sorterar RAM-X och bygger maskpekare från RAM-Y för identiteterna. Tredje sorterade X väljer ett registerschema medan individens bitmap kommer från radcachen. Gophers buss visar fem RESP1-strobes men ingen RESP0-strobe i den spårade aktiva raden. Vid X82 är F-pixlarnas form bevarad men ligger två pixlar för långt åt höger (uppmätt X84) i den mätta helbilden. Vid X64 blir SF:s GRP1-pixlar fel. Modellen har ingen fullständig TIA START-/serializer-modell, och den exakta interna orsaken till de två felen är INCONCLUSIVE.

## Koordinatområde och längre körning

Samtliga lägen kördes med samma `all-p1.bin`; koordinatvektorerna nedan matades via debugger till RAM.

| Prov | Indata, i ordning M/M/F/SM/SF | Utfall |
|---|---|---|
| Höger M | X 124,19,67,100,46 | FAIL, 136/0 |
| Vänster M | X 127,22,67,100,46 | FAIL, 136/0 |
| SF | X 127,19,67,100,43 | FAIL, 136/0 |
| SM vänster | X 127,19,67,97,46 | FAIL, 136/0 |
| SM höger | X 127,19,76,103,46 | FAIL, 136/0 |
| Alla fem ändrade | X 130,22,70,103,43 | FAIL, 136/0 |
| Band uppåt | X 127,19,67,100,46 · Y 69,68,69,67,68 | PASS, 0/0 |
| Band nedåt | X 127,19,76,100,46 · Y 78,77,78,76,77 | PASS, 0/0 |
| Vertikalt spridd | X 127,19,67,100,46 · Y 74,68,83,71,76 | FAIL, 136/0 |

De sex nya X-vektorerna kördes som RAM-prov. MATCH-vakten avvisade dem eftersom den här generatorn har fasta yttre slots, vilket behåller P0/M0/PF men lämnar alla NPC dolda. Det är en programgräns; de sex kombinationernas TIA-renderbarhet är NOT_RUN. För vertikal spridning avvisar maskcachen `max(Y)-min(Y)>2`. Det provade bandet är elva fysiska rader och start beräknas från RAM med tillåten `min(Y)` 66–76. Hela Y-domänen är inte uttömmande testad.

- **600/600 PASS** i samma RAM-ROM, FR21–620, utan avbrott och 262 rader på samtliga bilder. Block om 100 bilder följde X73, X67, X76, band uppåt, band nedåt och X67 igen. Varje godkänd bild hade 136/136 maskpixlar, 32/32 P0, 25/25 M0 och 3047/3047 PF på rätt `(x,y,RGB)`.
- De 20 äldre fixturerna kördes med tre bilder vardera. **1/20 PASS** för historisk separerad och **19/20 FAIL**. **60/60 ×262**. ITER2:s andra godkända fjärde-X-scheman X97/X103 ingår inte i ITER3-kärnan. Den frysta ursprungliga 600-matrisen som helhet är **NOT_RUN** på ITER3 då kandidaten inte täcker den.
- De sex nya X-vektorerna och tre Y-fallen gav **36/36 ×262**. Gopher-matrisens tre tredjeslottskörningar, utökade körning, äldre fixturer och 600-körning gav tillsammans **792/792 ×262** efter uppvärmning. Uppstarten och Gophers automatiska bildutsnitt loggas separat.
- Stock Stella **6.7.1** upprepar B:s X67 PASS i 12/12 bilder och X76 i 3/3, och B:s X82 FAIL i 4 stabila bilder. Stock Stella **7.0** upprepar X67 PASS i 7 stabila bilder, X76 i 10 och X82 FAIL i 10. Metod A:s X67 FAIL upprepades i 3 respektive 10 stabila bilder. Tidiga helt blanka startbilder ligger kvar i råloggarna och är **INCONCLUSIVE** för scenen. Stella-bildrutelängd och live-POKE är **NOT_RUN**; Stella-kontrollen använder bootvarianter med enbart annat initialt X-byte.

## Budget, solver och tidigare fel

- Standard F6/NTSC med fyra identiska 4 KiB-banker per ROM. DASM-listningar och binär opkodrevision omfattar **99 radpaket** (44 A, 55 B), alla **76 CPU-cykler**, inklusive utfyllnad eller hopp. Sista TIA-skrivningen ligger vid c70–73 i A och c61–64 i B. Gopher stoppar vid början av Y76 och Y77 på samma FR och vid samma färgklocka CL−68 på påföljande rasterrad. Tre färgklockor per CPU-cykel. Mask- och spelarindexering ligger på respektive ROM-sida.
- **91/128 RIOT-byte inklusive två stackbyte**. 55 cachebyte, fem XY-par, fem sorteringsindex, fem tvåbytespekare, en räknare, fyra kontroll-/temporärbyte och fyra gemensamma styrbyte. Resten fri mellan de använda områdena. Nollställningen berör hela RIOT vid reset.
- Z3 4.15.4 med trecykels RIOT-masklast hittar ett A-schema för X64/67/73/76 vid de prövade fönstren och UNSAT för X82. För B finns SAT för alla fem X, även de två som blev fysiskt fel. Modellfönstren avgränsar CPU-instruktionspackning, skrivfaser och A/X-livslängder. SAT och UNSAT säger bara vad den modellen tillåter.
- Tidig linjär uppslagning för tredje X gav 263 rader i X73. Den ersattes med ett direkt indexerat val. En första Y-bandversion gav åtta väggpixelavvikelser efter senarelagd VBLANK-avblankning. Ett kortare min-Y-steg och en synkroniserad avslutning av VBLANK återställde väggens hela pixelmatris. Tidiga ROM:ar, assembler, resultat och originalbilder finns i råarkivet. Gophers automatiska utsnitt beskär ibland väggens överkant under tidiga uppstartrutor. Dessa loggas som warmup i reproduktionen och ändrar inte ROM:ens acceptansgräns.

## Bygg, kör och granska

| Verktyg | Utfört och bevis |
|---|---|
| DASM 2.20.14.1, G5AR | `python build.py`; `evidence/brief/dasm-rebuild.log`, bank/lista/symboler och SHA-256 |
| Gopher2600 v0.57.2, G5AR | `replay.py` med verklig POKE/PEEK, `trace.py` med verkliga TIA-busskrivningar; direktläsbara frame- och bussloggar samt rå PTY i arkivet |
| Stock Stella 6.7.1/7.0, G5AR/isolering från G5BB | `capture_stella.sh` och `score.py --boot-x`; originalbilder, versionstitlar och bildresultat |
| Z3 4.15.4 och Python/Pillow | `schedule.py`, `audit.py`, `score.py`; solver-, budget- och pixelmatriser |

Exakta binärhashar för verktygen finns i `evidence/brief/tools.txt`. [G5AR-källa](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [G5BB:s stock Stella 7.0](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

- `all-p1.bin` SHA-256 `f2a78617e6ec7f1481127aececda5e7ad0d857fd96ac084d08b411755d2676c7`
- `late-p0.bin` SHA-256 `b561cfcd2bb741365526cd7f201ce9b6f74a9f86c470192b7fc9a717fa04bd74`
- `SHA256SUMS` täcker källor, ROM:ar, modell, budget, originalbilder, råarkiv och maskvisa diffar. `evidence/brief/matrix.tsv` innehåller individuella X/Y-värden och resultat. Per-frame score-JSON visar varje mask och radvis positionsdiff.

Kör från `experiments/g5be_iter3` med G5AR-prefixet. `build.py` anropar DASM `-DDYNAMIC=1 -DBOOT_X=<koordinat> -f3` och upprepar varje 4 KiB-bank fyra gånger.

```bash
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
out=$(mktemp -d)
python -m venv "$out/z3"
"$out/z3/bin/pip" install -r requirements.txt
"$out/z3/bin/python" schedule.py > "$out/model.jsonl"
cmp solver.jsonl "$out/model.jsonl"
python build.py
python audit.py | cmp - evidence/brief/cycles.jsonl
for spec in late-p0:third all-p1:third all-p1:extended all-p1:legacy all-p1:soak; do
    rom=${spec%:*}
    group=${spec#*:}
    tag="$rom-$group"
    python replay.py "roms/$rom.bin" "$out/$tag" --group "$group" > "$out/$tag.jsonl"
    python score.py "$out/$tag" evidence/reference/frozen-gopher-y76.png \
        --ref-height 214 --log "$out/$tag.jsonl" > "$out/$tag-score.jsonl"
done
python replay.py evidence/reference/frozen-iter2-stream.bin "$out/control" > "$out/control.jsonl"
python score.py "$out/control" evidence/reference/frozen-gopher-y76.png --ref-height 214 --log "$out/control.jsonl"
python trace.py roms/late-p0.bin > "$out/late-p0-bus.jsonl"
python trace.py roms/all-p1.bin > "$out/all-p1-bus.jsonl"
bash capture_stella.sh roms/all-p1-boot67.bin "$out/stella671" 531
python score.py "$out/stella671/images" evidence/reference/stella-671-frozen.png --boot-x 67
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash capture_stella.sh roms/all-p1-boot76.bin "$out/stella70" 532
python score.py "$out/stella70/images" evidence/reference/stella-70-frozen.png --boot-x 76
```

**Beslutspunkt för MAIN IX.** Den femstrobs P1-vägen har fysisk evidens för frikoppling av tredje X och för två förflyttade Y-band. Den avgränsning som återstår är generering av fler P1-faser för de yttre X-slotsen, samt cache för större vertikal spridning. Resultaten gäller de två testade arkitekturerna. Oberoende Verification är **NOT_RUN**. `G5_FORMAL_OPEN` kvarstår.
