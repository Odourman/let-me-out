# LET ME OUT! – AUKTORITET OCH NULÄGE / MAIN VIII V5

**G5AG – senare faktisk status:** LM-D21/G5AD gav ett enda avgränsat TIA-kalibreringsuppdrag men slutade `NO_BUILD_INSTRUMENTATION_BLOCKER`; de sex C0–C4/N1-proven kördes inte. LM-D22/G5AF tillät endast reparation och två Actions-kontroller på redan fryst F9. ROM DEVELOPMENT III levererade `G5AF_INSTRUMENTATION_READY_BOUNDED` (första Actions-rundan FAIL, andra SUCCESS); MAIN VIII har källgranskat och mottagit som utvecklarinstrumentering, inte oberoende verification. [Specialist-original](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md), [Issue #14 stängt som avgränsat instrumenteringsarbete](https://github.com/Odourman/let-me-out/issues/14). `G5Z_G0=INCONCLUSIVE_NO_ROM`, `G5_FORMAL_OPEN` och alla begränsningar för ny ROM, H4/G1/G6/F12/S05/fem-NPC/Verification/merge kvarstår. Inget nytt tekniskt prov får härledas från detta källpaket.

**Designbeslut oförändrade av G5AF:** Framtida fem NPC M,M,F,SM,SF, individuell fri logisk X/Y, synlighets-/O1-gräns, `-30` per kill, fem validerade spawnpunkter per godkänd kartlayout, 1/5 keyholder och exakt `A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01` gäller som **framtida designmål** enligt LM-D12–19. Inga källfiler/ROM-kartor eller tidigare v0.18 sexfiendersbevis skrivs om. Ny riktig fem-NPC 8×9-kollision, dynamisk AI, S05 och fysiskt körbar kernel är fortfarande obevisade.

> **V5-supersession:** Alla daterade formuleringar nedan från V4 som säger att G5AC ännu enbart är ett förslag, att G5AF är `NOT_YET_RUN`, att inga F9-körningar gjorts, eller att MAIN VII fortfarande leder är *historisk V4-status*. De upphäver inte LM-D21/LM-D22 och G5AG. Gamla negativa resultat behålls oförändrade. Hämta gällande originalkällor live.



**LÄSANVISNING V5:** Tidigare versioners källangivelser, gamla GitHub Issues, initiala ROM-beställningar och äldre framtidsförslag är historiska vid sina respektive tidpunkter. Högre auktoritet och senare uttryckliga användarbeslut gäller inom exakt beslutat ämne. Ingen source-only-status är fysisk Atari/Stella-verifiering. Detta källpaket ger ingen ny teknisk auktorisation.

**Datum/snapshot:** 2026-11-17 efter G5AA, G5AB och administrativ historikmarkering. **Status:** orientering; originalfiler, direkt användarbeslut och frysta tekniska bevis styr. Denna sammanfattning får aldrig skriva över originalspec eller äldre testhistorik.

**Aktuellt statusindex:** [GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [Google Drive](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit). Vid konflikt eller nyare commit måste detta index och exakt originalbeslut läsas live. Äldre tidsbundna statusrader upphäver inte senare godkännanden.

## Bindande och senare uttryckliga beslut

| Område | Aktuell rätt status och källor |
|---|---|
| Originalspel | Historiskt Master Spec/57 beslut i [ursprungsarkivet](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), kontroll enligt [G1 authority diff](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G1_AUTHORITY_DIFF_2026-11-17.md) |
| Visual/door | Svart bakgrund, bruna väggar, gul spelare, vita mänskliga fiender, guldnyckel, orange ENDAST högerdörr med svart genomskinligt nyckelhål som del av *dörrens bitmap*, inte en separat sprite |
| Nyckelskymning O1, LM-D06 | **Godkänt endast vid faktisk NPC/key-överlapp** och kvalitativt litet kortvarigt flimmer. Inget generellt döljande i samma Y, ingen kvantifierad 10 Hz-waiver; [direkt användarbeslut](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md) |
| Rörelse LM-D12 + läsbarhet LM-D13 | Fem NPC ska röra sig **fritt logiskt i X/Y, fyra riktningar**, utan fasta hårda Y-banor; hot/nyckel ska inte döljas som tekniskt fusk. [G5Q](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Antal LM-D14 | **Framtida mål R1: fem NPC M,M,F,SM,SF**; R2: fyra överlevande + synlig nyckel efter bärares död. Historiskt v0.18 R1: 6 och R2: 5+key **oförändrade**. [G5S](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Poäng LM-D15 | **Framtida -30/kill**, scoregolv 0 per händelse, +50 när key tas, +100 vid utgång, +15/levande NPC vid riktig rumsexit. Historiskt **-25/kill** oförändrat i gamla tester. [G5S](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Spawn/key LM-D16 | 5 separata förhandsvaliderade spawnkoordinater per rum på rätt godkänd karta, **1/5** likformigt vald individuell nyckelbärare. **Inga exakta spawns eller PRNG är godkända**. G5T/G5V 2×2-geometri räcker inte för riktiga 8×9-hitboxar. |
| Rum LM-D17/LM-D19 | Exakt framtida **40×22**: `A_OPEN_01`, `B_OPEN_02`, `C_OPEN_01`, `D_OPEN_01`, källpinnat i [G5X manifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json). Historiska `A01/B01/C02/D01` bevaras; **ingen fysisk kartcutover**. |
| ROM-grind LM-D20 | En enda H4-ONE G0 source-only-källgranskning var auktoriserad, **har nu genomförts**, avslutad `G0_INCONCLUSIVE_NO_ROM`; [G5AA](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) |

## Varje viktigt påstående måste ha rätt bevisnivå

**Goda men begränsade äldre ROM-prov:** F9: tre korrekta originalmasker med **binära** RAM-X-väljare, inte fri numerisk X. R1f/R1g: P0-dual/multilägen i tidigare ROM, men **M0 på föregående rasterrad**, inte same-Y. R3: separat orange dörr-P1-prototyp, inte integrerad same-Y med key/NPC. R1ba felvänd orientering trots positiv 600/600-rapport. **F11** källmässigt G0-FAIL för fyra numeriska P1-X inom dess allokering; inget universellt Atari-NO-GO. Källa: [G2 negativa tester](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md).

**G5Z nyaste tekniska utfall:** H4-ONE med P0 player/M, P1 F/SM, en M0 och verkligt PF saknar korrekt 6507-instruktions-/TIA-START-/NUSIZ-/GRP-/ENAM-tidsplan. 72/72 CSV-rader i G5Z granskade av MAIN; 58/68c är en **ofullständig opcodekostnadsmall**, inte körbar kernel. `INCONCLUSIVE` betyder **varken bevisad möjligt eller bevisad universellt omöjligt**. Se [fryst G5Z-rapport](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md).

**Största återstående luckor:** fem vita + gul player + ett M0 + verkliga bruna PF samtidigt på samma Y; rätt 8×9-kollision/spawns/AI; **S05** guldkey+vit NPC+gul player+orange P1-högerdörr+M0/PF på samma Y; samlad spelkod och obestridd oberoende VERIFICATION.

## Aktuella spärrar och öppna historiska ärenden

- **G5 formellt OPEN**; **G1/G6/F12/ny ROM/Stella/Verifiering/PR-merge inte auktoriserade** av färdig G0 eller någon V4-fil. Inga nya Y-lanes, 10Hz-flimmer eller ändrade originalmasker utan separat användarbeslut.
- `main` innehåller dokumentation/kartdata och ett källindex; ROM-experimenten ligger på historiska frysta **separata branches**. Länka aldrig till en ny `main`-ROM som inte finns.
- [PR #7](https://github.com/Odourman/let-me-out/pull/7) historisk blockerad **draft, inte merge**. [Issue #6](https://github.com/Odourman/let-me-out/issues/6) är **stängt administrativt som historisk v0.18-order** (6 NPC; inte därför att gamla tester fått PASS). [Issue #8](https://github.com/Odourman/let-me-out/issues/8) historiskt oberoende verifieringsuppdrag, **uppskjutet tills uttrycklig batchorder**. [Issue #3](https://github.com/Odourman/let-me-out/issues/3) är **stängt som supersederad historisk S0/S1 sexfiendersjämförelse** på v0.11, inte en genomförd framtida femfienders ROM-verifiering. [Issue #5](https://github.com/Odourman/let-me-out/issues/5) framtida nyckel/dörr-test, ej kodmandat. [Issue #12](https://github.com/Odourman/let-me-out/issues/12) stängt G0.
- Kontrollera relevant spel-/acceptansprotokoll, aktuell HEAD och nyliga beslut igen före konkreta tekniska påståenden.
