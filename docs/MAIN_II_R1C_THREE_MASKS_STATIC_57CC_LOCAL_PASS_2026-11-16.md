# MAIN II R1c – tre OLIKA originalmasker samtidigt på samma Y: static 57 CC LOCAL PASS

Datum 2026-11-16. **Egenkontrollerad forskningsdiagnostik, inte R1 full PASS och inte oberoende VERIFICATION.**

## Reproducerbar byggning och verklig Stella-körning

- [GitHub Actions SUCCESS #43785836805](https://github.com/Odourman/let-me-out/actions/runs/43785836805)
- Testad GitHub-commit: `c6096cba4e41654104369e9d859c455c43dc567b`; forskningsgren `research/main-ii-r1c-three-masks-57cc-20261116`.
- Artifact ID `14189798683` (`main-ii-r1c-three-masks-57cc-evidence`), innehåller DASM-källa, list/symboler, rå Stella 6.7.1 skärmbild, fem PC-stopp och `evidence/audit.json`.
- ROM standard NTSC F6, **16 384 byte** (fyra upprepade 4KB-banker), SHA256 `da8a360fc9f3db149d1dc12f9b29ef10c4b2220328395b338083839534425da1`.
- Tre **orörda** källmasker från `main/design/NPC_REFERENCE_8x9_masks.json`, blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`: `large_male`, `large_female`, `small_male`. Liten man har 9 maskrader varav ursprungligen tomma rader, dessa är inkluderade i pixeljämförelsen.
- Stella X11 råbild, scanlines=262, P0 gul och M0 gult skott synliga, inga extra vita pixlar utanför de tre originalmaskerna.

## Exakt maskjämförelse i verklig Stella-skärmbild

| Figur | Stella-debugger X (1366x900) | Matchning |
|---|---:|---|
| Stor man | 166 | 72/72 bitpositioner |
| Stor kvinna | 280 | 72/72 bitpositioner |
| Liten man | 394 | 72/72 bitpositioner |

`audit.py` validerar pixelmönstren direkt från rå Stella X11-skärmbild; tar även med originalets transparenta rader, spelaren, skottet, oönskade vita pixlar och NTSC HUD. Resultat `LOCAL_PASS_STATIC_THREE_DISTINCT_MASKS`.

## Verkliga Stella PC-stopp (frame 13, scanline 119, F6 bank 0)

| Instruktion FÖRE exekvering | PC | CPU-cykel | TIA-färgklocka |
|---|---|---:|---:|
| `STA RESP1` första | `$F088` | 23 | 69 |
| `STA GRP1` byte till stor kvinna | `$F08F` | 33 | 99 |
| `STA RESP1` andra | `$F096` | 42 | 126 |
| `STA GRP1` byte till liten man | `$F09D` | 52 | 156 |
| `STA RESP1` tredje | `$F0A4` | 61 | 183 |

Två intervall om **19 CPU-cykler = 57 färgklockor**. Värden mäts FÖRE respektive instruktion, inte efter TIA-registret skrivits. Statiskt beräknat slutar tredje `STA RESP1` c64, `DEY+BPL` c69 och efterföljande `STA WSYNC` c72, vilket lämnar cirka 4 cyklers marginal på 76-cykelsraden i just detta schema. Marginalen är begränsad och ingen PF-rendering ingår.

## Bevarat viktigt negativt prov

Den första 54-CC-varianten i [Actions #43785579266](https://github.com/Odourman/let-me-out/actions/runs/43785579266) hade stor man 72/72, liten man 72/72 men stor kvinna **71/72** (bitmaprad `$FF` visades `$FE`). Ökad väntan via två `BIT FRAMELO`-instruktioner (3 cykler vardera i stället för 2-cykels NOP) återställde saknad pixel. Förklaringen "för tidig andra `GRP1`-omskrivning" är sannolik, men saknar gate-nivåverifiering.

## Begränsning och nästa grind

**Endast tre STATISKA figurer**, ett fåtal Stella-rutor; ingen individuell fri X, inga 600 sammanhängande bildrutor, ingen 4–6 NPC-uppskalning, inga väggar/PF, ingen R2-nyckel/O1 eller riktig konsol. P0 är temporär spelargrafik. Slutligt R1 står fortsatt BLOCKED tills alla sex med fri X visas och oberoende verifiering godkänner.

`main`, PR #7 och äldre oberoende VERIFICATION Issue #8 har inte ändrats. Ingen ny implementation cutover eller fullspel auktoriserad.
