# LET ME OUT! – MAIN V: SCORE & LIVES HUD VISUAL v0.1 – mottagning och prioritering

**Datum:** 2026-11-16
**Klass:** GRAPHICS CANDIDATE DATA STUDY, **MOTTAGEN OCH AVSLUTAD**.
**Beslut:** **H1 är preliminär visuell förstahandskandidat**, H2 arkiverad som möjlig teknisk kompromiss. **Ingen HUD-font, placering, NTSC-bildhöjd, sprites, ny poänglogik, ROM, timing, GAME OVER-font eller canon godkänns av den här mottagningen.** Inget nytt GRAPHICS-v0.2-uppdrag utfärdas. Nästa verkliga beroende är bevis från ROM-kernel/rasterbudget, inte fler grafikskisser.

## 1. Källa och oberoende MAIN-granskning

MAIN hämtade **direkt via Google Drive** alla sju länkarna från GRAPHICS handoff, och har både inspekterat originalbilden och kontrollerat dessa fakta mot de nedladdade bytes:
- [Verkligt ZIP-paket](https://drive.google.com/file/d/1onEQZXXAK2GM7atBr3qOd1BdJCNBzPU-/view), `LET_ME_OUT_SCORE_LIVES_HUD_V01_GRAPHICS_CANDIDATES_2026-11-16.zip`, filstorlek exakt **317 321 byte**, **134 ZIP-poster**, ZIP CRC **PASS**, full faktisk SHA256 **`de9780f60c1caf1d0a5319d20d4302717562f60624d79b44b291c1d048945b38`**.
- ZIP:s `SHA256SUMS.txt`: **132/132** SHA256-inträden kontrollerade och samtliga matchar sin verkliga ZIP-file entry. Övriga 2 poster är `SHA256SUMS.txt` och `MANIFEST.json`.
- [Handoff](https://drive.google.com/file/d/1NmfH6FXJWeGP_Nh0v7qJnPBemQIjwQwT/view) 7 222 bytes, [käll-JSON](https://drive.google.com/file/d/173MnUad7ax5FNcXYljOxHJj5Ase84N6d/view) 22 486 bytes, [faktisk huvudjämförelse](https://drive.google.com/file/d/12luUqCSVORoDpTVqgaWofwgfTNWRoc0S/view) 45 643 bytes, [numbers/lives contact sheet](https://drive.google.com/file/d/1HXUVxQ6W58Ufj4p_uZErwELk7y5whKqv/view) 35 368 bytes, [H1 event 4× GIF](https://drive.google.com/file/d/193U65HlTgk5_EMYpxTSssLZt4NJ7GqUC/view) 29 544 bytes, [H2 event 4× GIF](https://drive.google.com/file/d/19MSwNAOmPqx7DsadKsIvh0QsuUkki1sV/view) 26 948 bytes. Samtliga bekräftade i dedikerad projekt-Drive-mapp med parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.
- `SCORE_LIVES_HUD_V01_SOURCE.json` `C02_grid` = filens `sources/C02_GRID_ORIGINAL_UNCHANGED_40x22.txt` **EXAKT**, 22 × 40, joined `SHA256` **`9247cc46c7003b1011b43af333f2876279f196167277813e78a718faf54a0460`**, motsvarar den oförändrade godkända planerade `C02` i GitHub `design/PLANERADE_RUMSKARTOR_V011.json`, blob `820a74e5fb77c818ffb1286c5b23698d4374e771`. X=0 stängd, x=39 dörrmarkören endast y9–12. Ursprunglig NPC-källfil i ZIP har full SHA256 **`1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`**, och både dess och JSON:s samtliga fyra NPC-8×9-masker matchar `design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Exakt sex instanser (2 large_male, 2 large_female, 1 small_male, 1 small_female) i originalmask, player V03_B endast `NOT_APPROVED_COMPARISON`.
- Båda koncepten har `score_cases=[0,475,700,1500,10250]`, `life_cases=[0,1,2,3]`. MAIN:s oberoende PNG/Pillow-audit: **40/40** verkliga source 1×-PNG rätt bildstorlek (20 H1 à **160×189**, 20 H2 à **160×176**); alla **40/40** 4×-bilder exakt `NEAREST`-uppskalning av var sin 1×-PNG. Fontmatriser och individuella hexrader för `H1_5x7` och `H2_3x5`: kontrollerade för dimension och bytekonvertering, **inga avvikelser**.
- Alla **4 verkliga event-GIF** (H1/H2 × 1×/4×) avkodades frame-för-frame och jämfördes pixel för pixel med sina verkliga `500/475/525/700` source-PNG. **16/16 frames PASS**, duration per GIF `[950,950,950,1600]` ms, **ILLUSTRATIVE_ONLY**, ej NTSC/Game tick.
- Egen aritmetikkontroll: `500 -25 =475`, `475 +50 =525`, `525 +100 +5×15 =700`. Sekvensen förutsätter att extralivströskeln 500 redan är använd; återpassage `475→525` får inte utfärda extraliv en gång till. Det är en korrekt *grafisk illustration*, inte realiserad logik. Status för maxpoängssiffror, maxliv och highscore-persistens fortfarande öppen.

## 2. MAIN:s grafiska beslut och tekniska beroenden

| Koncept | Illustrativ utformning | Grafisk bedömning | Teknisk osäkerhet |
|---|---|---|---|
| **H1** | 160×189 = 176 C02-illustrationsrader + **13 nya synliga** överliggande bildrader; score vänster `S`, lives höger `L` med numeriskt antal + stavar, **5×7** digit-font | **FÖRSTA VISUELLA KANDIDATEN**. Större tecken, tydlig livstatus, minimerar overlap med aktiva androider/utgång. | **NO FREE SCANLINES**. Kräver verklig mätning av synlig bildhöjd, VSYNC/VBLANK/overscan, spelfältets 176 rader, ny scorefont/GRP/PF/TIA-split och CPU-cykelbudget. 13 rasterrader är inte beviljade eller rentav automatiskt möjliga bara för att 189 < 262. |
| **H2** | 160×176 oförändrad ytterbild, score i öppna övre C02 y≈13–17, lives höger, **3×5** font och små figursymboler | Reservkandidat; sämre 1× läsbarhet och reell NPC-överlappning i levererat separat konfliktprov. | Inga extra bildrader, men sannolikt betydande timing-/registerkonflikter där sex NPC, P0, M0 och PF konkurrerar. Inte bevisat att H2 är billigare i körning. |

H1:s 70 bytes för tio 5×7-siffror och H2:s 50 bytes för tio 3×5-siffror är **endast glyphdata**, plus `S`/`L` glyphs (14 resp. 10 ytterligare) – inte rendering, score state, antalet samtidiga siffror eller RAM-krav. G2:s tidigare `GAME OVER`-bokstäver och siffror är också fortfarande icke-godkända mockupresurser. Om extra toppband visar sig oförenligt med faktisk TV-kernel innebär detta **inte** automatiskt att H2 accepteras, eller att ett ROM-team får byta spelrum.
 
**Granskningens gräns:** varenda PNG/GIF är OFFLINE, ingen NTSC/Stella screenshot, inga 6502/GRP1-analyser, inga riktiga färg-/skärmproportions- eller läsbarhetsblindtester. Att filhashar, pixelbytes och samma canon rör sig korrekt i Python är **inte** "HUD tekniskt klar".

## 3. Stopp för ny grafikspekulation och nästa verkliga prioritet

**GRAPHICS v0.1-SCOPE avslutas.** Efter de färdiglevererade, ännu icke slutgodkända sprite-, animation-, GAME OVER-, key- och HUD-kandidatstudierna ska MAIN **inte automatiskt** utfärda fler isolerade grafikskepp bara för att arbetet ska fortsätta. GRAPHICS ska avvakta en uttrycklig ny beställning som har en *konkret* grafisk fråga med faktiskt behov.

**Nästa projektprioritet är att få oberoende teknisk evidens om R1:s blockerade sex-android P1-geometry/timing, varefter ett avgränsat, separat ROM/NTSC-kapacitetstest av synliga topprader och scorefont kan övervägas.** Detta dokument är **inte** en ROM-order, inte ytterligare F3/F4-start, ingen PR-merge eller VERIFICATION-grind. Ingen senare GAME OVER, nyckel, score, extraliv, fullspel, PAL, eller cutover-implementation startas här.

**Slutstatus:** `SCORE_LIVES_HUD_V01_GRAPHICS_STUDY_CLOSED / H1_PROVISIONAL_VISUAL_REFERENCE_ONLY / H2_RESERVE / BOTH_NOT_STELLA_TESTED / NO_CANON_OR_ROM_CHANGE`.
