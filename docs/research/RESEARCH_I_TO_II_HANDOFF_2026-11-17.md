# LET ME OUT! – RESEARCH I → RESEARCH II
## Ren chattmigrering, källor, ansvar och spärrar
Datum: 2026-11-17
Status: rådgivande forskningshandoff. INGET nytt ROM-mandat, canonbeslut eller VERIFICATION.
Roller: MAIN V leder och beslutar. ROM DEVELOPMENT II implementerar endast separat godkänt scope. VERIFICATION granskar självständigt. RESEARCH II söker, granskar, jämför och rapporterar källbelagd teknik, utan kodändringar.

SYFTE
Denna handoff gör det möjligt att överge den långa RESEARCH I-chatten och börja en fristående RESEARCH II-chatt som kan arbeta självständigt från verkliga projektkällor. Chatthistorik eller Memory är inte auktoritet. Överlämningen ersätter INTE MAIN:s aktuella projektstatus, beslutsregister eller arbetsorder. En ny chatt skapas manuellt av användaren; ingen chatt kan automatiskt flyttas av denna fil.

KÄLLOR OCH HÖGRE AUKTORITET – LÄS LIVE
1. https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md – historiskt filnamn men löpande uppdaterat innehåll; läs ÖVERSTA nya beslut först.
2. https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md – användarbeslut, visuella mål, begränsningar och äldre 57 beslut.
3. https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F10_SOURCE_ONLY_RECEIPT_AND_F11_DECISION_2026-11-17.md – F10 avslutat, F11 beslutat.
4. https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F11_FOUR_NUMERIC_X_P1_DIAGNOSTIC_ONE_ROM_AUTHORIZED_2026-11-17.md – bindande F11-gräns; ENDA nya auktoriserade diagnostikuppdraget vid denna lästidpunkt.
5. Fryst F10-källa: https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md
6. Projekt-Google Drive: https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u
7. Aktuella brancher, commits, issues och bilagor måste kontrolleras i GitHub vid nytt uppdrag. Äldre PR #7 är historisk draft, inte automatiskt dagens utvecklings-HEAD; Issue #8 är äldre fryst oberoende verifieringsgrind.

KONTROLLERAD STATUS 17 NOVEMBER 2026 (SNAPSHOT, UPPDATERAS INTE AUTOMATISKT)
- R1-F9: developer-local + MAIN direkt pixelgranskning av TRE olika rättvända originalmasker och TRE fristående BINÄRA RAM-X-val i åtta fasta lägen, 144/144 äkta PNG-pixelpass. Detta är INTE tre godtyckliga numeriska X, ingen fri Y och inte sex oberoende X/Y.
- F10: SOURCE-ONLY accepterat/stängt: F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN. Tre familjer A (datastyrd P1/RESP/GRP), B (bankfördelad standard-F6), C (NUSIZ/Y/VDEL) analyserade; sex fria X/Y inte visade. Source-only cykellower-bound 61/76 gäller en SPECIFIK metod, inte universell omöjlighet.
- F11: ENDA aktuellt uttryckligt MAIN V-uppdrag: G0 source-only först, sedan högst EN standard F6/NTSC ROM om G0 passar. Fyra oförändrade rättvända M/F/SM/SF originalmasker med numeriska RAM-X, förregistrerad A [16,36,56,76] CC → B [19,36,56,76] CC, P0 spelare, M0 skott, PF väggar, same-Y och exakt raster-/pixelbevis. STOPP vid G0 FAIL/första fel, inget F12 eller sexobjekt-test utan nytt beslut.
- Full R1 fortsätter BLOCKED/NOT ACCEPTED; R2 nyckelkonflikt och R3 högerdörr kvar som separata integrationsfrågor.
- Originalmål: sex människoliknande vita androider i fyra formtyper (2 stora M, 2 stora F, liten M, liten F), gul spelare, skott, fem androider plus nyckel i R2, högerdörr endast, original grafikmasker och stark same-Y-test. Inga tysta ändringar av krav, mängd eller färger.

ARKIVERAD RESEARCH (RÅDGIVANDE, TIDIGARE DATUM)
- Komplett historiskt forskningspaket (30 ursprungliga trick + 52 överlappande teknikmönster + 67 riskscenarier + källförteckning): https://drive.google.com/file/d/1JgLBpjUIVRQegVUFVNn3DoZpxguDqSs4/view
  SHA-256 ursprungligt ZIP 5b2046cd78dd65e6b64806dc3b90e20ef87059c988eeb2b2ef3e7a7591bbefe8; storlek 902192 byte; ZIP CRC lokal PASS.
- Samlad historisk avhandling (55 sidor): https://drive.google.com/file/d/1IHKg63PZGAYoi3fdJdwmOYsomDxumlIv/view
  SHA-256 ursprunglig PDF 596ee313bbbfcf3926efea61807a7b169363dd1aef994a4fc9a635877c62019f.
- Exakt original 30-tricksbilaga redigerbar: https://drive.google.com/file/d/1ASGA7wDZNsYNILVOswdQJfdvpOBtDKM2/view
  https://github.com/Odourman/let-me-out/blob/main/docs/research/ATARI_30_ORIGINAL_TRICKS_HISTORICAL_2026-11-16.md
- The Cabin-överföring i repo: https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_THE_CABIN_TRANSFER_2026-11-15.md
- Viktiga teknikkällor: Stella Programmer's Guide, AtariAge TIA/bankswitching, Stella Debugger, 8bitworkshop Versatile Playfield/Three Stream, Cyloid, AStar, Space Invaders, Video Chess och historisk gameplayassembler. Källkritik och eventuella GPL/upphovsrättskrav måste redovisas.

RESEARCH II:S FUNKTION
A. Verifiera tillgång till GitHub och Google Drive vid uppstart; använd dessa appar och webbresearch direkt. Om åtkomst saknas, säg vilken exakt källa som inte gick att läsa.
B. Innan varje faktapåstående om status, pågående gate, versionsnummer, hash eller auktorisation: kontrollera livekällan, håll isär fryst commit, utvecklarens lokala PASS, MAIN-mottagning och oberoende VERIFICATION.
C. Undersök 30 trick och 52 teknikmönster med precis verkan på TIA-kopia/GRP-latch/RESP/START/76 cykler/128 B RIOT/4 KB aktiv F6-bank. Ange emulator- och källbevis, inte bara analogier till kända spel.
D. Prioritera fruktbar research om sex numeriskt fria X/Y och framför allt falsifierbara mål som MAIN själv får välja. Respektera F11 som aktivt utvecklingsscope, aldrig ge ROM DEVELOPMENT nya steg genom research.
E. Lämna läsbara forskningsrapporter till MAIN med observation / källa / begränsning / konkreta experimentidéer / stoppkriterier / kostnad / icke-goals / status. Ändra aldrig MAIN-status eller design-canon på eget initiativ.
F. Ingen implementering, ingen assembler/ROM-bygge, ingen Stella-test som påstås oberoende verifiering, ingen PR-merge, inga ändringar i The Cabin/I Love a Fish, inget Linear för detta projekt.
G. RESEARCH I är avslutad som aktiv forskningsyta när RESEARCH II skapats. Ny chatt ska INTE försöka fortsätta i gammalt chattfönster.

FÖRSTA RESEARCH II-SVAR
Efter att ha läst startprompten: (1) redovisa verifierade huvudkällor, (2) sammanfatta aktuell gate i 5–10 meningar, (3) skilj gamla 30 trick från senare F10/F11, (4) föreslå högst tre konkreta forskningsfrågor som inte innebär nya implementationsmandat. Fråga inte användaren att återberätta innehållet i arkiven när de går att läsa.
