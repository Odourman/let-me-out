# TO_MAIN_V02_TOP_BOTTOM_DOOR_TRIAL

**Två körbara test-ROM:ar med fungerande kollisionsgrind och joystickutgång. R3-pixelkravet och full grafikregression är FAIL.** Fryst spelbas `8177c09368721988debb5407d8ffc2ed4bf4d94e`, SHA-256 `f4ec909d57c583bc4cd58caa8550e6ff3f7a261a9f74f00156303c478fdd5b31`. Den senare mottagningen tillämpades som teknisk startpunkt. [Arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643) · [Fryst basbeslut](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753)

| ROM, 16 384 byte F6/NTSC | SHA-256 |
|---|---|
| `let-me-out-v02-door-top.bin` | `8b95313f8a02d7ba6bd1ab04a792a542c25ccaf7ff415c8f827e52f071e61891` |
| `let-me-out-v02-door-bottom.bin` | `cd351628b8432263462944da0d832381b5efc56ce3c7c6689d024cbcbc4a7dfb` |

## Kollisions- och pixelorakel

Provgeometrin har en 32 pixlar bred öppning X64–95, åtta rader hög. Hela spelarens 8-pixlars bredd måste rymmas i öppningen. Den frysta kartans inre geometri bevaras, och högerkanten är nu en vanlig vägg. I båda ROM:arna stoppade den valda ytterväggen spelaren utan nyckel. Med nyckel, den gamla högerutgången, rätt vägg med fel X och motsatt yttervägg förblev stängda i särskilda joystickprov. Upplåsning, öppen väntan och fysisk förflyttning in genom öppningen provades separat. Den övre provvarianten registrerar utpassage vid Y0, den nedre vid Y168. Inga slutspelsformat eller karttilldelningar har antagits.

- **Topp:** Spelbar passage **PASS**. Vid öppet läge är alla 256 pixlar i X64–95/Y15–22 bakgrundssvarta på Gophers originalbild och all omgivande kant-PF brun. I låst läge räknas 232 orange pixlar inne i öppningen och 80 utanför inom samma band. Inga orange pixlar finns på någon annan rad.
- **Botten:** Spelbar passage **PASS**. I det öppna provet är 254 av 256 aperturpixlar svarta. Två gula rester på (75,183) och (80,183) kommer från den föregående spelarraden. Omgivande kant-PF är brun. I låst läge räknas 230 orange pixlar inne i öppningen och 80 utanför inom samma band. Inga orange pixlar finns på någon annan rad.
- **Exakt R3-nyckelhål FAIL för båda.** PF2:s nollbit låter svart bakgrund synas genom en åtta pixlar bred speglad utskärning på tre rader. R3 kräver en eller två pixlar i sina utskurna rader. PF:s fyrklockors bitupplösning och de använda COLUPF-skrivningarna gav också orange spill på kantväggen i låst läge. Försöken använder P0/P1 för vanliga spelobjekt där de är synliga. Någon separat svart sprite används inte. Provoraklet redovisar skillnaden, och den grova formen är inte en canonändring. [R3-källa](https://github.com/Odourman/let-me-out/blob/82667dae033f70570dce903f8e1d4866528be02a/rom/v018/tools/build.py)

## Resurser, spelrunda och regression

| Utfall | Fryst högerdörr | Topprov | Bottenprov |
|---|---:|---:|---:|
| Fem exakta masker utan extra vitt, standard | 595/600 | 595/600 | 595/600 |
| Helt osynliga NPC i standardprovet | 0 | 0 | 0 |
| Kallstartsnyckel | 65/65 | 65/65 | 65/65 |
| Nyckel med aktivt skott | 14/14 | 14/14 | 14/14 |
| Nyckel i spelarens rasterband | 0/14 | 0/14 | 0/14 |
| Fem NPC på samma Y86 | 2/5 | 2/5 | 2/5 |
| Enpixelsskott i det tidigare dörrbandet | 10/10 | 9/10 | 9/10 |
| Joystickrunda från kallstart, utan RAM-POKE | 210p / tre liv | 210p / tre liv | 210p / tre liv |

M (0), F, SM och SF är kompletta i alla 600 standardbilder. M (1) är komplett i 595. Båda varianter ger en extra gul skottpixel vid X12 i ett riktat prov. RGB-jämförelsen på identiska standardbilder, inom den gemensamma inre rektangeln, gav i varje variant 180 ändrade gula bilder (2 174 gula pixelkoordinater förlorade, 2 168 tillkomna), inga ändrade vita koordinater och 2 704 återkomna bruna pixlar i det jämförda området, utan brun förlust där. Den integrerade sidovägens grafik är därför historisk regressionsreferens. Gamla högerdörrens 48/48-orakel och den frysta väggcheckpointens 80/96 avser annan yttre geometri. De användes inte som ett pixel-PASS för dessa två prov.

Båda slut-ROM:ar körde 600 sammanhängande Gopher2600 v0.57.2-bilder med **262 scanlines**. Debuggern uppmätte COLUPF före skrivning vid CL52 och CL94 i låsta kantlinjen och WSYNC vid CL148 (c72 före den trecykliga skrivningen). I öppet läge nådde kantvägen WSYNC vid CL151 (c73) och därmed c76 inklusive instruktionen. Vid X148 kom den vanliga setupvägen också till WSYNC vid c72. Den bevarade sena väggvägen mättes upp till c76 inklusive WSYNC. Kollisionsspåret gav SP=$F7 och 128 RIOT-byte inklusive stack. Stock Stella kördes med verklig tangentinput, 6.7.1 för toppen och 7.0 för botten. Fysisk Atari är NOT_RUN.

I det tidigare högerdörrsbandet, SL138–140, flyttades uppmätt WSYNC från CL112 till CL94. Det ger **sex CPU-cykler mer marginal per uppmätt rad** när den ordinarie spritevägen används. Dörren tar där ingen P0/P1-plats. Det räcker i det provade schemat inte för en tredje komplett NPC på samma Y eller för nyckeln i spelarens band. M (1):s fem överlappningspixlar och återstående vägg- och spelarfel är fortsatt öppna.

## Kasserade varianter och framtida former

Första kantloopen gav 274 scanlines i båda varianter. En senare bottenloop gav 263 innan sista kantlinjen synkades direkt. En annan iteration tolkade specialrader som dörrar och lade orange utanför den enda avsedda kanten. Nästa återställde split-rader och SF:s M1-aktivering. Den kasserade öppningsfärgen gjorde den mörka öppningen för bred genom att även släcka angränsande väggfärg. Slutproven lämnar väggen brun runt öppningen. De visar testbar passage och mätt rastermarginal, med grafikkraven fortsatt öppna.

Den rådgivande formanalysen är i `FUTURE_NPC_FORMS.md`. En 8-bitars RNG kan inte nå alla 1 024 ordnade maskkombinationer enbart från ett rumstillstånd. Ingen formslumpning eller flerrumsimplementation har lagts i ROM:arna.

[Bygg och återkör](README.md) · [Mätprotokoll](evidence/brief) · [Råloggar och originalbilder](evidence) · [Kasserade prov](evidence/negative)

**DEVELOPER_OBSERVED · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
