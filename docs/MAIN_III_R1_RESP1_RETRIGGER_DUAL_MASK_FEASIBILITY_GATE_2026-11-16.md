# Let Me Out! – MAIN III: konkret feasibility-grind för två fullständiga P1-masker på samma rasterrad

> **MAIN korrigering 2026-11-16:** Denna första rapport behandlar c30/c38 som primär skiss. Efter direkt granskning av **Stella 6.7.1** har c30/c38 **nedgraderats till ett gränsfall**: den andra resetten kan inträffa när den första 8-pixelkopian visar sin sista pixel. **Den nya föredragna ordningen är c30/c40 för kalibrering och c30/c42, c32/c42, c30/c44, c32/c44 för faktiskt oberoende tvåmaskers-X-test.** Se den [nyare källkodskontrollen med exakt cykelmatris](MAIN_III_R1_RESP1_DUAL_MASK_STELLA_671_SOURCE_AUDIT_AND_8_CYCLE_VARIANTS_2026-11-16.md). Alla X-värden är fortsatt BERÄKNADE, inte uppmätta i en ny ROM.

**Datum:** 2026-11-16. **Disposition:** statisk teknisk studie och snävt experimentkontrakt. **INGEN ny ROM har byggts eller körts i detta dokument.** Ingen automatisk återstart av ROM DEVELOPMENT, inget R1-PASS och ingen oberoende VERIFICATION.

## A. Gällande styrning, exakt baseline

- [Aktuellt projektläge](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md), [NTSC v0.18-authorization](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [scope](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_SCOPE.md), [acceptans](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md), [blockers](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_BLOCKERS.md).
- Main SHA vid kontroll: `f6b3fc76c59161e04e583dc8c0787332d2f261c7`. PR #7 DRAFT på `82667dae033f70570dce903f8e1d4866528be02a`. VERIFICATION Issue #8 gäller fryst äldre baseline, INTE de nya researchresultaten.
- MAIN:s tidigare [NUSIZ-close-analys](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md) och [R1x–R1ab intake](MAIN_III_R1X_R1AB_INTAKE_SIX_NPC_FIRST_2026-11-16.md). Fortfarande sex självständiga NPC med alla fyra ursprungliga masktyper; aldrig ändra antalet eller raderna tyst.
- PR #7:s relevanta källa: `rom/v018/experiments/venetian_blinds/vb_9_interleave.asm` (Git blob `a25c92adb4ca5087eeace674e371be98b273ae5b`), `vb_9_vdel.asm` (blob `22ea32c52b36d9004cafad16b8e0413f85e9f3e2`), `ci_pc_cycle_probe.sh`. Den senare gör `break; frame #1; step` och lyckades INTE fånga faktisk `STA RESP1`. Inget bevisat registerskrivningsspår i T07.

## B. Ny konkret idé att mäta: BYT GRP1 MELLAN TVÅ RE-TRIGGADE close-kopior

**Verklig extern teknikgrund:** Andrew Towers [TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), avsnitten *Player Position Counter* och *The Re-trigger Trick*. `RESP1`-reset på synlig rasterrad startar INTE direkt P1:s huvudkopia. Under `NUSIZ1=$01` kan en *close*-kopia börja ungefär 17 TIA-color-clocks efter reset, med TIA-clock-phase-undantag. Om man strobar igen senare på samma rad kan ännu en close-kopia börja. P1:s 8-bitars grafiska skiftregister är separat från positioneringsräknaren; `GRP1` är normalt direkt läsbart för nya pixlar. Originaldemon `grid2` refereras i källan, men dess faktiska assemblerkällfil har INTE kunnat öppnas i denna MAIN-granskning – vi påstår därför inte ha verifierat dess maskladdningar.

**Fördjupad forskningshypotes:** För att två kopior ska visa OLIKA 8-bitars bitmaprader räcker inte två `RESP1`. Man måste också låta första kopian slutföra sin 8-färgklockors rad och sedan skriva nästa radbyte till `GRP1` INNAN andra kopians första pixel. En andra `RESP1` kan göras FÖRE det andra `GRP1`-bytet, eftersom close-start fördröjs ~17 färgklockor. Detta är hela det nya schemaläggningsfönstret; inte en ROM/PASS-claim.

### Statisk TIMINGKANDIDAT, ej emulatormätt

Anta vanlig NTSC-rad med 228 TIA-color-clocks = 76 CPU-cykler, ca 68 HBLANK-CC. För beräkningsillustrationen, och ENDAST för denna: `x_close ≈ 3*c_write - 68 + 17`, där `c_write` är aktuell ungefärlig CPU-write-sluttid. Verklig TIA-fas, strobe-latch och eventuell HMOVE ger korrigeringar som måste mätas.

| Händelse | Nominell CPU-cykel | Beräknad horisontell TIA-X | Krav |
|---|---:|---:|---|
| `STA RESP1` nr 1, NUSIZ1=$01 | c30 | close-kopia 1 startar ~x39 | Första masken redan skriven till GRP1 |
| Kopia 1, 8 pixlar | ca c36–c39 | x39–46 | Första originalbitmapraden får inte skrivas över |
| `STA RESP1` nr 2 | c38 | close-kopia 2 startar ~x63 | Andra reseten avlägsnar inte pågående första grafikskiftning |
| `STX GRP1` med förladdad andra bitmaprad | c41 | skrivning ungefär vid x55 | Efter första 8 pixlar (slut x46), före andra kopians start x63 |
| Kopia 2, 8 pixlar | ca c44–c47 | x63–70 | Andra hela originalbitmapraden används |

**Viktig detalj:** Om samma `STA RESP1`-operand används för båda strobningarna kan exempelvis `NOP` (2 CPU-cykler), `BIT FRAMELO` (3 CPU-cykler) och `STA RESP1` (3 CPU-cykler) ge totalt 8 cyklers avstånd mellan write-sluttiderna. Efter andra reseten sker `STX GRP1` (3 cykler). Den andra originalbitmapraden kan vara förladdad i X före första reseten; den första i A. Det måste fortfarande finnas tid för aktuell Y-rad, P0, M0, väggar samt övrig uppstart och avstängning.

En 8-bitars P1-kopia behöver 8 färgklockor. I idealiserade exemplet c30→c38 ger kopiorna X-separation cirka 24 CC, alltså 16 CC *mellan* pixlarna. Den andra bitmapskrivningen, uppskattat x55, ligger ca 8 CC efter första grafikens slut och 8 CC före andra start. **Detta är en möjlig skrivlucka på papper, inte ett bevis att 6507+TIA kan utnyttja den under resten av vår kernel.**

### Närmare avstånd – sätt i TEST, inte som garanterad funktion

| RESP-write-sluttider | Reset-avstånd | Nominella två close-starter | Kommentar |
|---|---:|---|---|
| c30 / c50 | 60 CC | x39 / x99 | Bred kalibrering, god tid för två bitmapladdningar |
| c30 / c38 | 24 CC | x39 / x63 | Primär tvåmaskerskandidat med andra GRP1-skrivningen efter den andra reseten |
| c30 / c37 | 21 CC | x39 / x60 | Stramare fönster; kräver extra fas- och instruktionstidsprov |
| c30 / c36 | 18 CC | x39 / x57 i idealmodell | Särskild hårdvarufasgräns! Towers beskriver upp till ±några pixlar av förskjutning/tappad start. |
| Resetavstånd mindre än ~17 CC | — | — | Tidigare close-start kan inhiberas: **negativ kontroll**, ej två-NPC-förväntan |

**Oberoende X, inte bara olika X:** CPU:s 6507-skrivningar sker i steg om 3 TIA-CC och två reset-tider ligger inom en 76-cykelsrad. Ett och samma HMP1/HMOVE-finvärde korrigerar vanligtvis båda P1-kopiorna tillsammans. Vi får INTE av detta härleda godtycklig enkelfärgklocke-/pixelprecision för vardera sprite, eller förutsätta att de kan vara nära/överlappa. En positiv testsekvens måste visa två LOGISKT separat varierade X över minst två olika X-par; därefter krävs en separat begränsningskarta för X-kvantiseringssteg, överlappningsfall och maximum.

## C. Körprotokoll och beslutskriterier – inga ROM-ändringar ännu

### R0: instrumentering – testa den gamla felande koden först

1. Pinna gammal Venetian ROM:s verkliga `.bin`, `.lst`, `.sym`, källcommit och SHA. Kontrollera att `STA RESP1` verkligen ligger på adresserna i just den byggda ROM:en (historiskt `$F0A8` och `$F0BD`), rätt F6-bank/mirror. Global `autoexec.script` måste isoleras från tidigare tester.
2. Stella 6.7.1: `clearBreaks`, `break <VERIFIERAD_PC>`, `listBreaks`, **`run`**; kräva att debuggern verkligen stannar med `PC=<VERIFIERAD_PC>` innan instruktionen utförts. `print _bank`, `print _scan`, `print _sCycles`. Ett enstaka `step` ger den efterföljande cykeln. Alternativt `trapWrite $11` (TIA RESP1, post-write), men var noga med att det är efter instruktionen.
3. Registrera båda typiska instruktionspositionerna med faktisk TIA-rasterrad och observerade P1-pixlar. Fel PC/skript-/bankstopp = **INCONCLUSIVE**, aldrig nytt R1-FAIL eller PASS.

### R1a: kopieutlösningsprov (enbart om ROM-utvecklingsmandat separat bekräftats)

- **A0-kontroll:** NUSIZ1=0, en RESP1 per rasterrad; skilj huvudkopians emission på följande rad från close-emission på aktuell.
- **A1:** NUSIZ1=$01, en RESP1; kontrollera faktisk close-position och eventuell överflödig huvudkopia/ghost.
- **A2:** två RESP1 kring c30/c50; samma enkla bitmönster kan användas enbart för att mäta verkliga två close-kopior och två färgklocke-X.
- **A3:** c30/c38, därefter c30/c37 och c30/c36; logga varje verkligt P1-X och eventuell fasskiftning, saknad kopia eller skärmradsklippning. Enkla testbitmaps ger INGEN originalfigur-acceptans.

### R1b: två olika, kompletta originalmasker och oberoende X

- Efter A2/A3-PASS: på **samma 9-radershöjdband**, använd exakt `MaleRows` och `FemaleRows` ur senaste styrande v0.18-originalkälla, totalt 9 8-bitarsrader per mask, utan lodrät förstoring eller Venetian-radförlust. Låt minst en kritisk rad med olika bitmapbytes (exempelvis raden med `$3C` kontra `$7E`) visa att andra `GRP1`-skrivningen verkligen bytt bild.
- Första masken ska laddas före första P1 close-kopian; andra masken före andra start, exempelvis via X→GRP1 efter andra RESP1. Bekräfta **samtliga 9 originalrader** på både nära och långt avstånd. Om första kopian avbryts av GRP1, eller andra får första bitmapen, = **FAIL**.
- Kör kombinationer där första X ändras och andra X är konstant, och vice versa; testa även båda ändrade oberoende. Nominella RAM-X måste jämföras med faktisk P1-pixel-X i Stella, och X-precision/kvantisering dokumenteras.
- Integrera sedan **gul P0-originalspelare, EN aktiv M0-testsymbol** och godkänd åtminstone minimal asymmetrisk väggbudget. Ingen färgflip, spökpixel, maskbyte eller gömd kopia får räknas som PASS. NTSC 262, CPU <=76/scanline.
- **Kritisk begränsning:** Deltabevis för två särskiljbara masker är inte bevis för R1:s sex NPC. Vissa testpositioner kan vara geometriomöjliga med nuvarande specialkernel; dokumentera vilka i stället för att koppla X-positionerna tyst.

### R1c: sex NPC endast efter R1b positivt och separat uppskalningsauktorisation

Skala 3→6 med samma-Y, fulla maskbytes, två stora män + två stora kvinnor + liten man + liten kvinna, individuell X, gul player/M0, vägg och senare R2-nyckel. Minst 600 sammanhängande faktiska Stella frames per väsentlig stressscen, mask- och färgdelta per NPC och pixel, longest-invisible-streak/flimmer, verklig `_scan/_sCycles` och F6-ROM-hash. Ingen automatisk designwaiver. Separat oberoende VERIFICATION signerar slutlig bedömning.

## D. Hårda stoppregler och status

- **Ingen ny implementering** följer bara av denna statiska research. Efter att tidigare ROM DEVELOPMENT rapporterat STOPP får MAIN inte behandla en allmän 'fortsätt' som tyst nytt ROM-kodmandat. Villkoret ska kontrolleras vid eventuell ny kodorder.
- Befintlig godkänd research-delprototyp R1x: 600/600 med fem NPC; R1y/R1z/R1aa/R1ab är FAIL för respektive skott-/grafikkonflikt. Inget av dem är FULL R1.
- Om A1/A2 bevisar fler kopior men B förlorar en originalrad eller oberoende X: **FAIL** för B, inte extrapolering till sex. Om responsen bara fungerar på exakta avstånd, dokumentera hård begränsning i stället för att ändra gameplay- eller spawncanon.
- Ingen merge till `main`, ändring av ROM DEVELOPMENT PR #7, oberoende VERIFICATION issue #8, PAL-/v0.19-kartcutover, ny mapper, fullspelsprogrammering eller tredjepartskodkopiering.

## Källor och bevishierarki

- Andrew Towers (2003), [TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), 'Using Horizontal Position Counters', 'Player Graphics Scan Counters', 'The Re-trigger Trick', särskilt specialfallen 18/33 CC.
- [Stella 6.7 debugger-dokumentation](https://repo.caluette.com/software/Games/Emulators/Atari/Stella-6.7/docs/debugger.html), breakpoint före instruktion, `trapWrite` efter och `_bank/_scan/_sCycles`.
- [MAIN:s gamla RESP1-rotorsak](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md). Uppskattade statiska cykler får **inte** påstås vara en uppmätt Stella-registretiming.

**MAIN-disposition:** `RESEARCH-PREPARATION PASS` – nytt väldefinierat testbart schema och fail-closed kontrakt. `ROM-EXECUTION NOT STARTED`, `R1 FULL FAIL/BLOCKED`, `INDEPENDENT VERIFICATION NOT RUN`.
