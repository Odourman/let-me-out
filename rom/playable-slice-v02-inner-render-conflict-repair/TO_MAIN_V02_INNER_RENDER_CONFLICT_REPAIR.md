# TO_MAIN_V02_INNER_RENDER_CONFLICT_REPAIR

**DEVELOPER_OBSERVED — integrerad, avgränsad PF-reparation.** Både TOP och BOTTOM från den frysta bruna V02-basen är spelbara. Vid P1 X60–62 kan reservfasen lägga RESP1 fyra CPU-cykler tidigare och behålla sena HMOVE. Reservfasen är begränsad till köer vars första P1-slot ligger till vänster om den etablerade fasens X63–78-band. En hel andra kögenomsökning hamnade utanför VBLANK-budgeten i dörrprovet. Båda varianterna återställer de bruna pixlarna X0–3 på Y86 i låsfixturen. Ingen ändring av vit eller gul grafik i den bilden. PF-felet är kvar i andra rader och tillstånd.

| Prov | Fryst bas | Ny TOP och BOTTOM | Status |
|---|---:|---:|---|
| Inre bruna PF-pixlar saknas, låst/öppen/kallstartsnyckel | 20/20/16 | 16/20/16 | Låst förbättrad, övriga FAIL |
| Exakta femmaskersbilder utan extra vitt | 595/600 | 595/600 | Regressions-PASS |
| Helt osynliga NPC i standardprovet | 0 | 0 | PASS |
| M(1) partiella standardbilder | 5 | 5 | FAIL |
| M(1) med skott/nyckel | 23/28 | 23/28 | Regressions-PASS, fortfarande partiell |
| Fem NPC på Y86, X20/44/68/92/116 | 2/5 | 2/5 | FAIL |
| Golvnyckel med spelare, delat rasterband | 0/14 | 0/14 | FAIL för både separerade X och in-band |
| Kallstartsnyckel, utan extra guld | 65/65 | 65/65 | PASS |
| Nyckel med aktivt skott, utan extra guld | 14/14 | 14/14 | PASS |
| Enpixelskott, ingen (12,106) | 10/10 | 10/10 | PASS |
| Brun låst dörr, svart kontur och nyckelhål | Pixelrätt | Pixelrätt, 160 svarta pixlar i öppningsytan | PASS |
| Öppen dörr | 256/256 svart | 256/256 svart | PASS |
| Kallstart med joystick utan RAM-ingrepp | 210 poäng, tre liv | 210 poäng, tre liv | PASS |

Gopher2600 v0.57.2 körde två separata profiler med vardera 600 sammanhängande bildrutor och 262 scanlines i varje. Alla 600 original-PNG:er per variant är byteidentiska med motsvarande PNG:er från den frysta standardsekvensen. DASM byggde två 16 384-byte F6-ROM:ar. Logikbankens samtliga 4 096 byte är oförändrade i vardera ROM. Registerspåret för X60 visar före skrivning RESP1 vid CL52, HMOVE vid CL142, WSYNC vid CL151 och följande GRP1-väg vid CL19. Med linjestart vid CL−68 ligger WSYNC vid c73 före skrivningen och vägen når c76 inklusive instruktionen. Kollisionsspåret visar SP=$F7, åtta stackbyte. Intilliggande RAM och stacklayout är oförändrade och ryms i 128 RIOT-byte. Stock Stella 6.7.1 för TOP och 7.0 för BOTTOM kördes med riktig tangentinput och originalbilder sparades. Full joystickrunda och kvantitativa pixelbevis är från Gopher2600.

**Positionssvep.** Gopher provade 114 koordinatpar per ROM: X60–78 och sex Y-nivåer. Alla NPC-pixlar stämde i 114/114, med 262 scanlines. Mot fryst TOP respektive BOTTOM återställdes fyra väggpixlar i 18 fall (72 pixlar per variant). Övriga 96 fall var oförändrade. Ingen vit, gul eller brun pixel förlorades i svepet. Den extra breakpointprofilen för BOTTOM fångade 174 händelser mot skriptets generella tröskel 175; råspåret och tröskelfelet finns i bevisen. Bildanalysen för standard, dörr och riktade prov kördes separat.

**Negativa prov.** Tvåobjektsplanen BOLL+M0 gav 0/14 rätt, 20 extra guldpixlar vid högra väggen, 3 saknade gula pixlar och 267 scanlines. Ett oberoende M1 för en del av F på Y86 gav 32/38 för F, 22/22 för SF, 0 för de tre övriga, 10 extra vita pixlar och 262 scanlines. Båda är kasserade och arkiverade med ASM-diff, ROM, originalbild och logg. M(1):s fem standardavvikelser sammanfaller med gula spelarpixlar på samma koordinat. Att ändra visningsprioritet skulle flytta avvikelsen till spelarens mask. Dessa observationer gäller de provade resursplanerna.

Fysisk Atari och oberoende verifiering **NOT_RUN**. **G5_FORMAL_OPEN. INDEPENDENT_VERIFICATION=NOT_RUN.**
