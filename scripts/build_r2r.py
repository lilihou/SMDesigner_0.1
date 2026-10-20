#!/usr/bin/env python3
"""Build pinned R2R from the included source; no global install or downloads."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'SMDesigner' / '_vendor'
SHA256 = '1ba8f51db92866ebe1aeb3c056f17489bceefe2f67c5c0bbdfbddc0eee17743d'


def main():
    archive = VENDOR / 'source' / 'R2R-1.0.6.tgz'
    if hashlib.sha256(archive.read_bytes()).hexdigest() != SHA256:
        raise RuntimeError('R2R source archive checksum mismatch')
    system = platform.system().lower()
    machine = {'aarch64': 'arm64', 'amd64': 'x86_64'}.get(platform.machine().lower(), platform.machine().lower())
    if system not in ('darwin', 'linux') or machine not in ('arm64', 'x86_64'):
        raise RuntimeError('Build on macOS or Linux/WSL with ARM64 or x86_64')
    env = os.environ.copy()
    make = os.environ.get('MAKE') or shutil.which('make')
    if not make:
        raise RuntimeError('make is required')
    make_args = [make, '-j2']
    configure_args = []
    env.setdefault('CFLAGS', '-O2')
    env.setdefault('CXXFLAGS', '-O2 -std=c++11')
    if system == 'darwin':
        # Use the separately installed Command Line Tools when available.
        tools = Path('/Library/Developer/CommandLineTools/usr/bin')
        if (tools / 'clang').exists():
            env.setdefault('CC', str(tools / 'clang'))
            env.setdefault('CXX', str(tools / 'clang++'))
            env.setdefault('SDKROOT', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk')
            make_args += [f'AR={tools / "ar"}', f'RANLIB={tools / "ranlib"}']
        sdk = env.get('SDKROOT') or subprocess.check_output(['xcrun', '--show-sdk-path'], text=True).strip()
        env['SDKROOT'] = sdk
        headers = Path(sdk) / 'usr/include/c++/v1'
        if headers.exists():
            env['CXXFLAGS'] += f' -isystem {headers}'
        env['MACOSX_DEPLOYMENT_TARGET'] = '11.0'
        env['CFLAGS'] += ' -mmacosx-version-min=11.0'
        env['CXXFLAGS'] += ' -mmacosx-version-min=11.0'
        configure_args = [f'--build={"aarch64" if machine == "arm64" else machine}-apple-darwin']
    with tempfile.TemporaryDirectory(prefix='smd-r2r-build-') as tmp:
        with tarfile.open(archive) as tar:
            # Digest pins a known archive, also reject escaping members and links.
            for entry in tar.getmembers():
                path = Path(entry.name)
                if path.is_absolute() or '..' in path.parts or entry.issym() or entry.islnk():
                    raise RuntimeError(f'Unsafe archive entry: {entry.name}')
            tar.extractall(tmp)
        source = Path(tmp) / 'R2R-1.0.6'
        patches = {
            'config.sub': ('| arm-* ', '| aarch64-* | arm64-* | arm-* '),
            'src/multiDimVector.h': ('this->Load(_s1,_s2,_s3);', 'this->Init(_s1,_s2,_s3);'),
            'src/SymbolicMath.h': ('return finite(x)!=0;', 'return std::isfinite(x);'),
            'src/GSCConsensus.cpp': ('return finite(x)!=0;', 'return std::isfinite(x);'),
        }
        for name, (old, new) in patches.items():
            path = source / name
            text = path.read_text()
            if old not in text:
                raise RuntimeError(f'Expected patch location missing in {name}')
            path.write_text(text.replace(old, new))
        # Optional CFSQP and NLopt are disabled by upstream default. Do not pass
        # --disable-* here: this old configure treats presence as enabling them.
        subprocess.run(['sh', './configure', *configure_args], cwd=source, env=env, check=True)
        subprocess.run(make_args, cwd=source, env=env, check=True)
        destination = VENDOR / f'{system}-{machine}'
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / 'src/r2r', destination / 'r2r')
        (destination / 'r2r').chmod(0o755)
        metadata = {'version': '1.0.6', 'source_sha256': SHA256,
                    'platform': f'{system}-{machine}', 'patches': list(patches),
                    'build_script': 'scripts/build_r2r.py',
                    'macos_deployment_target': '11.0' if system == 'darwin' else None}
        (destination / 'build.json').write_text(json.dumps(metadata, indent=2) + '\n')
        print(f'Bundled R2R: {destination / "r2r"}')


if __name__ == '__main__':
    main()
