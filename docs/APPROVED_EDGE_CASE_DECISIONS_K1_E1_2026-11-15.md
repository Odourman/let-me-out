# MAIN-beslut – K1 och E1

**Projekt:** Atari 2600 – Let Me Out! (aldrig The Cabin eller I Love a Fish)
**Datum:** 2026-11-15
**Beslutsunderlag:** [MAIN v0.9 – rekommendationerna](https://github.com/Odourman/let-me-out/blob/main/docs/COLLISION_EDGE_CASES_V09_PROPOSAL.md), [v0.9-arkiv i Drive](https://drive.google.com/file/d/1Ztg48ihTanH58Z07OhH3Ge3-Rim2v3iC/view?usp=drivesdk)
**Auktorisation:** I direkt svar på MAIN:s fråga "Godkänner du båda reglerna?" svarade användaren "Ok, fortsätt". MAIN tolkar detta som bifall till *båda just presenterade reglerna*, inte som en generell implementationstillåtelse.

## BESLUT K1 – Nyckel framträder under stillastående spelare
Nyckeln framträder först efter att nyckelbärarens dödsanimation avslutats. Om spelaren står på dess position får nyckeln plockas upp automatiskt **tidigast nästa logiska uppdatering**, utan att spelaren måste flytta sig. +50 utdelas **exakt en gång** vid upptagning, inte i samma uppdatering som nyckeln skapas. Dödlig kontakt under en uppdatering hindrar en ännu inte intjänad upptagningsbonus.

## BESLUT E1 – Samtidig androidkontakt och utgång
Om spelaren under faktisk passage genom den upplåsta högra dörröppningen i samma logiska uppdatering får dödlig kroppskontakt med en *överlevande* jagande android, avgörs dödlig kontakt **före** rumsutgång. Liv förloras; ingen +100 och ingen +15/levande bonus utdelas. Redan intjänade poäng behålls.

**Redan beslutad träffprioritet består:** ett skott som förstör en android samma uppdatering tar bort faran från just den androidens kroppskollision. Andra överlevande androider kan fortfarande vara farliga. Rums- och överlevnadsbonus utdelas bara en gång vid faktiskt lyckad utgång.

## FÖLJDBESTÄMMELSE – logisk händelseprioritet
1. Godkänd första avfyrning aktiverar omedelbart jakt.
2. Skottträff förstör android innan kroppskollision med *den* androiden avgörs.
3. Dödlig kontakt med kvarvarande levande androider avgörs.
4. Vid överlevnad: upptagning av nyckel som fanns redan före uppdateringen och relevant dörrkontakt.
5. Vid överlevnad och *verklig* utpassage: rumsbonus exakt en gång.
6. Nyckel som skapas i denna uppdatering får inte tas före nästa logiska uppdatering.

Detta specificerar logiska regler, **inte** en validerad 6502/TIA-/Stella-exekveringsordning.

## Status
- **DESIGNBESLUT: godkänt.**
- **Implementerat i Atari ROM: nej.**
- **Verifierat i Stella: nej.**
- **ROM-development: fortfarande uttryckligen pausad** tills användaren separat auktoriserar kodstart.
- Den ursprungliga 57-posters beslutstabellen är historisk och ändras inte i efterhand. Detta är ett tillägg med senare beslut.
