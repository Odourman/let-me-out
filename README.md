# Let Me Out! (Atari 2600)

## MAIN VII – SLUTLIG PROJECT SOURCES-VERSION, 2026-11-17

**ENDA REKOMMENDERADE VERSION FÖR NY UPPLADDNING:** [LET_ME_OUT_PROJECT_SOURCES_MAIN_VII_FINAL_2026-11-17.zip](https://drive.google.com/file/d/1mLSqMZZx_j7g8ha6Mje4PyBsjiwZ6V6F/view), SHA256 `2c20ea7a5dbc9ae6809d2731fecfbc12acd6be279acb2d9255ba49d723fd792d`, 9 individuella källfiler, 35 spårbara källreferenser. Den nedladdade Drive-kopian har bytejämförts med originalet; ZIP CRC och alla 8 SHA256-filposter kontrollerades utan avvikelse.

Denna slutgranskning rättar en saknad direkt källregisterpost till G5M samt bevarar två kartauktoritetsnivåer: luftiga rum är godkänd riktning (LM-D04), men v0.19:s exakta `*_OPEN_01`-kartor är fortfarande förslag, medan `A01/B01/C02/D01` fortsatt är källvald äldre baseline. O1:s tidigare dokumenterade begränsade godkännande bevaras. Inga spelregler, originalmasker eller tidigare ROM-/Stella-evidens har ändrats.

**Tidigare paket är nu historiska, inte parallella Project Sources:** `LET_ME_OUT_PROJECT_SOURCES_2026-11-17.zip` (MAIN VI) och `LET_ME_OUT_PROJECT_SOURCES_MAIN_VII_CORRECTED_2026-11-17.zip` (första MAIN VII-rättelsen). Det som följer i äldre text beskriver sina respektive historiska revisionsögonblick. **G5:s formella användarbeslut återstår och G6/F12 är inte auktoriserat.**


Ett fristående Atari 2600-spel under design. Projektet är **inte** The Cabin och **inte** I Love a Fish.

## MAIN VII – kontrollerad migration och korrigerat Project Sources-paket

[MAIN VI → MAIN VII mottagningskvitto](docs/MAIN_VI_TO_MAIN_VII_RECEIPT_2026-11-17.md) · [Project Sources-rättelse och O1:s godkännandestatus](docs/project_sources/PROJECT_SOURCES_MAIN_VII_CORRIGENDUM_2026-11-17.md) · [Korrigerad niofilspaket-ZIP i officiell Drive](https://drive.google.com/file/d/1fxexRLz9fE8egW9bFnA1zA3x3j7f9AYj/view). **Original-MAIN VI-ZIP:en är historik, ladda inte båda.** G5-formal fortfarande öppet, G6/F12 ej auktoriserade, äldre PR #7 blockerat/draft.

## GRAPHICS - ren chattmigrering 2026-11-17

**MAIN V har avslutat sex GRAPHICS-kandidatstudier.** Alla är mottagna som dokumenterade grafiska underlag, men **ingen är slutgodkänd eller Stella-testad**. Ingen ny GRAPHICS-version/studie är auktoriserad. Nästa dedikerade GRAPHICS-chatt ska läsa aktuell MAIN-status och invänta en separat avgränsad designorder.

- [GRAPHICS -> ny chatt: fullständig, källstyrd handoff](docs/GRAPHICS_HANDOFF_TO_NEW_CHAT_2026-11-17.md)
- [GRAPHICS II: fristående startprompt](docs/GRAPHICS_NEW_CHAT_STARTPROMPT_2026-11-17.md)
- [Verifierbart migreringspaket i Google Drive](https://drive.google.com/file/d/1fEAW-oCkGWUq02yJ_klIFChQ5rSENHgT/view)

**Migreringen gäller enbart dokumentation och chattroll.** Den auktoriserar inte nya grafikmasker, ändringar i canon, ROM-kod, teknisk gate eller PR-merge. För aktuell ROM-status gäller alltid översta tillämpliga avsnitt i [CURRENT_PROJECT_STATE](docs/CURRENT_PROJECT_STATE_2026-11-15.md).

## MAIN IV → MAIN V – överlämning 2026-11-16

**MAIN IV har förberett projektöverlämningen till MAIN V.** [Fullständigt handoffpaket](docs/MAIN_IV_TO_MAIN_V_HANDOFF_2026-11-16.md) · [MAIN V:s färdiga startprompt](docs/MAIN_V_STARTPROMPT_2026-11-16.md) · [separata startprompter för ROM DEVELOPMENT och VERIFICATION](docs/MAIN_V_ROM_DEV_AND_VERIFICATION_STARTPROMPTS_2026-11-16.md). Alla tre finns även i [projektets Google Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). **Ingen ny kodauktorisation eller full R1–R4-acceptans följer av överlämningen.** ROM DEVELOPMENT och VERIFICATION ska arbeta i olika chattar, med faktisk verifiering oberoende av kodaren.

## MAIN IV – integrerat forskningsprov R1ba, 2026-11-16

[Reproducerbar R1ba-GitHub Actions-körning](https://github.com/Odourman/let-me-out/actions/runs/43884511590) fick **600/600 lokala Stella-PASS** med **sex hela originalandroider, tre sammankopplade runtime-X/Y-uppställningar, bruna speglade PF-sidoväggar, gul P0 och en statisk M0-symbol**. [MAIN IV:s uppdaterade projektcheckpoint](docs/MAIN_IV_CHECKPOINT_2026-11-16.md), [fullständigt forskningsbevis](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view?usp=drivesdk) och [R3-dörrkällgranskning](docs/MAIN_IV_R3_RIGHT_DOOR_SOURCE_AUDIT_2026-11-16.md). **Inte full R1/R2/R3/R4 eller oberoende VERIFICATION.** Individuellt fria X/Y och R2-nyckel/R3-högerdörr är fortfarande olösta.

## MAIN IV – statusuppdatering 2026-11-16

Den nya [MAIN IV-checkpointen](docs/MAIN_IV_CHECKPOINT_2026-11-16.md) samlar aktuell auktorisation, kod-/evidensläget och nästa steg från GitHub och Google Drive. Nya R1aq–R1az-forskningsprov har uppnått pixelkorrekta **sex originalsilhuetter**, avgränsade förkompilerade X-lägen och tre små-NPC Y-profiler växlande i samma NTSC-ROM. **Detta är positiva lokala diagnostikdelprov, inte godkänd full R1 eller R1–R4 och inte oberoende VERIFICATION.** R1ax har nu klarat **600/600** lokal Stella-pixelkontroll med **två speglade bruna sidoväggar**; det är fortfarande inte R3:s asymmetriska högerdörr eller full R1. PR #7 är draft och fullspelsutveckling saknar tillstånd.

## Status – 2026-11-15

- **Design:** grundregler finns dokumenterade; fortsatt granskning pågår.
- **Förstudier:** labyrinter v0.1–v0.2, AI/rörelse v0.3, v0.7–v0.8, grafikrisk v0.4–v0.5, svårighetskurva v0.6, kollisionsbeslut v0.9, kartjämförelse v0.10, godkänd planerad C02-bas/spawngranskning v0.11 **högerdörrstudie v0.12**, visuellt mål v0.13, nyckelkontrast v0.14 och nyckelöverlappning v0.15, följt av [åtta avslutade MAIN-studier v0.16](docs/MAIN_EIGHT_STEPS_V016_2026-11-15.md).
- **ROM-kodning:** **endast diagnostik v0.18 uttryckligen auktoriserad 2026-11-15** för NTSC R1–R4, 16 KB F6 om motiverat; **inte fullspelet**. **Körbar DASM-byggd NTSC-diagnostik levererad i draft PR #7**, men **grafiktestet har blockerande FAIL** och den är inte oberoende verifierad. [Auktorisation](docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md).
- **Nya godkända spelregler:** K1 (nyckel kan tas från och med uppdateringen efter att den uppstått under stillastående spelare) och E1 (dödlig androidkontakt avgörs före samtidigt utträde). [Beslutslogg](docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md).
- **Planerat fyrarum-set:** A01/B01/**C02**/D01. C02 är **godkänd som planerad karta C** av användaren; C01 behålls som historisk jämförelse. [Exakt kartdata i GitHub](design/PLANERADE_RUMSKARTOR_V011.json) och [beslutslogg/spawngranskning](docs/APPROVED_MAP_C02_AND_SPAWN_AUDIT_V011.md).
- **Godkänt visuellt mål V2B/GULD:** orange dörr med svart nyckelhål som försvinner vid upplåsning; guldgul nyckel med runt genomgående hål, kort skaft och tänder. [Designunderlag v0.13](docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md). Exakt pixelmask och TIA-grafik är fortfarande öppna.
- **Nytt v0.14-underlag:** [offline RGB-kontrastjämförelse](docs/KEY_CONTRAST_RGB_REVIEW_V014.md) antyder att en något djupare guldton för nyckeln passar bättre än nästan spelargult. Exakt färgkod är **inte** godkänd eller TIA-verifierad.
- **Ej godkända testkandidater:** P2 (patrull), J2 (jakt), C-1 (svårighetskurva), S1 (alternativt android-startfilter), K11/K09-nyckelsilhuetter. Varken verklig pixelgeometri, timing eller spelbalans är verifierade. **O1 (android kan tillfälligt skymma nyckeln utan att den flyttas)** är nu **godkänt** av användaren. Ett mindre, tillfälligt flimmer i spelet är acceptabelt utan att någon mätbar tolerans är fastställd. [Beslutslogg och kommande 10 steg](docs/MAIN_STATUS_NEXT_10_2026-11-15.md).

## MAIN v0.18 – ROM DEVELOPMENT:s första leverans (BLOCKERAD)

- [Draft PR #7](https://github.com/Odourman/let-me-out/pull/7) innehåller NTSC/F6 ROM och autentiska Stella-skärmbilder; [MAIN:s mottagningsgranskning](docs/MAIN_REVIEW_ROM_V018_STELLA_2026-11-15.md) noterar fem FAIL, framför allt oläsliga androidsilhuetter. DASM-bygget är byteidentiskt i utvecklarens CI.
- [Oberoende VERIFICATION uppdrag #8](https://github.com/Odourman/let-me-out/issues/8) inväntar separat kontroll. **Ingen merge, inget fullspel och ingen ny utvecklingsfas**.

## MAIN v0.16 – genomförd designresearch

De första åtta momenten i användarens tio-stegsplan är nu [genomförda och dokumenterade](docs/MAIN_EIGHT_STEPS_V016_2026-11-15.md): nyckelskymning, rasterstress, högra dörren, nyckelpixelgrafik, AI, startpositioner, svårighetskurva och HUD. Nästa punkter är **9 ljud/presentation** och **10 framtida ROM-grind**. Dessa v0.16-tester var offline. **Senare har endast den avgränsade diagnostiken v0.18 kodats**, se status ovan.

## Presentation

- **Beslutat:** Ingen separat startskärm.
- **Beslutat:** Berzerk-inspirerad Game Over-effekt i labyrinten med färgväxling och blinkande slutpoäng. **Endast konsolens GAME RESET/RESET startar om. Fire gör ingenting efter Game Over.** Vid omstart: 0 poäng och 3 liv. Exakta effekter är inte ROM-verifierade. [Game Over- och RESET-beslut](docs/GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md).

## Ljuddesign v0.17 – fyra korta effekter

- **Redan beslutat i ursprunglig Master Spec:** ljud vid nyckelupptagning (+50), precis en gång.
- **Användarens föreslagna riktning:** stigande elektroniskt tjut när första verkligt avfyrade skottet gör androiderna aggressiva; androidförstörelseljud och kort skottljud.
- **MAIN:s testrekommendation:** fyra ljud totalt (jaktlarm, skott, androidförstörelse, nyckelupptagning). Ingen bakgrundsmusik eller kontinuerligt jaktljud. Tekniken använder TIA:s två ljudkanaler.
- **Fortfarande preliminärt:** exakta tonhöjder, längder, ljudprioritering, slutlig ljudpalett och samtidiga effekter. **Inget ROM-ljud byggt.**
- [Ljudspecifikation v0.17](https://github.com/Odourman/let-me-out/blob/main/docs/SOUND_DESIGN_V017_2026-11-15.md) och [identiskt originalunderlag i Drive](https://drive.google.com/file/d/1bm19imkHic0zPSvDk-MGJ5842VfQtuWS/view).

## Teknisk ROM-grind v0.18 – kodad diagnostik, ej godkänd

- Avgränsad diagnostik omfattar **R1–R4**: rastervärstafall 6 androider+spelare+skott, 5 androider+spelare+nyckel+skott, asymmetrisk högerdörr och styrd rasterstress.
- **16 ROM-testfall** är definierade. Utvecklarens senare utfall: 5 PASS / 5 FAIL / 5 INCONCLUSIVE / 1 NOT_RUN. Fristående [VERIFICATION](docs/ROM_GATE_V018_VERIFICATION.md) krävs fortfarande.
- [Uppdragets scope](docs/ROM_GATE_V018_SCOPE.md) · [acceptanskriterier](docs/ROM_GATE_V018_ACCEPTANCE.md) · [testmatris](planning/ROM_GATE_V018_TEST_MATRIX.csv) · [risker och stopp](docs/ROM_GATE_V018_BLOCKERS.md).
- [Ladda ned hela grinden från Drive](https://drive.google.com/file/d/1FzQJWYYMzO0T18wxil079WxqmdboFPiw/view?usp=drivesdk).
- **Kodning är nu tillåten endast för diagnostik v0.18** enligt [separat uttrycklig auktorisation](https://github.com/Odourman/let-me-out/issues/6). Fullspel och alla senare implementeringssteg är fortfarande spärrade.

## Spelidé

Spelaren ska hitta en nyckel som döljs hos en av sex androider. Första *avfyrade* skottet gör de tidigare ofarliga androiderna fientliga. Efter att nyckeln plockats upp måste spelaren ta sig ut genom dörren på höger sida. Fler överlevande androider ger en poängbonus vid lyckad utgång.

Fastslagna grundvärden: sex androider (fyra stora, två små), fyra speglade rum, tre startliv, poäng **-25 per förstörd android / +50 nyckel / +100 verklig utgång / +15 per överlevande android**, extraliv vid 500, 1500, 2500 och därefter per ytterligare 1000 poäng.

## Underlag

- [Master specification och beslutsregister i projektets Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).
- Google Drive innehåller 18 versionerade projektarkiv (till v0.18), en separat kopia av den valda kartdatan, mobilrapporter och en besluts-/färdplanfil som motsvarar GitHubs statusrapport. GitHub innehåller egna textbaserade beslut, arbetsunderlag och [öppna designärenden](https://github.com/Odourman/let-me-out/issues), men inga referens-ROM:er eller tredjepartsfiler. Linear används inte för detta spel.

## Arbetsregler

1. MAIN koordinerar och håller isär beslut, förslag och verifierad implementation.
2. ROM DEVELOPMENT ska få ett separat, uttryckligt koduppdrag innan implementation inleds.
3. VERIFICATION ska utföra en oberoende kontroll av ett eventuellt framtida ROM-test.
4. Uppdatera inte The Cabin eller I Love a Fish som del av detta projekt.
5. Inga Berzerk-ROM:er, kopior av kommersiell tredjepartskod eller osäkra licenstillgångar ska publiceras här.

*Sammanställt för Let Me Out! MAIN, 2026-11-15.*
