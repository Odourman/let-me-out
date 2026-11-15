# Let Me Out! (Atari 2600)

Ett fristående Atari 2600-spel under design. Projektet är **inte** The Cabin och **inte** I Love a Fish.

## Status – 2026-11-15

- **Design:** grundregler finns dokumenterade; fortsatt granskning pågår.
- **Förstudier:** labyrinter v0.1, AI/rörelse v0.2–v0.8 och grafik-riskanalys v0.4–v0.5.
- **ROM-kodning:** **pausad**. Ingen prototyp, binär eller emulatorverifierad spelimplementation finns här.
- **Designförslag är inte automatiskt beslut:** P2 (patrull), J2 (jakt), C02 (rum C) och C-1 (svårighetskurva) är testkandidater.

## Spelidé

Spelaren ska hitta en nyckel som döljs hos en av sex androider. Första *avfyrade* skottet gör de tidigare ofarliga androiderna fientliga. Efter att nyckeln plockats upp måste spelaren ta sig ut genom dörren på höger sida. Fler överlevande androider ger en poängbonus vid lyckad utgång.

Fastslagna grundvärden: sex androider (fyra stora, två små), fyra speglade rum, tre startliv, poäng **-25 per förstörd android / +50 nyckel / +100 verklig utgång / +15 per överlevande android**, extraliv vid 500, 1500, 2500 och därefter per ytterligare 1000 poäng.

## Underlag

- [Master specification och beslutsregister i projektets Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).
- GitHub-förrådet innehåller endast egna textbaserade projektbeskrivningar och arbetsunderlag; referens-ROM:er eller tredjepartsfiler ingår inte.

## Arbetsregler

1. MAIN koordinerar och håller isär beslut, förslag och verifierad implementation.
2. ROM DEVELOPMENT ska få ett separat, uttryckligt koduppdrag innan implementation inleds.
3. VERIFICATION ska utföra en oberoende kontroll av ett eventuellt framtida ROM-test.
4. Uppdatera inte The Cabin eller I Love a Fish som del av detta projekt.
5. Inga Berzerk-ROM:er, kopior av kommersiell tredjepartskod eller osäkra licenstillgångar ska publiceras här.

*Sammanställt för Let Me Out! MAIN, 2026-11-15.*
