# MAIN v0.12 – dörrens visuella läge och högeröppning

**Status 2026-11-15:** rådgivande design- och hårdvaruförstudie. Inga nya visuella beslut är godkända. **Ingen ROM, assembler eller Stella-test är gjord.**

## Befintliga spelbeslut (oförändrade)
- Varje rum har **en enda låst dörr i högra ytterväggen**, på samma vertikala plats.
- Inre väggar ska vara symmetriska; ytterdörren är ett undantag. Vänster vägg får aldrig bli utgång.
- Spelare med upphämtad nyckel berör dörren; **dörren försvinner helt**, men inget rumsbyte sker förrän spelaren går genom öppningen.
- Android kan blockera öppningen men får inte gå ut. Befintlig regel E1: dödlig kontakt före samtidig utgång.

## Exakt projektion i godkänd kartbas v0.11
Utifrån [de planerade kartorna A01/B01/C02/D01](../design/PLANERADE_RUMSKARTOR_V011.json):
- Alla fyra har markören `D` på **x=39, y=9–12** i sitt 40×22-rutnät.
- Alla fyra har **x=0 stängt** i samtliga 22 rader, och **x=38 öppet** på de fyra dörrraderna.
- För den *logiska* upplåsta lägesbilden ersätts endast de fyra `D`-cellerna på högerkanten med `.`. Övriga kartceller ändras inte.
- I den tidigare förhandsgranskningen svarar en cell mot fyra färgklockor horisontellt och åtta scanlines vertikalt. De vertikala måtten är **inte** bindande för en framtida Atari-kernel.

## Visuell rekommendation – ännu inte godkänd
**V2:** en smal, sammanhängande **orange** port på högerkanten. När nyckeln används försvinner den omedelbart och lämnar en svart/mörk öppning. Porten ska inte blinka så att den ser öppnad ut när den är låst. Ett detaljerat hänglås är inte nödvändigt i den minimala 4-färgklockors bredden.

**Reserv V1:** brun port i samma färg som väggarna. Mindre tydlig för spelaren men bra som första hårdvarumässiga testbaseline.

**Reserv V3:** separat BALL- eller annan TIA-objektport. Ger potentiellt större visuell frihet men reserverar en mycket eftertraktad rasterresurs; ingen anledning att välja utan faktiskt test.

## Hårdvarurisk
`CTRLPF` kan spegla 20-bits playfield. `PF0` bit D4 motsvarar yttersta biten vid x=0 och, vid spegling, x=39. En tidsstyrd PF0-uppdatering **efter att vänsterkanten visats men innan högerkanten visas** är en tekniskt motiverad möjlighet att släcka endast dörrbiten på högra sidan. PF0 måste återställas inför nästa vänstra kant.

**Orange endast på dörren är svårare:** en särskild färg på den sista 4-färgklockors ytan kan kräva extra väl tajmade `COLUPF`-skrivningar. TIA ger totalt 76 CPU-cykler per scanline, varav robot- och spelargrafik redan kan behöva mycket. Använd därför inte färgförslaget som påstående om genomförd grafik.

## Genomförda kontroller
- **4 av 4 planerade kartor:** statisk geometri låst/öppen, endast rätt sidodörr, ingen annan cell förändrad.
- **16 av 16 offline-referenstester:** logisk upplåsning, faktisk passage och bonus, K1/E1, blockerade kanter, skott kontra kroppskollision. Detta är en **egen Pythonreferensmodell**, inte genomförda ROM- eller emulatorsteg.
- Inga egentliga spelbarhets-, TV-kontrast-, scanline-, flimmer- eller RAM-tester är körda.

## Nästa beslutspunkt
Fastställ om **V2 orange tydlig port** ska vara **visuellt mål**, med V1 som tekniskt basfall, **utan** att låsa färgkod eller renderingsmetod och **utan** ROM-auktorisation.

## Källor och bevis
- [Fullt v0.12-paket på Google Drive](https://drive.google.com/file/d/1UkgypMHlJd7VdAVX_GStHl1p1mcHdAs1/view?usp=drivesdk) (12 filer, inklusive kontrollskript och SHA-256-manifest).
- [Tvåsidig läsrapport i Drive](https://drive.google.com/file/d/1U30NSlfyeem-QgYfX11_en0yRHvdnPqV/view?usp=drivesdk).
- [Ursprungligt beslutsunderlag – Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u), `02_MASTER_SPEC.md` avsnitt 4/7, `03_DECISIONS.csv` ID 016–019/053/057.
- [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): PF0/PF1/PF2, CTRLPF och cykelbudget.
- [2600 Cookbook – Asymmetrical Playfield](https://alienbill.com/2600/cookbook/playfield.html): timingprincip.
- [Stella Debugger](https://stella-emu.github.io/docs/debugger.html): framtida oberoende register- och scanlinekontroll.

## Projektgräns
Det här berör bara **Let Me Out!**, inte **The Cabin** eller **I Love a Fish**. Linear används inte. **ROM DEVELOPMENT är pausad tills användaren uttryckligen godkänner kodstart.**
