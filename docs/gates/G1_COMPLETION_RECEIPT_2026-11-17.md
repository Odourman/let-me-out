# LET ME OUT! – MAIN VI G1 – mottagning, källkontroll och avslutad dokumentgrind
**Datum:** 17 november 2026. **Beslutsroll:** MAIN VI. **Resultat:** `G1_DOCUMENTATION_COMPLETE_WITH_DOCUMENTED_OPEN_ITEMS`. Detta är **INTE** tekniskt `R1 PASS`, **INTE** nytt användarbeslut, **INTE** kodorder, **INTE** oberoende `E02` och **INTE** auktorisation att påbörja G2 automatiskt.

## 1. Avgränsad utförd arbetsorder
Användaren gav MAIN VI fria händer för **nästa steg** i den redan överenskomna G1–G10-sekvensen, med krav att stegresultatet redovisas när klart. Tolkat som endast **G1: fastställ aktuell beslutskanon, originalreferenser, v0.18-acceptans, källa-/commitstatus och öppna frågetecken**. G2 och alla framtida G6+ ROM-/verifieringsorder lämnas orörda.

## 2. Verkliga källor och integritetskontroll
- Original från projektets Drive: [LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), 738586 bytes, SHA256 `f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4`.
- ZIP:s integritetstest godkänt. **Alla 20/20 filer i originalets SHA256-manifest matchade**. 21 ZIP-poster totalt inklusive själva manifestet. Tre handskisser låg i `assets/`; användarens referens-Berzerk-ROM har INTE extraherats till eller kopierats in i publika GitHub-projektet.
- `03_DECISIONS.csv`: exakt **57** konsekutiva originalbeslut ID 001–057, käll-SHA256 `e0136b89195c567c33a7435896c77f57e44c0a66555d6fcefed3df81ae8614f1`.
- Originalmask `assets/NPC_REFERENCE_8x9_masks.json` SHA256 `1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`; jämförelse av exakt originalbytes Git-blob SHA-1 `058800a4c1904d1ff289e7e61b3902aa111ba16d` med live [GitHub-masker](../../design/NPC_REFERENCE_8x9_masks.json) **MATCH**. M/F 9 fyllda rader, SM/SF 6 synliga av 9 (nollrader 0,1,8). Dessa är fast diagnostisk pixelreferens men ingen automatisk slutlig spel-ROM-acceptans.
- Live GitHub före G1 var HEAD `a2dcc8b5faaae681cfd91e73b51f5eb155ff457e`. Issue #6 OPEN, v0.18 NTSC diagnostik R1–R4 auktoriserad (F6 16KiB om motiverat), PR #7 OPEN/DRAFT/UNMERGED, Issue #8 OPEN för **äldre frysta 561d3ba-baseline**. Full R1 fortfarande BLOCKED/NOT ACCEPTED, F11 G0 FAIL/G1 NOT RUN; ingen ny ROM/Stella/DASM körd i G1.
- Nuvarande MAIN-status och G1–G10 beredskapsplan lästes, liksom källvalsregistren för player/room/O1/K1/E1/key/door/RESET, v0.18 Scope/Acceptance/T01–T16 samt senare LM-D01–LM-D11.

## 3. Resultatet i fyra permanenta filer
1. [G1_REQUIREMENTS_TRACE_2026-11-17.csv](G1_REQUIREMENTS_TRACE_2026-11-17.csv) – **102 spårbara poster**: alla 57 original-ID, samtliga 11 kompletterande LM-D-id, alla 18 v0.18 A01–E04 acceptanskriterier och samtliga 16 T01–T16 test-ID. Varje rad har källa, äldre status, effektiv status, scope och ett relevant delta. **Normaliserad samlad katalog**, inte en omskrivning av ordagranna originalbeslut i ZIP.
2. [G1_BASELINE_MANIFEST_2026-11-17.json](G1_BASELINE_MANIFEST_2026-11-17.json) – originalarkivets fulla checksumreferenser, GitHub source blobs, status-/scopegränser, frysta F9/F10/F11 och verifieringsbaslinjens identiteter. Git SHA är en **snapshot**, inte ett evigt löfte att HEAD ska förbli identiskt efter dokumentationscommits.
3. [G1_AUTHORITY_DIFF_2026-11-17.md](G1_AUTHORITY_DIFF_2026-11-17.md) – faktisk senare supersession och tolkning, kandidat kontra bindande beslut, identifierade öppna frågor utan förtida designwaiver.
4. Detta mottagningsdokument – beslutet om G1-status och nästa auktoriserade gräns.

## 4. Skarpa fynd som nästa ansvariga chatt INTE får tappa
- **Original beslut 053 är historiskt supersederat endast för NTSC v0.18 R1–R4**, genom användarens särskilda Issue #6-samtycke. **Ingen** fullspelsscope, PAL eller ny F12 auktoriserad. Äldre "ROM paused" gäller sin tidpunkt och gör inte Issue #6 ogiltig.
- **Original 005 supersederade äldre åtta fiender med exakt sex**. Nuvarande standardfördelning M,M,F,F,SM,SF är fast; sex individuella numeriska X/Y är ett hårt v0.18-diagnotiskt mål, inte redan verifierad kapacitet.
- **Fyra rum** och endast högerutgång fast; speglade innerväggar; brun vägg. v0.11-källset `A01/B01/C02/D01` är bevarad diagnostikbaseline; nya v0.19 OPEN-room **exakta rutmatriser är kandidater**, inte godkända ersättningar. De är offline framkomlighetsstudier, inte pixel-Stella.
- **Gul spelare lika stor som stora androids**, hatt/vapen, visuellt inte större än dörröppningen är godkänt; **exakta spelarpixlar inte slutgodkända**. NPC 8×9 originalmaskreferenser måste vara rättvända i diagnostisk pixelaudit.
- **Guldnyckel med runt hål/kort tandat skaft och orange högerdörr med svart nyckelhål** är godkänd visuell riktning. `K11/K09/K09-R`, exakt färg och svart keyhole-mask är inte slutliga godkända sprite-/TIA-mönster. `D03` måste få särskild sann teknisk status. Brun port är endast teknisk testreserv, inte designwaiver.
- **O1**: android får visuellt skymma key men får inte flytta dess logiska X/Y. **K1**: om key uppstår under stillastående spelare får pickup ske tidigast nästa logiska tick och +50 exakt en gång. **E1**: skottträff före kroppskollision med träffad android, dödlig överlevande NPC-kontakt före faktisk rumsutgång/bonus.
- **GAME OVER/RESET**: ingen separat startsida och FIRE får inte starta om. Endast konsol RESET; effekternas exakta färger/blinkfrekvens är fortfarande öppna.
- **Full R1/R2/R3/R4** inte integrerat eller oberoende verifierat. F9 / R1e/f/g är begränsade experiment, inte sex godtyckliga numeriska X/Y. R1ba stora vertikalt felvända bilder får aldrig vara mask-PASS. PR #7 är draft, ingen merge.
- **Öppna verkliga frågor**: exakta fyra OPEN-rum, NPC/NPC exakt pixelöverlagring kontra logiskt aktörantal och visuell läsbarhet, exakt spelarsprite, K11/K09, färgflimmergräns, bakgrund/ljud/GAME OVER-effekt, svårighet C-1 och gameplay-AI/hitbox. De är flaggade och får inte få ett påhittat resultat.

## 5. Kvalitetskontroll, kvarvarande arbete och G1-beslut
- **Källkontroll:** originalarkiv öppnat, CRC och 20/20 checksums verifierade; 57/57 ID sekvenskontroll; referensmask jämförd på exakt Git blob-nivå; live Issue/PR kontrollerade; inga personliga Memory-referenser användes som auktoritet.
- **Spårbarhet:** 102/102 register-ID finns och har status/källa; verklig differens dokumenterad. Inga originalfiler raderades eller skrivs om. Ingen utvecklar-/verifieringsgren, ROM, TIA-assembler eller testkällkod ändrades.
- **Öppna poster:** åtta kategoriserade öppna design-/teknikpunkter. De är BEKANTA GRÄNSER och blockerar inte dokumentgrinden G1, men kan bli beslutspunkter vid G3–G5.
- **G1 resultat:** `DOCUMENTATION_COMPLETE_WITH_DOCUMENTED_OPEN_ITEMS`. Detta är administrativt, inte `E03 PASS` för en ROM.
- **Avbryt efter G1.** Nästa separat uppdrag bör vara **G2: faktisk käll-/råevidensgranskning av R1e/R1f/R1g och F9/F11**, med R1ba-korrigering och skarpa bevisklasser; denna G1-leverans **startar inte G2**, F12, G6, gameplay, ny mapper, PAL eller oberoende E02.

## G1 arkiveringskvittens (GitHub + projektets Drive, 2026-11-17)

- **Drive huvudrapport och auktoritet:** https://docs.google.com/document/d/1t41LBeuSLCxe-zpIwBgZJxMf11ZpUVXGL1BP2uQoPwQ/edit
- **Drive hela 102-postersregistret och fullständiga integritetsmanifestet:** https://docs.google.com/document/d/1gQv8njPYULlPGdeFPsKF-Olm6gSVGlq6I_egVRyu-0s/edit
- Bägge filerna är lästa tillbaka efter skrivning; bägge ligger i projektmappen `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.
- GitHub normativt maskinläsbart källformat: [G1 CSV](G1_REQUIREMENTS_TRACE_2026-11-17.csv), [manifest](G1_BASELINE_MANIFEST_2026-11-17.json), [differens](G1_AUTHORITY_DIFF_2026-11-17.md). Google Docs är bevarade sökbara speglar och skapar ingen ny användarcanon.

## 6. Signeringsgräns
Författare MAIN VI, dokumentär källgranskning. Inget tekniskt ROM-PASS, ingen ny användarauktorisation och ingen oberoende VERIFICATION-underskrift. All verklig framtida implementation kräver **separat uttrycklig arbetsorder** med fryst scope och rätt projektroll.

**Läs först för framtida G2:** [G1 authority diff](G1_AUTHORITY_DIFF_2026-11-17.md) + [G1 full registry](G1_REQUIREMENTS_TRACE_2026-11-17.csv) + [G1 manifest](G1_BASELINE_MANIFEST_2026-11-17.json) + [CURRENT_PROJECT_STATE](../CURRENT_PROJECT_STATE_2026-11-15.md).
