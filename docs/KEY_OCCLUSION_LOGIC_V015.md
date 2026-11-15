# MAIN v0.15 – Nyckelns synlighet när en android går över den

**Datum 2026-11-15. STATUS: rådgivande designstudie. Ingen ny visuell prioritetsregel godkänd; ingen ROM-kodning auktoriserad.**

## Redan gällande regler
1. Nyckeln uppstår på nyckelbärarens fallposition **efter** dödsanimationen. Den är stilla tills spelaren hämtar den. En android får gå över nyckeln utan att flytta eller plocka upp den (Master Spec §7; beslut 023–025).
2. Spelaren får +50 exakt en gång vid faktisk upptagning (beslut 044).
3. **K1:** Nyckeln som uppstår under stillastående spelare kan tas tidigast **nästa logiska uppdatering**, inte samtidigt som den visas.
4. Skottet som eliminerar en samtidigt kolliderande android har företräde; andra överlevande androider kan fortfarande orsaka dödlig kontakt. Dödlig kontakt avgörs före ännu ej intjänad nyckelbonus.
5. v0.13:s guldnyckel med runt hål och tandat skaft och v0.14:s djupguldton som **färgtestkandidat** består; exakta pixelmasker och TIA-färger är inte låsta.

## Tre möjliga visningsprinciper
- **O1 – Android över nyckel (MAIN:s preliminära rekommendation):** nyckeln kan skymmas helt eller delvis när en android passerar. **Logiskt läge oförändrat**; samma nyckel blir synlig på samma koordinat när androiden flyttat sig. Ingen avsiktlig blinkning.
- **O2 – Nyckel över android:** nyckeln förblir synlig men kan skymma en farlig android och ge rasterproblem.
- **O3 – Bildruteväxling/blinkning:** varannan bildruta för key/robot. Risk för störande flimmer. Rekommenderas inte innan faktisk TIA-/speltest.

**Föreslagen arbetsbas är O1, inte ett fastställt beslut.** Den kostar inget nytt logiskt tillstånd för att styra roboters beteende, men TIA-renderingen är fortfarande en öppen teknisk fråga. Undersök senare om en android kan stå ovanpå nyckeln så länge att spelaren inte ser den.

## Genomförda kontroller
- **20/20** deterministiska **offline-händelsetester** passerade i separat Pythonmodell.
- Testfall täcker bland annat animationen, K1-timing, engångsbonus, 1–3 överlappande androider utan förändring av nyckelposition, återkomst efter skymning, skottprioritet och dödlig kontakt.
- **Inte testat:** riktiga Atari-pixlar, TIA-objekt, flimmer, verklig animation, spelerfarenhet, 6502-cykler eller Stella.

## Grafisk risk
Efter att bäraren förstörts kan spelbilden innehålla **fem androider + nyckel + spelare + ett aktivt skott** på samma rasterhöjd. En frigjord logisk robotslot innebär inte att sex grafiska objekt är automatiskt lätta att visa. Prioritera att inget av nyckelns status/poäng går förlorat även när bilden skymmer den.

## Framåtblick
För framtida, separat godkänt ROM-test: låt android passera nyckel vid partiell/total överlappning, stå kvar i flera bildrutor, sedan gå därifrån; kontrollera att nyckelposition och +50 pickup inte påverkas. Testa även samtidig farlig kontakt och skott. En oberoende VERIFICATION ska kontrollera de faktiska TIA-resultaten.

## Källor
- Ursprunglig projektöverlämning i [Drive-mappen](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u), `02_MASTER_SPEC.md` och `03_DECISIONS.csv`.
- [Godkända K1/E1-regler](APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md), [visuell nyckel v0.13](KEY_AND_DOOR_VISUAL_TARGET_V013.md), [färgstudie v0.14](KEY_CONTRAST_RGB_REVIEW_V014.md).
- [Komplett v0.15-arkiv på Google Drive](https://drive.google.com/file/d/1u6FNeEnsNUNufpJtugXfGfm7irAEOQPm/view?usp=drivesdk), med händelsetest, skript, CSV och intern SHA-256-manifest.
- [Mobilrapport v0.15](https://drive.google.com/file/d/1Bx87knKFYTXCJXYbfDwE7OXAfKZe6Z40/view?usp=drivesdk) (2 sidor).

**Projektgräns:** endast *Let Me Out!*. Linear används inte. Inga ändringar i The Cabin eller I Love a Fish. **ROM DEVELOPMENT fortsatt pausad.**
