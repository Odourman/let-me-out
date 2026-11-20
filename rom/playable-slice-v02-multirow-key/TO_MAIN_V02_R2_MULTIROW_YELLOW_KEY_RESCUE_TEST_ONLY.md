# TO_MAIN_V02_R2_MULTIROW_YELLOW_KEY_RESCUE_TEST_ONLY

**DEVELOPER_OBSERVED. Flerradigt pixelbevis med P1. Direkt integration överskrider rasterbudgeten.** Spelbar referens är fryst vid efe23bde. Ingen ny spelbar checkpoint utses.

| Prov | Nyckel | Spelare i bandet | SM i bandet | M0 | PF | Scanlines |
|---|---:|---:|---:|---:|---:|---:|
| P1-nyckel, PX24 | 14/14 | 18/18 | 10/10 | 1/1 vid X32 | 40/40 | 262 |
| P1-nyckel, PX60 | 14/14 | 18/18 | 10/10 | 1/1 vid X32 | 40/40 | 262 |
| P1-nyckel till vänster om PX104 | 14/14 | 18/18 | 10/10 | 1/1 vid X32 | 40/40 | 262 |
| P1-nyckel, PX60 med indirekta maskläsningar | 14/14 | 18/18 | 10/10 | 1/1 vid X32 | 40/40 | 262 |
| Indirekt plan plus tre tabellstyrda PF-skrivningar | FAIL | FAIL | FAIL | FAIL | Lokal brun remsa kvar | **267** |

De fyra godkända bandproven har noll extra gula, vita och bruna pixlar. Alla fem upplysta nyckelrader ligger efter varandra, med originalformen på X85 och gul $1E. SM står vid X59 eller, i PX60-provet, vid X51. PF-oraklet gäller två lokala fyrpixlarsremsor.

Den nya radplanen låter P0 stå kvar. P1 tidsdelas mellan vit SM och gul nyckel. I det indirekta PX60-provet startar första RESP1 vid c30 och andra vid c41. Andra RESP1 går CL55→64 och GRP1 CL64→73. COLUP1 byts till gult före första nyckelpixeln. NUSIZ1 och vitt återställs före nästa rad. M0 påverkas därmed inte av P1:s kopieinställning.

P0-planen visade hela bandet med sent skott X120 i de separerade PX24- och PX60-proven när NUSIZ0 återställdes. Med tidigt skott X32 gav den en extra M0-kopia vid X48 och skott på fel rad. Vänsterprovet flyttade nyckelpixlar. **FAIL** för P0 som allmän lösning.

## Gräns för direkt integration

Den indirekta P1-raden når 64 cykler före WSYNC och 67 inklusive WSYNC. Tre vanliga tabelläsningar och PF-skrivningar kräver ytterligare 21 cykler i den provade ordningen. Det ger 88 och en sammanlagd ökning från 262 till 267 scanlines, med förvanskade objektpixlar. Den här blockeraren gäller det testade direkta schemat.

De fungerande 16 KiB F6-proberna har konstanta väggbitar och fixturbundna X-faser. Den indirekta varianten läser P0/P1 genom fyra befintliga nollsideadresser för pekare. CPU-spåret visar SP=$FF i rasterbandet. Full V02-integration, AV/upptagning och alla fem bärare med den nya kärnan är **NOT_RUN**. Det finns inget nytt helspelsbevis för RIOT/stack och skyddade regressioner. Fem levande på samma Y förblir separat R1.

## TOP-lure

Samma arkiverade joystick- och framekommandon gav första avvikelse på **bild 387, 289 scanlines** på både fryst kontroll och 8/4. Under FR386 gick GameBank in SL228 CL37 med INTIM=$22. VideoBank återkom SL257 CL97 med INTIM=$00. Vid Overscan PC=$F1FE på SL257 CL118 återstod en timercykel i nollintervallet. LDA INTIM kom ut vid CL130 med **A=$FD** och BNE fortsatte väntan. SP var $FF. Liv gick från tre till två under uppdateringen och NPC återställdes. Detta reproducerar en befintlig överskärmstimerbugg i kontrollen. Ingen timerfix ingår.

## Spelbara referenser och nästa beslut

Färska ordinarie joystickrundor på fryst TOP 8/4 och BOTTOM 6/6 gav dödsdrop, upptagning i AV och fysisk exit med **210 poäng och tre liv** utan RAM-ingrepp. De tidigare 595/600, 10/10, 16/16/16 PF och 256/256 för öppningen hör till de oförändrade referenserna. Gopher gav pixel-, register-, raster- och joystickbevis. Stock Stella gav bandbilder. Fysisk Atari är **NOT_RUN**.

**Ett nästa steg:** integrera P1-dubbelplanen som en schemalagd femradshändelse med förberedda PF-skrivningar och återbruk av köminne. Kräv först 14/14 på PÅ vid både konstant och övergående PF, med exakta spelare, NPC och tidiga/sena M0 samt 262/76/128. Därefter gäller ordinarie TOP/BOTTOM-rundor och alla bärare. Ingen blinkrytm väljs här.

**TEST_ONLY · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
