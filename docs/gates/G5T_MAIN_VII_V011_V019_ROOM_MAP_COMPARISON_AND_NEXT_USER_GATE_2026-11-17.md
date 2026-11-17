# LET ME OUT! – MAIN VII G5T: jämför gammal kartbas med luftiga v0.19-kandidater
**Datum:** 2026-11-17. **Klass:** `G5T_MAP_SELECTION_SOURCE_ONLY_NOT_APPROVED`.
**Inget exakta kartval eller versionsbyte har godkänts.** C1/D1/E1 är nyligen godkända framtida fem-NPC-regler enligt [LM-D14/15/16](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), men det innebär INTE v0.19-kartcutover, spawn-poolacceptans, ROM/G6/F12 eller ny grafisk designcanon.

## Källor och beräkningsmetod
- [v0.11 historiska exakta A01/B01/C02/D01 40×22](../../design/PLANERADE_RUMSKARTOR_V011.json), fortfarande exakta källbasen.
- [v0.19 `*_OPEN_01` fyra exakta 40×22-kandidater](../../design/OPEN_ROOMS_V019_40x22_CANDIDATES.json), uttryckligen `candidate precise 40x22 offline map; NOT approved as new canon or ROM implemented` enligt datafilen.
- [LM-D04: luftig rumskänsla redan godkänd som riktning](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md). [G5P reproducerade 8 kartgrider i offline-AI](G5P_MAIN_VII_RESEARCH_DELIVERY_INTAKE_AND_REPRODUCTION_2026-11-17.md).

Den här enkla inspektionen räknar enbart **interiörens** 38×20=760 teckenceller (kant r0/r21, c0/c39 exkluderade). `#` räknas som bruna väggar, `.` som öppna celler; dörren `D` ligger vid kanten och båda set har samma antal **4** markerade D-celler. Dessa mått bevisar INTE på riktigt spelbarhet, PF-bitkompilering, 8×9-hitbox, ROM eller visuell kvalitet.

## Källfaktiska resultat
| Rum | Historisk v0.11 | Öppet, % interiör | Föreslagen v0.19 | Öppet, % interiör | Väggceller 0.11 → 0.19 | Källkandidatankare 0.11 → geometriskt återanvändbara 0.19 |
|---|---|---:|---|---:|---:|---:|
| A | `A01` | 91,6 % | `A_OPEN_01` | 95,3 % | 64 → 36 | 20 → 18 |
| B | `B01` | 79,5 % | `B_OPEN_01` | 93,7 % | 156 → 48 | 13 → 9 |
| C | `C02` | 83,7 % | `C_OPEN_01` | 91,6 % | 124 → 64 | 18 → 16 |
| D | `D01` | 77,9 % | `D_OPEN_01` | 92,1 % | 168 → 60 | 15 → 15 |

**Konsekvens:** v0.19 har enligt källmatriserna fler öppna celler i alla fyra rum och ligger närmare användarens godkända luftiga designriktning. Men **B_OPEN_01 har bara nio återanvändbara gamla geometriska startkandidater mot tretton i B01**; det säger inte att fem verifierade startspawns eller riktig nyckel-/door-åtkomst är godkända. Fullständiga framtida spawnpooler kan behöva särskild validering/utökning efter kartval.

## MAIN:s rekommendation, inte automatiskt beslut
- Behåll `A01/B01/C02/D01` som **exakt historisk source-/testbas** tills ett separat, tydligt användarval sker.
- Låt GRAPHICS II inom en **uttryckligen beställd source-only designstudie**, om MAIN senare beställer det, visa **parvisa riktiga 40×22-kartor** A01 ↔ A_OPEN_01 osv, där originalets funktionella dörr, väggar, spelerstart och möjliga spawnankare framgår utan att ändra datan, rita nya sprites eller hävda ROM-visning. MAIN får själv granska data, men ska inte påstå specialistleverans utan faktisk GRAPHICS II-rapport.
- Visa också öppna kandidatkartornas faktiska gångvägar, spärrade spawnplatser och rumsidentitet för användaren före ett exakta-kartor-beslut.
- Om användaren då godkänner exakt `A_OPEN_01/B_OPEN_01/C_OPEN_01/D_OPEN_01` som kartversion ska formellt versionsbyte, spawn-poolacceptans, eventuella PF-/door-konflikter och framtida F6/NTSC-testscope dokumenteras separat. Ingen cutover eller grafisk waiver får antas av "fortsätt".

**Nuvarande gate:** `A1/B1/C1/D1/E1=APPROVED_TARGETS`; `V019_EXACT_MAP=USER_DECISION_PENDING`; `S05_G0=UNPROVEN`; `G5_FORMAL_OPEN`; `G6/F12_NOT_AUTHORIZED`; `ROM_NOT_ORDERED`.
