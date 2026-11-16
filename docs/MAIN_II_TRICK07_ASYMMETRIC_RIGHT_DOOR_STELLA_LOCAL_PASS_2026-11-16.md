# MAIN II – trick #07 Asymmetric Playfield: vänster stängd, endast höger öppnas i riktig Stella

**Datum 2026-11-16.** **`LOCAL_PASS_ASYMMETRIC_PF_LEFT_CLOSED_RIGHT_OPENS`**, begränsat brunt PF0/R3-primitivprov. INTE integrerad dörr i spelrum, ingen orange port/svart nyckelhål, inga fyra NPC samtidigt i samma rasterband och ingen oberoende VERIFICATION.

## Exakt projektkälla och krav

Utgångspunkt `main/docs/ROM_GATE_V018_ACCEPTANCE.md`, **D01–D03** och `main/docs/DOOR_VISUAL_RIGHT_ONLY_STUDY_V012.md`: planerade kartors högra dörr vid **x39, y9–12 i 40×22-kartmodellen**, vänster ytterkant x0 måste alltid vara stängd. Den orange porten och det svarta nyckelhålet är separata visuella mål och kan inte anses testade av en brun PF0-prob.

## Utförande

- [GitHub Actions `43816293703` – hela CI-kedjan SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43816293703), testad commit **`414dec91ef2414de3d95c1c7c59db5864613f7ad`**, gren `research/main-ii-trick07-asymmetric-pf-20261116`.
- Artifact ID **`14201629635`**, 26 filer, `main-ii-trick07-asymmetric-PF-rightdoor-evidence` med 16KB ROM, egen 6502-assembler, symboler/listning, två riktiga Stella 6.7.1 X11-råbilder, binär-SHA och `audit.json`. Nedladdad ZIP har `testzip()==None` och audit/resultat har omlästs.
- **ROM 16 384 byte standard-F6 NTSC**, SHA256 **`39ce0027c28baf6c74c7c0c2aaabee7dd2c045399f93dd19e1277d9ebc71ef5b`**, verifierad direkt från levererad `door_F6.bin`.
- Reflekterad playfield `CTRLPF=$01` och brun `COLUPF=$36`. Skapar PF0 D4-biten på **vänster ytterkant** varje rasterrad, väntar tills den vänstra biten redan ritats, och skriver `PF0` igen så att bit D4 på **höger ytterkant** kan bli 0 under öppningen, utan att radera vänster.
- Baslinjen representerar **48 fysiska testlinjer**: 8 stängda ovanför, 32 öppningslinjer, 8 stängda under. Detta är en kontrollerad visualisering av R3-principen, **inte** implementation av 40×22-rumskartan eller de exakta slutliga 8 scanlines per cell.

## Maskinmätta Stella-pixlar

| Kontroll | Låst (frame13) | Öppet (frame29) |
|---|---:|---:|
| Vänster PF0-vägg, rå GUI-X104–111 | **48/48 stängd** | **48/48 stängd** |
| Höger PF0-vägg, rå GUI-X416–423 | **48/48 stängd** | **16/48 stängd**, bara övre/nedre åtta |
| Höger mittersta öppning | Nej | **32 rasterrader** |
| Oväntad brun PF-grafik i mitten | 0 | 0 |
| Verklig NTSC bildrutelängd, Stella HUD | 262 | 262 |

- `audit.json` ger **`LOCAL_PASS_ASYMMETRIC_PF_LEFT_CLOSED_RIGHT_OPENS`** med samtliga fem delkontroller `true`.
- Den första insamlingen [Actions `43816034615`](https://github.com/Odourman/let-me-out/actions/runs/43816034615) var röd på grund av **felaktigt skärmbildsfärgfilter**: det räknade Stellas grå 1px-debuggerram som PF men sorterade bort brun 192/97/47. Ingen ändring i ROM/6502 gjordes; den korrigerade auditen använder den verkliga brunfärgen och spelplanens x104..423. Råbilder och maskinresultat från den godkända körningen är beviset.

## Begränsningar och MAIN-överlämning

Det går att öppna bara x39-sidan genom en mid-scanline `STA PF0` i ett isolerat standard-F6-NTSC-R3-prov. **Det är ännu inte bevisat att detta kan kombineras på samma rasterrader med R1f:s fyra olika originalmasker, två RESP0, tre RESP1, P0 gul och M0.** R1f är mycket nära CPU-radbudgetens gräns. Fulla väggar, orange port, svart nyckelhål, nyckel/O1 och 600-frame integrerad spelplan är inte verifierade. Enbart brun reserv kan inte räknas som visuellt komplett dörrbeslut.

Forskning på separat branch, ingen ändring i `main`, draft PR #7 eller oberoende Verification Issue #8. Inte full R3 PASS eller någon auktorisation för senare ROM-utveckling.
