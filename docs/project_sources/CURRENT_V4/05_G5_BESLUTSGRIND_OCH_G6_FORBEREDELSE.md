# LET ME OUT! – G5-GRIND OCH NÄSTA TEKNISKA VÄGVAL / V4


**LÄSANVISNING V4:** Tidigare versioners källangivelser, gamla GitHub Issues, initiala ROM-beställningar och äldre framtidsförslag är historiska vid sina respektive tidpunkter. Högre auktoritet och senare uttryckliga användarbeslut gäller inom exakt beslutat ämne. Ingen source-only-status är fysisk Atari/Stella-verifiering. Detta källpaket ger ingen ny teknisk auktorisation.

**Fryst V4-läge: 2026-11-17 efter G5AA/G5AB och arbetskörens historikmarkering.** [Aktuell status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [Drive](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit). Denna fil ger **INGEN** implementeringsauktorisation. Original auktoritetsgrind: [G5](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).

## Vad är klart?

1. G1–G4 var käll-/historikgrindar, inte ny slutlig ROM-verifiering. G5 designbeslutsdel för femfienders framtida mål LM-D12..16, exakta kartor A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01 (LM-D17/19), och H4-ONE G0 source-only uppdrag LM-D20 är dokumenterade.
2. G5T och G5V grafikstudier har lämnats, källtroget reproducerats offline och stängts som studier; **inte teknisk raster-PASS**.
3. **G5Z H4-ONE source-only G0 har avslutats med `G0_INCONCLUSIVE_NO_ROM`**, mottaget i [G5AA](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md). Ingen ASM/ROM/Stella/CI eller independent Verification av G5Z har skett. G0-ordern är **förbrukad**; kan inte automatiskt återstartas.

## Vad är fortfarande öppet?

- **G5 FORMAL=OPEN**, eftersom fem fria NPC samt key/door/skott/PF på verklig TIA, exakta 8×9-spawns, key-drop, score/AI samt oberoende slutacceptans inte har verifierats.
- **G1/H4 fysisk mikro, G6/F12, R1/R2/R3/R4 framtida spelimplementation, S05-test, Verification II, PR-merge ej auktoriserade.** G6-förslaget i [G4 utkast](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md) är fortfarande ett UTKAST, inte en order.
- G5-S0 fri same-Y-femfiendersvisning är mycket riskfylld, med G5H 79/76 i en specifik direktmetod. G5-S1 hårda Berzerk Y-banor är *inte godkänt* därför att LM-D12 kräver fri logisk X/Y. G5-S2 strukturerad osynlighet/flicker kräver tydlig separat acceptans; O1 är bara faktisk key/NPC-pixelöverlapp.
- **S05** gul player, vit NPC, gold key, orange P1 högerdörr, M0 och PF samma Y är självständigt olöst och skulle inte bli PASSED ens av ett hypotetiskt H4-PASS.

## MAIN VII:s säkra nästa arbetsriktning (endast förslag)

**Högsta informativa nästa tekniska fråga** efter INCONCLUSIVE (se även [G5AC beslutsberedskap, EJ auktoriserad](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AC_MAIN_VII_TIA_PHASE_CALIBRATION_DECISION_READY_NOT_AUTHORIZED_2026-11-17.md)) är om **en enda minimal, instrumenterad TIA-fas-/kopie-kalibrering** kan isolera okända `RESP`-START, `NUSIZ0=$02` på P0/M0 med EN M0, `GRP`-latens och `ENAM0`-gate. Kräv en ny, tydlig förhandsregistrering där positiva/negativa förväntningar kan skiljas åt från faktisk Stella-emulering och där en specifik kod-/ROM-/mätorder omfattar **endast** den isolerade kalibreringen. Det skulle **inte** godkänna H4, fem NPC, S05 eller G5. [G5AA rekommendation](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md).

**Ingen ny ROM-order via "fortsätt":** ett framtida konkret instrumenterat prov måste ha **separat uttrycklig användarauktorisation** för exakt testscope och output. Innan dess får MAIN VII bara göra källrevision, beslutsunderlag, offline granskning, arkiv och källnavigation. ROM DEVELOPMENT III får inte påbörja G1, G6, F12 eller nytt G0 på eget initiativ; VERIFICATION II körs fristående efter särskild batchorder och faktiskt relevant fastlåst ROM.

**GitHub-arbetskö vid detta snapshot:** [Issue #3](https://github.com/Odourman/let-me-out/issues/3) och #6 är administrativt stängda som ersatt historik. **Issue #8 öppet endast DEFERRED**, inte en aktiv order.  [PR#7](https://github.com/Odourman/let-me-out/pull/7) blockerad draft, [Issue #6](https://github.com/Odourman/let-me-out/issues/6) administrativt stängd historisk v0.18, [Issue #8](https://github.com/Odourman/let-me-out/issues/8) fortfarande öppen men uttryckligen uppskjuten, [Issue #12](https://github.com/Odourman/let-me-out/issues/12) G0 levererad och stängd.

**Framstegsdefinition:** rapporter om rådgivande forskning eller offline-renderingar får aldrig påstå att vi har en fungerande slutlig R1/R2/spel-ROM. Syftet är att skapa **ett så bra spel som möjligt med respekt för ursprunglig vision**, upptäcka hårda stopp tidigt och inte förbruka projektet i oändlig analys.
