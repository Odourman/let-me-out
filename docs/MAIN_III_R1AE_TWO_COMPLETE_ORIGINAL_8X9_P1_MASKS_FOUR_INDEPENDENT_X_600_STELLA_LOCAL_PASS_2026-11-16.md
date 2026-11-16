# Let Me Out! – MAIN III R1ae: två olika FULLSTÄNDIGA original-8×9-androidmasker, individuella X och ett gult skott på samma rasterhöjd

**Datum 2026-11-16. Status: `LOCAL_RESEARCH_PASS_R1AE_TWO_ORIGINAL_MASKS_600`.** Inte fullt v0.18 R1-PASS, inte godkänd 6-NPC-fri-X, inte ROM DEVELOPMENT implementation och inte oberoende VERIFICATION. Ingen merge till `main` eller PR #7.

## 1. Reproducerbar absolut evidens

- [**GitHub Actions #43857799040: SUCCESS**](https://github.com/Odourman/let-me-out/actions/runs/43857799040). Testad exakta källcommit **`18bbfaa1e500feee93ca85ab446d5915071d9030`** på `research/main-iii-r1ae-late-grp1-finish-20261116`.
- [**Fullständig körningsartefakt #14222326030**](https://github.com/Odourman/let-me-out/actions/runs/43857799040/artifacts/14222326030): **622 ZIP-poster**, inklusive **600 autentiska konsekutiva Stella 6.7.1/X11-PNG**, originalbaserad genererad 6502-source, fullständig DASM-listing/symboler, 600-raders CSV, `summary.json`, 16 KB F6/NTSC ROM och full build-chain-kod.
- Nedladdad råevidens ZIP SHA256 **`0a28cc3eca3c86035e1e17548ad6ef3020cf23b638feca0d8f43c424c3dd0dd2`**; **ZIP CRC PASS**. En separat nedladdningsgranskning av 600 autentiska PNG/CSV fann **600/600 strikta PASS**.
- **Faktisk ROM:** 16 384 byte standard **F6/NTSC**, SHA256 **`05606a5fd7426df00941be5621ca46c113df794c4ac3fa0f00f0e15cca66a993`**. Alla fyra 4096-byte-banker i demonstrationsfilen är identiska; inga nya mapper-/hotspottekniker antas eller testas.
- Toolversioner enligt Actions: **DASM 2.20.14.1**, Debian/Ubuntu package-string `2.20.15~20201109+really2.20.14.1-2`; **Stella 6.7.1** (`6.7.1+dfsg-1build2`).
- Generatorn pinnar tidigare äkta R1ad-ROM SHA256 `38d910cc9980c9f6d8f57303df02f3cd87c0fe8ab32dbb19041786a9406a14f1`, som i sin tur pinnar tidigare R1ac SHA `af47683fccff5fa48546de9c81032502ccf2ea7a980de90ed1880812789a7f30` och ursprungs-Venetian-källblob `a25c92adb4ca5087eeace674e371be98b273ae5b`. Reproduktionen kräver att hela källgrenen checkas ut, eftersom bygggeneratorerna är hierarkiska. Alla källor ligger i samma Gren.
- Exakt originalgrafik i `MaleRows`, `FemaleRows`, `PlayerRows`: **nio 8-bitars bitmaprader per mask**, omvänd tabellindexering Y=8..0, inte modifierade och inte upprepade till 14/15 rader. Detta är därför en betydligt renare 8×9-bitmask-invarians än tidigare fem-NPC-14-radsexperiment.

## 2. Cykelneutral teknik – varför det fungerar

En skärmrad har **76 CPU-cykler / 228 TIA color clocks**. Första `STA RESP1` utlöser P1 närkopian under `NUSIZ1=$01`. Efter andra `STA RESP1` byts `GRP1` till andra förladdade originalmasken med `STX GRP1`. Fyra förberäknade kernelvarianter har olika resp-strobcykler men samma instruktionsprofil.

**Tre riktiga steg i faktisk Stella-beviskedja:**

| Research variant | Första mannens `GRP1` CPU-end | Riktigt resultat |
|---|---|---|
| **R1ac** [#43856319003](https://github.com/Odourman/let-me-out/actions/runs/43856319003) | **c7** | **300/600** strikta PASS; övriga 300 hade **4 vita första-rad-spökpixlar** var; inga saknade originalmaskpixlar |
| **R1ad** [#43857306216](https://github.com/Odourman/let-me-out/actions/runs/43857306216) | **c33/c35** | **487/600** strikta PASS; kvarstående 113 har exakt **2 vita spökpixlar** (GUI x67–68, y96) vardera |
| **R1ae** [#43857799040](https://github.com/Odourman/let-me-out/actions/runs/43857799040) | **c35/c37** | **600/600 FULLT lokalt forsknings-PASS**; **0** extra pixlar, **0** saknade bitmapdelar |

**Specifik R1ae-ändring relativt R1ad:** En existerande `NOP` (2 CPU-cykler) flyttas **från efter till före `STA GRP1` på första skottraden**. Totala CPU-cykler och samtliga `STA RESP1`-deadlines förblir IDENTISKA. Den avsiktliga P1-kopian hinner läsa första originalmasken, men P1:s tidigare oönskade huvudkopieutmatning hinner inte få den vita grafiken. Detta är en observerad Stella-effekt, inte ett generellt TIA-hårdvarubevis för alla avstånd.

**Exakta fyra kompilerade registerfaser:**

| Mode | P1 `RESP1` #1 CPU | P1 `RESP1` #2 CPU | första `STA GRP1` CPU | andra `STX GRP1` CPU |
|---|---:|---:|---:|---:|
| C | 30 | 42 | 35 | 45 |
| D | 32 | 42 | 37 | 45 |
| E | 30 | 44 | 35 | 47 |
| F | 32 | 44 | 37 | 47 |

Source har ingen villkorlig branch på själva nio-raders-bandet. Varje variant väljs före bandet utifrån `FRAMELO & 3`, och två `RESP1` sker på varje synlig rasterrad, `VDEL0/1=0`, `NUSIZ0=$00` (en gul spelare och enkel M0), `NUSIZ1=$01` (close). M0 aktiv bara en rasterrad i mitten, med en tvåpixlig gul symbol.

## 3. Pixelbevis över 600 verkliga bildrutor

| Strikt kriterium | Utfallet från faktisk Stella 6.7.1 |
|---|---:|
| Fysiska 600 verkliga X11-PNG och nummer från debugger | **600/600** |
| NTSC 262 rasterlinjer | **600/600** |
| Stor originalman **alla nio 8x9-bitmaprader** | **600/600**, **0 saknade pixlar** |
| Stor originalkvinna **alla nio 8x9-bitmaprader** | **600/600**, **0 saknade pixlar** |
| Båda på **identiskt nio-raders rasterhöjdband** | **600/600** |
| Extra vita pixlar / tidig P1-kopia | **0** |
| Originalgul P0-spelare, komplett mask | **600/600**, **0 saknade pixlar** |
| En ensam gul M0-testprojektil, mittenraden | **600/600** |
| Fyra olika två-X-varianter med separat X-ändring | **4/4 mätt** |
| Samtliga villkor samtidigt | **600/600** |
| Saknade eller felade frame-ID, trasig ZIP eller fel ROM-format | **0** |

Faktiska **lokala Stella GUI-crop-koordinater** (x är horisontell pixel inom en 900x300-screenshot-beskärning, **inte TIA-CC**):

| Mode | Stor man originalmask-X | Stor kvinna originalmask-X |
|---|---:|---:|
| C | **87** | **159** |
| D | **99** | **159** |
| E | **87** | **171** |
| F | **99** | **171** |

**Independens uppmätt:** C→D flyttar **endast** mannen +12 GUI-pixlar; C→E **endast** kvinnan +12; C→F båda. En separat nedladdad bildgranskning beräknade SHA256 över spelregionens råa RGB-data för **samtliga 600 PNG**: exakt **fyra unika stabila bitmaphashar**, en för varje positionspar. Det finns ingen annan spökfärg/extra vit pixel mellan en moderepetition och nästa.

## 4. Viktig status/auktoritet för MAIN

**Detta är ett verkligt positivt R1-DELPROV, inte R1 C01/C04-PASS.** Denna isolerade ROM har bara **två** samtidiga vita NPC-originalmasker (stor man + stor kvinna), en fullstor gul P0-spelare och en M0-symbol. Det finns **ingen** andra stora man, ingen andra stora kvinna, ingen liten man, ingen liten kvinna, inga totalt sex individuella NPC, inget fullhorisontellt oberoende X-område, ingen stress med nära/överlappande X, inga integrerade R1–R4-nyckel-/dörrbudgetbevis eller systematiska flimmerkvoter. Ett fåtal begränsade diskreta positionspar bevisar **inte** generellt fri-X-placering på alla 160 TIA-color-clocks.

På P0/M0 finns här `NUSIZ0=0`, vilket undviker hela den tidigare R1y–R1ab-konflikten men inte går att förutsätta när vi senare använder P0-kopior för fler NPC på samma Y. FULL v0.18-scen kräver **sex NPC + player + shot**, och de accepterade maskerna får inte ändras. Därför är **R1 fortfarande FAIL/BLOCKED** och ROM DEVELOPMENT:s tidigare STOPP återstartas inte automatiskt av det här researchbeviset.

### Nästa rekommenderade MAIN-grind

1. **Preservera R1ae som reproducerbar R1b-teknikbaseline**, på separat researchgren. Repetera med särskilt nära och långt valda oberoende X-par samt **visuell överlappningsstress**. Redovisa de faktiska begränsningarna för P1-närkopia, inte bara fyra bekväma lägen.
2. **Separat teknikskalning:** lägg till tredje original-NPC och därefter till fjärde/sextet, en resurs i taget. Varje tillägg måste ge verifierbara originella 8x9-bitmaps, player, M0, 262 scanlines och inga spökpixlar med nya registrets deadlines. **Inget PASS-extrapoleras automatiskt.**
3. Först när faktisk **sex-NPC-feasibility** visats med accepterat flimmer och inga designwaivers, får MAIN prioritera den fulla R1–R4-implementationen under gällande, separat kontrollerat mandat och överlämna exakt commit/ROM-SHA till självständig VERIFICATION.

**Tekniskt inspirationsursprung, inte kopierad kod:** originalprojektets 30 trick **#01 sprite multiplexing, #02 mid-scanline GRP rewrites, #14 multiple display kernels, #15 NUSIZ copies, #24 cycle-exact scheduling** och Andrew Towers TIA-retrigger-hypotes. **Ingen tredjepartsdisassembly inkluderad**.

**Integritet:** Endast separat researchgren, inga commits i GitHub `main`, ROM DEVELOPMENT PR #7 eller oberoende VERIFICATION issue #8. Ingen ny integrationsteg eller byte av standard-F6-banking.
