# TO_MAIN_PLAYABLE_SLICE_V02 · ROM DEVELOPMENT IV → MAIN X

**Resultat: Spelbar enrums-ROM med partiell grafikreparation.** F6/NTSC, 16 KiB. V01-basen är `51128e443cb5d65f44c95ab8d50f35c145c8d485`. V02 ligger i `rom/playable-slice-v02/` på `rom-dev/playable-slice-v02-20261119`. ROM SHA-256 står i `SHA256SUMS`. [V01:s mottagningsbeslut](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7002252372)

## Utvecklarresultat

| Prioritet | Status | Observation |
|---|---|---|
| A · Fem rörliga NPC | **FAIL** för full grafik. | V01: minst en utelämning i 347/600 ramar. V02: 247/600 på samma joystickföljd. 353 ramar hade alla fem köade, 237 hade en utelämning och 10 hade två. Exakt pixeltest nedan. |
| B · Golvnyckel | **PASS** för spelreglerna. **FAIL** för grafik. | Kontrollerat efter dödsanimation: 14/14 förväntade guldpixlar vid (79,60), med fyra extra pixlar. Kallstart vid (85,153): 0/14 pixlar i den tagna golvbilden. Hela 65 uppmätta bildrutor med golvstatus under östpassagen saknade nyckelpixlar. Upptagning fungerade. |
| C · Högerdörr | **PASS** för provad färgväxling och passage. **FAIL** för det svarta nyckelhålet. | Stängd provbild: 128/128 orange pixlar i dörrfältet x156–159, y72–103. Öppen före passage: 128/128 mörka där. Vänstersidan var 128/128 brun i båda kontrollerna. Utan nyckel stoppade joystick spelaren vid x148. Upplåsning utan passage gav ingen bonus. |
| D · Bruna väggar | **FAIL** för exakt grafik. **PASS** för provad rättning och kollision. | Samma frysta karta och väggfärg. Kontrollerad stillbild med P1 vid X64, dörrytan exkluderad för båda ROM:arna: V01 180 saknade och 84 extra av 4 864 förväntade bruna pixlar. V02 åtta saknade och noll extra. Dynamiska ramar kan förlora fler bruna pixlar kring övergångar och objektritning. |

P1-planeraren räknar första och sista icke-tomma raden per oförändrad mask och väljer tillgängliga vertikala intervall. PF skrivs bara när rutnätet ändrar registervärde. Tabellstyrningen skyddar dessa uppdateringar från P1:s två förberedelserader. Samma färgregister kan färga vänsterkanten brun och högerdörren orange eller mörk senare på samma rad. Det mörka tillståndet åstadkoms med `COLUPF=$00` för högerkanten under dörrbandet. Passage prövas av V01:s befintliga programkollision.

När två masker konkurrerar om samma rastertid kan den valda P1-planen sakna en renderingsplats. I kallstart delar nyckelns förberedelseintervall de sista fysiska raderna med SM. Tidigare nollställning av GRP1 inför bytet och en separat serie tidiga skrivningar vid tomma PF-övergångar producerade 263 respektive 268 scanlines i verklig Gopher-körning och kasserades. Den första ooptimerade intervallsökningen missade VBLANK:s timerfönster. Första dörrkärnan skrev GRP1 för sent för X32 och X47. Tidigare GRP1-skrivning återställde de båda maskerna, och de åtta exakta X-proven från V01 gav åter noll differens. Kandidaterna och råspåren finns under `evidence/negative/`.

### Utebliven köplats per individ

| Objekt | Logiskt aktiv | Utelämnad | Längsta obrutna utelämning |
|---|---:|---:|---:|
| M, index 0 | 600 | 0 | 0 |
| M, index 1 | 600 | 10 | 10 |
| F | 600 | 0 | 0 |
| SM | 600 | 0 | 0 |
| SF | 600 | 247 | 211 |
| Nyckel | 0 | Ej tillämpligt | Ej tillämpligt |

Detta är läsning av köplanen i samtliga 600 bildrutor. Den separata stickprovsjämförelsen läser 60 ursprungliga emulatorbilder mot objektens tidigare RAM-koordinater för bilden som just avslutats. En köplats kan ge en ofullständig mask. I de 60 proven syntes hela respektive mask 58, 55, 53, 47 och 34 gånger. M (1) saknades helt i ett prov och SF i 26. Vita pixlar utanför maskunionen fanns i 40/60 provbilder. Se `evidence/brief/soak-pixels.jsonl` för X/Y, masktäckning per individ och vita pixlar utanför maskunionen.

## Genomförd runda och regressioner

**PASS · Kallstart till passage utan POKE.** Från vänsterstart går spelaren söderut, skjuter nyckelbäraren österut, korsar sydkorridoren, plockar upp nyckeln och går upp längs högerkanten. Nyckel ger 50 poäng. Upplåsning ligger kvar vid 50. Faktisk passage slutför rummet med 210 poäng och tre liv. Gopher körde verkliga knapp- och joystickkommandon. Se `evidence/brief/unseeded.jsonl` och `key-lifetime.jsonl`.

**PASS · Styrning och logik i provade fall.** Åtta joystickriktningar, avfyrning, låst sikte under hållen knapp och nytt skott först efter återarmning, väggträff, spelar- och fiendekollision, fredlig patrull och jakt efter eldgivning, livsförlust, skottprioritet vid samtidig kontakt, dödsanimation före nyckelsläpp, upptagning, högerutgång och engångsbonus. Gophers seedade prov använder POKE för startläget och verklig joystick därefter. Den byggda logikbanken är byteidentisk med V01. Stock Stella 6.7.1 och 7.0 körde båda V02 med verklig tangentinput. Videoklippet är åtta sekunder från Stella 6.7.1. M0:s uppmätta X korrigerades från BX−1 till BX i tio dörrbandsprov. V02 hade exakt en skottpixel vid fem kontrollpositioner från X64 till X148. X12, X24, X32, X47 och X56 hade även en pixel på följande rad. Skottets exakta grafik är därför **FAIL**. Se `evidence/brief/missile.jsonl` och V01-jämförelsen under `evidence/negative/`.

## Hårdvara och verktyg

- **NTSC, Gopher2600 v0.57.2.** 600/600 sammanhängande dynamiska bildrutor med 262 scanlines. Kallstart och provad upplåsning/passage gav också 262 i de loggade bildrutorna. Rumsrader SL44–219 och spellogikbankens inträde SL228. Gopher spårade en hel aktiv rumsbild vid WSYNC och prövade separat X148. Senaste uppmätta WSYNC-ingång var CL148 före skrivningen, c72 från radstart och c75 inklusive själva skrivningen. Källberäknad längsta dörrväg är 76 cykler inklusive WSYNC, med båda indextilläggen och skottgrenen.
- **RIOT.** Adresser `$80–$f4` reserverar 117 byte. Uppmätt stack i Gopher nådde SP=$F7 från $FF i väggkollisionsvägen, åtta byte. Totalt **125/128** inklusive uppmätt stack.
- **DASM 2.20.14.1.** Reproducerbar byggning av två kodbanker som packas till standard F6. Bankerna 2 och 3 innehåller varsin kopia av videobanken. `README.md` anger exakta kommandon. Verktygens SHA-256 i `evidence/brief/tools.txt`.
- **Stella 6.7.1 och 7.0.** Utförda visuella rörelse- och skottprov. De automatiska 600 bildrute- och RGB-resultaten ovan avser Gopher. Full pixelregression i Stella och fysisk Atari är **NOT_RUN**. [Verktygsmiljö G5AR](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [Stock Stella 7.0](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

`evidence/images/` innehåller original-PNG, `evidence/raw.tar.gz` innehåller bildserier och fulla PTY-transaktioner och `evidence/brief/` innehåller läsbara loggar. MAIN X mottagningsgranskar. **Oberoende VERIFICATION II är NOT_RUN. G5_FORMAL_OPEN kvarstår.**
