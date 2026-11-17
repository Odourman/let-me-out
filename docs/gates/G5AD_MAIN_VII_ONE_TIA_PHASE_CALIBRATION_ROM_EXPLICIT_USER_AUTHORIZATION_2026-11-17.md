# LET ME OUT! – MAIN VII G5AD: EN enda TIA-fas-/kopiekalibrerings-ROM – uttryckligen auktoriserad

> **SENARE AVSLUT LM-D21/G5AE (2026-11-17):** Denna order var uttryckligen auktoriserad men har sedan genomförts till förbyggsgrinden och korrekt STOPPATS `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER` innan ROM-bygge. Ingen TIA-C0–C4/N1 mätt, ingen ny ASM/BIN/DASM/STELLA G5AD-case. [MAIN:s G5AE granskning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) · [fryst ROM DEVELOPMENT III leverans](https://github.com/Odourman/let-me-out/blob/1fe92438c3aa0d9f41cca0066f0a95e6c0335acc/rom/g5ad_tia_calibration_2026-11-17/TO_MAIN_G5AD_TIA_CALIBRATION.md) · [Issue #13](https://github.com/Odourman/let-me-out/issues/13). **Den här historiska LM-D21-ordern är inte fortfarande aktiv och får inte starta om automatiskt.** Full H4/G1/G6/F12/S05/fem-NPC/ny Verification/PRmerge fortsatt ej auktoriserad.

**Datum:** 2026-11-17. **Besluts-ID:** `LM-D21`. **Status:** `G5AD_SINGLE_TIA_MEASUREMENT_ROM_AUTHORIZED_NOT_YET_EXECUTED`.
**Beställare:** MAIN VII. **Utförare:** ROM DEVELOPMENT III. **Mottagare:** MAIN VII för käll-/artefaktkontroll. **Oberoende Verification II:** EJ beställd.
**Mandatets avgränsning:** ett tekniskt instrumenterat, isolerat Atari 2600 standard-F6 NTSC-kalibreringsförsök för bestämda TIA-registerfaser, **inte H4-ONE fullt, inte G6/F12, ingen spelimplementation, inget PF/S05-/femfienders-PASS eller PR-merge**.

## 1. Direkt uttrycklig användarauktorisation och tidigare källa
MAIN VII rekommenderade uttryckligen **"ett enda begränsat TIA-mätprov, där vi undersöker de faktiska RESP, GRP, NUSIZ0, M0 och ENAM0-effekterna som G0 inte kunde avgöra"** i stället för större källanalys eller byggandet av spelet.
**Användaren svarade: "Gör så"** direkt på den citerade rekommendationen.
Detta är ett senare **exakt positivt** användarbeslut att låta ROM DEVELOPMENT III implementera och köra just det avgränsade tekniska mätprovet i Stella. Det supersederar tidigare `G1/NEW_ROM_NOT_AUTHORIZED` **endast för detta G5AD-diagnostikuppdrag**, inte för full H4/G6/F12/S05/femfienders- eller spel-ROM. Ett allmänt "fortsätt" behövdes inte; explicit order finns.

Tidigare, fortfarande giltiga primärkällor:
- [G5AC förberett, men då ännu inte godkänt testkoncept](G5AC_MAIN_VII_TIA_PHASE_CALIBRATION_DECISION_READY_NOT_AUTHORIZED_2026-11-17.md); efter LM-D21 är enbart det specifika G5AD-provet nu godkänt.
- [G5AA MAIN:s slutgranskning av G5Z G0 H4-ONE `INCONCLUSIVE_NO_ROM`](G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) och [specialistens frysta G0-rapport](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md).
- [G4 ursprungliga H4-ONE fysiska hypotes](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md) och [G2 historiska negativa/non-repeat](G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md). **Dessa är referenser, inte G5AD:s acceptance eller nytt fulltest.**
- [G5X framtida exakta fyra kartor](G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json), [LM-D12..13](G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D14..16](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) gäller som framtida designkrav, utan ändringar.

## 2. Förhållningsregel till emulator och verklig hårdvara
En ROM faktiskt byggd med DASM och körd i Stella är **ett emulatormätt tekniskt resultat**, inte ett fysiskt test på original-Atari. Stella 6.7.1 är en relevant referenskälla (se `Player.cxx`, `TIA.cxx`, `Missile.cxx`), men observerat Stella-beteende ska uttryckligen märkas `STELLA_OBSERVED`. Källkod kan hjälpa tolka observationer men får inte ersätta rå emulatormätning, och emulatorns modell får inte förklaras likvärdig med all verklig TIA-hårdvara utan annan grundad test.

## 3. Leveransomfång: EXAKT ETT diagnostiskt NTSC/F6-ROM-bygge med flera förregistrerade kontrollscener
ROM DEVELOPMENT III får:
- Skapa **en** ny, separat diagnos-ROM-källfamilj och **en slutligt fryst standard-F6 16 KiB NTSC `.bin`** (max aktiv bank 4 KiB, RIOT 128 byte inklusive stack, 76 CPU-cykler per scanline). Nödvändiga interna utvecklingsbyggen för att nå **en korrekt fungerande leverans** är tillåtna inom samma snäva implementation, men inga parallella experimentfamiljer eller flera olika levererade ROMs.
- Programmera **enbart** separata kontrollscener `TIA-C0`, `TIA-C1`, `TIA-C2`, `TIA-C3`, `TIA-C4`, `TIA-N1`; deras scenval och nödvändiga numeriska X/phase-parametrar kan styras av RAM/Testkontroll eller en **förregistrerad** diagnostik-tabell. **Detta är tillåtet för kalibrering**, men får aldrig marknadsföras som H4:s dynamiska X-sorteringskärna. Behåll en enda slutlig binär så samma ROM-hash gäller samtliga slutfall.
- Köra den frysta ROM:en i Stella/Debugger, samla **verkliga CPU-PC/cykel-, TIA-register-, scanline- och råpixelpositioner i synliga colorclocks**. Använd stabil angiven Stella-version och dokumentera build/ROM SHA256. Om råa effekter inte kan mätas tillräckligt noggrant med tillgängliga verktyg, klassificera det **NOT_DETERMINABLE**, inte PASS.
- Använd källtroget 8×9-maskband för figurer i kontrollfall där masksynlighet är väsentlig och hänvisa direkt till `design/NPC_REFERENCE_8x9_masks.json` (original TOP-DOWN); ingen omritning av masker eller smygändring av spelregler. En ensam färg-/pixelkalibreringskontroll får ha enklare testmönster endast **om den är uttryckligt märkt som diagnostiskt kontrollmönster**.

**Förbjudet:** ändra `design/` original, v0.11/v0.18 baseline eller historiska testresultat, bygga H4-ONE komplett eller framtida R1/R2/S05-integrationen, börja G6/F12, införa förkompilerad slutspels-Y-lane eller generell flicker/key-waiver, skapa PR-merge, beordra oberoende Verification II utan separat godkännande.

## 4. Förregistrerade scener och kravet att de verkligen skiljer mellan hypoteser
Alla slutfall dokumenteras med **gemensam fryst ROM-hash**. Varje scenario ska beskriva numerisk RAM-X, maskrader/identitet, exakt `STA`-skrivfönster och TIA-skärmutdata i CC. Den exakta scenmatrisen finns i [G5AD testregister](G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv). Nedan anges *avsiktlig* skillnad som ska kunna upptäckas, **inte redan fastställda uppmätta cykler**.

| ID | Syfte och minst kontrollerna | Krav för bestämbart resultat |
|---|---|---|
| `TIA-C0` | Stabil baslinje: ensam P0 8×9-bitmap vid minst två numeriska X; skilj P0-pixel-CC från CPU-cykel/STA-counter. | En identifierbar bitmap i alla nio rasterrader, samma orientering, jämförd CC för två X. Utan tydlig C0 är beroende fall inte bestämbara. |
| `TIA-C1` | `RESP0` under/strax före aktiv P0-bitmap med *separat* kontroll för gul→vit och vit→gul identitetsordning; mät klipp/ghost/START-fas under ändrat skrivögonblick. | Bevara aktörsidentitet och source-mask och ange om det ena fönstret påverkas. **Gäller P0 i isolation**, inte H4 med P1+PF+M0. |
| `TIA-C2` | P0 `NUSIZ0=$02` med **en avsiktligt aktiverad M0 samma Y**, jämfört med ensam M0-baslinje utan P0-kopiefterfrågan; M0-position/antal/storlek. | Mät varje synlig missile-kopia i CC och dess scanline. Ingen separat föregående rad som fejkad same-Y. |
| `TIA-C3` | Från samma C2-kontroll jämför **förregistrerade** `ENAM0`-start/stopp-faser och ev. reset som kan påverka oavsiktlig M0-kopia. | Samma start-X/-Y och NUSIZ som C2, endast explicita aktiveringsfönster skiljer; notera en/extra/noll M0. |
| `TIA-C4` | Kontrollera `GRP0` **och** `GRP1` uppdatering före och närmast aktiv bitmap-START; jämför särskilt påverkan av GRP1 på fördröjda P0-state/shuffle. | Pixelmönster jämförs med rätt markerade `VDELP0/1` och uppskjuten latch; ingen falsk omedelbar `GRP`-effekt. |
| `TIA-N1` | Färgdelning: vit P0-pixel plus begärd separat gul M0 **exakt överlappande colorclock**. | En och samma fysiska `COLUP0` kan inte samtidigt lagra två olika färger. Negativ kontroll **för denna allokering**, inte H4 allmän NO-GO. |

**Skilj testväsentligt**:
- En *observerad* C2-duplicering och en *observerad* C3-gate ska jämföras med P0-/M0-state i samma scanline; övriga signaler hålls konstanta. En frånvaro av duplikat i C2 måste också rapporteras, inte tvinga fram C3-"räddning".
- Ett kontrollfall som kör med PF avstängt kan **inte** användas som evidens för bruna PF-väggar i H4 eller kartornas 40×22-raster.
- TIA-GRP/RESP skrivslut eller synlig pixel-fas bör uttryckas i **både CPU-clock i scanline och synlig colorclock** med skärmens HBLANK/offset explicit. En nominell `x=3c`-formel utan råpixel-/registerlogg räcker inte.
- **Öppna inte fler ROM-varianter** för att dölja misslyckade scener. Komprimera hellre resultaten och märk `NOT_DETERMINABLE` om en specifik mätning inte kan stödjas.

## 5. Go/no-go före slutlig ROM, när uppdraget får stoppas
**Inom denna redan auktoriserade en-ROMS-order** gör ROM DEVELOPMENT III en kort källbaserad *instrumenterbarhetskontroll* innan första meningsfulla slutbygge: går separata C0–C4/N1-moder, testvärden, cykelbokföring och Stella-trace faktiskt att reproducera med tillgängliga verktyg?
- **Om nej:** leverera `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER` med en konkret orsak och möjliga senare mätkrav. **Ingen ROM med fabricerad PASS.** Ingen extra auktorisation för nytt verktyg/mätfamilj följer av detta.
- **Om ja:** bygg *en* final `.bin`, pin SHA256, frys före slutlig mätmatris, kör dokumenterade C0–C4/N1-kontroller och leverera oavsett resultat.
- **Om några fall är oavgörbara:** leverera vad som faktiskt mättes och markera exakt vilka celler är `NOT_DETERMINABLE`; ROM-order ändå avslutad, inget automatiskt påföljande ombygge.

**Endast tillåtna per-case verdicts:** `OBSERVED_EXPECTED`, `OBSERVED_UNEXPECTED`, `NOT_DETERMINABLE`. **Global leveransstatus:** `G5AD_MEASUREMENT_COMPLETE_BOUNDED` / `G5AD_PARTIAL_NOT_DETERMINABLE` / `G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER`. Inget `H4_PASS`, `G5_PASS` eller `G6_GO`.

## 6. Bindande dokumentation, verifierbar leverans, en slutlig STOPP
Leverera på en **ny isolerad ROM DEVELOPMENT III-branch**, gärna under `rom/g5ad_tia_calibration_2026-11-17/`, utan originaländringar/merge:
1. **Körbar standard-F6/NTSC `.bin` (en fryst leveransbinär)**, komplett käll-ASM, DASM-buildlogg/kommandon, `.lst/`.sym` diagnostik vid behov; exakt 16 384 byte, SHA-256 och Git full commit.
2. **PLAYTEST.md / TEST_PROTOCOL.md** som förklarar scenval, joystick/RAM/testparametrar, förväntade testfenomen, hur de reproduceras; inga fuskade tidsresultat.
3. **RAW_TRACES/** Stella/Debugger bevis, version och inställningar, CPU/scanline/cycle/PC samt `RESP0/1`, `GRP0/1`, `NUSIZ0`, `ENAM0`, `RESM0`, `COLUP0` och rå pixelCC, per kontrollfall. Screenshots räcker **inte** ensamma.
4. **TO_MAIN_G5AD_TIA_CALIBRATION.md** med varje per-case-värde, eventtabell och exakt verdict, byte-/CC-räkning och ärlig avgränsning mot H4/S05/fem-NPC. Ange okända faser explicit.
5. **MANIFEST.txt** filindex och hashar, tidigare historisk negativ evidens kvar i källregister, inga tidigare originalfiler skrivs över.
6. Publicera GitHub-länkar och, om möjligt, verifierad leveranskopia i **officiell Google Drive-mapp**. Utföraren gör egenkontroll; **oberoende VERIFICATION II är separat arbete**.

**STOPP efter en leverans till MAIN VII**. Inget ROM-merge, ingen följande H4-/S05-/fem-NPC-testorder, inget G6, ingen separat verifiering utan nytt explicit användarmandat. GitHub Issue får vara en aktiv specialistorder men startar inte automatiskt den separata ChatGPT-ROM DEVELOPMENT III-chatten.

## 7. Tidigare och senare status i samma källa
`G5Z_G0_H4_ONE=COMPLETE_INCONCLUSIVE_NO_ROM` (bevarad historisk status), **`G5AD_SINGLE_EMULATOR_CALIBRATION=AUTHORIZED_NOT_YET_RUN`** (nytt, separat uppdrag).
**`G5_FORMAL_OPEN`**. `FULL_H4_G1/G6/F12/S05/FIVE_NPC_IMPL/PR_MERGE/NEW_INDEPENDENT_VERIFICATION=NOT_AUTHORIZED`.
