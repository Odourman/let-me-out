# LET ME OUT! – MAIN V till GRAPHICS
## PLAYER SPRITE v0.2: två avgränsade förbättringar av kandidat A

**Datum:** 2026-11-16. **Roll:** grafiskt designuppdrag, inte en ROM- eller implementationauktorisation. **Status v0.1:** GRAPHICS CANDIDATE / underlag mottaget / EJ GODKÄND SLUTMASK / EJ STELLA-TESTAD.

### 1. MAIN:s bedömning och bindande beslut

GRAPHICS har levererat tre föreslagna spelarfigurer à **8×9 binärpixlar** och nio synliga rader. ROM DEVELOPMENT II har källmässigt bedömt dem som rimliga P0-kandidater utan byte- eller ROM-ändring. MAIN har läst de **faktiska nio raderna för A/B/C** och jämfört med användarens **ursprungliga blå handtecknade spelare** i `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip/assets/02_USER_PLAYER_SKETCH.jpg`.

Kandidat A (33 pixlar) är bäst som **arbetsbas**: hattsilhuetten och vapnets ungefärliga riktning åt **nedre vänster** liknar originalskissen mer än B/C. Men vapnet kan förväxlas med en böjd arm och vänster arm-/vapendel ser orolig ut vid ursprunglig 1×-upplösning. B (34 pixlar) har ett bredare brätte och mindre naturlig vapenarm. C (33 pixlar) verkar högerorienterad och är mindre lik handskissen. **Inget av dessa estetiska omdömen är ett nytt användarbeslut**.

**MAIN auktoriserar endast v0.2 som en fortsatt grafikstudie.** Uppgiften är att utforma **TVÅ tydligt skilda förfiningar av A**, inte att producera 20 förslag, byta alla sprites, eller beskriva A som slutgodkänd. Bevara A oförändrad som jämförelsebas, inte byta dess rader retrospektivt.

### 2. Exakt oföränderlig v0.1-A-bas

Rader uppifrån ned, exakt 8 bitar, '1' = synlig gul pixel:

```text
0  00111100
1  01111110
2  00111100
3  00011000
4  01111100
5  11011100
6  10011000
7  00100100
8  01000010
```

33 tända pixlar, nio av nio synliga rader. De exakta fyra godkända androidreferenserna ligger i `design/NPC_REFERENCE_8x9_masks.json`. Stora androidmasker har alla nio rader fyllda; små har bara sex synliga rasterrader. Spelaren ska vara **jämförbar i visad skala med de stora** och gul.

### 3. Detta ska GRAPHICS göra nu

1. **Referenskontroll.** Läs aktuellt `docs/MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md`, `docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md`, originalskissen och A:s riktiga bitmatris. Kontrollera nytt repo-/Drive-läge innan statusuppgifter.
2. **V0.2-A1 – prioriterat, skissnära:** Försök göra vapnet **tydligt separat från vänster arm/hand** i samma 8×9-ram. Vapnet ska om möjligt fortfarande peka ungefär snett **nedåt-vänster**, som användarens ursprungliga skiss. Behåll hattkrona + läsbart brätte och tydlig mänsklig torso/ben. Undvik att göra figuren större, bredare än 8 eller kortare än 9 synliga rader.
3. **V0.2-A2 – alternativ med tydligare vapen:** Gör en annan **visuellt märkbart skild** lösning på vapenproblemet med ett mer urskiljbart separat vapen-/handgrepp, utan att göra figuren till robot eller ändra dess skala. Undvik enbart kosmetisk enpixeländring som inte löser igenkänningen. Redovisa vad som offrats i hatt/arm/body.
4. **Storlek/teknik:** Båda måste vara verkliga **8×9, 1-bitars, nio synliga pixelrader** med en **enda gul P0-färg** i grundmasken, om inte en teknisk begränsning uttryckligen redovisas som icke godkänt alternativ. Ingen ny P1, M1, BL eller PF-resurs reserveras för att rädda vapnet; P0 är aktuell spelare, P1 är redan hårt belastad av sex androider, M0 aktivt skott.
5. **Jämförbarhet:** Leverera A v0.1 + A1 v0.2 + A2 v0.2 samt stora originalandroider **i exakt samma bildskala** och mörk bakgrund, både **1× närmaste-granne och 20× grid**. Gör också ett **svartvitt kontrasttest**: är hatten, handen/vapnet och de separata benen läsbara utan hjälp av etiketter?
6. **Pixeldataleverans:** För A1 och A2: nio binära strängar, nio hexbytes, antal tända pixlar, faktiskt ändrade koordinater jämfört med exakt A, byte-/radchecksumma och en separat `JSON`-masktabell märkt `GRAPHICS_CANDIDATE_NOT_ROM_APPROVED`. Skapa PNG/bildpaket och en läsbar PDF endast om det konkret hjälper, men **inkludera fungerande direkta fil-/Drive-länkar**: v0.1 påstods ha ZIP/PNG/JSON utan någon faktisk bifogad länk i MAIN:s mottagning. Inga låtsaslänkar. Om du inte kan publicera en fil, leverera faktisk bitmatris och dokumentera att arkivet saknas.
7. **Egen kritisk bedömning:** Välj EN preliminär favorit med två sakliga motiv för läsbarhet och ett dokumenterat offer. Förklara om vapnet **inte går att skilja från armen** inom 8×9; skriv då det direkt, inte PASS eller "klart" genom större mockup.
8. **Handoff:** En samlad `PLAYER_SPRITE_V02_TO_MAIN.md` eller motsvarande läsbar handoff med källor, variationer, 1×/20×-visningar och länk till verkande artefakter. Beteckning **`GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`** tills MAIN och användaren uttryckligen väljer kandidater och separat ROM-utvecklare senare har auktoriserat ett test.

### 4. Avgränsning gentemot ROM DEVELOPMENT

R1-F2 visade endast en tidstyrd liten X-ändring för android index 2. R1-F3 rapporterar på commit `65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190` **`F3_SECOND_INDEX_GEOMETRY_FAIL`** för *en enda* index0 +1-cykel-prob (faktisk RESP1 c19→20 men grafiskt X kvar); **`F3_TWO_INDEPENDENT_RUNTIME_X_LOCAL_INCONCLUSIVE/NOT_RUN`**, eftersom senare test stoppades. Detta bevisar inte att alla andra scheman är omöjliga. Fullt R1 fortfarande BLOCKED/NOT ACCEPTED. Ingen anledning att ändra grafiska originalkrav eller spelarfigurens skala.

**Ingen** ändring av `design/NPC_REFERENCE_8x9_masks.json`, spelarens nuvarande ROM-P0, kartor, godkända designbeslut, GitHub `main`, utvecklarbranch, PR#7 eller VERIFICATION-baslinje. Ingen ROM-, DASM- eller Stella-implementation beställd. Inga nya ljud, regler, dörr-/nyckelcutover, R2/R4, fullspel, PAL eller nya Atari-kassetthårdvaror. Grafikkandidater hålls separat från canon. Ändra inte The Cabin eller I Love a Fish.

### 5. Mottagningskällor

- [GRAPHICS rollinstruktion](MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md)
- [Spelarens 8×9-skalbeslut](MAIN_PLAYER_SCALE_V018_2026-11-15.md)
- [Fyra oföränderliga NPC-referensmasker](../design/NPC_REFERENCE_8x9_masks.json)
- [Originalöverlämning i dedikerade projekt-Drive](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view)
- [Verifierad F3 utvecklarslutrapport](https://github.com/Odourman/let-me-out/blob/65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F3.md)

**Huvudprincip: först visuell tydlighet på naturlig 8×9, därefter eventuellt separat tekniskt ROM-prov.**
