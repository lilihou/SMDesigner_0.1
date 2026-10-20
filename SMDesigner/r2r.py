"""Checked, shell-free R2R invocation."""
import os
import platform
import shutil
import subprocess
from pathlib import Path



def bundle_platform():
    machine = platform.machine().lower()
    machine = {'aarch64': 'arm64', 'amd64': 'x86_64'}.get(machine, machine)
    return f'{platform.system().lower()}-{machine}'


def resolve_r2r():
    override = os.environ.get('SMDESIGNER_R2R')
    if override:
        path = Path(override).expanduser().resolve()
        if not path.is_file() or not os.access(path, os.X_OK):
            raise RuntimeError(f'SMDESIGNER_R2R is not executable: {path}')
        return str(path)
    directory = Path(__file__).parent / '_vendor' / bundle_platform()
    bundled = directory / 'r2r'
    if bundled.is_file():
        if not os.access(bundled, os.X_OK):
            raise RuntimeError(f'Bundled R2R lacks execute permission: {bundled}')
        return str(bundled)
    executable = shutil.which('r2r')
    if executable:
        return executable
    raise RuntimeError(f'No R2R available for {bundle_platform()}. Install a matching bundled wheel; on Windows run inside WSL. See README_INSTALL.md.')

def run_r2r(arguments, output):
    executable = resolve_r2r()
    try:
        subprocess.run([executable, *map(str, arguments)], check=True,
                       capture_output=True, text=True, timeout=300)
    except OSError as exc:
        raise RuntimeError(f'Cannot execute R2R at {executable}: {exc}. Check CPU architecture and permissions.') from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f'R2R failed (exit {exc.returncode}): {exc.stderr or exc.stdout}') from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('R2R timed out after 300 seconds.') from exc
    output = Path(output)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(f'R2R did not produce a nonempty output: {output}')


def run_consensus(source, output):
    run_r2r(['--GSC-weighted-consensus', source, output,
             '3', '0.97', '0.9', '0.75', '4', '0.97', '0.9', '0.75', '0.5', '0.1'], output)
