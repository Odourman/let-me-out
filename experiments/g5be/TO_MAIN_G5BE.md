# TO_MAIN_G5BE · LM-D37 · ROM DEVELOPMENT IV → MAIN IX

**`G5BE_LOCAL_CONFLICT_PARTIAL` · 18 november 2026**

Z3 hittade ett **SAT-schema för en förberedd fysisk rad** i P0/P1-familjen. Den genererade DASM-ROM:en bekräftade **0 saknade och 0 extra vita pixlar på var och en av Y74–78 när de kördes separat**. På Y76 visades alla fem originalmaskers radbyte exakt i Gopher och båda stock Stella-versionerna. Två alternativa RAM-ordningar och ändrat X för den fjärde sorterade sloten klarade motsvarande radtest. **Hela femfiendersscenen är fortfarande FAIL.** ROM-provet förbereder bara en vald NPC-rad per bild. **G5_FORMAL_OPEN kvarstår.**

## Modell, kalibrering och sökutrymme

Utgångspunkt `c271d66a4bea16b78a7d43d7d48707c7d163d3e1`. Fryst `shareearly.bin` SHA-256 `20573d9c3bad3025b58d03bc65a71bf0753d91a0e7b97f9b2ab88df55742aba2`. `calibrate.py` avkodade faktiskt RIOT-instruktionsminne och jämförde 24 bussrader vardera mot fyra tidigare mätningar. Den positiva femslotskontrollen gav 0/0, phaseprobe gav 5/20, shareearly 20/1 och shadow 48/0. Dekodern återger RESP1-tider och korrekta 5/5/4/3 effektiva maskslotar. Där Gopher TRACE saknar en skrivrapport (phaseprobe c37) syns instruktionen i RAM-dekodningen. Pixelutfallen är fryst emulatorbevis. De räknas inte fram av modellen.

`schedule.py` bygger en diskret CPU-modell med beslut för instruktionernas start, A/X-registret och absolut/nollsida för skrivning. Instruktionerna får inte överlappa. Läsare måste ligga i datats livstid, och alla oanvända intervall måste kunna fyllas med hela 2- eller 3-cykelinstruktioner. Y är radindex och används som valfri data vid RESP-strob. Indexerad ROM-läsning är fyra cykler under auditens sidgräns. Immediate är två cykler, nollsidesskrivning tre, absolut fyra. Urvalet låser strobarna på de fysiska X-deadlines, med **c22/31/40/49/58** i huvudfallet. Relationen till den synliga bildklockan är `CL=3*c−68` i spåren. Registerfönstren är empiriska gränser, utan en komplett fysikalisk TIA-modell. TIA:s interna START och hela latchkedjan är **NOT_DETERMINABLE** med materialet här.

| Familj och variant | Modellsvar för historiskt X/Y |
|---|---|
| P1 med VDEL på, separat GRP1-new→GRP0 för varje mask och möjlighet att dela första transfern med gula P0 | UNSAT för fyra-cykels radläsningar och för en förberedd rad |
| P1 med avgränsat delayed-fönster för SF/F, två VDEL-skrivningar och direct för övriga | UNSAT i båda datamodellerna |
| P0:s andra kopia och fyra P1-strobar, M0-spärr, färgväxling och färgåterställning | UNSAT för fyra-cykels radläsningar. **SAT** när de fem operandbytena kan förberedas före den valda raden |
| P0/P1 som ovan, fjärde sorterade stroben vid c48 eller c50 | Båda SAT för förberedd rad |

Z3 4.15.4, Pythonpaket `z3-solver==4.15.4.0`, seed 0 och gräns 15 000 ms per konfiguration. Inga TIMEOUT/UNKNOWN. Dessa UNSAT-resultat gäller de uttryckliga register-, strob-, laddnings- och färgfönstren i koden, inklusive reserverat slut c71. De utesluter inte fler förladdade register-/cacheprotokoll, annan fysisk kopieplanering, otestade TIA-fönster eller andra sätt att mata heltalsbyte till en sammanhängande flerradskärna.

## Äkta ROM och pixelbevis

`emit_packet.py` emitterar Z3-vittnet till `packet.inc`. DASM bygger en 16 KiB standard-F6-diagnos. Före bandet väljer 6507 en tillämplig deadlinevariant (c48/49/50 för den fjärde sorterade sloten) och fyller fem immediate-operander med originalradbyte lästa från maskpekare beräknade från riktig RAM-X/Y. P0:s andra fysiska kopia kräver X73 och övriga strobdeadlinegränser gäller. Ingen jämförelse med en viss identitetsordning. Radindextestet drivs via RAM `$A8`. Andra rader visar ordinarie P0/M0 och PF genom testets omgivande kontrollprogram. Detta är en avsiktlig enradig mät-ROI, utan accepterad NPC-utestängning i en hel renderer.

| Faktiskt emulatorprov | Utfall |
|---|---|
| Gopher, historiskt X127/19/73/100/46, Y73/72/73/71/72, var och en av Y74–78 i eget prov | **15/15 exakta radbilder**. Alla fem aktiva originalbyte i varje vald rad. |
| Stock Stella 6.7.1 och 7.0, samma historiska Y76 | **12/12 exakta radbilder per version**. Y74/75/77/78 är NOT_RUN i Stella. |
| Gopher, Y76 med X19/127/73/46/97 respektive X19/127/73/46/103, Y72/74/73/70/71 | **3/3 exakta per variant**, samma ROM SHA. Dessa använder de andra två stencilerna. |
| Historisk helbild, paketet på Y76 | **FAIL, 110 saknade/0 extra**, eftersom de övriga NPC-raderna inte renderas. |

På Y76 var maskbytena i ID-ordning **FF / 18 / FF / 7E / 18** i både orakel och PNG. I alla de fokuserade Gopher/Stella-proven matchade P0, M0 och PF referensens **32 / 25 / 3047** pixelpositioner och RGB, i respektive emulator. Gopher följde Y76/SL112 med RESP1 c22/31/49/58, GRP1 c15/37/54/63, GRP0 c10/34, ENAM0 off c26/on c71 och COLUP0 vitt c42/gult c68. NUSIZ0 fyr-varianten aktiveras för provraden och rensas innan följande spelares kopia. Observerade CPU-skrivslut och bildfacit har separata filer. Stella-skärmbilder är självständiga emulatorobservationer inom utvecklarens egenkontroll. Stella-cykeltimer för enradspaketet **NOT_RUN**.

Målraden gjorde sista registerinstruktionen klar vid **c71**, följd av ett 6-cykels RTS som använder sista fem cyklerna på raden och en cykel på nästa oscorade rad. Den mätta bilden hade **262 scanlines** och ingen drift i kortproven. Audit fann **56/64** emitterade byte för huvudfallet, assembly-kontroll kräver högst 64 för varje stencil. F6 är fyra byteidentiska 4 KiB-banker. RIOT **128 B** reserverat: 1 bildräknare +10 X/Y +5 sortindex +16 arbetsbyte +24 delat scratch/komposit +64 kod +8 stack. Paketets PHA används separat från innersta JSR, reserv täcker de ärvda fallbackvägarnas 6 stackbyte. Originalmaskfilen bytejämfördes mot designkällan.

## Regression och slutsats för nästa arkitekturbeslut

- **Tidigare positiva:** 8/8 äldre familjer och 12/12 gamla seedade separerade fall består på uppmätta, ärvda vägar. Separat långregression gav **600/600 pixelrätta bilder**, 608 konsekutiva avläsningar inklusive scenövergångar, alla 262. Detta var **regression av de positiva hela bilderna**, utan 600-bilders godkännande för en ny femmaskerskärna.
- **Negativ stress:** Alla fem historiska fixtures kontrollerades. Separerat är fortsatt 0/0 och den historiska omordningen är FAIL som helbild. Den blandade körningen med aktivt paket följt av täta fall utan omstart gav dessutom **263 scanlines, och senare kortare bilder / ibland ej identifierbar P0**. Det finns därför ingen godkänd live-övergång till de täta reservvägarna. I den första kortmatrisen gav close3/close1/mixed-same-X vid 262 scanlines fortsatt 76/28, 37/28 och 42/0. Under 12-omordningsmixen fick 11 lägen 263 scanlines. Råloggar och oracle-INCONCLUSIVE för två bilder utan P0 ligger kvar i leveransen. Detta är en prov-ROM, vars scenväxling och helbild inte är leveransklar.
- **Konkret nästa steg:** Behåll det uppmätta P0/P1-paketet som mål för en radmatningsarkitektur och lös hur fem bytespecifika tvåcykelsoperander kan matas till **fem på varandra följande aktiva rader**, utan ny scendrift. Paketschemat lämnar fem cykler på raden efter sista registerinstruktionen. En vanlig refill av fem byte med indexerad läsning plus skrivning kostar minst 35 cykler. Det dokumenterar en konkret dataförsörjningskonflikt för just den här planen. P1:s mätta fullmaskväg är fortsatt bäst för flera glesare 3-pixelankrade fixturer. Fri heltals-X, tät generell geometri och en sammanhängande femmaskerskärna är **NOT_RUN eller FAIL** enligt matrisen.
- Om en senare arkitekturbedömning kräver layoutrestriktioner, tidsmultiplex/flimmer eller mask-/färgrevision måste användaren besluta om det separat. Inget sådant alternativ är implementerat här. R2/S05, fysisk Atari och oberoende VERIFICATION **NOT_RUN**.

## Reproduktion

Kör från `experiments/g5be` med G5AR ENV-01 och tidigare isolerade Stella 7.0-binären. Z3 installerades i egen venv. Ingen modifierad emulator.

```bash
set -e
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python -m venv /tmp/g5be-z3
/tmp/g5be-z3/bin/pip install -r requirements.txt
/tmp/g5be-z3/bin/python schedule.py > evidence/brief/solver.jsonl
python emit_packet.py
python build.py
sha256sum -c SHA256SUMS
python calibrate.py
out=$(mktemp -d)
for f in bin sym; do
  git show "c271d66a4bea16b78a7d43d7d48707c7d163d3e1:experiments/g5bd_iter3/roms/shareearly.$f" > "roms/baseline.$f"
done
for y in 74 75 76 77 78; do
  python runtime_capture.py packet "$out/y$y-png" --fixture historic-reorder --row "$y" > "$out/y$y.jsonl"
  python measure.py packet "$out/y$y.jsonl" "$out/y$y-png" "$out/y$y-pixels.jsonl"
  python row_diff.py "$out/y$y-pixels.jsonl" "$out/y$y-png"
done
python runtime_capture.py baseline "$out/baseline-historic-reorder-png" --fixture historic-reorder > "$out/base.jsonl"
python runtime_capture.py packet "$out/packet-packet-permuted-png" --fixture packet-permuted > "$out/permuted.jsonl"
python runtime_capture.py packet "$out/packet-latesm-png" --fixture packet-latesm > "$out/late.jsonl"
python trace_runtime.py packet historic-reorder > "$out/trace-packet.jsonl"
python audit_kernel.py "$out/trace-packet.jsonl"
for series in cases seeded reorders soak; do
  flags=()
  if [[ $series != cases ]]; then flags+=("--$series"); fi
  python runtime_capture.py packet "$out/$series-png" "${flags[@]}" > "$out/$series.jsonl"
  python measure.py packet "$out/$series.jsonl" "$out/$series-png" "$out/$series-pixels.jsonl"
done
stella7=/workspace/work/g5bb/stella7/usr/bin/stella
for m in baseline packet; do
  timeout 25 bash capture_stella.sh "roms/$m.bin" "$out/stella-671-$m-select" 380 select
  STELLA_BIN="$stella7" timeout 25 bash capture_stella.sh "roms/$m.bin" "$out/stella-70-$m-select" 381 select
done
python probe_matrix.py "$out"
python color_diff.py "$out"
python color_diff.py "$out" --stella
```

Denna leverans är utvecklarens egna mätningar och väntar på MAIN IX:s granskning.
