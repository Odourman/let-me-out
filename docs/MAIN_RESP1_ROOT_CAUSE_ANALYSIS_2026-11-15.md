# MAIN – RESP1: avgränsad rotorsaksanalys och reproducerbar felsökningsplan
**2026-11-15. Projekt:** Atari 2600 Let Me Out! Endast MAIN-teknikanalys och forskningsråd. **Ingen ändrad ROM-kod, ingen självständig Stella-körning, ingen ny kodauktorisation eller oberoende VERIFICATION.**

## Baslinje och bevisgräns
- Senast kontrollerad utvecklings-HEAD: `82667dae033f70570dce903f8e1d4866528be02a`, [draft PR #7](https://github.com/Odourman/let-me-out/pull/7), inte mergad.
- [Venetian Blinds-rapport](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/TO_MAIN_VENETIAN_BLINDS_2026-11-15.md); [ursprungligt evidens-ZIP](https://drive.google.com/file/d/1toh8XDyCBk2LckDwrm4oAQHJ_E4RSEfP/view), SHA-256 `b8141a874ad1e10de1ec958d1af36f46c51cc7a548181370ccfe6714dcfda271`, 94/94 interna manifestposter kontrollerade av MAIN.
- Tre verkliga DASM/Stella-diagnoser FAIL för 2 kompletta oberoende silhuetter. Sex exempelbilder har 262-scanline-HUD; TIA-write-cykeltrace **inte** godkänd. Här görs **statisk analys av den levererade assemblerkoden**, inte ny verifierad runtime-mätning.
- Separat fryst [VERIFICATION #8](https://github.com/Odourman/let-me-out/issues/8) gäller `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, inte nya Venetian-HEAD.

## Fynd 1 – instrumenteringsskriptets brytpunkt mäter inte RESP1
I [`ci_pc_cycle_probe.sh`](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/ci_pc_cycle_probe.sh):
```
base #10
frame #12
break $f0a8
frame #1
step
print _fCount
print _scan
print _sCycles
```
Detta körs som `autoexec.script`; inspelat originalfoto `evidence/pc_cycle_breakpoints/f0a8/pc_break_image.png` visar **PC `$F047`, scanline 0**, inte breakpoint vid `$F0A8`. `frame #1` flyttar fram till nästa frame-gräns, efterföljande `step` stegar där. Den faktiska TIA-skrivningen mäts alltså **inte**. Stella-dokumentationen instruerar att en satt `break` ska följas av **`run`** för att emuleringen ska stoppa vid breakpoint, och att PC där pekar på instruktionen *innan* den körs: https://stella-emu.github.io/docs/debugger.html.

**Reproducerbart verifieringsupplägg för ROM DEVELOPMENT, utan att påstå testad framgång:**
1. Kontrollera att `proof.lst`/ROM-hash verkligen matchar. DASM-listningen i levererad ZIP har `STA GRP1` vid `$F0A1`, `STA RESP1` vid `$F0A8`, nästa `STA GRP1` vid `$F0B6` och `STA RESP1` vid `$F0BD`.
2. I Stella 6.7.1: fram till vald frame, `clearBreaks`; `break $f0a8`; `listBreaks`; **`run` (inte `frame #1`)**. Alternativt prova `runToPc $f0a8`; mätmetoden måste verifieras med faktisk stoppbild.
3. Kräv PC `$F0A8`, korrekt F6-bank, meningsfull `_scan` och `_sCycles`, samt breakpoint-status. Inget av detta får ersättas med en förväntad adress.
4. Vid verklig träff: registrera cykel **före** `STA RESP1` och efter exakt ett `step`; upprepa för `$F0BD`. Koppla varje skrivning till pixelutfall på nästa skärmrad och kontrollera om ROM körs via spegeladress (`$10A8` etc).
5. Om `run` inte träffar: avgränsa separat skriptladdning, aktiv bank, PC-mirror, breakpoint toggle och eventuellt `runToPc`/TIA-write-trap. Resultatet för T07 är `INCONCLUSIVE` tills faktisk träff påvisas.

## Fynd 2 – stark statisk hypotes: same-line RESP1 ompositionerar i praktiken efter den avsedda bildpunkten
Ursprunglig [`vb_9_interleave.asm`](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/vb_9_interleave.asm) gör per rasterrad:
```
STA WSYNC
LDA #mask
STA GRP1
LDX MALE_DELAY eller FEMALE_DELAY
DEX/BNE ...
STA RESP1
LDA #player
STA GRP0
LDA #shot
STA ENAM0
```
**Hårdvarumodellen:** TIA Player Position Counter omstartas av `RESP1`, men själva omstarten startar inte en ny *huvudkopia* omedelbart. TIA-hårdvarunoter beskriver hur den nya startpositionen för huvudkopian blir synlig på **nästa och efterföljande scanline**, efter att motorn räknat runt; se https://retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php, och refererad hårdvarurealisering https://github.com/rejunity/Atari-2600-FPGA/blob/main/TIA.v. Detta är en förklaring att pröva, inte en uppmätt trace från vår ROM.

Med utvecklarens **statiska** cykelschema ger `MALE_DELAY=4/5` ungefär `STA RESP1` vid CPU-cykel **30/35**, `FEMALE_DELAY=8/9` ungefär **50/55**. Med 68 HBLANK-färgklockor och cirka 5 färgklockors fördröjning motsvarar detta nominellt ungefär X **27/42** respektive **87/102** (färgklockor); faktiskt X måste mätas och kan påverkas av HMOVE/TIA-fas.

**Mekanism att undersöka:** den tidiga mannen-resetten på nästa scanline kan ske **innan** kvinnans senare förberedda X-position börjar ritas. Den sena kvinnan-resetten hinner däremot ske efter den tidiga positionens ritstart och träder in först inför nästa scanline, som i sin tur återställs tidigt. Resultatet kan då bli bara vänster X-grupp – precis som i leveransens sex bilder (`vb_9_interleave` vitt GUI-X 158–173, 5 rader; `vb_18_doubled` samma grupp, 10 rader). Detta är **en specifik, testbar källkodshypotes**, inte ett redan definitivt fastställt TIA-fel.

**Separat datalogisk begränsning:** `MALE_REQ_X/FEMALE_REQ_X` uppdateras i RAM, men inom de synliga raderna används **bara delay-tabellerna** för `RESP1`. Att RAM-tabellernas sexvärde ändras är alltså inte bevis för oberoende renderad X.

## Fynd 3 – interfoliering av två fullständiga 8×9-masker i 9 linjer kan inte räcka utan ytterligare teknik
Varannan-linje-schemat ger max 5 av 9 originalrader för man och 4 av 9 för kvinna per frame i samma nio-linjersband. Detta är en deterministisk **källdatabegränsning**, oavsett om `RESP1` korrigeras. 18 linjers dubbelhöjd är diagnostiskt, **inte godkänd skala**; `VDEL1` ger ingen extra P1-kanal. Inte ens en korrekt ompositionering skulle ensam innebära full R1-PASS.

## Snäva föreslagna tester – ingen ny fas eller tyst kodorder
- **P0: instrumentation-only:** verifiera att `run`/alternativet `runToPc` faktiskt stoppar på `STA RESP1`, inte frame-start. Rapportera verklig `_scan`, `_sCycles`, PC och bank före/efter instruktionen.
- **P1: separat positioneringskontroll** (endast om inom befintligt uttryckligt R1-scope): en P1-originalbitmap, stabil X-position satt **före rasterbandet**, P0-spelare och M0-skott. Bekräfta grundpositionering utan inline-RESP.
- **P2: kontrollerad enlinjesförskjutning:** jämför nuvarande `GRP1`-före-`RESP1` mot förberedelse av P1-position på föregående rasterrad, utan att ändra kraven. Testa om höger-X-fragment nu uppstår och om förtidig nästa reset klipper det.
- **P3: acceptansgräns:** bara om P1/P2 ger faktiskt separat synliga positioner, utvärdera om hela ursprungliga 8×9-maskerna alls kan visas på samma höjd. Innan det: **inga nya 600-frame-uppskalningar**; ingen full R1-acceptans.
- Vid fel: `FAIL` eller `INCONCLUSIVE` per delprov och exakt stödd orsak. Stanna om fortsättning kräver annan kassetthårdvara, färre androider, förändrade originalmasker eller ny implementation scope.

**Kvarstående status:** R1 **FAIL/BLOCKED**, Venetian T07 **INCONCLUSIVE**, R2–R4 **NOT_RETESTED**, oberoende VERIFICATION ny commit **NOT_RUN**. PR #7 förblir draft/ej merge. Ingen automatisk ROM-auktorisation genom denna MAIN-teknikrapport.
