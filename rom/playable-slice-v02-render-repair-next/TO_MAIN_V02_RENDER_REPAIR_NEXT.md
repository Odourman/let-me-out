# TO_MAIN_V02_RENDER_REPAIR_NEXT

**Spelbar V02-checkpoint med förbättrade fiendemasker och synlig golvnyckel i det provade skottfallet.** Startcommit `3486b07347c5bae5728d85dc0acb0b01214b37de`, ROM SHA-256 `23b925a4b9f469ef25a23713079c90f6458ac9e6b3cf78c6b21d197f5e58f704`. Ny ROM SHA-256 `51e85c7787483927ff3ca0924cdcd3b10e311b7fe44916ccc3f26ee874732800`. [MAIN:s arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7009917916)

| Mätning | Fryst start-ROM | Ny ROM |
|---|---:|---:|
| Fem kompletta originalmasker utan extra vitt | 520/600 | **549/600** |
| Bildrutor med minst en utebliven fiende | 59/600 | **46/600** |
| Bildrutor med vita extrapixlar | 21/600 | **0/600** |
| Längsta fysiska frånvaro för SF | 49 | **46 bildrutor** |
| Exakt kallstartsnyckel under loggad golvtid | 65/65 | **65/65** |
| Fryst nyckelprov med aktivt skott | 0/14 | **14/14 +0 extra** |
| Fryst nyckelprov där spelaren använder bytesbandet | 0/14 | **0/14** |
| Exakta skottpixlar i dörrbandets X-fixturer | 10/10 | **10/10** |
| Standard-PF, saknade/extra bruna pixlar | 8/0 | **8/0** |
| Låst orange, öppen mörk, passage | Verifierat i prov | **Verifierat i prov**. Svart nyckelhål återstår. |
| Kallstartsrunda utan POKE | 210 poäng, tre liv | **210 poäng, tre liv och faktisk passage** |

## Samma 600 bildrutor, verifierade originalpixlar per individ

Varje cell anger **komplett mask / helt osynlig / längsta följd helt osynlig**. De fem individerna positionerades med sina vanliga, fria RAM-X/Y. Logikbanken jämfördes byte för byte.

| Individ | Start-ROM | Ny ROM |
|---|---:|---:|
| M (0) | 600 / 0 / 0 | **600 / 0 / 0** |
| M (1) | 590 / 10 / 10 | **595 / 0 / 0** |
| F | 600 / 0 / 0 | **600 / 0 / 0** |
| SM | 579 / 0 / 0 | **600 / 0 / 0** |
| SF | 551 / 49 / 49 | **554 / 46 / 46** |

Bortfallen för M (1) började när dörrbandets första rad behandlades som en PF-geometriövergång. Efter justeringen kan P1 positioneras intill dörrens början. Den fasta PF-geometrin hämtas från samma kartdata. M (1) saknar en vit pixel i var och en av fem bilder. På de exakta koordinaterna lästes gult RGB 255/255/41 från spelarens befintliga bild. Ett kortare P0-byteskrav för nedre objekt återvann tre bilder för SF och behåller det större skyddet för P1:s egna senare förberedelser.

Tidigare GRP1 i dörrbandet reparerade SM:s 21 partiella bilder. Ett obegränsat byte av GRP-ordning försämrade spelarprovet från fyra saknade och noll extra gula pixlar till 13 saknade och 15 extra. Den levererade F6-ROM:en väljer under VBLANK mellan två adresseringsidentiska grafikbanker med olika GRP0/GRP1-ordning. Spelarens band väljer P0 först och återställde fixturen till fyra saknade och noll extra. P1-kalibreringen på X32, utanför spelarens dörrband, gav nu noll differens.

Fem NPC på Y86 ger fortfarande bara två kompletta originalmasker. Fixturen med två små fiender på samma Y kan visa båda komplett när P0 är ledig, men en annan mask i bilden är partiell. När spelaren och skottet konkurrerar om P0/M0 lämnar den aktuella vertikala kärnan ingen generell tredje spriteplats. De 46 SF-bortfallen och den täta fixturen kvarstår som **FAIL**.

## Nyckel, dörr och PF

Nyckelns P0/P1-byte med aktiv projektil är tillåtet när projektilens Y ligger helt efter bytet och därför behåller spelarens gula färg. I den frysta fixturen på (120,160) återgavs nyckeln med 14 rätta pixlar och 0 extra samt 262 scanlines. Spelaren och skottet hade noll saknade gula pixlar och två extra i hela provbilden. När spelaren själv upptar bytesbandet saknas plats för den lilla fienden på P0, och nyckeln har fortfarande 0/14 pixlar. Kontrollerad golvnyckel och alla 65 loggade kallstartsbilder gav 14 rätt och 0 extra.

Dörrens högra fyra pixlar per rad förblir orange i den låsta fixturen och mörka efter upplåsning. Ett separat M1-prov finjusterade positionen till ett centrerat svart fält med orange på båda sidor. Provet gav **268 scanlines** och den vita P1-masken tappade pixlar. Det finns därför inget integrerat svart nyckelhål i checkpointen. En separat X64-fixtur flyttade fyra väggpixlar från orange till brunt på P1:s förberedelserad, men skadade originalmasken (2/28 rätt, 26 extra). Fyra mörka pixlar på HMOVE-raden återstod också. Därför kvarstår åtta saknade standardpixlar i checkpointen.

## Reproduktion och hårdvara

Bygg med DASM 2.20.14.1 enligt `README.md`. Ny binär är standard F6/NTSC med 16 384 byte. Bank 1 är byteidentisk med start-ROM:ens spellogik. Bank 2 använder den andra GRP-ordningen och återgår genom samma F6-hotspots. Gopher2600 v0.57.2 mätte 600 sammanhängande bildrutor med 262 scanlines och spelrundan från riktig joystick. X148-fasen gav c75 inklusive WSYNC och källberäknad största stödda väg är c76. SP=$F7 i djupaste uppmätta spelvägen, vilket ger 128/128 RIOT-byte inklusive åtta stackbyte. Stock Stella 6.7.1 och 7.0 körde ROM:en med tangentinput. Bilder och video ingår. Långprovet och pixelmätningarna ovan avser Gopher. Fysisk Atari är **NOT_RUN**.

Korta protokoll ligger i `evidence/brief`. Originalbilder, inspelning och råloggar finns i `evidence/images`, `evidence/stella-play.mp4` och `evidence/raw.tar.gz`. Kasserade prov ligger i `evidence/negative`.

**G5_FORMAL_OPEN kvarstår. Oberoende VERIFICATION II är NOT_RUN.**
