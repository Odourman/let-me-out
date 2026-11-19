# TO_MAIN_G5BE_ITER5 · LM-D37 · ROM DEVELOPMENT IV → MAIN X

**G5BE_ITER5_SECOND_X_AND_SEGMENTED_Y15_OBSERVED_BOUNDED.** Den andra sorterade fienden flyttades från X46 till X43, X49 och X52 via RAM i samma körande F6-ROM. I en annan körande F6-ROM fungerade fyra samtidiga X-ändringar och den tidigare avvisade Y-spridningen på 15 rader. De fem originalmaskerna samt P0, M0 och PF var pixel- och RGB-exakta. Resultatet är utvecklarobserverat och gäller den mätta koordinatdomänen.

Arbetet följer [MAIN X:s arbetsorder](https://github.com/Odourman/let-me-out/issues/30#issuecomment-7000732771) från fryst ITER4 `ca14918a2ebe81c7986a73b34aa5d1de2e1cebb7`. Maskfilen matchade `design/NPC_REFERENCE_8x9_masks.json` byte för byte.

## Vänsterslotten och TIA

Alla koordinater nedan anges i maskordningen M/M/F/SM/SF. Grundprovet behöll X=[127,19,73,100,**x**] och Y=[73,72,73,71,72]. Gopher skrev och läste tillbaka alla tio X/Y-byte vid scenbyten.

| ROM och prov | Andra RESP1, CL före→efter | Vita SF-pixlar på Y76 | Resultat |
|---|---|---|---|
| Fryst ITER4, X46 | 16→25 | 49,50 | PASS |
| ITER5, X46 | 16→25 | 49,50 | PASS 8/8 |
| ITER5, X43 | 13→22 | 46,47 | PASS 8/8 |
| ITER5, X49 | 16→28 | 52,53 | PASS 8/8 |
| ITER5, X52 | 22→31 | 55,56 | PASS 8/8 |

På fryst ITER4:s Y76 mättes första RESP1 vid CL −14→−2 och följande GRP1 vid −2→7. Andra RESP1 mättes vid CL16→25 och dess GRP1 vid 25→34. Den vita masken vid X19 gav de tända pixlarna 22,23 på Y76 i alla fyra lägen. Bussloggen innehåller faktiska skrivningar, CPU-register och Gophers P1-readout. Intervallen gäller hela instruktionen. Tänd pixelstart avläses från PNG; den interna TIA START-fasen mellan klockkanterna är **INCONCLUSIVE**.

Vid tidigt X43-prov började F:s nya GRP1-grafik före tredje RESP1. Det gav 4 saknade och 19 extra vita pixlar, med saknade pixlar i SF. När generatorn krävde att F:s GRP1 kommer efter dess RESP1 blev X43 pixelrätt. Det är en uppmätt schemaskillnad; intern latchkausalitet är INCONCLUSIVE. En separat tidig uppslagstabellsversion avvisade felaktigt alla fyra lägen när LDX ersatte flaggvärdet från koordinatjämförelsen. Dessa bildrutor är **REJECTED**, och den rättade sekvensen prövades i en ny ROM. Den ordinarie fem-RESP1-metoden nådde milstolpen och gjorde ett separat HMOVE-/VDEL-prov obehövligt.

## Kombinerade koordinater och långkörning

- **`left.bin`** väljer en F6-bank från den andra sorterade X-platsen. Utöver de tre ändrade X-lägena i tabellen har första X kvar sitt mätta värde 19. Första X22 i senare ROM gav **REJECTED** och har inget fysiskt TIA-utfall.
- **`unified.bin`** visar en verklig kombination av andra, tredje, fjärde och femte RAM-X, exempelvis X=[133,19,76,103,49] och Y=[74,68,75,71,71] med sju raders spridning. Samma ROM klarar även [127,19,73,97,43], [136,19,76,100,52], omordning med olika originalmasker samt ett senare band. Fasfamiljerna täcker en begränsad uppsättning kombinationer. Vid X=[136,19,67,100,52] saknas motsvarande schema, vilket gav **REJECTED**. Tidigare ROM och referensbevis finns kvar.
- **`segmented.bin`** klarar den tidigare avvisade spridningen Y=[74,68,83,71,76] både på historiska X=[127,19,73,100,46] och på [133,19,76,103,49]. Det senare provet visar fyra numeriskt ändrade X och 15 raders spridning i samma ROM och bildruta. Den täta same-Y-fixturen och XY utanför fasgrupperna är **REJECTED** före raster.
- Tre separata Gopher-serier gav **600/600 PASS per ROM**, FR21–620, med sex RAM-sceningångar per serie. Alla positiva bilder hade 136/136 NPC-, 32/32 P0-, 25/25 M0- och 3047/3047 PF-pixlar med referensens exakta `(x,y,RGB)`. I den segmenterade serien ingick 200 bildrutor med 15 raders spridning, 100 vardera med historiska respektive fyra flyttade X.
- Sammanlagt gav slutmatrisen **2044/2044 ×262 scanlines**, inklusive avvisade och negativa bilder. Fryst ITER4 reproducerade tidigare fysiska tredje-X64/82-fel och tredje-X67/73/76 PASS. Alla åtta tidigare positiva ITER2/ITER3-fixturer gav 32/32 PASS på fryst `mixed.bin` i samma miljö. Den segmenterade ROM:en klarade 3/20 äldre fixturer, inklusive två tidigare avvisade seedade lägen. Resterande 17 avvisades före fysisk rasterprövning. Den nya ROM:en kombinerar de mätta förmågorna ovan inom sin fasdomän; uttömmande ekvivalens med samtliga tidigare fasbankar är **NOT_RUN**.
- Stock Stella 6.7.1 bekräftade X43 i 12/12 bilder. Stock 7.0 bekräftade de fyra ändrade X-värdena i 12/12. Den tidigare 15-radersfixturen bekräftades dessutom med 12/12 bilder vardera i stock 6.7.1 och 7.0. Stella använder dokumenterade bootkoordinater. Live-POKE och 262-logg i Stella är **NOT_RUN**.

## Segmentering och hårdvarubudget

Den segmenterade diagnostiken fyller 17 rader för alla fem slots. Vid långt band spärras övriga aktörer så att endast den sent placerade tredje sloten kan bidra efter rad 17. Dess sista sju maskbyte förladdas i samma VBLANK genom att återanvända nollrader tidigt i den tredje slotens ordinarie cache. Den sorterade indextabellens första två byte återanvänds först som maskpekare och därefter som körpekare. Delkedjan ansluts vid en rastergräns och behåller fem RESP1-faser med noll grafik på de inaktiva slotarna. Skottet släcks efter sin sista synliga pixel på Y88 och överskanningen startar på den ursprungliga raden. Det långa läget har mätt bandstart Y68 och selekterade fasbankar. Det är ingen generell strömmande cache för valfri spridning.

De första segmenterade versionerna gav 263–267 scanlines. Flytt av delmoment mellan VBLANK-rader och stackfri pekaruppbyggnad löste randöverskridandena. Ett senare försök återgav samtliga NPC-pixlar och 262 scanlines men gav 824 extra gula spelarpixlar efter läsning förbi den gamla P0-tabellens nollfält. Nollfältet förlängdes och GRP0 nollställdes vid det långa bandets slut. Två avvisningsvägar höll då fortfarande 263. Tidsloggen visade att fjärde slotens kontroll sköt över synkgränsen; uppdelad kontroll över de två befintliga pekarraderna gav 262 även i de negativa slutproven. ROM:ar, bilder och/eller direkt bildloggar för mellanproven finns i råarkivet.

| ROM | RIOT inklusive stack | Rastreviderade paket | Max CPU/rad | Minsta lediga bankssvans före F6-hotspots |
|---|---:|---:|---:|---:|
| left | 92/128, SP=$FD | 187 | 76 | 157 byte |
| unified | 122/128, SP=$FD | 187 | 76 | 413 byte |
| segmented | 126/128, SP=$FF | 150 | 76 | 666 byte |

Varje ROM är standard F6/NTSC, 16 384 byte. Binärauditen täcker 524 radpaket, exakta TIA-skrivcykler, sidgränser och noll överhäng efter 76 cykler. Stackdjupet lästes via Gophers CPU-kommando vid pekaruppbyggnadens högsta användning. I långprovet mättes cache-radernas sista WSYNC-inträde som senast CL148 (c72, plus 3 cykler för WSYNC), slutlig blankning vid SL35 CL142 och avblankningsvägens start vid SL36 CL−47. Delkedjan började SL121 CL−68 och slutade SL128 CL−68, sju fysiska rader. Overscan började SL228 CL−56. Gopher rapporterade 262 scanlines i båda långa X-varianterna.

Z3 4.15.4 gav 28 SAT och 7 UNSAT i den begränsade fasmodellen. Exakta strob-/instruktionsfönster och operandlivslängder finns i koden och solverloggen. Den gamla X64/X82-kontrollen visar varför modellutfall och faktiska pixlar redovisas separat.

## Bygg, mät och verifiera

- `left.bin` SHA-256 `9c6d92a72212a7e07a38480c0213a8fe555ac68c2a2f07f6591c5fed5d4f0110`
- `unified.bin` SHA-256 `50c3615e92f94d7ba897409fd0a9819ea5014dad8f022aa7d1551f75b77bfabd`
- `segmented.bin` SHA-256 `ef62f4a582a16b9ee3152b6e223ce2a2e5ea25876e120c676a56587862263f97`

DASM 2.20.14.1 byggde varje bank. Gopher2600 v0.57.2 mätte NTSC, POKE/PEEK, strålfas och stack. Stock Stella 6.7.1/7.0 gav originalbilder. Python/Pillow verifierade de fysiska bildpixlarna per mask och RGB. Versioner och verktygshashar ligger i `evidence/brief/tools.txt`, kommandoutdata i `evidence/brief/dasm.log` och alla filhashar i `SHA256SUMS`. [G5AR](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [G5BB](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

Kör från `experiments/g5be_iter5`. `matrix.tsv` innehåller individuella X/Y och klassificering. Score-JSON innehåller maskvis och radvis diff samt RGB. Råarkivet har PTY-kommandon, svar och originalbilder.

```bash
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
out=$(mktemp -d)
python -m venv "$out/z3"
"$out/z3/bin/pip" install -r requirements.txt
"$out/z3/bin/python" schedule.py > "$out/solver.jsonl"
cmp solver.jsonl "$out/solver.jsonl"
python build.py
python build.py --name unified --unified --rows 17
python build.py --name segmented --unified --rows 17 --segmented
python audit.py | cmp - evidence/brief/cycles.jsonl
python banks.py | cmp - evidence/brief/banks.jsonl
ref=evidence/reference
python beam.py "$ref/outer.bin" --baseline > "$out/historical-beam.jsonl"
python beam.py roms/left.bin > "$out/left-beam.jsonl"
python beam.py roms/unified.bin --stack-only > "$out/unified-stack.jsonl"
python beam.py roms/segmented.bin --stack-only > "$out/segment-stack.jsonl"
python ram.py left "$out/left-beam.jsonl"
python ram.py unified "$out/unified-stack.jsonl"
python ram.py segmented "$out/segment-stack.jsonl"
python phase.py roms/segmented.bin --fixture original-far-y > "$out/tail.jsonl"
for spec in left:left left:left-soak unified:unified unified:unified-soak \
            segmented:unified segmented:seg-soak segmented:legacy; do
    rom=${spec%:*}
    group=${spec#*:}
    tag="$rom-$group"
    python replay.py "roms/$rom.bin" "$out/$tag" --group "$group" > "$out/$tag.jsonl"
    python score.py "$out/$tag" "$ref/frozen-gopher-y76.png" --ref-height 214 \
        --log "$out/$tag.jsonl" > "$out/$tag-score.jsonl"
done
python build.py --name segment-bootfar --unified --rows 17 --segmented --boot-far
bash capture_stella.sh roms/segment-bootfar.bin "$out/stella671" 563
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash capture_stella.sh roms/segment-bootfar.bin "$out/stella70" 564
python score.py "$out/stella671/images" "$ref/stella-671-frozen.png" --far
python score.py "$out/stella70/images" "$ref/stella-70-frozen.png" --far
```

**Till MAIN X:** Den andra vänsterplatsen och det specifika 15-radersbandet är demonstrerade inom spelvisionen. Första sorterade platsen X19 och tätare X-faser är nästa tekniska avgränsning. Fri X/Y är ännu **FAIL som acceptanskrav**. Oberoende Verification II är **NOT_RUN**. `G5_FORMAL_OPEN` kvarstår.
