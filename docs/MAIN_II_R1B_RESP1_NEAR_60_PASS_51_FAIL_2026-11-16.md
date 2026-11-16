# MAIN II – R1b närhetsgrind: 60 CC PASS, 51 CC FAIL

2026-11-16. **Endast två olika fullständiga original-8×9-masker**, same Y, gul P0 och gult M0 på standard NTSC F6. Forsknings-/egenkontroll, ej oberoende Verification eller R1 full PASS.

## Faktisk körning och evidens

- GitHub Actions run: https://github.com/Odourman/let-me-out/actions/runs/43778195729
- Kod-commit `f33a77233e676b39f2ee37a16c5873c12090df70`, branch `research/main-ii-r1b-near-copy-20261116`.
- Artifakt ID `14186249747` (`main-ii-r1b-near-60-51-stella-evidence`), 120 filer med 4 råa Stella GUI-bilder + 3 PC-stopp per ROM samt audit-JSON.
- Båda 16KB standard-F6-binärerna genererade med DASM 2.20.14.1 och körda i Stella 6.7.1; **inte** specialkassetter.
- `near60` ROM-SHA256 `9e39939318e46984a2a5cd3247f4a2ea64f21fe2830bf275c87bb3c621da0e99`
- `near51` ROM-SHA256 `f32407f2b9e3c55948fe459745e5c4f7ace7b99eefef9642c6a89fec9efa2ba0`

## Verkliga PC-mätningar i Stella (frame 13, scanline 119, bank 0)

| Variant | STA RESP1 första | STA GRP1 kvinna | STA RESP1 andra | Skillnad mellan RESP1 |
|---|---|---|---|---|
| near60 | `$F09F`, cykel 28 | `$F0A6`, cykel 38 | `$F0AD`, cykel 48 | 20 CPU-cykler = 60 CC |
| near51 | `$F09F`, cykel 28 | `$F0A4`, cykel 35 | `$F0AB`, cykel 45 | 17 CPU-cykler = 51 CC |

Brytpunkterna är FÖRE instruktionerna; en efter-skriv-trap har inte utförts.

## Pixel-utfall ur RÅ Stella-bilder

- **near60: `LOCAL_PASS_4_CONFIGS`**. Fyra positioneringskombinationer: båda maskerna 72/72 korrekta bitpositioner på var och en av de nio raderna, inga extra vita pixlar, P0 och M0 synliga, två begränsat oberoende X-justeringar.
- **near51: `FAIL_OR_INCONCLUSIVE`**. I alla fyra positionerna är första figurens återgivna bitmap **kvinnans**, inte mannens. Mannens bitfel är 18/72 och hennes 0/72 vid den första positionen; även andra positionen är kvinnans fullständiga mask. P0 och M0 fortfarande synliga, 262-raders NTSC. Detta **uppfyller inte kravet på två OLIKA originalmasker**. Zero-ghost är inte pass.
- Samma giltiga källmasker, register och kernel utom ändrad längd på väntan mellan första RESP1 och GRP1. Resultatet stöder mekanismen att `GRP1` för 51 CC skrivs för tidigt före den första kopians datalatchning, men detta är en **inferens**, inte gate-nivå-verifikation.

## Teknisk slutsats och fortsatt gräns

60 CC fungerar och 51 CC misslyckas **för just detta kontrollerade 6502-schema**. Det är inte en allmän TIA-hårdvarugräns. Mellanvariant 57 CC med tvåcykel-NOP är en rimlig snäv undersökning. Inte godtyckligt fria X, inte nära överlappningar inom en 8-pixelfigur, inte 3–6 NPC, R2, PF/väggar, fullspel eller oberoende VERIFICATION.

Run markerades FAIL eftersom den avsiktligt krävde båda varianterna att passera: när 51 CC fallerade var det rätt att stoppa den samlade grinden och bevara artefakterna.

`main`, PR #7 och Issue #8 lämnade orörda.
