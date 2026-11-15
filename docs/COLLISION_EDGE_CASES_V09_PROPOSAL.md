# MAIN v0.9: två öppna kollisionsfall

**Status: FÖRSLAG / ej godkända spelbeslut.** Ingen ROM-kodning eller Stella-verifiering har utförts.

## K1 – nyckeln uppstår under spelaren
- Befintligt beslut: nyckeln blir synlig först när bärarens dödsanimation är färdig; +50 först vid faktisk upptagning.
- **Förslag:** när nyckeln dyker upp under en stillastående spelare kan den plockas upp i **nästa** logiska uppdatering utan extra rörelse. Inte samma uppdatering som framkomsten.
- Om spelaren lämnar området innan dess ligger nyckeln kvar; androider kan gå över den. Död samma uppdatering prioriteras framför ännu ej intjänad +50.

## E1 – dödlig kontakt samtidigt som utgången passeras
- Befintligt beslut: spelaren måste faktiskt passera en upplåst högra dörr; +100 och +15 per levande android vid lyckad utgång. Androider kan blockera dörren.
- **Förslag:** dödlig kontakt med överlevande android i passage prioriteras **före** lyckad rumsutgång. Ingen rumsbonus vid död. Redan intjänade poäng behålls.
- Befintlig skottprioritet kvarstår: androiden som förstörs samma uppdatering kan inte orsaka död av just sin kroppskontakt, men en annan överlevande android kan.

## Testgräns
15 specificerade acceptansfall i [Drive-paketet v0.9](https://drive.google.com/file/d/1Ztg48ihTanH58Z07OhH3Ge3-Rim2v3iC/view?usp=drivesdk), samtliga **NOT_RUN** och uppdelade på vad som redan är beslutat respektive föreslaget. Ingen faktisk ROM, TIA-timing eller Stella-mätning har utförts.

## Referenser och isolation
- [Huvudprojektets Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u)
- Ursprunglig 02_MASTER_SPEC.md och 03_DECISIONS.csv från huvudöverlämningen, samt v0.8:s öppna testfall T09/T17.
- Detta gäller **bara Let Me Out!**. Linear används inte. ROM DEVELOPMENT kräver separat uttryckligt godkännande.

**MAIN inväntar användarens besked om K1 och E1 innan de får märkas BESLUT.**
