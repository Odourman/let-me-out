# TO_MAIN_V02_RASTER_REPAIR_CONTINUATION

**Spelbar F6/NTSC-checkpoint med utökad väggreparation. BOUNDED_RENDER_PROGRESS / RENDER_FAIL.** Fryst start `be1784a90718f0d90688becaeabdfbaf93139554`, SHA-256 `2d2559671f8b920dc6849d1ec0d42da7f2a6dee42406a8531896b1a138cd7687`. Ny ROM SHA-256 `54f14f5211366c8d619ddfd10d9e3d03c1096f33257a6f41e29247382c569ed4`. [MAIN X:s arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7014902496)

## Mätningar i den spelbara ROM:en

| Prov | Fryst start | Ny ROM |
|---|---:|---:|
| Fem kompletta masker utan vitt extra | 595/600 | 595/600 |
| Bildrutor med någon helt osynlig NPC | 0/600 | 0/600 |
| Kompletta masker M (0), F, SM och SF | 600/600 var | 600/600 var |
| Komplett/partiell M (1) | 595/5 | 595/5 |
| X63–70, Y77/90/100, intakt PF och NPC | 24/24 | 24/24 |
| X72–78, Y77/90/100, intakt PF och NPC | 0/21 | 21/21 |
| Golvnyckel från kallstart | 65/65 | 65/65 |
| Nyckel med skott | 14/14 | 14/14 |
| Nyckel när spelaren upptar Y-bandet | 0/14 | 0/14 |
| Fem NPC på Y86 | 2/5 | 2/5 |
| Svart nyckelhål | Saknas | Saknas |

I var och en av de 21 nya väggfixturerna återställdes åtta bruna vänsterväggspixlar. En tabellfri X-kodning återanvänder den sena HMOVE-vägen för X72–78. X71 ligger utanför den uppmätta vägen. Andra dynamiska PF-fel återstår. Alla 600 standardbilder behöll samma gula, bruna och orange pixelkoordinater som start-ROM:en. I första varianten hamnade kod vid F6:s bankväxlingsadresser och störde både P1 och PF. Hjälprutinen flyttades till ett ledigt område, och assemblerbygget avvisar kod som inkräktar på `$FFF6` och framåt.

## R3-dörr, nyckel och resurskonflikter

- **Dörr FAIL.** Den historiska R3-källan använder bitmapraderna `$3c/$66/$76` och har en separat, ospeglad PF-kärna som lämnar dörren öppen i PF. Prototypen portade de oförändrade bitraderna, reserverade P1 och färgade PF mörkt vid högerkanten. Den renare prototypen gav 130 orange pixlar mot originalets 132, en bildrad längre ned. Efter Y-justering saknas (154,99) och (154,103). Öppen dörr gav 0 orange pixlar. Prototypen klarade de låsta och öppna fixtures vid 262 scanlines. Under detta prov var spelkärnans vanliga NPC-kö frånkopplad. Prototypen visar bitmapens fysiska effekt men förlorar NPC-renderingen och kasserades. Den spelbara ROM:en behåller orange låst dörr, mörk öppning och genomförbar utgång. [R3-originalkälla](https://github.com/Odourman/let-me-out/blob/82667dae033f70570dce903f8e1d4866528be02a/rom/v018/tools/build.py)
- **Nyckelband FAIL.** När spelaren flyttas till X24 men ligger kvar på Y151 är nyckeln fortfarande 0/14 vid X85/Y153. Spelaren och nyckeln har där separata X-intervall. Med SM på X59 behöver P1 byta både mask och färg på samma rad. De första guldpixlarna krävs kring färgklocka 154 räknat från radstart, c51⅓. Mellan slutet av SM:s intervall och nyckelns början finns omkring sju CPU-cykler för ett byte, medan en direkt RESP1/GRP1/COLUP1-sekvens redan kräver nio cykler enbart för skrivningarna. Detta gäller det direkta schemat, med P0 upptagen av spelaren.
- **Samma-Y FAIL.** VDEL-provet höll 262 scanlines men gav bara SF komplett och F delvis synlig (34/38), utan vita extrapixlar. VDEL lät P1 använda föregående latch. Det skapade ingen tredje självständig sprite. Fem oberoende masker i samma band saknar fortfarande en fungerande tile-/registerplan inom den integrerade kärnan. M (1):s fem partiella bilder kvarstår vid samma gula överlappningskoordinater som i starten.

## Budget och spelrunda

16 384 byte F6/NTSC, byteidentisk spellogikbank. Gopher2600 v0.57.2 gav 600 × 262 scanlines. Den sena väggvägen når WSYNC vid c73 och avslutar skrivningen inom c76. Den nya X-kodningen i VBLANK uppmättes till SP=$F7, åtta stackbyte inom totalbudgeten 128 RIOT-byte. Kallstart via joystick gav faktisk högerpassage, 210 poäng och tre liv utan RAM-ingrepp. Stock Stella 6.7.1 och 7.0 körde spel-ROM:en med tangentinput. Fysisk Atari är NOT_RUN.

[Byggkommandon](README.md) · [Mätprotokoll](evidence/brief) · [Råloggar och originalbilder](evidence/raw.tar.gz) · [Negativa försök](evidence/negative)

**G5_FORMAL_OPEN. INDEPENDENT_VERIFICATION=NOT_RUN.** Alla nya emulatorobservationer är utvecklarens egenkontroll.
