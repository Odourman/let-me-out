# LET ME OUT! – MAIN III: R1h rasterrevision och R1i-feasibility (ENDAST RESEARCH)

**Datum:** 2026-11-16  
**Bevisnivå:** Statisk, av den faktiska DASM-listningen reproducerbar cykelanalys + rådgivande nästa rasterhypoteser. **Ingen ny ROM har byggts, startats eller verifierats inom R1i.** R1h förblir lokalt delbevis; full R1 är FAIL/BLOCKED.

## 1. Källor och källordning

1. GitHub `main` commit `f6b3fc76c59161e04e583dc8c0787332d2f261c7`: `docs/ROM_GATE_V018_SCOPE.md`, `ACCEPTANCE.md`, `BLOCKERS.md`, R1–R4 och förbud mot att tolka forskning som ny kodorder.
2. GitHub Actions [#43821560463](https://github.com/Odourman/let-me-out/actions/runs/43821560463), testad R1h-commit `3e5b79fd0409a7ed9f9ae381ade6ac1e66d51b32`, artefakt `14204881614`. Original `r1h_integrated.asm`, `r1h.lst`, `r1h.sym`, `evidence_600/summary.json`, 600 bildrutor. R1h-ROM SHA256 `2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39`.
3. [MAIN III:s tidigare R1h-granskning](MAIN_III_R1H_EVIDENCE_AUDIT_AND_NEXT_GATES_2026-11-16.md), med separat arkiv-/bildhashkontroll.
4. De två uppladdade forskningsfilerna `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(3).md` (SHA256 `6d45b2ba5747ee7c64a7446d5295f6f8add988386593b5662a70b700aabff28c`) och 55-sidiga `LET_ME_OUT_SAMLAD_AVHANDLING_MAIN_MED_ALLA_30_TRICK_2026-11-16(3).pdf` (SHA256 `596ee313bbbfcf3926efea61807a7b169363dd1aef994a4fc9a635877c62019f`). De är **rådgivande äldre snapshot**; deras uppgift att fyra originalmasker ännu inte var bevisade ska inte ersätta senare R1e–R1h-forskning.
5. Teknikstöd: [Atari STELLA Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) (76 CPU-cykler/linje) och [Andrew Towers TIA Hardware Notes](https://retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) (retrigger och specialfas vid exakt 18 color clocks).

## 2. Ny mätbar statisk upptäckt: nästan exakt 76-cykels tak

Ur `r1h.lst` och `r1h.sym`, på varje **tagen** BPL i de åtta första NPC-raderna:

| Nio-raders-kernel | Exekverade CPU-cykler efter WSYNC till nästa WSYNC, inklusive nästa WSYNC | Cykler kvar före 76 | BPL sidkorsning |
|---|---:|---:|---|
| R1gRowsA | **75** | **1** | **JA**, branch från `$F116` via `$F118` till `$F0E4` |
| R1gRowsB | **74** | **2** | Nej |
| R1gRowsC | **74** | **2** | Nej |
| R1gRowsD | **74** | **2** | Nej |

För den **nionde** raden tas inte `BPL`; den cykelraden är ett separat avslutsfall. Alla `LDA/LDX absolute,Y`-källtabeller är på `$F400`–`$F424` och indexeras Y=8..0 utan page crossing.

Kritiska **statiska instruktioners sluttid** efter ingångs-WSYNC (samma i samtliga varianter om inget anges):

| TIA-registerhändelse | Slut av CPU-cykel |
|---|---:|
| `STA GRP1` stor man | c7 |
| `STA GRP0` gul spelare | c14 |
| `STA COLUP0` gul färg | c19 |
| `STA RESP1` stor man | c26 |
| `STA RESP0` spelare | c29 |
| `STA GRP1` stor kvinna | c36 |
| `BIT FRAMELO` padding 1 | c39 |
| `BIT FRAMELO` padding 2 | c42 |
| `STA RESP1` stor kvinna | c45 |
| `STA RESP0` vit liten kvinna | c48(A), c51(B), c53(C), c56(D) |
| `STA COLUP0` vit färg | c56 |
| `STA GRP1` liten man | c63 |
| `STA RESP1` liten man | c66 |

**Varning:** Dessa är assembler-/6502-cykeltider, **inte** observerad TIA registerbusstid, en exakt visible-X-mappning eller bevisad ny spriteposition. Ytterligare `STA RESP1` kostar 3 cykler; rutinerna har bara 1–2 cykler marginal. En fjärde P1-figur kan därför inte adderas naivt i den nuvarande sekvensen.

## 3. R1i-A: ny tvåaxlig rörelse via 3-cyklers PERMUTATION, inte fler instruktioner

Alla fyra R1h-kärnor innehåller exakt två `BIT FRAMELO` (zero page, 2 byte, 3 cykler) mellan `STA GRP1 FemaleRows,Y` och andra `STA RESP1`. En `STA RESP1` (zero page, 2 byte, 3 cykler) har **samma längd och cykelkostnad**.

Därför kan den **BEFINTLIGA** kvinnliga P1-resetinstruktionen, som forskningshypotes, permuteras mellan följande tre 3-cykelplatser, utan att flytta nästa `STA RESP0` eller den tredje P1-masken:

| Females P1 reset-sluttid | Nominell förskjutning från R1h, *inte emulatorbevis* | Gap från första P1-reset | Gap till tredje P1-reset |
|---|---:|---:|---:|
| **c39** | −18 CC | 39 CC | 81 CC |
| **c42** | −9 CC | 48 CC | 72 CC |
| **c45** | 0 CC | 57 CC | 63 CC |

Det är i teorin möjligt att välja **två** av dessa lägen för den stora kvinnan, samtidigt som R1h redan väljer fyra lägen för den lilla kvinnan via P0. Med två extra unrollade versioner av de befintliga fyra P0-ordningarna blir resultatet **8 fasstyrda, lika långa loopar** (4 P0-lägen ×2 P1-lägen). Om kvinnoläget väljs med en separat framebit och dörren fortsatt med sin egen bit, skulle 4×2×2=**16 olika X-/dörrkombinationer** kunna provtas under en 600-frame-sekvens.

**ROM-kostnad, statiskt:** De nuvarande fyra kärnorna är var och en 57 bytes (fysiskt `$F0E4..$F1C7`). Fyra ytterligare 57-byteskärnor kräver **228 extra bytes**. R1h:s sista körbara byte ligger i området `$F1F1` och bitmaptabellerna börjar `$F400`, alltså är ROM-placering **teoretiskt möjlig** utan att flytta masker. Den utökade dispatch-koden, eventuella page crosses, blanking och framtida full-R1-kod är **inte** budgeterade/byggda: detta är endast en platsindikation, inte kodleverans.

**Hård stoppgrind:** Inget c39/c42-läge får kallas fungerande förrän en separat auktoriserad Stella-ROM visar alla ursprungliga masker med 0 skuggpixlar, oförändrad spelare/fjärde NPC/dörr och uppmätta verkliga positioner. Viktigast att kontrollera om P1-kopians counter/latch faktisk förskjuts eller försvinner när reseten flyttas.

## 4. R1i-B: femte androiden med ett enda ytterligare P1-reset (MER OSÄKER)

En alternativ **forskningstanke, inte kodbevis**, är att ersätta *första* `BIT FRAMELO` med *ytterligare* `STA RESP1` (båda 3 CPU-cykler). Eftersom `FemaleRows,Y` laddas till `GRP1` vid c36 skulle då två P1-återutlösningar med **samma oförändrade stora kvinnomask** ske vid c39 och c45, 18 CC isär, utan mer CPU-tid.

Om **och endast om** båda grafikkopiorna syns kompletta inom samma nio rader och originalmaskerna bevaras, skulle R1h kunna visa **fem** vita NPC (1 stor man, **2 stora kvinnor**, 1 liten man, 1 liten kvinna) och gul spelare. Men den **andra stora mannen saknas** och kopiorna är fortfarande inte fritt positionsbara.

TIA-noterna beskriver just 18CC som en särskild retriggergräns där föregående start kan förskjutas +2 CC; därför behövs nytt verkligt Stella-bevis för båda kompletta bitmapparna och deras exakta X. En andra enkel utbyte av sista `BIT` skulle bara lämna 9 CC mellan två resetar och får **inte** antas fungera.

## 5. Forskningsordning och skydd mot falska PASS

1. **R1i-A först:** kartlägg 2 (sedan 3) P1-kvinnolägen mot 4 P0-kvinnolägen, intakta R1h-väggar, dörr, testskott och gul spelare. Varje position ska vara faktiskt observerad och inte bara ändrad timingvariabel. För detta steg krävs tydligt avgränsat nytt kod-/testuppdrag om det ska bli exekverbar ROM.
2. **R1i-B endast separat efter TIA-review:** byt ett BIT mot P1-strobe och kontrollera om verkligen **fem** oförändrade 8×9-maskar visas; mät eventuellt +2CC-fasfel. Misstolkas inte som fri X.
3. **Full-R1-grind:** återstår ytterligare en stor man samt **alla sex oberoende och generellt rörliga X**, näraöverlapp, aktiv spelarrörelse, M0 i samma höjdband, fulla väggar, R2-nyckel/O1 och orange/svart dörr. Nuvarande isolerade bevis har ingen sådan PASS.
4. **Mät med riktig Stella**: PC, bank, scanline, `_sCycles`, TIA-register, ROM-SHA, råa originalbilder per frame och fallerade minst 600 frames. Reproducera inte tidigare felaktig `break; frame; step`-sekvens. Registercykler i denna rapport ska inte förväxlas med busstrace.
5. **Bevara beslut och oberoende verifiering:** Inget merge till `main`, inget ROM DEVELOPMENT-PR #7-merge, ingen övertagning av VERIFICATION Issue #8, ingen PAL eller specialcart. De 30 gamla trickens 27–30 är inte tillåtna F6-implementationer.

## 6. Slutsats

**Reell ny forskningsmöjlighet:** Vi behöver inte nödvändigtvis öka antalet CPU-cykler för att ge **en andra NPC ett separat dynamiskt X-läge**. De två 3-cykels padding-slotsen på P1 låter oss i teorin omordna befintlig strobe och därefter pröva 4×2 positionskombinationer. Det finns också en spekulativ och strikt separat möjlighet att visa **en femte originalandroid** via en extra 18CC P1-retrigger utan mer cykelbudget. Ingen av dessa teser är ännu en fungerande ROM eller en lösning på sex fria android-X.

**Status:** `R1 = FAIL/BLOCKED`, `R1h = LOCAL_PASS within limited scope`, `R1i-A/B = STATIC RESEARCH ONLY`.
