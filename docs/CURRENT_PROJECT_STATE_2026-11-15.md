# Let Me Out! – aktuellt projektläge (MAIN)

**Datum:** 2026-11-15  
**Omfattning:** endast Atari 2600-spelet *Let Me Out!*.

## Beslutsstatus

- 57 beslut registrerades i den ursprungliga överlämningen. Beslutsregistret i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip` är underlag för beslutens exakta status och historik.
- Senare studier v0.1–v0.9 är i huvudsak **rådgivande förslag**. Undantag: K1 och E1 godkändes av användaren i direkt svar på MAIN:s fråga 2026-11-15; se beslutslogg nedan.
- ROM-prototyp, 6502-kodning och test i Stella är **pausade** i väntan på uttryckligt separat godkännande.

## Fastställd kärna

Sex vita människoliknande androider, fyra stora och två små; en gul spelare. Fyra speglade labyrinter slumpas utan direkt upprepning. Start vid vänster sida, utgång genom låst högerdörr. En android bär nyckeln och måste förstöras för att den ska uppstå efter dödsanimationen.

Androiderna är ofarliga fram till första **faktiskt avfyrade** skottet, då de omedelbart börjar jaga. Androiderna skjuter aldrig. Högst ett aktivt spelarskott, ett per nytt knapptryck. Väggar är ogenomträngliga men ofarliga.

**Poäng:** -25 per android (aldrig under 0), +50 vid nyckelupptagning, +100 vid faktisk rumsutgång, +15 per överlevande android vid utgång. Tre liv, extraliv vid 500, 1500, 2500, osv. Strategin att skjuta alla är tillåten.

## Preliminära tekniska kandidater

- **Kartor:** A01/B01/C01/D01 är förslag, C02 är modifierat rum C som underlättar enkel jakt-AI.
- **AI:** P2 (patrullera rakt och sväng ibland) och J2 (enkel närmandelogik med kort slumpmässig omväg).
- **Svårighet:** C-1 är en föreslagen kurva, inte fastslagen hastighetsimplementering.
- **Grafik:** sex androider på samma rasterhöjd, spelarskott, dörr i speglad playfield och nyckel kräver verkliga timingtester.
- **Dörr:** PF0-/playfield-ändring är en hypotes, inte verifierad lösning.

## Senast godkända MAIN-beslut (K1/E1)

- **BESLUT K1:** Nyckel som uppstår under stillastående spelare får tas i nästa logiska uppdatering utan rörelse.
- **BESLUT E1:** Dödlig kontakt med överlevande android i öppnad dörr prioriteras före rumsbonus.
- Båda är **godkända som spelregler**, men **inte implementerade eller verifierade**: [beslutslogg](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md) och [avslutat GitHub Issue #1](https://github.com/Odourman/let-me-out/issues/1). [Underlag v0.9](https://drive.google.com/file/d/1Ztg48ihTanH58Z07OhH3Ge3-Rim2v3iC/view?usp=drivesdk).

## Viktigaste öppna val

1. Godkännande eller korrigering av C02 och övriga labyrinter.
2. Detaljer för patrullering, jakt och svårighet (P2/J2/C-1), tills vidare testkandidater.
3. Grafikarkitektur och tolerans för flimmer – först efter uttryckligt godkänd ROM-prototyp.

## Källor och isolation

- [Let Me Out! i Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) – tio versionerade ZIP-arkiv från huvudöverlämning till kollisionsförslag v0.9, inklusive manifest.
- [GitHub-förrådet](https://github.com/Odourman/let-me-out) – egna projekttexter, inga tredjeparts-ROM:er.
- Ändra aldrig **The Cabin** eller **I Love a Fish** som del av detta projekt.
- **Linear används inte för Let Me Out!** (användarbeslut 2026-11-15). Arbetsuppgifter hanteras vid behov i GitHub Issues.

**Auktoritet:** Senare direkta användarbeslut > registrerade spelbeslut > experimentella modellförslag > tredjepartsresearch.  
**Detta är en statusöversikt**, inte ersättning för originalbeslutsregistret.