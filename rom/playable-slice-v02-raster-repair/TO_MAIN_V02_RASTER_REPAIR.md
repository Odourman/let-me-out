# TO_MAIN_V02_RASTER_REPAIR

**Ny spelbar F6/NTSC-checkpoint med kortare fiendebortfall. Resultatklass: BOUNDED_RENDER_PROGRESS / RENDER_FAIL.** Gopher2600 återgav fem kompletta originalmasker utan vita extrapixlar i 585 av 600 bildrutor, jämfört med 549 i start-ROM:en. Samtliga nya emulatorobservationer är utvecklarens egenkontroll.

Startcommit `4ffd58c02d31f6553afc591ccf9c0c6d6d149444`, ROM SHA-256 `51e85c7787483927ff3ca0924cdcd3b10e311b7fe44916ccc3f26ee874732800`. Ny ROM `let-me-out-v02-raster-repair.bin`, SHA-256 `c6ec4d8fd70dd233bb4fef9fefc62c5fa824ce7041b778884de3d43b36f589b5`. [MAIN X:s arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7011242001)

## 600 sammanhängande Gopher2600-bildrutor

Varje NPC-rad anger komplett mask / delvis synlig / helt osynlig / längsta sammanhängande osynlighet. Koordinaterna lästes från spelets RAM och pixelvärdena jämfördes med de godkända maskerna.

| Mätning | Fryst start | Ny ROM |
|---|---:|---:|
| Fem kompletta masker, 0 extra vita pixlar | 549/600 | **585/600** |
| Minst en utelämnad NPC | 46/600 | **10/600** |
| Bildrutor med extra vitt | 0/600 | **0/600** |
| M (0) | 600 / 0 / 0 / 0 | 600 / 0 / 0 / 0 |
| M (1) | 595 / 5 / 0 / 0 | 595 / 5 / 0 / 0 |
| F | 600 / 0 / 0 / 0 | 600 / 0 / 0 / 0 |
| SM | 600 / 0 / 0 / 0 | 600 / 0 / 0 / 0 |
| SF | 554 / 0 / 46 / 46 | **590 / 0 / 10 / 10** |

P1 avslutar SM när SF behöver sina första två tända rader. Båda raderna hos SF är fyra sammanhängande pixlar. Den tredje grafikbanken använder den separat positionerade M1 för dessa pixlar och byter sedan P1 till resten av den oförändrade SF-masken. Den nya vägen gäller en uppmätt domän i dörrbandet med SF på X72–78, fyra raders Y-skillnad, minst 20 pixlars X-skillnad och fri tid från spelare, projektil och nyckel i de berörda raderna. Den lämnar de logiska positionerna fria. Tidig HMOVE tog vänsterväggens pixlar. Den sena HMOVE-vägen använder en justerad HMP1 och kompenserar P0:s redan satta position med HMP0. De 10 kvarvarande SF-bortfallen inträffar när P0:s gula mask ligger på raderna som behövs för bytet. M (1) tappar fortfarande en vit pixel i fem bilder där spelarens gula pixel har samma koordinat.

Det frysta fem-samma-Y-provet på Y86 visar fortsatt 2/5 fullständiga figurer, F och SF. M1:s fyra sammanhängande pixlar kan återge SF:s två översta tända rader i det förskjutna fallet. Den kan inte återge de tre återstående originalmaskerna i samma-Y-körningen. Det nya riktade provet på X74 med fri P0 visar fem fullständiga masker mot tidigare fyra och inga extra vita pixlar. De redan felaktiga gula pixlarna i just den fixturen är oförändrade, 10 saknade och 6 extra. Fixturen med spelaren på bryggraderna utelämnar fortfarande SF.

## Nyckel, dörr, väggar och skott

| Prov | Fryst start | Ny ROM |
|---|---:|---:|
| Pixelkorrekt kallstartsnyckel under golvtiden | 65/65 | **65/65** |
| Nyckel med aktivt skott | 14/14 +0 extra | **14/14 +0 extra** |
| Nyckel när spelaren upptar bytesbandet | 0/14 | **0/14 FAIL** |
| M0-skott, tio provpositioner | 10/10 | **10/10** |
| Standard-PF i X64-provet, saknade / extra | 8 / 0 | **8 / 0 FAIL** |
| Låst orange / öppet mörkt / fysisk passage | PASS | **PASS** |
| Svart utskuret dörrnyckelhål | Saknas | **FAIL** |

I nyckelprovet med spelaren i samma band återgav ROM:en samtliga gula pixlar och 10/20 av SM:s vita. P0 har här spelarens gula mask medan P1 försöker bära SM. En M1-rad av den typ som hjälpte SF kan inte återge den separata guldmaskens olika radformer samtidigt med den vita P1-färgen. Skottfixturen återger alla 14 nyckelpixlar men har fortsatt två delvisa NPC-masker och tio extra vita pixlar. Det tidigare frysta försöket med en svart M1-stencil för dörren gav 268 scanlines och skadade P1-masken. Försöket är kvar i startcheckpointens negativa material.

En direkt jämförelse av exakt pixel-RGB i alla 600 par gav samma gula och orange koordinater i varje bild. Fyra korrekta bruna vänsterväggspixlar återkom i vardera 23 bilder, vid X0–3 på bildrad 121. Inga bruna pixlar tillkom utanför vägggeometrin eller försvann jämfört med start-ROM:en. Skillnaderna finns som koordinatlistor i `evidence/brief/rgb-delta.json`.

## Raster, CPU, RAM och spelprov

- **PASS i mätprofilen:** 16 384 byte, standard F6/NTSC och 600 sammanhängande bildrutor med exakt 262 scanlines, inklusive skiften mellan grafikrutter. Logikbank 1 är byteidentisk med start-ROM:ens.
- Gopher-debuggern stannade före RESP1 på SL133 c44, före late HMOVE på c70 och före följande WSYNC på c73. Nästa rad (SL134) kom in vid c3, började ladda SF:s GRP1 vid c29 och nådde följande WSYNC vid c73. Den trecykliga WSYNC ger c76 totalt på den vägen. Standardvägen vid X148 mättes till c75 inklusive WSYNC. Faser för VBLANK, synlig kärna och overscan finns i `evidence/brief/stage.jsonl`.
- Gopher läste SP=$F7 i kollisionens djupaste provade anropskedja. 120 arbetsbyte + högst 8 stackbyte i den granskade kedjan ger 128/128 RIOT-byte. M1-vägen använder en tidigare oanvänd RAM-position och befintlig kölagring.
- **PASS:** Den joystickstyrda rundan i Gopher gick från kallstart via skott, golvnyckel, upptagning och upplåsning till faktisk högerpassage, **210 poäng och tre liv**. Inga RAM-skrivningar användes i denna runda. Stock Stella 6.7.1 och 7.0 körde samma ROM med tangentstyrning. Bildpixelmatrisen och 600-bildruteprovet avser Gopher. Fysisk Atari är **NOT_RUN**.

## Tekniska alternativ som kasserades

| Variant | Observerad begränsning |
|---|---|
| Obegränsad tidig M1/HMOVE | SF 600/600, men SM delvis felaktig i 20 bilder, 20 bilder med extra vitt och skadade spelarpixlar i överlappningsprovet. |
| Tidig M1/HMOVE med spelarskydd | 585/600 exakta femmaskersbilder och 0 extra vitt, men HMOVE-blankningen tog bruna vänsterväggspixlar. |
| RESP1 utan HMOVE | Synlig P1-kropp hamnade på X78 när det begärda intervallet var X72–77. |
| Sen HMOVE utan positionskompensation | P1 flyttades åtta pixlar åt vänster. En korrigering för P1 utan HMP0-korrigering rubbade den redan positionerade spelaren. |
| Sen kompenserad HMOVE med vidare X-domän | X79–80 gav fel i SF:s mask, med vita extrapixlar i 12 bilder. Den publicerade domänen slutar vid X78. |

Bygg med DASM enligt [README.md](README.md). [Råprotokoll och originalbilder](evidence/raw.tar.gz), [läsbara loggar](evidence/brief), [Stella-video](evidence/stella-play.mp4) och [negativa prov](evidence/negative) hör till samma leverans.

**G5_FORMAL_OPEN kvarstår. INDEPENDENT_VERIFICATION=NOT_RUN.**
