# LET ME OUT! – MAIN VIII G5AQ: källgranskat slutmottagande av G5AP OFF-01

**Datum:** 2026-11-18. **MAIN-beslut:** `G5AP_OFF01_SOURCE_REVIEW_ACCEPTED_OFFLINE_ONLY_PASS`. **Bevisklass:** `OFFLINE_SYNTHETIC`, inte `STELLA_OBSERVED`, `GOPHER_OBSERVED`, ROM-bevis eller oberoende VERIFICATION II. **G5-grind:** `G5_FORMAL_OPEN`.

## 1. Auktoritet och original

- [Bindande G5AP/OFF-01 Issue #18](https://github.com/Odourman/let-me-out/issues/18), [MAIN VIII:s originalöverlämning](https://github.com/Odourman/let-me-out/issues/18#issuecomment-6965174994) och [ROM DEVELOPMENT III:s frysta handoff](https://github.com/Odourman/let-me-out/issues/18#issuecomment-6965331211).
- Fryst ROM DEVELOPMENT III-specialistbranch `rom-dev-iii/g5ap-off01-offline-parser-regression-20261118`, [slutcommit `cfef90529f53bf449a90d7e267a0ad2e7d8b2328`](https://github.com/Odourman/let-me-out/commit/cfef90529f53bf449a90d7e267a0ad2e7d8b2328), [TO_MAIN](https://github.com/Odourman/let-me-out/blob/cfef90529f53bf449a90d7e267a0ad2e7d8b2328/rom/g5ap_off01_2026-11-18/TO_MAIN_G5AP.md), [reparerad parser](https://github.com/Odourman/let-me-out/blob/cfef90529f53bf449a90d7e267a0ad2e7d8b2328/rom/g5ap_off01_2026-11-18/audit_g5ap_offline.py), [fixtures-runner](https://github.com/Odourman/let-me-out/blob/cfef90529f53bf449a90d7e267a0ad2e7d8b2328/rom/g5ap_off01_2026-11-18/run_g5ap_offline_fixtures.py), [JSON-resultat](https://github.com/Odourman/let-me-out/blob/cfef90529f53bf449a90d7e267a0ad2e7d8b2328/rom/g5ap_off01_2026-11-18/G5AP_OFFLINE_TEST_RESULTS.json), [manifest](https://github.com/Odourman/let-me-out/blob/cfef90529f53bf449a90d7e267a0ad2e7d8b2328/rom/g5ap_off01_2026-11-18/MANIFEST_SHA256SUMS.txt).
- **GitHub compare faktiskt kontrollerad**: basmain `103de29025fed4ec603b437f927ab874b0b9965e`, huvud `cfef90529f53bf449a90d7e267a0ad2e7d8b2328`, **2 commits ahead, 0 behind, 14 filer samtliga ADDED**, 0 historiska ändrade/raderade filer och **ingen merge**. Huvudbranch `main` stod kvar på bas-sha vid mottagningen.
- Den särskilt kopierade [frysta G5AL originalparsern](https://github.com/Odourman/let-me-out/blob/cfef90529f53bf449a90d7e267a0ad2e7d8b2328/rom/g5ap_off01_2026-11-18/audit_g5al_frozen_original_reference.py) har **exakt samma Git blob SHA1 `f159c1f8668c1f504fd9538a8d1ef17b2ddefafa`, 8426 bytes** som [historiska originalet i fryst G5AL commit `f16e1e4`](https://github.com/Odourman/let-me-out/blob/f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431/rom/g5al_f9_method_2026-11-18/audit_g5al.py), kontrollerat av MAIN via GitHub-connectors. Frysta originalet är inte en av de tolv ZIP-medlemmarna, men finns separat som ny tillagd fil på specialistbranch.

## 2. Verkligt originalarkiv från Drive – MAIN VIII egen bytekontroll

**Original:** [officiell Drive-arkiv ZIP](https://drive.google.com/file/d/1aUCJXERZqFwJ2T0se81Ns-HmY1MkBoKW/view). MAIN VIII använde live Google Drive connector för att själv hämta **rå bytes** och lokalt räkna om:
- Projektmapp ID `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u` verifierades genom Drive-metadata. MIME `application/zip`, **42 508 byte**.
- SHA-256 för verkligt nedladdade ZIP-bytes: **`b6d722eae0b358d32172d54131f1fec3eab7facecc20bee6ef6f3bf2deb42894`**, exakt samma som specialistens manifest. ZIP öppnat med Python `zipfile`, **12 medlemmar**, `testzip() is None`, inga trasiga medlemmar.
- Manifestet är **inte självhashande**, innehåller **11 rader** för de 11 andra medlemmarna; MAIN VIII beräknade **själv SHA-256 av ZIP-bytes för varje medlem**: **11/11 exakt rätt**, ingen medlem saknas eller är olistad. Arkivets tolvte medlem är `MANIFEST_SHA256SUMS.txt`.
- JSON `G5AP_OFFLINE_TEST_RESULTS.json`: faktiskt parsad och räknad med Python: **98 rader, 98 `assertion_pass=true`, 0 fail**, `classification=OFFLINE_SYNTHETIC`, `exception=null`, `historical_G5AL=G5AL_F9_TRAP_CONTROL_FAIL_UNCHANGED`, `g5=G5_FORMAL_OPEN`.
- Båda frysta `RAW_TEST_STDOUT*` var **byteidentiska** med SHA-256 `41074505221bbf7269e7f5aff165d1a36cfc0d94091613f80cbd7de8c15d40a4`. Båda frysta `RAW_TEST_STDERR*` var **0 byte**.

## 3. MAIN VIII:s EGEN reproducerbara offline-återkörning

MAIN VIII extraherade de tolv ZIP-medlemmarna i en separat lokal granskarkatalog och läste koden för att avgränsa exekvering till **syntetiska filer och Python-subprocesser för parsern**. Därefter kördes:
```bash
cd /mnt/data/g5ap_main_source_review
python3 run_g5ap_offline_fixtures.py \
  >/mnt/data/g5ap_main_source_review_replay_stdout.txt \
  2>/mnt/data/g5ap_main_source_review_replay_stderr.txt
```
**Observerad verklig exitkod 0, 98/98 offline-assertions PASS, 0 fail**, sista rad `G5AP_FINAL {"failed_assertions": 0, "g5ao_zip_original_available": false, "passed_assertions": 98, "result": "OFFLINE_ONLY_PASS", "total_assertions": 98}`. **MAIN:s lokala stdout exakt byteidentisk med frysta `RAW_TEST_STDOUT.txt`** (SHA-256 `41074505221bbf7269e7f5aff165d1a36cfc0d94091613f80cbd7de8c15d40a4`); lokal stderr **0 byte**. Den vid återkörningen nyskrivna JSON-filen har samma SHA-256 `477a86a280a054340b1fa339c2cafae63f9cc85a197179b466664b9fbebe90d0` som fryst original.

Detta är en **extra käll- och reproduktionskontroll av MAIN**, inte utförd av specialisten VERIFICATION II, och är **inte ett nytt emulator- eller ROM-test**. Att samma testkod producerar samma utfall ger reproducerbarhet men inte bevis för att alla tänkbara parserfall är täckta.

## 4. Vad som faktiskt godtas – och inte

**MOTTAGET:** En **ny, offline-testad reparerad kopia** av G5AL:s audit-parser som på de **testade syntetiska** exemplen har:
1. En kanonisk `<STAGE>_debugger_session.txt`-path för fixture writer, `--gate` och `--fullaudit`, utan det gamla finalaudit-suffixfelet.
2. Specifika krav `A_REENTRY_HANDSHAKE PC=$F1F0`, `B_REENTRY_HANDSHAKE PC=$F1EE` utan skuggande generisk `endswith("HANDSHAKE")`.
3. Syntetisk registeroutput som kopplas till rätt `print`, avvisning av joinade/duplicerade/missade kommandon och felaktiga bank/frame/scan/cykler, krav på explicit syntetiskt index för filhash/entry/source/seq och kompletterande PNG-närvaro/hash/dimensioner.
4. Hård fail-closed på testade stale/inkonsekventa prover, inklusive archive-PASS plus metod-FAIL; A-only/B&C-not-run **`OFFLINE_SYNTHETIC_PARTIAL_NOT_DETERMINABLE`**, full artificiell ABC **`OFFLINE_SYNTHETIC_A_B_C_CONTRACT_PASS`**, aldrig `STELLA_OBSERVED`.

**INTE MOTTAGET SOM VERIFIERAD RUNTIME:** G5AO-original `LET_ME_OUT_G5AO_OFFLINE_FIXTURES_2026-11-18.zip` saknades i ROM DEVELOPMENT III-specialistchatten och dess checksumma verifierades därför **inte** av specialisten; återbyggd GitHub-18-fixturebaslinje är tillåten och korrekt redovisad. Den reparerade parsern kräver syntetiska proveniensmarkörer och `G5AP_CAPTURE_INDEX.json` vilka **inte existerar som autentiska Stella-6.7.1-`saveSes`-uppgifter**. Det är **inte** en drop-in parser för oförändrad Stella, ingen bevisad emulator-kommandokanal, inget CPU/TIA-bevis och ingen verifiering av F9- eller C0-ROM. En senare verklig adapter måste dokumentera och tillhandahålla tillförlitlig motsvarande proveniens; inga syntetiska kvitton får tas som emulatorbevis.

**G5AP OFF-01 är SLUTFÖRT inom exakt offline scope, utan några nya Stella/Gopher2600/Actions-körningar, ASM/BIN/DASM/ROM-byggen, emulatorpatch, senare steg, spelcanon, PR-merge eller oberoende Verification II.** Issue #18 **stängs av MAIN som "completed / OFFLINE_ONLY_PASS"**, inte som godkänd G5-emulator- eller grafikgrind. G5AL/LM-D25 `G5AL_F9_TRAP_CONTROL_FAIL` 2/2 förbrukade, G5AJ/LM-D24 `G5AJ_F9_TRAP_CONTROL_FAIL` 2/2 förbrukade, G5AH original hash-FAIL, G5AF bounded instrument-PASS oförändrade; **`G5_FORMAL_OPEN`**.

## 5. MAIN:s nästa rimliga vägval – inga nya uppdrag här

Mot bakgrund av [G5AP:s webbresearch](https://github.com/Odourman/let-me-out/blob/main/docs/research/G5AP_MAIN_VIII_WEB_VERIFIED_DEBUGGER_ALTERNATIVES_AND_NEXT_OFFLINE_GATE_2026-11-18.md) är nästa möjliga *separat auktoriserade* tekniska fas en **liten, fryst, versionspinnad Gopher2600 HEADLESS-undersökning** av endast original F9/RESP1 med definierad kommandokvittens via stdin/stdout, F6-bankar och jämförelsekontroller. Gopher2600 är **en annan emulator**: sådana framtida resultat kan bara klassas `GOPHER_OBSERVED`, aldrig retroaktivt ge `STELLA_OBSERVED` eller `G5_FORMAL_PASS`. Stellas kommandotransport måste fortfarande lösas separat om G5 kräver det. **Ingen sådan Gopher-run auktoriseras eller påstås här.**

Project Sources fortsatt **navigationsstöd**; ingen ny release eller manuell utbytesfil begärs.
