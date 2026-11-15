# Let Me Out! – aktuellt projektläge (MAIN)

**Datum:** 2026-11-15  
**Omfattning:** endast Atari 2600-spelet *Let Me Out!*.

## Beslutsstatus

- 57 beslut registrerades i den ursprungliga överlämningen. Beslutsregistret i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip` är underlag för beslutens exakta status och historik.
- Senare studier v0.1–v0.16 är i huvudsak **rådgivande förslag**. Undantag: K1/E1 (kollisioner), C02 (planerad kartlayout), V2B/GULD (visuell riktning) och nu **O1 (android får tillfälligt skymma nyckeln)** har godkänts av användaren. En mindre mängd flimmer i spelet har accepterats kvalitativt, utan numerisk tolerans. Se [besluts- och planrapporten](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md).
- **NYTT ANVÄNDARBESLUT 2026-11-15:** Endast **ROM DEVELOPMENT-diagnostik v0.18 med NTSC**, R1–R4, är **uttryckligen kodauktoriserad**. F6 16 KB får användas om tekniskt motiverat. [Auktorisation](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [Issue #6](https://github.com/Odourman/let-me-out/issues/6). **Ingen fullspelsutveckling, PAL-utbyggnad eller senare ROM-steg är auktoriserade. Ingen körbar ROM eller oberoende verifiering har ännu rapporterats.**

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

## Senaste arbetsstatus v0.16 – åtta analyser fullföljda

- [Samlad 8-stegsstudie i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_EIGHT_STEPS_V016_2026-11-15.md), [37+1 filer i Drive ZIP](https://drive.google.com/file/d/1YrXJtgqvY9bjaSKKxoyb7hvs7ye5msx-/view?usp=drivesdk), [mobil-PDF](https://drive.google.com/file/d/1RbjgcJs_oTlYIqeHF3tZk6PZawRIbiZu/view?usp=drivesdk).
- Avgränsat innehåll: lång nyckelskymning (160 modellförlopp), rastervärstafall (8 logiska enheter), högerdörr, nyckelmasker, P2/J2-AI (480 modellförlopp), S0/S1 (64 045 kombinationer), C-1/C-soft-kurvor och score/HUD.
- **Arbetsrekommendationer, inte nya canon-beslut:** P2/J2 med 1/8, K11 med K09 som reserv, S0, C-1 och HUD-A. De 22 framtida tekniska fallen är **NOT_RUN_IN_ROM**.
- **Återstår i 10-stegsplanen:** steg 9 – presentation/ljud; steg 10 – integrerad teknikgrind. Ingen ROM-kodstart har auktoriserats.

## Senaste användarbeslut: O1 och viss flimmertolerans

- [Beslut, senaste tio steg och kommande tio steg i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_STATUS_NEXT_10_2026-11-15.md), [identiskt dokument i Drive](https://drive.google.com/file/d/1N4D5GH-hhBsbQPIK82v2KF5IdMgq33HJ/view).
- **O1 godkänt:** Androidens figur får skymma nyckeln, men position/status/poäng påverkas inte. Nyckeln visas på samma ställe när roboten flyttat sig.
- **Lite flimmer accepterat:** inte tillstånd för långvarig oläslighet eller skymd spelarfara. Bedöms i framtida ROM och oberoende VERIFICATION.
- Ingen ytterligare ROM-/6502-auktorisation har givits.

## Presentation – nytt användarbeslut och öppet designförslag

- **BESLUT:** Ingen separat startskärm i Let Me Out! (användarens direktinstruktion 2026-11-15). Spelstart/omstart sker utan fristående titelskärm; exakt kontroll- och startflöde återstår att specificera.
- **BESLUT GAME OVER/RESET:** Berzerk-inspirerad slutpresentation i labyrinten med färgväxling och långsamt blinkande slutpoäng. **Endast Atari-konsolens GAME RESET/RESET startar om** efter GAME OVER; Fire får inte starta om och är inaktivt efter sista livet. RESET startar nytt spel med 0 poäng och 3 liv. Ingen separat start- eller Game Over-skärm. Exakta färger och blinkintervall är tekniskt öppna; original-Berzerks Game Over-inversion är inte styrkt av manualen. [Beslutslogg](https://github.com/Odourman/let-me-out/blob/main/docs/GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md), [samma på Drive](https://drive.google.com/file/d/1r417oy8bAyVBj-bfeeC58QjynEwzHevv/view).
- Dessa effekter får inte förväxlas med användarens accepterade **begränsade flimmer under spel**. Ingen ROM-implementation har godkänts.

## Viktigaste öppna val

1. **C02 valt som planerad karta C** (beslut; inte speltestad): [GitHub-beslut och spawngranskning v0.11](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_MAP_C02_AND_SPAWN_AUDIT_V011.md), [Drive-paket](https://drive.google.com/file/d/1WbnLfcSKM-bqmVIz5jCJ0ga0sUzPU0UK/view?usp=drivesdk), [avslutat Issue #2](https://github.com/Odourman/let-me-out/issues/2). A01/B01/D01 ej ändrade. Jämför bara A/B/D med annat utförande om senare speltest kräver det.
2. **Spawnspelbalans ännu öppen:** samtliga 64 045 möjliga sexstartval ur nuvarande fyra pools klarade offline 2×2-kontroll. S0 oförändrad bas, S1 (minst 12 fyrvägssteg från spelarstart) **endast testkandidat**.
3. Detaljer för patrullering, jakt och svårighet (P2/J2/C-1), tills vidare testkandidater.
4. **VISUELLT MÅL BESLUTAT v0.13:** guldgul nyckel med runt genomgående hål och kort tandat skaft; smalt orange dörrstreck med **svart nyckelhål**. Hela dörren och symbolen försvinner vid upplåsning. [Beslutsunderlag](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md) och [avslutat designärende #4](https://github.com/Odourman/let-me-out/issues/4). **Exakt pixelmask och TIA-teknik överifierade.** [Öppet framtida testärende #5](https://github.com/Odourman/let-me-out/issues/5).
5. **Nyckelns kontraststudie v0.14, inte beslut om färgkod:** tre hypotetiska RGB-toner jämförda, preliminärt föredras en något djupare guldton framför nästan spelargult; varken K11/K09 eller PAL/NTSC-kod låst. [Designstudie i GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_CONTRAST_RGB_REVIEW_V014.md), [ZIP i Drive](https://drive.google.com/file/d/17I6nUhYTCSRIQ35fMvILE1pmVIIDh8SA/view?usp=drivesdk). 9 matematiska RGB-kombinationer och två offline-maskkontroller, **ingen Atari-körning**. [Framtida verifieringsärende #5](https://github.com/Odourman/let-me-out/issues/5).
6. **Nyckelöverlappning v0.15 – O1 NU GODKÄND:** Android får tillfälligt skymma statisk nyckel, men får aldrig flytta, påverka eller ta den. Nyckeln återkommer synligt på oförändrad position när skymningen upphör. Ingen avsiktlig blinkväxling. Mindre tillfälligt flimmer i spelet är acceptabelt, men exakt teknisk gräns är inte bestämd. 20/20 offline-händelsetester klarade. **Ingen TIA-/ROM-verifiering.** [Studie](https://github.com/Odourman/let-me-out/blob/main/docs/KEY_OCCLUSION_LOGIC_V015.md), [Drive ZIP](https://drive.google.com/file/d/1u6FNeEnsNUNufpJtugXfGfm7irAEOQPm/view?usp=drivesdk).
7. Grafikarkitektur och tolerans för flimmer – först efter uttryckligt godkänd ROM-prototyp.

## MAIN v0.18 – uppdragsgrind nu separat AUKTORISERAD för diagnostik

- **Design/analys steg 10 genomfört.** Avgränsat framtida ROM-test omfattar endast **R1** (sex androider, spelare, testsymbolskott), **R2** (fem androider, nyckel, spelare, skott), **R3** (endast högerdörr, orange och nyckelhål), **R4** (förprogrammerad raster-/nyckelskymningsstress).
- **16 definierade testfall**, alla `NOT_RUN_IN_ROM`, med egentliga acceptanskriterier, stoppregler och **oberoende VERIFICATION**. **ROM-kodning för exakt detta diagnostikscope är nu auktoriserad men ingen faktisk ROM, Stella-verifiering eller byggning har rapporterats.**
- [Scope](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_SCOPE.md) · [Acceptans](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) · [Testmatris](https://github.com/Odourman/let-me-out/blob/main/planning/ROM_GATE_V018_TEST_MATRIX.csv) · [Oberoende verifiering](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_VERIFICATION.md).
- [Gemensam ZIP i Drive](https://drive.google.com/file/d/1FzQJWYYMzO0T18wxil079WxqmdboFPiw/view?usp=drivesdk) · [mobilrapport](https://drive.google.com/file/d/1gVhSzEX3UnD1UTm-nl4pwdwrtrRFFGm4/view?usp=drivesdk) · [Issue #6: separat uttryckligt kodgodkännande givet](https://github.com/Odourman/let-me-out/issues/6).
- NTSC och 16KB F6 är **tekniska förslag**, inte nya bindande beslut. **Godkänd diagnostik ska aldrig automatiskt öppna ett senare fullspelsuppdrag.**

## Ljuddesign v0.17 – fyra korta effekter

- **Redan beslutat i ursprunglig Master Spec:** ljud vid nyckelupptagning (+50), precis en gång.
- **Användarens föreslagna riktning:** stigande elektroniskt tjut när första verkligt avfyrade skottet gör androiderna aggressiva; androidförstörelseljud och kort skottljud.
- **MAIN:s testrekommendation:** fyra ljud totalt (jaktlarm, skott, androidförstörelse, nyckelupptagning). Ingen bakgrundsmusik eller kontinuerligt jaktljud. Tekniken använder TIA:s två ljudkanaler.
- **Fortfarande preliminärt:** exakta tonhöjder, längder, ljudprioritering, slutlig ljudpalett och samtidiga effekter. **Inget ROM-ljud byggt.**
- [Ljudspecifikation v0.17](https://github.com/Odourman/let-me-out/blob/main/docs/SOUND_DESIGN_V017_2026-11-15.md) och [identiskt originalunderlag i Drive](https://drive.google.com/file/d/1bm19imkHic0zPSvDk-MGJ5842VfQtuWS/view).

## Källor och isolation

- [Let Me Out! i Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) – arton versionerade ZIP-arkiv från huvudöverlämningen till den färdiga ROM-grinden v0.18, inklusive manifest, samt status-/färdplanfil (O1-beslut), Game Over-/RESET-beslut, kartdata JSON och mobilrapporter/RGB-skisser.
- [GitHub-förrådet](https://github.com/Odourman/let-me-out) – egna projekttexter, inga tredjeparts-ROM:er.
- Ändra aldrig **The Cabin** eller **I Love a Fish** som del av detta projekt.
- **Linear används inte för Let Me Out!** (användarbeslut 2026-11-15). Arbetsuppgifter hanteras vid behov i GitHub Issues.

**Auktoritet:** Senare direkta användarbeslut > registrerade spelbeslut > experimentella modellförslag > tredjepartsresearch.  
**Detta är en statusöversikt**, inte ersättning för originalbeslutsregistret.