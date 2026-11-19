# TO_MAIN_V02_RASTER_REPAIR_NEXT

**Spelbar F6/NTSC-checkpoint. Resultatklass: BOUNDED_RENDER_PROGRESS / RENDER_FAIL.** Startcommit `58e54d6fd1673462671a466ccd21dd629cb97fe2`, start-ROM SHA-256 `c6ec4d8fd70dd233bb4fef9fefc62c5fa824ce7041b778884de3d43b36f589b5`. Ny ROM SHA-256 `2d2559671f8b920dc6849d1ec0d42da7f2a6dee42406a8531896b1a138cd7687`. [MAIN X:s arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7013044155)

| Gopher2600-prov | Fryst start | Ny ROM |
|---|---:|---:|
| Fem kompletta masker, inga extra vita pixlar | 585/600 | **595/600** |
| Bildrutor med en helt osynlig NPC | 10/600 | **0/600** |
| SF komplett / längst osynlig | 590/600 / 10 | **600/600 / 0** |
| M (0), F och SM kompletta | 600/600 var | **600/600 var** |
| M (1) komplett / partiell | 595 / 5 | **595 / 5** |
| Extra vita pixlar i standardsekvensen | 0/600 | **0/600** |
| Fem NPC på samma Y86 | 2/5 | **2/5 FAIL** |
| Golvnyckel från kallstart | 65/65 | **65/65** |
| Golvnyckel med aktivt skott | 14/14, +0 extra | **14/14, +0 extra** |
| Spelaren i nyckelns rasterband | 0/14 | **0/14 FAIL** |
| X64-PF, saknade/extra bruna pixlar | 8/0 | **0/0** |
| Enpixelsskott i dörrbandet | 10/10 | **10/10** |
| Orange låst dörr, mörk öppning och utpassage | PASS | **PASS** |
| Svart dörrnyckelhål | Saknas | **FAIL** |

Två spelarmaskrader förladdas under VBLANK och skrivs före P0:s vänstra pixelgräns. M1 behåller SF:s två första fyra pixlar medan P1 avslutar SM. Spelarfixturen på bryggraderna går från fyra till fem fullständiga NPC-masker utan extra vitt. Dess kvarvarande gula fel minskar från 15 saknade och 15 extra till 14 saknade och 12 extra. M (1) saknar fortfarande en vit pixel per felbild: (112,97) i fyra bilder och (117,97) i en. Samtliga koordinater har spelarens gula RGB i originalbilderna. Bilden kan bara visa en färg på de koordinaterna. De två godkända originalmaskerna finns kvar.

En separat väg återanvänder den sena HMOVE-fasen med M1 avstängd för en planerad P1-omställning, när samtliga aktiva objekt redan ryms och nyckel och skott är frånvarande. Kalibreringen täcker X63–70 och Y77, 90 och 100. Alla 24 kombinationer gav 262 scanlines, exakt NPC-mask och noll saknade eller extra bruna pixlar. Det frysta X64-fallet återfår båda radernas fyra bruna vänsterväggspixlar med P1-masken intakt. Den grövre väggen utanför den uppmätta domänen har fortsatt öppna dynamiska fel. I 11 bilder ändrades gult och varje ändrad bild fick färre fel mot spelarmasken. Bruna och orange pixlar var identiska i den jämförda standardsekvensen.

## Negativa emulatorprov

- Indirekta spelarmaskläsningar lade till en cykel vid sidgränsen och gav 264 scanlines. Förladdning i två redan allokerade byte löste cykelvariationen. En senare kandidat hade två bytes adressskillnad mellan speglade grafikbanker och flyttade spelarmasken. Bygget kontrollerar nu gemensamma symboladresser.
- En extra väg överbelastade VBLANK i provet med nyckel och skott (139 scanlines). Vägvalet flyttades bakom den redan befintliga kontrollen för skott/nyckel. Omprovet på den levererade ROM:en återgav 14/14 nyckelpixlar och 262 scanlines.
- Tidigare P1-överlämning i nyckelns spelarfixtur gav 14/14 guldpixlar men minskade SM från 10 till 6 av 20 vita pixlar och gav fyra extra gula pixlar. Samma prov bröt skottfixturen. Kandidaten kasserades.
- NUSIZ1 med två kopior i fem-samma-Y-provet gav fortfarande bara två fullständiga masker och 38 vita extrapixlar. En kopia repeterar samma maskbyte och lägger ingen självständig mask på den saknade NPC:ns koordinat.
- Svart M0-stencil visade en tvåpixlars öppning och en smalare mitt på det orange dörrfältet. Den låsta provsekvensen fick 274–275 scanlines och upplåsningen 273. Kandidaten kasserades.

## Budget och spelbarhet

Standard F6/NTSC, 16 384 byte. Logikbank 1 är byteidentisk med start-ROM:ens. 600 sammanhängande Gopher-bilder gav 262 scanlines. Båda bryggvägarna når WSYNC vid c73 och slutför den trecykliga instruktionen vid c76. Kollisionstestet uppmätte SP=$F7, alltså åtta stackbyte inom 128 RIOT-byte. Den joystickstyrda kallstartsrundan slutfördes utan RAM-skrivning med 210 poäng, tre liv och faktisk högerpassage. Stock Stella 6.7.1/7.0 körde ROM:en med tangentstyrning. Pixel- och timingresultaten gäller Gopher2600 v0.57.2. Fysisk Atari är NOT_RUN.

Se [bygg- och testkommandon](README.md), [läsbara mätprotokoll](evidence/brief), [råloggar och originalbilder](evidence/raw.tar.gz), [Stella-video](evidence/stella-play.mp4) och [kasserade kandidater](evidence/negative).

**G5_FORMAL_OPEN kvarstår. INDEPENDENT_VERIFICATION=NOT_RUN.**
