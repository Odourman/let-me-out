# LET ME OUT! – MAIN VIII G5AS: G5AR ENV-01 installerad i aktuell Codex-task, ej beständig

**Datum:** 2026-11-18. **Mottagningsklass:** `G5AR_ENV01_SOURCE_REVIEW_RECEIVED_ENV_NOT_PERSISTED`. **Gällande uppdrag:** [Issue #19 – G5AR ENV-01](https://github.com/Odourman/let-me-out/issues/19), [specialistens faktiska TO_MAIN/skript/råbevis](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310). **Issue #19 förblir OPEN** eftersom beständig Cloud Environment-publicering och kontroll i ny Codex-task saknas. **`G5_FORMAL_OPEN`**.

## 1. Vad MAIN VIII har kontrollerat

MAIN VIII har via den aktiva GitHub-kopplingen läst **hela specialistens faktiska Issue-kommentar `6976852310`**, inklusive exakt tabell, käll- och SHA-256-pinnar, tre kompletta skript, install-/terminalutdrag och den uttryckliga stopplistan. Detta är en **dokumenterad specialistleverans med källkontrollerad rapport**, inte MAIN:s egen terminalkörning i samma Cloud-instans. MAIN har inte oberoende hashat de nerladdade sju ursprungsbinärerna eller själv exekverat skripten i Codex Cloud; inga sådana tekniska påståenden får härledas från ett publicerat råloggutdrag ensamt.

Rapporterad och internt dokumenterad installation i aktiv task `/workspace/.g5ar-env01`, Debian 13.6 x86_64, utan sudo och utan systemets dpkg-förändring:
- **DASM:** motorn `2.20.14.1`, Debian-paket `2.20.15~20201109+really2.20.14.1-2`, faktisk usage/versionsrad men exit 1 på argumentlöst anrop (inte kompileringsbevis).
- **Stock Stella:** officiell upstream distribution `6.7.1`, package metadata kontrollerad utan att starta emulatorn; debugger-dokumentation finns. **Ingen emulator- eller debuggerfunktion har provkörts.**
- **Xvfb:** Debian Security `2:21.1.16-1.3+deb13u4`, metadata och resolved ELF-beroenden, ej X-serverstart.
- **xdotool:** `3.20160805.1` (Debian `1:3.20160805.1-5.1`), faktisk versionsutskrift; ingen X11-kommandosändning.
- **Gopher2600:** officiell `v0.57.2` för Linux amd64, `VERSION -v` rapporterar `2af86eb725739adbf3d9d45cea2ed69eea57da2a`; **skiljer sig** från tidigare G5AP:s source-review pin `74c544203378c1448a33c29bc8b4586079b050f4`, dvs versionsskifte måste redovisas vid framtida separat tekniskt test.
- **Befintliga:** Python `3.12.14`, Pillow `13.0.0`, ImageMagick `7.1.1-43`.

Specialist rapporterar att samtliga sju nerladdade filer SHA-256-kontrollerades före extraktion, Debian APT-index-/InRelease-kedja verifierades och beroenden kontrollerades med `ldd`. Officiell Stella releasefil saknade publicerad upstream digest och pinades mot nedladdad fil-SHA; Gopher2600:s SHA matchade publicerad officiell digest. Två **separata tomma prefixes i samma task** gav byteidentiska binärer/wrappers. **Detta är inte bevis på bevarad installation i senare task.**

GitHub original vid mottagningen: [STATUS](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) och [G5 boundary](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md) kontrollerades; live `main` före nytt receipt var `8352f860327daec010ae0f56db9f080187d062c2`.

## 2. Vad som uttryckligen INTE är utfört

**`ENV_NOT_PERSISTED` / `PERSISTENCE_NOT_VERIFIED`:** specialistens Cloud API hade bara läsåtkomst för miljökonfiguration, ingen edit/publish. Ingen uppdaterad Cloud-draft sparad. Nuvarande konfigurering i tasken försvinner potentiellt mellan fristående tasks. Att `let-me-out` var publicerad tidigare bevisar **inte** att de fem verktygen ligger i den publicerade versionen.

Rapportens tre bilagor:
- `install_g5ar_env01.sh` SHA-256 `4ebb08277acbc0a82c383cce31e8eb16dc615ed4cd3e9dd1fde74a15f9100d16`.
- `start_g5ar_env01.sh` SHA-256 `e2103acd57980f70c9ed566a9ab7a71f3b2909b9eba04b174d56919f116f6d8a`.
- `evidence-check.sh` SHA-256 `1b0ac63b05b178f9000fdea3085cacde85d0e0fe947580db1e9c6d87ed2930d7`.

**OBS:** `start_g5ar_env01.sh` exporterar endast `PATH` när det **sourcas i samma process**; att bara exekvera en separat startprocess ändrar inte framtida tasks PATH. Installatören är medvetet fail-closed om prefixet redan finns, så setup måste villkoras på ett sätt som är förenligt med användarens sparade miljö. Ingen automatisk omskrivning eller körning av dessa skript av MAIN har skett.

**0** ROM-byggen, DASM-assemblering, emulator-/debuggermätning, Actions, sourcepatch, merge, Verification II rapporterade under G5AR. `ROM_BUILD_VERIFIED=NOT_RUN`, `EMULATOR_RUNTIME_VERIFIED=NOT_RUN`; inga äldre misslyckanden eller G5-gates omklassificeras.

## 3. Kvarvarande uppgift enligt redan auktoriserat scope

Miljöägaren behöver i Codex **Settings → Codex Cloud → Environments → `let-me-out` → … → Edit** öppna publicerad miljö, ge setup-uppgiften till Codex eller manuellt föra in granskade `install_script` och `start_skill`/samma-process PATH-konfiguration enligt [Issue #19:s faktiska bilagor](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310), kontrollera installatörens villkor, **Save** och **Republish**. Officiell UI-väg och hur ändringar gäller nya tasks dokumenteras av [OpenAI Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments).

Sedan: skapa **en ny Codex Cloud-task med uttryckligen den uppdaterade `let-me-out`-miljön**; gör endast fresh `PATH`, `command -v`, paket-/versionssträngar och SHA-256-kontroll **utan ROM eller emulatorstart**, inklusive faktisk miljökonfigurationsrevision och rapport om skripten tillämpats. Publicering + positiv fresh-task-versionkontroll är villkor för `G5AR_ENV01_ENV_INSTALL_ONLY_PASS`. Om nytt prefix saknas eller versioner skiljer sig: `ENV_NOT_PERSISTED`/FAIL, dokumentera och stoppa.

**Detta är återstående del av redan godkända Issue #19:s miljöscope, ingen ny ROM-/emulatorauktorisation.** En Gopher HEADLESS F9/RESP1-pilot och verkliga Stella-mätningar kräver separat nytt uttryckligt användarbeslut med eget kör-/stoppkontrakt; de är inte nästa automatiska moment.

## 4. MAIN VIII:s beslut

**Källmottagen delinstallation, inget slutligt PASS.** Issue #19 lämnas **öppen** och markeras för ägarens Cloud-miljöpublicering och senare fresh-task-kontroll. Project Sources behöver inte bytas. **`G5_FORMAL_OPEN`**.
