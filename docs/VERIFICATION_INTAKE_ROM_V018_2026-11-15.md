# VERIFICATION – oberoende intake för Let Me Out! v0.18 (ej utfört)

**Uppdrag:** Oberoende granskning av ROM DEVELOPMENT:s leverans för **enbart NTSC-diagnostik R1–R4**. Detta dokument är en uppdragsbeskrivning, inte ett verifieringsutlåtande.

## Låst evidensbaseline

- Projekt: https://github.com/Odourman/let-me-out
- Draft PR: https://github.com/Odourman/let-me-out/pull/7
- Commit: `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`
- Utvecklarens ZIP SHA256: `7500dae4f4a63d27f765bad3b3872384bd2ccb842a7e807abb9e50a475df2dc4`
- Utvecklarens ROM SHA256: `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`
- Besluts-/testunderlag på `main`: `docs/ROM_GATE_V018_SCOPE.md`, `docs/ROM_GATE_V018_ACCEPTANCE.md`, `planning/ROM_GATE_V018_TEST_MATRIX.csv`, `docs/ROM_GATE_V018_VERIFICATION.md`, `docs/ROM_GATE_V018_BLOCKERS.md`.

## Ditt ansvar

1. Läs och verifiera åtkomsten till GitHub/Google Drive och använd egna DASM-, Stella Debugger- och hashverktyg. Lita inte på utvecklarens PASS som bevis.
2. Hämta källkod vid **exakt commit**, gör ren rebuild och kontrollera SHA256 mot ROM i evidensarkivet. Rapportera avvikelse, även om utvecklarens CI var grönt.
3. Kör R1–R4 själv. Kontrollera fyra humanoidtyper i R1/R2, nyckelns oförändrade RIOT-position vid skymning och återkomst, ensidig högerdörr, orange färg och igenkännbart svart nyckelhål.
4. Mät riktig Stella-stabilitet med 600 sammanhängande bildrutor per R1/R2/R4 och kritiska TIA-/CPU-cykelpositioner (76-cykelsbudget). Redovisa faktiskt mätta värden, inte uppskattade Python-värden.
5. Bedöm kvalitativt `CLEAR`, `MINOR_FLICKER_READABLE`, `MAJOR_FLICKER`, `CRITICAL_OBJECT_LOST`. Lite flimmer är tillåtet men inte otillräcklig fiendeläsbarhet.
6. Sätt **PASS/FAIL/INCONCLUSIVE/NOT_RUN** för varje av de 16 fallen, bifoga artefaktvägar och bevis. Verifiera att inga delar kommer från The Cabin, I Love a Fish eller kommersiell Berzerk-ROM.
7. Skriv en **separat** `VERIFICATION_REPORT.md`. Ingen merger av PR #7. Avsluta med `PASS`, `PASS_WITH_EXPLICIT_DESIGN_WAIVER`, `FAIL` eller `INCONCLUSIVE`, utifrån ditt eget arbete och gällande acceptanskriterier.

**För närvarande rapporterar utvecklaren:** 5 PASS, 5 FAIL, 5 INCONCLUSIVE, 1 NOT_RUN. Din roll är att kontrollera detta oberoende; du får inte utgå från att dessa resultat är korrekta.

**Scope och skydd:** Verifiera, ändra inte ROM-koden och börja inte nästa utvecklingsfas. MAIN hanterar korrigeringsuppdrag inom befintligt auktoriserat v0.18. The Cabin och I Love a Fish är uteslutna.
