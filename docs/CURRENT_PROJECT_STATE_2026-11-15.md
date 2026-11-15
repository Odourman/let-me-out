# Let Me Out! – aktuellt projektläge (MAIN)

**Datum:** 2026-11-15  
**Omfattning:** endast Atari 2600-spelet *Let Me Out!*.

## Beslutsstatus

- 57 beslut registrerades i den ursprungliga överlämningen. Beslutsregistret i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip` är underlag för beslutens exakta status och historik.
- Senare studier v0.1–v0.13 är i huvudsak **rådgivande förslag**. Undantag: K1/E1 (kollisioner) och C02 (planerad kartlayout) godkändes av användaren i direkt svar på MAIN:s respektive förslag 2026-11-15; se separata beslutsloggar nedan.
- ROM-prototyp, 6502-kodning och test i Stella är **pausade** i väntan på uttryckligt separat godkännande.

## Fastställd kärna

Sex vita människoliknande androider, fyra stora och två små; en gul spelare. Fyra speglade labyrinter slumpas utan direkt upprepning. Start vid vänster sida, utgång genom låst högerdörr. En android bär nyckeln och måste förstöras för att den ska uppstå efter dödsanimationen.

Androiderna är ofarliga fram till första **faktiskt avfyrade** skottet, då de omedelbart börjar jaga. Androiderna skjuter aldrig. Högst ett aktivt spelarskott, ett per nytt knapptryck. Väggar är ogenomträngliga men ofarliga.

**Poäng:** -25 per android (aldrig under 0), +50 vid nyckelupptagning, +100 vid faktisk rumsutgång, +15 per överlevande android vid utgång. Tre liv, extraliv vid 500, 1500, 2500, osv. Strategin att skjuta alla är tillåten.

## Preliminära tekniska kandidater

- **Kartor:** Planerat fyrarum-set är **A01/B01/C02/D01**. **C02 är godkänd som planerad version av C**; C01 sparas som jämförelsekarta. A01/B01/D01 behålls oförändrade som hittills studerade kandidater. Ingen pixel- eller ROM-verifiering har skett.
- **AI:** P2 (patrullera rakt och sväng ibland) och J2 (enkel närmandelogik med kort slumpmässig omväg).
- **Svårighet:** C-1 är en föreslagen kurva, inte fastslagen hastighetsimplementering.
- **Grafik:** sex androider på samma rasterhöjd, spelarskott, dörr i speglad playfield och nyckel kräver verkliga timingtester.
- **Dörr:** v0.12 visar att alla fyra kartorna har samma högerdörrzon **x=39, y=9–12** och konstant stängd vänsterkant. Logikmodell 16/16 PASS, **inget ROM-test**. [v0.12](https://github.com/Odourman/let-me-out/blob/main/docs/DOOR_VISUAL_RIGHT_ONLY_STUDY_V012.md) föreslår orange smal port (V2) som visuellt mål, med brun PF0-port (V1) som tekniskt testbasfall. Färg och implementering är **inte godkända eller verifierade**.

## Senast godkända MAIN-beslut (K1/E1)

- **BESLUT K1:** Nyckel som uppstår under stillastående spelare får tas i nästa logiska uppdatering utan rörelse.
- **BESLUT E1:** Dödlig kontakt med överlevande android i öppnad dörr prioriteras före rumsbonus.
- Båda är **godkända som spelregler**, men **inte implementerade eller verifierade**: [beslutslogg](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md) och [avslutat GitHub Issue #1](https://github.com/Odourman/let-me-out/issues/1). [Underlag v0.9](https://drive.google.com/file/d/1Ztg48ihTanH58Z07OhH3Ge3-Rim2v3iC/view?usp=drivesdk).

## Senaste visuella användarreferenser

- Två användaruppladdade formreferenser från 2026-11-15: guldgul nyckel med runt hål/tandat kort skaft samt svart nyckelhål med rund topp och kilformad nederdel. Bilderna är vattenmärkta stockfoton; **originalbilderna har inte lagts i publika GitHub eller i ZIP**. Projektet använder egna bitmapskisser i v0.13.
- Originalnyckelns form var redan beslutad i Master Spec; ny bild preciserar det visuella målet utan att ändra poäng eller kollisionsyta.

## Viktigaste öppna val

1. **C02 valt som planerad karta C** (beslut; inte speltestad): [GitHub-beslut och spawngranskning v0.11](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_MAP_C02_AND_SPAWN_AUDIT_V011.md), [Drive-paket](https://drive.google.com/file/d/1WbnLfcSKM-bqmVIz5jCJ0ga0sUzPU0UK/view?usp=drivesdk), [avslutat Issue #2](https://github.com/Odourman/let-me-out/issues/2). A01/B01/D01 ej ändrade. Jämför bara A/B/D med annat utförande om senare speltest kräver det.
2. **Spawnspelbalans ännu öppen:** samtliga 64 045 möjliga sexstartval ur nuvarande fyra pools klarade offline 2×2-kontroll. S0 oförändrad bas, S1 (minst 12 fyrvägssteg från spelarstart) **endast testkandidat**.
3. Detaljer för patrullering, jakt och svårighet (P2/J2/C-1), tills vidare testkandidater.
4. **VISUELLT MÅL BESLUTAT v0.13:** guldgul nyckel med runt genomgående hål och kort tandat skaft; smalt orange dörrstreck med **svart nyckelhål**. Hela dörren och symbolen försvinner vid upplåsning. [Beslutsunderlag](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md) och [avslutat designärende #4](https://github.com/Odourman/let-me-out/issues/4). **Exakt pixelmask och TIA-teknik överifierade.** [Öppet framtida testärende #5](https://github.com/Odourman/let-me-out/issues/5).
5. Grafikarkitektur och tolerans för flimmer – först efter uttryckligt godkänd ROM-prototyp.

## Källor och isolation

- [Let Me Out! i Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) – fjorton versionerade ZIP-arkiv från huvudöverlämningen till visuell nyckel- och dörrstudie v0.13, inklusive manifest, plus kartdata JSON och separata mobilrapporter.
- [GitHub-förrådet](https://github.com/Odourman/let-me-out) – egna projekttexter, inga tredjeparts-ROM:er.
- Ändra aldrig **The Cabin** eller **I Love a Fish** som del av detta projekt.
- **Linear används inte för Let Me Out!** (användarbeslut 2026-11-15). Arbetsuppgifter hanteras vid behov i GitHub Issues.

**Auktoritet:** Senare direkta användarbeslut > registrerade spelbeslut > experimentella modellförslag > tredjepartsresearch.  
**Detta är en statusöversikt**, inte ersättning för originalbeslutsregistret.