# Let Me Out! · Playable Slice V01

Öppna `let-me-out-v01.bin` i stock Stella som **F6 / NTSC**. Piltangenterna styr joysticken och mellanslag skjuter med Stellas standardbindningar. Släpp knappen innan nästa skott. Konsolens Reset startar om prototypen.

Du börjar vid vänsterväggen i A_OPEN_01. Efter första skottet jagar androiderna dig. En fiende bär nyckeln. Efter upptagning, gå till högerkanten mitt i rummet och fortsätt åt höger för att avsluta rundan. Dörrgrafiken visar ännu inte upplåsningen. Rasterfel kan göra nyckeln eller en fiende osynlig.

Bygg från den här katalogen med Python 3 och DASM 2.20.14.1.

```bash
python build.py --dasm /workspace/.g5ar-env01/bin/dasm
sha256sum -c SHA256SUMS
```

[Resultat och återkörning](TO_MAIN_PLAYABLE_SLICE_V01.md) · [Stella-inspelning](evidence/stella-play.mp4)
