# Let Me Out! – ROM DEVELOPMENT v0.18 / Stella 6.7.1 utvecklarförtest

Datum: 2026-11-15. Auktorisation: GitHub Issue #6 och `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md`. Endast NTSC R1–R4.

**STATUS: BLOCKERAD / FAIL för grafikacceptans.** Detta är ROM DEVELOPMENT:s egna tester, inte oberoende VERIFICATION. Ingen fullspels- eller PAL-auktorisation finns.

## Källor och miljö
- Projekt: https://github.com/Odourman/let-me-out
- Draft PR: https://github.com/Odourman/let-me-out/pull/7
- GitHub Actions run med 8 bildruteexakta debugger-vyer: https://github.com/Odourman/let-me-out/actions/runs/43743513953
- Installation: Ubuntu 24.04, DASM paket `2.20.15~20201109+really2.20.14.1-2`, Stella `6.7.1+dfsg-1build2`, Xvfb med mjukvarurendering.
- Ingen DASM/Stella-installation i lokala ChatGPT-containern; verkliga körningar skedde i GitHub Actions-runnermiljön.
- ROM SHA-256: `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`. DOS/Unix bytejämförelse `cmp`: DASM-byggd 16 384-byte F6-ROM identisk med den ursprungliga Python-byggda ROM:en. DASM är nu hård CI-spärr, inget `continue-on-error`.

## R1: sex androider / spelare / skott – blockerande FAIL
- Sex vita PF-figurer återges samtidigt på samma höjdband, P0 är gul spelare, testsymbolskott är vit PF-bit.
- **FAIL C01/C03/C04:** spelarnas riskobjekt är korta horisontella figurer, inte tydliga människor. Fyra godkända silhuetter (två stora män, två stora kvinnor, en liten man, en liten kvinna) är inte åtskiljbara.
- Det är ett resultat från Stella Debugger frame #130, inte en schematisk simulering. Figurantalet har INTE minskats; felet beror på 4 PF-cellers grova horisontella upplösning.

## R2: O1 – lokal nyckelkontroll PASS, grafikhelhet FAIL
- Frame #625: nyckeln synlig i guld. Frame #715: nyckeln skymd. Frame #835: nyckeln synlig igen på samma koordinat.
- Alla tre debuggerbilder visar RIOT RAM `KEY_X=$1B` (27), `KEY_Y=$50` (80), `KEY_ALIVE=$01` (1).
- **PASS T05 endast som lokal egenkontroll.** De fem white PF-androidernas läsbarhet uppfyller inte C02/C03 i nuvarande form. K11/K09-valet och långa oavbrutna blockeringar saknar full Stella-film.

## R3: planerad C02-karta / asymmetrisk högerdörr
- Frame #1225: teknisk stängd markör, *lila* på skärmen trots kodens avsikt att vara brun. `$64` är olämplig NTSC-testfärg för brun.
- Frame #1335: låst orange vertikalt streck synligt på högerkant, men svart mitturtag ger ingen tydligt godkänd rundad/kilformad nyckelhålssymbol. Ingen slutlig designwaiver är given.
- Frame #1420: högerkanten har en öppning i dörrbandet, medan vänsterkanten fortfarande är stängd. Teknisk asymmetri fungerar på minst denna mätpunkt.
- **PASS T09/T10** som utvecklarens punktvisa Stella-kontroll, **FAIL T11/T12** färg/symbol. Väggarnas nuvarande vita PF-färg är inte det planerade bruna visuella målet.

## R4: rörelsestress
- Frame #1925 är fångad i verklig Stella med förprogrammerad stressprofil. Det finns ännu inte 600 filmade/loggade sammanhängande bildrutor för variation och eventuell flimmerbedömning. **T08 INCONCLUSIVE.**

## Rastertiming – mätning kontra ej mätning
- Stellas GUI visar **262 scanlines för föregående bildruta** i var och en av de 8 debugger-fångsterna. Proven ger viss punktvis stöd för stabil NTSC-timing och korrekta F6 bank 0/1/2/3.
- **Inte visat**: 600 oavbrutna 262-linjers bildrutor per kritisk scen, eller faktisk logg över TIA-registerskrivningar med exakta CPU-cykelpositioner för belastade scanlines. T01/T07 därför **INCONCLUSIVE**, även om den äldre fristående CPU-modellen tidigare körde 600 per scen.
- Offline-kernelmodellen uppskattade PF0/1/2-vänsterwrite vid cykel 7/14/21 och högerwrite vid 36/43/50. Dessa får **inte** presenteras som Stella-mätdata.

## ROM / RAM / TIA
- F6 med fyra 4096-byte banker, bytevärde 16 384; F6-hotspots $FFF6..$FFF9.
- 8 RAM-byte $80..$87 för SCENE, FRAMELO, FRAMEHI, PHASE, KEY_X, KEY_Y, KEY_ALIVE och DOORCOLOR. Stock 128-byte RIOT-RAM i konsolen.
- PF0/PF1/PF2 ritar sex/fem androider, skott och C02-rummets väggar. P0 ritar gul spelare. P1 ritar guldnyckel i R2/R4 och låst dörr i R3. M0/M1/BALL används inte.
- PF-upplösning 4 färgklockor/cell är det observerade läsbarhetsproblemet; fler ROM-banker ökar inte antalet samtidiga hårdvarusprites eller 76 CPU-cykler per scanline.

## Full 16-testrapport
Läs `docs/TEST_RESULTS_16_STELLA.csv`. Utvecklarbedömning: **5 lokala PASS** (T05,T09,T10,T14,T16), FAIL 5 (T02,T03,T04,T11,T12), INCONCLUSIVE 5 (T01,T06,T07,T08,T13), NOT_RUN 1 (T15). Totalt 16. Varken PASS-med-waiver eller oberoende slutresultat.

## Blockerare och endast två förslag till MAIN
1. Utred **scanline-multiplexning av P0/P1 med bankförberäknade 8x9-masker** för humanoiderna; skott/nyckel/dörr kvar, sex androiders logiska och synliga representation bibehålls. Behöver ny mätning av 76-cykelbudget och begränsat flimmer. Detta är en teknisk hypotes, inte verifierad åtgärd.
2. Alternativt utred **bytevis ändrat PF-/TIA-kernel med tätt uppdaterade maskdata och prioriterad spelarsynlighet** samt oförändrade sex androider och O1-logik. Testa om fulla 8x9-silhuetter ens ryms; acceptera inte oläsliga fiender.

**Stoppvillkor:** Ingen tyst förenkling av figurantal eller godkänd svart nyckelhålssymbol, ingen integrerad gameplay. MAIN beslutar ev. nästa *diagnostiska* underuppgift inom redan godkänd v0.18, och separat VERIFICATION måste bygga om och bedöma. Ingen merge till `main` innan relevant process.

## Viktig evidensbegränsning
De 8 `debugger_screen.png` är oredigerade, direkta skärmdumpar från Stella 6.7.1 och kan läsas med Frame/Scn Ln/RAM/bank. `evidence/crops` är beskurna utsnitt. Stellas `saveSnap` från debuggerläget gav 320x228 svarta stillbilder i denna CI-körning och **används inte som bildbevis**. Stellas interna debugger-preview är korrekt och återges i fullskärmdumparna. Inga ändrade eller syntetiserade pixelbilder är märkta som Stella-original.
