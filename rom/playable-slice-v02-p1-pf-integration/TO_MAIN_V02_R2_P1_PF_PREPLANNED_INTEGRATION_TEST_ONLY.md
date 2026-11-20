## TO_MAIN_V02_R2_P1_PF_PREPLANNED_INTEGRATION_TEST_ONLY

`DEVELOPER_OBSERVED` · `TEST_ONLY` · `G5_FORMAL_OPEN` · `INDEPENDENT_VERIFICATION=NOT_RUN`

Utgångspunkt för riktig spel-ROM var `efe23bde3a1b6c6edbfc4fbf9f96c3f95dddd66a`. Blinkreferensen var `058e3e67a40e3e0b72985a814f19520ea39a910f` och den frysta P1-diagnostiken `08f0f13064e48db3b4ec106cffb00185f6cb0268`. De frysta katalogerna är separata från leveransen.

### A · P1/PF · rasterprov PASS, spelintegration kvarstår

Förberäknade verkliga PF0/PF1/PF2 från A_OPEN_01. Den stabila rastervägen behåller PF-register mellan rader. Övergångsvägen uppdaterar endast ändrade register efter att speglade pixlar från den gamla kartremsan har ritats. I tvåregisterfallet förladdas första värdet i X. Generatorn läser originalmaskerna för P0 och nyckeln från fryst ASM och SM från originalmaskfilen. Proverna jämför fem rader med guldnyckelns nya gula färg `$1E`, gul P0, vit SM, M0 och brun PF. Matrisen gäller färg och position i Gopher2600.

| Rasterprov | PX / nyckel-X | Nyckel | Spelare / SM / M0 | Brun PF | Scanlines | Resultat |
|---|---:|---:|---|---:|---:|---|
| Stabil vägg | 60 / 85 | 14/14 | 18/18 · 10/10 · 1/1 | 40/40 | 262 | PASS |
| Y144 · ett ändrat PF-register | 60 / 85 | 14/14 | 18/18 · 10/10 · 1/1 | 48/48 | 262 | PASS |
| Y144 · nyckel vänster om spelaren | 104 / 85 | 14/14 | 18/18 · 10/10 · 1/1 | 48/48 | 262 | PASS |
| Y120 · två ändrade PF-register | 24 / 85 | 14/14 | 18/18 · 10/10 · 1/1 | 120/120 | 262 | PASS |
| Y120 · sen andra RESP1 | 24 / 88 | 14/14 | 18/18 · 10/10 · 1/1 | 120/120 | 262 | PASS |
| Samma Y120 med spelvägens `INY` | 24 / 88 | 8/14 | 15/18 · 6/10 · 0/1 | 120/120 | 263 | FAIL |

Noll extra pixlar i PASS-radernas övervakade färgorakel. Sista fallet gav 16 extra gula och sju extra vita pixlar. De tidiga M0-proven ligger vid X24/X32, de sena vid X120. Den sista fungerande väggövergången tar hela 76-cykelbudgeten inklusive WSYNC-skrivningen. Loggen vid SL69 visar andra RESP1 CL58→67, GRP1 CL67→76, PF1 CL127→136 och PF2 CL142→151. Därpå följer WSYNC. Att flytta in radens tvåcykliga Y-uppdatering i samma väg överskrider budgeten och ger faktiskt fel i emulatorn. Det avgränsar den provade registerplanen och dess bokföring.

`NOT_RUN` för komplett P1/PF-integration med levande KeyX/KeyY, fem dynamiska NPC, närliggande X med full spriteorkestrering och fulla TOP/BOTTOM-rundor med den nya renderaren. Diagnostik-ROM:arnas rasterband väljs vid bygge. Originalmaskerna används, men pixeloraklet i detta band täcker fem verkliga rader av P0 och SM, inte hela spelrummet. Rekommenderat nästa tekniska angreppssätt är ett i VBLANK förberett rasterpaket med utrullade rader och all Y-bokföring utanför de fem aktiva raderna. Det behöver plats- och livstidsprövas mot hela spelkön.

### B · separat spelbar timerreparation · PASS i körda prov

| TOP-replay av arkiverad joysticksekvens | Kontroll | 8/4 |
|---|---:|---:|
| Fryst referens vid replaybild 387 | 289 rader | 289 rader |
| BMI/BNE utan förankrad synkstart | 263 rader | 263 rader |
| BMI/BNE och WSYNC före VSYNC-laddning | 515/515 × 262 | 515/515 × 262 |

Basen väntade på exakt noll. När INTIM räknat under noll används en snabb nedräkning och noll kan missas. Den nya pollningen accepterar en tidig underströmning via bit 7. Första WSYNC i nästa bild sker före VBLANK-/VSYNC-laddningen, vilket gav tillbaka den felande raden i reproduktionsprovet. Ett oanvänt scratchfält i kontrollbygget ersattes med tidsutfyllnad för att hålla befintlig banklayout. Fixen hanterar den observerade underströmningen. Extremt försenad återkomst efter underströmningsfönstret är oprövad.

- Alla sex ROM:ar är 16 384 byte F6/NTSC. För varje byggdes TOP/BOTTOM med blinkparametern 0, 8 och 6. Kontrollens kontinuerliga guldnyckel är en referens. Båda gula blinkrytmerna finns som jämförelser.
- Samtliga sex hade 600/600 bildrutor på 262 scanlines med RGB-identitet mot den frysta normalserien, som hade 595/600 kompletta femmaskersbilder och inget helt NPC-bortfall.
- Alla sex gav 10/10 riktade skottpixlar, 16/16/16 saknade inre PF-pixlar, exakt låst brun dörr och 256/256 svart öppning. Det första TOP 8/4-skottprovet använde fast bildbeskärning och rapporterade 0/10. Omprovet loggade emulatorns faktiska TV-apertur och gav 10/10. Båda råloggarna finns kvar.
- Alla sex fullbordade joystickstyrd kallstartsrunda till verklig passage med 210 poäng och tre liv utan RAM-skrivningar. Historisk kontroll gav 65/65 synliga nyckelbilder per kant. 8/4 gav 48/48 PÅ och 21/21 AV per kant med upptagning vid fas 8. 6/6 gav 36/36 PÅ och 31/31 AV per kant med upptagning vid fas 6.
- Kritisk befintlig rasterövergång slutade vid 76 cykler i de loggade proverna. Stackprovet nådde SP=$F7, åtta byte, inom befintlig 128-byte RIOT-budget. Nytt heltäckande bevis för samtliga exekveringsvägar är NOT_RUN.
- Gopher2600 gav de pixel- och timingjämförelser som redovisas här. Stock Stella gav rökprov och originalbilder. Fulla paritytester mellan emulatorerna och fysisk Atari är NOT_RUN.

Timerreparationen behåller spelkärnans kända R2-problem där nyckeln kan saknas när spelaren använder samma rasterband. Fem levande NPC på samma Y kvarstår som separat R1-problem. Ingen blinkrytm är slutligt vald.
