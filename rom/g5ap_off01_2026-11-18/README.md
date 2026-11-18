# G5AP / OFF-01 – ONLY offline synthetic parser regression

A development self-test of a NEW audit parser copied conceptually from the
frozen G5AL auditor. Nothing here starts Stella, Gopher2600, GitHub Actions,
DASM, a ROM, or an emulator. **No PASS here applies to physical Atari/TIA.**

## Execute

Run from this directory with Python 3 and Pillow (`PIL`):

```sh
python3 run_g5ap_offline_fixtures.py > RAW_TEST_STDOUT.txt 2> RAW_TEST_STDERR.txt
```

The test runner creates deterministic temporary fixture trees under the OS
temporary directory. The fixture generator writes its sessions using the same
`session_path()` as `audit_g5ap_offline.py`, and the CLI `--gate`/`--fullaudit`
read those exact paths. The runner writes `G5AP_OFFLINE_TEST_RESULTS.json` and
runs a few actual separate-process CLI assertions in addition to in-process
assertions; all 98 assertions must pass. Run twice and compare SHA-256 of JSON,
stdout and stderr. No network access is used.

`G5AP_SYNTHETIC_FIXTURE_EXAMPLES.zip` contains complete representative specimen
trees with real PNG format but **invented RGB image pixels and invented numeric
Stella-like text**. They do not contain a ROM or actual emulator measurements.

## Capture contract and limitations

- Exact file: `A_TRAP/<STAGE>_debugger_session.txt` or
  `B_BREAK_STEP/<STAGE>_debugger_session.txt`. Generic `*_session.txt` rejected.
- Each stage requires `G5AP_CAPTURE_INDEX.json` with canonical relative path,
  source kind `OFFLINE_SYNTHETIC`, source SHA-256, sequence and entry-ID, plus
  exactly matching `G5AP_SYNTHETIC_CAPTURE` embedded marker.
- Different debugger entries must not be recycled after `run`; B/C cannot
  qualify without their approved prior stage. Native images need valid 320x228
  RGB data and matching hashes. Actual G5AF RGB pixels are NOT bundled as a
  simulated historical reference: the reference in examples is deliberately fake.
- In a future *separately authorized* real emulator protocol, a trusted capture
  writer would need to generate/attest the entry ID, command sequencing,
  timestamp and file digest. A string inside a Stella `saveSes` cannot prove
  its own freshness. **Do not apply this offline-only parser to historical
  G5AL raw files and call them method PASS.**

`OFFLINE_ONLY_PASS` means synthetic assertions behave as specified, not
`STELLA_OBSERVED`, G5 formal PASS, Verification II or project authorization.

## Provenance

Actual frozen G5AL source at commit `f16e1e4ac3736e3d6bb1bc0b959b0213e28f6431`,
Git blob `f159c1f8668c1f504fd9538a8d1ef17b2ddefafa`, 8426 B. Exact original
text was copied **without changes** into the new isolated GitHub branch as
`audit_g5al_frozen_original_reference.py`. The new parser is exclusively
`audit_g5ap_offline.py`. G5AO reference ZIP from MAIN VIII was **not attached
or accessible in this specialist chat**, so its claimed ZIP SHA-256
`c519555a974199a2c19e07583c179a2af32819af69d2b42ccdb00c4ba1aad633`
was NOT rehashed by ROM DEVELOPMENT III; the documented G5AO report is the
source for the earlier 18 assertions.

No files under the G5AL/G5AO historical GitHub paths were edited. No PR merge.
