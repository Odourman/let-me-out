# LET ME OUT! – MAIN XI: VÄNTANDE ÖVERLÄMNING TILL ROM DEVELOPMENT IV

**2026-11-20 NY STATUS: FULFILLED_BY_4c4fc5b7 – ÖVERLÄMNINGSKRAVET ÄR REDAN GENOMFÖRT GENOM VERKLIG ROM-LEVERANS.** ROM DEVELOPMENT IV publicerade båda avsedda spelbara test-ROM:ar `TO_MAIN_V02_TOP_BOTTOM_DOOR_TRIAL` i [Issue #31](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7037851276), fryst `4c4fc5b7c5545217b2321a38d9db6db5dac7db2f`, med senare start `8177c` enligt tidigare order. MAIN XI mottog med [formellt begränsat beslut](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7037903760). **DEN HÄR GAMLA KOPIERBARA TOP/BOTTOM-PROMPTEN SKA INTE LÄNGRE SKICKAS TILL ROM DEVELOPMENT.** Hur den separata chatten initierades är inte här styrkt; faktisk provleverans finns och är granskat. Originaltext nedan bevaras som historiskt **PENDING**-läge innan den rapporten inkom. Inga automatiska nya test-, implementations- eller specialistjobb startas av detta statusbyte. **R3 exact FAIL, orange spill FAIL, bottom aperture 254/256, shot 9/10, key/player 0/14, same-Y 2/5, G5_FORMAL_OPEN, INDEPENDENT_VERIFICATION=NOT_RUN.**


**Registrerad:** 2026-11-20, efter användarens uttryckliga besked att först invänta ROM DEVELOPMENT IV:s svar.

**Status: `PENDING_USER_SEND_AFTER_DEV_REPLY`.** Användaren har sagt att den färdiga prompten **ÄNNU INTE** skickats till den separata ROM DEVELOPMENT IV/Codex-chatten. Ingen sådan körning får antas ha startat bara för att en MAIN-arbetsorder finns i GitHub. Detta är en påminnelse/överlämningskö, **inte** en ny kodorder eller tillåtelse att starta specialist nu.

## Vad som ska överlämnas när användaren återkommer med utvecklarens svar

Det senaste färdiga, kopierbara MAIN XI-uppdraget heter:

**`LET ME OUT! – ROM DEVELOPMENT IV: TOP/BOTTOM DOOR TRIAL`**, föregående MAIN-chattmeddelandes kompletta 6-punktsprompt (2026-11-20). Den fullständiga tekniska arbetsordern finns redan i [Issue #31, MAIN XI:s kommentar 7036700643](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643).

**Primär teknisk start efter senare mottagning:** exakt fryst `8177c09368721988debb5407d8ffc2ed4bf4d94e`, katalog `rom/playable-slice-v02-object-conflict-repair/`. [MAIN XI:s mottagning som uppdaterade basen från gamla X71](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753). Äldre `a1b4449fe92fb8045f6f88f040c7f94be03e2ffb` är historisk X71-regressionsbas, **inte** start för nästa variant efter mottagningen.

## Kort sammanfattning av den ej skickade prompten

1. Två **verkliga F6/NTSC test-only spel-ROM-varianter** med EN centrerad öppning/dörr: en i ÖVRE och en i NEDRE ytterväggen. Utnyttja speglad playfield om det verkligen hjälper. Inte ännu en fyrarumsproduktionscutover.
2. Dörren orange låst med exakt svart **utskuret** nyckelhål = avsaknad av orange pixlar mot svart bakgrund; inga extra svarta objekt som tar bort spelarens eller fem fienders sprite-resurser. Funktionell upplåsning och fysisk passage, inga extra öppningar.
3. Mät på riktig TIA/Gopher/Stella om topp/botten minskar P0/P1-konflikterna med gul spelare, guldnyckel, vit fem-NPC samt dynamisk brun PF. Fortsätt reparera andra redan godkända V02-grafikblockerare (key+player på samma rasterband, fem same-Y och väggfel); redovisa kvarvarande FAIL utan dolda rasterkompromisser.
4. Gör endast rådgivande analys av framtida oberoende slumpat original-8×9-maskval per fem fiendeindivider, **inte** fyra rum i skarp ROM.
5. F6/NTSC **16 384 B, 262 scanlines, ≤76 CPU-cykler/scanline, 128 RIOT-byte inklusive stack**, fem individuella fiender med fria logiska X/Y, befintliga originalmasker, AI, skott, nyckel, score/liv; DASM/Gopher2600/Stella, joystick från verklig kallstart utan RAM-POKE; bevara frysta original och positiva/negativa bevis. Ändrad dörrgeometri måste få nya exakta pixel-/kollisionsorakel (gamla högerdörrsfixturer är historiska regressioner).
6. Leverera i **samma Issue #31**, rubrik `TO_MAIN_V02_TOP_BOTTOM_DOOR_TRIAL`, med fryst commit, byggbar assembler, 16KiB-binärer, SHA-256, bilder, raster-/CPU-/RAM-/färg-/pixelspår, regressioner och ärliga negativa resultat; `DEVELOPER_OBSERVED`, `G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`.

Ingen ny V03/G6/F12, fyrarums-cutover, PAL/mapperbyte, mask-/canon-/flimmerwaiver, PR-merge, release eller egen verifieringsgodkännande.

## Exakt nästa MAIN-åtgärd

**VÄNTA** på utvecklarens svar; ingen ny specialistchatt eller ROM-körning från denna post. När användaren tillhandahåller svaret:
1. Kontrollera aktuell Issue, senaste frysta commit/ROM/SHA och publicerade positiva/negativa resultat och om svaret redan innefattar topp-/bottendörrtrial.
2. Mottagningsgranska eventuell ny ROM och uppdatera GitHub/Drive-status.
3. Om provet ännu **inte** utförts: påminn användaren om att **den färdiga TOP/BOTTOM DOOR TRIAL-prompten ännu inte skickats**; ge den fullständigt kopierbar med kontrollerad **aktuell** startpunkt och hänvisning till Issue-order. Skicka den inte automatiskt; användaren överlämnar den till separat ROM DEVELOPMENT IV.
4. Om utvecklaren redan utfört samma prov: **duplicera inte** uppdraget; granska resultat och justera kön.

**Förlita dig inte på ChatGPT Memory** för denna väntande överlämning. Den här dokumenterade statusen och levande GitHub/Drive är referens. Designbeslutet som styr framtida form-/dörrmål: [MAIN XI 2026-11-20](../gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md).
