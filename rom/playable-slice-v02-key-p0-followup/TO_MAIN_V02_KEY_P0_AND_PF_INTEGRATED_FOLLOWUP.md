# TO_MAIN_V02_KEY_P0_AND_PF_INTEGRATED_FOLLOWUP

**DEVELOPER_OBSERVED.** Spelbar, avgränsad PF-förbättring från fryst `4be191123f0e54b583fd72f6aef782be8ee84a2f` i både TOP och BOTTOM. P1:s etablerade sena HMOVE-väg kan nu användas när nyckeln bärs och inget skott är aktivt. En golvnyckel använder sin befintliga väg. Vid öppen dörr återkommer X0–3 på Y85 i den riktade bilden. Inga vita eller gula pixlar ändras där.

| Prov per ROM | Fryst bas | Ny TOP/BOTTOM | Utfall |
|---|---:|---:|---|
| PF saknade bruna, låst/öppet/golvnyckel | 16/20/16 | 16/16/16 | Öppet förbättrat, kvar FAIL |
| Fem exakta masker i standardsekvens | 595/600 | 595/600 | Regression PASS |
| Helt osynliga NPC i standardsekvens | 0 | 0 | PASS |
| M(1) i skott-/nyckelprov | 23/28 | 23/28 | Regression PASS, mask partiell |
| Fem NPC på Y86 | 2/5 | 2/5 | FAIL |
| Golvnyckel med PY151, PX24/PX60 | 0/14 i båda | 0/14 i båda | FAIL |
| Nyckel från kallstart | 65/65 | 65/65 | PASS |
| Nyckel med aktivt skott | 14/14 | 14/14 | PASS |
| Skott, ingen extra pixel (12,106) | 10/10 | 10/10 | PASS |
| Brun låst dörr och negativ svart kontur/nyckelhål | Korrekt | Korrekt | PASS |
| Upplåst svart öppning | 256/256 | 256/256 | PASS |
| Joystick från kallstart utan RAM-ingrepp | 210p/3 liv | 210p/3 liv | PASS |

## Nyckel och spelare

Både PX24/PY151 och PX60/PY151 tar `KeyAssistRejected` vid SL0 CL55. Ackumulatorn är $97 (151) efter den första jämförelsen. PX24:s X-spärr nås därför aldrig i just detta flöde. Båda faller därefter ur P1-bryggan på ordningsvillkoret med A=$9B (155). Kontrollen PX60/PY159 väljer assistenten och ger 14/14 utan extra guld. Den gamla GRP1-raden ($24) skrivs vid SL201 CL−59, HMP0 vid CL40, RESP0 vid CL49, HMP1 vid CL64, HMOVE vid SL201 CL83 och nästa GRP1 ($04) vid SL202 CL−35. Värdena i spåret är före instruktionen. `TIA` visar räknarfas; ingen ny VDEL-sekvens provades i den här integrationen.

- **Utvidgad assist, FAIL.** PX60/PY151 gav 14/14 guld utan extra guld, men 30 gula pixlar försvann. PX24/PY151 gav 14/14 med två extra guldpixlar, 32 saknade gula och 263 scanlines.
- **Tidigare P1-överlämning utan P0-ompositionering, FAIL.** PX24/PY151 gav 14/14 utan extra guld och 262 scanlines, men SM sjönk från 20/20 till 16/20. Dess fyra förlorade vita pixlar ligger på X62–63/Y169 och X61,64/Y170. PX60/PY151 gav 14/14 utan extra guld men SM föll från 10/20 till 6/20. En X-separerad variant skyddade fallet med PX60 genom att inte använda den tidigare fasen där, men löste inte de förlorade SM-raderna vid PX24. Kasserade prov har faktiska ROM-filer, bilder, källor och loggar.

## PF, M(1) och ITER6

Det verifierade PF-spåret med buren nyckel visar RESP1 vid CL52, HMOVE vid CL142, WSYNC före instruktionen vid CL151 och efterföljande GRP1-väg vid CL19. WSYNC slutar vid c76; patchen lägger inte till arbete i själva rasterkärnan. F6/NTSC väger 16 384 byte per variant. Kollisionsspåret har SP=$F7 och åtta använda stackbyte inom oförändrad 128-byte RIOT-layout. Gopher2600 körde vardera 600 sammanhängande bildrutor vid exakt 262 scanlines. Samtliga 600 standard-PNG:er per variant är byteidentiska med motsvarande frysta bilder. De första försöken nådde testverktygets gamla 175-sekundersgräns; de kompletta omkörningarna använde 420 sekunders totalbudget och oförändrad femsekundersgräns per kommando. Logikbankerna är byteidentiska. Stella 6.7.1 och 7.0 användes för UI-prov med faktisk input och originalbilder. Kvantitativa pixelprov och fullbordade kallstartsrundor är från Gopher.

M(1) saknar exakt en vit pixel i bild 96, 97, 98 och 99 vid (112,97) och i bild 101 vid (117,97). Alla fem koordinater är faktiskt gula (RGB 255,255,41) i båda ROM:arna. Spelarens prioritet bevarades. Detta kvittar inte kravet på komplett vit mask.

V02 visar två kompletta masker både vid X20/44/68/92/116, omordnad maskidentitet och tätt X50/56/62/68/74. I den täta gruppen ligger två vita pixlar också inom M(1):s förväntade silhuett; pixelräkningen ensam identifierar inte det ritande objektet där. G5BE ITER6:s frysta combined-ROM accepterade kontrollscenen (4×262). Den avvisade alla tre V02-vektorer; den diagnostiska avvisningsbilden hade 267/267/266 scanlines respektive. Det ger inget pixelutfall för ett accepterat ITER6-schema i dessa lägen. En integrerad femslottsport är **NOT_RUN**.

Fysisk Atari **NOT_RUN**. **G5_FORMAL_OPEN. INDEPENDENT_VERIFICATION=NOT_RUN.**
