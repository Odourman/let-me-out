# TO_MAIN_G5BD_ITER3 · LM-D36 · ROM DEVELOPMENT IV → MAIN IX

**`G5BD_ITER3_LOCAL_PHYSICAL_CONFLICT_OBSERVED` · 18 november 2026 · DEVELOPER_OBSERVED**

Den historiska omordningen är fortfarande **FAIL**. P0-delning gav två verkliga förbättringar. P0 kan återge F i den vita andra kopian samtidigt som spelarens, skottets och väggarnas positioner och RGB-värden matchar referensen. Med en fjärde mask återställd gav `shareearly` alla avsedda pixlar i fyra maskfönster, men **hela SM:s 20 pixlar saknades och en vit pixel tillkom vid SF**. `sharefour` gav **21 saknade/0 extra**, varav 20 från SM och en från F. Inget femmaskers-PASS. **G5_FORMAL_OPEN kvarstår.**

## Fryst utgångspunkt och huvudprov

Iter2:s `shadow.bin` hämtades ur `653b184d13f2504aa8bd4092b0f4b5367b787d6e`, SHA-256 `479ba85f24c3d31345cf378baf1ca225229849a520add18e6524a2099888b2f7`. Historisk omordning X **127/19/73/100/46**, Y **73/72/73/71/72**. Maskfilen jämfördes byte för byte mot `design/NPC_REFERENCE_8x9_masks.json`. Alla fem aktörers XP/YP skrivs och läses i RAM. POKE/PEEK bekräftade alla tio byte före/efter huvudprovet. Exakt fysisk pixelunion och unika bitar redovisas separat.

| ROM | Synliga unika pixlar per ID M/M/F/SM/SF (av 28/28/38/20/22) | Saknade/extra vita | M0 gula | Radcykler |
|---|---|---:|---:|---:|
| Fryst `shadow`, upprepad referens | 28/0/38/0/22 | 48/0 | 25 | 66 |
| `latch4`, P1-hybrid med riktade latchöverföringar och vänster M | 28/28/18/0/22 | 40/4 | 25 | 72 |
| `sharep0`, P0:s andra kopia och M0-spärr inom bandet | 28/0/38/0/22 | 48/0 | **27** | 76 |
| `shareclean`, dessutom spärr på bandets båda kanter | 28/0/38/0/22 | 48/0 | 25 | 76 |
| `sharefour`, förladdning av F över radgränsen och fyra maskfönster | 28/28/37/0/22 | 21/0 | 25 | 76 |
| `shareearly`, tidigare M0-spärr och F-aktivering | 28/28/38/0/22 | 20/1 | 25 | 76 |

Alla rader är **FAIL** för hela omordningen. Alla kortprov gav samma pixelutfall i 3/3 Gopherbilder samt 12/12 GUI-bilder vardera i Stella 6.7.1 och Stella 7.0. Alla Gophers huvudprover hade 262 scanlines. För jämförelse har den frysta femslotsreferensen `phaseprobe` fortfarande alla fem synliga med **5 saknade/20 extra**. Ingen tidigare kandidat skrivs över.

## A · Latchpipeline och fyra P1-strobar

Analys av fysiska originalrader visade **fem aktiva maskbyte på samtliga Y74–78**. Runt dem finns rader med färre aktiva byte. Y71 är tom. Y72 har en aktiv mask, Y73/Y79 har fyra, Y80 tre och Y81 två. Att dela upp enbart tomma rader löser därför inte kärnkonflikten.

`latch4` förbereder 24 **radvisa SF-byte i RIOT** efter att strobklockorna har konsumerats av emitteraren men innan det synliga bandet börjar. Nollbyte ger tom rad. Den provade loopen strobade också på tomma rader. Dynamisk inställning av en full händelseplan för alla fem aktiva maskbyte **NOT_RUN**. Vid Y74–78 finns ändå inget tomt maskfönster att använda i det historiska fallet.

Med X som bärare av korrekt P0-byte skrev `latch4` P1:s nya mask i c16/34/47/61 och överförde den med GRP0. RESP1 låg på c22/31/40/58. Vänster M återkom med 28/28 och SF och höger M var fortsatt exakta. F:s nya byte anlände senare och transfern c50 kostade 20 F-pixlar och gav fyra extra vita pixlar i scenen. Jämfört med Iter2:s 66-cykel-`shadow` använde fyrslotaren 72 cykler. Fyra återstående cykler räcker varken för SM:s indexerade maskläsning, strob och latchöverföring eller för att återställa F:s tidigare transfer inom just denna kedja. Det är en lokal begränsning för de uppmätta schemana.

Första provbygget avbröts när PEEK fann ändrade koordinater. Radcachen hade skrivits innan strobklockorna i samma RIOT-region konsumerats. Det bygget är sparat som negativt råbevis med ROM och källsnapshot i arkivet. Ingen pixelpoäng tilldelades. Efter rättad livstid passerade PEEK/återläsning och audit för `latch4`.

## B · P0/P1-resursdelning och exakt färgkontroll

P0 har sin ordinarie gula första kopia vid X9. NUSIZ0=`$04` gör en andra kopia vid X73. Provvägen kan bara välja NPC vars RAM-X stämmer med den fysiska kopian. F är aktören där i historisk omordning. P1:s andra deadlines sätts av strobklockorna och maskpekare beräknas från individernas Y. Varken hela X-vektorn eller F-identiteten slår på vägen. Det testade fönstret är snävt och ingen generell positioneringsmetod.

- I `sharep0` gav vidkopieringen också två extra gula M0-pixlar vid **(66,63)** och **(66,88)**. Mitt i bandet var M0-spärren korrekt. `shareclean` spärrade även vid första och sista raden. Den behöll det ordinarie 25-pixelsskottet, tog bort båda dubletterna och återgav SF/F/höger M exakt.
- `sharefour` förladdade F:s nästa radbyte i X och återställde vänster M via P1. F:s breda rad vid Y76 saknade X73. `shareearly` flyttade F:s GRP0 från **c47 till c46**, behöll F:s begärda X/Y och återställde biten. Den senare SF-uppdateringen vid **c38** gav samtidigt en vit extra pixel **(46,75)**. SM är avsiktligt helt utelämnad i båda fyrfönsterproven.
- `shareearly` skrev ENAM0=0 på c27, COLUP0=`$0E` på c43, och återställde gult med `$1E` på c63 samt ENAM0 på c67. RESP1 c22/31/58 och GRP1 c16/38/53 är loggade. M0:s gula tidiga stråle var redan visad innan färgbytet. CPU-store och synliga rasterpixlar är mätta. Internt TIA START och komplett latch-/serializerförlopp är **NOT_DETERMINABLE**.
- RGB-oraklet jämförde faktiska (X,Y,RGB)-mängder mot respektive emulatorversion av fryst referens. För `shareclean`, `sharefour` och `shareearly` var **P0 32, M0 25 och PF 3047 exakt matchande pixelpositioner och färgvärden** i Gopher och båda Stella-versionerna. Ingen generell P0/M0-färgkompromiss godkändes.
- I detta förlopp återstår c46→c49 för SM:s önskade strob. Om stroben emitteras vid c49 följd av ett ROM-radbyte och GRP1, blir skrivslutet tidigast c56. Höger M:s c58-strob måste redan ha börjat c55. Utan annan förladdnings- eller fysisk kanalplan kan båda inte inkluderas här. De ordinarie färg-/projektilrestaureringarna och nästa rads F-cache fyller resten av radbudgeten.

## Regression, resurser och faktisk verktygsanvändning

`latch4`, `sharefour` och `shareearly` behöll 8/8 tidigare positiva familjer och 12/12 positiva G5BC-seedlägen. Tre av tolv Iter2-omordningar förblev PASS, de övriga är i respektive råmatris. Seed-dense 0/4. X19/20/21 mättes med samma tidigare 0/0, 13/13 och 13/13. Historiskt separerat 0/0, close3 76/28, close1 37/28 och mixed same-X 42/0. Full fri helskärmspositionering, nya seedordningar efter den befintliga Iter2-matrisen, R2/S05 och fysisk maskin **NOT_RUN**. Villkoret för bred femmaskersvalidering uppnåddes aldrig.

`sharefour` gav **600/600 exakta poängsatta bilder** i den separata gamla positiva grenen. 608 sammanhängande Gopher-avläsningar inklusive åtta övergångar, samtliga 262 scanlines. Max 0 helt osynliga NPC där. Långkörningen styrker bevarade fungerande fixturer. P0-delningens historiska omordning har separat 3+12+12 kortprover, fortsatt FAIL.

DASM 2.20.14.1 byggde fem nya 16 KiB F6-ROM, fyra identiska banker vardera. Audit av faktiska RAM-byte gav 53 byte i latch4 och 58 byte i P0-varianterna, inom 64-byte-reserven. Inga indexerade sidkorsningar vid Y0–23 i de auditerade raderna. RIOT-budget **128 B** = 1 bildräknare +10 X/Y +5 sortindex +16 arbetsbyte +24 delad cache/komposit +64 kod +8 stack. Max 6 stackbyte i emitterarnas tre JSR-nivåer. Stella 7.0 mätte 69×3 från $BA till $B8 i latch4 (72 inklusive WSYNC) och 73×3 från $BA till $EF i sharefour/shareearly (76 inklusive BNE). Stella-fällor och Gophers registerspår är sparade separat. Gopher2600 v0.57.2 gav 2 success/0 fail på två 30-frame positiva bootbaslinjer med oförändrad databashash. Live RAM- och pixelbevis är separat.

En vidare arkitekturavstämning kan utgå från en gemensam per-rad-plan med P0-delningen och oberoende förladdning av SM och höger M. Kräv på nytt färg-/projektilbevis på de fem fullt aktiva raderna. Dessa prov ger ingen global TIA-omöjlighet och inget stöd för en flimmer- eller grafikkompromiss.

## Reproduktion

Från `experiments/g5bd_iter3` med G5AR ENV-01 och stock Stella 7.0 sidobinär från G5BB.

```bash
set -e
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
for f in bin sym; do
  git show "653b184d13f2504aa8bd4092b0f4b5367b787d6e:experiments/g5bd_iter2/roms/shadow.$f" > "roms/baseline.$f"
done
for m in baseline latch4 sharep0 shareclean sharefour shareearly; do
  python runtime_capture.py "$m" "$out/$m-png" --fixture historic-reorder > "$out/$m.jsonl"
  python measure.py "$m" "$out/$m.jsonl" "$out/$m-png" "$out/$m-pixels.jsonl"
  python row_diff.py "$out/$m-pixels.jsonl" "$out/$m-png" > "$out/row-$m.jsonl"
  python trace_runtime.py "$m" historic-reorder > "$out/trace-$m.jsonl"
done
python color_diff.py "$out" > "$out/gopher-color.jsonl"
python audit_kernel.py "$out"/trace-*.jsonl
for m in latch4 sharefour shareearly; do
  for series in cases seeded reorders; do
    flags=()
    if [[ $series != cases ]]; then flags+=("--$series"); fi
    python runtime_capture.py "$m" "$out/$m-$series-png" "${flags[@]}" > "$out/$m-$series.jsonl"
    python measure.py "$m" "$out/$m-$series.jsonl" "$out/$m-$series-png" "$out/$m-$series-pixels.jsonl"
  done
done
python runtime_capture.py sharefour "$out/soak-png" --soak > "$out/soak.jsonl"
python measure.py sharefour "$out/soak.jsonl" "$out/soak-png" "$out/soak-pixels.jsonl"
bash -x native_regress.sh roms/baseline.bin roms/sharefour.bin "$out/native"
stella7=/workspace/work/g5bb/stella7/usr/bin/stella
bash stella_debug.sh roms/latch4.bin "$out/stella7-latch4" 360 "$stella7" '$b8'
bash stella_debug.sh roms/shareearly.bin "$out/stella7-shareearly" 361 "$stella7" '$ef'
for m in baseline latch4 sharep0 shareclean sharefour shareearly; do
  timeout 25 bash capture_stella.sh "roms/$m.bin" "$out/stella-671-$m-select" 362 select
  STELLA_BIN="$stella7" timeout 25 bash capture_stella.sh "roms/$m.bin" "$out/stella-70-$m-select" 363 select
done
python measure_stella.py "$out"/stella-*select > "$out/stella-pixels.jsonl"
python color_diff.py "$out" --stella > "$out/stella-color.jsonl"
```

Detta är utvecklarens egenkontroll. Iteration 3 stannar här för MAIN IX:s mottagningsgranskning.
