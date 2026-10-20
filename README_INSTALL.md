# Install bundled SMDesigner 1.1.0

Use Python 3.9 or later. Create an environment and install the wheel for your system:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install /path/to/smdesigner-1.1.0-py3-none-macosx_11_0_arm64.whl
SMDesigner test --run-r2r
```

The filename above is for Apple Silicon. R2R is included; a compiler, system R2R, Perl, and separate Infernal installation are not needed for the tested consensus/PDF workflow. R2R embeds the required Squid code.

## Windows through WSL / Linux

Run these commands inside WSL, with Linux Python. Use the `linux_x86_64` wheel from the Ubuntu release job instead of the macOS wheel. This first Linux build targets Ubuntu 22.04 or newer, including Ubuntu under WSL; it is not a general manylinux release. WSL on ARM requires a separate ARM64 Linux build.

## Maintainer builds

A C/C++ compiler, SDK/development headers and make are needed only when building R2R from source. The pinned archive is included, so building R2R itself requires no download.

```sh
python3 -m venv .build-env
. .build-env/bin/activate
python -m pip install 'setuptools>=77' wheel build
python scripts/build_r2r.py
python -W error -m unittest discover -s tests -v
python -m build --no-isolation
```

On macOS the script targets macOS 11+ and uses the installed Command Line Tools when available. Set `MAKE` to an alternate make executable if needed. `CC`, `CXX`, `SDKROOT`, and compiler flag overrides are available for maintainers. Do not use overrides that increase the minimum OS version without updating wheel tags.

On Ubuntu/WSL, install `build-essential` and Python's venv support before building. Linux builds use the host's system libraries, so build on the oldest intended Ubuntu target and test on your recipients' systems.

The workflow `.github/workflows/bundled-release.yml` builds on Apple Silicon, Intel macOS, and Ubuntu 22.04. It installs each wheel into an isolated environment and runs the real mutation/PDF smoke test with PATH emptied. It creates downloadable build artifacts; it does not publish to PyPI or GitHub Releases.

## Validation status

- Apple Silicon: 18 regression tests passed. The installed wheel ran with PATH empty and produced 2 FASTA files (351 records) and 117 PDFs using real R2R. The binary targets macOS 11+, but this test only establishes behavior on the current host.
- Intel macOS and Ubuntu/WSL: build/test workflow prepared; not executed in this local session. The old SMDesigner was tested in WSL, but the new bundle needs its own test.
- Optional R2R CFSQP/NLopt solvers are not included. Drawings requiring those optional solvers can fail with an explicit R2R error.

## Advanced override

Set `SMDESIGNER_R2R=/absolute/path/to/r2r` to use your own compatible build. Otherwise the matching bundled executable is preferred over PATH. System R2R installations are not changed.
