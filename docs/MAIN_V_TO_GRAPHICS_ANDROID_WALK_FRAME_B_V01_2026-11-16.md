# LET ME OUT! – MAIN V till GRAPHICS
## ANDROID WALK FRAME B v0.1 – fyra originaltyper, strikt designstudie

**Datum:** 2026-11-16. **Status:** AKTIVT NYTT AVGRÄNSAT GRAFIKUPPDRAG. **Enbart pixelgrafik-/animationskandidater**, inte acceptans av nya bytes i ROM, ny NPC-canon, gameplayregler, eller rätt att börja en senare R1/R2/R3/R4-implementation.

### 1. Bakgrund och anledning

GRAPHICS PLAYER SPRITE v0.3 är avslutad som grafiskt underlag med resultat `8x9 WEAPON READABILITY STILL FAILED`. MAIN föredrar **V03_B som tillfällig jämförelsekandidat**, men INGEN spelarbitmap är slutgodkänd. Spelarvapenfrågan pausas för användarbedömning och eventuell **senare separat** annorlunda grundpose, inte obegränsad v0.4.

Det tidigare visuella målregistret tillåter **en extra gångbild per androidutseende OM tekniskt möjligt**, och accepterar glidande rörelse som reserv. Detta uppdrag utvecklar sådana förslag **utan att påstå att R1-kerneln har plats för dem**.

Källor som ska kontrolleras live före design:
- [Ursprungligt designregister och originalets fyra exakt definierade masker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json), original Git-blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.
- [Kompletterande beslut](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md).
- [GRAPHICS ursprungliga rollinstruktion](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md).
- [PLAYER SPRITE v0.3 mottagning](MAIN_V_GRAPHICS_PLAYER_SPRITE_V03_RECEIPT_2026-11-16.md) och [v0.3 faktisk jämförelsebild](https://drive.google.com/file/d/1MgpxAg2rXrRO7G7mn8yGi4zqq-DRkHjI/view).
- [Originalöverlämning med användarens ritade figurer](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view).
- [Aktuell projektstatus](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md), särskilt eventuellt nytillkomna uppdrag. Läs verkliga källor, inte Memory.

### 2. Bindande originalgrafik, INGEN ny Frame A

För varje av följande fyra originaltyper används **exakt originalets 8×9 bitmap som `FRAME_A` – inte "förbättrad" version**:
1. `large_male` / 2 exemplar i planerat spel: 9 synliga pixelrader.
2. `large_female` / 2 exemplar: 9 synliga pixelrader.
3. `small_male` / 1 exemplar: exakt samma 8×9 lagringsformat, **sex** synliga rader (rader 2–7, nollbaserat); övriga tomma.
4. `small_female` / 1 exemplar: samma sex synliga rader inom 8×9.

Varje `FRAME_B` får förändra **ben-/fotpositioner** och vid behov *ett fåtal arm-/kroppspixlar* för en synlig men inte uppblåst stegförskjutning. Bevara originaltypens igenkännbara huvudsilhuett och ungefärliga kroppsmassa. Håll samma övergripande maxdimensioner, horisontella objektstart, höjd och golv-/fotankare inom samma 8×9-ruta. För små NPC:er ska 8×9-raderna 0,1,8 fortsatt vara noll; de ska fortfarande se mindre ut, men använda samma kollisionsyta. **Ingen avsiktlig blinkning, tredje sprite, färgskifte eller nya TIA-objekt som "animation".**

### 3. Uppdrag – fyra konkreta B-masker, högst en primärkandidat per typ

- Skapa **EN** tydlig `FRAME_B`-bitmap per originaltyp, totalt **fyra nya 8×9 1-bitarsmasker**. För större typer ska alla 9 rader ha åtminstone en synlig vit pixel; för de små ska endast raderna 2–7 innehålla vitt. Jämför samma skala och fotposition med låsta `FRAME_A`.
- För varje typ: två separata 8×9-bitmapbilder samt en A→B→A-alternation som existerande designförslag, både som fysisk 1× och nearest-neighbor 4×/20×. Vid animations-GIF: använd oförändrad bitmapdatabaserad ram och tydlig timingangivelse i bildrutor. En saknad GIF får inte stoppa fullständig data-/PNG-leverans.
- Visa en **samhöjdsscen** med två stora män, två stora kvinnor och båda små i naturlig storlek. Håll gul spelare, M0-skott, brun PF-vägg tillgängliga som statiska jämförelsesiluetter; dessa får inte vara utlovad ROM-/Stella-scener.
- Testa visuellt att de två paren och de små typerna inte byter identitet eller ser ut att hoppa vertikalt när A/B växlas; ingen "head bob" genom att flytta hela masken en pixel om ursprungligt fotankare då ändras.
- Bedöm rörelseläsbarhet **utan** etiketter vid 1×, med kontrollerad skillnadsbild och svartvit kontrast. Om variant B bara ser trasig eller flimrande ut, markera `WALK_FRAME_B_UNREADABLE` och förklara varför. Utgå inte från att ett förslag är lyckat för att antalet ändrade pixlar är stort.
- **Hårdvarukonsekvens separat:** Beräkna bytes som behövs för fyra nya 8×9-matriser (råbitmap 4×9 = **36 byte**, exklusive tabell-/bank-/selector-/kernelkostnader), antal mask- och bildbytes ändrade per källrad; påstå INTE att extra frames är "gratis" i 76 CPU-cykel-bandet. ROM DEVELOPMENT II:s 6-android P1-rasterkernel är inte generellt fri-X/Y och saknar visad kapacitet för gångbildbyte. Lista nya runtime-krav som **TEKNISK HYPOTES / EJ IMPLEMENTATIONSGODKÄND**.

### 4. Leverans och stopp

En grafisk `ANDROID_WALK_FRAME_B_V01_TO_MAIN.md` med:
- Fyra exakta, oförändrade original`FRAME_A` + fyra nya `FRAME_B`, per-källrad 8 binärbitar och hex, faktisk pixelantal, avvikande bitkoordinater och oförändrad käll-Jason SHA/blob.
- Ett manifest med PNG/GIF/JSON och egen kopierbar audit eller script som jämför A mot officiell källa och kontrollerar B dimensioner, synliga rader, färg/alpha, underkropp och pixel-CRC.
- 1×, 4×, 20× samt minst en skala-/kontrast-/A-B-sekvensvy med originaltyperna jämte varandra. Tydlig markering `GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`.
- **Fungerande Drive-länkar** från den dedikerade projektmappen, eller verifierbara sandbox-artifakter, inte bara ord som "Ladda ner". Historisk v0.2-länkbrist är nu löst; håll samma konkreta leveransstandard.
- Bedöm kort om vi har fyra **visuellt rimliga animationskandidater** eller om glidande rörelse bör vara reserv. Ingen fortsättning till fler animationstyper utan MAIN:s återkoppling.

**Avsluta efter exakt dessa fyra B-kandidater.** Inga nya Frame A-masker, ingen ny spelarpose, dödsanimation, nyckel-/dörrgrafik, kamera-/speldesign, fullspelsimplementation eller publicering av en ny grafikkodversion genom detta uppdrag.

### 5. Säker projektskillnad

GRAPHICS får arbeta med fristående grafik i separata, icke-kanoniska paket. **Ingen** ändring av `design/NPC_REFERENCE_8x9_masks.json`, ritade original, GitHub `main`, ROM DEVELOPMENT:s grenar, PR#7, Issue #8, kanoniska rum eller annan gameplaydata. **Ingen Stella-/DASM-utveckling beställd**, ingen status `TECHNICALLY TESTED` före separat faktisk ROM-order och verifierbar emulatorbild.

**R1-F3** har en utvecklarrapport med en verklig misslyckad index0 +1-cykel-probe, men detta påverkar inte den visuella ursprungsreferensen. Full R1 fortsatt BLOCKED. Skillnader mot original ska redovisas, inte tyst design-waiver-ersättas.
