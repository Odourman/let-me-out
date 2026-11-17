# LET ME OUT! – STARTA HÄR / PROJECT SOURCES V4


**LÄSANVISNING V4:** Tidigare versioners källangivelser, gamla GitHub Issues, initiala ROM-beställningar och äldre framtidsförslag är historiska vid sina respektive tidpunkter. Högre auktoritet och senare uttryckliga användarbeslut gäller inom exakt beslutat ämne. Ingen source-only-status är fysisk Atari/Stella-verifiering. Detta källpaket ger ingen ny teknisk auktorisation.

**MAIN VII, version V4, 17 november 2026, efter G5AA och ny inventering.** Klass: **KÄLLNAVIGERING OCH FRYST STATUSSNAPSHOT**. Detta är varken spelcanon, godkänd ROM, teknisk verifiering eller arbetstillstånd. Läs det här dokumentet först; hämta sedan alltid **aktuella original** vid statusfrågor.

## Aktuella originalingångar

| Fråga | Gå till aktuellt original |
|---|---|
| **AKTUELL STATUS, roll och arbetskö** | [Gällande status-/auktoritetsindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [Drive-spegel](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit) |
| Förra fullständiga inventeringen | [G5AB: GitHub/Drive/Project Sources](https://github.com/Odourman/let-me-out/blob/main/docs/project_sources/PROJECT_SOURCES_MAIN_VII_V3_CURRENT_AUDIT_AFTER_G5AA_2026-11-17.md) (historisk revisionssnapshot) |
| Formellt nuläge och ägda beslut | [Current Project State](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md) och [MAIN Decision Ledger](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) |
| G5-status och implementationsspärr | [G5 Authority Boundary](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md) |
| Senaste tekniska G0-resultat | [G5AA-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) och [fryst ROM DEVELOPMENT III G5Z-rapport](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md) |
| Nya exakta kartor | [G5X urvalsmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) och [LM-D17/LM-D19](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md) |
| Fem fiender, AI, score och spawn | [LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) och [LM-D14–16](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Ursprungliga spelbeslut | [Master Spec och 57 ursprungsbeslut, historiskt arkiv](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), samt [G1 auktoritetsgranskning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G1_AUTHORITY_DIFF_2026-11-17.md) |
| Projektöverlämningar / roller | [VERIFICATION II](https://github.com/Odourman/let-me-out/blob/main/docs/VERIFICATION_II_MIGRATION_HANDOFF_2026-11-17.md), [GRAPHICS II](https://github.com/Odourman/let-me-out/blob/main/docs/GRAPHICS_HANDOFF_TO_NEW_CHAT_2026-11-17.md), [RESEARCH II](https://github.com/Odourman/let-me-out/blob/main/docs/research/RESEARCH_I_TO_II_HANDOFF_2026-11-17.md) |

## Status vid V4-pakettillfället

- **G5Z G0 H4-ONE source-only** är utfört av ROM DEVELOPMENT III, mottaget av MAIN VII i G5AA som **`G0_INCONCLUSIVE_NO_ROM`**. Inga nya ASM/ROM/Stella-bevis uppstod.
- **G5 FORMAL = OPEN**. **G1/G6/F12/ny ROM/ny Verification/merge = EJ AUKTORISERADE** av detta paket. ROM-workorder LM-D20 är **förbrukad/avslutad**, inte kvarstående för utförande.
- Framtida *exakta* kartmål godkända: **`A_OPEN_01` / `B_OPEN_02` / `C_OPEN_01` / `D_OPEN_01`**. Källval är **inte** införda i ROM och historiska v0.11-kartor bevaras.
- **Fem fiender** M,M,F,SM,SF, **fri logisk individuell X/Y**, -30 per kill, fem förhandsvaliderade spawns och 1/5 nyckelbärare är senare godkända **framtida design-/testmål**. Historiska v0.18 sexfienderstester förblir frysta.
- O1 ger endast kortvarig nyckelskymning vid **faktisk pixelöverlapp** med NPC, inte generell same-Y-osynlighet eller godkänt 10 Hz-flimmer.
- [PR #7](https://github.com/Odourman/let-me-out/pull/7) är historisk blockerad draft. [Issue #8](https://github.com/Odourman/let-me-out/issues/8) gäller uppskjuten historisk oberoende verifiering; [Issue #12](https://github.com/Odourman/let-me-out/issues/12) är stängt som genomfört G0 source-only. Äldre [Issue #3](https://github.com/Odourman/let-me-out/issues/3) och [Issue #6](https://github.com/Odourman/let-me-out/issues/6) är också administrativt stängda som historiska/supersederade, **inte** som ROM-PASS.

## Auktoritetsordning

1. Ursprungliga och senare uttryckliga användarbeslut samt bindande Master Spec i de områden som inte ersatts.
2. Giltiga fastställda scope-/beslutsdokument med exakt supersession och versionsankare.
3. Faktisk fryst implementation, rå-Stella, reproducerbar ROM och **oberoende** verifiering för påståenden om teknisk funktion.
4. Research, grafikrenderingar, jämförelsekartor, offline-simuleringar: **rådgivande**.
5. Dessa sex Project Sources, minnen och äldre sammanfattningar: navigationshjälp, **aldrig** självständig projektauktoritet.

**Särskilda namnkonflikter:** `K1` (spelregel) ≠ `TK01..TK05` (forskningskombinationer); `S0/S1` (historiska spawnfilter) ≠ `G5-S0/G5-S1/G5-S2` (renderingsstrategier); `G4-A1` (microstimulus) ≠ `G5Q A1` (godkänd fri X/Y).

**Roller:** MAIN VII leder; ROM DEVELOPMENT III gör endast separat beordrat specialistarbete; RESEARCH II rådgivande; GRAPHICS II source-only grafikstudier enligt order; VERIFICATION II fristående ROM-granskning enligt separat uppdrag; ART/PACKAGING & MANUAL II emballage/manual. Specialistchattar körs inte automatiskt genom GitHub Issues.

**Källuppdatering V4:** Denna fil ersätter inte själv någon tidigare Project Source automatiskt. Byt de sex enskilda källfilerna utan dubbla versioner. Ett äldre Drive-/GitHub-dokument med formuleringen "ENDA REKOMMENDERADE" gäller bara sin egen release och får inte styra nya beslut.

**Uppdateringsregel:** Framtida commits och användarbeslut kan göra V4 inaktuell. Kontrollera live GitHub och Drive. Läs normalt bara 00 + den områdesrelevanta filen, inte hela paketet vid varje fråga.
