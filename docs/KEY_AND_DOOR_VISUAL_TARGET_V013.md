# MAIN v0.13 – Godkänd visuell riktning: guldnyckel och orange dörr med svart nyckelhål

**Datum:** 2026-11-15. **Status:** användargodkänt **visuellt mål**; specifik bitmap, TIA-objektallokering, färgkod och spelbarhet är **inte** verifierade eller kodauktoriserade.

## Direkta användarreferenser
Användaren har bifogat två bilder och skrivit: "Låter bra. Fortsätt. Så här tänker jag mig" efter MAIN:s förslag om V2B: en orange dörr med svart nyckelhålsmotiv och en igenkännbar nyckel.

- **Nyckeln:** ljus gul/guld, runt huvud med synligt genomgående runt hål, kort nedåtgående skaft och små tänder på högra sidan. Bilden har ett längre skaft, men originalbeslutet anger en **kort** 2600-nyckel – förkorta proportionerna i 8-bitarsiluetten.
- **Nyckelhål:** svart silhuett med rund överdel och avsmalnande nederdel. Läggs i mitten av orange dörrstreck som ett tydligt **mål**, inte en redan demonstrerad pixelimplementation.
- **Upplåsning:** orange streck **och** svart nyckelhål försvinner i samma händelse. Dörrzon x=39, y=9–12 i 40×22-skiss. Vänster yttervägg förblir helt stängd. Rumsbonus först när spelaren faktiskt går igenom högeröppningen.

## Originalmasker på bitmapnivå (endast rådgivande skisser)
**K11: 8×11:**
```
..####..
.######.
###..###
###..###
.######.
...##...
...###..
...##...
...###..
...##...
....#...
```

**K09: 8×9, fallback:**
```
..####..
.######.
###..###
.######.
...##...
...###..
...##...
...###..
...##...
```

**Inget av K11/K09 är godkänd slutgiltig pixelmask.** De har en sammanhängande färgad region och ett hål som är öppet mot den mörka bakgrunden i den lokala maskkontrollen. K11 är 2 pixlar högre än de godkända 8×9-NPC-maskerna; detta kan påverka rasterbudgeten.

## Teknikbegränsning och prioriteringar
Dörrens högra kant är bara en 40-bitars playfield-cell, cirka 4 horisontella färgklockor bred. Nyckelhålet kan **inte** antas ritas som oberoende svarta subpixlar i en enda sådan PF-bit. Att försöka med separat TIA-objekt, större dörrkoncept eller ny kernel kräver egen auktoriserad teknisk verifiering.

Prioritera: **(1)** korrekt och stabil högerutgång, **(2)** orange port som försvinner, **(3)** guldnyckel som syns efter dödsanimationen, **(4)** detaljerat svart nyckelhål. **V1 brun port** kvarstår som teknisk testreserv, inte nytt visuellt huvudmål.

Spelaren är redan gul. Den guldgula nyckeln måste i framtida skärmtest skilja sig med form/ton på mörk bakgrund. Exakt NTSC/PAL-färg ännu öppen.

## Bevisstatus
**4/4 originalmasker** (två nycklar, två nyckelhålsikoner) klarar intern pixelkontroll, inklusive en sammanhängande region och genomgående hål i nyckelhuvudena. **0 ROM, 0 Stella, 0 scanline-cykelmätningar** i denna studie.

## Filer
- [Drive: v0.13 ZIP med teknisk genomgång, JSON-masker, återkörbart testskript och mobilrapport](https://drive.google.com/file/d/146DjIg8BT4AfqeJFu3xjNB_GUQnqVIV5/view?usp=drivesdk)
- [Drive: mobilrapport PDF](https://drive.google.com/file/d/1SPsvkEtmNhowWlSD8vn-hyW-w5YGPFF_/view?usp=drivesdk)
- [Tidigare dörrförstudie v0.12](DOOR_VISUAL_RIGHT_ONLY_STUDY_V012.md)
- [Beslutsbas från ursprunglig överlämning i Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u): `02_MASTER_SPEC.md`, nyckelform, nyckel efter dödsanimationen, enkel högerutgång.

## Skyddsgränser
Användarens uppladdade referensbilder är vattenmärkta Adobe Stock-illustrationer: inga kopior har lagts i arkivet eller GitHub. Endast originala 1-bitskisser och designbeskrivningar levereras. **The Cabin och I Love a Fish ändras inte**; Linear används inte för Let Me Out!.

**ROM DEVELOPMENT är fortsatt pausad.** Separat uttrycklig auktorisation krävs före kodarbete, binärbygge eller riktig Stella-verifiering.
