# SMDesigner — Structure mutation designer

SMDesigner designs disruptive and restorative mutations from aligned RNA sequences and a consensus secondary structure in Stockholm (`.sto`) files. This is the updated 1.1.0 copy; see [CHANGELOG.md](CHANGELOG.md) for fixes and validation limits.

## Run from this folder

Python 3.9 or later is required. Platform wheels include R2R 1.0.6, so users do not need to install R2R separately. This checkout includes the tested Apple Silicon build. No Python third-party runtime dependencies are required.

```sh
python3 -m SMDesigner --help
python3 -m SMDesigner test
python3 -m SMDesigner "/path/to/input folder" --output-dir "/path/to/results"
python3 -m SMDesigner "/path/to/input folder" --run-r2r
```

Without an input argument, SMDesigner prompts for `test`, a folder path, or `exit`. `--run-r2r` adds per-sequence structure PDFs; R2R is required for consensus annotation even without this flag.

You can also install this copy in a dedicated virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dist/smdesigner-1.1.0-*.whl
SMDesigner test
```

## Inputs and outputs

Each input file must have aligned sequences and a balanced `#=GC SS_cons` annotation. Nested `()`, `[]`, and `{}` brackets are normalized to `<>`; crossing pseudoknots are not supported. Interleaved Stockholm blocks are concatenated. Missing annotations and length mismatches produce explicit errors. Unpaired structures are logged and skipped. As in the original selection workflow, only sequences longer than 20 ungapped bases are considered.

Every run creates a unique `SMDesigner_results_*` folder. Its default parent is the input folder's parent, or the current directory for the bundled test. `--output-dir` overrides that parent.

- `r2r_cons_sto/`: R2R consensus annotations.
- `seq_struc_mu/`: FASTA records (`w` wild type, `m..._1` disruptive, `m..._2` restorative).
- `skipped.txt`: unpaired structures, when present.
- `r2r_cons_add/`, `r2r_meta/`, `r2r_meta_pdf/`: optional drawing artifacts.
- `FAILED.txt`: error details if a run fails; partial artifacts are retained for diagnosis.

Intermediate annotation files use a private temporary directory. Existing sibling directories are never used for cleanup. A run with no mutations fails explicitly rather than reporting success. Errors exit with status 1.

## Tests

```sh
python3 -W error -m unittest discover -s tests -v
```

See [README_INSTALL.md](README_INSTALL.md) for R2R setup.

## Bundled R2R

SMDesigner uses an explicit `SMDESIGNER_R2R` executable override first, then the matching bundled binary, then R2R on PATH for source-only installations. It performs no downloads or compilation at runtime. The original source archive, build modifications, attribution and license notices ship inside the wheel under `SMDesigner/_vendor`.

For Windows, install and run the Linux package inside WSL. Native Windows Python cannot run the Linux executable. The original tool was tested in WSL; this new bundle still needs a WSL validation run. The release workflow builds Ubuntu 22.04 x86_64 wheels, targeting Ubuntu 22.04 or newer (including WSL), not every Linux distribution. Broad manylinux/PyPI distribution is a later release step.

Maintainers: `python scripts/build_r2r.py` builds the local binary; `python -m build` builds the distributions. See README_INSTALL.md for complete commands and current verification status.
