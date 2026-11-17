# LET ME OUT! – FEM FIENDER: GODKÄNDA FRAMTIDA REGLER / V5

**Designbeslut oförändrade av G5AF:** Framtida fem NPC M,M,F,SM,SF, individuell fri logisk X/Y, synlighets-/O1-gräns, `-30` per kill, fem validerade spawnpunkter per godkänd kartlayout, 1/5 keyholder och exakt `A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01` gäller som **framtida designmål** enligt LM-D12–19. Inga källfiler/ROM-kartor eller tidigare v0.18 sexfiendersbevis skrivs om. Ny riktig fem-NPC 8×9-kollision, dynamisk AI, S05 och fysiskt körbar kernel är fortfarande obevisade.

**G5AG – senare faktisk status:** LM-D21/G5AD gav ett enda avgränsat TIA-kalibreringsuppdrag men slutade `NO_BUILD_INSTRUMENTATION_BLOCKER`; de sex C0–C4/N1-proven kördes inte. LM-D22/G5AF tillät endast reparation och två Actions-kontroller på redan fryst F9. ROM DEVELOPMENT III levererade `G5AF_INSTRUMENTATION_READY_BOUNDED` (första Actions-rundan FAIL, andra SUCCESS); MAIN VIII har källgranskat och mottagit som utvecklarinstrumentering, inte oberoende verification. [Specialist-original](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md), [Issue #14 stängt som avgränsat instrumenteringsarbete](https://github.com/Odourman/let-me-out/issues/14). `G5Z_G0=INCONCLUSIVE_NO_ROM`, `G5_FORMAL_OPEN` och alla begränsningar för ny ROM, H4/G1/G6/F12/S05/fem-NPC/Verification/merge kvarstår. Inget nytt tekniskt prov får härledas från detta källpaket.

> **V5-supersession:** Alla daterade formuleringar nedan från V4 som säger att G5AC ännu enbart är ett förslag, att G5AF är `NOT_YET_RUN`, att inga F9-körningar gjorts, eller att MAIN VII fortfarande leder är *historisk V4-status*. De upphäver inte LM-D21/LM-D22 och G5AG. Gamla negativa resultat behålls oförändrade. Hämta gällande originalkällor live.



**LÄSANVISNING V5:** Tidigare versioners källangivelser, gamla GitHub Issues, initiala ROM-beställningar och äldre framtidsförslag är historiska vid sina respektive tidpunkter. Högre auktoritet och senare uttryckliga användarbeslut gäller inom exakt beslutat ämne. Ingen source-only-status är fysisk Atari/Stella-verifiering. Detta källpaket ger ingen ny teknisk auktorisation.

**Aktuella källbeslut:** [Samlad status- och auktoritetsguide](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). Detta dokument beskriver *framtida design*, inte ett implementerat spel.

**Klass:** källankrade beslutsgränser och återstående valideringsfrågor, inte implementation. Historisk originalspec/57 beslut får inte skrivas över utan uttrycklig supersession.

## Nu godkänt, inte längre bara förslag

- **Framtida roster LM-D14:** exakt fem fiendeinstanser: **två stora män (M1, M2), en stor kvinna (F), en liten man (SM) och en liten kvinna (SF)**. Bara fyra bitmap-originaltyper, men fem olika individers positioner. Framtida R1 fem NPC, R2 fyra kvarvarande NPC och en fysisk synlig guldkey. 
- **LM-D12/13:** individuell fri logisk X/Y, fyra riktningar, inte fasta Y-banor. Rättvis hot-/key-synlighet; ingen konstant rasterdöljning när NPC eller key inte pixeltäcks.
- **LM-D15:** **-30 poäng per dödad NPC**. Övriga ursprungliga poängregler: **+50 vid pickup**, **+100 vid verklig utgång**, **+15 per levande NPC vid exit**, aldrig score under **0** vid någon händelse. Historiska ROM-/scoretester med -25 skall vara frysta.
- **LM-D16:** fem **olika och korrekt förhandsvaliderade** spawnplatser på per-rum exakt beslutad framtida karta. Endast **en** av fem individuella instanser bär key, likformigt **1/5**, inte modulobias/slump från statisk typ. Nyckeln kommer först efter bärares dödsanimation, på faktisk logisk dödsposition. Exakta pooler och PRNG återstår.
- **LM-D17/19:** de exakta framtida kartlayoutmålen A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01 är nu godkända; ingen renderad ROM-PF eller kartcutover finns.

Bindande källor: [LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D14/15/16](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D17/19 kartmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json), [K1/E1](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md).

## Ny poängmatematik och fallgrop med golv

Vid fem NPC och k dödade, **om inga nollgolv inträffar före exit**, blir framtida rumspott: `Δ=150 + 15*(5-k) - 30*k = 225 - 45*k`. Vid **fem dödade**: `0 netto/rum` efter komplett pickup/exit när startsaldot räcker för alla fem -30-avdragen. Men vid startscore 0 och fem dödade **före** pickup nollklampas varje -30, varefter pickup/exit kan ge **+150**. Det är **avsedd regelkonsekvens att testa**, inte 0 oavsett händelseordning. G5R:s 210-körnings offline-CSV ersätter inte faktisk ROM-verifiering: [G5R](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5R_FIVE_NPC_SCORE_FLOOR_210_CASES_SOURCE_ONLY_2026-11-17.csv).

## Historiskt fryst, inte upphävt i efterhand

| Område | Historisk v0.18 / original | Framtida godkänt mål |
|---|---|---|
| Antal | R1=6 M,M,F,F,SM,SF; R2=5+key | R1=5 M,M,F,SM,SF; R2=4+key |
| Killavdrag | -25 | **-30** |
| Kartor | A01/B01/C02/D01 | A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01, **designbart ännu ej ROM** |
| Spawn | Historiska 2×2-kandidater och S0/S1-filter | Nya fem 8×9-förhandsvaliderade platser per exakt karta (ej valda) |

**Kvar att bevisa:** verklig 8×9 NPC/player/wall-/key-/door-kollision och fria AI-vägar, alla 5 keyholder-fall, K1-pickup först senare tick vid key under spelaren, E1 utgångs-/dödskollision, score 0-golv och extraslivströsklar, riktig samtidig 5NPC/P0/M0/PF och S05. Ingen generell Y-lane/flicker-waiver får införas utan nytt uttryckligt användarbeslut.
