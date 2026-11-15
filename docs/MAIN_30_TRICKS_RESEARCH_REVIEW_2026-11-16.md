# Let Me Out! – MAIN:s bedömning av teknikavhandlingen och samtliga 30 Atari-trick

**Datum:** 2026-11-16. **Typ:** råd, källkritisk MAIN-granskning och prioritering. **Ingen ny auktorisation**, ROM-implementation, användargodkänd visuell kompromiss, ny mappartyp eller oberoende VERIFICATION.

## Källor och proveniens

- Användaruppladdning `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(1).md`: 30 374 byte, SHA-256 `6d45b2ba5747ee7c64a7446d5295f6f8add988386593b5662a70b700aabff28c`. **30/30** nummer i tabell och fulltext kontrollerade. [Källbilaga bevarad som text i GitHub](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md). GitHub-uppladdning genom textverktyg har inte påståtts vara en byte-identisk binär spegling.
- Användaruppladdning `LET_ME_OUT_SAMLAD_AVHANDLING_MAIN_MED_ALLA_30_TRICK_2026-11-16(1).pdf`: **55 sidor**, 534 513 byte, SHA-256 `596ee313bbbfcf3926efea61807a7b169363dd1aef994a4fc9a635877c62019f`; PDF har öppnats och kontrollerats med sidtext och renderade representativa sidor. Första delen är ny avhandling/teknikatlas, andra delen tidigare 67-riskrapport. PDF-originalet förvaras i den här konversationens bilagor; ingen Drive-kopia hävdas.
- **De 52 T-posterna och de 30 ursprungliga numrerade tricken överlappar**, alltså inte 82 oberoende lösningar.
- Repo [Odourman/let-me-out](https://github.com/Odourman/let-me-out), vid granskning [PR #7](https://github.com/Odourman/let-me-out/pull/7) **DRAFT**, omergad, HEAD `82667dae033f70570dce903f8e1d4866528be02a`. [Kodauktorisation](ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [huvudstatus](CURRENT_PROJECT_STATE_2026-11-15.md), [RESP1-analys](MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md), [F6-minnesrevision](MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md). Ett möjligt framtida commitbyte måste kontrolleras på nytt.

## Beslutsmässig sammanfattning

**R1 sex oberoende och läsbara humanoider är fortfarande FAIL/BLOCKED.** SEX_X_FREE A (100/600 per NPC) har för mycket bildruteflimmer; B har otillräckliga PF-silhuetter; 9-, 18-linjers Venetian och VDEL gav inte två kompletta fria P1-masker. **Stella-mätning vid den faktiska `STA RESP1`-instruktionen saknas.** `ci_pc_cycle_probe.sh` använde `break` följt av `frame #1`/ `step`, vilket gav PC `$F047` i stället för avsett `$F0A8`. En stilla möjlig TIA-felmekanism är senare `RESP1` efter `GRP1` på varje rasterrad och reset av föregående figurposition. Hypotesen är ännu **inte** en uppmätt rotorsak. Relevant dokumentation: https://stella-emu.github.io/docs/debugger.html (`break` + `run`, `trapWrite` efter instruktion, `_bank/_scan/_sCycles`).

**Kritiskt missförstånd att undvika:** F6-bankbyten skapar bara fler ROM-byten/kod/data; inga nya TIA-sprites, RAM-byte eller fler än 76 CPU-cykler på samma scanline. [Tidigare F6-revision](MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md) fann 1 557 oallokerade ROM-byte per huvuddiagnostikbank, men ingen ny R1-grafik-PASS.

## Prioritering av 30-tricksunderlaget

| Nummer i originalbilagan | Teknik | MAIN:s nuvarande bedömning | Får påstås ha löst R1? |
|---|---|---|---|
| **02** | Mid-scanline GRP Rewriting | **Högsta relevans efter giltig RESP-trace.** Pröva tidsfönster på faktisk P1, inte enbart förinställda NUSIZ-kopior. | Nej |
| **10** | HMOVE Fine Positioning | Kritisk exakt X-kalibrering, men ger inte fler sprites. | Nej |
| **24** | Precomputed Tables and Cycle-Exact Kernels | Starkaste arkitekturstödet: register-/pixeldeadlines och beräkningsförläggning under VBLANK. | Nej |
| **01** | Sprite Multiplexing | Mycket relevant för åtskilda Y-band och gränsfall, men same-Y kräver separat bevis. | Nej |
| **09** | VDEL / Delayed Graphics | Del av GRP-timing, inte en tredje P1; tidigare fragment-Fail. | Nej |
| **08** | Two-Line Kernel | Kan frigöra relativ cykeltid men 8×9-originalmasker måste bevaras. | Nej |
| **15** | NUSIZ Sprite Duplication | Verkligt tvåmaskers delbevis vid 32/64 klockors kopieavstånd, men inte fria X. | Nej |
| **14** | Multiple Display Kernels | Bankvisa R1/R2-diagnosvarianter kan forskas kring med säker hotspot-trampolin; integrerad dörr/vägg/P1 är separat bevis. | Nej |
| **07** | Asymmetric Playfield | **Hög R3-prioritet** för högerport och stängd vänsterkant; rätt PF-skrivfönster krävs. | Nej |
| 03 | Venetian Blinds | 9/18/VDEL har **lokalt misslyckats**, är inte ett allmänt omöjlighetsbevis. Originalmaskens 9 rader blir 5/4 i enkel interleave. | Nej |
| 04 | Sprite Flickering | Den prövade 6-fasmetoden gav 100/600 NPC-frames; **visuellt FAIL**. | Nej |
| 05 | Dynamic Playfield Sprites | PF-silhuetter misslyckades kvalitativt, men PF kan vara nyttigt för vägg/enkla objekt. | Nej |
| 17 | Missile and Ball Reuse | Relevant R2-resursinventering, men M0/M1/BL är inte humanoida bitmapkanaler. | Nej |
| 19 | Playfield Priority Switching | Relevant O1-grafik och visuellt lager, inte logiska nyckelregler. | Nej |
| 12 | Raster Color Changes | Bruna väggar, gul spelare, orange dörr/nyckelhål måste stämma i riktiga NTSC-bilder. | Nej |
| 13 | 48-Pixel / Six-Digit Score Kernel | Fast geometri; värdefullt som GRP-exempel och senare HUD. | Nej |
| 21 | RIOT Timer Scheduling | Frame-stabilitet och blankperioder; inga extra beamcykler. | Nej |
| 06 | Mid-frame Sprite Resizing | Framtida specialeffekter, får inte ändra godkända figurmasker. | Nej |
| 11 | Late HMOVE Trick | Låg: timing-/modellrisk, undersöks först efter stabil bas. | Nej |
| 16 | Sprite Reflection | Möjlig senare ROM-besparing; ändrar inte antalet sprites. | Nej |
| 18 | Playfield Score Mode | Låg: P0/P1-färgkonflikter och inte relevant som NPC-lösning. | Nej |
| 20 | Hardware Collision Latches | Framtida gameplay; identifierar inte vilken logisk flickerad NPC som kolliderade. | Nej |
| 22 | Stack/RAM Mirroring | Framtida minnesdisciplin, risk för stackfel; skapar inte mer RAM. | Nej |
| 23 | Undocumented 6502 Opcodes | Låg, portabilitets-/hårdvarurisk; åtgärdar inte spritebristen. | Nej |
| 25 | Stack-Based TIA Register Tricks | Specialistrutin, hög regressionsrisk och ingen extra sprite. | Nej |
| 26 | Timing-Based Horizontal Scrolling | Ej aktuellt behov för rumskartorna. | Nej |
| **27** | SCABS | **Inte vanlig F6**. Kräver annan cartridgearkitektur. | Nej |
| **28** | Superchip/Supercharger extra RAM | **Inte vanlig F6**. Kräver ny användarauktorisation och ändrar inte TIA. | Nej |
| **29** | DPC | **Inte vanlig F6**. Kräver specialchip/mapper. | Nej |
| **30** | DPC+/CDF/ARM | **Inte vanlig F6**. Kräver ny cartridge/hårdvaru-/distributionsdesign. | Nej |

## Teknisk väg framåt enligt källavhandlingen, rangordnad och med stopp

1. **P0 – instrumentering, högsta prioritet, råd ej kodorder:** verifiera konkret Stella Debugger-`break` + `run`/`runToPc` mot `STA RESP1` vid uppmätt PC/bank/frame/scanline/cykel; separera breakpoint *före* instruktion från `trapWrite` *efter* instruktion. Verifiera verktygsbeteendet för installerad Stella 6.7.1, inte enbart nyare manual. Saknas giltigt spår → **INCONCLUSIVE**.
2. **P1 – minsta visuella feasibility-bevis:** två oförändrade, olika 8×9-masker vid **verkligt oberoende X** i samma 9-radersband, med fullstor gul P0-spelare och M0-skott. Minst ett nära och ett långt X-avstånd; riktiga pixlar, inte bara sex logiska RAM-X. Undviker vi komplett originalmask och ersätter med 5/4 rader → **FAIL** för full design.
3. **P2 – full R1 + R2 först när P1 lyckas och scope är auktoriserat:** sex NPC i R1, fem NPC plus guldnyckel i R2 med O1-skymning, väggar och skott. 600 faktiska sammanhängande Stella-frames för relevant scen; per-NPC-synlighet/masker, longest invisible streak, `_scan/_sCycles/_bank`, registerdeadlines och ROM SHA. **Ingen godkänd numerisk flimmergräns finns**, visuell bedömning krävs.
4. **P3 – R3/R4 först när relevant scope och förutsättningar är uppfyllda:** asymmetrisk högerdörr med svart synligt nyckelhål, bruna väggar och korrekt färg; senare raster-/Y-/objektstresstest. Bankvis specialisering får inte användas som bevis för att dessa objekt fungerar i samma faktiska spelbild.
5. **P4 – separat VERIFICATION på exakt ny commit**, och endast därefter ett MAIN-/användarbeslut om något nytt steg. Nuvarande [Issue #8](https://github.com/Odourman/let-me-out/issues/8) avser äldre, fryst `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, inte PR #7 HEAD.

## Källkritiska noteringar
- Den nya PDF:en innehåller en äldre 67-problemsrapport efter den nya avhandlingen. **Historisk rapportstatus får inte ersätta kontrollerad senaste projektstatus**.
- Historisk *Space Invaders* bitmapvariation via GRP/NUSIZ bevisar inte oberoende sex-X. Video Chess fungerar med accepterad radförlust och fast schackgeometri, inte automatiskt fyra hela 8×9-masker.
- Begränsningarna på 76 cykler är hårda, men gamla cirka 74/76-scheman är **statiska beräkningar för annan kernel**, inte uppmätta aktuella RESP1-deadlines.
- Alla 30 poster är pedagogiskt relevanta; en historisk effekt eller teknik som kan exekveras på standard F6 är **inte** automatiskt kompatibel med R1/R2:s kombinerade belastning.
- Tillstånd enligt [ROM_GATE_V018_AUTHORIZATION_2026-11-15.md](ROM_GATE_V018_AUTHORIZATION_2026-11-15.md) gäller bara NTSC v0.18/R1–R4. ROM DEVELOPMENT har senast stoppat vidare Venetian-uppskalning. Den här forskningsbedömningen är **inte** separat uttrycklig kodauktorisation efter STOPP, och får inte starta fullspel, gameplay/AI, PAL, v0.19-kartcutover, ny mapper eller ändrade grafikkrav.
- Det här dokumentet är MAIN:s källgranskning, **inte oberoende VERIFICATION**. *The Cabin*, *I Love a Fish* och Linear lämnas orörda.

**MAIN:s slutsats:** De 30 originaltricken och 52 teknikmönstren är ett bra, fullständigt rådmaterial. De stärker framför allt en minimal register- och cykelriktig RESP1-undersökning och efterföljande tvåmaskers feasilibility-grind; de ger ännu inget nytt R1 PASS och motiverar inte att överge sex androider.
