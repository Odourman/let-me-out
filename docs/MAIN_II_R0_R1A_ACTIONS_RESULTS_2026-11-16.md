# MAIN II R0/R1a — GitHub Actions, 2026-11-16

**Forskningsprov, inte R1 PASS eller oberoende VERIFICATION.**

- Repo: Odourman/let-me-out
- Isolerad gren: research/main-ii-r0-r1a-actions-20261116
- Testad commit: ae5f8bd2c763f692563d5fce6abff24d8df1e8f6
- Körning (SUCCESS): https://github.com/Odourman/let-me-out/actions/runs/43775024026
- Artifact ID 14184804775, `main-ii-r0-r1a-stella-evidence`.
- DASM Ubuntu 2.20.14.1; Stella 6.7.1.
- NTSC / standard F6 16 384 byte.
- ROM SHA256: `1830e59c1eb468f3d0f530d078b705fbd2e6a9b103508a98f15110445fd28777`.

## Faktiska brytpunkter (Stella frame 13, bank 0)

| Breakpoint före instruktionen | PC | Scanline | _sCycles | GUI Color Clock |
|---|---|---|---|---|
| R1aFirstRESP1, STA RESP1 | $F08C | 119 | 32 | 96 |
| R1aSecondRESP1, STA RESP1 | $F093 | 119 | 51 | 153 |

Skillnad **19 CPU-cykler / 57 TIA-färgklockor** före de två instruktionerna. Beräknat slut efter var och en av STA: 35 respektive 54 cykler, men inget separat post-write-trap har registrerats. Debuggerbilderna visar rätt PC och disassembler.

Stella visar **262 rasterlinjer** efter korrigering av en felaktig extra rad. Visuell rå Stella-bild visar **två identiska vita P1-kopior** på samma höjd, gul P0-spelare och synligt M0-testskott.

## Begränsningar

**Lokalt R0- och snävt R1a-delbevis:** godkänt för faktiska före-instruktionsstopp och två synliga lika kopior, under utvecklar-/research-egenkontroll.

**INCONCLUSIVE:** exakta post-write TIA-registerpunkter, faktisk pixelseparation i konsolens 160-pixelskoordinater, 600 konsekutiva frames och samintegrering med nyckel och väggar.

**INTE UTFÖRT:** två olika kompletta 8x9-originalmasker med oberoende fria X; 3–6 figurer, full R1, R2–R4 och oberoende VERIFICATION.

Tidigare fel upptäckta och åtgärdade: odefinierad RESM0, 263 istället för 262 scanlines, oavsiktligt dubbelladdat proof.script som kunde toggla bort breakpoints. Riktiga mätningen använder Stella `runToPc`.

PR #7, main och Issue #8 oförändrade. Ingen merge- eller fullspelsauktorisation.
