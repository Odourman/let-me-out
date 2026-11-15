# Let Me Out! – ROM DEVELOPMENT v0.18, SEX_X_FREE, faktisk Stella-evidens

**Datum:** 2026-11-15. **Utvecklarens egenkontroll – inte oberoende VERIFICATION.**

**Scope:** Endast NTSC-diagnostik v0.18 (förberedande R1 inom R1–R4); repo `Odourman/let-me-out`, arbetsgren `rom-dev/v018-ntsc-diagnostic`, PR #7 utkast. Den frysta verifieringsbaslinjen `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` och dess ROM är **inte** ändrade.

## IMPLEMENTERAT

Två fristående, reproducerbara originalskrivna 6502-kandidater för samma R1-stress med sex separata logiska X-positioner i RIOT RAM `$90`–`$95`: initialvärden **16, 36, 56, 76, 96, 116** färgklockor. Varje android följer ett individuellt deterministiskt 32-positionsmönster (upprepas); typerna är stor man, stor man, stor kvinna, stor kvinna, liten man, liten kvinna, med fyra *oförändrade* original-8×9-masker. Gul spelarkandidat i P0 (nio synliga pixelrader), M0 testskott. Spelaren och skottet har egna RAM-positioner `$87`–`$88`, men just detta stresstest animerar inte deras koordinater.

A: P1 visar en **(1)** exakt originalandroid per frame; valet roterar genom alla sex. Oberoende X styr RESP1/HMP1/HMOVE. Ingen NPC borttagen ur logiskt tillstånd. **Diagnostisk avsikt, inte en designwaiver.**

B: Asymmetriska PF0/PF1/PF2-register skriver förberäknad 4-färgklockorsgrova kroppar på samtliga sex individuella X. En originalmask per bildruta visas dessutom med P1. VBLANK kopierar 54 PF-bytes från ROM till RAM (`$A0`–`$D5`) för aktuellt rörelsesteg. Detta är en hybrid av ett ofullständigt grovt synligt underlag och en exakt sprite. Originalmasker ersätts **inte** i den kanoniska grafiken.

## BYGGT

DASM: Ubuntu 24.04 paket `2.20.15~20201109+really2.20.14.1-2` (DASM-motor 2.20.14.1). Stella: `6.7.1+dfsg-1build2` (Stella 6.7.1). Båda: **16 384 byte, F6 med fyra identiska 4 096-byte-bankkopior**, därför ingen extra TIA-kapacitet genom bankning.

- Kandidat A `.bin` SHA-256: `677cbeb59f09f3b8dcb55cc89059a55f0c4878e5049e72c3ea0d60c9a79002e1`.
- Kandidat B `.bin` SHA-256: `f06c235e808e24ce370e8d00165c4daff5ded37ccce2c09f4a84d494c7f4f18c`.

Originalens verkliga DASM `.lst`, `.sym` och byggloggar finns i källartefakten. `build.sh` validerar att fyra kB ger exakt 16 kB och `sha256sum -c` kontrollerar byggda filer. Källor och ROM i denna ZIP är byte-identiska med GitHub Actions-körning **43759690033**.

## TESTAT I STELLA – 600 sammanhängande bilder PER teknikspår

GitHub Actions-körning: https://github.com/Odourman/let-me-out/actions/runs/43759690033 . Bildrutor **11–610** för A respektive B, inspelade från Stella Debugger under Xvfb efter 600 *separata* `Frame +1`-kommandon. Originalevidens är exakt **1 200 råa GUI-PNG-filer** i oförändrad Actions-artefakt, som ingår som kapslat arkiv i ZIP. Beskurna bilder märks uttryckligen `CROPPED`.

En reproducerbar analys av riktiga skärm-pixlar registrerade bildnummer och `_scanEnd`-HUD-mätaren i varje original-PNG. Kalibrering: Stella-kända `262`-HUD-pixlar matchas exakt mot en kalibrerad referens; **inga avvikande eller okända scanlineindikatorer klassas automatiskt som 262.** Detta är **emulatorns visade efterföljande bildrutans antal scanlines**, inte en individuell registerwrite-/CPU-cykeltrace. Inga stillbilder eller Python-simuleringar ersätter emulatorbeviset.

| Mått | A: tidsmultiplexning | B: PF/P1-hybrid |
|---|---:|---:|
| Verkliga infångade bildrutor | 600 | 600 |
| Bildrute-ID 11–610 utan luckor | 600/600 | 600/600 |
| Med faktiskt visade `262` scanlines | 600/600 | 600/600 |
| P0 gul spelare observerad | 600/600 | 600/600 |
| M0 testskott observerat | 600/600 | 600/600 |
| NPC 0, stor man | 100/600 | 600/600 |
| NPC 1, stor man | 100/600 | 469/600 |
| NPC 2, stor kvinna | 100/600 | 449/600 |
| NPC 3, stor kvinna | 100/600 | 549/600 |
| NPC 4, liten man | 100/600 | 600/600 |
| NPC 5, liten kvinna | 100/600 | 600/600 |
| Max osynlig följd per NPC | 5 frames | 0–5 frames |
| Exakt 8×9-mask | 72/72 för varje A-android när synlig | i regel ej; medel 47–59/72 i approximativ avläsning |

**Metodbegränsning:** B:s `visible`-mått söker separata vita pixelgrupper nära begärd X. Överlappningar och 4-färgklockors kvantisering kan feltolkas; resultatet är en **utvecklarmätning**, inte en oberoende, manuell full kvalitetsgranskning eller garanti om objektets exakta synlighet. CSV visar både begärd och uppmätt X där sådana kunde utläsas. Några B-bilder kan visa PF-blobs på samma plats som P1-spriten.

**Teknik A FAIL:** exakt silhuett men bara **1/6 av bildrutorna per android**, fem följande bildrutor osynlig. Cirka 10 Hz synlighetscykel vid 60 Hz. Det uppfyller inte kvalitetsmålet om begränsat flimmer.

**Teknik B FAIL:** sex samtidiga logiska figurer och grova PF-kroppar, men **inte fyra tillförlitligt identifierbara människoliknande 8×9-silhuetter**. Endast en per bildruta använder exakta P1-8×9-källmasken. Att bocka av sex vita figurer på skärmen vore missvisande.

## Hårdvaruresurser, RAM och cykler

- TIA: P0 = spelaren, M0 = skottet, P1 = en exakt android, PF0/1/2 = ytterligare grova kroppar (endast B), P0-missiler/BL/P1-missil oanvända i R1. NUSIZ-kopior ger inte fria X-positioner.
- RAM A: `$80`–`$8A` ramregister plus `$90`–`$95` sex NPC X. B lägger dessutom 54-byte PF-cache `$A0`–`$D5`; standard RIOT 128 bytes tillåter detta. Inga extra RAM-objekt antagna.
- **Statiskt beräknad** A-scanline-rutin: omkring 30 6502-cykler inklusive start-`WSYNC`. **Statiskt beräknad** B-scanline: omkring 67–70 6502-cykler inklusive följande `WSYNC`. Den exakta TIA-skriv-/cykelpositionen har inte mätts i Stella Debugger, så det är inte acceptans för T07.
- Bildväxlingstabeller och sex logiska positioner uppdateras under VBLANK, inte i den kritiska synliga rutinen. R2 skulle kräva P1 för guldnyckeln, vilket **ökar** hårdvarukonflikten; inget R2-steg implementerat i denna nya experimentkod.

## FAIL / INCONCLUSIVE / BLOCKERAT

1. **R1/FULL – FAIL:** Ingen av de två prövade arkitekturerna uppfyller både sex samtidigt läsbara humanoider med individuella X och begränsat flimmer.
2. **R2/R3/R4 – NOT_RETESTED:** Enbart R1-provet är nya kodens scope; äldre diagnosdata är historiska och får inte överföras som PASS.
3. **T01 – INCONCLUSIVE i hela v0.18:** 600/600 scanlineindikatorer finns för vardera ny R1-kandidat, men inte alla godkända testscener eller explicit individuell TIA-registerwrite-trace/VSYNC-beteende.
4. **T07 – INCONCLUSIVE:** ingen komplett mätt per-register cykel-/scanlineposition; statisk beräkning separat redovisad.
5. **T15 – NOT_RUN:** kräver oberoende VERIFICATION för ny commit. Fryst baseline i Issue #8 förblir oförändrad.
6. **T14 – lokal PASS för dessa teknik-ROM:** riktig DASM, två reproducerbara 16 kB F6-binärer, SHA-256 i bilagt manifest. Inte oberoende verifierad.
7. **T16 – lokal PASS:** ändringar ligger bara i Let Me Out!-projektet, inga kommersiella ROMs inkluderade. Separat VERIFICATION ska kontrollera själv.

## Slutpunkt för teknikspåren

**A tidsmultiplexning** ger endast en av sex på varje bildruta och **B PF/TIA-hybrid** ger inte godkända 8×9-silhuetter. Bägge av de maximalt två auktoriserade teknikspåren är därmed **blockerade i dessa implementerade former**. Detta är inte ett teorem att ingen framtida Atari 2600-teknik kan lösa problemet. Däremot får ROM DEVELOPMENT inte tyst minska sex androider, förenkla originalets fyra masker eller ändra spelmekanik. MAIN får avgöra om ytterligare riktad teknikforskning inom v0.18 ska prioriteras, och ett eventuellt visuellt kompromissbeslut kräver uttryckligt godkännande.

**Commit-baseline:** `f5c06f352ba8653f3ce65bbc3e5e392c892beec5` före detta SEX_X_FREE-deluppdrag; ursprunglig fryst VERIFICATION-baslinje `561d3baf...`. **Inget nytt utvecklingssteg, ingen main-merge.**
