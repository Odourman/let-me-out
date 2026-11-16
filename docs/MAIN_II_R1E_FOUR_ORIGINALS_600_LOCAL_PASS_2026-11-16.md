# MAIN II – R1e: FYRA olika original-8×9-NPC samtidigt, 600/600 verkliga Stella frames

**Datum:** 2026-11-16. **Status:** `LOCAL_PASS_STATIC_FOUR_ORIGINALS_600` för isolerad standard NTSC F6/6502-kernel. **Inte** R1 full PASS, inte fri X, inte oberoende VERIFICATION, inte fullspelsauktorisation.

## Slutligt reproducerbart bevis

- [GitHub Actions #43812461127 – SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43812461127), branch `research/main-ii-r1e-four-originals-600-20261116`, testad commit `d2f7905286b08cb7fc4a40fb57713743e8c6d3b5`.
- **GitHub Artifact ID `14201470518`**, `main-ii-r1e-four-originals-600-frame-evidence`: **626 filer**, 600 verkliga cropped X11-Stella-debugger-PNG, exakt källkod, DASM-sym/list, byggd ROM, testskript, 600-radig `frames_600.csv`, komplett `evidence_600/summary.json` och SHA-manifest.
- Laddad artefakt kontrollästs efter Actions, ZIP-integritet `testzip() == None`. Oavhängig omläsning av `summary.json` bekräftar `LOCAL_PASS_STATIC_FOUR_ORIGINALS_600` och tom `failed_frames_first_10`.
- 16 384 byte standard NTSC F6 (fyra identiska 4KB-banker), ROM SHA256 **`84083e1c01de7ab0347ac18e85bdf36f37a6a7a201dd060f1f5248020459e24a`**, omverifierat från binären i slutpaketet.
- DASM 2.20.14.1 och Stella 6.7.1 på Ubuntu 24.04 GitHub Actions.

## Uppmätt via 600 SAMMANHÄNGANDE bildrutor

| Mått | Utfall |
|---|---:|
| Frame-ID 11–610 utan luckor i Stellas debugger | **600/600** |
| NTSC 262 rasterlinjer enligt Stellas bild-HUD | **600/600** |
| Alla fyra **olika** och **oförändrade** 8×9 original-NPC-maskerna, 72/72 bitpositioner var | **600/600** |
| Gul P0-spelarkandidat exakt 8×9 | **600/600** |
| Enbart ett synligt gult M0-testskott (2 raw GUI-pixlar), ingen automatisk wide-dubblett | **600/600** |
| Extra vita GUI-pixlar i 9-raders NPC-bandet | **0 totalt** |
| Extra gula GUI-pixlar i 9-raders NPC-bandet | **0 totalt** |
| Summerade fullt godkända frames | **600/600** |
| Status | `LOCAL_PASS_STATIC_FOUR_ORIGINALS_600` |

Kontrollerna är pixel-för-pixel ur skärmbilder från **verklig Stella**, inklusive de två rå GUI-pixlarna per TIA-pixel; de härleds inte enbart ur masktabellerna.

### Exakta stillbildspositioner i rå 1366×900 GUI-bild

| Figur | TIA-metod | GUI-X | Mask |
|---|---|---:|---|
| Stor man | P1 RESP1 #1 | 154 | Original 8×9 |
| Stor kvinna | P1 RESP1 #2 | 268 | Original 8×9 |
| Liten kvinna | P0 automatisk fjärrkopia via NUSIZ0=$04, byte av GRP0 och COLUP0 | 316 | Original 8×9 |
| Liten man | P1 RESP1 #3 | 400 | Original 8×9 |
| Gul spelare | P0 första kopian | 188 | Temporär spelarkandidat |
| Gult M0-skott | M0 på rasterrad y160, en rad ovanför figurbandets start | 240 | En kopia |

Maskerna jämförda direkt mot `main/design/NPC_REFERENCE_8x9_masks.json`, inklusive den lilla kvinnans och mannens transparenta rader, **utan att ersätta några godkända NPC-bitmaps**.

## Varför R1e fungerar och vad det kostar

1. P0:s läge är kalibrerat med åtta verkliga Stella-ROM:er vid `P0Delay=4–15`; [Actions #43811638502](https://github.com/Odourman/let-me-out/actions/runs/43811638502) visar att vänteloopen kan hoppa över rastergräns och att korta värden utan kompenserad VBLANK får 261 linjer. `P0Delay=4` + en extra tom VBLANK-rad återställer 262.
2. `NUSIZ0=$04` ger två långt separerade P0-kopior på samma rasterhöjd. Efter att den första 8×9-kopian (gul spelare) blivit ritad laddas `GRP0` om med den lilla kvinnans ursprungliga bitmaprad och `COLUP0` sätts vit före wide-kopian. Detta använder annars förbrukad per-rad väntetid i en specialiserad kernel.
3. P1 används fortfarande tre gånger på samma rasterrad, med olika `GRP1`-bitmapvärden per retrigger. Alla fyra NPC är vita och exakta.
4. `NUSIZ0` växlas till 0 en rad före NPC-bandet under M0-skottet och återställs till 4 inför P0-kopiorna, så M0 inte dubbleras. Det finns **ingen** kontinuerligt fritt placerad missile-/NPC-/PF-scenering här.
5. Ingen fjärde `RESP1`-skrivning, ingen extra kassetthårdvara, ingen bank-mergning, inga ROM-gradientswaivers.

## Viktiga ej uppfyllda grindar

- **Den vita lilla kvinnans X är hårt kopplat till spelarens P0-X: exakt +64 TIA-färgklockor.** Hon är **inte fritt positionerad**. De tre P1-figurerna har fasta X i detta prov. Det är därför **inte** fyra självständiga NPC, och absolut inte sex fria X på samma Y.
- M0-testskottet är förlagt till raden **ovanför** de nio NPC-raderna, inte en genomförd fri projektil med den fulla R1/R2-objektbudgeten. Ingen full PF-vägg/dörr-rendering, nyckel/O1, AI, kollisionslogik, HUD, PAL, faktisk Atari-konsol eller oberoende verifiering.
- Figuren P0 gult är en icke slutgodkänd temporär 8×9-testmask. Ingen ändrad designstatus får härledas från demon.
- CPU-kärnans tidsgräns är skarp; fyra former statiskt i en 262-raders Stella-sekvens bevisar inte att motsvarande kod kan hantera fri positionslogik, PF-skrivningar eller fullscenens kritiska rasterrader.
- **Slutlig full-R1 med sex oförändrade individuellt fritt placerbara androidsilhuetter är fortfarande BLOCKED**, trots fyra lokal-testgodkända former. Tidigare R1c tre-mask-tekniken och negativa R1d NUSIZ3-kopietest bevarade.

## Handoff och auktoritet

Denna rapport är **RESEARCH**. Alla kod- och Actions-filer ligger under `research/main-ii-r1e-four-originals-600-20261116`, och den bevisade binärens SHA framgår ovan. Ingen ändring har auktoriserats eller utförts på `main`, ROM DEVELOPMENT:s draft PR #7 eller oberoende VERIFICATION:s gamla baslinje. Det nya resultatet måste få en **separat implementeringsauktorisation** och en **ny, oberoende Verification mot exakt ny commit/binär** innan någon produktionsteststatus kan ändras.

**Rekommendation till MAIN:** använd detta som faktagrund för en separat X-oberoende-studie och PF-budgetstudie; anta inte att den automatiska P0-kopian ger en fjärde verkligt fri android. Ytterligare ROM-minne eller F6-bankswitching löser inte detta TIA-deadlineproblem ensamt.
