# Let Me Out! – MAIN: spelarskala och originalsilhuetter, v0.18

**Datum:** 2026-11-15  
**Scope:** Endast tidigare auktoriserad NTSC-diagnostik v0.18, R1–R4. Ingen fullspelsutveckling eller PAL.  
**Status:** Visuell förtydligande från användaren, **inte** en verifierad ändring av ROM eller ett godkännande av R1.

## 1. Senaste visuella beslutet

Användaren korrigerade den illustrativa jämförelsebilden: **"den gula spelaren ska vara lika stor som de stora"**. Den korrigerade illustrationen accepterades med **"Ah, är bra ut. Fortsätt"**.

**BESLUT:** Spelarfiguren ska framstå som lika stor som de stora vita androiderna på skärmen. Behåll färgen **gul**, samt originalskissens kännetecken **hatt och vapen**. Detta är visuella krav – det ändrar inte rörelse, skadevärden, AI, hitbox eller antalet fiender.

**Viktigt:** AI-genererade jämförelsebilder är en pedagogisk **målskiss**. De är inte autentiska Stella-bilder och ersätter inte tidigare användargodkända pixelreferenser. Illustrationens ramfärg/placeringar ska inte tolkas som nya spelbeslut. De godkända väggarna är fortsatt **bruna**, inte illustrationens lila.

## 2. Ursprungliga fyra NPC-matriser – kontrollerad källa

Exakta 8×9-referensmasker hämtade **utan ändringar** ur `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip` → `assets/NPC_REFERENCE_8x9_masks.json`, beskrivna i `10_PIXEL_ART_REFERENCE.md` och `02_MASTER_SPEC.md`.

- Källa, originalfil SHA-256: `1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`.
- [Exakt originalreferens i GitHub](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json).
- Alla fyra figurer har **8 kolumner × 9 rader** som datamatris.
- **Stor man och stor kvinna:** synliga pixlar på **alla nio raderna**.
- **Liten man och liten kvinna:** synliga pixlar på **sex rader (rad 2–7, nollbaserat)**; de övriga raderna är tomma. Det är så de små blir mindre, trots samma matrisformat.
- Standardfördelning av sex: **2 stora män, 2 stora kvinnor, 1 liten man, 1 liten kvinna**. Samma logiska kollisionsyta för samtliga androidtyper.

Maskerna är tidigare användargodkända **visuella referenser** och ännu **inte** verifierade som faktisk TIA-grafik. Tysta byten till grafiskt enklare figurtyper är inte tillåtna.

## 3. Spelarens dimension – nytt tekniskt verifieringsmål

- **Mål i R1/R2:** den gula spelarens synliga höjd ska vara **jämförbar med de stora androidernas 9 synliga pixelrader**, vid **samma grafikskala** på skärmen. Ingen förstoring bara i presentationen eller särskild förminskning i speldiagnostiken.
- En **8×9-prototypruta** för spelaren är lämplig att utvärdera eftersom den motsvarar de stora NPC-referensernas format; den är **inte** en redan godkänd exakt spelarpixelmask.
- Spelarens **hatt och vapen** från `assets/02_USER_PLAYER_SKETCH.jpg` måste fortsatt kunna uppfattas, i den mån det är möjligt i Atari 2600-formatet. Skissen är också stilreferens, inte pixelperfekt slutasset.
- Utvecklar-ROM:ens aktuella `P0DATA` innehåller nio fyllda 8-bitarsrader i den tidigare baslinjen. Detta visar inte att den synliga figuren eller jämförelsen i Stella redan uppfyller målet. Granska den verkliga renderingen i samma höjd- och skalförutsättningar som androiderna.

## 4. Begränsat delprov till ROM DEVELOPMENT – samma v0.18

1. Använd **ursprungliga** 8×9-NPC-referenser som utgångspunkt. Redovisa tydligt om teknisk lösning avviker från dem; markera då avvikelsen, inte PASS.
2. Visa **två olika stora, vita androidsilhuetter**, en **gul lika stor spelare** och ett testskott i **samma rasterhöjdband** i verklig Stella. Visa visuellt skillnad mellan stor man och stor kvinna. Det är ett **teknikdelprov**, inte ett uppfyllt R1.
3. Redovisa verkliga CPU-cykler och TIA-objekt per kritisk skärmlinje, särskilt konflikterna mellan P0/P1, PF, nyckeln och skottet.
4. **Skala först därefter till R1:** två stora män, två stora kvinnor, liten man, liten kvinna, gul spelare med samma visuella storlek som de stora, samt ett skott.
5. Verifiera sedan **R2:** fem androider, gul spelare, statisk guldnyckel och skott samt O1-skymning och återkomst på oförändrad plats. R3/R4 och full 16-fallstestmatris kvarstår.
6. Kör separata reproducerbara tester med olika X-avstånd och gemensam/angränsande rasterhöjd. Dokumentera flimmer ärligt: mindre mängd är accepterad men oläsliga farliga figurer är blockerande.
7. Behåll **draft PR #7**, ingen merge. Oberoende VERIFICATION granskar fryst baseline i Issue #8; ny utvecklarcommit kräver senare en **egen** verifieringsomgång.

## 5. Ingen ny implementation på MAIN:s vägnar

Den här anteckningen ändrar bara testmålets tydlighet. Ingen ny ROM har byggts eller verifierats genom detta dokument. ROM DEVELOPMENT får arbeta enbart inom redan beviljade v0.18/R1–R4. Fullspel, PAL, ändrade spelregler och minskat antal androider är fortfarande förbjudna utan separat uttryckligt beslut. Inga ändringar i **The Cabin** eller **I Love a Fish**. Ingen Linear.
