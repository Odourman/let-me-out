# Let Me Out! (Atari 2600)

Ett fristående Atari 2600-spel under design. Projektet är **inte** The Cabin och **inte** I Love a Fish.

## Status – 2026-11-15

- **Design:** grundregler finns dokumenterade; fortsatt granskning pågår.
- **Förstudier:** labyrinter v0.1–v0.2, AI/rörelse v0.3, v0.7–v0.8, grafikrisk v0.4–v0.5, svårighetskurva v0.6 samt kollisionsbeslut v0.9 och kartjämförelse v0.10.
- **ROM-kodning:** **pausad**. Ingen prototyp, binär eller emulatorverifierad spelimplementation finns här.
- **Nya godkända spelregler:** K1 (nyckel kan tas från och med uppdateringen efter att den uppstått under stillastående spelare) och E1 (dödlig androidkontakt avgörs före samtidigt utträde). [Beslutslogg](docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md).
- **Designförslag är inte automatiskt beslut:** P2 (patrull), J2 (jakt), C02 (rum C) och C-1 (svårighetskurva) är fortfarande testkandidater. [Senaste kartjämförelse](docs/MAP_C01_VS_C02_REVIEW_V010.md).

## Spelidé

Spelaren ska hitta en nyckel som döljs hos en av sex androider. Första *avfyrade* skottet gör de tidigare ofarliga androiderna fientliga. Efter att nyckeln plockats upp måste spelaren ta sig ut genom dörren på höger sida. Fler överlevande androider ger en poängbonus vid lyckad utgång.

Fastslagna grundvärden: sex androider (fyra stora, två små), fyra speglade rum, tre startliv, poäng **-25 per förstörd android / +50 nyckel / +100 verklig utgång / +15 per överlevande android**, extraliv vid 500, 1500, 2500 och därefter per ytterligare 1000 poäng.

## Underlag

- [Master specification och beslutsregister i projektets Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).
- Google Drive innehåller 11 versionerade projektarkiv (till v0.10). GitHub innehåller egna textbaserade beslut, arbetsunderlag och [öppna designärenden](https://github.com/Odourman/let-me-out/issues), men inga referens-ROM:er eller tredjepartsfiler. Linear används inte för detta spel.

## Arbetsregler

1. MAIN koordinerar och håller isär beslut, förslag och verifierad implementation.
2. ROM DEVELOPMENT ska få ett separat, uttryckligt koduppdrag innan implementation inleds.
3. VERIFICATION ska utföra en oberoende kontroll av ett eventuellt framtida ROM-test.
4. Uppdatera inte The Cabin eller I Love a Fish som del av detta projekt.
5. Inga Berzerk-ROM:er, kopior av kommersiell tredjepartskod eller osäkra licenstillgångar ska publiceras här.

*Sammanställt för Let Me Out! MAIN, 2026-11-15.*
