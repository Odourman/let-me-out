# LET ME OUT! – MAIN III R1n: 14/15 synliga rasterrader med fem R1k-androidfigurer

**Datum 2026-11-16. Status: ISOLATED RESEARCH LOCAL_PASS för båda höjderna. Full R1 fortfarande FAIL/BLOCKED.**

## Uppdrag och varför bilden ser hoptryckt ut

Användaren upptäckte att samtliga originalandroider ser ihoptryckta ut i de faktiska Stella-debuggerbilderna. En rå Stella-debuggerbild från vår R1k-körning hade en synlig TIA-yta **320 × 192** bildpunkter med horisontell dubblering av TIA:s 160 färgklockor, medan normalt NTSC-innehåll bör bedömas ungefär som **4:3**. Korrekt visning ger jämförelseytan **256 × 192**, vilket minskar det artificiellt breda utseendet. Officiell emulatorreferens: [Stella: `-tia.correct_aspect`](https://stella-emu.github.io/docs/index.html), [Libretro Stella 4:3](https://docs.libretro.com/library/stella/).

Men även i korrigerat 4:3 är originalbitmaparna bara **8 bitar × 9 rasterrader**, vilket ger en kompakt bredsilhuett. MAIN III skapade därför först bildsimulerade förhandsvisningar för 9/14/15 rasterrader, sedan **två faktiska byggbara ROM-experiment** utan ändring av ursprungliga 8×9-källbytes.

## Exakt utförd ROM-forskning, inte produktionsintegration

Forskning branch `research/main-iii-r1n-14-15-row-aspect-20261116`.

[GitHub Actions **#43834213779**](https://github.com/Odourman/let-me-out/actions/runs/43834213779): **SUCCESS** på testad commit **`2cf5eb9e30f2e35ea06866b4309c889a0c8d82c1`**, matrisjobb höjd **14** och **15**, vardera **600 verkliga konsekutiva Stella 6.7.1 frame-skärmbilder**. Byggning på R1k, exakt original-R1k ROM-SHA `99c2cc160713899a8662508a4eeafec956b3d9b4825668e66b135404ec79f2a7` verifieras i generatorn.

| Kontrollerad egenskap | 14 rader | 15 rader |
|---|---:|---:|
| Exakt byggd 16 384-byte standard NTSC F6 ROM | PASS | PASS |
| Följd av 600 faktiska Stella-frame-ID | **600/600** | **600/600** |
| Rätt NTSC 262 rasterlinjer | **600/600** | **600/600** |
| Fem fullständiga ursprungliga NPC-instansmasker, vertikalt upprepade utan förändring av mönsterradernas bitar | **600/600** | **600/600** |
| Gul temporär spelare och M0 diagnostiskt ovanför huvud, oförändrat | **600/600** | **600/600** |
| BALL vänster vägg / PF0 höger 32-raders dörröppning | **600/600** | **600/600** |
| Fjärde androidens 4 X-lägen × dörrens 2 lägen | **8/8** | **8/8** |
| Extra vita och gula pixlar | **0 / 0** | **0 / 0** |
| Källtabeller med original 8×9 exakt oförändrade | **JA** | **JA** |
| ROM SHA256 | `eb52e6baf37a396acbbf424a7ba937d78ef662cce7a47aff0cda9d9c6cf25558` | `15b2f950a68d8846ec9aeec3ed9ea7c37e6011f9db5da44fe1463d581d6549d0` |

Evidens:
- [**14 rader** – Actions artefakt #14209209639](https://github.com/Odourman/let-me-out/actions/runs/43834213779/artifacts/14209209639), nedladdad ZIP SHA256 `17a6e1ea258f5135b278fa09eaae75f5445b416596e79843f00a270ac944a476`; **619 poster**, **600 PNG**, ZIP CRC PASS.
- [**15 rader** – Actions artefakt #14209224508](https://github.com/Odourman/let-me-out/actions/runs/43834213779/artifacts/14209224508), nedladdad ZIP SHA256 `8d8c4c445bcbc30f7acd44cc537715e57a1704e6b34e59a1c996c0c4744d270a`; **619 poster**, **600 PNG**, ZIP CRC PASS.
- Källgenerator `rom/v018/experiments/main_iii_r1n_height/build_r1n.py`, källor `r1n_14.asm`, `r1n_15.asm`; frameanalys `analyze_600.py`; båda `.bin`, DASM-lister, `summary.json` och CSV i artefakterna.

### Tekniken

**Inga godkända NPC-originalmasker har redigerats.** Varje 9-byte tabell finns kvar bit för bit. Generatorn skapar separata forskningsbitar för visning: `height` byte per mask, där visad rad `i` väljer originallinje `floor(i*9/height)`. Alltså förlängs de redan existerande bitmapraderna genom upprepning; antal spelkaraktärer och originalbitmaparnas åtta horisontella bitar förändras inte.

Denna metod påverkar **antal fysiska scanlines** per figurs band (9→14 eller 15) men **inte** antalet CPU-cykler som behöver utföras inom en enskild återutlöst figurrad. R1k-kerneln används med fyra olika lägen för lilla kvinnans X och två nära separata `RESP1`-utlösningar för båda stora kvinnor. TIA följs fortfarande rasterrad för rasterrad. Två kod- och datavarianter byggdes under `ORG $F400` i standard-F6, koden rymdes i ett 4KiB-program som upprepas fyra gånger.

Dörrens 32-raders öppning behålls genom att minska `R1hDoorBottom` från **10** till **5** respektive **4** scanlines när figurbandet får 5 respektive 6 fler scanlines. Övrig undre marginal förblev `BottomLines=91`, så **NTSC 262** bibehölls.

**Reproducerbart första fel:** [Actions #43833868916](https://github.com/Odourman/let-me-out/actions/runs/43833868916) byggde båda ROM:arna och pixelgranskningen fann originalmaskerna fullt korrekta men 0/600 NTSC-frames. Faktiskt Stella-HUD visade **267** (14) respektive **268** (15) scanlines. Felorsak: de 5/6 rader som flyttades ur den lilla dörrbottenmarginalen lades felaktigt till den stora undre marginalen. Denna EXTRA addering togs bort; båda körningarna blev därefter SUCCESS med exakt 262. Detta är en explicit rättning av verklig frametimebugg, inte ett försvagat test.

## Visuell slutsats

När bilderna jämförs sida vid sida i ungefär **NTSC 4:3** är **14 visade rasterrader** en rimlig estetisk förstakandidat. 9 rader är synbart för brett/lågt; 15 rader fungerar tekniskt men ger enligt MAIN III:s bedömning en något längre, smalare stil än 14. Detta är **research-rekommendation, inte godkänd ny höjd/canon**. Beslut om spelgrafik måste tas separat under MAIN:s ordinarie designordning.

## Skott från handen – blockerare fortfarande kvar

**R1n löser inte skottet.** Det äldre M0-testskottet är fortfarande på GUI-y160, över den temporära spelarens huvud; dess acceptans är blockerad. Med 14-radersupprepningen flyttas spelarens synliga armrad från cirka **y165** till **y167–168**, så ett nytt skottbörvärde bör vara **y167**, nära faktiskt hand-X (för närvarande ungefär GUI-x230, inte x240). Men tidigare R1m bevisade att `STX ENAM0` inne i det fem-NPC-bandet med `NUSIZ0=$02` genererar **en extra vit M0-missilkopia** vid x304–305, trots att den gula huvudkulan syns x240–241. Totalt 1 200 vita extrasträckpixlar över 600 frames; denna biverkning får **inte** godkännas.

**Framtida korrekt test** måste antingen (a) tidsmässigt avsluta M0 efter spelarens handskott men före NUSIZ0:s andra missile-copy utan att missa någon av de fem NPC:ernas mask/strobefönster; (b) prova annan sprite-/missilresurs som inte ger fler automatkopior, med kollisions- och färgkontroll; eller (c) om detta inte ryms, **öppet erkänna att en annan rasterkernel-arkitektur behövs**. Skottet ska bli EXAKT EN projektil från spelarhanden, i rätt färg och utan falska TIA-kollisioner. Att dölja kopian under en vit android räcker inte.

## Status- och beslutsgates

- **R1n14/R1n15 = LOCAL_PASS för enbart renderad 14/15-raders visning med fem R1k originalNPC-instanser.**
- **Full R1 = FAIL/BLOCKED**, andra stora mannen saknas, sex fritt styrbara X saknas, komplett karta, orange dörr och nyckelhål saknas, skottet felplacerat, spelaren en temporär bitmap, ingen full R2–R4.
- F6/NTSC oförändrat; **ingen F6SC/DPC+/ARM/PAL, inget tillåtet scopebyte**, inga ändringar på `main`, ROM DEVELOPMENT:s draft PR #7 eller VERIFICATION issue #8. Detta är ännu inte oberoende verifiering.
- Nästa grind efter separat MAIN-godkännande: undersök **14-raders armrad y167** och en ensam korrekt färgad projektil med **samtliga fem** originalNPC intakta; fortsatt forskning om sjätte stor man och fria X görs separat.
