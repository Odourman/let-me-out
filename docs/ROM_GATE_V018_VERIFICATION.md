# 04 – Separat oberoende VERIFICATION-kontrakt

## Mottagare
VERIFICATION ska vara **separat från ROM DEVELOPMENT** och får inte enbart kopiera utvecklarens PASS. MAIN sammanställer mottagarnas leveranser men ändrar inte uppmätta resultat för att de ska passa förslaget.

## Inför verifiering
1. Kontrollera faktiskt åtkomst till **eget** Let Me Out!-GitHub och Google Drive. Ändra inte The Cabin eller I Love a Fish. Använd tillgängliga verktyg automatiskt om åtkomst finns (Stella, DASM/annan assembler, debugger, hashverktyg).
2. Hämta **den faktiskt levererade ROM-zippen, GitHub-commit och manifestet** från framtida ROM DEVELOPMENT, inte ett tidigare designpaket som v0.16.
3. Notera OS, buildverktygs-version, Stella-version, NTSC/PAL-läge, ROM hash och commit hash.
4. Gör ren reproducibel byggning; jämför SHA-256 bit-för-bit.

## Oberoende körning
- Kör R1 och R2 minst föreslagna 600 bildrutor **efter init**, med logg av antalet scanlines per frame och kritiska cykelpositioner.
- Ändra verkliga objektplaceringar inom fördefinierade scenariointervall och kontrollera om samma TIA-kernel fortsätter fungera; ett enda fruset skärmdump-fall räcker inte.
- Kör O1-nyckeln genom att skymma den helt, låta en android stå kvar en längre tidsperiod och flytta den därifrån. Kontrollera **både skärmbilden och sparad logisk nyckelkoordinat**.
- Kör dörren stängd och öppen; kontrollerna måste särskilja vänster från höger i samma TV-bild. Bedöm separat orange port och svart nyckelhål.
- Kontrollera fyra silhuetter (två stora/två små), synlig spelare och aktivt skott i värstafallen.
- Kontrollera att filerna i ROM DEVELOPMENT:s arkiv går att reproducera, samt att inga kommersiella Berzerk-ROM-bytes eller tredjepartsassets har råkat publiceras.

## Resultatmall
För varje `test_id` i `03_TESTMATRIS.csv`: resultat `PASS`, `FAIL`, `INCONCLUSIVE` eller `NOT_RUN_IN_ROM` och separat `evidence_path`, `frame_start`, `frame_end`, `worst_scanline`, `max_cycle`, `observed_artifact`, `verifier_notes`. Lämna blankt för det som inte mätts; fyll aldrig med fiktiva siffror.

## Visuell granskning
Kvalitativ klassning `CLEAR`, `MINOR_FLICKER_READABLE`, `MAJOR_FLICKER`, `CRITICAL_OBJECT_LOST`. Användaren har accepterat lite flimmer, men inte godkänt ett numeriskt tröskelvärde. Varje `MAJOR_FLICKER` eller `CRITICAL_OBJECT_LOST` är blockerande tills lösning finns eller användaren uttryckligen beslutar om en specifik kompromiss.

## Slutrapport
Separat `VERIFICATION_REPORT.md` med uppdragsscope, bevislista, käll-/ROM-hash, exakt Stella-version, återbyggnadsresultat, bildbedömning, tester per ID, kvarstående fel, slutbedömning. Respektive brist får inte redigeras bort i MAIN-status.
