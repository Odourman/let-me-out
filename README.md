# Let Me Out! (Atari 2600)

Ett fristående Atari 2600-spel under design. Projektet är **inte** The Cabin och **inte** I Love a Fish.

## Status – 2026-11-15

- **Design:** grundregler finns dokumenterade; fortsatt granskning pågår.
- **Förstudier:** labyrinter v0.1–v0.2, AI/rörelse v0.3, v0.7–v0.8, grafikrisk v0.4–v0.5, svårighetskurva v0.6, kollisionsbeslut v0.9, kartjämförelse v0.10, godkänd planerad C02-bas/spawngranskning v0.11 och **högerdörrstudie v0.12**.
- **ROM-kodning:** **pausad**. Ingen prototyp, binär eller emulatorverifierad spelimplementation finns här.
- **Nya godkända spelregler:** K1 (nyckel kan tas från och med uppdateringen efter att den uppstått under stillastående spelare) och E1 (dödlig androidkontakt avgörs före samtidigt utträde). [Beslutslogg](docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md).
- **Planerat fyrarum-set:** A01/B01/**C02**/D01. C02 är **godkänd som planerad karta C** av användaren; C01 behålls som historisk jämförelse. [Exakt kartdata i GitHub](design/PLANERADE_RUMSKARTOR_V011.json) och [beslutslogg/spawngranskning](docs/APPROVED_MAP_C02_AND_SPAWN_AUDIT_V011.md).
- **Godkänt visuellt mål V2B/GULD:** orange dörr med svart nyckelhål som försvinner vid upplåsning; guldgul nyckel med runt genomgående hål, kort skaft och tänder. [Designunderlag v0.13](docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md). Exakt pixelmask och TIA-grafik är fortfarande öppna.
- **Ej godkända testkandidater:** P2 (patrull), J2 (jakt), C-1 (svårighetskurva), S1 (alternativt android-startfilter), K11/K09-nyckelsilhuetter. Varken verklig pixelgeometri, timing eller spelbalans är verifierade.

## Spelidé

Spelaren ska hitta en nyckel som döljs hos en av sex androider. Första *avfyrade* skottet gör de tidigare ofarliga androiderna fientliga. Efter att nyckeln plockats upp måste spelaren ta sig ut genom dörren på höger sida. Fler överlevande androider ger en poängbonus vid lyckad utgång.

Fastslagna grundvärden: sex androider (fyra stora, två små), fyra speglade rum, tre startliv, poäng **-25 per förstörd android / +50 nyckel / +100 verklig utgång / +15 per överlevande android**, extraliv vid 500, 1500, 2500 och därefter per ytterligare 1000 poäng.

## Underlag

- [Master specification och beslutsregister i projektets Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).
- Google Drive innehåller 14 versionerade projektarkiv (till v0.13) samt en separat kopia av den valda kartdatan och en mobilrapport. GitHub innehåller egna textbaserade beslut, arbetsunderlag och [öppna designärenden](https://github.com/Odourman/let-me-out/issues), men inga referens-ROM:er eller tredjepartsfiler. Linear används inte för detta spel.

## Arbetsregler

1. MAIN koordinerar och håller isär beslut, förslag och verifierad implementation.
2. ROM DEVELOPMENT ska få ett separat, uttryckligt koduppdrag innan implementation inleds.
3. VERIFICATION ska utföra en oberoende kontroll av ett eventuellt framtida ROM-test.
4. Uppdatera inte The Cabin eller I Love a Fish som del av detta projekt.
5. Inga Berzerk-ROM:er, kopior av kommersiell tredjepartskod eller osäkra licenstillgångar ska publiceras här.

*Sammanställt för Let Me Out! MAIN, 2026-11-15.*
