# Let Me Out! – MAIN:s tekniska deluppdrag inom ROM-diagnostik v0.18

**Datum:** 2026-11-15  
**Projekt:** Enbart `Odourman/let-me-out`  
**Roll:** MAIN, teknisk källgranskning och nästa avgränsade åtgärd. **Inte** oberoende VERIFICATION eller ny ROM-fas.  
**Fryst utvecklarbaseline för oberoende granskning:** `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`  
**PR:** https://github.com/Odourman/let-me-out/pull/7 (DRAFT, EJ MERGE)  
**Auktorisation:** https://github.com/Odourman/let-me-out/issues/6 (endast NTSC/R1–R4)  

## 1. Ny verifierbar MAIN-observation: den befintliga kerneln har nästan ingen cykelmarginal

Granskad källa: `rom/v018/src/bank0.asm` på ovanstående commit. Samma programdel används i de fyra genererade bankerna.

**Båda huvudlooparna `FullLoop` och `BandLoop` har en beräknad normaliteration på 74 CPU-cykler** vid tagen slutgren och utan sidkorsning i de 256-byte sidjusterade ROM-tabellerna:

| Instruktionsgrupp | Cykler |
|---|---:|
| `STA WSYNC` | 3 |
| Sex `LDA table,Y` + `STA PF0/PF1/PF2`, vänster/höger | 42 |
| Fyra `NOP` | 8 |
| Två `LDA table,Y` + `STA GRP0/GRP1` | 14 |
| `INY` | 2 |
| `TYA` (`FullLoop`) eller `DEX` (`BandLoop`) | 2 |
| `BNE` tagen | 3 |
| **Summa** | **74** |

Atari 2600 tillåter 76 CPU-cykler per scanline. **Slutsats:** det finns endast omkring två cykler nominellt kvar i den befintliga loopmodellen, och en ytterligare registerladdning/skrivning ryms inte utan att ta bort eller omorganisera annat arbete. Ett ändrat antal NOP kan flytta en tidslucka men löser inte i sig multisprite-problemet. Detta är **statisk instruktionsekonomi**, inte faktisk Stella-cykelspårning. WSYNC/pixelpositioner måste mätas i emulatorn innan timing eller synlighet kan godkännas.

## 2. Dokumenterad TIA-resurskonflikt

Nuvarande fördelning enligt källkod och preflight:

- `P0`: gul spelare i R1/R2/R4.
- `P1`: guldnyckel i R2/R4 och högerdörr i R3. R1 använder inte P1 för en separat godkänd humanoid.
- `PF0/PF1/PF2`: sex/fem androidsilhuetter på grov 4-färgklockors rastergrid, testsymbolskott och väggar.
- `M0/M1/BALL`: oanvända i nuvarande version.

Att byta alla humanoider till `P0/P1` med enbart fler `GRP`-/`RESP`-skrivningar är **inte** en bevisad lösning: P0 krävs för spelaren, P1 krävs för nyckeln i R2, alla sex androiders höjdband måste bevaras och aktuell kernel använder 74/76 cykler. Dessutom måste fyra distinkta 8×9-silhuetter kunna läsas. Horisontell/samma-scanline-spriteåteranvändning får betraktas som en **hypotes** tills ett konkret per-scanline-schema finns.

## 3. Extra blockerare: debuggerfångstens mätinstrumentering

I de faktiska fullständiga Stella-bilderna, exempelvis `R1_frame_130_debugger_full.png` och `R3_locked_orange_frame_1335_debugger_full.png`, visas röd feltext om saknade script-, listing- och symbolfiler, exempelvis `/letmeout.script` och scenario-specifika `.lst`/`.sym` under `evidence/stella_live/`. Detta **ogiltigförklarar inte att skärmbilden kom från Stella**, men visar att den planerade automatiska debuggerinstrumenteringen inte genomfördes felfritt. Enstaka indikatorer för föregående bildrutas 262 scanlines kan inte ersätta 600 efterföljande faktiskt observerade bildrutor och per-scanline-register/cykeldata.

## 4. Avgränsad uppgift till ROM DEVELOPMENT – fortsätt endast v0.18/R1–R4

**A. Först ett resurs- och cykelschema, inte ett blint spriteexperiment.**

1. Lista för R1 och R2 varje TIA-objekts visuella funktion, rasterband, horisontella placering och möjliga samtidighetskrockar.
2. Visa planerad cykelposition för varje `PF0/1/2`, `GRP0/1`, `RESP0/1`, eventuellt `M0/M1/BALL`, `COLU*` samt `WSYNC`. Räkna med faktiskt lästa bytes och 6502-grenar.
3. Beskriv exakt vilket arbete som kan flyttas ut ur visible kernel, eller vilken ny kernelstruktur som gör plats. Bankning/F6 ger inte fler TIA-objekt eller cykler.
4. Jämför högst två tekniska alternativ som redan nämnts i v0.18: (A) en välmotiverad P0/P1-/hybridmultiplexning med bibehållen gul spelare och guldnyckel; (B) en annan PF/TIA-kernel med högre läsbarhet. Bedöm genom faktisk 8×9-läsbarhet, **inte** bara sex synliga block.
5. Om båda alternativen blockeras på resurser/timing: stoppa och rapportera teknisk blockerare. Minska **inte** antalet androider, stryk **inte** godkända silhuetter eller ändra O1.

**B. Rätta mätningen före nya acceptanspåståenden.**

1. Korrigera debugger-script/symbol/listing-sökvägar i GitHub Actions; kontrollera i loggen att kommandona faktiskt laddats utan fel.
2. Kör och logga **600 sammanhängande** riktiga Stella-bildrutor för kritiska scener R1, R2 och R4 efter init. Kravet är 262 scanlines/bildruta i föreslagen NTSC-profil; avvikelser ska loggas, inte filtreras bort.
3. Fånga **verkliga** kritiska `TIA`-skrivningar med scanline och CPU-cykelposition, inte CPU-modellens beräknade spår. Identifiera korrekt samma scen, RAM-/ROM-bank och frame-ID.
4. Bevara **hela, oredigerade** debuggerbilder samt eventuella crops tydligt separerade. Undvik `saveSnap` som bildbevis om den bara ger svarta bilder i CI.
5. Sammanställ alla 16 test-ID i ny utvecklar-egenkontroll med `PASS/FAIL/INCONCLUSIVE/NOT_RUN` och bevisväg, utan att skriva över historiken på commit `561d...`.

**C. Isolera dörrfel inom R3.**

- Testa C02 med solid vänstervägg och korrekt högeröppning (delbevis finns redan).
- Utvärdera separat NTSC-väggfärg (kod `$64` gav lila i underlaget), orange port och läsbar svart nyckelhålssilhuett. Symbolen får inte tyst tas bort eller ersättas med brun port som slutligt designval.

**D. Leverans och beslutsgräns.**

- Endast på befintlig utvecklingsgren `rom-dev/v018-ntsc-diagnostic` och befintlig **draft PR #7**. Redovisa nya commit-/ROM-hashar och en delta-rapport mot `561d...`.
- Fullständiga `R1–R4`, ingen ny AI, poäng, ljud, spelstart, PAL eller fullspel.
- **Oberoende VERIFICATION** på den frysta ursprungliga committen är separat i [Issue #8](https://github.com/Odourman/let-me-out/issues/8). Eventuell senare reviderad commit kräver en egen verifieringsomgång; en tidigare PASS överförs inte automatiskt.
- MAIN får inte slutgodkänna ROM-kvalitet genom sin egen tekniska analys.

## 5. Aktuell status (inte ändrad genom detta dokument)

Utvecklarens egna resultat: **5 PASS, 5 FAIL, 5 INCONCLUSIVE, 1 NOT_RUN**. Fullständigt ROM-godkännande **nej**. PR #7 **DRAFT, ej merge**. Ingen efterföljande implementeringsfas auktoriserad. **The Cabin** och **I Love a Fish** ska lämnas helt orörda; inget Linear.
