# Let Me Out! - uttrycklig kodauktorisation för endast v0.18

**Datum:** 2026-11-15
**Auktorisation:** Användaren skrev uttryckligen: "Jag godkänner uttryckligen ROM-kodning för enbart Let Me Out! diagnostik v0.18, med NTSC som första videosystem och 16 KB F6 om tekniskt motiverat. Följ scope R1–R4, acceptanskriterier och separat VERIFICATION. Ingen fullspelsutveckling är godkänd."

## Tillåtet
- ROM DEVELOPMENT får påbörja en reproducerbar **NTSC-diagnostik-ROM v0.18** i **Odourman/let-me-out**.
- Endast R1 sex androider + spelare + testskott, R2 fem androider + spelare + nyckel + testskott/O1-skymning, R3 ensidig högerdörr med låst/öppet, orange port/svart nyckelhål, R4 reproducerbar raster-/rörelsestress.
- 16 KB F6 får användas om tekniskt motiverat; dokumentera format och byggrecept.
- Endast separat, oberoende VERIFICATION får utfärda slutligt verifieringsutlåtande.

## Inte tillåtet
- Fullt spel, komplett AI, poäng/HUD, ljud/Game Over, progressionssystem, PAL-cutover, ytterligare senare ROM-steg eller ändrade spelregler.
- Ändringar i The Cabin eller I Love a Fish; Linear används inte.
- Publicering av Berzerk-ROM, tredjepartsdisassembly eller användarens vattenmärkta referensbilder.

## Bindande uppdragsunderlag
- [Scope](ROM_GATE_V018_SCOPE.md)
- [Acceptans](ROM_GATE_V018_ACCEPTANCE.md)
- [Testmatris](../planning/ROM_GATE_V018_TEST_MATRIX.csv)
- [VERIFICATION-kontrakt](ROM_GATE_V018_VERIFICATION.md)
- [Stoppkriterier](ROM_GATE_V018_BLOCKERS.md)
- [GitHub Issue #6](https://github.com/Odourman/let-me-out/issues/6)

**Status:** Auktoriserat att implementera och egenkontrollera endast v0.18. **Ingen kod är ännu rapporterad byggd eller oberoende verifierad.**
