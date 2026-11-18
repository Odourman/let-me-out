# LET ME OUT! – MAIN VIII: ROM DEVELOPMENT III → IV MIGRATION RECEIPT

**Datum:** 2026-11-18. **Beslut:** `ROM_DEVELOPMENT_IV_MIGRATION_SOURCE_REVIEW_ACCEPTED`. **Scope:** dokumentationsmigration och ROM DEVELOPMENT IV:s mottagningsrapport; **INTE** ny ROM-, DASM-, Stella-, Gopher2600- eller Actions-auktorisation. **`G5_FORMAL_OPEN`.**

## 1. Kontrollerade original och korrekt sammanställning

**GitHub:** huvudbranch `main` kontrollerad på `6927e7e280a3d920fb4c7d8beb815e04c3ed8c97` före detta källkvittos nya commit. Specialistens isolerade migrationsbranch `handoff/rom-development-iii-to-iv-20261118` fryst `dd8886e790ee7cfd291e866fdd64a56282ea0791`. [Jämförelse](https://github.com/Odourman/let-me-out/compare/6927e7e280a3d920fb4c7d8beb815e04c3ed8c97...dd8886e790ee7cfd291e866fdd64a56282ea0791): **1 commit ahead, 0 behind, fyra filer samtliga ADDED; inga historiska originaländringar och ingen PR-merge**.

**Migrationsoriginal på den frysta commiten:**
- [Komplett III→IV teknisk handoff](https://github.com/Odourman/let-me-out/blob/dd8886e790ee7cfd291e866fdd64a56282ea0791/docs/ROM_DEVELOPMENT_III_TO_IV_MIGRATION_HANDOFF_2026-11-18.md): Git-blob `02402a8017a55f2589a7b9c2cb9271e730b68246`, SHA-256 `4398aca3cfd86fe85d09e8cb753bb8157aca1be4503543dc981d8ad0f92ca476`.
- [IV startprompt](https://github.com/Odourman/let-me-out/blob/dd8886e790ee7cfd291e866fdd64a56282ea0791/docs/ROM_DEVELOPMENT_IV_NEW_CHAT_STARTPROMPT_2026-11-18.md): Git-blob `f3e5ebe24215a46f42378068c04731bc3e72ec1d`, SHA-256 `5119c59afdeacf5a0605dbf2043554d186f3db5b96a0374bd27fbe5c837088b0`.
- [IV Codex-readiness](https://github.com/Odourman/let-me-out/blob/dd8886e790ee7cfd291e866fdd64a56282ea0791/docs/ROM_DEVELOPMENT_IV_CODEX_READINESS_2026-11-18.md): Git-blob `bf308b8baba6d2615b55e722ac48dddf9b44`, SHA-256 `54fe11c8015e16d08c9b53ab98bf7643db52fd7ebecac5228989b6b982f9fd93`.
- [Icke-självrefererande originalmanifest](https://github.com/Odourman/let-me-out/blob/dd8886e790ee7cfd291e866fdd64a56282ea0791/docs/ROM_DEVELOPMENT_III_TO_IV_MIGRATION_MANIFEST_2026-11-18.txt).

**Officiell Google Drive:** [Original migrations-ZIP](https://drive.google.com/file/d/109CBUN7kO6v7sAmWsPm4Ue-fyu78RZM5/view) i [projektmappen](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) identifierades och **hämtades rått genom ansluten Drive**. MAIN VIII kontrollerade själv: **24 988 bytes**, ZIP SHA-256 **`b54077768f49c0f1d1e3177b824f6dcf620bad1cfc1eb7a481023e0e286cfc46`**, ZIP `testzip() is None`, **fyra medlemmar** varav tre Markdown och ett manifest. **Alla tre Markdown-SHA-256 matchar manifestet exakt**. MAIN beräknade dessutom själv respektive **Git blob SHA-1 från ZIP-filernas verkliga bytes**: samtliga tre stämmer exakt med filerna via GitHub `fetch_file`. Drive har även de fyra filerna separat: [teknisk handoff](https://drive.google.com/file/d/1NLmk9BzjFSILbRAqpPzpW9NH6dwol37A/view), [startprompt](https://drive.google.com/file/d/1tlLJoyQrjku2exkBx4KJ1S50huzJbvIy/view), [Codex-readiness](https://drive.google.com/file/d/1RnWYFCZy8UcSkH5Zwgf9yTK7h4sFziZH/view), [manifest](https://drive.google.com/file/d/1_MjwFUFUFfDGKAo4_-ZGwNpLkXA4SzI4/view). Ingen historisk ROM-arkivering kopierades in i migrations-ZIP.

**ROM DEVELOPMENT IV:s mottagningsrapport** till MAIN VIII (2026-11-18) granskat mot dokumentens källstatus. MAIN bekräftade via GitHub att [PR #7](https://github.com/Odourman/let-me-out/pull/7) är OPEN/DRAFT/UNMERGED, [#5](https://github.com/Odourman/let-me-out/issues/5) OPEN framtida S05, [#8](https://github.com/Odourman/let-me-out/issues/8) OPEN/DEFERRED oberoende Verification, [#18](https://github.com/Odourman/let-me-out/issues/18) CLOSED vid `OFFLINE_ONLY_PASS`. [Ursprunglig Master Spec/57-beslut-ZIP](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) går att nå i Drive: `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip` 738 586 bytes; MAIN har **inte i denna mottagning** omhashat den ursprungliga 738586-bytefilen, utan granskat dess rapporterade identitet mot migrationsfilen.

## 2. Roll- och teknisk status som verkligen mottagits

`ROM_DEVELOPMENT_IV_MIGRATION_RECEIVED` / tillgänglig i Codex Cloud, men **inte ROM runtime-ready**. IV rapporterade arbetskatalog `/workspace/let-me-out`, Debian 13.6, Git 2.52.0, gh 2.46.0, Codex CLI 0.167.0-alpha.4, Python 3.12.14, Pillow 13.0.0 och ImageMagick 7.1.1-43. **DASM, Stella 6.7.1, Gopher2600, Xvfb, xdotool saknas på PATH enligt IV:s lokala rapport**; MAIN har inte själv köråtkomst till just den Codex-containern och påstår därför inte oberoende verifikation av dess versionsutskrifter.

- G5AQ är [källmottaget `G5AP_OFF01_SOURCE_REVIEW_ACCEPTED_OFFLINE_ONLY_PASS`](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AQ_MAIN_VIII_G5AP_OFF01_OFFLINE_ONLY_PASS_SOURCE_RECEIPT_2026-11-18.md): exakt 98/98 **syntetiska** regressioner; **ingen** faktisk kommandokvittens, STA/TIA-färgklockor eller Stella-runtime-lösning.
- G5AL/LM-D25 och G5AJ/LM-D24 `F9_TRAP_CONTROL_FAIL` 2/2 vardera (förbrukat, återanvänd aldrig). G5AH ursprungliga readback/hash FAIL, ingen C0 byggdes. G5AF enbart bounded F9 PASS; G5AD no-build och G5Z/H4-ONE G0 INCONCLUSIVE. Historiska R1/6mask- och R1ba negativa resultat bevarade. Verklig framtida femfienders-/S05-/kartmotor **inte** implementerad/verifierad.
- Formella senaste framtida beslut: fem individuella fiender med fri X/Y, fem startpositioner och 1/5 nyckelbärare, kartor A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01, inte historiska sexmask- och C02-diagnostik som ny spelcanon. Detta är mål, inte ROM-bevis.
- [G5 bindande gräns](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md) kvarstår: `G5_FORMAL_OPEN`. **Ingen** ny Gopher2600 HEADLESS F9-pilot, Stella C++-adapter, ROM/DASM/Stella/Actions-mätning, G6/C0/S05/fem NPC, ny gameplay, PR-merge, oberoende VERIFICATION II är auktoriserad genom migrationen.

## 3. Nästa beslutspunkt, INTE beställning

**Tekniskt rekommenderad ordningsföljd** för ett eventuellt senare uttryckligt användarbeslut:
1. Separat snäv **miljöförberedelse** i Codex: skapa/versionspinna DASM/Stella (och vid behov Gopher2600/Xvfb), verifiera endast installation och körbarhet/versionssträngar, aldrig ROM-bygge eller emulator-F9-mätning av misstag. Notera att installation kan kräva internet/nedladdning; förhandsbegränsa detta i separat order och kontrollera installerade bytes/ursprung.
2. **Först därefter** en separat specifik **Gopher2600 HEADLESS F9-only-mätpilot**, om användaren godkänner ett nytt run-tak och ett mätningskontrakt med synkrona kommandosvar, nytt debugger-entry, bank/PC/frame/scan/cycle och proof class `GOPHER_OBSERVED`. Detta är **en annan emulator** och ger aldrig retroaktivt `STELLA_OBSERVED`.
3. En senare Stella-transportlösning, C0-kalibrering och G5-formal kan endast starta på nya separata beslut. VERIFICATION II förblir oberoende.

**Migrationsbeslutet medför inga nya arbetsorder.** ROM DEVELOPMENT IV är nu mottagen och inväntar MAIN VIII:s uttryckliga framtida order.

**Källkontrollstatus:** GitHub + Drive docs + ZIP byteidentitet: verifierad av MAIN; Codex-terminalversionsutskrifter: IV:s egen rapport (inte MAIN-observerade); ROM-emulatorbevis: inget nytt.
