# MAIN XI – tekniska lösningar för igenkännbart negativt nyckelhål

Datum 2026-11-20. Status RESEARCH_ADVISORY, ej implementerat eller verifierat. [Användarens nya visuella tolerans](../gates/MAIN_XI_USER_DECISION_RECOGNIZABLE_NEGATIVE_KEYHOLE_NOT_EXACT_R3_2026-11-20.md) tillåter en nyckelhålsliknande men inte pixelidentisk form; negativt hål i orange dörr mot svart bakgrund och fem NPC kvarstår som krav.

## Fysiskt konstaterat i senaste två spel-ROM-prov

[Leveransen och MAIN-mottagningen, Issue #31](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7037903760), testcommit 4c4fc5b7c5545217b2321a38d9db6db5dac7db2f. Nuvarande [build.py](https://github.com/Odourman/let-me-out/blob/4c4fc5b7c5545217b2321a38d9db6db5dac7db2f/rom/playable-slice-v02-top-bottom-door-trial/build.py) använder PFData2=0x7f på tre dörrrader och speglad CTRLPF=1, vilket släcker två sammanhängande 4-CC halvor kring mitten: ett 8px svart hål. [game.asm](https://github.com/Odourman/let-me-out/blob/4c4fc5b7c5545217b2321a38d9db6db5dac7db2f/rom/playable-slice-v02-top-bottom-door-trial/game.asm) BorderDoor rad 258–282 har COLUPF orange->brun; originaltrace visar CL52 till CL94 (42 färgklockor) mot en dörröppning 32px. 80 orange spillpixlar per åtta rader = tio per rad, förenligt med ett 10px för långt färgfönster (men faktisk TIA-fördröjning måste mätas). BorderDoor nollställer även GRP1 och är därför särskilt intressant för vertikalt avgränsad P1-återanvändning. Kantlinjer når redan c76. Sex cykler vunna på den tidigare högra dörrens MITTBAND gäller inte dessa nya ytterkantslinjer.

## Jämförelse och prioritering

1. A – P1 orange 32px dörrsprite i ENDA 8-raders ytterdörrbandet, NUSIZ1 quad/4x: 8 maskbitar × 4 CC = 32px. Låt PF förbli brun utanför och vara avstängd (svart bakgrund) i den 32px breda öppningen. Orange spritebit 0 synliggör svart på ett 4px brett område; två centrala nollbitar gör 8px huvud, en nollbit under gör 4px skaft. Ingen svart överläggssprite, utan verkligt frånvarande orange. Kan både förfina hålet och eliminera orange-PF-färgspill. Största risk: P1:s orange färg, RESP1/NUSIZ1 och maskrad måste återställas och ompositioneras för samtliga fem NPC även vid Y nära kanten. BOTTEN särskilt riskfylld vid slutet av aktivt NPC-band. Nuvarande gräns c76 kräver att registerskrivningar tas bort/omfördelas, inte bara läggs på. Bevisa även player/shot/collision, 262/76/128, same-Y fem och key-player i fysiska ROM. HÖGSTA potential, MEDEL–HÖG resursrisk.
2. B – Ren symmetrisk PF, 16px huvud och 8px skaft (testa 0x3f på huvudraden och befintligt 0x7f på skaftraderna; kontrollera fysisk PF2-bitordning). Inga extra TIA-sprites, nyckelhålet är fortfarande PF=0 mot svart bakgrund. Kvarstående: 8/16px grov form, orange spill via COLUPF, bottom gula öppningsrester och shot. LÅG sprite-risk, god reserv och snabb testbar maskstudie.
3. C – Flerkärnig cycle-exakt PF/COLUPF-rasterplan: korrigera brown/orange färgfönstret till 32px och se om kortare sammanhängande färg-/PF-objektssekvenser kan flyttas till precomputed VBLANK-staging. Kan kombinera med B; dock gör midline COLUPF-skrivningar inte PF till 1px upplösning och kantkernel är redan vid c76. HÖG timingrisk.
4. D – Svart missile-/player-overlay: en 1–2 CC svart objektpixel kan optiskt täcka orange PF om priority tillåter, men detta är INTE negativt genomskinligt nyckelhål. M1 delar COLUP1 med vita NPC, M0 delar COLUP0 med gul spelare/skott, BL delar COLUPF med brun/orange PF. HÖG aktörrisk och kräver separat uttryckligt användargodkännande för ändrad svart-hålsemantik. Inte primärt.
5. E – Venetian Blinds/flicker, chip/mapperbyte: adresserar inte huvudkonflikten utan introducerar förlorade bildrader eller nya hårdvarukrav. Ej lämpligt.

## Principskiss för A, före 4x horisontell förstoring

Åtta rader med 8 maskbitar, # betyder orange, . betyder transparens/svart bakom:

    ########
    ###..###
    ###..###
    ###.####
    ###.####
    ###.####
    ########
    ########

Detta är en hypotetisk 8px huvud/4px skaft i en 32px bred dörr, INTE godkänd slutbitmap.

## Källor

Originalets [30 trick](../RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md): relevanta #01 sprite multiplexing, #05 dynamic PF, #06 resizing, #07 asymmetric PF, #09 VDEL, #10 HMOVE, #12 raster color, #14 multiple display kernels, #17 missile/ball reuse, #19 priority, #24 precompute/cycle exact. [Cross-object research](../MAIN_VI_30_TRICKS_CROSS_OBJECT_REASSESSMENT_2026-11-17.md) varnar uttryckligen för att NPC-negativprov inte bevisar att ett isolerat door-band-knep misslyckas och lyfter PF med negativt hål och färgägande. [Äldre G5L](../gates/G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md) innehåller daterat ursprungligt exakt R3-krav; detta har delvis supersederats.

Webb:
- TIA primärguide: https://www.atariage.com/2600/programming/2600_101/docs/stella.html
- 4x NUSIZ-spelarsprite: https://bumbershootsoft.wordpress.com/2018/08/27/atari-2600-placing-static-sprites/
- Dynamisk PF och dess fönster: https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-17.html
- 76c samt registerplan för flerkärnor: https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html

**Konkret forskningsrekommendation:** test-only A först i TOP och BOTTOM, om A bryter fem-NPC eller budget välj B+C. Mät fysisk TIA/screenshot och regressioner, inga antagna PASS. Ingen ny Codex/ROM startas av forskningsrapporten, ingen G6, mapper- eller flimmerwaiver. G5_FORMAL_OPEN, INDEPENDENT_VERIFICATION=NOT_RUN.
