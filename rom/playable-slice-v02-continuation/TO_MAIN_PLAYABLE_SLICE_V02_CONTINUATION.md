# TO_MAIN_PLAYABLE_SLICE_V02_CONTINUATION

**Spelbar F6/NTSC-checkpoint med partiell grafikreparation.** Samma enrumsrunda och en byteidentisk logikbank. Fortsättningsgrenen är `rom-dev/playable-slice-v02-continuation-20261119`. V01/V02 ligger kvar på sina frysta refar. [MAIN X:s fortsättningsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7005343096)

Startcommit `56ca953a1125e86239db04ac80aa759b973b24b9` ger SHA-256 `8f5089545f412e80cb4930a48bb6d7cf3bec57fb9f112f2c355baaa38f07e65f` för V02-ROM:en. Jag räknade om SHA-256 från GitHub-blobben och jämförde med specialistmanifestet. MAIN X:s mottagningskommentar anger ett annat värde, med prefixet `8460fc52`. Fortsättnings-ROM:en har SHA-256 `d1b7c117a3838bdaa3f4cd2f6ac0cd20bd5580cba2ce48f1b768e72f5ae3a153`. [V02:s ursprungliga leverans](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7003129044)

| Prov | V01 | Fryst V02 | Fortsättningen |
|---|---|---|---|
| Minst en fiende utan renderingsplats i samma joystickföljd | 347/600 | 247/600 | **84/600**. Full synlighet **FAIL**. |
| Fem kompletta originalmasker, 0 extra vita pixlar | Ej mätt i alla 600 | 36/600 vid omkörning | **158/600** vid pixeljämförelse av samtliga 600. |
| Golvnyckel, kallstart | Osynlig i golvbilden | 0/65 synliga | **39/65 med 14/14 och 0 extra**, därefter 26/65 utan nyckelpixlar före upptagning. **FAIL** för visning under hela golvtiden. |
| Kontrollerad golvnyckel | 14 synliga | 14 rätt + 4 extra | **14 rätt, 0 extra. PASS** för fixturen. |
| Högerdörr | Ingen verifierad orange visning och öppning | Orange låst, mörk öppen. Svart hål saknas. | 128/128 högerpixlar orange låst, 128/128 mörka öppen före passage. Båda kontroller har 128/128 bruna vänsterpixlar. **FAIL** för nyckelhålet. |
| Bruna väggar, X64-fixtur utan dörrytan | 180 saknade / 84 extra | 8 saknade / 0 extra | **8 saknade / 0 extra. FAIL**. |
| Projektil i dörrbandets kalibrering | X−1 i 10/10 | 5/10 exakta enpixelprov | **10/10 exakta enpixelprov**, inklusive X12–56. |
| Riktig kallstartsrunda utan POKE | 210 poäng, tre liv | 210 poäng, tre liv | **210 poäng, tre liv. PASS**. |

## Fiender och golvnyckel

Vid platsbrist kan planeraren använda P0 för en utelämnad NPC på andra sidan ett rasterintervall där renderaren kan byta horisontellt läge utan att skriva över spelaren eller en aktiv M0. Tre möjliga rasterintervall väljs utifrån RAM-läget. Fienden använder sina vanliga RAM-koordinater och sin ursprungliga mask. Samma RAM-läge ger samma renderingsplan. SF ritades via P0 i 173 bildrutor i långtestet. En första fysisk variant fick P0 förskjuten när en tagen divisionsgren passerade en 6507-sidgräns. En tidigare variant gav 263 rader. Slutvarianten eliminerade båda felen i långtestet.

| Individ | Fryst V02 helt osynlig / längsta följd | Fortsättningen helt osynlig / längsta följd | Alla egna pixlar synliga, V02 → fortsättning |
|---|---:|---:|---:|
| M (index 0) | 0 / 0 | 0 / 0 | 580 → 479 |
| M (index 1) | 10 / 10 | 10 / 10 | 550 → 590 |
| F | 0 / 0 | 0 / 0 | 527 → 600 |
| SM | 0 / 0 | 0 / 0 | 457 → 426 |
| SF | 247 / 211 | 74 / 74 | 353 → 526 |

Vita pixlar utanför maskunionen fanns i 394/600 referensbilder och 432/600 fortsättningsbilder. Den förbättrade synligheten har därmed kvar pixelregressioner för M (index 0) och SM. I den isolerade dörrbandskalibreringen gick V02:s exakta P1-prov vid X32 tillbaka till 24 pixlars symmetrisk differens när ENAM0 nollställdes tidigare. X47–148 förblev exakta i de sju provpositionerna från X47. Senareläggning av ENAM0-nollställningen gav fortfarande dubbla skottrader i fyra positioner och lämnade fel vid X32. Den valda ROM:en prioriterar synliga hela fiender i den dynamiska serien och dokumenterar den kvarvarande rasterkonflikten.

I det frysta koordinatprovet med småmaskerna på samma Y86 och spelaren nedanför var båda småmaskerna fullständiga samtidigt, 20/20 och 22/22. De tre övriga figurerna hade synliga pixlar. Hela scenen är **FAIL** då en stor mask hade 23/28 och bildens vita union hade extrapixlar. I provet med alla fem på Y86 återgavs två av fem helt och tre saknades. När spelaren delar rasterbandet eller projektilen korsar det kan P0 behövas för spelaren och M0. Se koordinater och RGB-pixelprov i `evidence/brief/crowd.jsonl`.

P1-övergången till golvnyckeln förladdar föregående maskrad när Y-intervallen är skilda och RESP1 kan landa till höger om föregående objekt. Det lät SM:s sista rad ligga kvar samtidigt som nyckelns nya läge förbereddes i kallstart. Nyckelns position var (85,153) i hela mätningen. Från mätindex 39 trädde SM in på en faktiskt delad rasterrad vid separat X. Den nya enkla P1-övergången räckte inte för båda. I den kontrollerade fixturen kunde tidigare GRP1-skrivning på PF-övergången eliminera de fyra extra guldpixlarna.

## Dörr, väggar och skott

Gopher-provet utan nyckel stoppade spelaren vid X148. Ett separat prov efter upplåsning visade högeröppningen före passage, med oförändrad vänsterkant. En byggd och körd M1-stencil för svart urtag gav **268 scanlines**, visade ingen korrekt mörk silhuett i dörrfältet och behöll 10 vita pixlar i trängselfixturen. Kandidaten och dess bilder ligger under `evidence/negative/`. Den spelbara checkpointen behåller V02:s fungerande dörrfärg och öppning, med nyckelhålet som blockerare.

De åtta saknade bruna väggpixlarna i standardfixturen är vänsterkantens fyra pixlar på P1:s positioneringsrad och fyra på dess första HMOVE-rad. Den första raden är orange och den andra mörk i den sparade emulatorbilden. Fortsättningen återställde dessutom en väggfärgsregression vid dörrbandets slut som fanns i den första ombyggnaden. Dynamiska vägg- och P0-bilder har kvar andra avvikelser. En tidig separat nollställning av ENAM0 i dörrbandet eliminerade den extra skottraden på samtliga tio kalibrerade X-positioner. Skott- och väggkollision fungerade i replay.

## Exekverad hårdvarubudget och återkörning

- **DASM 2.20.14.1** byggde standard 16 KiB F6/NTSC. Logikbankens SHA-256 är `635718f220398f1c23c7d1281a251392a3cf6b4c7446f94477a785c2ed17f50f`, byteidentisk med V01/V02. Kart- och NPC-maskdata läses från de frysta projektfilerna.
- **Gopher2600 v0.57.2** gav 600 på varandra följande bildrutor med exakt 262 scanlines. Spelrunda, upplåsning, passage och alla sex positionstester höll också 262. Spåren täcker SL44–219 och särskilda RESP0-/RESP1-övergångar. X148-provet nådde c72 före WSYNC och c75 inklusive skrivningen. Källräknad längsta aktiv väg når **76** inklusive WSYNC. Gopher-spåret fångade SP=$F7 på kollisionsvägen, åtta byte stack från $FF. RAM-högvattenmärke $F7 ger **128/128 RIOT-byte**, inklusive stack. Inget speldata används som extra RAM utanför intervallet.
- **Stock Stella 6.7.1 och 7.0** körde den levererade ROM:en med tangentinput. Original-PNG och åtta sekunders video från 6.7.1 ingår. De heltäckande pixel- och scanlinetesternas siffror avser Gopher. Stella full pixelmatris och fysisk Atari är **NOT_RUN**.

Styrning, avfyrning, patrull, jakt, kollisioner, liv, nyckeltillstånd och rumsbonus klarade de provade regressionsfallen. I den fullbordade kallstartsrundan gav upptagning 50 poäng. Först vid passage ökade poängen till 210. `README.md` anger bygg- och körkommandon. `evidence/raw.tar.gz` innehåller ursprungliga Gopher- och Stella-bilder samt råloggar. Kortare underlag finns i `evidence/brief/`.

**G5_FORMAL_OPEN kvarstår. Oberoende VERIFICATION II är NOT_RUN.** MAIN X mottagningsgranskar denna checkpoint.
