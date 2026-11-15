# LET ME OUT! – ROM DEVELOPMENT till MAIN – Venetian Blinds v0.18

**Datum:** 2026-11-15. **Slutsats: FAIL/BLOCKED som full R1-rendering.** Detta är ROM DEVELOPMENTs egenkontroll, **inte oberoende VERIFICATION**. PR #7 ska förbli **DRAFT**. Ursprunglig verifieringsbaseline `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` ändras inte.

## Kontrollerad käll- och beslutsordning

- Projekt och auktorisation: GitHub `Odourman/let-me-out`, Issue #6, endast NTSC v0.18 och R1–R4. Ingen fullspel-, PAL-, v0.19-kart- eller specialhårdvaruimplementation. Den frysta baseline-committen används inte som utvecklingsyta.
- Projektkällor: CURRENT_PROJECT_STATE, MAIN_DECISION_LEDGER_SUPPLEMENT, ROM_GATE_V018_AUTHORIZATION/SCOPE/ACCEPTANCE/BLOCKERS/VERIFICATION, 16-testmatrisen samt `design/NPC_REFERENCE_8x9_masks.json` är öppnade och kontrollerade.
- Research som underlag, inte beslut: Drive `LET_ME_OUT_RESEARCH_TILL_MAIN_2026-11-15.zip` SHA256 `52c9c3f70532d22570139d98ff25d969c282c2dcb1999a1d2ff8986aa8772a21`, 67-problem-matris SHA256 `deaf0f5adf4ef1f6852faae1bb2f9f203714000ff4086bf371fd50aa74ff127c`. Studerade Video Chess/Venetian Blinds, Space Invaders/NUSIZ, RESP/HMOVE, PF, VDEL och tvålinjerskernels. Ingen kopierad kommersiell assemblerkod.

## IMPLEMENTERAT / BYGGT

Tre *separata originalskrivna* 6502-program på samma godkända NTSC/F6-basis:

1. `vb_9_interleave.asm`: stor man på jämna scanlines, stor kvinna på udda scanlines, originalens två oförändrade 8×9-masker som källdata; nio linjers band. `P1` ompositioneras med tidsstyrd `RESP1` utan NUSIZ-kopior. Två oberoende X-/delays-tabeller växlas i VBLANK. P0 = fullhöjdsgul 9-raders spelarkandidat, M0 = testsymbolskott.
2. `vb_18_doubled.asm`: 18-raders förstorad jämförelse med växelvis originalrader, **inte** godkänd ny skala.
3. `vb_9_vdel.asm`: 9-linjers VDEL1-latchprov. I första körningen fanns en felaktig lång restlinje; en extra `STA GRP0` efter `STA GRP1=0` korrigerar latch-clear. Endast **korrigerad** binär levereras som senaste variant.

Riktig DASM 2.20.14.1 (`2.20.15~20201109+really2.20.14.1-2` Ubuntu-paket) ger tre 4 096-byte bankbilder och tre 16 384-byte F6-binärer genom att upprepa identisk kodbank fyra gånger. Alla sex binärfiler har kontrollerats med `sha256sum -c`. Fullständig källa, `.lst`, `.sym`, verktygsloggar, byggskript och checksummefil finns i arkivet. F6 tillför ingen ny TIA-resurs.

**ROM SHA256:**
- 9-linjers: `84353409b5683c65644476e6c9ad852ae6acd320d4818d62fcdd32a6c721aa85`
- 18-linjers: `2f3dd7c3dd51f38bc70fbc1647e93ca5324d9a3f4037080337e7389a79cb929e`
- 9-linjers VDEL korrigerad: `60ceb07344d6d1b0fec69f85e4239ff8e2318fe1dc9d2c92f3ca764a581ebccf`

## TESTAT I VERKLIGA STELLA 6.7.1

GitHub Actions Ubuntu24.04 körde tre ROM-varianter under Xvfb med debuggerautoexec och `frame #13` respektive `#18`, vilka är olika faser med förändrade begärda X-lägen för *båda* androidernas källtider. Sex **oredigerade** 1366×900 Stella Debugger-PNG bevaras med DASM-symboler och maskinlistning. `VENETIAN_MEASUREMENTS.json` och CSV härleds endast från dessa riktiga Stella-skärmbilders pixlar, med rå bild-SHA256 per bild. Beskurna förstorningar är märkta separat.

| Prototyp | Vitt GUI-pixelmönster per observerad bildruta | Observerade vertikala rader | Resultat |
|---|---:|---:|---|
| 9 interleaved | 48 vita GUI-pixlar inom GUI-X 158–173 | 5 | Ingen andra 8×9-person vid oberoende X – FAIL |
| 18 doubled | 84 vita GUI-pixlar inom GUI-X 158–173 | 10 | Större/sammanhängande figur, men ingen andra person; skalan ej godkänd – FAIL |
| 9 + VDEL1 | 20 vita GUI-pixlar inom GUI-X 162–185 | 4 | Få fragment vid två X, ingen andra fullständig människa – FAIL |

Stellas HUD visar **262 scanlines i alla sex fångade rutor**. Gula spelaren syns med nio pixellinjer; separat M0-skott syns. Ingen 600-följande-bildrutorsprovning har gjorts för **dessa nya** ROM:er, eftersom A1 (två oberoende fullt läsbara androids i samma frame) inte klarade minimitestet. Tidigare 600+600 på `six_x_free` är en annan, redan misslyckad A/B-arkitektur och överförs inte som PASS.

**Begärd X och faktiskt observerad X:** Källkodens `MALE_REQ_X`/`FEMALE_REQ_X` beräknas från individuella tabeller. Båda förändras mellan testfaserna. I de inspelade Stella-bilderna kvarstår emellertid vita bildpunkter i i stort sett samma vänstra x-grupp, medan ingen komplett andra silhuett syns. Därmed har den begärda koordinaten inte visats motsvara en självständig fullständig renderad spriteposition. En display med två grupper av enstaka fragment är inte en av de två fullständiga godkända 8×9-människosilhuetterna.

## Venetian Blinds maskförlust – *teoretiskt* lägsta kostnad utan visuella artefakter

Om originalets nio rader fördelas på två logiska figurer på växelvisa rasterrader, får den stora mannen bara 5/9 vertikala rader och kvinnan 4/9 **inom samma bildruta**. Manmasken har 28 påslagna bitar: endast 12 av 28 finns på jämna rader (16 saknas). Kvinnmasken har 38 påslagna bitar: endast 20 av 38 finns på udda rader (18 saknas). Dessa siffror kommer från exakta ursprungliga bitmap-data och är en **källmaskberäkning, inte uppmätta Stella-pixlar**. Ett 18-raders prov kan använda fler originalrader men blir dubbel höjd, vilket användaren inte har godkänt. Växling mellan bildrutor kan komplettera rader men lägger till tidsflimmer och återstår **otestat i denna kod**.

## Kritisk TIA/CPU-resursplan – **statisk beräkning**, EJ faktisk write-trace

| Resurs | Planerad användning | R1-utfall | R2-risk |
|---|---|---|---|
| P0 + COLUP0 + GRP0 | Gul fullhöjdsspelare | Synlig i provet | Kan inte utan vidare lånas ut till NPC samtidigt |
| P1 + COLUP1 + GRP1 + RESP1 + HMP1/HMOVE | Växlande original-NPC-rader | Två separata 8×9-figurer ej uppnådda | P1 krävs eventuellt för guldnyckeln |
| M0 + ENAM0 | Testskott | Synligt | Fortsatt upptaget |
| NUSIZ0/NUSIZ1 | Inga kopior i ny variant | NUSIZ1=0, oberoende X *begärda*, ej full renderade | Kopiefunktion ger fasta avstånd, inte fria positioner |
| VDEL1 | En extra bildrutefördröjd P1-latch | Fragment, ej nytt hardware sprite | Fördubblar inte P1-kanaler |
| PF0/PF1/PF2 + COLUPF | Noll i denna A-kernel | Inga väggar | Tidigare B:s grova kroppar uppfyllde inte 8×9; dessutom krävs bruna väggar |
| M1/BALL | Ej utnyttjade | Inte 8-bitars sprites | Kan inte automatiskt ersätta högupplöst nyckel eller människor |

**En belastad 6502-rasterlinje** använder `STA WSYNC; LDA #bitmap; STA GRP1; LDX delay; DEX/BNE; STA RESP1; LDA #player; STA GRP0; LDA #shot; STA ENAM0; STA WSYNC`. Räknat efter första `WSYNC`-gränsen: `STA GRP1` c5, `STA RESP1` c(10+5n), `STA GRP0` c(15+5n), `STA ENAM0` c(20+5n), nästa `WSYNC` c(23+5n). För n=4/5/8/9 är nästa WSYNC c43/c48/c63/c68 av **76 CPU-cykler** (se `CYCLE_PLAN.csv`). Inga indexed-pagecrossings i de unrollade synliga raderna; BNE-grenarna räknade som n−1 tagna och en sista otagen. **Dessa är beräknade 6502-cykeltal**, INTE faktisk Stella-TIA-write-historik eller ett bevis för rätt pixeldeadlines. TIA-registers senare felplacerade bilder bekräftar att en cykelbudget under 76 inte räcker.

**RAM:** `$80`=bildruteindex, `$81`/`$82`=delays, `$90`/`$91`=begärda NPC-X, `$92`/`$93`=spelare/skott, totalt 7 namngivna RIOT-byte (stack tillkommer); ingen extra cart-RAM. Inget PAL, inget F6SC, ingen ARM/DPC+.

## Instrumentering – exakt vad som fungerar och inte fungerar

- Fulla Stella GUI-bilder: **fungerar** och visar frame-ID + 262 scanline-HUD för 6 provbilder. Bildernas pixelmönster mäts reproducerbart.
- `logTrace` i den installerade Stella 6.7.1: körning men ingen persistent användbar TIA-register-/CPU-write-logg; **INCONCLUSIVE**, kan inte markeras PASS bara på kommandot.
- `trapWriteIf` för `$11` (RESP1): försökt på scanline 120 och 121; ingen verifierad paus vid registrerad TIA-skrivning; **INCONCLUSIVE**.
- PC-brytpunkter mot assemblerad kod `$F0A8` / `$F0BD`: debuggerbilderna står i **PC `$F047`, scanline 0, cycle 7** vid frame13, alltså inte vid de avsedda `RESP1`-instruktionerna. De ger därför **inte** ett mätvärde på skrivcykeln. **T07 INCONCLUSIVE**. Full registertrace saknas.

## STATUS mot 16-testerna

Se `TEST_MATRIX_V018_VENETIAN_DELTA.csv`: 2 × `LOCAL_PASS` (T14, T16), 2 × `FAIL` (T02, T04), 2 × `INCONCLUSIVE` (T01, T07), 10 × `NOT_RUN`. Detta avser **enbart nya Venetian-Blinds-proverna**. Tidigare R1 A/B 600-frame-resultat är historiska separata misslyckanden; R2/R3/R4 har inte testats med den här nya koden. Oberoende T15 får inte ärvas.

## NÄSTA TEKNISKA BESLUTSPUNKT – MAIN

Den närliggande Video Chess-idén har prövats praktiskt men **gav inte ens två** fullständigt läsbara och självständigt placerade NPC i samma rasterhöjd, samtidigt med P0 och M0. Familj B:s tidigare real-Stella 600-bildrutors PF/P1-hybrid gav redan sex grova vita kroppar men inte fyra igenkännbara människosilhuetter (47–59/72 uppskattad bitmatch). Ingen av de genomförda familjerna har uppfyllt full R1. Detta bevisar **inte** att all vidare Atari 2600-teknik är omöjlig; det är däremot ett faktiskt tekniskt STOPP för nu testade implementeringar. Ingen oauktoriserad designwaiver genomförs: inga färre NPC, inga generiska former accepterade, inga hitbox- eller PAL-/kart-/specialkassetthårdvaruändringar. R2-nyckelkonflikten och R3/R4 kvarstår. MAIN bör inte ge full R1 PASS och bör besluta om eventuellt separat prioriterat fortsatt kernelarbete som en ny avgränsad uppgift; VERIFICATION oberoende om ny commit blir kandidat.

**GitHub-gren:** `rom-dev/v018-ntsc-diagnostic`, PR #7 förblir DRAFT. **Stella Actions-run:** https://github.com/Odourman/let-me-out/actions/runs/43770158692 (kod vid commit `e06c253629f9fe26bfe3879dc98f7527b59bbf32`). **Projektets ursprungliga frysta VERIFICATION commit:** `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`.
