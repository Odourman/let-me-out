# Let Me Out! – R1ad: två fullständiga original-8×9-P1 med 2×RESP1; fyra ghostpixlar blir två

**2026-11-16. Research-only: 487/600 STRICT PASS, 113/600 FAIL. INTE full R1, ingen oberoende VERIFICATION.**

[GitHub Actions #43857306216](https://github.com/Odourman/let-me-out/actions/runs/43857306216), testad commit `6439e766e27ada89d0196a242cc7569aa284db85`, 600 konsekutiva äkta Stella 6.7.1-X11-screenshots, 262 scanlines varje frame. [Evidensartefakt #14221681226](https://github.com/Odourman/let-me-out/actions/runs/43857306216/artifacts/14221681226), 622 arkivposter (600 PNG och full källa/ROM/DASM/CSV/summary), nedladdad ZIP SHA-256 `8719d5c61615f1de3922b49345a2aeab20b521e62f46364daec5f2e14f92b1b5`, CRC PASS. ROM 16 384 byte standard F6/NTSC, SHA-256 `38d910cc9980c9f6d8f57303df02f3cd87c0fe8ab32dbb19041786a9406a14f1`.

### Ändring från R1ac

R1ac hade 300/600 strikt PASS med 300 frames som gav fyra oönskade vita pixlar vid den första rasterraden till vänster om stora mannen; de två godkända originalmaskerna och alla fyra separata X-par fanns ändå exakt. R1ad flyttade första `STA GRP1` från CPU-cykel c7 till **c33/c35**, efter första `STA RESP1`, genom cykelneutral instruktionomordning. Både man och kvinna behåller samtliga original-8x9-byte och alla nio visuella rader. P0-originalspelare och M0-testskott visas utan bortfall.

### Exakt resultat

- **600/600** verkliga framemarker-ID korrekt; **600/600** NTSC 262 rasterlinjer.
- **0** saknade vit-pixlar från stora mannens OCH stora kvinnans fullständiga ursprungsmask, under **samtliga 600** frames.
- **0** saknade gula originalspelarpixlar; **600/600** har exakt en M0-gul tvåpixelskula på mittenscannline.
- Fyra uppmätta **separata** positioner i faktisk Stella GUI-beskärning: C (man 87, kvinna 159), D (99,159), E (87,171), F (99,171). Endast en X ändras per par C→D och C→E. **Det är inte fri X över hela skärmen**.
- **487/600** strict PASS; kvarstående **113 frames FAIL** med precis **två extra vita pixlar** (226 pixlar totalt). De ligger ALLTID i first raster row y96 på GUI-crop x67–68 när man-X=87 (första RESP c30). Alla maskbytes fortfarande korrekta i dessa frames.
- Detta visar att c33 `STA GRP1` fortfarande aktiverar två pixlar av den föregående initiala P1-huvudkopian. Vid c35 vid man-X=99 går det korrekt med R1ad-tidpunkten.

### Nästa isolerade hypotes R1ae

Flytta **en NOP om 2 CPU-cykler** från omedelbart efter `STA GRP1` till omedelbart före den. Därmed blir första maskens skrivning **c35/c37** i stället för c33/c35, medan samtliga fyra `STA RESP1`-faser förblir **c30/c42, c32/c42, c30/c44, c32/c44**. Inga extra cykler och inga ändrade maskdata. Eftersom första avsiktliga P1-close-kopian börjar ungefär c37/c39 i våra uppmätta screenshots är detta en sista konkret kandidat med cirka 1–2 CPU-cyklers marginal. R1ae får inte kallas PASS före fail-closed 600 verkliga Stella-frames.

### Varningar

Full R1 enligt v0.18 C01/C04 kräver **sex** androidinstanser på samma rasterhöjd + spelare + synligt testsymbolskott. R1ad har bara **två** och ingen PF-vägg/dörr; ingen R1–R4-godkänd integration, ingen fri X över hela spelplanen, ingen formell oberoende VERIFICATION. Forskningskoden ligger i separat branch, `main` och ROM DEVELOPMENT PR #7 ändras ej.
