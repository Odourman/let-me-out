# MAIN II – trick #08 Two-Line Kernel: 262-raders NTSC, men 8×9 originalhöjd FAIL i enkel tvålinjersvariant

**Datum:** 2026-11-16. **Resultat:** godkänt reproducerbart jämförande **experiment**, men **NEGATIV VARIANT** för projektets exakta 9-radersvisning. Ingen generell utsaga att alla two-line/VDEL-rasterkärnor är omöjliga.

## Källauktoritet och syfte

Punkt 08 i `main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md` heter **Two-Line Kernel**. Grundidén är att fördela rendering/förberedelse över två rasterrader. Den potentiella nyttan är CPU-budget; risken är att den vertikala bildgeometrin ändras. Detta snäva experiment prövar ett enkelt **WSYNC-baserat tvålinjeschema** med oförändrade data från vår positiva R1e-fyrmaskers-ROM. Inte en sofistikerad VDEL-pipeline.

## Verklig DASM- och Stella-jämförelse

- [GitHub Actions 43813868438 – **SUCCESS för experimentet**](https://github.com/Odourman/let-me-out/actions/runs/43813868438), testad commit `ae9660cd54aea5e48262a4a8ab5e9d1d0ff2f093`, separat gren `research/main-ii-trick08-two-line-20261116`.
- Artefakt-ID `14201139080`, `main-ii-trick08-two-line-control-versus-variant`. 31 filer, två verkliga Stella 6.7.1 X11 råbilder, två kompilerade standard 16KB F6-ROM:er, DASM-assembler/symbol/list, `audit.json`.
- Artefakt-ZIP `testzip()==None`, återläst `audit.json`.
- **Kontroll**: original R1e enradskärna, ROM SHA256 `84083e1c01de7ab0347ac18e85bdf36f37a6a7a201dd060f1f5248020459e24a` (16 384 byte).
- **Tvålinjersprov:** samma källmasker och P0/P1/M0; lägger en `STA WSYNC` mellan de nio originalbildraderna, minskar `BottomLines` 101→92 för att bibehålla exakt 262 NTSC-rasterlinjer. ROM SHA256 `f862edc97acbb5bf7f4f7d1442235ffa5138196bece82e16eec5b8c4c8f0bbac` (16 384 byte).
- Kontroll av originaldata jämförs direkt mot `main/design/NPC_REFERENCE_8x9_masks.json`. Ingen ändrad bit i de fyra originalmaskerna eller gula temporära spelarmasken.

## Pixelmätning från Stella, 1366×900 screenshot, GUI y162

| Mask/objekt | Kontrollen: fel i ursprungliga 9 rasterrader | Tvålinje: fel i ursprungliga 9 rader | Tvålinje: fel när man samplar varannan rad (9 av 18 rader) |
|---|---:|---:|---:|
| Stor man | 0 | **56** GUI-pixlar | **0** |
| Stor kvinna | 0 | **56** GUI-pixlar | **0** |
| Liten kvinna | 0 | **32** GUI-pixlar | **0** |
| Liten man | 0 | **36** GUI-pixlar | **0** |
| Gul P0-spelare | 0 | **64** GUI-pixlar | Inte separat sampel i denna audit |

Dessa fel är uppmätta **GUI-pixlar (horisontellt 2× TIA)**, inte antal ändrade källbits. Varannan fysisk bildrad i 18-radersbandet matchar däremot alla fyra ursprungliga källradsmönster exakt. Båda körningarna visar Stella-HUD **262 scanlines**. Koden finns och bilderna bevisar att WSYNC-förändringen genomfördes.

**Tolkning:** Tvålinjeschemat ökar figurbandets fysiska höjd från 9 till 18 rasterlinjer. Detta lämnar de ursprungliga 8×9-sourcebyten oförändrade, men uppfyller **inte** det godkända visuella kravet att de fyra originalmaskerna visas som fullständiga nio faktiska rasterrader i samma höjdband.

## Beslut och försiktighet

- **Trick #08 har ett eget praktiskt test**, men **NEGATIVT för detta enkla dubbel-WSYNC-schema** när 8×9-geometrin är bindande.
- Ett nytt specialiserat two-line-kodschema med t.ex. VDEL-pipeline/förberäkning kan fortfarande vara möjligt; det måste verifiera exakt nio ursprungsrader utan att öka höjd eller klippa pixlar. Ingen sådan variant är godkänd.
- 600 frame, fri X, sex NPC, fulla PF-väggar, R2 och speltest har inte utförts. Detta är RESEARCH, ej ROM DEVELOPMENT-fullspel eller oberoende VERIFICATION.
- `main`, ROM DEVELOPMENT:s draft PR #7 och fryst Verification Issue #8 är inte ändrade.
