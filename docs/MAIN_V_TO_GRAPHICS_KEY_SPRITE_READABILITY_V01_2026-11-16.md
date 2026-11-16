# LET ME OUT! – MAIN V till GRAPHICS
## KEY SPRITE – NATIVE 1× READABILITY v0.1

**Datum:** 2026-11-16. **Kategori:** NYTT **ENBART GRAFISKT DESIGNUPPDRAG** efter avslutad GAME OVER v0.1-studie. **Status alla nya bilder:** GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD. Ingen programmering, spelregeländring eller canon-cutover.

### 1. Läs de bindande aktuella källorna först

- [GRAPHICS-roll och arbetsmetod](MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md).
- [Aktuell översta projektstatus](CURRENT_PROJECT_STATE_2026-11-15.md).
- [MAIN:s GAME OVER-mottagning](MAIN_V_GAME_OVER_IN_ROOM_VISUAL_V01_RECEIPT_2026-11-16.md).
- [v0.13 användargodkänt visuellt mål för guldnyckeln](KEY_AND_DOOR_VISUAL_TARGET_V013.md). Det är den **ledande grafiska målbeskrivningen**, men **K09 8×9 och K11 8×11 är endast tidigare skisser, INTE slutmasker**.
- [v0.14 kontraststudie](KEY_CONTRAST_RGB_REVIEW_V014.md). `#F2AD00` djupguld är en **illustrativ RGB-kandidat** i offlinebilder, **INTE** fastställd NTSC TIA-färgkod.
- [v0.15 nyckel-överlapp](KEY_OCCLUSION_LOGIC_V015.md) samt [senare kompletterande godkänt O1-beslut](MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md): en annan android kan visuellt skymma nyckeln, men logisk position oförändrad och den återkommer synligt när androiden passerat.
- [Mottagen D1 dödsanimation](MAIN_V_COMMON_ANDROID_DEATH_ANIMATION_V01_RECEIPT_2026-11-16.md): **D1 är bara visuellt förstahandsförslag**, inte implementerad; nyckeln får komma på dödad nyckelbärares sparade position **först efter animationens sista EMPTY-fas**.
- [Godkända ursprungsandroider](../design/NPC_REFERENCE_8x9_masks.json), Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; [planerade rum C02](../design/PLANERADE_RUMSKARTOR_V011.json); [spelarens skalkrav](MAIN_PLAYER_SCALE_V018_2026-11-15.md).
- [Användarens originalöverlämning med egna referensskisser](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view). Adobe Stock-vattenmärkta användarreferenser är **endast inspiration, inte kopierbara publicerade assets**.

**Bindande visuellt mål:** En tydligt **guldgul** mycket liten lös nyckel med **runt ringhuvud, verkligt synligt mörkt genomgående hål, kort nedåtgående skaft och ett par små tänder längs högra sidan**. Nyckeln uppstår stillastående på tidigare androids fallposition **först efter färdig dödsanimation**, ligger still tills spelaren hämtar den; annan android kan skymma den (O1), men ingen nyckelflytt. Gul spelare med hatt/vapen är ljusare, och den godkända originalfiguren är lika stor som stor NPC. Vägg brun, bakgrund mörk, orange högerport med svart nyckelhål. **Nyckelns faktiska bitmap, dimension och NTSC-färgkod är ännu INTE slutgodkända.**

### 2. GÖR EXAKT TVÅ NYA KEY-MASK-KANDIDATER

**K09-R – strikt 8×9:** Förbättra eller metodiskt motivera en **niobytes 8×9-maske** med ringens mörka hål mot mörk spelbakgrund, en tydlig formskillnad från spelarens gula mänskliga siluett, ett kort skaft och små tänder på högersidan. Utgå från historisk K09-radmask som **opåverkad jämförelsebas**:
```text
00111100
01111110
11100111
01111110
00011000
00011100
00011000
00011100
00011000
```
Ingen ny rad/hårdvarusprite som dold kostnad. Behåll hela `8×9` med exakta 1-bitarsrader.

**K11-R – läsbarhetsorienterad 8×11:** Förbättra eller metodiskt motivera **8×11-radmasken** enligt samma visuella huvudmål, med ett tydligare runt hål om två extra rader hjälper men **kortare skaft än referensens för långa streck**. Utgå från historiska, INTE slutgodkända K11:
```text
00111100
01111110
11100111
11100111
01111110
00011000
00011100
00011000
00011100
00011000
00001000
```
**8×11 är endast en alternativ GRAFIKKANDIDAT:** två ytterligare vertikala maskrader kan belasta P1/GRP-kerneln, särskilt samtidigt som fem återstående androider, gul P0 och M0-skott. Ange den tydliga extra kostnadsrisken och `TECHNICAL DESIGN WAIVER REQUIRED` om detta förändrar nuvarande 8×9-objektsplan. Ändra aldrig collision footprint/logiskt nyckel-ankare i denna studie.

**Exakt två nya maskkandidater**, inte fler. Det är tillåtet att en av dem blir **byte-identisk med K09/K11** om du visar att inga förbättringar klarar läsbarhetstestet. Annars redovisa varje förändrad bit jämfört med respektive gamla bas. Ingen ny K12, ingen ny spritefärg för varje del, ingen extra P0/M0/P1/BALL/PF-resurs för ringhålet; hålet ska framgå ur NEGATIVT RUM i den egna enfärgade silhuetten.

### 3. VISUELLT TEST – fokus naturlig skala, inte stora reklam-mockups

Visa i samma kontrollscen de **fyra** nyckelbilderna (original K09/K11 och nya K09-R/K11-R), var och en i:
- verklig **1× maskpixel**, tydligt 4× samt 20× nearest-neighbor med valfria pixelgrid-annoteringar **endast utanför** maskassetet;
- ljusgul/gul P0 `V03_B` endast som märkt `NOT APPROVED COMPARISON`, stor vit man och kvinna 8×9 exakt ursprungsmask och brun PF-miljö/mörk bakgrund;
- minst två illustrativa guldtoner ur redan känd v0.14 RGB-studie, med samma mörka bakgrund. Märk färgerna `ILLUSTRATIVE RGB – NOT NTSC TIA VALUES` och påstå aldrig att en färgkod är tekniskt tillgänglig;
- **D1 nyckelbärarens storyboard:** ORIGINAL → HIT → DISSOLVE → EMPTY → **KEY VISIBLE** vid samma sparade maskursprung. Ingen nyckel före eller under dödsanimation. Högst en kandidateffekt per version i scenprov; D1-maskerna förblir oförändrade.
- **O1 skymning:** efter att nyckeln blivit synlig går en originalandroid över den, helt eller delvis skymning är tillåten, sedan återkommer exakt samma nyckel på samma position. Inget glittrande, ingen automatisk omplacering, ingen AI-/kollisionsregel skapas.
- En enkel svart/vitt-inverterad, etikettfri blindläsbarhetsbild i faktisk 1×; om ringhuvudets *mörka hål* bara är ett par otydliga pixlar, säg `KEY_HOLE_UNREADABLE_AT_1X`. Om tänderna blir otydliga, förklara vilken kompromiss som gjorts. Max två kandidater. Självbedömd läsbarhet ska inte kallas externt blindtestad.

Det viktiga är **nyckel + hål + tänder**, inte att alltid fylla 8×11 eller att en skiss ser snygg ut i 20×. Med två möjliga högder ska små sprites fortfarande få vara mindre än stora; använd ingen "automatic 2x" av nyckeln till ROM-proven.

### 4. Pixelrader, källor, proveniens, risker

- För båda kandidaterna: exakt 8 kolumner, **9 respektive 11 rader**, varje rad binär+hex, totalt antal "1"-pixlar, bitdiff/koordinater från respektive K09/K11-bas, aktuell mask SHA256 för exakt 9/11 bytes, deklarerad `MSB LEFT / TOP-TO-BOTTOM` och en mycket kort kodbar geometribeskrivning av ringens hål.
- Skilj även på **8×9 bilddatastorlek**, visuellt färgval, kollisionsyta och verklig ROM-rendering. Rita **inga** nya godkända key/hole/door-resurser.
- Fysisk användning av svart nyckelhål i en orange port är ett **SEPARAT** tidigare valt visuellt mål, inte en del av denna key-sprite; skapa inte ny dörrdesign.
- Teknisk risklista till MAIN: rå nyckelmask **9 vs 11 bytes** (och +2 synliga/ytterligare rader om de används), palettval, återstående fem NPC, samma-y konflikter med P0/M0/PF, P1/GRP1-kernel, eventuell O1-visningsprioritet, keyspawn efter death. **Inget påstående att bytes = total RAM/kerneltid**.
- Resultatet ska vara två **fristående kandidatmasker**, inte en ny slutfärdig nyckel. Rekommendera EN grafisk förstahandskandidat med tydlig kompromiss, eller bedöm `KEY_SPRITE_VISUAL_INCONCLUSIVE`.

### 5. Leverans och stopp

Leverera **EN** `KEY_SPRITE_READABILITY_V01_TO_MAIN.md`, JSON/TXT/ASM-**design-only** 9- och 11-byte-datatabeller, verkliga 1×-PNG, närmaste-granne 4×/20×, 1×/4× jämförelse och eventuell GIF storyboard med TID `ILLUSTRATIVE_ONLY`. Ta med källkopior av endast lagliga ursprungsreferenser, inte vattenmärkta stockbilder.

Skapa ett **faktiskt** ZIP-paket med `SHA256SUMS.txt` och manifest, egen verifieringsscript för radmått/hex/PNG-hash/8×9-konflikter, CRC, total SHA256, och publicera paketet samt handoff och 1–2 huvudjämförelsebilder som **verkliga öppningsbara fil-URL:er** i rätt [projekt-Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Ange äkta filstorlek och föräldermapp. Arkiv ska inte genereras med skenlänkar.

**STOPP efter exakt dessa TVÅ maskkandidater och en samlad handoff.** Ingen vidare färg/nyckel-v0.2, ingen justering av godkända original-NPC, gamla D1/G2, player, rum, GAME OVER-beslut, repos `main`, PR#7, Issue#8, bankswitching, PAL eller integration. GRAPHICS gör **inte** DASM/Stella/ROM/nyckelspawn/kollision, ändrar inte originalfiler och ger ingen ROM DEVELOPMENT-auktorisation. Full R1 ännu blockerad. Om du ser materialkonflikt mellan källor, **redovisa** den för MAIN i stället för att tyst välja.
