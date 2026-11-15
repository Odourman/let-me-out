# MAIN II – R1b: två olika fullständiga 8x9-masker i samma rasterband

**Datum:** 2026-11-16. **Bevisklass:** körbar DASM 6502 + verklig Stella 6.7.1 under GitHub Actions + automatiserad pixelmatch. Detta är rådgivande teknikexperiment, **inte full R1 PASS eller oberoende VERIFICATION**.

## Reproducerbart slutresultat

- **Success-run:** https://github.com/Odourman/let-me-out/actions/runs/43776110694
- **Testad commit:** `ee978836634ee07e520feadafffafc0fa8409626`
- **Branch:** `research/main-ii-r1b-masks-20261116`
- **Artefakt-ID:** `14185944035`, `main-ii-r1b-dual-mask-evidence`.
- **ROM:** standard 16 384-byte F6, fyra identiska 4KB-kodbanker, SHA256 `3ad7bf1b963ba201ce540c8e82a3b08fdd684bdff23a85236775deca93197a79`.
- **Maskauktoritet:** `main/design/NPC_REFERENCE_8x9_masks.json` (stor man och stor kvinna), utan ändrad maskgeometri.
- Samtliga jobb steg **SUCCESS** inklusive `pixel_audit.py`. Nedladdad `evidence/pixel_audit.json` kontrollerad: `LOCAL_PASS_4_CONFIGS`.

| Fas | A/B | Stor man, GUI-X | Stor kvinna, GUI-X | Man/mask | Kvinna/mask | P0 + M0 |
|---|---|---:|---:|---|---|---|
| 0 | 1/1 | 196 | 334 | exakt 72/72 | exakt 72/72 | synliga |
| 1 | 2/1 | 226 | 364 | exakt 72/72 | exakt 72/72 | synliga |
| 2 | 1/2 | 196 | 364 | exakt 72/72 | exakt 72/72 | synliga |
| 3 | 2/2 | 226 | 394 | exakt 72/72 | exakt 72/72 | synliga |

GUI-X är rå debuggerbild-koordinater i 1366×900. Ett steg 30 GUI-pixlar är 15 TIA-färgklockor. Fas 1→2 visar **mannen flyttad med kvinnan stilla**; fas 1→3 visar **kvinnan flyttad med mannen stilla**. Därmed finns en begränsad konkret grad av individuell X-justering men **inte bevis för godtyckligt fria X**. Undersökta separationsavstånd är 69 respektive 84 färgklockor, alltså inte närpositioner.

Samma nio TIA-rasterrader används för båda, NTSC 262 rasterlinjer; gul P0 9-raders temporär spelarkandidat och gult M0-testskott (två GUI-pixlar vid GUI X240–241, Y166) observerade. Ingen PF-/vägg-/dörrintegrering.

## Verkliga PC-stoppar i Stella, frame13 scanline119 bank0

| Instruktion | PC före instruktion | _sCycles före instruktion |
|---|---|---:|
| `STA RESP1` #1 | `$F09F` | 28 |
| `STA GRP1` (kvinnorad) | `$F0A9` | 41 |
| `STA RESP1` #2 | `$F0B0` | 51 |

Ingen separat register-post-write-trap har mätts. CPU-cykelavstånd mellan RESP1 är 23 = 69 färgklockor i denna fas.

## Tidigare fel och begränsningar

Testhärden upptäcktes felklassificera vissa riktiga GUI-bilder som svarta vid >20-färgkrav, fast de hade 12 färger. M0 klassades först fel som vitt men är gult. Båda fel är rättade i slutkörningen; alltså inte ROM-grafik-Fail.

**Fortfarande ej bevisat:** full fria X (också nära och överlappande), alla 6 olika NPC med deras X, 600 på varandra följande bildrutor, kombination med R2 nyckel/O1, PF-väggar/högerdörr, fullspel, PAL, annan cartridge. Inget användargodkänt visuellt avsteg. PR #7 och äldre oberoende Verification #8 är oförändrade. Ingen PR-merge.

**MAIN-beslut:** R1b lokalt positivt, begränsat tvåmaskersdelbevis; nästa rådgivande grind är utvidgad X-matris och hållbarhet, därefter eventuell separat auktoriserad uppskalning 3→6. Oberoende Verification krävs för framtida godkännande.
