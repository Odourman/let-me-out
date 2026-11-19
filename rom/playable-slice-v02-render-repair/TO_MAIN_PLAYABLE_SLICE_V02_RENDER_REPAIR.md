# TO_MAIN_PLAYABLE_SLICE_V02_RENDER_REPAIR

**Spelbar V02-checkpoint med reparerad kallstartsnyckel och bättre fiendegrafik.** Standard F6/NTSC, 16 KiB. Startcommit `e7e15b90d9ced6cee32df74dbbe954880384e750`, verifierad ROM SHA-256 `d1b7c117a3838bdaa3f4cd2f6ac0cd20bd5580cba2ce48f1b768e72f5ae3a153`. Ny ROM SHA-256 är `23b925a4b9f469ef25a23713079c90f6458ac9e6b3cf78c6b21d197f5e58f704`. Fullständigt manifest finns i `SHA256SUMS`. [MAIN X:s order och verifierade föregående resultat](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7008884707)

| Test | Fryst V02 | Föregående fortsättning | Grafikreparation |
|---|---:|---:|---:|
| Minst en utebliven fiende, samma 600-ramsprov | 247 | 84 | **59** |
| Fem fullständiga, pixelkorrekta originalmasker utan extra vita pixlar | 36/600 | 158/600 | **520/600** |
| Bildrutor med extra vita pixlar | 394/600 | 432/600 | **21/600** |
| Exakt kallstartsnyckel under uppmätt golvtid | 0/65 | 39/65 | **65/65, 14 pixlar, 0 extra** |
| Exakt kontrollerad golvnyckel | 14 rätt + 4 extra | 14 rätt + 0 extra | **14 rätt + 0 extra** |
| Bruna standardväggen, dörryta undantagen | 8 saknade / 0 extra | 8 / 0 | **8 / 0** |
| Låst orange, öppen mörk, korrekt passage | Ja | Ja | **Ja** i de provade fallen, svart nyckelhål återstår |
| Exakt M0 i tio X-prov i dörrbandet | 5/10 | 10/10 | **10/10** |
| NTSC-långprov | 262 × 600 | 262 × 600 | **262 × 600** |
| CPU i profilerad kantväg / källräknat tak | 75 / 76 | 75 / 76 | **75 / 76 cykler** inklusive WSYNC |
| RIOT inklusive stack | 125/128 | 128/128 | **128/128**, stack SP=$F7 i djupaste provade spelväg |
| Joystickrunda från kallstart utan POKE | 210 poäng, tre liv | 210 poäng, tre liv | **210 poäng, tre liv, faktisk passage** |

## Per individ

Varje cell anger **kompletta, helt osynliga, längsta fysiska frånvaro**, i bildrutor. Pixeljämförelsen använder originalmaskerna och RAM-positionerna för den färdiga emulatorbilden.

| Individ | V02 | Föregående fortsättning | Grafikreparation |
|---|---:|---:|---:|
| M (0) | 580, 0, 0 | 479, 0, 0 | **600, 0, 0** |
| M (1) | 550, 10, 10 | 590, 10, 10 | **590, 10, 10** |
| F | 527, 0, 0 | 600, 0, 0 | **600, 0, 0** |
| SM | 457, 0, 0 | 426, 0, 0 | **579, 0, 0** |
| SF | 353, 247, 211 | 526, 74, 74 | **551, 49, 49** |

De stora M (0)- och SM-felen koncentrerades till de logiska rasterraderna 69, 64 och 144. Tidigare GRP1 på bytesraderna och på PF-övergångarna återställde maskpixlarna. Det nya P0-bytesfönstret på Y104 kan ge plats åt en liten NPC över spelaren när resten av raden är fri. Samma RAM-läge väljer samma renderingsplan. De återstående 21 bildrutorna med vitt utanför maskunionen är långprovets sista 21, med SM-fel på logiska Y84–86 i dörrbandet. Tidig ENAM0-nollställning där bevarar skottets enpixelresultat, och GRP1/P0-delningen har fortfarande vänsterlägesfel inklusive den isolerade X32-regressionen.

I det separata provet med fem på Y86 visas fortfarande bara två av fem originalmasker. De två små maskerna på samma Y kan båda vara kompletta när P0 är ledig, medan en annan mask i den fixturen fortfarande har saknade pixlar. Prov med spelaren eller skottet i samma band har också kvar mask- och spelarartefakter. Därför är den generella femfiendersgrafiken **FAIL**.

## Golvnyckel och sex samtidiga objekt

När förhållandena tillåter det använder den lilla fienden P0 före spelaren och nyckeln P1. GRP1 matas på de tre rasterrader då P0 flyttas. Den faktiska Gopher-rundan innehåller **65/65 exakta golvbilder**, inklusive de tidigare 26 osynliga. Den lilla fienden och nyckeln behåller sina separata originalkoordinater. Det isolerade nyckelprovet behåller 14 rätt och 0 extra.

Det separata frysta fem-live-provet med SM på (59,148), nyckeln på (85,153) och spelaren på (60,159) visade **14/14 +0** för nyckeln, synliga pixlar för alla fem och 262 scanlines. SM hade 16/20, den andra M 23/28 och bilden tio extra vita pixlar. Den vägen är geometriavgränsad till det nedre bytesfönstret. Frysta motprov med aktivt skott eller spelaren inne i bandet har fortfarande **0/14** nyckelpixlar. Gopher-kallstarten använder joystick utan POKE. Koordinatfixturerna använder POKE för att etablera scenen.

Fem-live-fixturen fångade först planering som passerade RIOT-timerns nollfönster och gav 344 respektive 147 rader i två övergivna byggen. Färre uppslag och tre omfördelade tomrader gav VBLANK marginal med oförändrad roomstart SL44. Bytejämförelse visar att spelbankens 4 KiB är identiska med föregående checkpoint.

## Dörr och PF

Högerfältet har 128/128 orange pixlar när dörren är låst och 128/128 mörka när den är öppen före passage i referensfixturerna. Utan nyckel stannar spelaren vid X148. Fortsättningens M1-probe med omplacerad strob placerade två mörka pixlar i dörrfältet i sex rader. Provet gav **267 scanlines**, och färgen delades med P1 så den högra NPC-masken tappade vita pixlar. Det blev varken ett användbart nyckelhål eller en integrerad spelvariant.

Vänsterkantens fyra pixlar på P1:s förberedelserad är fortfarande orange och fyra på första HMOVE-raden är mörka i standardfixturen. I det avgränsade X64-provet försvann det mörka HMOVE-strecket när stroben flyttades sent, men färgen blev orange och originalmasken gick från 28/28 till **1/28, 27 extra**. Det sena alternativet kasserades. Ytterligare dynamiska PF-fel kvarstår.

## Körda verktyg och underlag

X148-provet stannade vid CL148 före WSYNC, c72 från radstart och c75 inklusive skrivningen. För den nya nyckelvägen återanvänds tre positioneringsiterationers 15 cykler för att skriva P1-byten medan P0 positioneras. Den längsta stödda övre gränsen är spelar-X123. Gophers fasprov vid gränsen finns i `evidence/brief/key-assist.jsonl` och den oförändrade väggkollisionens SP=$F7 i `evidence/brief/stage.jsonl`. Aktivt raster använder 120 RAM-byte till och med $F7, medan åtta stackbyte upptar $F8–$FF i det djupaste uppmätta spelprovet.

DASM 2.20.14.1, Gopher2600 v0.57.2 och stock Stella 6.7.1/7.0 användes. Gopher loggade det sammanhängande 600-ramsprovet och riktig joystickrunda samt läste 6507:s stack och TIA-faser. Reproducerbara kommandon och versioner finns i `README.md` och `evidence/brief/tools.txt`. Stella kördes med tangentinput och original-PNG samt video från 6.7.1 ingår. Den fulla pixelmatrisen och scanlineresultaten avser Gopher. Fysisk hårdvara och oberoende Verification II är **NOT_RUN**.

**G5_FORMAL_OPEN kvarstår.** MAIN X mottagningsgranskar den spelbara checkpointen.
