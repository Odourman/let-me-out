# TO_MAIN_V02_RASTER_X71

**Spelbar V02 F6/NTSC-checkpoint. BOUNDED_WALL_PROGRESS / RENDER_FAIL.** Startcommit `eb2591c9c16f2d08bd9fb2d18ee45535ce677b12`, SHA-256 `54f14f5211366c8d619ddfd10d9e3d03c1096f33257a6f41e29247382c569ed4`. Ny SHA-256 `03bcd638fb93fff088b5cb9ddc069f0dfe4c9604e436406877ae736ab510bf52`. [MAIN X:s arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7015342619)

## Spel-ROM och regressioner

Den sena HMOVE-vägen stöder nu hela det sammanhängande intervallet X63–78 i sitt befintliga dörrband. Den tidigare subtraktionsloopen kunde inte representera X71 utan en extra iteration. Den fasta aritmetiken ger HMP1=$F0 för det nya läget och behåller skrivfasen. Samma P1-mask och åtta bruna vänsterväggspixlar verifierades vid X71/Y77, X71/Y90 och X71/Y100. Start-ROM:en förlorade åtta bruna pixlar i vart och ett av de tre lägena.

| Prov | Start | Ny ROM |
|---|---:|---:|
| Exakta riktade vägg- och NPC-prov | 45/48 | **48/48** |
| Fem exakta masker utan extra vitt | 595/600 | 595/600 |
| Helt osynlig NPC i standardsekvensen | 0/600 | 0/600 |
| Golvnyckel kallstart | 65/65 | 65/65 |
| Golvnyckel med skott | 14/14 | 14/14 |
| Golvnyckel med spelaren i samma Y-band | 0/14 | 0/14 |
| Fem NPC på Y86 | 2/5 | 2/5 |
| Skott i dörrbandet | 10/10 | 10/10 |

M (0), F, SM och SF var fullständiga i 600/600 bilder. M (1) var fullständig i 595/600, med samma fem gula överlappningar. Den öppna väggvarianten provade att tillåta bryggan efter nyckelupptagning och använde faktiskt dörrfärg i den sena rutan. De ordinarie öppningsproven gav ingen väggvinst. Den varianten ingår inte i checkpointen. De separata locked/open/cold-key-väggfelen kvarstår. RGB-jämförelsen av alla 600 standardbilder gav oförändrade gula, orange och bruna pixelkoordinater.

## Fysiska motprov

- **Nyckel med P0:s andra kopia.** En separat subkernel bytte GRP0 och COLUP0 efter spelarbilderna och återanvände P0:s andra NUSIZ-kopia för guldgrafiken, medan P1 kunde fortsätta visa SM. Vid spelare X24 landar kopians ankare på X88, medan originalnyckeln behöver X85. Gopher gav 3/14 guldpixlar och 15 extra samt 12 saknade och 22 extra gula pixlar. SM gav 20/20 i detta prov. Den kasserade metoden höll 262 scanlines. Ett rörligt andra ankare och ett färg-/latchschema med korrekt gul mask krävs för den här tekniken.
- **R3-bitmap med P0 och ordinarie P1-kö.** Den kasserade prototypen flyttade dörren till P0 och höll alla fem NPC kvar i kön. Tre blev kompletta. M (0) gav 14/28, M (1) 26/28 och den gula spelaren förlorade 32 pixlar. Rasterlängden var 262. Detta kompletterar det frysta P1-provet med omvänd resursfördelning. Den spelbara ROM:en behåller orange låst dörr, mörk öppning och faktisk passage. Det svarta nyckelhålet återstår.
- **Fem på samma Y.** Radplanen i `raster-budget.json` redovisar de riktiga 8-bitars maskernas pixelintervall och deadlines per rad. På Y90 ligger de fem tända intervallen vid färgklocka 91–92, 115–116, 138–141, 163–164 och 187–188. De mellanliggande fönstren är 21–22 färgklockor. En direkt P1-omställning med förladdad mask kan rymma två skrivningar (RESP1 och GRP1, sex CPU-cykler), med cirka en cykel kvar innan den nya masken krävs. Samma sekvens med en vanlig trecyklig RAM-läsning tar nio cykler. Detta avgränsar behovet av förladdning och positioneringsmarginal på täta rader. En komplett körbar färg- och registerplan för alla nio rader är fortfarande öppen.

## Hårdvarubudget och kallstart

DASM byggde 16 384 byte standard F6/NTSC med byteidentisk spellogikbank. Gopher2600 v0.57.2 mätte 262 scanlines i alla 600 standardbilder. Den sena väggvägen använder c73 för WSYNC och c76 som instruktionsslut. Djupaste mätningen gav SP=$F7, åtta stackbyte inom 128 RIOT-byte. Stock Stella 6.7.1 körde med tangentinput. Joystickrundan från kallstart slutfördes i Gopher med 210 poäng, tre liv och högerpassage utan RAM-ingrepp.

[Byggkommandon](README.md) · [Mätprotokoll](evidence/brief) · [Råloggar och originalbilder](evidence/raw.tar.gz) · [Kasserade ROM:ar och källor](evidence/negative)

Alla emulatorutfall är **DEVELOPER_OBSERVED**. **G5_FORMAL_OPEN. INDEPENDENT_VERIFICATION=NOT_RUN.**
