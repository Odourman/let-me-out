# TO_MAIN_V02_BROWN_PF_DOOR_BLACK_OUTLINE_TRIAL

**Två spelbara, isolerade V02-test-ROM:ar med brun PF-dörr, negativ kontur och negativt nyckelhål.** Fryst startcommit `4c4fc5b7c5545217b2321a38d9db6db5dac7db2f`. [MAIN XI:s aktuella arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7038233205)

| Standard F6/NTSC, 16 384 byte | SHA-256 |
|---|---|
| `let-me-out-v02-brown-door-top.bin` | `556bd762246f5f0fa1dde32d843bf8eaf5583dbc0d2a67ce575af01036fd964e` |
| `let-me-out-v02-brown-door-bottom.bin` | `f74c7ce58c52a663fb6a6620eb98bb7d1c7777baca261a4f2a33f2a85a65b6b5` |

## Dörrgrafik och fysisk passage

- **PASS i Topp och Botten.** Dörren och väggarna har samma bruna RGB 199/107/33. Speglad PF2 lämnar kontur och nyckelhål svarta genom nollbitar. Det svarta huvudet är 16 pixlar brett och två rasterrader högt. Stammen är åtta pixlar bred och två rasterrader hög. De låsta bilderna matchar hela det bruna och svarta kantoraklet utan extra pixlar eller orange spill. Varken missil eller playersprite behövs för dörren.
- **PASS i öppet läge.** Aperturen X64–95 innehåller **256/256 svarta pixlar i båda ROM:arna** och omgivande kantvägg är pixelrätt. De två tidigare gula pixlarna på (75,183) och (80,183) i bottenprovet är borta. P0:s rad skrivs tidigare när färgbytena försvinner.
- **PASS för kollision och spelrunda.** Spelaren stoppas i mitten och vid de båda provade kantlägena X64 och X88 före nyckel. Den gamla högerkanten, fel X och motsatt yttervägg förblir stängda även med nyckeln. Separata kalla joystickspel utan RAM-POKE gav verkligt nyckelfall, upptagning, upplåsning och utpassage med **210 poäng och tre liv**. Kallstartsnyckeln mättes pixelrätt i 65/65 golvbilder på vardera vägen.
- En andra toppmask med en ensam 16-pixels huvudrad byggdes och speltes. Den gav en tunnare silhuett. Tvåradershuvudet valdes för att skilja huvud och stam tydligare i verklig emulatorbild. Originalbild och binär av den alternativa masken finns bland negativa prov.

## Hårdvara och regression

Den uppmätta kantvägen når WSYNC vid CL115 (c61) i låst läge och CL118 (c62) i öppet läge. Med tre cykler för skrivningen är det **c64/c65**, en besparing på **elva CPU-cykler per uppmätt kantrad** jämfört med motsvarande orange prov c75/c76. TIA-spåret visar PF2 och GRP0. Kantvägen har inga COLUPF-skrivningar. De befintliga maximala 76-cykelsvägarna kvarstår utanför kanten. Djupaste uppmätta stackposition är SP=$F7, åtta stackbyte inom 128 RIOT-byte. Båda ROM:arna körde 600 sammanhängande Gopher2600-bilder med **262 scanlines** och kördes med tangentinput i stock Stella (6.7.1 topp, 7.0 botten).

| Prov | Topp | Botten |
|---|---:|---:|
| Fem kompletta masker utan extra vitt | 595/600 | 595/600 |
| Någon NPC helt osynlig i standardprovet | 0/600 | 0/600 |
| Kallstartsnyckel | 65/65 | 65/65 |
| Golvnyckel med aktivt skott | 14/14 | 14/14 |
| Golvnyckel i spelarens band, inklusive separat X | 0/14 FAIL | 0/14 FAIL |
| Fem NPC på Y86 | 2/5 FAIL | 2/5 FAIL |
| Enpixelsskott | 9/10 FAIL | 9/10 FAIL |

Den inre RGB-jämförelsen mot respektive orange prov gav samma gula, vita och bruna pixlar i det gemensamma jämförelseområdet under alla 600 standardbilder. M (1):s fem partiella standardbilder och kända inre PF-fel kvarstår. Det riktade X12-provet har fortfarande en extra gul skottpixel. En spelbar kontrollvariant med tidigare ENAM0-nollställning fick 10/10 skott men försämrade M (1) i nyckel- och skottfixturen från 23/28 till 18/28 vita pixlar. Den ändringen kasserades. Tidsvinsten vid kanten löser inga separata objektkonflikter i inre rasterband. Fysisk Atari är NOT_RUN.

[Bygg- och testkommandon](README.md) · [Mätprotokoll](evidence/brief) · [Originalbilder och råprotokoll](evidence) · [Kasserade prov](evidence/negative)

**DEVELOPER_OBSERVED · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
