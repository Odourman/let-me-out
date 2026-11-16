# MAIN II R1c — första tre-olika-masker-provet, 54 CC: FAIL

Datum 2026-11-16. Endast isolerad NTSC/F6-diagnostik, ingen spelimplementering eller oberoende VERIFICATION.

- GitHub Actions körning: https://github.com/Odourman/let-me-out/actions/runs/43785579266
- Testad commit: `e1b2f38be3b0a91ab6d704a0d9f2f1b180a5ba22`
- Artifact ID `14190770035`, `main-ii-r1c-three-masks-same-y-evidence` (DASM/ROM, fem PC-stopp, Stella-bild och faktisk pixel-audit).
- Originalkällan jämförd mot `main/design/NPC_REFERENCE_8x9_masks.json` blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, ingen mask omskriven.
- Godkänd F6-byggning, 16384 byte, Stella 6.7.1 NTSC 262 scanlines, gul P0 och M0 synliga.
- P1 via tre `STA RESP1` på samma rasterrad, men separationsavstånd **54 TIA color clocks**, mätt före instruktionerna enligt Stella: första c23, andra c41, tredje c59 på scanline119 bank0.
- Exakt stor man `72/72` bitpositioner vid debugger-X 166.
- Stor kvinna `71/72` vid debugger-X 274. Bitmaprad 4 (`$FF`) återges `$FE`: lägsta biten saknas.
- Exakt original liten man `72/72` vid debugger-X 382, även hennes ursprungligt helt transparenta övre och nedre rader ingår.
- Lokal audit `FAIL_OR_INCONCLUSIVE` p.g.a. **en bit fel**, inget R1c PASS.
- Möjlig orsak (inferens, ej gate-bevis): tredje `STA GRP1` inträffar för tidigt för föregående P1-kopias sista bildpixel, dvs för kort byte-separation. Fixkandidat: ersätt 2-cykel NOP efter båda RESP1 med 3-cykels `BIT FRAMELO`, vilket ger 57 CC mellan varje RESP1.
- Ingen oberoende fri X-positionering eller 600-framesproving gjord. Ingen full R1, R2, PF eller merge.
