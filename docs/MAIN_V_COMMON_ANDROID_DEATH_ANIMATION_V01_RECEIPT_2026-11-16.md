# LET ME OUT! – MAIN V: COMMON ANDROID DEATH ANIMATION v0.1 mottagning

**Datum:** 2026-11-16. **Klassning:** GRAPHICS CANDIDATE, grafisk och databaserad studie **mottagen och avslutad**. **INTE** användar-slutgodkänd, Stella-testad, ROM-testad, animations-/nyckel-spawnimplementation eller oberoende VERIFICATION.

## 1. Faktiskt kontrollerade projektfiler

- [Grafik-ZIP i projektets Drive](https://drive.google.com/file/d/1zujHqITl_UJYWSb2aRPxJZoL7EpqA0bP/view): **385 148 byte**, **273 ZIP-poster**, faktisk full SHA-256 **`aa1478e3476d5b6afaf1a2d4e8843247d65685ac030921188697bdfa8f0ca338`**, ZIP CRC PASS. **271/271 SHA256SUMS-manifestfilhashar matchar**; de ytterligare två posterna är själva `SHA256SUMS.txt` och `MANIFEST.json`.
- [Fullständig GRAPHICS-handoff](https://drive.google.com/file/d/1e6uFScH64ZfCgfQhLCQQRF5zxjNwSpsX/view) 11 723 byte; [exakt mask-JSON](https://drive.google.com/file/d/1KONJDSFGxnb4Zm6aBnHZTIFCaX22vkBs/view) 65 656 byte; [1×/20×-jämförelse](https://drive.google.com/file/d/131xNp226OuYaU26_ICrNZ3W1NEs5t-mD/view) 69 237 byte; [två scenförlopp](https://drive.google.com/file/d/1tJ2pgCxRfLv4flK69AdzO-i14DkG16cz/view) 64 546 byte; [D1 nyckelbärare GIF](https://drive.google.com/file/d/1w47NrHDxx1gOV82OiBoTX-fi0F0EVf9g/view) 8600 byte; [D1 ej nyckelbärare GIF](https://drive.google.com/file/d/1WqY6Jcce3qLEuOACq1yDLVH-M9EIULiP/view) 6709 byte. Google Drive metadata för alla filer bekräftar föräldermappen `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`. Filkopior hämtade för kontroller.
- Oberoende **MAIN-skript** (Python, Pillow, zipfile/hashlib) har utgått direkt från nedladdat ZIP, **inte** litat på GRAPHICS egen `verify_android_death_animation.py`. `OFFICIAL_FRAME_A_REFERENCE_8x9_masks.json` SHA256 **`1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`** matchar den tidigare arkiverade fyra-typs-JSON och exakt det aktuella GitHub-innehållet med känd blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. **Samtliga fyra Frame A-rader intakta.**
- MAIN har räknat om alla typernas D1-`HIT` och `DISSOLVE` **från den angivna matematiska regeln** för vart och ett av 72 originalbitsplatser per typ och jämfört med JSON: **4/4 rätt**. D2 använder identiska faktiska HIT/DISSOLVE-9-byte-masker för 4/4 typer. 8×9-fas-byte-SHA, radhex och vitpixelantal överensstämmer.
- MAIN har jämfört **alla 32 8×9 1×-fas-PNG** (två koncept × fyra typer × ORIGINAL/HIT/DISSOLVE/EMPTY) pixel för pixel mot binära maskdata; **32/32 PASS**. **Alla åtta 1× individ-GIF** är 4-fasers och identiska med motsvarande råmask-PNG. För varje av 4 kombinationer av `D1/D2` och bärare/icke-bärare har MAIN jämfört alla bevarade 1×-scen-PNG och GIF: **4/4 korrekt**; nyckeln syns **först i femte scenläget**, aldrig under HIT/DISSOLVE/EMPTY. Ej-bärarens fjärde och femte PNG är identiska; därför kondenserar GIF-kodaren tomma frames till fyra GIF-rutor, korrekt dokumenterat och ingen nyckel förekommer.
- **Ej självständigt bevisat:** att 1×-grafiken uppfattas som död av blinda mänskliga observatörer; faktisk TIA-objektallokering, överlapp/flicker vid fem andra NPC och skott, CPU-/scanline-deadlines, in-game RAM-faser, nyckel-/kollisionslogik eller CRT-kvalitet. Alla bilder är OFFLINE, **inte Stella-bilder**.

## 2. Visuell bedömning och vad som *inte* godkänns

### D1 – SKISSLÄGE FÖREDRAS, EJ GODKÄND SLUTGRAFIK

Gemensam deterministisk **ursprungsmask-baserad** matematik för varje typ:

```text
HIT(x,y)      = A(x,y) AND ((x+y) mod 3 != 0)
DISSOLVE(x,y) = HIT(x,y) AND ((x+2*y) mod 3 == 0)
EMPTY(x,y)    = 0
```

D1:s verkliga pixelantal ORIGINAL→HIT→DISSOLVE→EMPTY:
- stor man **28→20→5→0**
- stor kvinna **38→23→6→0**
- liten man **20→13→5→0**
- liten kvinna **22→15→5→0**.

**Styrka:** Inga tillagda vita pixlar utanför den aktuella originalmasken, igenkännbar originalform under HIT innan den spricker. Samma regel och faser för alla typer. Små förblir högst sex synliga rader i 8×9-canvas. Nyckel kommer efter dödsförloppet i visualisering.

**Risk:** DISSOLVE med 5–6 pixlar är nära en ren prickeffekt vid 1×; det visar inte pålitlig synlighet under rasterflimmer. Fyra typer × två mellanbilder ger **72 råbytes vid lagring**, innan tabeller, state och TIA-timing. Den matematisk-gemensamma regeln är **inte** samma 9-byte-mellanbild för alla och ingen automatisk billig runtimealgoritm.

### D2 – ALTERNATIVT KONCEPT, LÅG PRIORITET

Gemensam mask HIT `00 00 00 24 66 3C 18 24 00` (14 pixlar) och DISSOLVE `00 00 00 00 00 24 18 24 00` (6 pixlar), totalt **18 råbytes**, oberoende av typ.

**Styrka:** byte-delning gör ren datamängd mindre. **Svaghet:** abrupt förlust av en stor androids höjd/egensilhuett; universell mellanfigur kan misstolkas som ny liten android. D2 får **inte** prioriteras bara för lägre råbytes, eftersom inga 76-cykels-/GRP1-bevis finns.

### MAIN-beslut

**COMMON ANDROID DEATH ANIMATION v0.1 stängs som genomförd, verifierad grafik-DATA-studie. D1 kvarstår som MAIN:s preliminära visuella FÖRSTAHANDSKANDIDAT**, D2 som svag/inte rekommenderad reserv. **Ingen** visuell canonändring, användarapproval, death-frame-final, verkande ROM, keyspawn, timings, TIA-allokering eller specialintegration är härmed godkänd.

## 3. Källgrund och efterföljande, separat grafikuppdrag

Ursprunglig `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip`, `02_MASTER_SPEC.md` och `03_DECISIONS.csv` ursprungs-ID **010** (gemensam död) och **023** (nyckel efter död). Bevarad [MAIN v0.13 nyckel-/dörrreferens](KEY_AND_DOOR_VISUAL_TARGET_V013.md), [v0.14 kontraststudie](KEY_CONTRAST_RGB_REVIEW_V014.md), [v0.15 O1/överlapp](KEY_OCCLUSION_LOGIC_V015.md). R2/nyckel-integrationen och R1 sex fria NPC X/Y är **inte** genomförda.

Nästa fristående *grafikuppdrag*, inte ROM: [GAME OVER – IN-ROOM VISUAL v0.1](MAIN_V_TO_GRAPHICS_GAME_OVER_IN_ROOM_VISUAL_V01_2026-11-16.md), grundat i senare direkta användarbeslutet [GAME OVER + RESET](GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md): ingen separat startskärm, game-over-bild inuti befintligt rum, blinkande slutpoäng och avvikande/kontrastväxlande färger, **endast konsolens RESET** startar om. Exakt form, timing, färgkod och scorefont är öppna. Detta får **inte** innebära någon GAME OVER-kodimplementering.

Övrig ROM-status: R1-F3 enda index0 +1-cykeltest hade **DEVELOPER_LOCAL_GEOMETRY_FAIL**; två-X-runtime NOT_RUN, full R1 BLOCKED/NOT ACCEPTED, ingen ny ROM-order. PR#7 draft, VERIFICATION STANDBY.
