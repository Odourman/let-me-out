# LET ME OUT! – MAIN III: exakt Stella 6.7.1-källgranskning och åtta 6502-tidsvarianter för RESP1 + två olika P1-masker

> **MAIN:s senare verifierade forskningsuppföljning 2026-11-16:** Denna rapport var tidigare en statisk hypotes utan ny ROM. Därefter testades **R1ac → R1ad → R1ae** med verklig Stella 6.7.1. **R1ae nådde 600/600 lokalt PASS** för TVÅ fullständiga olika original-8×9-P1-masker på samma Y, fyra separat varierade X-par, gul originalspelare och en aktiv M0 utan ghost. Läs [MAIN:s senare R1ae-intag](MAIN_III_R1AE_TWO_FULL_P1_MASKS_INDEPENDENT_X_600_LOCAL_RESEARCH_PASS_DECISION_2026-11-16.md). Det ändrar INTE full R1: sex NPC och fri-X över hela spelplanen återstår, liksom oberoende VERIFICATION. Denna äldre rapport behålls som historisk statisk timinganalys; modellen är **inte** bevis i sig.

**Datum:** 2026-11-16. **Status:** `SOURCE_AUDIT_COMPLETE; STATIC_CYCLE_TABLE_VALIDATED; ROM_NOT_BUILT; STELLA_TEST_NOT_RUN; FULL_R1_BLOCKED`. Detta är MAIN:s forsknings- och beslutsunderlag, ingen ROM DEVELOPMENT-kodorder, inget VERIFICATION-godkännande. Ändra inte sex-androidkravet eller 8x9-originalmaskerna.

## Vad är nytt jämfört med MAIN:s första rapport?

Första statiska hypotesen i [MAIN:s tidigare dual-mask-kontrakt](MAIN_III_R1_RESP1_RETRIGGER_DUAL_MASK_FEASIBILITY_GATE_2026-11-16.md) använde nominella `RESP1` c30/c38 som främsta exempel. **Den modellen är inte emulatormätt och är för snäv som förstahandsvariant.** Här är en korrigerad, **cykelkostnadsberäknad** uppdelning:

- **Kalibrera först c30/c40**, som ger förväntade close-start-X cirka **39/69**, inte x39/63. Andra resetten inträffar nära beam-X52, **sex** color-clocks efter första kopians nominella sista pixel x46.
- För *oberoende* tvåpositionsvariation med större marginal: **c30/c42, c32/c42, c30/c44, c32/c44**. Dessa fyra lägen ändrar den första och andra `RESP1`-tiden var för sig med 2 CPU-cykler. Säkraste namnet är **hypotes**, inte bevis för helt fri X eller godkänd bitmap.
- c30/c38 och c32/c40 är särskilda **boundary-stress**-fall: andra resetten inträffar teoretiskt samtidigt som den första kopians sista pixel. c30/c36 är en **avsiktlig negativ kontroll** vid 18-clock-fasgränsen, inte ett obligatoriskt positivt PASS.

## Exakt verifierade källkodsfakta, från samma Stella-version som vår CI

Följande filer har öppnats genom GitHub-anslutningen **med explicit tagg `6.7.1`**, inte från Stellas föränderliga `master`:

1. [Stella 6.7.1 – Player.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx), Git blob **`af6978b9f517692b7cbeff7560466cbfd7455bf5`**: `Player::grp` uppdaterar nytt bitmapbyte direkt till aktiv rendering när VDEL inte är aktiv. `Player::resp` sätter räknarvärdet men har också en korrigering om spritekopians egen renderingssekvens just startat: `myIsRendering` samt `myRenderCounter` kan påverkas. Därför får vi inte anta att en ny reset alltid lämnar föregående spritepixelskiftning opåverkad.
2. [Stella 6.7.1 – DrawCounterDecodes.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx), Git blob **`e0b89c7c167be6c9f405b448c12b3d4b22a960b5`**: `NUSIZ1=$01` väljer närkopia via dekodtabell `myDecodes1[12] = 2`, med huvudkopiedekoder nära räknartalet 156.
3. [Stella 6.7.1 – TIA.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx), Git blob **`4c61e197fa2a4dc37c307327120319698fb41ab6`**: `GRP1` går via fördröjningskö med **`Delay::grp = 1` color-clock**, medan `RESP1` behandlas som en omedelbar strobe av P1:s horisontella position. En sen GRP-ändring kan alltså ske mellan två avsiktliga kopiestarter. Även `GRP1` kan påverka den andra spelarlatchen via `shuffleP0`, varför VDEL0/VDEL1 uttryckligen måste vara av för huvudkalibreringen.
4. [Andrew Towers – TIA Hardware Notes (2003)](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), avsnitten *The Re-trigger Trick* och *CPU Clock to Player Pixel Table*: en `close`-kopia väntas cirka **17 TIA-clock** efter en RESP-strobe, med särskilda fasfall runt 18/33 clocks. En huvudkopia utlöses inte omedelbart av resetten.

Detta är **statisk källgranskning plus en statisk 6502-cykelmodell**, INTE emulering av en ny ROM. Stellas beräknade interna bildmodell och verklig konsol måste hållas skilda.

## Fullständig, avkodningsbar kandidat på papper – c30/c40

Villkor: v0.18-originalmasker `MaleRows`, `FemaleRows`, `PlayerRows` (exakt 9 byte vardera), deras index Y i **samma ROM-page för varje index**, `ShotEnable` per originalrad, `NUSIZ1=$01`, `NUSIZ0=0`, `VDEL0=VDEL1=0`, `COLUP1=white`, `COLUP0=yellow`, vald P0- och M0-basposition förberedda under VBLANK. `WSYNC` har just släppt CPU vid scanline c0. `BPL` tas inom samma ROM-page; inga indexed-page-crossing eller cache-beroenden får ändra cykelkostnaden. OBS: detta är en **skiss**, inte körbar ROM.

```asm
RowSync:
    STA WSYNC              ; +3 on the preceding line; resumes at new row c0
Row:
    LDA MaleRows,Y         ; +4, end c04
    STA GRP1               ; +3, end c07, first mask
    LDX FemaleRows,Y       ; +4, end c11, preload second mask
    LDA PlayerRows,Y       ; +4, end c15
    STA GRP0               ; +3, end c18, yellow player
    LDA ShotEnable,Y       ; +4, end c22
    STA ENAM0              ; +3, end c25, one diagnostic M0 at later X
    NOP                    ; +2, end c27
    STA RESP1              ; +3, end c30, close #1 ≈ x39
    BIT FRAMELO            ; +3, end c33, preserves A/X
    NOP                    ; +2, end c35
    NOP                    ; +2, end c37
    STA RESP1              ; +3, end c40, close #2 ≈ x69
    STX GRP1               ; +3, end c43, new mask effective approx x62
    DEY                    ; +2, end c45
    BPL RowSync            ; +3, end c48 (taken and same ROM-page)
    ; next invocation executes WSYNC before beginning Row again
```

**Loopskalet ovan är schematiskt:** `BPL RowSync` återgår till nästa `STA WSYNC`, och `STA WSYNC` kostar ytterligare 3 CPU-cykler (c51), därefter väntar CPU till följande scanline. Den sista originalraden har otagen BPL och kräver egen säker exit. Exakt källplacering och index/page-cross måste kontrolleras i byggd DASM-listning; snutten är ingen fristående körbar ROM.

### Modellerade pixeldeadlines och varför c30/c38 är riskabelt

Använd **enbart som uppskattning** `x_close ≈ 3*c_RESP_END - 68 + 17 = 3c−51`, `x_GRP_END ≈ 3c−68`, följt av en klockas Stella-fördröjning. Exakt fas och 6502:s faktiska slutförande måste avläsas i emulatordebuggern.

- Vid c30/c40: första kopia x39..46; andra `RESP1` inträffar nominellt vid beam-x52, **6 clocks efter** första kopians sista pixel. `STX GRP1` skriver vid c43 ≈ x61 och blir aktiv cirka x62, **7 clocks före** andra kopian omkring x69..76. Detta är ett mer rimligt första test.
- Vid c30/c38: andra `RESP1` inträffar kring beam-x46, **samma tid som första kopians sista pixel**. Även om testet visar två startpunkter kan första maskens sista pixel bli fel. Därför en boundary-stress-gren, inte MAIN:s huvudrekommendation.
- Varje `GRP1`-byte i en scanline måste kontrolleras mot **alla åtta bitmapbitar**, samt att andra kopian inte är duplicerad första mask eller dolda spökpixlar.

## Åtta exakt cykelberäknade nominella varianter

All rå data ligger i [**maskinläsbar CSV, 140 schemarader**](MAIN_III_R1_RESP1_DUAL_MASK_STATIC_6502_CYCLE_MATRIX_2026-11-16.csv) på denna separata MAIN-gren. Kontrollprogrammet räknade varje instruktionens nominella cykler och avvisar avvikande förväntad `RESP1`-sluttid eller summa som går över 76. **Ingen av dessa varianter har byggts med DASM eller körts i Stella.**

| Variant | RESP1-slut (CPU) | Förväntade P1-close X | Total CPU inkl. WSYNC | Cyklers teoretiska utrymme kvar | Avsikt |
|---|---|---|---:|---:|---|
| **A** | 30 / 40 | 39 / 69 | **51** | 25 | Första kalibrering |
| B | 32 / 40 | 45 / 69 | **51** | 25 | Gränsnära första-maskstresstest |
| **C** | 30 / 42 | 39 / 75 | **53** | 23 | Rekommenderat oberoende X-par |
| **D** | 32 / 42 | 45 / 75 | **53** | 23 | Rekommenderat, endast första X varierad mot C |
| **E** | 30 / 44 | 39 / 81 | **55** | 21 | Rekommenderat, endast andra X varierad mot C |
| **F** | 32 / 44 | 45 / 81 | **55** | 21 | Rekommenderat, båda X varierade |
| G | 30 / 38 | 39 / 63 | 49 | 27 | Boundary-stress, föregående huvudförslag nedgraderat |
| H | 30 / 36 | 39 / 57 | 47 | 29 | 18-clock-fasgräns, negativ kontroll |

**C→D, C→E, C→F** är en mycket skarpare test av *två separat varierade fysiska positioner* än att endast variera `FRAMELO` i RAM; C→D ska lämna andra P1-X oförändrat, C→E ska lämna första P1-X oförändrat, C→F ska flytta båda.

## Stopp, regressionsrisker och implementation-gate

**Måste mätas i riktig Stella 6.7.1, inte på papper:**
1. R0: den redan tidigare missade `STA RESP1`-brytpunkten i PR #7:s Venetian-ROM, med rätt PC, F6-bank, `_scan`, `_sCycles`, före/efterinstruktion; otillräckligt = INCONCLUSIVE.
2. R1a: NUSIZ1 ONE_COPY med en RESP som kontroll, därefter NUSIZ1 CLOSE med en RESP, sedan c30/c40, sedan fyra C/D/E/F-varianter och G/H som gränsprov. Fånga **faktiska** P1-X, extra huvudkopior från föregående frame, saknade pixlar, fasförskjutning.
3. R1b: byt från diagnostiska enkla bitmaprader till två **OLIKA fullständiga oförändrade original 8×9-masker**, på samma 9 ursprungliga scanlines utan höjdförstoring/interfoliering, med exakt var och en av de 72 ursprungliga maskbitarna jämförda pixel för pixel, och lägg till gul full Player0 och en aktiv testsymbolsmissil M0. `COLUP1` ska vara vit, `COLUP0` gul. Detta är ett deltest, inte full R1.
4. Kontrollera att tabeller inte korsar ROM-page för något Y (annars `abs,Y` +1 cykel), att BPL-loopgren inte korsar kodpage, och att GRP1 har `VDEL1=0` och inte olägligt latchar GRP0 (sätt `VDEL0=0`). Om dessa premisser inte stämmer är CSV-cykelbudgeten **ogiltig tills omräknad**.
5. När PF-vägg, högerdörr, sjätte NPC eller fyra banors relevanta grafik senare läggs till kan de 21–25 återstående nominella cyklerna vara otillräckliga vid fel horisontell registrering. Cykler kvar är **inte** bevisat lediga där de relevanta TIA-registerna måste skrivas.
6. Teoretiska P1-close-kopior har begränsad separations-/fasgeometri. Om två fullständiga masker bara visas vid diskreta positioner får det INTE markeras som sex individuellt fritt rörliga NPC i R1. Endast användaren kan ge eventuell designwaiver, inte MAIN.
7. Från tidigare R1x–R1ab bevaras skott-RAM-arkitekturen som framtida research men full gameplay-eldknapp/hit-ID är **utanför** denna R1-diagnostiska minimigrind.

**Beslutsdisposition:** `MAIN_SOURCE_ONLY_TECH_REVIEW_COMPLETE`; bäst nästa beslut enligt gällande status är R0 instrumentering följt av en snäv R1a-positioneringskalibrering **endast om ROM DEVELOPMENT:s återupptagningsmandat uttryckligen är kontrollerat**. En allmän uppmaning att "fortsätt" öppnar inte av sig själv senare implementationsteg efter tidigare STOPP. `main`, PR #7, VERIFICATION issue #8 och originalmaskcanon förblir orörda.
