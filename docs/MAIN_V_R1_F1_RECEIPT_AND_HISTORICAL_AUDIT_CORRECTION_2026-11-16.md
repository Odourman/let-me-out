# LET ME OUT! – MAIN V: R1-F1 mottagen, korrigerad R1-historik
**Datum:** 2026-11-16. **Typ:** MAIN:s käll- och dokumentgranskning av fryst utvecklarleverans, ej oberoende VERIFICATION, ROM-merge, designwaiver eller ny utvecklingsauktorisation.

## 1. Exakt fryst leverans
- [ROM DEVELOPMENT II:s R1-F1-rapport](https://github.com/Odourman/let-me-out/blob/ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F1.md), branch `rom-dev/v018-r1-f1-sixmask-forensics-20261116`, HEAD `ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a`.
- Auktoriserad F1-order: [MAIN V till ROM DEVELOPMENT II R1-F1](MAIN_V_TO_ROM_DEV_II_R1_F1_SIX_MASK_TIMING_FORENSICS_AUTHORIZED_2026-11-16.md). Utgångsbas R1 `b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0`, oförändrad.
- Fullständig original-R1 ZIP i rätt projekt-Drive: https://drive.google.com/file/d/1j8r7vzgKmx_XiRRzvZKGFZWlJ776t3F1/view. F1-delarkiv och CSV ligger i [rapporten](https://github.com/Odourman/let-me-out/blob/ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F1.md).
- GH Actions riktade, verifierat via API `success` för **43919329143**, **43920307403**, **43921122338**, **43921910809**, på olika F1-förstadiecommits. Dessa är **utvecklar- och CI-tester, inte oberoende verifiering på enbart slut-HEAD**. Den äldre generella R1-körningen `43913227299` förblir röd.
- MAIN har läst full teknisk rapport, ursprunglig `analyze_six_sweep.py`, korrigerande `r1_f1_archive_reaudit.py` och enskilda CI-körningars statuser. MAIN har **inte** hämtat ned varje ZIP-byte eller genomfört en helt oberoende Stella-rebuild. Läs inte dokumentkontroll som verifieringsgodkännande.

## 2. Kritisk supersession av gamla R1:s generella "0/80"
Det äldre `analyze_six_sweep.py` kör `len(groups)==n` där `n` är en **sträng** som `'6B'`, medan `len(groups)` är heltal. Därmed returnerar den gamla pixelklassificeringen automatiskt `False` även för verkligt korrekta 6B-bilder. Detta typfel finns kvar **i ursprunglig fryst R1-källa** som evidens och bör inte ändras retroaktivt.

- **N5, fast X:** enligt F1:s nya läsande analys av 16 oförändrade råa Stella-PNG: **16/16** källkorrekta fullmasker.
- **6B, fast X:** enligt F1:s nya rå-PNG-revision **16/16 sex källkorrekta originalmasker vid fasta X**; ROM SHA256 `36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4`. Detta **ersätter** äldre påståendet att 6B var 0/16.
- **6C före A/B, fast X:** **0/16** med verklig x0-ghost, sista masken vid högra bildkanten, delvis övertäckt av aktivt M0. Vissa äldre missade "vita pixlar" var gula M0-pixlar eller utanför spelplanens synliga gräns. ROM SHA256 `c9c71fb9c41cee3d1c5bb4839c7d4bbea759151e4e49510b98d4ed3ad2f03c58`.
- **6C-F1AB, exakt en fasvariant:** sista RESP1 c67 -> c65 och GRP1 c70 -> c68; sista start-X i Stella crop 309 -> 297 (6 färgklockor). Riktig Stella audit av 16 rutor rapporterar **16/16 korrekta sex originalmasker vid fast X**, ingen x0-ghost. ROM SHA256 `d07387b4da66a4fd41dd782cc86252d36282eea0805cb8899e59cb189f1eabdb`.
- Sexschemana **6A, 6D och 6E har inte omgranskats** i F1 och har varken retroaktivt PASS eller förnyat bevisat FAIL i detta tillägg.

**MAIN:s korrigering:** Det generella påståendet **"0/80 pixelperfekta sexmaskbilder" är sakligt opålitligt och får INTE längre användas som projektets aktuella sanningsvärde.** Ett framgångsrikt 6B-kontrollfall bland de tidigare räknade 80 har nu påvisats. Historisk R1-rapport behålls fryst med hänvisning till denna supersession. Även den ursprungliga R1-delmatrisens `T02/T04=FAIL` avser *hela fri-X/Y-kravet*, inte att exakt sex originalmasker aldrig kan visas på en enda rasterhöjd.

## 3. Autentiska TIA-mätningar och begränsningar
- F1 rapporterar verklig Stella 6.7.1 debugger på frame 12, bank 0, scanline 123/källrad 05: 6B sex `RESP1` skrivcykler 19/28/37/46/56/66 och fyra faktiska `GRP1` c22/40/59/69; 6C `RESP1` c20/29/38/47/57/67 och `GRP1` c23/41/60/70. Positiv N5-kontroll finns. Första c19-provet togs om för korrekt GUI-trap. Ursprungliga felradstaggar återanvändes inte som bevis.
- Käll- och pixelbevis stödjer F1-rapportens **F1-CAUSE_IDENTIFIED** inom 6B auditbugg och 6C:s sista sprite-start vid skärmkanten. Detta är **utvecklarens avgränsade resultat**. Det är inte ett bevis för ett komplett, generellt X/Y-styrt sexandroidspel eller att sex sprites skulle kunna använda P1 utan positionsrestriktioner.
- `NUSIZ1=$01` initieringsskrivning på motsvarande sexmask-ROM är källkontrollerad men inte själv uppmätt i senare frame 12: **påstå inte att varje init-register fångats av verklig trap**.
- Fortfarande öppet: sex *individuellt fria* X/Y över hela rummet, varianter med nära/överlappade X/Y, kontinuerliga 600 sexmaskbilder under rörlig X/Y, sexmaskens completa worst-case-registerprofil, R3:s P1-port på samma frame, oberoende clean rebuild och slutlig designacceptans.

## 4. MAIN:s beslut
**R1-F1 mottagen som `F1-CAUSE_IDENTIFIED / DEVELOPER_LOCAL` och avslutad inom sin snäva arbetsorder.** Inget ytterligare F1-arbete krävs just nu. Full R1 är alltjämt **BLOCKED / NOT ACCEPTED** för sex fritt och individuellt X/Y-positionerbara originalandroider. R3 isolerad DEVELOPER_LOCAL_PASS kvarstår. R2 och R4 är inte beställda, R1+R3-integration inte beställd, PR #7 draft/omergerad, Issue #8 fryst/vilande, VERIFICATION STANDBY.

**Nästa teknikfråga:** på en ny av MAIN separat auktoriserad, snävt avgränsad R1-uppföljning behöver man pröva *om ett redan pixelkorrekt sexmask-fall med fast X kan omvandlas till sex individuellt fritt valda X och Y utan originalmask-/positionskoppling*. Tydliga falsifierbara gränser krävs. **Ingen sådan ny kodorder utfärdas genom detta mottagningsdokument.**

Övriga tidigare beslut och användarens grafiska canon oförändrade.
