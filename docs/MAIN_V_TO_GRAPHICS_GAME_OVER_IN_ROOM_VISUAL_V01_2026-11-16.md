# LET ME OUT! – MAIN V till GRAPHICS
## GAME OVER – IN-ROOM VISUAL CONCEPT v0.1

**Datum:** 2026-11-16. **Status:** NYTT SEPARAT OCH AVGRÄNSAT **GRAPHICS DESIGN**-uppdrag, **inte** kod- eller ROM-implementation. Avsluta med en samlad grafikleverans.

## 1. Källkontroll och redan bindande beslut

Du är dedikerad GRAPHICS, inte MAIN, ROM DEVELOPMENT eller VERIFICATION. Läs de faktiska källorna:
- [Direkt användarbeslut: GAME OVER + endast konsol-RESET](GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md). **Senare specifikt beslut väger över äldre generella 'obeslutat titelskärm' i historisk Master Spec.**
- [Ursprunglig 57-beslutshandoff](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), särskilt `02_MASTER_SPEC.md` om 3 liv, game over, poäng och 6 NPC, samt `03_DECISIONS.csv` för ursprungliga regler.
- [GRAPHICS rollinstruktion](MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md).
- [Aktuellt projekttillstånd](CURRENT_PROJECT_STATE_2026-11-15.md), läs den senaste översta sektionen och särskilt vad som supersederats.
- [MAIN:s just mottagna dödsanimationsstudie](MAIN_V_COMMON_ANDROID_DEATH_ANIMATION_V01_RECEIPT_2026-11-16.md), ingen death-Frame-implementation beställd.
- [Ursprunglig planerad 40×22-C02-kartbas](../design/PLANERADE_RUMSKARTOR_V011.json) och [MAIN v0.19 öppna alternativa rum](MAIN_OPEN_ROOMS_V019_2026-11-15.md). **Använd C02 som illustrativ bas för den här studien, ingen cutover till `C_OPEN`**.
- [Visuellt mål för orange högerport, guldnyckel, brun vägg](KEY_AND_DOOR_VISUAL_TARGET_V013.md); [färgkontrastkandidater](KEY_CONTRAST_RGB_REVIEW_V014.md).

**Låst spel- och visuell riktning:**
1. **Ingen separat startskärm** inför spelstart.
2. GAME OVER efter tredje/sista förlorade livet: en **enkel, Berzerk-inspirerad slutpresentation I DEN BEFINTLIGA SPELPLANEN**, inte ett helt nytt fullskärmsgränssnitt. Ett tänkt gammalt spelplansfoto används som bas; visa inte ny design för rum/nivå.
3. **Avvikande eller växlande kontrastfärger** och **blinkande SLUTPOÄNG** är godkänd riktning, men *exakta* färger, antal färgtillstånd, blinkfrekvens, text, siffrornas maxantal, placering och timing är **öppna designfrågor**.
4. Efter game over **endast konsolens GAME RESET / RESET** startar om spelet med tre startliv och noll poäng. **FIRE startar inte om**, skjuter inte och spelar ingen gameplayroll i detta läge. Detta är **logik**, som du bara ska redovisa som **icke-kodad storyboardetikett** – du får inte implementera den.
5. Ingen fastställd GAME OVER-font, ljud, poängformat/scoreboard-placering, permanent highscorelagring eller ny fiende-/spelare-spawn vid slutbilden.
6. Visuell canon fortsätter gälla: **vita människoliknande androidoriginal**, gul spelare med hatt och vapen som *ännu ej låst* pixelmask (V03_B får användas enbart märkt som ILLUSTRATIVE COMPARISON), bruna väggar, mörk normalbakgrund, stängd vänsterkant och högerdörr endast i C02. Ingen kopiering av Berzerks ROM/asset/typsnitt. Använd Berzerk som historisk inspirationsrikning, inte påstående om exakta originaleffekter.

## 2. ENDA nya konstnärliga frågan

Hur ska **GAME OVER uppfattas omedelbart, med tydlig blinkande poäng, utan att spelaren tror att ett nytt rum, ett nyckeltapp eller en vanlig gameplay-paus har inträffat – samtidigt som samma spelplan visuellt behålls**?

Skapa **exakt två** meningsfullt olika fristående, OFFLINE-grafikkoncept, ingen tredje v0.1-kompromiss utan ny order:

**G1 – lågmäld spelplans-palette shift:** Behåll samma vägggeometri, snapshotfigurernas former/positioner och poängexempel i varje frame; prova en läsbar, kontrasterande *helhetsväxling* mellan två högkontrastpalett-tillstånd inuti samma plan. Slutpoängen blinkar tydligt/med återkommande "off" inom samma snapshot. Den mörka normala bakgrunden måste fortsatt kännas igen i ett av tillstånden; inga snabba helskärmsblixtrar.

**G2 – stabil spelplan, markerat score pulse:** Spelplanens ursprungsfärger och positioner förblir huvudsakligen stabila. Koncentrera den visuella effekten till en tydlig tvåfasmässig, begränsad vägg-/score-kontrast och blinkande slutpoäng, utan grafiska blinkeffekter som kan likna farliga NPC eller vapen. Hitta ett tydligt grafiskt sätt att visa GAME OVER-upplevelsen i samma plan utan att anta att separat "GAME OVER"-text automatiskt får plats i kernel.

För varje koncept: minst två frysta, sammanhängande möjliga visuella faser med samma frusna gameplaybild och ett **samma** illustrativt slutscorevärde per koncept, plus en tredje illustration som visar score i 'blink off' om det behövs. Ingen ny gameplay-händelse mellan faserna. Båda ska bedömas i 1×/uppskalning, vanligt/mörkt skärmläge och tydligt mot de redan vita NPC:erna. **Om du använder texten GAME OVER** måste du ange den som **separat valbar grafikhypotes** med kostnad för nyskapad rastergrafik, inte redan godkänd font eller självklart tillgängliga sprites. En slutbild kan enligt källbeslutet fungera utan ordet "GAME OVER" om poäng och kontrast ger tillräcklig läsbarhet; redovisa osäkerheten.

### Geometri/uttrycksgräns

- Bevara ursprungs-C02:s **exakta 40×22-celler**, inkl högra dörr-zon `x=39, y=9–12` och oförändrat stängd vänsterkant. Inga nya väggar eller val av `C_OPEN_01`.
- En 40-bitars playfield-kolumn motsvarar ca **4 TIA-color clocks** horisontellt, medan en illustrationsrad tidigare modellerats som **8 scanlines** vertikalt. Leverera exakt rutmatris-snapshot som källa. När grafik förstoras eller visningsproportioner ändras, märk **SQUARE PIXEL PREVIEW** respektive **ILLUSTRATIVE NTSC-TV ASPECT** – inga påståenden om att ett 160×176-PNG är uppmätt Stellaskärm/CRT-bild eller att ett specifikt bildupplösningsformat redan beslutats.
- Guldnyckel, orange dörr och sex original-NPC bevaras som ikon-/rumsreferenser, men **GAME OVER-beslutet fastställer inte exakt hur många NPC, key, bullet eller vilken dörrfas som fortfarande visas i den frusna slutscenen**. Skapa därför en tydligt märkt **illustrativ enda C02-snapshot** och håll den identisk i alla fasbilder. Påstå inte att denna slutstatus är ny spelregel.
- Använd alternativt player V03_B bara om spelaren explicit märks som **unapproved comparison**; annars använd generell schematisk markör, aldrig ny canonbitmask.
- Poängexempel ska vara **illustrativt, positivt och samma genom fasväxling** (t.ex. `700`, ett känt scenario ur ursprunglig Master Spec), inte bestämt antal score-siffror eller font. Undvik anti-kontrast där blinkande poäng blir osynlig samtidigt som resten av bilden växlar på ett sätt som liknar skärmfel.
- **Inte tillåtet:** ny startskärm, oändlig ljusblixtring, dold förväntad skärmrasterbudget, palett som antas vara riktig TIA-NTSC-kod, fysisk joystick/RESET-kod, nya ljud, ändrad poänglogik eller ny highscorelayout.

## 3. Leverans, granskning och stopp

Leverera EN `GAME_OVER_IN_ROOM_VISUAL_V01_TO_MAIN.md` och ett faktiskt tillgängligt grafikpaket i [projektets Google Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u):
- G1, G2 med verkliga offline-PNG i källstorlek och minst 4× nearest-neighbor, gärna kort GIF med etiketten `ILLUSTRATIVE_TIMING_ONLY`; statiska bilder är primärdata. Behåll samma snapshot så att **endast färg/scorefaser** ändras.
- JSON/TXT med ursprunglig C02-cellsgrid och exakt avgränsning av varje grafiks färgfas, läslig score-vy, flaggade antaganden och 1×-visning. Verifiera att vänstervägg och högerdörrens logiska originalceller inte ändras.
- En tydlig A/B-jämförelse och egen kritisk **score readability / room continuity / eye-strain risk** med **inte-blindtestat** som läsbarhetsnivå. Rekommendera EN grafisk kandidat men ändra ingen designkanon.
- Liten riskmatris för eventuell framtida Atari-teknik: `COLUPF/COLUBK/scorefont`, runtime-befintliga 2×players/M0/PF, eventuell separat enradig textscanline, CPU-cykler/scanline, NTSC-färger och RAM. Allt **hypotes, INTE implementerat**.
- ZIP/filer inklusive faktisk filstorlek, antal poster, ZIP-CRC, full SHA-256 och alla per-file SHA256. För separata Drive-filer ge fungerande länkar och bekräftad rätt föräldermapp. Inga låtsaslänkar, inga externa copyrighted sprites/ROM.
- Begränsa dig till dessa **TVÅ** tydliga designkoncept. Om båda är otydliga i 1× eller tekniskt uppenbart orimliga, returnera `GAME_OVER_VISUAL_INCONCLUSIVE` i stället för att hitta på en tredje design.

**MOTTAGNING:** GAME OVER-bildskisser får högst status `GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`. Ingen ny ROM-kod, gammal ROM-ändring, main-/PR-merge, separat implementation, AI, scorelogik, PAL, dörrintegration eller VERIFICATION auktoriseras. Inga ändringar i The Cabin, I Love a Fish eller Linear.

**Syftet:** Förbereda visuellt val av GAME OVER-stil utan att blanda samman grafik med en spelbar Atari-implementation.
