# LET ME OUT! – MAIN IV – kontroll och samordning 2026-11-16

**Projekt:** Atari 2600-spel `Let Me Out!`; repository [Odourman/let-me-out](https://github.com/Odourman/let-me-out); [dedikerad Google Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).  
**Rapporttyp:** MAIN-kontroll, bevisinventering och nästa avgränsade diagnostikarbete. **Ej ny spelcanon, ej utvecklarens fullständiga leverans, ej oberoende VERIFICATION.**

## 0. SENASTE MAIN IV-DELTA – integrerat R1ba, 2026-11-16

**FORSKNING (ej full acceptans): [R1ba 600/600 Stella SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43884511590).** En **och samma ROM** visar sex fullständiga originalmasker (2 stora män, 2 stora kvinnor, 1 liten man, 1 liten kvinna), **tre växlande X-lägen**, **tre växlande Y-profiler**, **två bruna speglade PF-sidoväggar**, full gul P0-spelare, ett statiskt testsymbolskott M0 och 262 NTSC-scanlines under alla 600 verifierade lokala bildrutorna. **Noll saknade/extra vita maskpixlar.** ROM **16 384 byte**, SHA256 `41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`. X/Y-lägena är fortfarande **tre ihopkopplade, förberäknade uppställningar**, inte sex individuellt fria X/Y.

- [Detaljerad R1ba-forskningsrapport i GitHub](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ba-integrated-xyz-pf-20261116/docs/MAIN_IV_R1BA_INTEGRATED_X_Y_PF_SIX_ORIGINALS_600_STELLA_2026-11-16.md).
- [Komplett originalbevis: GitHub Actions ZIP, 600 Stella PNG](https://github.com/Odourman/let-me-out/actions/runs/43884511590/artifacts/14233733448).
- [Verifierad Google Drive ZIP-kopia i projektmappen](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view?usp=drivesdk), **3 930 298 byte** och lokalt kontrollerad ZIP SHA256 `f8dd41e62939aa1699d80f70df0c5b5081b87441a1e2c740ff2786139908f325`. Arkivets 622 poster och alla 600 original-Stella-bilder var läsbara; intern ROM-hash matchade manifestet.

**Fortfarande BLOCKED full R1/v0.18:** individuellt fria X för sex NPC, fria Y och oberoende kombinationer, aktiv shot-/kollisionsstress, R2 nyckel + O1, asymmetrisk högerdörr R3 med orange markör och svart nyckelhål, T07 verklig write-cycle-trace och oberoende VERIFICATION. Inte ett godkänt fullspel, ingen waiver, ingen produktionsmerge eller ny implementeringsfas.

## 1. Auktoritet och nuvarande fas

1. Direkt användarbeslut och originalhandoffens 57 beslut är fortfarande styrande. [MAIN:s kompletterande 11 besluts-/statusposter](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) kompletterar, inte ersätter, dem.
2. [Uttrycklig auktorisation 2026-11-15](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md) / [Issue #6](https://github.com/Odourman/let-me-out/issues/6): **endast NTSC/F6 vid behov, diagnostik v0.18 R1–R4**. Ingen full spelkod, AI, ljud, poängsystem, ny mapper, PAL eller senare implementeringsfas. Äldre Drive-scope eller status som säger ”kod ännu inte auktoriserad” beskriver ett historiskt läge och får inte överstyra den senare uttryckliga auktorisationen.
3. [Acceptanskriterier](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) A01–E04, [testmatris](https://github.com/Odourman/let-me-out/blob/main/planning/ROM_GATE_V018_TEST_MATRIX.csv) T01–T16 och [VERIFICATION-kontrakt](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_VERIFICATION.md) står kvar utan sänkta krav.
4. Det tidigare valda kartsetet **A01/B01/C02/D01** är kvar som planerad bas. `A_OPEN_01`–`D_OPEN_01` från designstudie v0.19 är **kandidater**, inte godkänd kartcutover. Sex humanoider: 2 stora män, 2 stora kvinnor, liten man, liten kvinna. Gul spelare lika stor som de stora. Endast höger utgång, orange port och svart nyckelhål som visuella mål. O1-nyckelskymning, K1/E1 och RESET-regeln består.
5. Repo `main` var vid pre-write-kontroll `f6b3fc76c59161e04e583dc8c0787332d2f261c7`. [Produktionsutkast PR #7](https://github.com/Odourman/let-me-out/pull/7) var fortfarande **draft/open, ej mergad** på `82667dae033f70570dce903f8e1d4866528be02a`. Detta MAIN-dokument ändrar **bara dokumentation**, inte ROM-kod.
6. [Oberoende VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8) gäller äldre fryst commit `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` och får inte användas som PASS för senare forsknings-ROM:er.

## 2. Verifierade lokala forskningsprov 2026-11-16

**Här betyder PASS endast egen CI-/Stella-pixelkontroll på exakt angivet, avgränsat research-scope.** Det är aldrig liktydigt med full C01/C04, T01–T16, oberoende verifiering eller merge-tillstånd.

| Forskningsserie | Faktiskt uppmätt resultat | Viktig begränsning |
|---|---|---|
| [R1aq, run 43866445424](https://github.com/Odourman/let-me-out/actions/runs/43866445424) | 2 × 600/600 autentiska Stella-bildrutor: 2 stora man-masker, 2 stora kvinna-masker, 1 liten man, 1 liten kvinna; full gul P0 + en M0; original 8×9 helt intakta; NTSC 262 | Fasta NUSIZ-relaterade X-separationer |
| [R1at runtime-three, run 43868138075](https://github.com/Odourman/let-me-out/actions/runs/43868138075) | 600/600; samma ROM växlar mellan 3 X-uppställningar; separata förflyttningar för stor mansgrupp respektive stor kvinnogrupp | Gruppförflyttning, inte 6 individuellt fria X |
| [R1au one-group walk, run 43869049214](https://github.com/Odourman/let-me-out/actions/runs/43869049214) | 600/600 kontrollerade steg A–B–C–B–A, bara en stor grupp byter X per övergång | Begränsade förkompilerade positioner |
| [R1ay, run 43871126664](https://github.com/Odourman/let-me-out/actions/runs/43871126664) | 3 × 600/600, totalt **1 800/1 800** real-Stella-bilder med olika intilliggande Y-profiler för småmasker; noll vita pixelavvikelser | Olika statiska ROM-varianter; inte allas fria Y |
| [R1az, run 43871769128](https://github.com/Odourman/let-me-out/actions/runs/43871769128) | 600/600, **en** ROM med tre växlande små-NPC Y-profiler. 297/151/152 bilder per profil, alla sex 8×9 originalmasker hela, P0/M0 och 262 NTSC | Y via 3 förberäknade lägen, stora NPC står kvar, PF saknas |
| [R1ax, corrected run 43883269341](https://github.com/Odourman/let-me-out/actions/runs/43883269341) | **600/600 local PASS** for mirrored brown PF side walls, all six source-exact white masks, yellow P0 and one M0, 262 NTSC; three observed runtime-X layouts, zero missing/extra white. ROM SHA256 `64ba6cd5152a395737b2c41607b0a9e54c7836319bbed2bfee9bfdc6af1f81d1`. Controls PF-off and nonreflected PF each FAIL side-wall criterion, as expected. | Real measured **PF technical baseline** only: does not prove R3 right-only unlocked opening, orange port or black keyhole, and does not solve six independently free X. |

Originalgrafiken har inte förenklats för dessa delprov. De upprepade F6-experimentfilerna består av fyra lika 4 KiB-banker; de bevisar **inte** att F6-bankswitching i full diagnostik är löst.

Mer detaljer: [R1ay-överlämning](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ay-neighbor-y-six-source-masks-20261116/docs/MAIN_IV_R1AY_SIX_ORIGINAL_NPC_STAGGERED_Y_1800_STELLA_2026-11-16.md) och [R1az-överlämning](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1az-runtime-three-y-profiles-20261116/docs/MAIN_IV_R1AZ_RUNTIME_THREE_Y_PROFILES_SIX_ORIGINALS_600_2026-11-16.md).

## 3. Faktiska öppna blockerare enligt accepterade testkrav

- **R1/C01, individuell X:** Målet kräver sex oberoende logiska X-positioner och samtidigt synliga, läsbara originalmasker. Kopplade NUSIZ-kopior i flera begränsade uppställningar är positiv teknikforskning, men inte full fri X eller riktig original-ROM-belastning med väggar och aktivt spelflöde. Kombinerat X+Y+PF i **en och samma ROM** måste provas.
- **R1/B02/T07:** Ingen komplett, oberoende verifierad register-write-trace för de senaste experimenten med scanline, STA RESP1/GRP1, CPU-cykel och samlad budget på 76 CPU-cykler per linje. 262-scanline-HUD och skärm-PASS ersätter inte cykelspår.
- **R2/C02:** Fem androidmasker plus guldnyckel, P0 och M0 på samma Y, O1 skymning och oförändrat logiskt nyckel-X/Y med återkomst: ej visat i de aktuella R1aq–R1az-delproven.
- **R3/D01–D03:** Asymmetrisk **endast höger**-öppning, vänstervägg stängd, orange port och svart nyckelhål i faktisk Stella: ej visat. Speglad brun sidovägg är högst ett tidigt PF-basprov.
- **R4/T08:** Färre förkompilerade X- och Y-lägen ger rasterbelastningsdata; inte full belastad scen med samtidiga positionskorsningar, nyckelåterkomst och PF.
- **E01–E03/T14–T16:** Komplett leverans för R1–R4, ren separat rebuild och signerat oberoende VERIFICATION saknas. Utvecklarens gamla 5 PASS / 5 FAIL / 5 INCONCLUSIVE / 1 NOT_RUN är historiskt för PR #7 och får inte överföras till forskningskärnorna.

**MAIN-beslut:** v0.18 är **BLOCKED / NOT ACCEPTED** som full diagnostik. Ingen automatisk waiver, kartändring eller produktionsmerge.

## 4. Prioriterat arbete inom oförändrad befintlig auktorisation

1. **R1ax slutförd som lokalt delprov:** bruna speglade sidoväggar, 600/600 i Stella med bevarad P0/M0 och alla sex masker. Både felklassade förtest och senare godkänd färgseparerad analys bevaras; inget R3-högerdörr-PASS följer.
2. **R1ba integrerat delprov slutfört med 600/600 local PASS.** Nästa inom befintlig v0.18 R1/R4-forskning: testa frikopplade X-/Y-profiler (minst en oberoende korsningskombination) eller dokumentera varför sex individuella X inte ryms utan visuell eller designmässig kompromiss. Mät en riktig TIA-register-/CPU-cykeltrace i Stella, inte enbart en statisk cykelbudget.
3. Därefter förbered separata **R2**- och **R3**-teknikscener på det redan beviljade diagnostikuppdraget, men låt ROM DEVELOPMENT utföra och egenkontrollera sin kod. MAIN prioriterar och mottagningsgranskar; VERIFICATION gör senare självständig ombyggnad och test.
4. Stoppa förslaget om samma-R1-acceptans ifall sex självständiga X eller riktig scenvisning inte kan uppnås: dokumentera blockerare och högst två tekniska alternativ utan att ändra objektantal eller grafiska mål.

## 5. Käll- och systemintegritet

- GitHub är versionskontroll och källspårning. Google Drive är beslut-/rapportarkiv. Samma MAIN IV-checkpoint bör finnas i båda; äldre rapporter skall inte skrivas över.
- Beslut måste återföras till separat explicit beslutslogg först vid faktiskt användarbeslut. Detta dokument **ändrar inga användarbeslut**.
- Endast `Odourman/let-me-out` och dess dedikerade Drive-mapp omfattas; ändra inte The Cabin, I Love a Fish eller Linear.
- R1ax är **nu 600/600 LOCAL_RESEARCH_PASS** för speglad brun PF-sidovägg, inte för full R1 eller asymmetrisk högerdörr. Oväntade PF-väggspixlar klassades om korrekt i pixelgranskaren utan att ROM-koden ändrades.

**MAIN IV, koordineringsnotering 2026-11-16.**
