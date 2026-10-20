# Bundled release validation

Version: SMDesigner 1.1.0 / R2R 1.0.6

- 18 Python regression tests passed.
- Bundled R2R rebuilt using scripts/build_r2r.py and the pinned source archive.
- Native ARM64 executable links only to /usr/lib/libSystem.B.dylib and /usr/lib/libc++.1.dylib.
- Platform wheel and source distribution built successfully.
- Wheel installed into an isolated virtual environment outside the source tree.
- Installed-package smoke test emptied PATH and cleared SMDESIGNER_R2R.
- Actual R2R consensus + mutation + PDF workflow passed: 2 FASTA files, 351 records, 117 PDF files. PDF headers were verified; visual layout was not manually reviewed.
- Original project files and system R2R were not modified.

Pending external validation: Intel macOS, Ubuntu 22.04, Windows WSL, and the claimed minimum macOS version. CI definitions are provided but were not submitted or run remotely. This is a locally tested Apple Silicon release candidate, not a verified release for every target.
