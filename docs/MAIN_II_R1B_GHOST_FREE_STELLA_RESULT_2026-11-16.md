# MAIN II – R1b: borttagen P1-ghost med oförändrade 8×9-masker

**Datum:** 2026-11-16. **Status:** lokalt positivt, reproducerbart DASM/Stella-bevis, ej oberoende VERIFICATION och ej full R1.

## Slutprov (alla steg SUCCESS)

- [GitHub Actions #43776440801](https://github.com/Odourman/let-me-out/actions/runs/43776440801).
- **Commit:** `d8afbde1c7c1a39be9db940e719d4c46d0ca0595` på `research/main-ii-r1b-ghost-fix-20261116`.
- **Artefakt:** ID `14186776054`, `main-ii-r1b-ghost-fix-evidence`.
- **Nya F6-ROM SHA256:** `19b385c4a747d07547725b4753fc6e37309156f5ac9330f48f7c3b153219cd37`; 16 384 byte, fyra upprepade 4KB-banker, NTSC.
- **DASM/Stella:** DASM 2.20.14.1, Stella 6.7.1 i Ubuntu 24.04 GitHub Actions.
- Råemulatorbilder och `evidence/pixel_audit.json` verifierade efter nedladdning, samtliga `LOCAL_PASS_4_CONFIGS`.

## Skillnaden mot föregående redan lyckade tvåmaskersprov

Den ursprungliga R1b-varianten hade två kompletta olika originalmasker men på fas 1 och 3 ett **extra vitt streck** (8 GUI-pixlar på övre NPC-raden) utanför maskerna. Möjlig orsak: P1:s ordinarie startkopias position före första omstarten i rasterkärnan.

Denna variant ändrar **enbart inledande P1-grovposition under VBLANK**, från `LDX #6` till `LDX #10` i `P1Delay`. Den dokumenterade tänkta mekanismen är att sätta den tidigare huvudkopians X längre till höger så att den inte hinner börja ritas före den första nya `RESP1`-reseten. Det är en plausibel förklaring; orsaken är inte bevisad på TIA-gatenivå.

## Verkligt uppmätta fyra rasterbilder

| Fas | Man GUI-X | Kvinna GUI-X | Manmask | Kvinnomask | Extra vita GUI-pixlar | P0 / M0 |
|---|---:|---:|---|---|---:|---|
| 0 | 196 | 334 | 72/72 | 72/72 | 0 | båda synliga |
| 1 | 226 | 364 | 72/72 | 72/72 | 0 | båda synliga |
| 2 | 196 | 364 | 72/72 | 72/72 | 0 | båda synliga |
| 3 | 226 | 394 | 72/72 | 72/72 | 0 | båda synliga |

Både stor man och stor kvinna är oförändrade originalmasker från `main/design/NPC_REFERENCE_8x9_masks.json`. Samma nio rasterrader, gult P0-spelarprov och gult M0-skott. 262 NTSC scanlines i råbilderna. `pixel_audit.py` kräver numera inte bara 0 bitfel i båda maskerna utan **0 vita pixlar utanför de två förväntade maskområdena**.

Fas1→2 flyttas mannen 15 TIA färgklockor med kvinnan stilla; fas1→3 flyttas kvinnan 15 färgklockor med mannen stilla. Observerat avstånd mellan paret: 69 eller 84 färgklockor. Detta är **endast begränsat oberoende X**, inte godtyckliga fria X eller nära positioner.

Stella `runToPc` ger på rasterrad 119, bank 0, för den isolerade kernelns tre instruktioner: `STA RESP1` på `$F09F` vid CPU-cykel 28, `STA GRP1` på `$F0A9` vid cykel 41 och andra `STA RESP1` på `$F0B0` vid cykel 51, mätt **före** respektive instruktion. Ingen separat post-write-trap.

## Fortfarande öppet

R1 sex fritt och samtidigt placerade NPC på samma Y **ej godkänd**; endast två originalmasker och två grova X-lägen vardera är visade. Mycket liten separation, överlappningar, fri X längs hela skärmen, 600-följande-bildrutorsstabilitet, R2 fem NPC + nyckel/O1, PF/vägg/dörr, PAL och fullspel är **inte bevisade**. Varken ROM DEVELOPMENT:s draft PR #7 eller oberoende VERIFICATION Issue #8 är ändrade. Ingen ändring av spelregler eller kassetthårdvara.

MAIN II bör behandla denna ROM som **avgränsad teknisk kandidat för mer X-matris och hållbarhetstest**, inte som oberoende slutverifierad R1.
