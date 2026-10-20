# 1.1.0 — bundled R2R

- Bundle a native R2R executable, with explicit override and system fallback.
- Include R2R 1.0.6 original source, checksum, build script and upstream notices.
- Apply documented compiler compatibility fixes for ARM64 and modern C++.
- Build platform-specific Python wheels; refuse a binary wheel without R2R.
- Add platform/selection tests and an installed-package real R2R smoke test.
- Prepare GitHub Actions builds for Apple Silicon, Intel macOS and Ubuntu/WSL.
- No automatic system installation, runtime download, or publication.

# 1.0.1 — review fixes

- Isolate each run's outputs and temporary annotation files; remove deletion of shared sibling folders.
- Fix full stem identifier comparison and guard insufficient mutation pairs.
- Sort tied stem lengths numerically.
- Use checked subprocess argument lists for R2R consensus and PDF calls; validate output and propagate errors.
- Normalize structure brackets before checking pairs; correctly log and skip unpaired inputs.
- Concatenate interleaved alignment blocks and reject mismatched annotations.
- Keep dotted filenames intact in drawing metadata and PDF names.
- Consolidate CLI behavior around main.py, add noninteractive arguments and module execution, and return nonzero on failure.
- Make external installation explicit, user-local, and fail-fast.
- Correct ungapped sequence-length counting, keep sequence IDs intact, and filter intermediate files by extension.
- Add 14 regression tests and refresh installation and usage documentation.

Validation: regression tests pass, including a full Python mutation pipeline with a controlled R2R consensus fixture. The test checks two disruptive changes and four restorative changes, including loss/restoration of the selected base pairs. Shell invocation, error handling, and drawing filenames are tested independently. These tests do not establish biological effectiveness for every RNA structure.

Actual R2R analysis and PDF rendering could not be completed on the reviewed machine because its installed R2R executable is incompatible. No external software was installed or replaced. Unsupported pseudoknots require a separate design change.
