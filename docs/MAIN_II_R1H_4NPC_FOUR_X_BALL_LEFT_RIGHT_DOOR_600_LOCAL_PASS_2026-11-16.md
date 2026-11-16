# MAIN II → MAIN: R1h – FYRA originalandroider + oberoende fjärde X + asymmetrisk högerdörr i SAMMA rasterband

**Datum:** 2026-11-16  
**Evidensstatus:** **`LOCAL_PASS_R1H_FOUR_NPC_X_BALL_LEFT_PF_RIGHT_DOOR_600`**. Egenkontrollerad reproducerbar forsknings-/diagnostikkod i isolerad researchgren. **Inte full R1/R3, inte sex fria NPC, inte oberoende VERIFICATION eller prod-merge.**

## 1. Avgörande nya resultatet

En enda standard NTSC/F6 16KB-körbar Atari 2600-ROM visar **fyra olika oförändrade godkända 8×9 androidmasker**, en temporär gul 8×9-spelare, ett M0-testskott, en brun vänster yttervägg och en **separat höger yttervägg som öppnas under exakt 32 sammanhängande rasterlinjer**. Den fjärde NPC byter mellan **fyra egna horisontella positioner** med oförändrad gul spelarposition; vänsterkanten är stängd i båda dörrlägena.

Detta är det första praktiska experimentet i serien där **asymmetrisk dörr, fyra original-NPC och dynamisk fjärde-X samexisterar på samma nio figur-rasterrader**. Det är INTE ett bevis för full rumskarta, sex fritt placerade androider, andra individuellt rörliga NPC, orange port eller svart nyckelhål.

## 2. Auktoritet, byggning och råmaterial

- **[GitHub Actions #43821560463 – SUCCESS alla steg](https://github.com/Odourman/let-me-out/actions/runs/43821560463)**, testad kod-commit **`3e5b79fd0409a7ed9f9ae381ade6ac1e66d51b32`**, branch `research/main-ii-r1h-ball-left-asym-pf-four-x-20261116`. Rapporterande senare committer gör inte att den testade binären är en annan.
- **Artefakt-ID `14204881614`**, `main-ii-r1h-integrated-4NPC-BALL-PF-rightdoor-600-evidence`; **624 filer**, inklusive 600 råa autentiska Stella 6.7.1 X11-frame PNG, DASM .asm/.lst/.sym, 16KB ROM, buildskript, exakt `evidence_600/frames_600.csv` med 600 kontrollrader, `evidence_600/summary.json`, `ROM_SHA256.txt` och processor-/emulatorversioner.
- Den nedladdade ZIP-en har kontrollerats med **`testzip()==None`**, 624 poster, 600 PNG i rå-katalogen och CSV med 600 giltiga `local_pass=True`. Binärbyte SHA är separat omberäknade.
- **ROM-format:** standard-F6 exakt 16 384 byte, 4 kopior av en 4 096-byte egen kodbank. ROM-SHA256 **`2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39`**. F6 ger ROM-utrymme men **inte** extra TIA-sprites eller rastercykler.
- **Originalgrafik:** rå byte-jämförelse med `main/design/NPC_REFERENCE_8x9_masks.json` och verklig två-GUI-pixlar-per-TIA-bit kontroll av alla nio rader. Den gula spelarens bitmap är fortfarande en **temporär icke slutgodkänd** testkandidat.
- Projektets dörrkrav lästa direkt i `main/docs/ROM_GATE_V018_SCOPE.md`, `main/docs/ROM_GATE_V018_ACCEPTANCE.md` D01–D03 och `main/docs/DOOR_VISUAL_RIGHT_ONLY_STUDY_V012.md`. Här provas 32 fysisk-rasterradig öppning i ett testband, inte full 40×22-karta eller godkänd orange/nyckelhålsgrafik.

## 3. Uppmätt 600/600 i faktisk Stella 6.7.1

| Mätning ur råa 600 X11-bilder | Resultat |
|---|---:|
| Konsekutiva Stella-frame-ID 11–610 utan luckor | **600/600** |
| NTSC 262 rasterlinjer per bild | **600/600** |
| Fyra separata olika oförändrade original-NPC:s 8×9 masker exakt | **600/600** |
| Gul temporär P0-spelarmask exakt | **600/600** |
| Ett enda gult M0-skott på GUI-y160, x240–241 | **600/600** |
| Vänster brun BALL-vägg **rå GUI-X104–111** (TIA x0..3), inkl. när dörr öppnas | **600/600** |
| Endast höger **32 sammanhängande** dörrrader öppnas när flaggan är satt, rå GUI-y149–180, NPC-band y162–170 ingår | **600/600** |
| Höger ytterkant stängd över/under dörren | **600/600** |
| Dörr låst / öppen | **310 / 290 bilder** |
| Fjärde NPC X330 / X348 / X360 / X378, rå GUI-koordinater | **150 / 160 / 146 / 144** |
| Alla **åtta** kombinationer fjärde X × dörrläge uppträder | **JA** |
| Extra vita / gula GUI-pixlar i figurbandet | **0 / 0 totalt** |
| Oklara lägen eller misslyckade bildrutor | **0** |
| Full auditstatus | **`LOCAL_PASS_R1H_FOUR_NPC_X_BALL_LEFT_PF_RIGHT_DOOR_600`** |

Åtta kombinationers direkta bildantal i `summary.json`: `pre_mask_locked=70`, `pre_mask_open=80`, `post_mask_locked=80`, `post_mask_open=80`, `post_lda_locked=80`, `post_lda_open=66`, `post_color_locked=80`, `post_color_open=64`. Verkligt debuggerräknarfas-offset = **127 mod 128**, gemensamt för fjärde-X `FRAMELO & $30` och dörr `FRAMELO & $40`.

Rå GUI-X för alla objekt: gul P0-spelare **216**, tre övriga original-P1 NPC **166/280/406**, fjärde lilla kvinna i **330/348/360/378**, M0 **240–241** på raden ovanför. GUI-X är *inte* native Atari 160px X; två GUI-pixlar motsvarar en TIA-färgklocka.

## 4. Lösningens resurskarta och varför 76-cykelgränsen hålls

**P1:** tre exakta olika vita original-NPC:s maskdata per rasterrad via tre `STA RESP1` och maskbyte `GRP1`. Övriga tre NPC X är STILLA i denna ROM.

**P0:** gul spelare och vit liten kvinna via två separata `STA RESP0` per rasterrad i `NUSIZ0=$02` medium-läge. Fyra förkompilerade, cykelidentiska P0-omordningskärnor väljs **före** de nio rasterraderna genom `FRAMELO & $30`; det finns INGA nya filialer mitt i deras kritiska spriteuppdateringsfönster. De fyra kritiska källkropparna är programmässigt verifierade **text-identiska** mot R1g:s tidigare `600/600`-PASS.

**M0:** ett gult testskott på en **separat föregående** rasterrad. Det är inte full rörelse/kollision eller samtidig 9-radig projektilscen.

**BL/BALL:** upptar BALL-hårdvarukanalen PERMANENT i testet och ritar en brun **4-färgklockors** vänster ytterkant vid exakt native-x0. `CTRLPF=$21` ger reflekterad PF och 4CC BALL-bredd. `RESBL` sker vid blankraden; `HMBL=$20` + `HMOVE` direkt efter `WSYNC` i blankning finjusterar BL **−2 CC** till x0 utan att flytta P0/P1/M0 (deras HM-register =0).

**PF0 (D4):** styr höger yttervägg. När dörren låses är reflekterad PF0 D4 synlig på x39; när den öppnas stängs PF0 under exakt 32 rader, men BALL håller vänsterkanten stängd. Spelets enstaka högerdörr får därmed **verklig asymmetri utan mid-scanline PF0-skrivning i den redan belastade NPC-loopen**. Detta förbrukar dock BALL som R2/keyhole senare skulle kunna behöva.

**Rasterbudget:** tidigare TopLines 79 har delats i 67 + 12 dörrförberedelser, BottomLines 101 i 10 dörravslut +91 normala rader. Högerläget sätts **FÖRE** NPC-bandet och återställs **EFTER** dörrbandet. Synliga fyra 8×9 sprite-scanlines har oförändrad instruktionsekvens och tidsläggning. Stella mäter 262 bildlinjer i alla 600 bilder. Ingen bankprocessor/extraram infördes.

## 5. Två viktiga NEGATIVA experiment och korrigeringar (full spårbarhet)

1. **BALL först 2 CC fel:** [Actions #43820733068](https://github.com/Odourman/let-me-out/actions/runs/43820733068) åtta autenthiska Stella-skärmbilder med 0..7 NOP efter `WSYNC`, alla gav GUI-X108–115 (TIA +2CC), vilket skulle lämna vänsterkanten x0..1 öppen. `HMBL=$20` + `HMOVE` i blankningen ger i den slutliga faktiska binären x104–111, **600/600**. Det var en felkalibrering, inte en visad generellt misslyckad BL-metod.
2. **M0 bredden blev fel enbart när dörren var låst:** [Actions #43821164519](https://github.com/Odourman/let-me-out/actions/runs/43821164519) pixelgranskade båda dörrbilderna och fann 4 gula GUI-pixlar i stället för 2 i låst läge. Orsaken var att dörrväljaren lämnade `A=$10`, som i originalets skottrad skrevs till `NUSIZ0`. En explicit **`LDA #0` före shotline `STA NUSIZ0`**, utanför NPC:s nio kritiska rader, korrigerade buggen. [Actions #43821344076](https://github.com/Odourman/let-me-out/actions/runs/43821344076) är grön 2-frame regression; slutligen 600/600 i #43821560463.

Dessa negativa bevis måste sparas; R1h får inte omtolkas som problemfritt genomförd fullspelsteknik.

## 6. Kvarstående separata blockerare

- **Full R1 C01/C04 fortfarande BLOCKED:** spelet behöver **sex** androider på samma rasterhöjd (två stora män, två stora kvinnor, liten man, liten kvinna), inte bara fyra med tre statiska X. Fjärde NPC har fyra **diskreta** X inom 24 TIA CC, **inte** fri 0..159-X. Näröverlapp, kanter, kollisioner och individuell P1-/spelarrörelse återstår.
- **Full R3 D01–D03 fortfarande BLOCKED:** 32-raders brun x39-öppning är **en skalad testgeometri**, inte insatt i samtliga verkliga 40×22-kartor. Vänsterkanten har visualiserats men **ingen ogenomtränglig positions-/kollisionsregel är implementerad**. **Orange port och svart nyckelhål saknas**; brunt ersätter inte användarbeslutad estetik. Endast R3-princip och fyra NPC i samma scanlines har delbevis.
- **BALL-kostnaden:** BL används som vänster vägg genom hela scenen. Det blir inte automatiskt tillgängligt som nyckel, projektil, dekor eller valfri rasterresurs utan separat omallokering. Originalmaskerna får inte ändras för att köpa cykler.
- **M0:** testsymbol på raden **före** NPC, ingen full R1/R2 skottavläsning eller rörelse. Ingen O1-nyckelskymning, femte/sjätte NPC, PF-interiör, AI, PAL eller fysisk Atari-hårdvara.
- **Testnivå:** detta är MAIN II:s **egenkontroll**, inte separat oberoende Verification. Användarens v0.18-auktorisation ger INTE automatiskt mandat för senare steg/fullspel.

## 7. Rekommendation till MAIN

**Ny bästa experimentella grund:** R1h är starkare än att lägga en mid-scanline `PF0`-skrivning ovanpå R1g (nästan full 76-cykelrad). Att reservera BALL som statisk vänstervägg och PF0 som högerdörr ger verklig fyra-NPC-plus-dörr-samkörning utan spriteförvrängning. Den *hårda kostnaden* är BL-exklusivitet.

Före eventuell produktionsimplementation krävs **separat avgränsad specifikation och oberoende Verification**. MAIN bör väga: (a) återstående M1/övriga TIA-resurser för svart hål/nyckel, (b) full vänsterkants-/dörrkollision och kartmodell, (c) ytterligare två äkta fulla NPC med individuellt rörlig X, (d) andra PAL och emulator-/hårdvarutester. Inga tester av trick 27–30 (SCABS, extrakassett-RAM, DPC, DPC+/CDF/ARM) ingår.

**GitHub-spår:** forskning under `research/main-ii-r1h-ball-left-asym-pf-four-x-20261116`. `main`, ROM DEVELOPMENT:s draft PR #7 och gamla Verification Issue #8 har inte ändrats. Ingen adoption/merge och ingen designwaiver.
