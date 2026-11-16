# Let Me Out! – aktuellt projektläge (MAIN)

**Datum:** 2026-11-15  
**Omfattning:** endast Atari 2600-spelet *Let Me Out!*.

## MAIN V – R1-F2 Individual-X Feasibility, aktiv från 2026-11-16

**NY ENDA AKTIVA ROM DEVELOPMENT II-ORDER:** [R1-F2-arbetsorder](MAIN_V_TO_ROM_DEV_II_R1_F2_INDEPENDENT_X_FEASIBILITY_AUTHORIZED_2026-11-16.md) · [Drive-kopia](https://docs.google.com/document/d/13DMNoefdmi8AaxvQat0BDxucmxhHRWPNzT3T_1qBxCQ/edit). MAIN:s användaruppföljning "ok, fortsätt" auktoriserar ett **nytt snävt R1-diagnostikprov inom redan användargodkänd v0.18 NTSC**, inte allmän R1/R2/R3/R4-implementation. F1 `F1-CAUSE_IDENTIFIED` är mottagen och avslutad. Använd **fasta pixelkorrekta 6B (16/16)** som baseline, korrigerad pixel-audit inklusive negativ mutationstest; prova max tre utvalda enskilda individers få små X-förskjutningar med **fem andra exakta X oförändrade**, verklig Stella-pixel + TIA-cycle-frames. Bara vid positivt G1: samma ROM skall växla EN individs X mellan två lägen. **Profilbyte mellan två kompletta fasta formationer räknas separat `F2_PROFILE_SWITCH_ONLY`, inte generellt fri-X.** Runtime-data-baserad en-individ-demo kan högst kallas `F2_LIMITED_RUNTIME_SINGLE_X_PASS`. F2 har hårda maxantal korta frameprover och inga nya 600-frame-serier. En enda isolerad ny gren, en samlad `TO_MAIN_R1_F2.md`. Inga Y-prover, R2/R4/integration, ny mapper, modifierad canon, PR merge eller VERIFICATION. Fullt R1 **BLOCKED/NOT ACCEPTED**, R3 isolerat DEVELOPER_LOCAL_PASS, Issue #8 vilande och VERIFICATION STANDBY.

## MAIN V – R1-F1 forensik mottagen, historisk 0/80-resultat korrigerat 2026-11-16

[MAIN V:s F1-mottagning och supersession](MAIN_V_R1_F1_RECEIPT_AND_HISTORICAL_AUDIT_CORRECTION_2026-11-16.md); [ROM DEVELOPMENT II:s frysta F1-rapport](https://github.com/Odourman/let-me-out/blob/ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F1.md). F1-branch HEAD `ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a`, uppdrag **F1-CAUSE_IDENTIFIED / DEVELOPER_LOCAL**, nu **avslutat**. Tidigare R1 `analyze_six_sweep.py` har verifierbar klassificeringsbugg `len(groups)==n` där `n` är text; därför är det historiska påståendet att 6A–6E gav **0/80 sexmaskframes** felaktigt/otillförlitligt. F1 rapporterar **6B 16/16 källkorrekta sex originalmasker vid fasta X**, 6C original 0/16 med x0-ghost/högerklippning/M0-övertäckning, och **6C-F1AB 16/16** efter EN tidsändring sista RESP1 c67→c65. 6A/6D/6E ej omgranskade. Verkliga Stella 6.7.1 traps rapporterade; fyra riktade Actions framgång verifierad via GitHub API, men **ingen oberoende Stella-verifiering av MAIN**. R1 sex **individuellt fria X/Y** förblir **BLOCKED/NOT ACCEPTED**, ingen ny R1-order utfärdad via mottagningen. R3 isolerad utvecklare-PASS, R2/R4/integration inte beställda, PR #7 draft, Issue #8 fryst, VERIFICATION STANDBY.

## MAIN V – NY AKTIV ARBETSORDER R1-F1 till ROM DEVELOPMENT II, 2026-11-16

[Fullständig auktoriserad R1-F1-forensikorder](MAIN_V_TO_ROM_DEV_II_R1_F1_SIX_MASK_TIMING_FORENSICS_AUTHORIZED_2026-11-16.md), [Drive-kopia](https://docs.google.com/document/d/15cA6s3rD_QLaMZ1k3gSY12mLk3lKTHNYaopnXnqsaHQ/edit). Migreringsrapport ROM DEVELOPMENT II godkänd; gamla R1:s 0/80 sexmask-Fail fortsätter BLOCKED. MAIN väljer **alternativ B** från utvecklarens intake, inte A: A:s NUSIZ1-close + två RESP1/GRP1 har redan begränsat 600/600 tvåmask- och 48/48 XY-bildbevis. R1-F1 får nu endast felsöka exakt två äldre misslyckade sexmaskscheman **6B och 6C** med verklig Stella-register-/pixeldeadline-trace, plus femmaskens fasta-X positiva kontroll. En liten avgränsad A/B-provändring får göras endast om analysen ger en falsifierbar hypotes, max 16 bildrutor; inga stora nya 600-frame-serier eller full kernel-implementationsfamilj. Leverera EN samlad rapport `TO_MAIN_R1_F1.md`, annars INCONCLUSIVE vid saknade tekniska data. Ingen R2/R4/integration eller designwaiver; Issue #8 och VERIFICATION fortsatt STANDBY; PR #7 draft/omergerad, main endast dokument. Full v0.18 BLOCKED/NOT ACCEPTED.

## MAIN V – ROM DEVELOPMENT II: chattmigrering efter fryst R1-blockerare, 2026-11-16

[Ny källkontrollerad migrationsrapport och startprompt](MAIN_V_ROM_DEVELOPMENT_MIGRATION_R1_BLOCKER_2026-11-16.md), [Drive-kopia](https://docs.google.com/document/d/1PYDcMtckYD5Fq4xyd7DOlEVVeXBUGPl8vCe-xo3XXh0/edit). Föregående ROM DEVELOPMENT-chatt nådde samtalets maxlängd efter att ha arkiverat R1-utvecklarens **BLOCKED**-rapport på gren `rom-dev/v018-r1-independent-xy-20261116`, fryst HEAD `b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0`. Verkliga rapporterade delprov: två originalmasker 600/600 (begränsade individuella X), två X/Y 48/48 (endast 1 rasterlinjes Y-offset), tre–fem originalmasker 16/16 var på fast X; **sex originalmasker 0/80 i fem scheman**, full R1 FAIL/BLOCKED, T07 globalt INCONCLUSIVE. R1-koduppdraget avslutades som tekniskt blockerat; den nya chatten ska först läsa fryst slutrapport och lämna kort mottagnings-/alternativrapport, **ingen ny kod eller lång testserie auktoriseras av migreringen**. Latest generic Actions run `43913227299` FAIL på `capture_pilot.sh`; tidigare 600/48-specifika Actions PASS med separata commits. R3 mottagen DEVELOPER_LOCAL_PASS; R2/R4/integration inte beställt; VERIFICATION STANDBY, Issue #8 fryst och vilande, PR #7 draft/unmerged. Full v0.18 BLOCKED/NOT ACCEPTED. Originalbeslut och övrig kodauktorisation oförändrade.

## MAIN V – 30 Atari-trick värderade för pågående R1, 2026-11-16

[Ny källkritisk R1-tillämpningsbedömning av alla 30 trick](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md). Forskningsrekommendation, **inte** ytterligare utvecklingsorder: prioritera verklig Stella-RESP1/GRP1-trace, trick **02** mid-scanline GRP, **15** NUSIZ-close same-scanline retriggering, **10** HMOVE och **24** förberäknad cykelexakt kernel. Först två **olika exakta** 8×9-masker med faktiskt oberoende X, därefter eventuell sex-NPC-uppskalning. R3:s trick **07** asymmetrisk PF är redan isolerat utvecklarvisat, ej R1-fix. Trick 03/04 var negativt prövade; 27–30 kräver annan mapper och är inte auktoriserade. **Inga av de 30 är bevisad fullständig R1-lösning**, R1 fortsatt aktivt, VERIFICATION STANDBY.

## MAIN V – R3/C02 utvecklarleverans mottagen, R1 nästa arbetsorder 2026-11-16

[MAIN V:s källgranskade R3-mottagning och avgränsade nya R1-arbetsorder](MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md). R3 på commit `000b6f2a579e4aa96995229b2174884fb7c565e2`, ROM SHA256 rapporterad `991cea24f67accb2128743bba5722a87ee8cec08c00f6e39e4df1e07c3826e9c`, är **MOTTAGEN SOM AVSLUTAD ISOLERAD DEVELOPER_LOCAL_PASS**, inte oberoende eller integrerad acceptans. 600/600 Stella GUI-frames 262, 7 verkliga registertraps i en kritisk scanline, T09–T12/T14/T16 lokal PASS; T01/T07 globalt INCONCLUSIVE; resterande NOT_RUN. Drive-evidens 3 420 134 byte metadata kontrollerat; utvecklarens SHA/729-manifestposter har inte oberoende omkontrollerats av MAIN. **Nästa och enda aktiva uppdrag är nu R1 inom v0.18 NTSC** med sex individuellt X/Y-positionerbara källkorrekta androider + P0/M0 och bruna PF-väggar. Ingen R2/R4 eller R1+R3-integration utan ny MAIN-arbetsorder. R3-bankens P1-port och statiska 74/76 cykler är integrationsrisker. VERIFICATION fortsätter STANDBY; Issue #8 fryst; PR #7 draft/unmerged, main enbart dokument.

## MAIN V – ROM DEVELOPMENT startprompt och första R3-uppdrag, 2026-11-16

[Komplett operativ ROM DEVELOPMENT-startprompt](MAIN_V_ROM_DEVELOPMENT_STARTPROMPT_2026-11-16.md) samt [Google Drive-kopia](https://docs.google.com/document/d/1aHAq7ZZ7Kw2zEhXXISA1aomocOY6xYOW4H2epdHG360/edit). ROM DEVELOPMENT får självständigt experimentera, implementera, felsöka och egenkontrollera inom **det enda aktiva R3/C02-uppdraget** men inte automatiskt gå till R1/R2/R4 eller senare fas. VERIFICATION förblir vilande till MAIN beställer en större fryst batch. Ingen produktionsmerge, ny spelcanon eller bredare kodauktorisation.

## MAIN V – användarbeslut om samlad VERIFICATION, 2026-11-16

[Ny bindande verifieringspolicy och startprompt](MAIN_V_VERIFICATION_BATCH_POLICY_AND_STARTPROMPT_2026-11-16.md) med [kopia i Drive](https://docs.google.com/document/d/1ynrElK86xYZ5jy27ytyrxwxUL1qX7Vj8QWc4fjsswJs/edit). **Oberoende VERIFICATION är nu vilande som standard** och får inte köras automatiskt vid chattuppstart, varje ROM-ändring eller enskilda forsknings-PASS. MAIN ska vid verkligt behov lämna en uttrycklig, fryst och innehållsrik samlad batch. **Issue #8 bevaras i kö som separat historisk baseline, inte annullerad men ej beställd nu.** Ingen ändring av krav på slutlig oberoende granskning, v0.18-scope eller canon.

## MAIN V – källkontrollerad mottagning 2026-11-16

[MAIN V intake och första R3-/VERIFICATION-arbetsorder](MAIN_V_INTAKE_R3_AND_VERIFICATION_ORDERS_2026-11-16.md) med [läsbar Google Drive-kopia](https://docs.google.com/document/d/10-aZ48bTCaa0szyLm7LRouMGuCTZbmzwfa0bL_xY78g/edit). HEAD och PR/Issues har kontrollerats live; de 57 ursprungliga besluten i Drive-ZIP har granskats. **Full v0.18 fortsatt BLOCKED/NOT ACCEPTED; R1ba är enbart lokal forsknings-PASS; PR #7 är draft/unmerged; fryst Issue #8 kräver egen VERIFICATION.** Detta är MAIN-dokumentation, inte auktorisation av kod utanför v0.18 eller av ny fas. Chattuppdragen är förberedda och ska lämnas till separata chattar av användaren.

## MAIN V – överlämningsläge 2026-11-16

**Nytt datumstämplat överlämningspaket från MAIN IV:** [Handoff](MAIN_IV_TO_MAIN_V_HANDOFF_2026-11-16.md) · [Startprompt MAIN V](MAIN_V_STARTPROMPT_2026-11-16.md) · [ROM DEVELOPMENT/VERIFICATION rollprompter](MAIN_V_ROM_DEV_AND_VERIFICATION_STARTPROMPTS_2026-11-16.md). Identiskt sakmaterial finns som tre Google Docs i [Let Me Out!-mappen](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Denna historikfil fortsätter att innehålla äldre avsnitt; bedöm auktoritet och kronologi, och verifiera live commit/PR/Actions/Drive vid ny MAIN-start. **Full v0.18 fortsatt BLOCKED; PR #7 draft/unmerged; Issue #8 fryst äldre baseline.** Handoffen låser inte upp ny fas.

## MAIN IV – nytt integrerat teknikbevis och R3-granskning 2026-11-16

- [R1ba: verkligt Stella-resultat 600/600](https://github.com/Odourman/let-me-out/actions/runs/43884511590). En ROM visar 2 stora män, 2 stora kvinnor, liten man och liten kvinna i byte-oförändrade originalmasker med tre **kopplade** runtime-X/Y-profiler, två bruna PF-sidoväggar, gul P0 och M0-testsymbol; 262 NTSC och 0 saknade/extra vita pixlar. SHA256 `41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`. [Alla 600 Stella-bilder, ROM, source och manifest i rätt Google Drive-mapp](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view?usp=drivesdk).
- [R3 högerdörr: aktuell källgranskning](MAIN_IV_R3_RIGHT_DOOR_SOURCE_AUDIT_2026-11-16.md). PR#7 har ospeglade vänster-/högerskrivningar och portfärgkod, men ingen godkänd riktig D01–D03-Stella-/kollisions-/nyckelhålgrind.
- **Inga nya accepterade testfall i produktions-PR**, ingen oberoende VERIFICATION; `main` har endast dokumentändringar. Enbart v0.18 diagnostik auktoriserad, full R1 och senare faser fortsatt blockerade.

## MAIN IV – daterad projektkontroll 2026-11-16

**Aktuellt besluts- och bevisdelta:** [MAIN IV CHECKPOINT 2026-11-16](MAIN_IV_CHECKPOINT_2026-11-16.md). Detta tillägg är MAIN:s samordnade status efter ny GH-/Drive-kontroll och ersätter inte denna fil som historik, de 57 ursprungliga besluten eller separat VERIFICATION.

- **Fortfarande endast v0.18 NTSC R1–R4 auktoriserat.** Produktions-PR #7 är DRAFT, ej mergad; oberoende Issue #8 avser fryst äldre baseline.
- Forskning i separata grenar har demonstrerat samma-Y sex originalmasker, förkompilerade begränsade X-uppställningar samt senare tre faktiska runtime-växlande små-NPC-Y-profiler ([R1az 600/600](https://github.com/Odourman/let-me-out/actions/runs/43871769128)). R1ay:s tre statiska Y-profiler klarade [1 800/1 800](https://github.com/Odourman/let-me-out/actions/runs/43871126664).
- Dessa resultat **upphäver inte R1-blockeringen**: sex individuellt fria X, integrerat X+Y+PF i ett bevis, R2-nyckel/O1, R3-högerdörr/nyckelhål, T07-cykeltrace och oberoende VERIFICATION återstår.
- **R1ax:** [senaste forskningstestet](https://github.com/Odourman/let-me-out/actions/runs/43883269341) klarade **600/600** lokala Stella-bildrutor med sex originalmasker, P0/M0, tre X-uppställningar och **två speglade bruna PF-sidoväggar**. ROM SHA256 `64ba6cd5152a395737b2c41607b0a9e54c7836319bbed2bfee9bfdc6af1f81d1`. Två negativa väggkontroller underkändes som avsett; hela workflowt är därför rött trots positivt mode-0-jobb. Detta bevisar **inte** enbart högerdörr eller full R1.
- **Google Drive har en ny MAIN IV-checkpoint i projektmappen**, daterad 16 november 2026; tidigare arkiv och beslut lämnas intakta.

## Beslutsstatus

## MAIN – 16 november: NUSIZ1-close retriggering, nytt snävt forskningsfynd

- **Ny källgranskad teknikhypotes, inte ny kod eller PASS:** [MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md). Andrew Towers [TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) beskriver Eckhard Stolbergs `grid2` och hur `RESP1` med `NUSIZ1`-kopieläge kan utlösa en *nära* P1-kopia på **samma rasterrad** cirka 17 färgklockor efter reset (mellan ~33). **Det är inte samma teknik som tidigare misslyckade NUSIZ1=0-Venetian-prover**, vilka gör en P1-reset per rad och inte triggar samma-rad-kopior.
- **Viktig gräns:** flera nära-kopior bevisar bara flera former om `GRP1` laddas om i korrekt tidsfönster för **två olika kompletta 8×9 originalmasker på fria X**. Ny P1-kopiemekanism ger inte gratis pixelbandbredd, oberoende 6-X, vägg-PF eller R2-nyckel. Same-Y-full-R1 fortfarande **FAIL/BLOCKED**, T07-trace fortfarande INCONCLUSIVE.
- **Rådgivande minimiprovsordning** (inget nytt implementationstillstånd): först giltigt `break` + `run` vid faktisk `STA RESP1`; därefter minimal *två RESP1 på samma rad* med `NUSIZ1=$01` som kopieutlösningsprob, sedan två originalmasker med olika bitmapdata och fria X. Först därefter, om mandat och delbevis räcker, skala mot sex och R2 med key/O1 och full PF-/TIA-budget. Historisk `grid2` är inte verifierat Let Me Out!-PASS.
- **Scope/respekt:** endast tidigare uttryckligen auktoriserad v0.18 NTSC/R1–R4; stoppad ROM-utveckling får inte automatiskt återstartas av forskning. Ingen ny mapper, fullspelsfas, waiver, PAL, kartcutover eller PR-merge. PR #7 ska förbli DRAFT; oberoende VERIFICATION äldre baslinje separat.


## MAIN – research 16 november: samtliga 30 Atari-trick, 52 teknikmönster

- **Inläst och granskat:** 55-sidig, användaruppladdad samlad Atari 2600-teknikavhandling (inklusive historiska 67-problemsstudien) samt separat 30-tricksbilaga. [30 originaltrick arkiverade](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md); [MAIN:s fullständiga prioriterade granskning med samtliga 30](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_30_TRICKS_RESEARCH_REVIEW_2026-11-16.md). 52 T-poster och 30 numrerade trick överlappar; inte 82 oberoende lösningar.
- **Nya filers proveniens:** MD-original 30 374 byte, SHA-256 `6d45b2ba5747ee7c64a7446d5295f6f8add988386593b5662a70b700aabff28c`, 30/30 index- och rubrikposter. PDF 55 sidor, 534 513 byte, SHA-256 `596ee313bbbfcf3926efea61807a7b169363dd1aef994a4fc9a635877c62019f`; PDF-bilagan finns i konversationen, ingen Drive-kopia hävdas.
- **Teknisk prioritet oförändrad:** först giltig Stella `STA RESP1` PC/bank/scanline/cykeltrace (tidigare `break; frame; step` missade), sedan två oförändrade 8x9-originalmasker med fria X på samma höjd samtidigt med P0-spelare och M0-skott. Vid faktiskt bevis och rätt auktorisation: full R1 och R2 med nyckel/O1, därefter R3/R4. **Ingen ny R1 PASS**, fortfarande **FAIL/BLOCKED**. R2–R4 på Venetian inte omtestade; självtester ej oberoende VERIFICATION.
- **Historiska trickens värde och spärr:** hög forskning för GRP/NUSIZ-deadlines, HMOVE, precompute, P0/P1-displaylistor, F6-specialkernels och asymmetrisk PF för högerdörr. Venetian/sixfas-flicker/grov PF redan lokalt negativa. Tricken **27–30** kräver annan kassetthårdvara än godkänd standard F6. Ingen ny ROM-kod, ny mapper, fullspelsfas, PAL, kartcutover eller grafisk waiver auktoriseras genom forskningen. Draft PR #7/VERIFICATION #8:s äldre baseline förblir åtskilda.


## MAIN – F6-bank- och ROM-minnesrevision (rådgivande)

- **Ny statisk käll-/symbolbaserad revision:** [MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md). Verifierat i utvecklingsgrenens `rom/v018/tools/build.py`, `src/bank0.asm`–`bank3.asm` och `dist/symbols.json`, mot rapport om bank switching som användaren bifogat.
- **Huvuddiagnostiken använder fyra skilda R1/R2/R3/R4-databanker men samma exekverbara kernel.** Kernel `$F000-$F1E0` = **481 byte/bank**, åtta fulla tabeller `$F400-$FBFF` = **2 048 byte/bank**, säkert tillgängligt oallokerat ROM i `$F1E1-$F3FF` och `$FC00-$FFF5` = **1 557 byte/bank** (hotspots `$FFF6-$FFF9` och sista vektorområdet reserverade). Detta är **ROM, inte extra RIOT-RAM eller TIA-/cykeltid**.
- **Skilj diagnostik från faktiskt spel:** separata bank-R1 (NPC) och bank-R3 (dörr) bevisar **inte** att dörr och alla NPC kan visas samtidigt i en spelruta. Senare sex-X/Venetian-ROM:er upprepar sin egen 4 KB-bank fyra gånger, utnyttjar inte extra unika data i 16 KB.
- **Forskning, ingen kodstart:** specialiserad R1/R2-kernel och förberäknade data kan undersökas, men gemensam bankbytesfortsättning/reset måste säkras och själva RESP1-timingen fortfarande mätas. `STA $FFF6` vs `BIT $FFF6` är en hypotetisk A/B-kontroll, inte ett konstaterat fel. **Ingen ändring av godkända R1–R4, fullspel, PAL, kartcutover, ROM-gren eller PR-merge.**


## MAIN – RESP1: rotorsakshypotes och rättad mätmetod (v0.18)

- **Ny MAIN-analys av faktiska källor och sex ursprungliga Stella-skärmbilder:** [RESP1-rotorsaksanalys](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md). Inga ändringar i ROM eller godkännanden.
- **Bekräftad instrumenteringsbrist:** `ci_pc_cycle_probe.sh` använder `break $f0a8; frame #1; step`; sparad Stella-bild står vid PC `$F047`/scanline 0, inte `$F0A8`. Rekommenderat `break` + `run` eller `runToPc` med kontrollerad PC/bank/cykel före och efter faktisk `STA RESP1`. T07 fortsatt INCONCLUSIVE.
- **Stark men ännu omätt TIA-förklaring:** `GRP1` skrivs tidigt, `RESP1` senare på varje rasterrad (man ungefär CPU-cykel 30/35, kvinna 50/55 statiskt). En RESP-reset av P1:s huvudkopia sätter position för följande scanline; nästa tidiga reset kan hinna överstyra den sent förberedda positionen innan den ritas. Förutsäger att mest vänstergruppen syns, i linje med skärmbilderna; behöver verklig TIA-debuggertrace för bekräftelse. 9-raders radinterfoliering tappar ändå 4/5 originalrader och är inte full R1-PASS.
- **Scope bevarat:** endast befintligt uttryckligt v0.18 R1–R4; ytterligare kod efter tidigare rapporterat STOPP kräver kontroll av gällande mandat och separat uttryckligt tillstånd om ny teknisk uppgift ligger utanför det. Ingen fullspel/PAL/ny designwaiver/merge. Draft PR #7 och äldre frysta VERIFICATION-baslinjen lämnas orörda.


## MAIN – Venetian Blinds v0.18: tre verkliga ROM, R1 FAIL/BLOCKED

- **Nyaste ROM DEVELOPMENT-leverans:** [full rapport](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/TO_MAIN_VENETIAN_BLINDS_2026-11-15.md), [T01–T16-delta](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/TEST_MATRIX_V018_VENETIAN_DELTA.csv), [MAIN:s mottagningsgranskning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_VENETIAN_BLINDS_INTAKE_2026-11-15.md). Draft [PR #7](https://github.com/Odourman/let-me-out/pull/7) HEAD vid mottagning `82667dae033f70570dce903f8e1d4866528be02a`; **ej mergad**.
- **Resultat:** tre reproducerbara 16 KB F6/NTSC-prototyper byggda i DASM och prövade i Stella 6.7.1: 9-line Venetian interleave, 18-line diagnostisk dubbelhöjd och 9-line VDEL. I sex valda råa Stella-bilder ser man P0-spelare/M0-skott och 262-scanline-HUD, **men ingen komplett andra fritt placerad originalandroid**. Det här bevisar fel i de prövade implementationerna, **inte** att all Venetian Blinds-teknik är omöjlig.
- **Bevisbegränsning:** endast sex utvalda Venetian-bilder, inget nytt 600-frame-test och **ingen giltig individuell TIA-register-/CPU-skrivtrace**. Statisk cykelbudget är inte uppmätt registertiming. Ny delta-matris: **2 LOCAL_PASS, 2 FAIL, 2 INCONCLUSIVE, 10 NOT_RUN**. R1-grafik fortfarande **FAIL/BLOCKED**. R2–R4 inte omtestade på denna kod.
- **Evidensarkiv kontrollerat av MAIN:** [Google Drive ZIP](https://drive.google.com/file/d/1toh8XDyCBk2LckDwrm4oAQHJ_E4RSEfP/view) 355 517 byte; SHA-256 `b8141a874ad1e10de1ec958d1af36f46c51cc7a548181370ccfe6714dcfda271`; ZIP-integritet OK, **94/94 interna manifestposter korrekta**.
- **Rotorsak ej fastställd:** `GRP1` skrivs före `RESP1` på synliga rader; MAIN rekommenderar exakt uppmätt register-/pixeldeadline före ytterligare uppskalning. Nominella X-tabeller är inte visade fria X i bild. Även lyckad 9-line varannan-rad-modell förlorar originalrader och uppfyller inte automatiskt hela silhuettkravet.
- **Grind fortsatt oförändrad:** endast tidigare uttryckligen auktoriserad v0.18 NTSC/R1–R4-diagnostik; ingen ny spelversion, PAL, designwaiver, v0.19-kartcutover eller merge. Fryst oberoende [VERIFICATION #8](https://github.com/Odourman/let-me-out/issues/8) på `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` får inte överföras till ny commit. Eventuell ny teknisk insats kräver separat prioritering och vid behov uttrycklig utökad auktorisation.


## MAIN – research från The Cabin: rådgivande, ingen ny teknik-PASS

- **Arkiverad användarlevererad research**: [exakt källrapport](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_THE_CABIN_TRANSFER_2026-11-15.md) (också [Google Drive-kopia](https://drive.google.com/file/d/1BXeRmUnBUtO-Xexisw6O0cadz3Sklw3C/view)) samt [MAIN:s källkritiska bedömning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_RESEARCH_CABIN_EVALUATION_2026-11-15.md). **Research är rådgivande; ändrar inga användarbeslut, ROM-grindar eller Canons.**
- **Kontrollerad primärkod** i användarens The Cabin-källarkiv: Cyloid = tvålinjers P0/P1/M0/PF + endast ett utvalt P1-mål åt gången (ingen ny lösning för same-Y sex NPC); AStar = tidsbestämda asymmetriska PF1/PF2-skrivningar (relevant för högerdörr/väggar, inte en lösning för fyra exakta androidsilhuetter). AStar-källan är GPL-3.0: studera idéer, ingen obehörig kodkopiering. Crystal Castles' vertikala objektåterbruk löser inte sex på samma rasterhöjd. PoC/Pachinko överför framför allt verifieringsmetodik.
- **Senaste ROM-delta ersätter äldre historiskt statuspåstående om att sex-X inte levererats:** [SEX_X_FREE-rapport i PR #7](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/six_x_free/TO_MAIN_SIX_INDEPENDENT_X_STELLA_2026-11-15.md), kontrollerad HEAD `febfda591c1a4b81682bbb33b20f02b6a99aae0c`: sex logiskt fristående X fungerar som utvecklarprov. **R1-grafik FAIL:** A varje NPC 100/600 bildrutor, B PF-former oläsliga som godkända människosilhuetter. 600/600 Stella-HUD med 262 scanlines per A och B rapporterat, men ingen fullständig individuell TIA-/CPU-registertrace och ingen oberoende VERIFICATION. **R2–R4 ej omtestade på denna kod.**
- **Cykelgräns:** older/historiskt ~74/76 får inte användas som uppmätt värde för de nya experimenten. A ~30, B ~67–70 cykler är **statiska estimat** (inte en bevisad friskrivning från 76-cykelrestriktionen).
- **Nästa tekniska undersökning, ej användarbeslut eller nytt implementeringssteg:** verifiera `RESP1/HMOVE/GRP1/VDEL` vid samma-Y för två oberoende exakta NPC-masker i samma frame med gul P0 och testsymbolskott M0; bara vid positivt Stella-bevis skala 3→6. Separat R2-nyckel och R3-asymmetrisk PF. Om ej möjligt, öppet FAIL/BLOCKED till MAIN. **Ingen** designwaiver, fullspelsauktorisation, PAL, kartcutover eller merge.


### Synkad beslutslogg – senaste beslut, 2026-11-15

- **[Kompletterande MAIN-beslutsregister i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md)** och **[identisk kopia i Google Drive](https://drive.google.com/file/d/1bMUNx-8-sUkx4CHo5Rmm7DpzIFzAXJkF/view)** bevarar de elva nyare användarbesluten/prioriteringarna med explicit status, länkade originalkällor och öppna frågor. Detta kompletterar (ersätter inte) originalhandoffens 57 beslut.
- **Senaste rumsvilja:** få bruna väggar, öppna Berzerk-inspirerade rum som *antyder* små avdelningar. **Godkänd designriktning**, inte godkännande av varje exakt ny 40×22-kartcell. `A_OPEN_01`–`D_OPEN_01` är fortfarande **v0.19-kandidater**; tidigare A01/B01/C02/D01 bevarade, inklusive godkänt C02-val.
- **Senaste spelar-/spritevilja:** gul spelare lika stor som stor android, mindre än dörröppningen; två stora män, två stora kvinnor, liten man och liten kvinna. Ursprungliga 8×9-NPC-masker kvarstår som referenser, inte slutligt implementerade 2600-sprites.
- **Grindar fortsatt separata:** endast NTSC/R1–R4 v0.18 kodauktoriserat; prioritera sex individuella X. PR #7 är draft och inte full R1 PASS; oberoende VERIFICATION #8 gäller fryst baseline. Inga nya kartbyten, fullspelsfaser, PAL, ändrade AI-/kollisions-/poängregler utan särskilt godkännande.


- 57 beslut registrerades i den ursprungliga överlämningen. Beslutsregistret i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip` är underlag för beslutens exakta status och historik.
- Senare studier v0.1–v0.16 är i huvudsak **rådgivande förslag**. Undantag: K1/E1 (kollisioner), C02 (planerad kartlayout), V2B/GULD (visuell riktning) och nu **O1 (android får tillfälligt skymma nyckeln)** har godkänts av användaren. En mindre mängd flimmer i spelet har accepterats kvalitativt, utan numerisk tolerans. Se [besluts- och planrapporten](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md).
- **NYTT ANVÄNDARBESLUT 2026-11-15:** Endast **ROM DEVELOPMENT-diagnostik v0.18 med NTSC**, R1–R4, är **uttryckligen kodauktoriserad**. F6 16 KB får användas om tekniskt motiverat. [Auktorisation](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [Issue #6](https://github.com/Odourman/let-me-out/issues/6). **Ingen fullspelsutveckling, PAL-utbyggnad eller senare ROM-steg är auktoriserade. En körbar 16 384-byte F6/NTSC-utvecklar-ROM har nu levererats via PR #7, men den är blockerad och ännu inte oberoende verifierad.**

## Fastställd kärna

Sex vita människoliknande androider, fyra stora och två små; en gul spelare. Fyra speglade labyrinter slumpas utan direkt upprepning. Start vid vänster sida, utgång genom låst högerdörr. En android bär nyckeln och måste förstöras för att den ska uppstå efter dödsanimationen.

Androiderna är ofarliga fram till första **faktiskt avfyrade** skottet, då de omedelbart börjar jaga. Androiderna skjuter aldrig. Högst ett aktivt spelarskott, ett per nytt knapptryck. Väggar är ogenomträngliga men ofarliga.

**Poäng:** -25 per android (aldrig under 0), +50 vid nyckelupptagning, +100 vid faktisk rumsutgång, +15 per överlevande android vid utgång. Tre liv, extraliv vid 500, 1500, 2500, osv. Strategin att skjuta alla är tillåten.

## Preliminära tekniska kandidater

- **Kartor:** Planerat fyrarum-set är **A01/B01/C02/D01**. **C02 är godkänd som planerad version av C**; C01 sparas som jämförelsekarta. A01/B01/D01 behålls oförändrade som hittills studerade kandidater. Ingen pixel- eller ROM-verifiering har skett.
- **AI:** P2 (patrullera rakt och sväng ibland) och J2 (enkel närmandelogik med kort slumpmässig omväg).
- **Svårighet:** C-1 är en föreslagen kurva, inte fastslagen hastighetsimplementering.
- **Grafik:** sex androider på samma rasterhöjd, spelarskott, dörr i speglad playfield och nyckel kräver verkliga timingtester.
- **Dörr:** v0.12 visar att alla fyra kartorna har samma högerdörrzon **x=39, y=9–12** och konstant stängd vänsterkant. Logikmodell 16/16 PASS, **inget ROM-test**. [v0.12](https://github.com/Odourman/let-me-out/blob/main/docs/DOOR_VISUAL_RIGHT_ONLY_STUDY_V012.md) föreslår orange smal port (V2) som visuellt mål, med brun PF0-port (V1) som tekniskt testbasfall. Färg och implementering är **inte godkända eller verifierade**.

## Senast godkända MAIN-beslut (K1/E1)

- **BESLUT K1:** Nyckel som uppstår under stillastående spelare får tas i nästa logiska uppdatering utan rörelse.
- **BESLUT E1:** Dödlig kontakt med överlevande android i öppnad dörr prioriteras före rumsbonus.
- Båda är **godkända som spelregler**, men **inte implementerade eller verifierade**: [beslutslogg](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md) och [avslutat GitHub Issue #1](https://github.com/Odourman/let-me-out/issues/1). [Underlag v0.9](https://drive.google.com/file/d/1Ztg48ihTanH58Z07OhH3Ge3-Rim2v3iC/view?usp=drivesdk).

## Senaste visuella användarreferenser

- Två användaruppladdade formreferenser från 2026-11-15: guldgul nyckel med runt hål/tandat kort skaft samt svart nyckelhål med rund topp och kilformad nederdel. Bilderna är vattenmärkta stockfoton; **originalbilderna har inte lagts i publika GitHub eller i ZIP**. Projektet använder egna bitmapskisser i v0.13.
- Originalnyckelns form var redan beslutad i Master Spec; ny bild preciserar det visuella målet utan att ändra poäng eller kollisionsyta.

## Senaste arbetsstatus v0.16 – åtta analyser fullföljda

- [Samlad 8-stegsstudie i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_EIGHT_STEPS_V016_2026-11-15.md), [37+1 filer i Drive ZIP](https://drive.google.com/file/d/1YrXJtgqvY9bjaSKKxoyb7hvs7ye5msx-/view?usp=drivesdk), [mobil-PDF](https://drive.google.com/file/d/1RbjgcJs_oTlYIqeHF3tZk6PZawRIbiZu/view?usp=drivesdk).
- Avgränsat innehåll: lång nyckelskymning (160 modellförlopp), rastervärstafall (8 logiska enheter), högerdörr, nyckelmasker, P2/J2-AI (480 modellförlopp), S0/S1 (64 045 kombinationer), C-1/C-soft-kurvor och score/HUD.
- **Arbetsrekommendationer, inte nya canon-beslut:** P2/J2 med 1/8, K11 med K09 som reserv, S0, C-1 och HUD-A. De 22 framtida tekniska fallen är **NOT_RUN_IN_ROM**.
- **Återstår i 10-stegsplanen:** steg 9 – presentation/ljud; steg 10 – integrerad teknikgrind. Ingen ROM-kodstart har auktoriserats.

## Senaste användarbeslut: O1 och viss flimmertolerans

- [Beslut, senaste tio steg och kommande tio steg i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md), [identiskt dokument i Drive](https://drive.google.com/file/d/1N4D5GH-hhBsbQPIK82v2KF5IdMgq33HJ/view).
- **O1 godkänt:** Androidens figur får skymma nyckeln, men position/status/poäng påverkas inte. Nyckeln visas på samma ställe när roboten flyttat sig.
- **Lite flimmer accepterat:** inte tillstånd för långvarig oläslighet eller skymd spelarfara. Bedöms i framtida ROM och oberoende VERIFICATION.
- Ingen ytterligare ROM-/6502-auktorisation har givits.

## Presentation – nytt användarbeslut och öppet designförslag

- **BESLUT:** Ingen separat startskärm i Let Me Out! (användarens direktinstruktion 2026-11-15). Spelstart/omstart sker utan fristående titelskärm; exakt kontroll- och startflöde återstår att specificera.
- **BESLUT GAME OVER/RESET:** Berzerk-inspirerad slutpresentation i labyrinten med färgväxling och långsamt blinkande slutpoäng. **Endast Atari-konsolens GAME RESET/RESET startar om** efter GAME OVER; Fire får inte starta om och är inaktivt efter sista livet. RESET startar nytt spel med 0 poäng och 3 liv. Ingen separat start- eller Game Over-skärm. Exakta färger och blinkintervall är tekniskt öppna; original-Berzerks Game Over-inversion är inte styrkt av manualen. [Beslutslogg](https://github.com/Odourman/let-me-out/blob/main/docs/GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md), [samma på Drive](https://drive.google.com/file/d/1r417oy8bAyVBj-bfeeC58QjynEwzHevv/view).
- Dessa effekter får inte förväxlas med användarens accepterade **begränsade flimmer under spel**. Ingen ROM-implementation har godkänts.

## Viktigaste öppna val

1. **C02 valt som planerad karta C** (beslut; inte speltestad): [GitHub-beslut och spawngranskning v0.11](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_MAP_C02_AND_SPAWN_AUDIT_V011.md), [Drive-paket](https://drive.google.com/file/d/1WbnLfcSKM-bqmVIz5jCJ0ga0sUzPU0UK/view?usp=drivesdk), [avslutat Issue #2](https://github.com/Odourman/let-me-out/issues/2). A01/B01/D01 ej ändrade. Jämför bara A/B/D med annat utförande om senare speltest kräver det.
2. **Spawnspelbalans ännu öppen:** samtliga 64 045 möjliga sexstartval ur nuvarande fyra pools klarade offline 2×2-kontroll. S0 oförändrad bas, S1 (minst 12 fyrvägssteg från spelarstart) **endast testkandidat**.
3. Detaljer för patrullering, jakt och svårighet (P2/J2/C-1), tills vidare testkandidater.
4. **VISUELLT MÅL BESLUTAT v0.13:** guldgul nyckel med runt genomgående hål och kort tandat skaft; smalt orange dörrstreck med **svart nyckelhål**. Hela dörren och symbolen försvinner vid upplåsning. [Beslutsunderlag](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md) och [avslutat designärende #4](https://github.com/Odourman/let-me-out/issues/4). **Exakt pixelmask och TIA-teknik överifierade.** [Öppet framtida testärende #5](https://github.com/Odourman/let-me-out/issues/5).
5. **Nyckelns kontraststudie v0.14, inte beslut om färgkod:** tre hypotetiska RGB-toner jämförda, preliminärt föredras en något djupare guldton framför nästan spelargult; varken K11/K09 eller PAL/NTSC-kod låst. [Designstudie i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_CONTRAST_RGB_REVIEW_V014.md), [ZIP i Drive](https://drive.google.com/file/d/17I6nUhYTCSRIQ35fMvILE1pmVIIDh8SA/view?usp=drivesdk). 9 matematiska RGB-kombinationer och två offline-maskkontroller, **ingen Atari-körning**. [Framtida verifieringsärende #5](https://github.com/Odourman/let-me-out/issues/5).
6. **Nyckelöverlappning v0.15 – O1 NU GODKÄND:** Android får tillfälligt skymma statisk nyckel, men får aldrig flytta, påverka eller ta den. Nyckeln återkommer synligt på oförändrad position när skymningen upphör. Ingen avsiktlig blinkväxling. Mindre tillfälligt flimmer i spelet är acceptabelt, men exakt teknisk gräns är inte bestämd. 20/20 offline-händelsetester klarade. **Ingen TIA-/ROM-verifiering.** [Studie](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_OCCLUSION_LOGIC_V015.md), [Drive ZIP](https://drive.google.com/file/d/1u6FNeEnsNUNufpJtugXfGfm7irAEOQPm/view?usp=drivesdk).
7. Grafikarkitektur och tolerans för flimmer – först efter uttryckligt godkänd ROM-prototyp.

## MAIN – fyra öppna rum 40×22 (v0.19 förslag, inte ny canon)

- **Användargodkänd designriktning:** fyra luftiga rum med få bruna väggpartier som antyder mindre utrymmen, inte en tät labyrint. **Nya exakta kandidater** i [design/OPEN_ROOMS_V019_40x22_CANDIDATES.json](https://github.com/Odourman/let-me-out/blob/main/design/OPEN_ROOMS_V019_40x22_CANDIDATES.json): A_OPEN_01, B_OPEN_01, C_OPEN_01, D_OPEN_01. [Full MAIN-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_OPEN_ROOMS_V019_2026-11-15.md) samt [reproducerbart ZIP i Drive](https://drive.google.com/file/d/1kO38zm26fFSwu0cAnwQYAZ56D52HrJvK/view).
- **Innerväggar:** 4,74 % / 6,32 % / 8,42 % / 7,89 % av respektive 38×20 inneryta (tidigare 8,42 % / 20,53 % / 16,32 % / 22,11 %). Fortfarande 40×22, stängd vänstergräns, högerdörr x39/y9–12, spelstart x2/y10 och symmetrisk innervägg.
- **Offline-geometri:** 623/623, 619/619, 579/579 respektive 591/591 godkända 2×2-fotankare nåbara från spelstart och högerdörr, med minst sex separata historiska S0-exempelstartpositioner i varje rum.
- **Förenklad dynamisk studie:** 100 deterministiska trafikförsök per rum (400 totalt, 180 logiska steg), sex 2×2-NPC-objekt och en spelare som söker dörren. Spelaren nådde utgången i 400/400; längsta observerade robotstopp ≤2 steg. Detta **är inte** godkänd P2/J2-fiende-AI, riktig 8×9-kollision, faktisk Atari-grafik eller en garanti för att ingen kan fastna under gameplay.
- **Behåll gamla kartor och tidigare användarval:** [A01/B01/C02/D01 v0.11](https://github.com/Odourman/let-me-out/blob/main/design/PLANERADE_RUMSKARTOR_V011.json) har inte ersatts. **C02:s tidigare godkännande upphävs inte automatiskt.** De fyra nya rutmatriserna behöver ett separat exakt kartbeslut före canon-byte.
- **Ingen ny ROM-fas:** befintlig NTSC-diagnostik v0.18 R1–R4 är enda auktoriserade implementationen. [Draft PR #7](https://github.com/Odourman/let-me-out/pull/7) lämnas oförändrad och ingen fullspelsspelmotor/kartcutover är godkänd.

## MAIN – sex individuella X-positioner (v0.18, offline-stresstest och utvecklingsuppdrag)

- **Uttrycklig ny arbetsprioritet från användaren:** börja med sex androider på **individuella X-positioner**, viktigaste tekniska hindret. Fortsatt enbart auktoriserade v0.18 NTSC/R1–R4, ingen ny fas.
- [MAIN:s geometriska stresstest](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md), [reproducerbart paket i Drive](https://drive.google.com/file/d/1s4gWod2rnvYJRFoyQlDpkR3VMeXTnffU/view): **44 191 av 64 045** historiska S0-sexval saknar NPC-par på just de **i tidigare Stella-prov verifierade** NUSIZ-separationerna 32 och 64 färgklockor; A01 66,9%, B01 24,1%, C02 77,5%, D01 69,2%. Avser *offline-x-geometri*, inte faktisk same-Y-rendering eller spelbarhetsrisk.
- **Konkreta R1-provet skickat till [PR #7](https://github.com/Odourman/let-me-out/pull/7):** sex separata X-koordinater och NPC-typer, same-Y-test x i färgklockor `[16,36,56,76,96,116]`, högst två tekniska renderingsspår, faktiskt 600 konsekutiva Stella-frame-värden, per-android-synlighetsmask/frekvens/längsta osynlighet och verkliga CPU/TIA-skrivcykler. Ingen förenklad spriteformation får räknas som full R1 PASS.
- **Status:** Implementation och faktisk Stella-körning av detta sex-X-prov **inte levererad eller verifierad**. PR #7 fortsatt DRAFT. [VERIFICATION #8](https://github.com/Odourman/let-me-out/issues/8) gäller fryst historisk baseline, ej ny implementatörscommit.

## MAIN – första fungerande originalsilhuetter i Stella (v0.18 teknikdelta)

- **Ny utvecklarcommit på [draft PR #7](https://github.com/Odourman/let-me-out/pull/7):** `f5c06f352ba8653f3ce65bbc3e5e392c892beec5`. Fryst originalbaseline för separat [VERIFICATION #8](https://github.com/Odourman/let-me-out/issues/8) är fortfarande `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` och har **inte** ersatts.
- **MAIN:s mottagningsgranskning:** [full rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_REVIEW_SPRITE_DELTA_V018_2026-11-15.md), [ZIP-evidens i Drive](https://drive.google.com/file/d/1Ho50YGc7IDYodm962MpBNxLvkqtt6xZ7/view). Arkiv-SHA-256 `675bfcf17343bccdd2bf2d5843dcf77738d9d0521fa5e9ae606bd52eabbf03b6`, 52/52 interna checksummor OK.
- **Lokalt teknikdelprov:** NUSIZ kan visa två olika godkända 8×9-androider (stor man + stor kvinna) med pixeljämförelse 72/72 per mask i två fasta kopieavstånd (32/64 färgklockor). Gul nio-raders spelarkandidat och testskott synliga. Försök med två oberoende RESP1-repositioneringar misslyckades.
- **Ingen R1–R4-godkänd ROM:** sex individuella androider i R1 fortfarande **BLOCKERADE**; R2/R3/R4 inte omimplementerade av detta delprov. 600-frame script har bildruta 610 men **saknar 600 individuella sparade scanlinemätningar** (tom `saveSes`). CI kördes på föregående kodcommit och ny HEAD lägger endast till rapport/paket, inte ny kod.
- **MAIN:s nästa avgränsade instruktion kommenterad i PR #7:** jämför högst två implementeringskandidater för individuella X-värden (kontrollerad frame-tidsmultiplexning eller PF/TIA-hybrid), logga faktisk per-android-synlighet och 600-frame-rasterdata, behåll originalmasker och sex logiska androider. Inget tyst designundantag; **ingen merge, fullspelsutveckling eller ny fas**.

## MAIN – spelarstorlek och fyra ursprungsmasker (senaste visuella förtydligandet)

- **Användarbeslut:** gul spelare ska vara **lika stor som de stora androiderna** på skärmen och fortsatt ha hatt och vapen från originalsissen. Den nya jämförelsebilden är pedagogisk målskiss, **inte** en godkänd ny pixelmask eller autentisk Stella-bild.
- [Original 8×9-NPC-referenser (oförändrade)](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json) är importerade byte-identiskt ur huvudöverlämningens `assets/NPC_REFERENCE_8x9_masks.json`. Stora figurer har 9 synliga rader, små 6 inom samma 8×9-matriser. SHA-256 `1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`.
- [Spelarskalans MAIN-specifikation](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md), [samma i Drive](https://drive.google.com/file/d/1ZEq-8_69amjwSIEZFjroT0q2w-pTn_aY/view). Integrerat **förprov inom befintligt R1**, inte ny fas eller separat R1-acceptans.
- **Ingen ny ROM-byggning** eller oberoende verifiering följer av de visuella referenserna; **draft PR #7** får fortsatt inte merge innan blockerarna åtgärdats och separat VERIFICATION slutförts.

## MAIN:s två-silhuetters förprov v0.18 – rådgivande avgränsning

- [Teknisk analys av NUSIZ och sprite-/PF-konflikten](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_SPRITE_FEASIBILITY_V018_2026-11-15.md), [samma memo i Google Drive](https://drive.google.com/file/d/1LUEuhOVYcOw6rgey7kS_NTbXyCEFWKI6/view).
- **Förprov till R1, inte ändrat acceptanskrav:** verklig Stella-bild med **två olika 8×9-androidsilhuetter + spelare + skott på samma rasterhöjd**, och ett instruktions-/TIA-schema. Om detta misslyckas ska teknikförslaget revideras eller stoppas före uppskalning.
- **Slutkrav oförändrade:** sex androider R1, fem+nyckel R2, högerdörr R3 och R4; 16 fall enligt v0.18. `NUSIZ`-kopior ger inte automatiskt olika sprites och fria individuella X-positioner.
- Uppgiften kommenterad i [draft PR #7](https://github.com/Odourman/let-me-out/pull/7); separat [VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8) förblir oberoende och gäller fryst originalcommit.

## MAIN:s statiska rasterbudget v0.18 – nytt deluppdrag (inte egen ROM-verifiering)

- [Beräknad 6502-instruktionsbudget](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_RASTER_DELTA_V018_2026-11-15.md): både `FullLoop` och `BandLoop` i frysta utvecklarkällan har **74/76 CPU-cykler per normalt loopvarv**, innan faktisk Stella-kontroll. Resurskonflikt: P0 används för spelaren och P1 för nyckeln i R2, medan PF ritar grova androidblock.
- Debuggerskärmbilderna visar saknade `.script`, `.lst` och `.sym`-filer, vilket måste rättas innan fullständig Stella-mätdokumentation kan erhållas.
- **MAIN har kommenterat PR #7** med ett strikt avgränsat korrigeringsuppdrag inom redan godkända R1–R4: först objekt-/cykelschema, sedan prövad hybrid/PF-kernel, 600 faktiska sammanhängande Stella-bildrutor och explicit ny R3-dörrbedömning.
- **VERIFICATION Issue #8** gäller fortsatt fryst baseline-commit; inga omdömen från MAIN ersätter dess oberoende ombyggnad.

## Mottagen ROM DEVELOPMENT-leverans – MAIN preflight (2026-11-15)

- **Utvecklarbaseline:** [draft PR #7](https://github.com/Odourman/let-me-out/pull/7), commit `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, ROM SHA-256 `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`.
- **Mottagningsgranskning, inte oberoende verifiering:** [MAIN-rapport](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_REVIEW_ROM_V018_STELLA_2026-11-15.md), [arkiverad utvecklar-evidens i Drive](https://drive.google.com/file/d/1jGG6b_g8LSH_fyGe4pX9bsx0phQ0sDJ8/view).
- **5 utvecklar-PASS, 5 FAIL, 5 INCONCLUSIVE, 1 NOT_RUN.** Kritisk avvikelse: sex vita androider har inte igenkännbara silhuetter; nyckelhål och väggfärg brister; full 600-frame/CPU-cykelspårning saknas. DASM-byteidentitet är demonstrerad av utvecklarens CI, inte självständigt av VERIFICATION.
- **Beslut:** PR #7 förblir draft / ej merge. Begränsat tekniskt korrigeringsförsök inom samma auktoriserade R1–R4, inga spelregeländringar och ingen designwaiver.
- **Oberoende VERIFICATION väntar:** [Issue #8](https://github.com/Odourman/let-me-out/issues/8) med [separat intake](https://github.com/Odourman/let-me-out/blob/main/docs/VERIFICATION_INTAKE_ROM_V018_2026-11-15.md). Ingen ny senare ROM-fas får börja utan nytt tillstånd.

## MAIN v0.18 – uppdragsgrind auktoriserad; utvecklar-ROM blockerad

- **Design/analys steg 10 genomfört.** Avgränsat framtida ROM-test omfattar endast **R1** (sex androider, spelare, testsymbolskott), **R2** (fem androider, nyckel, spelare, skott), **R3** (endast högerdörr, orange och nyckelhål), **R4** (förprogrammerad raster-/nyckelskymningsstress).
- **16 definierade testfall** i originalgrinden. ROM DEVELOPMENT har nu lämnat en **egenkontroll med 5 PASS, 5 FAIL, 5 INCONCLUSIVE och 1 NOT_RUN**, men detta är inte oberoende VERIFICATION. Körbar F6/NTSC-ROM är byggd; **grafikacceptansen är blockerad**. Originaltestmatrisen är planeringsunderlag, den faktiska utvecklarmatrisen finns i PR #7.
- [Scope](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_SCOPE.md) · [Acceptans](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) · [Testmatris](https://github.com/Odourman/let-me-out/blob/main/planning/ROM_GATE_V018_TEST_MATRIX.csv) · [Oberoende verifiering](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_VERIFICATION.md).
- [Gemensam ZIP i Drive](https://drive.google.com/file/d/1FzQJWYYMzO0T18wxil079WxqmdboFPiw/view?usp=drivesdk) · [mobilrapport](https://drive.google.com/file/d/1gVhSzEX3UnD1UTm-nl4pwdwrtrRFFGm4/view?usp=drivesdk) · [Issue #6: separat uttryckligt kodgodkännande givet](https://github.com/Odourman/let-me-out/issues/6).
- **NTSC är uttryckligen auktoriserat** för första diagnostiken och utvecklaren har valt **16 KB F6**; detta utvidgar inte till PAL eller fullspel. **Godkänd diagnostik ska aldrig automatiskt öppna ett senare fullspelsuppdrag.**

## Ljuddesign v0.17 – fyra korta effekter

- **Redan beslutat i ursprunglig Master Spec:** ljud vid nyckelupptagning (+50), precis en gång.
- **Användarens föreslagna riktning:** stigande elektroniskt tjut när första verkligt avfyrade skottet gör androiderna aggressiva; androidförstörelseljud och kort skottljud.
- **MAIN:s testrekommendation:** fyra ljud totalt (jaktlarm, skott, androidförstörelse, nyckelupptagning). Ingen bakgrundsmusik eller kontinuerligt jaktljud. Tekniken använder TIA:s två ljudkanaler.
- **Fortfarande preliminärt:** exakta tonhöjder, längder, ljudprioritering, slutlig ljudpalett och samtidiga effekter. **Inget ROM-ljud byggt.**
- [Ljudspecifikation v0.17](https://github.com/Odourman/let-me-out/blob/main/docs/SOUND_DESIGN_V017_2026-11-15.md) och [identiskt originalunderlag i Drive](https://drive.google.com/file/d/1bm19imkHic0zPSvDk-MGJ5842VfQtuWS/view).

## Källor och isolation

- [Let Me Out! i Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) – arton versionerade ZIP-arkiv från huvudöverlämningen till den färdiga ROM-grinden v0.18, inklusive manifest, samt status-/färdplanfil (O1-beslut), Game Over-/RESET-beslut, kartdata JSON och mobilrapporter/RGB-skisser.
- [GitHub-förrådet](https://github.com/Odourman/let-me-out) – egna projekttexter, inga tredjeparts-ROM:er.
- Ändra aldrig **The Cabin** eller **I Love a Fish** som del av detta projekt.
- **Linear används inte för Let Me Out!** (användarbeslut 2026-11-15). Arbetsuppgifter hanteras vid behov i GitHub Issues.

**Auktoritet:** Senare direkta användarbeslut > registrerade spelbeslut > experimentella modellförslag > tredjepartsresearch.  
**Detta är en statusöversikt**, inte ersättning för originalbeslutsregistret.