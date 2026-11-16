# MAIN II – forskningsregister för alla 26 standard-F6-trick

**Datum:** 2026-11-16. **Spår:** enbart isolerade forsknings-/diagnostikexperiment för *Let Me Out!* v0.18 NTSC, inte implementering eller oberoende VERIFICATION. Ursprunglig numrering/rubrik hämtad från `main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md`. Användarbeslut: **27–30 utesluts helt**. De 52 T-mönstren är överlappande med dessa 30, inte 52 nya uppgifter.

**Kriterier:** `LOKALT DELBEVIS` = riktig DASM/F6+Stella visar en konkret begränsad funktion; `NEGATIV VARIANT` = en bestämd variant underkänd, inte generell omöjlighet; `INDIREKT` = använts som detalj men inte isolerat tricktest; `EJ EGET TEST` = återstår separat experiment. Vi separerar tidigare utvecklarprov, rådgivande historisk källa och oberoende verification.

| Nr | Originaltrick | Befintligt praktiskt läge | Nästa avgränsade standard-F6-test / godkännandekrav |
|---:|---|---|---|
| 01 | Sprite Multiplexing | LOKALT DELBEVIS, R1c tre fasta exakta P1-masker | Två Y-band och same-Y med oförändrade maskdata; särskilj när X verkligen är fri |
| 02 | Mid-scanline GRP Rewriting | LOKALT DELBEVIS, R1e P0/P1 byte och fyra exakta masker statiskt | Mäta registerdeadlines och maskens 72/72 vid närläge |
| 03 | Venetian Blinds | NEGATIV VARIANT, tidigare 9/18/VDEL | Alternativ strikt nio-raders vävning utan förlorade originalrader, annars dokumentera blockerare |
| 04 | Sprite Flickering | NEGATIV VARIANT, 6-fas 100/600 NPC-rutor | Jämför 2/3/4-fas med maskens synlighet och längsta osynlighetsserie; inga godtyckliga waivers |
| 05 | Dynamic Playfield Sprites | NEGATIV VARIANT för full NPC via sex_x; inte isolerat enklare PF-objekt | PF-hjälpsymbol + befintlig vägg samma rasterrad med explicit 4-CC/PF-pixel-limit |
| 06 | Mid-frame Sprite Resizing | EJ EGET TEST | Riktig NUSIZ-strobe mellan rader, observera normal/dubbel/quad och bevarad originalmask |
| 07 | Asymmetric Playfield | Studerat logiskt, EJ EGET självständigt rastertest | Vänster vägg konstant, höger dörröppning med 2× PF-data per rad, verkligt NTSC-ROI |
| 08 | Two-Line Kernel | **NEGATIV VARIANT**, [Stella 262-linjers dubbel-WSYNC-test](https://github.com/Odourman/let-me-out/blob/research/main-ii-trick08-two-line-20261116/docs/MAIN_II_TRICK08_TWO_LINE_REAL_STELLA_NEGATIVE_VARIANT_2026-11-16.md). Alla bitmaprader finns men utspridda över 18 fysiska rader i stället för 9 | Nästa: separat VDEL-/förberedelsepipeline som bevarar exakt 9-radersgeometri; ingen generell omöjlighet påstås |
| 09 | VDEL / Delayed Graphics | NEGATIV VARIANT, tidigare 9-raders VDEL | Separat enbitars latchprov före dynamiskt objektprov |
| 10 | HMOVE Fine Positioning | **LOKALT DELBEVIS**, [4/4 HMOVE Stella-PASS](MAIN_II_TRICK10_HMOVE_REAL_STELLA_LOCAL_PASS_2026-11-16.md); P0+wide-kopia flyttas gemensamt ±3 CC, P1/M0 orörda | Utöka till −8..+7, kantfall och kombinationer; HMOVE frigör inte fjärde NPC:s X från P0 |
| 11 | Late HMOVE Trick | EJ EGET TEST | Isolerat tidigt/sent strobe-A/B, vänsterkanteffekter, flera Stella-TIA-lägen |
| 12 | Raster Color Changes | LOKALT DELBEVIS, R1e gul P0 och vit P0-wide-copy | Färgfas/skrivdeadline över flera X-positioner, oförändrade originalmasker |
| 13 | 48-Pixel / Six-Digit Score Kernel | EJ EGET TEST | Sexsiffrig diagnostisk HUD och mätbar 48px mask, fast geometri deklarerad |
| 14 | Multiple Display Kernels | LOKALT DELBEVIS, R1c två frame-valda kärnor | Jämför separata zon-kärnor, explicit bank-/cykelkontrakt; ej extra NPC-pass |
| 15 | NUSIZ Sprite Duplication | LOKALT DELBEVIS R1e P0 wide + NEGATIV VARIANT R1d NUSIZ1=3 | Täck alla 8 NUSIZ-mönster med faktisk kopiegeometri och extrakopior |
| 16 | Sprite Reflection (REFP0/REFP1) | EJ EGET TEST | Spegelvänd asymmetrisk känd mask och jämför 8 pixlar per rad |
| 17 | Missile and Ball Reuse | INDIREKT M0-testskott, inte objektåterbruk | M1/BL som separat objekt utan att offra M0-skott, pixel- och kollisionskontroll |
| 18 | Playfield Score Mode | EJ EGET TEST | CTRLPF SCORE färgkoppling med gul P0 och vit P1, uppmätt färgkonflikt |
| 19 | Playfield Priority Switching | EJ EGET TEST | CTRLPF-prioritetsväxling med överlapp och O1-formprov, ej logisk nyckelregel |
| 20 | Hardware Collision Latches | EJ EGET TEST | CXCLR/avläsning med kontrollerad P0/P1/M0/PF-överlapp, objekt-ID-begränsning |
| 21 | RIOT Timer Scheduling | EJ EGET TEST | TIM64T för VBLANK/overscan; oförändrade 262 linjer, mät riktig tidsvinst |
| 22 | Stack/RAM Mirroring | EJ EGET TEST | 6507/RIOT-speglingsadress med cykel- och RAM-integritetstest |
| 23 | Undocumented 6502 Opcodes | EJ EGET TEST | Endast isolerad emulatorprov, explicit hårdvaru-/kompatibilitetsrisk; ingen produktionskod |
| 24 | Precomputed Tables and Cycle-Exact Kernels | INDIREKT cykelexakt, lokalt 600-frame-bildbevis; ingen full precompute-prob | Förberedd per-rad registerhändelsetabell i VBLANK mot dynamisk hämtning |
| 25 | Stack-Based TIA Register Tricks | EJ EGET TEST | Minimal PHA-till-TIA busskarta med återställd SP, ingen BRK i produktionskod |
| 26 | Timing-Based Horizontal Scrolling | EJ EGET TEST | Rasterflyttad originalbar utan extra sprite, verifiera faktisk rörelse mot tidtabell |

## Dokumenterade befintliga bevis att inte förväxla med nya test

- **R1e fyra olika originalmasker statiskt, 600/600, P0 gul + M0 en rad ovanför:** [Actions 43812461127](https://github.com/Odourman/let-me-out/actions/runs/43812461127), ROM SHA256 `84083e1c01de7ab0347ac18e85bdf36f37a6a7a201dd060f1f5248020459e24a`. Fjärde NPC:s X är fast kopplat till P0 med +64 TIA CC, inte fri rörelse.
- **R1c tre olika maskdata och liten oberoende 3-CC-förflyttning:** [Actions 43786384041](https://github.com/Odourman/let-me-out/actions/runs/43786384041); 600/600 lokalt.
- **Negativa varianter** bevaras: Venetian/VDEL, sexfasflimmer, R1d NUSIZ1=$03-fyrmaskförsök och tidigare 69-CC rasteröverlast. Dessa FAIL gäller den provade varianten, inte varje möjlig implementation.

## Arbetsordning och stoppgrindar

1. **Grupp A – raster/X/objekt:** 10, 08, 05, 25, 07, 11, 15. Testa en mekanism i taget med känd ROM-hash, rå Stella-bild, PC/CPU-cykler och pixelmasker.
2. **Grupp B – grafik/objekt:** 06, 13, 16, 17, 18, 19, 26. Gör riktiga men avgränsade registerprov, utan att ändra spelregler.
3. **Grupp C – logik/timing:** 20, 21, 22, 23. Separera emulatorkompatibilitet från faktisk hårdvarusäkerhet.
4. **Regressions- och kombinationstester:** 01, 02, 03, 04, 09, 12, 14, 24; bevara både lokala PASS och precisa negativa observationer.
5. **27–30:** helt uteslutna ur planen (SCABS, extrakassett-RAM, DPC, DPC+/CDF/ARM).

**Stoppvillkor:** en testad teknik får inte upphöjas till giltig full R1 om någon originalbit saknas, sex olika fria NPC saknas, P0/M0/PF påverkas eller rasterlängden avviker. Resultat till MAIN är RESEARCH. Inga produktionsändringar, PR-merge, PAL eller oberoende Verification utförs här.
