# LET ME OUT! – MAIN V till GRAPHICS
## SCORE & LIVES HUD – VISUAL CONCEPT v0.1

**Datum:** 2026-11-16. **Status:** NYTT, avgränsat **ENBART OFFLINE GRAPHICS-/READABILITY-UPPDRAG**. Skapa **två** presentationsförslag för löpande poäng och återstående liv, inte en Atari-kernel, nya score-/life-regler, ROM-kod eller final HUD-canon.

### 1. Källauktoritet och faktiskt beslutade spelvärden

Kontrollera aktuella källor i GitHub och projektets Drive innan du ritar:
- [MAIN:s GRAPHICS-roll](MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md) och [högst prioriterat projektläge](CURRENT_PROJECT_STATE_2026-11-15.md).
- [MAIN:s KEY SPRITE v0.1 mottagning](MAIN_V_KEY_SPRITE_READABILITY_V01_RECEIPT_2026-11-16.md), K09-R **endast preliminär jämförelsekandidat**, inte en godkänd key-implementering.
- Ursprungshandoff [`LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip`](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), framförallt `02_MASTER_SPEC.md` §§8–12 och **`03_DECISIONS.csv` rader #042–050**. Kontrollera äldre historisk presentation mot [senare användarbeslut om GAME OVER och RESET](GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md), vilket **supersederar** den ursprungliga obeslutade startskärmsfrågan.
- [GAME OVER G1/G2 endast grafikstudie](MAIN_V_GAME_OVER_IN_ROOM_VISUAL_V01_RECEIPT_2026-11-16.md): G2 är *preliminär*, dess nya pixeltypsnitt och `GAME OVER`-text **inte tekniskt möjligt bevisade eller godkända**.
- [Planerat C02-rum med exakt 40×22 rutmatris](../design/PLANERADE_RUMSKARTOR_V011.json); [fyra låsta originella androidmasker](../design/NPC_REFERENCE_8x9_masks.json); [spelarens gula skala](MAIN_PLAYER_SCALE_V018_2026-11-15.md).

**Endast följande är redan fastställda spelregler och ska återges korrekt i illustrativa räkneexempel:** `score=0` vid spelstart och aldrig under 0; **-25** per förstörd android; missat skott 0; **+50** när nyckeln verkligen plockas; **+100** först när spelaren verkligen har lämnat rummet; **+15 per överlevande android** vid utgång; highscore rangordnas endast på poäng; **3 liv** vid spelstart; en förlorad spelare mister ett liv och behåller redan intjänade poäng; extraliv vid **500, 1500, 2500, ...** varje gräns högst en gång per omgång. Inga tal ska bli en ny poängbalansregel på grund av HUD.

**FORTFARANDE ÖPPET:** var score/liv visas, antal ciffror som max stöds i framtida spel, font, en eller flera separata bildband, porträtt eller livsymboler, dynamik för 4/5-siffror, max liv, highscore-lagring, exakt NTSC-timer/palette, ljud och äkta 6502/TIA-resurs. **Du får jämföra tydliga alternativ, men inte avgöra bindande gameplay- eller maskbeslut åt MAIN.**

### 2. Den begränsade grafiska frågan

Hur visar Let Me Out! **aktuella poäng och liv utan att spelares, vitandroidernas, skottets, nyckelns eller högerutgångens läsbarhet försämras i ett litet, rasterkänsligt Atari 2600-rum?**

Skapa **exakt två** faktiska och visuellt meningsfullt olika OFFLINE-koncept, i samma låsta C02-matris utan att byta väggar, rum, NPC-utseende eller spelares grundfigur:

**H1 – Toppband (separat score/lives-visning)**: Visualisera en kompakt rad över spelplanens översta vägg, där en kort poängsiffersekvens och diskret livindikator placeras. Rita en tydlig rumsbild och en avskild band-skiss i rätt relativ storlek. **Rita INTE bandet som om VBLANK/overscan kan användas som synliga pixlar**; eventuellt synligt separat toppband kräver NYA synliga NTSC-scanlines och/eller att själva spelplanen kortas/omorganiseras. Explicit märk `DISPLAY-LAYOUT HYPOTHESIS / NO FREE SCANLINES`.

**H2 – Integrerat i befintligt synligt rum**: Visa en kompakt poäng-/livstext/ikon i redan öppna översta inre C02-området, **som separat illustrativt grafiskt överlägg**, utan att ändra en enda `#`/`.`/`D`-cell. Om informationen kan överlappa en rörlig android, skottet eller användarens flyktväg: illustrera konfliktrisk och mörka ytor, men anta INTE att den fysiska P0/P1/PF/M0-kerneln har kapacitet för displayen.

### 3. Läsbarhets- och scenarioserie – INGEN ny score-canon

I båda H1/H2:
- Visa ett **och samma** exakta C02-rum/samma placeringar med sex **oförändrade** originalandroider (2 stora män, 2 stora kvinnor, 1 liten man, 1 liten kvinna), brun PF-vägg, mörk bakgrund, högra orange port enbart **ILLUSTRATIVE**, och gul spelare `V03_B_UNAPPROVED_COMPARISON` om behövligt. K09-R får bara visas som **preliminär** nyckeljämförelse vid samma kända ursprungsposition efter en redan illustrerad death; inte som ny spelmekanisk HUD-ikon.
- Visa statiska poängprov med verklig variabel **0, 475, 700, 1500, 10250**, och **3, 2, 1, 0 liv** som separat annotationsserie. `10250` är **bara ett gränsfall för fontbredd**, INTE beslut om maxpoäng, antal siffror eller möjligen uppnåelig poäng. `0 liv` hör samman med redan beslutat GAME OVER, inte att en levande spelare skulle röra sig med 0 liv.
- Minst en annoterad **poänghändelse-sekvens** som följer redan fastställda regler: exempelvis ursprungligt Master Spec-exempel `500 → 475` vid en förstörd android `→ 525` när nyckeln plockas `→ 700` efter faktisk utgång med fem överlevande. Förklara att extra liv vid 500 avgörs av tröskelns tidigare uppnådd-status; **gör INTE en animation som ger nya liv varje gång 500 passeras fram och tillbaka**. Det kan räcka att visa statiska siffror/metadata, inte nya gameplayrutiner.
- Leverera siffrorna 0–9 som *design-only* exakta bitmönster/radbitar för en föreslagen 3×5 eller 5×7 font och visa score/liv i faktisk 1× källstorlek, nearest-neighbor 4× och 20×. Det är helt okej att olika koncept har olika fontstorlek, men redovisa bytekostnad och att **siffror INTE redan är reservade TIA-resurser**.
- Två tydligt åtskilda livindikatorstilar som kan läsas utan färg (t.ex. tre korta stavar och tre små spelarsiluettsmarkörer), men **gör INGA nya godkända sprites** och påstå inte att extra lives "är ledigt gratis" i P0/P1/BL/resurserna. Du får visa `3/2/1/0` numeriskt som fallback med teknisk risk.
- Kontrollera att en sexfigursruta, högerdörrens x39/y9–12 och ramen inte förändrats. Mät var displayen skymmer/byter färg och redovisa konflikter när en NPC faktiskt passerar nära HUD-överlägget. Ingen personskarpa överlappsåtgärder låses.
- Om en eller båda grafiklösningarna är uppenbart fel vid 1×, skriv `HUD_VISUAL_INCONCLUSIVE` med tydligt hinder. Välj **en** preliminär rent **grafisk** favorit med tydliga kompromisser; ingen ny v0.2-serie utan nytt beslut.

### 4. Framtida Atari-teknik måste hållas i egen, osäker risklista

Belys utan att implementera:
1. NTSC 262 scanlines/76 CPU-cykler per scanline; separata synliga scoreboard-scanlines kräver **verklig tidsbudget** och kan krympa spelplanet. VBLANK/overscan är inte synliga textytor.
2. TIA saknar generell textvideo/teckenfont; poängsiffror och livesymboler måste ritas med befintliga eller nya register-/kernelmetoder, vilka kan konkurrera med P1-sexandroidmultiplex, P0-gul spelare, M0-skott, brun speglad PF och orange högerport.
3. Möjlig extra ROM-/RAM-/bankkostnad för sexfaser, scorefont och lives-symboler; 128-byte RIOT RAM (ingen ny allokering här).
4. GAME OVER G2 behöver separat score/text-resurser som denna grafikstudie **inte** kan godkänna genom snygg mockup.
5. Highscore persistens/högsta score/antal liv är **öppna**. Skapa ingen batteri-/SaveKey-/extra-maskinvarurestriktion och ingen fake highscore-rankning.

### 5. Leverans, kontroll och stopp

Skapa `SCORE_LIVES_HUD_VISUAL_V01_TO_MAIN.md`, JSON för **ursprungliga C02-rader, alla score-cases, de faktiskt ritade digit-bitarna, H1/H2-lägen och renderingskoordinater**, grundoriginalen byteexakta. Faktiska 1×-PNG och 4×/20× pixelgrid, en tydlig sammanställd huvudbild, gärna en kort A/B-jämförelse-GIF endast `ILLUSTRATIVE_ONLY`. Leverera **fungerande** ZIP/JSON/PNG/rapport i [rätt dedikerad Google Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u), med ZIP-CRC, äkta storlek/postantal, full arkiv-SHA256 och per-file `SHA256SUMS.txt`. Markera alla skisser `GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`.

**STOPP efter H1 och H2 och en samlad handoff.** Ingen kod, DASM, ROM, Stella, bankbyte, score-/lives-/extraliv-implementation, högre R1–R4, PAL, kart-/NPC-/spelarspritemaputbyte, GAME OVER-/KEY-ny canon, eller ny maskuthållighet. Vid källkonflikt redovisa för MAIN innan konstnärlig beslutswaiver. Här väljer GRAPHICS inte slutlig HUD-canon.

**Syftet:** fatta ett bättre framtida presentationsbeslut utan att lägga UI-information ovanpå redan blockerad TIA-kernel och anta att den magiskt ryms i hårdvaran.
