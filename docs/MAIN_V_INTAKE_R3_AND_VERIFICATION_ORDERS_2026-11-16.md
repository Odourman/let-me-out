# Let Me Out! - MAIN V intake, R3 order and independent verification intake
**Date:** 2026-11-16. **Role:** MAIN V project coordination only. **Authority:** status delta and task dispatch within existing v0.18 authorization, not a new user decision, design waiver, ROM acceptance, merge authorization or new implementation phase.

## 1. Verified source access and authority
- GitHub repository: https://github.com/Odourman/let-me-out (connected read/write). Google Drive project folder: https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u (connected read/write).
- Read MAIN IV handoff in both GitHub and Google Docs, MAIN V start and both role prompts; current state, checkpoint, 11-decision supplement, authorization, scope, acceptance, blockers, verification contract, T01-T16 matrix, R3 audit and R1ba technical report.
- Opened original Drive ZIP LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip; the 03_DECISIONS.csv has exactly 57 decisions (001-057); ZIP SHA256 f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4. Historical decision 053 paused all ROM development, but the later explicit user authorization on 2026-11-15 in Issue #6 supersedes that pause ONLY for v0.18 NTSC R1-R4 diagnostic coding.
- Respect direct user decisions and the original 57 decisions as supplemented; present explicit v0.18 authorization and its acceptance conditions govern diagnostic work. Research, newer handoffs and local developer tests do not silently supersede these sources.

## 2. Snapshot observed at MAIN V intake
- main HEAD at first audit: d694a2f2944f155ed8a6eea8e298544f72730046 (handoff/documentation commit, not evidence of a merged ROM). Check HEAD again before using it as a live pointer.
- Draft PR #7: open, draft, NOT merged; branch rom-dev/v018-ntsc-diagnostic at 82667dae033f70570dce903f8e1d4866528be02a. Historical production diagnostic preflight has visual/cycle failures; no final PASS.
- Issue #6: open; only v0.18 NTSC R1-R4 authorized, with F6 16 KiB if technically justified. No full game, PAL, new mapper, gameplay/rule/graphics waiver, map cutover, additional step or PR merge.
- Issue #8: open and NOT independently performed. Frozen historical developer commit 561d3baf00c6c4c4bd9bc46599a91dc693abdeba, developer ROM SHA256 d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620, evidence ZIP SHA256 7500dae4f4a63d27f765bad3b3872384bd2ccb842a7e807abb9e50a475df2dc4. Do not substitute later PR HEAD or R1ba.
- R1ba (research/main-iv-r1ba-integrated-xyz-pf-20261116; Actions run 43884511590, success) locally audited 600/600 genuine Stella frames in one 16384-byte NTSC F6 ROM with all six source-exact original masks, yellow P0, one static M0, three LINKED X/Y layouts, and two mirrored brown PF walls, 262 scanlines; ROM SHA256 41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361. This is LOCAL RESEARCH PASS, NOT six individual free X/Y, complete R1, real T07 write-cycle trace, R2, R3 or R4 acceptance, and NOT independent verification. All four F6 banks repeat one program.
- Overall full v0.18 diagnostic: BLOCKED / NOT ACCEPTED. PR #7 remains draft; no other step authorized.

## 3. First and ONLY immediately issued ROM DEVELOPMENT work order - R3-C02
**Status:** Prepared for the user to start the separate ROM DEVELOPMENT chat. No claim is made that a chat has received or started it.
**Purpose:** Isolated, executable, reproducible R3/NTSC test of only-right-hand door, with separate evidence for orange gate and recognizable black keyhole. Do not implement R1/R2/R4 as part of this order.
**Authority:** Existing Issue #6, A01-A04/B01-B03/D01-D03/E01-E04, T01/T07/T09-T12/T14/T16 and the MAIN IV R3 source audit; no extension of user authorization.
**Source freeze and geometry:** Read design/PLANERADE_RUMSKARTOR_V011.json selected C02 40x22 map as source; x=0 closed in every row, x=39 door marker at rows y=9,10,11,12 and wall elsewhere. DO NOT replace C02 with proposed v0.19 map A_OPEN_01-D_OPEN_01. Inspect PR #7's rom/v018/tools/build.py and rom/v018/src/bank2.asm (asymmetric CTRLPF=0, separate LEFT/RIGHT PF writes, P1 DOORCOLOR phases) as a hypothesis, not proven ROM rendering.
**Execution order:** (a) reproduce current R3 behavior on exactly pinned source, tool versions and frames; (b) check left/right PF before and after deterministic locked/open diagnostic flag with identical viewport and frame numbering; (c) individually demonstrate orange port and truly distinguishable black keyhole; (d) demonstrate both disappear on unlocking while only right boundary opens, no left gap or stale black mark; (e) minimal door-state/right-exit positioning test within diagnostic scope, no full key/AI/gameplay; (f) actual Stella NTSC 262-scanline observations plus critical TIA register-write scanline/cycle measurements and worst 76-cycle budget; if genuine cycle trace is unavailable mark T07 INCONCLUSIVE, never replace by static estimates.
**Allowed fixes:** Only if test failures require them, modify R3 code on a separate, explicitly named research/development branch; leave PR #7 and main unmerged and keep original failed runs. Preserve original graphics and rules. If black keyhole cannot coexist, report D03 FAIL/BLOCKED and tradeoff(s), not silent waiver.
**Required handoff:** pinned source commit+branch and changes, full assembler source, reproducible DASM build script/versions, executable .bin and mapper/size, SHA256 manifest, authentic unedited Stella screenshots with frame ID and locked/open states, frame-by-frame scanline log (600-frame runs per stable state strongly preferred), actual CPU/TIA cycle/register trace or explicit INCONCLUSIVE, applicable T01-T16 delta rows, failure log and local status LOCAL_DEVELOPER_PASS/FAIL/INCONCLUSIVE. Deliver artifacts to MAIN V; do not independently grant final PASS or begin the next assigned R1/R2/R4 task.

## 4. Separate initial VERIFICATION assignment - historical frozen baseline ONLY
**Status:** Prepared for independent VERIFICATION chat, not yet executed.
Read Issue #8 and docs/VERIFICATION_INTAKE_ROM_V018_2026-11-15.md; fetch exactly 561d3baf00c6c4c4bd9bc46599a91dc693abdeba and its corresponding historical evidence ZIP, not branch HEAD or R1ba. Independently clean-build using pinned tool versions, compare byte-for-byte SHA256 with the claimed ROM and ZIP, run/inspect R1-R4 under the required T01-T16 matrix; report actual 600-frame scanline evidence where required, observed TIA cycles, visual quality, O1 constant key coordinate/occlusion/return, right-door/gate/keyhole separately. Mark all 16 cases PASS, FAIL, INCONCLUSIVE or NOT_RUN with evidence paths and no fabricated measurements. No source patch, no PR merge and no borrowed developer PASS. Submit a separate signed VERIFICATION_REPORT.md and explicit overall verdict. Later fixed developer R3 or complete v0.18 deliveries need separate new verification intake, never inherit this baseline's verdict.

## 5. After first intake
- First ROM task: R3 C02; next only after a reviewed R3 handoff: R1 six independently movable X/Y and source masks; then R2 five NPC + gold key/O1; then R4 movement/overlap + timing stress. This is prioritization INSIDE the existing v0.18 authorization, not authorization to start all tasks now.
- User must create two dedicated chats separately and paste the role prompts in docs/MAIN_V_ROM_DEV_AND_VERIFICATION_STARTPROMPTS_2026-11-16.md plus this work order. MAIN V reviews developer artifacts; only independent VERIFICATION may make a verification finding. No claim that either chat exists or was instructed.
- Keep historical sources unmodified. Update project status after actual evidence. Do not modify The Cabin, I Love a Fish or Linear.

## Primary links
- MAIN IV handoff: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_IV_TO_MAIN_V_HANDOFF_2026-11-16.md
- Role prompts: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_ROM_DEV_AND_VERIFICATION_STARTPROMPTS_2026-11-16.md
- Source audit R3: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_IV_R3_RIGHT_DOOR_SOURCE_AUDIT_2026-11-16.md
- R1ba Actions proof: https://github.com/Odourman/let-me-out/actions/runs/43884511590
- PR #7: https://github.com/Odourman/let-me-out/pull/7
- Authorization Issue #6: https://github.com/Odourman/let-me-out/issues/6
- Verification Issue #8: https://github.com/Odourman/let-me-out/issues/8
