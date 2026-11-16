# LET ME OUT! – MAIN III R1k: fem originalandroider på samma nio rader, 600 Stella-frame – lokal PASS

**Datum 2026-11-16. Kategori: ENDAST FORSKNING / INGEN SPEL-ROM-ACCEPTANCE / INGEN INDEPENDENT VERIFICATION.**

## 1. Primärresultat, commit och artefakt

**GitHub Actions [#43830971243](https://github.com/Odourman/let-me-out/actions/runs/43830971243): SUCCESS** på exakt testad commit **`c938c51c681171394f3ba19fdc6cd31e989f509a`**, branch `research/main-iii-r1k-fifth-large-female-20261116`.

- **16 384-byte NTSC standard-F6-ROM**: SHA256 **`99c2cc160713899a8662508a4eeafec956b3d9b4825668e66b135404ec79f2a7`**, exakt fyra identiska 4 096-byte-banker. **Inga specialchips eller extra RAM.**
- [Bevisartefakt #14208802023](https://github.com/Odourman/let-me-out/actions/runs/43830971243/artifacts/14208802023), fulltext `.asm`, `.lst`, `.sym`, `.bin`, original 600 Stella-X11 PNG, CSV, SHA och `summary.json`. Nedladdad ZIP: SHA256 **`5492c0c606f2144771f7f4eac888b1bfbd1ca3b7d6333c986f6953d10ef0973d`**. 622 arkivposter varav 600 PNG; ZIP CRC-test utan fel.
- Exakt verifierad byggbas R1h, tidigare [Actions #43821560463](https://github.com/Odourman/let-me-out/actions/runs/43821560463), ROM SHA `2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39`. Byggskriptet kontrollerar den hashen innan källan ändras.

### Faktiskt observerat i riktiga Stella 6.7.1-bilder

| Kontroll | Utfall |
|---|---:|
| Fem hela godkända vita originalandroid-instansmasker på identiska nio rasterrader (originaltyp 4 olika, kvinnomasken visad två gånger) | **600/600** |
| Samtliga fem med exakt 8x9 pixlar, ingen förlorad rad | **600/600** |
| Gul temporär spelare och ett M0-diagnostiskt skott på **föregående** rad | **600/600** |
| NTSC med 262 rasterrader och löpande observerade frame-ID | **600/600** |
| Vänster yttervägg via BALL, brun asymmetrisk högervägg med rätt 32-raders dörrhål | **600/600** |
| Fjärde NPC i alla fyra fördefinierade X-lägen | 150 / 160 / 146 / 144 frames |
| Dörr öppen/låst | 290 / 310 frames |
| Alla 4×2 kombinationer av fjärde NPC:s X och dörr | **8/8**, var och en minst 64 frames |
| Vita/gula skuggpixlar och brutna originalmasker | **0** |
| Felslagna frame-kontroller | **0** |

Exakt figuruppsättning: 1 **stor man** på GUI-x166, **två stora kvinnor** på GUI-x**248 och 280**, 1 **liten man** på GUI-x406, 1 **liten kvinna** på GUI-x330/348/360/378. Gul testspelare x216. Det här matchar fem av de sex R1-individerna (kravet är två stora män + två stora kvinnor + en liten man + en liten kvinna); den **andra stora mannen saknas**.

## 2. Mekanism och ett verkligt hardware-fynd

I den bevisade R1h-kerneln skrivs `FemaleRows,Y` till `GRP1` vid CPU-cykel c36, därefter kommer två `BIT FRAMELO` (3 CPU-cykler per instruktion) och `STA RESP1` vid c45. **R1k ersatte första `BIT FRAMELO` med ytterligare `STA RESP1` (båda tre cykler / två programbyte).**

- Strobe-slut vid c**39** och c**45**, separerade med **6 CPU-cykler = 18 TIA-färgklockor**.
- Det gör att två separata stora kvinnor, vardera med **samma kompletta originalbitmap**, syns på samma skannade rasterrad. Den första masken är **inte en pixelförenklad PF-kropp och inte tidsmultiplexat 10 Hz-flimmer**.
- **Viktigt faktisk mätfynd:** naivt antagen x244 för första kvinnan var **fel**. Verklig Stella X var **x248**, alltså **+4 GUI-pixlar = +2 TIA-färgklockor** på grund av 18CC-återtriggningens särskilda TIA-fas. Andra kvinnans x280 var oförändrat. **Observerat avstånd mellan kvinnorna är alltså 16 TIA-färgklockor**, trots 18CC mellan reset-CPU-händelser. Detta är viktigt för framtida positionsbudget.
- Inga CPU-cykler tillfördes i rasterloopen, inga byte flyttades i originalbitmaptabellerna, ingen F6SC/DPC/ARM användes.

**Spårbar tidigare FAIL:** Första [Actions #43830343687](https://github.com/Odourman/let-me-out/actions/runs/43830343687) byggde och spelade in exakt samma ROM men underkändes av en **felaktig provhypotes** x244. Felrapporterna visade `large_female_early_errors=64`, `large_female_late_errors=0`, `ghost_white=36`, 0/600. MAIN III öppnade de verkliga råbilderna, mätte exakt två fullständiga masker vid **x248** och **x280**, ändrade enbart auditens **förväntade observerade x** och provade om **600** bildrutor i Actions. Detta är en transparent rättning av felaktig TIA-koordinatprediktion, **inte** en tillåten ändring av originalmasker eller visuella acceptanskrav.

## 3. Extra bild-/arkivkontroll, skild från men inte formell independent verification

MAIN III laddade ned det **framgångsrika** evidenspaketet och kontrollerade:

1. ZIP CRC och exakt 622 poster (600 original-PNG).
2. Den faktiskt ingående 16384-byte-ROM-hashen stämmer med både manifest och Actions.
3. Råbildernas huvudspelregion ger **exakt 8 unika SHA-256-bildbilder**, en stabil bild för varje av 4 NPC-X × 2 dörrtillstånd, **600/600**; ingen bildhash delas mellan två tillstånd. Den femte kvinnan syns i varje enskilt tillstånd.
4. Föregående misslyckade körnings råbilder, med enbart auditkorrektionen x248, gav också 600/600 lokalt. Starka dubbla observationer, **inte** en från ROM DEVELOPMENT oberoende slutverifierare.

## 4. Hårda gränser – detta är **inte full R1**

- **Fem**, inte **sex**, vita originalandroid-instanser; andra stora mannen saknas.
- Kvinnorna är **låsta tillsammans**: två P1-utlösningar c39/c45 med fast faktisk separation **16CC**. De har **inte** individuella, fullt fria X-positioner. De tre övriga stora/lilla männen och den gula testspelaren har fasta X. Fjärde lilla kvinnan har **fyra diskreta** X, inte fritt 160CC.
- Om den extra kvinnan och en annan kvinna ska röra sig oberoende, krävs ytterligare positionsmekanik utan att förstöra synliga masker. En reproducerbar 600-frame animation kan fladdra i tidslägen, men är ännu inte spelarstyrd/AI-drivet gameplay.
- **M0-skott på föregående rasterrad**, inte i samma nio-raderskonflikt. BALL används kontinuerligt som vänstervägg.
- Endast brun PF0 högeröppning; **ingen orange låst port eller svart nyckelhål**, ingen komplett 40×22-karta.
- R2:s fem NPC + gold key/O1, R3:s fulla portfärg/nyckelhål och R4:s rörelsestress **inte PASS**. PAL/äkta Atari-hårdvara ej testad. Ingen formal VERIFICATION på det exakta SHA-paret.

**Projektstatus:** `R1k 5-original-NPC same-Y = LOCAL_PASS`. **`R1 full = FAIL/BLOCKED`.** `main`, ROM DEVELOPMENT:s draft PR #7 och gamla VERIFICATION-issue #8 ändras inte.

## 5. Föreslagna nästa forskningsgrindar

**R1l (endast analytiskt förslag, inte automatisk fullspelsimplementation):** Kartlägg P1/P0:s faktiska register/cykel- och färgmaskbudget för **den andra stora mannen**, men tillåt inte enklare felaktiga masker, 10 Hz-flicker eller nya mapper. Beakta att P1 nära retrigger i R1k flyttar första kvinnokopian +2CC och att ett ytterligare `STA RESP1` normalt kostar 3 cykler medan R1h-kerneln redan upptar 74–75 cykler. Utan ny cykelneutral slot eller kompletterande kernel är sex originella same-Y-instanser inte bevisade. Efter ett positivt sjätte-objektsprov återstår den långt svårare grinden med **alla sex fria X** över hela rummet samt samlad R1/R2-bakgrund, skott och spelare.
