# MAIN II – R1g: EN enda 16KB F6-ROM med FYRA fjärde-NPC-X-lägen, 600/600 verkliga Stella frames

**Datum 2026-11-16. Status `LOCAL_PASS_R1G_FOUR_INDEPENDENT_FOURTH_X_600`.** Detta är den högsta uppmätta statusen för fyr-NPC-forskningen, men **endast fyra diskreta X-lägen för fjärde figuren**. Ingen full fri X över skärmen, femte/sjätte NPC, integrerade PF-väggar, R2/R3, riktig Atari-maskin eller oberoende VERIFICATION.

## Primär evidens

- [GitHub Actions 43817440347 – SUCCESS i samtliga steg](https://github.com/Odourman/let-me-out/actions/runs/43817440347)
- Testad kodcommit **`d1d16758c549ecd657aba3b0aa4d6d7559e19264`** på branch `research/main-ii-r1g-four-X-dynamic-600-20261116`. Senare rapportcommits ändrar inte denna ROM.
- GitHub Actions artifact **`14202444990`**, `main-ii-r1g-four-independent-fourth-X-dynamic-600-evidence`. **622 filer**: originalskriven assembler, DASM-list/sym, exakt 16 384-byte F6/NTSC-ROM, 600 sammanhängande verkliga Stella 6.7.1 X11-bildutskärningar, `evidence_600/frames_600.csv`, `summary.json`, SHA-256 och byggskript.
- ZIP efter nedladdning: **`testzip()==None`**, 622 filer. ROM SHA256 **`a2cef3a6cf63bd1f0139f041d08e71c1a70e6569b298082aeb23e94b1776802b`** kontrollerat direkt ur ZIP och mot JSON. Standard F6 med 4 identiska 4096-byte-banker, alltså F6-ROM-layout, inte extra RAM eller coprocessor.
- Godkända ursprungliga 8×9-bitmapmasker från `main/design/NPC_REFERENCE_8x9_masks.json`, käll- och bitjämförda med varje faktisk Stella-bild. Temporär gul spelar-testmask är inte slutlig designmask.

## Resultat: 600 av 600 fullständigt godkända bildrutor

| Test | Utfall |
|---|---:|
| Äkta konsekutiva Stella frame-ID 11–610 | **600/600** |
| Varje bildruta exakt 262 NTSC-rasterlinjer | **600/600** |
| Fyra olika ursprungliga vita originalmasker + gul full 8×9-spelare, inga fel | **600/600** |
| Ett enda gult M0-testskott på rasterraden **ovanför** NPC-bandet | **600/600** |
| Oväntade vita eller gula pixlar över hela nio-radersbandet | **0 totalt** |
| Fjärde NPC raw GUI-X330 (`pre_mask`) | **150** bilder |
| Fjärde NPC raw GUI-X348 (`post_mask`) | **160** bilder |
| Fjärde NPC raw GUI-X360 (`post_lda`) | **146** bilder |
| Fjärde NPC raw GUI-X378 (`post_color`) | **144** bilder |
| Oklara eller feldetekterade positioner | **0** |
| Sekvensen följer fyra 16-frame-block | **Ja**, uppmätt unik fasoffset |
| Resultat | `LOCAL_PASS_R1G_FOUR_INDEPENDENT_FOURTH_X_600` |

Rå debugger-GUI-positioner är inte TIA:s logiska 160 horisontella färgklockor. Varje TIA-färgklocka visas som två GUI-pixlar. Fjärde NPC rör sig därför i **24 TIA-color-clocks spann** från X330 till X378, medan gul spelare står hela tiden vid **X216** och de tre vita P1-originalandroiderna är statiska i sina positioner.

## Hur fyralägesväxlingen fungerar

- R1f [tvåläges-600-PASS](https://github.com/Odourman/let-me-out/actions/runs/43815510141) avlägsnade R1e:s fasta `P0-wide-copy = player X+64CC` genom **TVÅ skilda `STA RESP0` per synlig rasterrad** i `NUSIZ0=$02` mediumkopieläge. Den första ger gul spelare; den senare, efter eller i samband med `GRP0`-/`COLUP0`-byte, ger vit fjärde originalandroid.
- R1g undersökte fyra **lika långa instruktionsordningar** av samma `STX GRP0` / `LDA #$0E` / `STA COLUP0` / `STA RESP0`, med vardera en egen maskkorrekt 16KB test-ROM. [Statiska R1g-prov #43816935556](https://github.com/Odourman/let-me-out/actions/runs/43816935556) visade fyra rena lägen utan extra CPU-cykler.
- Denna nya ROM packar fyra specialiserade **obran­chade per-rad-kärnor** i samma 4KB exekverbara bank. `FRAMELO & $30` väljer **en gång per bildruta före första NPC-raden** vilken 9-raders-kärna som används. Varje 16-frame-block använder ett av de fyra diskreta lägena; inga nya branch- eller registercykler tillkommer inuti de kritiska raderna.
- Read-only masktabeller flyttades till `ORG $F400` för att lämna plats till fyra specialiserade kernlar; originalbytes och TIA-pixlar förändrades inte. Standard-F6-format, inga externa specialchip.

## Hårda gränser / vad vi INTE har bevisat

1. **Inte fri X över 160 CC:** bara fyra specifika diskreta X, alla nära höger sida. Det finns inget bevis för näraöverlapp med andra NPC, kantlägen, alla sex fria X eller styrning av fjärde X till valfri logisk position.
2. **Endast fjärde NPC rör sig i denna 600-frame-prob.** Gul spelare och tre P1-androider är fortfarande statiska; de utlovade fyra+ två NPC och deras gameplay-positioner/AI saknas.
3. **M0-skottet är ett testobjekt på rasterraden före de 9 NPC-raderna**. Ingen samtidig aktiv projektil-/vägg-/nyckelbelastning på varje NPC-rad.
4. #07 asymmetrisk brun PF-högerdörr [Actions 43816293703](https://github.com/Odourman/let-me-out/actions/runs/43816293703) och #25 TIA-stackskrivning [Actions 43816526765](https://github.com/Odourman/let-me-out/actions/runs/43816526765) fungerar var för sig men är **inte kombinerade** med denna R1g-kernel. Vägg-PF och dörrens orange/svarta detalj kräver fler registerskrivningar inom 76 CPU-cykler.
5. Ingen fysisk Atari 2600-hårdvara, ingen PAL, ingen full R1/R2/R3/R4, ingen oberoende VERIFICATION. **Inget `main`-/PR #7-merge eller designwaiver**.

## Rekommenderat nästa tekniska rastersteg

Utvidga systematiskt vilka `RESP0`-tidfönster och X-positioner som fungerar med samtliga fyra 8×9-masker, särskilt vänstra/centrala/över­lappande scenlägen. Prioritera **kombination med #07 PF-dörr- och väggskrivningar på samma rasterrad**, eller frigjord per-rad-CPU utan att offra originalmaskerna. Dessa är nya testhypoteser, inte godkända implementeringssteg. Innan fortsatt utökning till femte/sjätte NPC krävs ett tydligt resurskontrakt mellan P0/P1, M0, PF0/1/2, 76 cykler och RAM.

**R1 är ännu BLOCKED** enligt `main/docs/ROM_GATE_V018_ACCEPTANCE.md` C01/C02/D01/D03. Endast separat VERIFICATION kan signera en framtida leverans. Denna researchgren ändrar inte `main`, draft PR #7 eller Issue #8.
