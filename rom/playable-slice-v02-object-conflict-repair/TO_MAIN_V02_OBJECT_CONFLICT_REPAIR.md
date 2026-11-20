# TO_MAIN_V02_OBJECT_CONFLICT_REPAIR

**Spelbar V02-checkpoint, BOUNDED_WALL_PROGRESS / OBJECT_CONFLICT_FAIL.** Startcommit `a1b4449fe92fb8045f6f88f040c7f94be03e2ffb`, start-ROM SHA-256 `03bcd638fb93fff088b5cb9ddc069f0dfe4c9604e436406877ae736ab510bf52`. Ny ROM SHA-256 `f4ec909d57c583bc4cd58caa8550e6ff3f7a261a9f74f00156303c478fdd5b31`. [MAIN XI:s arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7035920560)

## Integrerad väggreparation

Den sena HMOVE-vägen kan nu arbeta utanför dörrbandet när den befintliga plansorteraren lämnar ett stabilt PF-intervall. Förberedelsen väljer brun eller orange högerfärg före rasterstart. Den vanliga ritvägen återställer HMP0 före nästa HMOVE så att spelarens X behålls. En tidigare kandidat lämnade HMP0 kvar mellan figurerna och försköt gula pixlar, vilket syns i den kasserade RGB-loggen.

| Mätning | Fryst start | Ny ROM |
|---|---:|---:|
| Ursprungliga väggfixturer X63–78, Y77/90/100 | 48/48 | 48/48 |
| Ytterligare Y40/130, X63–78, exakt vägg och NPC | 0/32 | 32/32 |
| Brunpixelsfel, låst dörr | 40 | 36 |
| Brunpixelsfel, öppnad dörr före passage | 58 | 58 |
| Brunpixelsfel, kallstartsnyckel | 16 | 16 |
| Fem kompletta originalmasker utan extra vitt | 595/600 | 595/600 |
| Någon NPC helt borta i standardprovet | 0/600 | 0/600 |
| Kallstartsnyckel exakt | 65/65 | 65/65 |
| Aktivt skott och golvnyckel | 14/14 | 14/14 |
| Spelare i samma Y-band, båda X-fixturer | 0/14 | 0/14 |
| Fem NPC på Y86 | 2/5 | 2/5 |

RGB-jämförelsen visar fyra återställda bruna pixlar i vardera 272 standardbilder (1 088 sammanlagt), noll förlorade bruna pixlar samt samma gula och orange koordinater i alla 600 bilder. Alla tio skottproven klarades. På Y160 minskade brunpixelsfelen från sex till två i alla 16 prov, med exakt NPC-mask.

## Kasserade fysiska prov

- **R3 negativ grafik, två PF-prototyper.** R3:s `$66` har två separata orange segment och en tvåpixelsöppning. `$76` har en enpixelsöppning. Registerprovet som släckte högerfärgen behöll bara 80 orange pixlar i högerkantens fyrpixelsband och gav 294 scanlines. Det andra provet ändrade PF0-biten på högersidan efter att vänsterdelen passerat och återställde den på nästa rad. Det behöll 68 orange pixlar i samma band och gav 282 scanlines. Reflekterad PF0 ger här ett helt fyrpixelfält. En tät serie normala nollsidesskrivningar har minst nio färgklockor mellan skrivningarna, mot en eller två för öppningen. Det blockerar denna PF-metod och lämnar det exakta R3-målet öppet. Den levererade låsta dörren har fortsatt 128 orange högerkantspixlar. [R3-original](https://github.com/Odourman/let-me-out/blob/82667dae033f70570dce903f8e1d4866528be02a/rom/v018/tools/build.py)
- **Sen P1-omställning efter SM.** Kasserad kandidat läste första guldraden via bitmappekaren efter att SM:s kritiska tid reserverats. Den gav 9/14 guldpixlar utan extra guld i båda spelarfixturerna vid 262 scanlines. Separerad X behöll SM:s 20/20, medan samma-band-provet gav 9/20 SM mot startens 10/20. De två första guldraderna upptar X86–88 och ligger bara 21–22 fria färgklockor efter SM:s sista pixel i samma rader. RESP1, GRP1 och COLUP1 tar redan 27 färgklockor i den direkta sekvensen.
- **Reserverad P1-plats för nyckeln.** Kasserad omprioritering gav 14/14 utan extra guld i båda spelarfixturerna men tog bort SM:s samtliga pixlar. Den höll 262 scanlines. De två försöken visar separat vad en fullständig slot och en senare omställning fysiskt kan återge. Exakt nyckel tillsammans med övriga objekt återstår.
- **Fem på samma Y och M (1).** Den integrerade kärnan visar F och SF komplett på Y86. Den behåller fem logiska NPC. Den tidigare radanalysen gäller fortfarande, inklusive 21–22 fria färgklockor mellan tända maskintervall på Y90, där två förladdade skrivningar förbrukar sex CPU-cykler före positioneringsmarginal. Ingen komplett flerobjektskernel byggdes i denna iteration. Fem av M (1):s vita pixlar är fortsatt täckta av gult i standardprovet.

## Hårdvarubudget och spelrunda

Utvecklarprov med DASM, Gopher2600 v0.57.2 och stock Stella. Spel-ROM standard F6/NTSC, 16 384 byte, byteidentisk logikbank. Den uppmätta bryggan går till WSYNC vid c73 och använder högst c76 inklusive instruktionen. Debuggerns djupaste mätta SP=$F7 ger åtta stackbyte inom 128 RIOT-byte. Gopher gav 262 scanlines i alla 600 standardbilder. En riktig joystickstyrd kallstartsrunda slutfördes utan RAM-ingrepp med 210 poäng, tre liv och fysisk högerpassage. Stock Stella 6.7.1 och 7.0 körde samma binär med tangentinput. Fysisk Atari och oberoende verifiering är NOT_RUN.

[Byggkommandon](README.md) · [Mätprotokoll](evidence/brief) · [Råloggar och originalbilder](evidence/raw.tar.gz) · [Kasserade prototyper](evidence/negative)

**DEVELOPER_OBSERVED · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
