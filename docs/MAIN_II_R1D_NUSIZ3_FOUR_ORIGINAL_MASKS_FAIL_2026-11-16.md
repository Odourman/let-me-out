# MAIN II – R1d NUSIZ1=$03: fyra unika originalmasker FAIL (verkligt Stella-prov)

**2026-11-16. Status: isolerad forskningsdiagnostik på standard NTSC/F6, ej oberoende VERIFICATION och ej full R1.** Den tidigare lokalt lyckade R1c-kärnan med tre originalmasker och ett litet individuellt X-steg lämnas oförändrad.

## Hypotes och källor

Andrew Towers [TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), "The Re-trigger Trick", beskriver hur `NUSIZ1=$03` ger close- och mediumkopior (+ca 17 och +33 TIA-färgklockor efter varje `RESP1`), och att flera `RESP1`-skrivningar kan ge fler än tre P1-kopior på en rasterrad. Ataris [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) dokumenterar det delade `GRP1`-registret. Kopiorna är inte per automatik olika bitmappar. För att uppfylla Let Me Out!-R1 måste de ha separata, exakta original-8×9-mönster och till slut individuellt fria X.

## Reproducerbara bevis

- Källa i grenen `research/main-ii-r1d-nusiz-triple-20261116`, katalog `rom/v018/experiments/main_ii_nusiz3_four/`, utan ändring av `main`, PR #7 eller oberoende verifieringsbaslinje.
- [GitHub Actions run 43794517045 (DASM-build och Stella-fångst PASS, fyra-originalmaskers pixelgrind FAIL)](https://github.com/Odourman/let-me-out/actions/runs/43794517045), commit `b4411d2fe7fd5274033a00460a0bd1303147722c`.
- Evidence-artifact **14193628087**, `main-ii-r1d-nusiz3-four-originals-evidence`: 73 filer, två körbara 16KB standard-F6 ROM, källor, DASM .sym/.lst, sex faktiska `RESP1` PC-fångster, två Stella-råbilder och `evidence_audit.json`.
- DASM 2.20.14.1 / Stella 6.7.1 / NTSC. Samtliga ursprungliga data hämtas från `main/design/NPC_REFERENCE_8x9_masks.json`, inklusive den fjärde `small_female`-maskens tomma rader.
- `nusiz3_only` ROM SHA256: `504914be5fda016372dd4cd48a7b5a526a16acf12e4d4630a81543f3bc44e900`.
- `four_mask_probe` ROM SHA256: `8e6960b07b33a1a6b18b66ce435235b5dcd268009e2e252ebf1baed8e3049f16`.

## Två varianter och verkliga pixelresultat

### A. NUSIZ3 utan fjärde GRP1-omskrivning

Håller P0/9-radersspelaren och M0-skottet i ursprungliga testpositioner. Ändrar `NUSIZ1=$01` till `$03`, annars R1c:s tre ursprungliga P1-masker.

- Stella: 262 NTSC-scanlines, P0 och M0 synliga.
- Stor man exakt `72/72` vid raw debugger-GUI X166 (en kopia).
- Stor kvinna exakt `72/72` vid X198 **och** X280 (två kopior).
- Liten man exakt `72/72` vid X312 **och** X394 (två kopior).
- **250 oväntade vita GUI-pixlar** utanför de förväntade unika maskområdena. De extra kopiorna är verkliga Stella-pixlar, inte omritade illustrationer.
- Slutsats: NUSIZ ger fler P1-grafikkopior men ingen distinkt fjärde originalandroid.

### B. NUSIZ3 med fjärde originalmask och flyttad M0-uppdatering

Försöker ladda `SmallFemaleRows` direkt efter tredje `STA RESP1`. För att frigöra 7 CPU-cykler per NPC-rad ligger M0-projektilen på en separat föregående rasterrad. Denna skillnad är **ett forskningsavsteg från full R1-belastning**, inte en tillåten gameplay-ändring.

- Efter korrigerad NTSC-radbudget har ROM:en **262 rasterlinjer**.
- Gul spelare P0 finns faktiskt vid raw GUI X400–411, och gult M0-testskott vid X240–241/Y160. Den första automatiska auditens P0-region var för snäv och rapporterade felaktigt noll P0. I den slutliga CI-körningen validerades däremot P0:s **exakta gula 8×9-mask vid X398** och M0:s två GUI-pixlar samtidigt; detta skiljer säkert ett tidigare instrumenteringsfel från ett verkligt maskfel.
- Stor man: **0 fullständiga originalmasker**, bästa möjliga maskmatch 36 pixelavvikelser i den valda sökregionen (inte godkänd).
- Stor kvinna: tre exakt återgivna kopior (X142, 174, 238).
- Liten man: en exakt kopia (X270).
- Liten kvinna: två exakta kopior (X352, 384).
- **316 extra/oförklarade vita GUI-pixlar** efter kravet på unika originalmasker. Exakt fyra, och endast fyra, separata godkända originalfigurer uppnås **inte**.
- Maskfel beror inte på en 270-linjers failure i den korrigerade bilden; de finns även med korrekt 262-raders NTSC.

De tre verkliga P1-stroberna i variant B har Stella-stopp **före** `STA RESP1` på scanline119 / bank0 vid CPU-cykler **16, 35, 54**, alltså två intervall om 19 CPU-cykler = 57 TIA-färgklockor. Den potentiella fjärde figuren skulle komma från det automatiska mediumkopiefönstret; den har ingen självständig fjärde RESP-position.

## Slutsats och rekommenderad MAIN-hantering

**R1d fyra olika exakta originalmasker: FAIL i båda prövade implementationerna.** Detta bevisar inte att varje tänkbar TIA-metod är omöjlig. Det visar att man inte kan skala den lyckade trefigurskärnan enbart genom att växla `NUSIZ1` till tre-close. Kopietriggern spar CPU-strober men skapar oönskade dubbletter och tvingar ytterligare bitmapbyten in i mycket snäva fönster. All formell fler-NPC-grind förblir blockerad.

**Viktig aktuell positiva baslinje:** [R1c tre olika masker, begränsat oberoende tredje X, 600/600 lokalt PASS](https://github.com/Odourman/let-me-out/actions/runs/43786384041). Forskning kan nu prioritera en annan avlastad rasterlayout, kontrollera vad som faktiskt kan förberäknas före varje rad, eller en separat kvalitativ flicker-/designavvägning via MAIN om hårdvaran inte medger sex fullständiga samtidigt. Sådan avvägning innebär **inte** automatisk waiver.

**Grindar:** R1 kräver fortsatt sex individuellt placerade originalandroidsilhuetter på samma Y med P0/M0 och senare PF-/R2-belastning. Ingen R1 PASS, ingen PR-merge, inget nytt ROM-implementationsteg eller ändrade användarbeslut. Oberoende VERIFICATION återstår.
