# LET ME OUT! – MAIN V → ROM DEVELOPMENT II
## R1-F10: ARKITEKTURFÖRSTUDIE FÖR SEX GODTYCKLIGA INDIVIDUELLA X/Y – ENDAST SOURCE-ONLY

**Datum:** 2026-11-17. **Ny separat uttrycklig MAIN V-auktorisation:** exakt **EN read-only arkitektur-/TIA-källstudie** inom användarens tidigare auktoriserade NTSC/standard F6/v0.18 R1-kernelundersökning, inte en ROM-implementation. F9:s tre binära X är nu mottagen lokal PASS; F10 **får inte** göra samma sak igen med en fjärde binär X eller bara utöka 8 profiler till 16.

**HÅRT FÖRBUD** under F10: **inga nya ASM/DASM/ROM/Stella/GitHub Actions/byggskript/test-Python/PNG/ZIP**, ingen ändring av frysta F2–F9, ROM-masker, PR#7 eller `main`, inga kodgenererade alternativ, ingen bank-/mappercutover, ingen grafik, PAL, R2/R3/R4/gameplay/fullspel eller separat VERIFICATION. Endast EN text/Markdown-rapport på NY isolerad branch från exakt fryst F9 `c36982aef770af6cd3f68c2da37b8ed14aee2393`. Sluta direkt när rapporten är överlämnad till MAIN V i Issue #6. Ingen F11 utan nytt separat MAIN-beslut.

### 1. Bindande faktisk bevisbas och spelmål

1. Läs [MAIN:s faktiska oberoende F9-mottagning](MAIN_V_R1_F9_RECEIPT_INDEPENDENT_EVIDENCE_AUDIT_AND_ARCHITECTURE_DECISION_2026-11-17.md) och [fryst F9-utvecklarrapport](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md). F9 fryst ROM `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, en standard-F6/NTSC ROM, tre rättvända källmasker (M/F/SM), `X0=$A0` (39↔45), `X1=$A1` (99↔105), `X2=$A4` (195↔207), 144/144 verkliga rasterbilder, 12/12 binära ortogonalitetskontroller. Koden har **åtta** i förväg upprullade nio-radersrutiner. **Detta är inte numeriskt fri X/Y**.
2. [Faktiska spel-/testkraven](ROM_GATE_V018_ACCEPTANCE.md): R1 **sex** visuellt skilda objekt (M,M,F,F,SM,SF) med egna X/Y och same-Y/shifted-Y, top-down ursprungs-8×9, P0 gul spelare, M0 aktiv projektil, PF bruna väggar; riktig tid 76 CPU-cykler per scanline, stabil 262 NTSC, plus senare R2 fem NPC+nyckel/O1 och R3 asymmetrisk högeröppning/svart nyckelhål. [Sex-X-auktoritet](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md) kräver sex numeriskt individuellt uppdaterbara X och Y, inte sammanlänkade NUSIZ-grupper eller särskilda spawnpositioner.
3. [Låsta originalmasker](../design/NPC_REFERENCE_8x9_masks.json), Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Bevara alla fyra typsilhuetter och varje originalrad. Ingen rotering, invertering eller R1ba-konvertering; forskningskärnan R1ba har bekräftat fyra vertikalt felvända stora originalmasker och kopplade X.
4. Läs den faktiska [ursprungliga 30-tricksbilagan](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), [MAIN:s tillämpningsgranskning](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md), [TIA-retriggering-research](MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md), [F6-banks-/ROM-budget](MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md) och relevanta primära TIA/Stella 6.7.1-källor, samt verklig F9 `.asm/.lst/.sym` ur frozen ZIP. Dessa forskningskällor är rådgivande och förklarar inga nykörda ROM-resultat.
5. PR#7 fortsatt OPEN/DRAFT/UNMERGED, Issue #8 standby, GRAPHICS stängt. R1 FULL BLOCKED.

### 2. EN skarp arkitekturfråga som faktiskt leder mot R1

**Hur kan sex självständigt uppdaterbara NUMERISKA X/Y och fyra ursprungliga 8×9 former ritas i samma belastade frame utan att minska antalet NPC, ändra originalpixlar, acceptera otillåtet flimmer eller tyst sammanlänka deras X?**

Värdera **högst tre** specificerade verkliga arkitekturfamiljer med en matris som har **hårda hårdvaru-/sourcegrindar**, inte en lös idélista:

**A. Data-/timingstyrd P1-retriggering istället för 2^n kernel-unrolling.** Beskriv exakt hur sex individuella numeriska sorterade X (och om nödvändigt bytt ordning beroende på dynamisk X) kan mappas till `RESP1`- och `GRP1`-deadlines; hur framräknade väntcykler/pos-state kan användas under raster med 6502 ROM som **inte är skrivbar**, och vad som händer vid täta/överlappande X. Ställ upp radbudget för P0/M0/PF, 6× RESP/GRP inklusive kopie-START, förberedelse i VBLANK, nollrader och 76-cykels deadline. Avfärda möjligheten om man inte kan visa 6× timing/datafönster, även om F9:s 3×binära är positivt.

**B. Bankfördelade specialiserade standard-F6-displaykernlar med byte-/maskdelad data.** Ingen bank switch **mitt under en kritisk P1-copy/GRP-rad** får antas gratis. Räkna faktisk bankbyte-/entry-/return-cycle, 4×4096 limit, resetvektorer/identiska kontra specialiserade banker, 128-byte RIOT, delad kod och hur många 8×9 kernelvarianter som ryms. Visa varför även 4-bankars distribution av `2^6=64` fasta kombinationer **inte uppfyller sex numeriskt fria X/Y** även om vissa 4-bitars diagnoser kan få plats.

**C. Adaptiv NUSIZ close/medium grupperad med ordnings-/Y-multiplex, ev. VDEL/HTR- eller PF-hybrid.** Pröva hur NUSIZ-fasta grupper kan nyttjas **utan** att fiendernas logiska X kopplas ihop, inklusive fall där inga två NPC har användbara kopieavstånd, och **sex exakt samma Y**. Läs faktisk äldre R1ba och dess motbevis för kanonorientering. Flicker/9-radersdelning/4-pixel PF-gubbar har historiskt lokalt misslyckats; ingen omärkt visuell waiver.

Varje familj ska redovisa vad som *redan visats*, vad som är **HYPOTES**, vad som skulle göra tekniken **OMÖJLIG inom 76 cykler/TIA-pixel/ROM/RAM**, och **EN** minimal future TEST som tydligt kan falsifiera familjens centrala premiss. Ingen testspec innebär tillåtelse att bygga.

### 3. Obligatorisk kvantitativ redovisning, även om ingen lösning finns

- **F9:s faktiska bankfakta:** 3019 code +115 data +6 vectors = 3140 byte per 4096-byte exekverande bank, kvar 956 byte; 8 förkompilerade nio-raderskernlar. Fryst G0-plan 59/76 CPU-cykler slutrad, denna **SOURCE-BUDGET** är inte en universell 17-cykelreserv för godtyckliga sex X/Y; varje ytterligare write, prefetched mask och branching måste mätas i sin tänkta kritiska rad.
- Ställ upp en **mask-/CPU-/färgklockshändelse-tidslinje** för minst (i) sex godtyckliga X same-Y, (ii) sex tätt intill varandra (flera <8 CC eller delvis överlappande), (iii) mixed Y som börjar/slutar på förskjutna scanlines, (iv) vart NPC par kan byta relativ X-ordning genom förflyttning, och (v) R2 där key behövs samtidigt. Alla scenarier ska utgå från fyra låsta masktyper och P0/M0/PF-resurser. Om hard-stop vid fysisk överlappning kräver uttalad objektprioritet/occlusion från gameplay/spec, dokumentera exakt vilket beslut MAIN/användaren skulle behöva, anta inte själv.
- Minnesbudget: 128-byte RIOT med sex oberoende X + sex oberoende Y, typer/animation/collision/status, spelar-/skott-/nyckel-state, samt kod-/bankbudget. **Separera** temporär test-ROM-kod från framtida faktisk spelkod.
- Redovisa eventuella ytterligare `NUSIZ1/HMOVE/VDEL/PF/P0/M0`-konflikter när [R3 vägg/högerdörr](MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md) integreras; F9:s **speglade bruna sidoväggar** är inte ett R3-högeröppningsbevis.
- Gör en konkret tids-/rymdundre gräns för sex `RESP1/GRP1`-par i en 76-cykels rasterrad. **Överdriv inte**: cykelsummor för registerskrivningar bevisar inte att noll copy-deadlines missas eller att sex godtyckligt åtskilda slots finns.
- Ange tydligt om standard F6 är fortsatt trovärdig för strikt låst originaldesign. Om inte, skriv `NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN` i stället för en vag positiv roadmap. Ingen automatisk designerförenkling, ingen flytt av P0, ny mapper/ARM eller färre NPC.

### 4. Leveransgrind och STOPP

Skriv ENDAST EN ny Markdown-fil på **separat F10-analysbranch från fryst F9**: `docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md`. Ha tabell med familj A/B/C, källdata, budget, blockerare, falsifierbar enskild framtida prob och en rangordning med en vinnare **endast om sakligt motiverad**. Välj exakt EN slutklass:

- `F10_CONSTRAINED_ARCHITECTURE_WITH_ONE_FALSIFIABLE_GATE`: välmotiverad arkitekturväg med en *sourcebaserad, specifik* framtida falsifieringsgrind, **inte** fungerande ROM, inte sex-X/Y-acceptans.
- `F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`: ingen av metoderna ger ännu en beläggbar teknisk väg inom låsta krav; föreslå MAIN:s nästa beslutsgrind och tydliga användarval.
- `F10_SOURCE_INCONCLUSIVE`: central faktisk TIA-/verktygsproveniens saknas och gör en familjjämförelse otillräcklig; beskriv exakt saknad källdata.

Rapportera öppet **vilka delar som kräver senare ny implementeringsauktorisation** och vilka som ligger utanför tidigare accepterat scope. **Sluta** därefter: ingen F11, ROM, fjärde NPC-prob, R2/R3/R4-implementation, ny GAME OVER/HUD/KEY, PAL, F6SC, ARM, PR#7 merge, grafik, fullspel eller oberoende Verification. **Fullt R1: `BLOCKED / NOT ACCEPTED`**, oavsett hur god arkitekturanalysen är.
