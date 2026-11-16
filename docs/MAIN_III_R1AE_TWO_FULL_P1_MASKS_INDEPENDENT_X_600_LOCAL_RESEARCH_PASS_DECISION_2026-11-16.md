# LET ME OUT! – MAIN III: nytt R1-delbevis R1ae – två helt olika originalmasker på samma 9 rader med separat varierad X

**Datum 2026-11-16. Beslutsklass: MAIN INTAKE OF RESEARCH, inte ROM DEVELOPMENT implementation och inte independent VERIFICATION.** Aktuell live-GitHub `main` är `f6b3fc76c59161e04e583dc8c0787332d2f261c7`; ROM DEVELOPMENT PR #7 DRAFT på `82667dae033f70570dce903f8e1d4866528be02a`; VERIFICATION Issue #8 OPEN för en annan historisk baslinje. Inget av dessa har ändrats genom forskningen.

## 1. Kontroll mot projektets gällande v0.18-gates

Bindande [v0.18-autorisering](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [acceptans](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md), [scope](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_SCOPE.md), [blockers](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_BLOCKERS.md) gäller fortfarande. C01/C04 kräver **sex** androider med fyra urskiljbara ursprungliga masktyper, spelare, aktivt skott på samma rasterhöjdband och rörelse-/hoppstress; utan full R1 finns ingen R2–R4-acceptans. Ingen designwaiver antas.

**MAIN tar emot R1ae som strikt `LOCAL_RESEARCH_PASS_TWO_DISTINCT_8x9_P1_MASKS`, INTE `v0.18_R1_PASS`.** R1ae bevisar en viktig men snäv feasibility-delmängd: **två olika** hela ursprungs-P1-masker kan renderas på SAMMA nio ursprungliga scanlines, och deras begränsade X-positioner kan varieras separat med gult fullständigt P0-original och en separat M0-testsymbol, under samma CPU- och NTSC-budget.

## 2. Pinad verifierbar evidens

- [**GitHub Actions #43857799040**](https://github.com/Odourman/let-me-out/actions/runs/43857799040): **SUCCESS**, testad commit **`18bbfaa1e500feee93ca85ab446d5915071d9030`** på isolerad forskningsgren `research/main-iii-r1ae-late-grp1-finish-20261116`.
- [**622 filers råevidensartefakt #14222326030**](https://github.com/Odourman/let-me-out/actions/runs/43857799040/artifacts/14222326030), 600 äkta konsekutiva Stella 6.7.1/X11-PNG, `frames_600.csv`, `summary.json`, DASM-käll/list/symboler och 16 KB F6-ROM.
- Exakt rå-ZIP **SHA256 `0a28cc3eca3c86035e1e17548ad6ef3020cf23b638feca0d8f43c424c3dd0dd2`**; separat **ZIP-CRC PASS**, 600/600 CSV `strict_mask_and_shot_pass=True`, 600 PNG omräknade med **fyra distinkta RGB-spelregion-hashar**, en stabil hash per X-par.
- Körbar **16 384-byte F6/NTSC ROM SHA256 `05606a5fd7426df00941be5621ca46c113df794c4ac3fa0f00f0e15cca66a993`**; fyra identiska 4096-byte-banker. DASM `2.20.14.1`, Stella `6.7.1`.
- **Kompakt handoff-zip till MAIN:** `Let_Me_Out_R1ae_Research_Handoff_To_MAIN.zip`, **SHA256 `8024702898e7a413ba8b51d693eb98d0230620ad5a4d12e21b4af64d1cb4931d`**, ZIP CRC PASS, 18 poster. Innehåller MONOLITISK komplett `r1ae.asm` som kan byggas direkt med DASM, ROM, listning, källa, skript, 600-raders CSV, summary och fyra autentiska Stella-exempel; fulla 600 PNG ligger i Actions-artefakt.
- [Fullständig R1ae-forskningsrapport](https://github.com/Odourman/let-me-out/blob/research/main-iii-r1ae-late-grp1-finish-20261116/docs/MAIN_III_R1AE_TWO_COMPLETE_ORIGINAL_8X9_P1_MASKS_FOUR_INDEPENDENT_X_600_STELLA_LOCAL_PASS_2026-11-16.md). All källkod är projektets egen, inga Berzerk-maskinbytes eller skyddad disassembly kopieras.

## 3. Vad exakt löstes? P1-main-ghost utan att offra någon maskpixel

| Version | Första mans-`GRP1` CPU-cykel | Exakt Stella strict PASS | Extra vita P1-pixlar | Saknade originalmaskpixlar |
|---|---|---:|---:|---:|
| [**R1ac**](https://github.com/Odourman/let-me-out/actions/runs/43856319003) | 7 | **300/600** | 1 200 | **0** |
| [**R1ad**](https://github.com/Odourman/let-me-out/actions/runs/43857306216) | 33/35 | **487/600** | 226 | **0** |
| [**R1ae**](https://github.com/Odourman/let-me-out/actions/runs/43857799040) | 35/37 | **600/600** | **0** | **0** |

`NUSIZ1=$01` P1 close-copy; 2× `STA RESP1` på **samma** rasterrad vid c30/c42, c32/c42, c30/c44, c32/c44. Första `GRP1`-laddningen av manmasken har med cykelneutral schemaläggning lagts efter första reset vid c35/c37. Andra masken är förladdad i X och skrivs via `STX GRP1` efter den andra resetten vid c45/c47. **Inget nytt maskbyte, ingen flimmercykel och ingen extra CPU-kostnad.** Det eliminerade en tidigt avfyrad felaktig P1-huvudkopia som tidigare gav spökpixlar på bandets första rasterrad.

**Faktiskt uppmätta X i Stella GUI-crop (inte TIA-color clocks):**

| Mode | Stor man | Stor kvinna | Verifierat logiskt oberoende |
|---|---:|---:|---|
| C | 87 | 159 | Bas |
| D | 99 | 159 | Bara mannens X +12 |
| E | 87 | 171 | Bara kvinnans X +12 |
| F | 99 | 171 | Båda X +12 |

Alla **600** faktiska frames har:
- exakta nio **8-bitars ursprungsbitmaprader för både stor man och stor kvinna på samma Y**, ingen saknad vit pixel, ingen extravit;
- fullständig gul original-P0-spelare med **0** saknade gula pixlar;
- **EN** gul tvåpixel-M0 på mittenscanline, ingen ghostkula;
- 262 stabila NTSC-scanlines;
- identisk reproducerbar scen för varje positionstillstånd.

R1ae:s statiska källa och verkliga Stella-data uppfyller en tidigare principiell MAIN-delfråga: **olika** P1-originalmasker behöver inte tvunget ligga på **olika** vertikala scanline-sektioner (som i Berzerk). Vi har påvisat två samma-Y-masker med olika X, i **fyra särskilda lägen**. Det bevisar inte att teknikens X-geometri fungerar fritt och godtyckligt i hela rummet.

## 4. Vad MAIN fortfarande INTE får kalla löst

- **C01/C04 full R1**: endast 2 av krävda 6 androider visas; en stor man och en stor kvinna, inte två stora män + två stora kvinnor + liten man + liten kvinna. Ingen sex-NPC-overlap/stress, inga flimmerbedömningar under verklig last.
- Fyra diskreta X-par är INTE fri oberoende X för alla sex eller godtycklig nära-/överlappningsgeometri. Den här positiva demonstrationen använder relativt åtskilda P1-masker; deras re-trigger-window förhindrar sannolikt mycket små avstånd och har inte begränsningskartlagts.
- Player P0 använder **`NUSIZ0=ONE_COPY`**, så tidigare R1y/R1z/R1aa/R1ab-konflikt med P0:s multipla kopior och M0-kulans färg är **inte löst under 5–6-NPC-last**.
- Den existerande testbildens högerkant/dörrmönster är inte en integrerad verifiering av R1/R3:s PF/BALL-dörr/geometri och varken R2-nyckel, R3-högerdörrs nyckelhål eller R4 stress omfattas i detta rapporterade PASS.
- Ingen ren oberoende ombyggnad av **separat VERIFICATION**, ingen fysisk originalkonsolkontroll, ingen PAL eller gameplay implementation.

## 5. MAIN:s nästa rekommenderade forskningsgrind

**Närmast:** R1b-**positionsstress** utifrån R1ae, ännu INTE skalning till sex. Prova och registrera separata X-lägen med växlande första och andra `RESP1`-skrivning, **både nära och långt avstånd samt avsiktlig överlappning**, samtidigt som exakt alla nio maskrader, original-P0, gul M0 och 262-cykel/scanline-NTSC klaras utan undantag. Korrelera faktisk pixel-X med CPU-cykel och 6507 `_scan/_sCycles`; dokumentera fail som **geometriska hårdvarubegränsningar**, inte som något som får döljas. R1ae:s fyra positiva diskreta lägen förblir stabil referens.

**Därefter:** separat kontrollerad feasibility för **tredje** vita original-NPC på samma 9-radersband (t.ex. en andra stor man), därefter stegvis vidare till fyra–sex under oförändrade mask-/spelar-/skottkrav och accepterbar synlighet. En R1b-synlighetsvinst godkänner INTE automatiskt nästa implementation-step eller senare R2–R4-cutover. MAIN får bara auktorisera ändring inom befintligt uttryckligt scope efter mandats-/STOPP-kontroll. ROM DEVELOPMENT utför tillåten implementation och egenkontroll; en separat VERIFICATION-mottagare prövar självständigt exakt commit, ROM-SHA och råevidens.

**MAIN-disposition:** `INTAKE: R1AE_RESEARCH_LOCAL_PASS`; `FULL_V018_R1: FAIL/BLOCKED`; `ROM_DEV_PR7: DRAFT/UNMODIFIED`; `VERIFICATION_ISSUE8: UNMODIFIED/HISTORICAL`. Ingen merge eller godkännande av produktions-ROM utifrån detta dokument.
