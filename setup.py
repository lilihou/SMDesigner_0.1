from pathlib import Path
import platform
from setuptools import setup, find_packages
from setuptools.command.bdist_wheel import bdist_wheel

ROOT = Path(__file__).parent
machine = {'aarch64': 'arm64', 'amd64': 'x86_64'}.get(platform.machine().lower(), platform.machine().lower())
key = f'{platform.system().lower()}-{machine}'
binary = ROOT / 'SMDesigner' / '_vendor' / key / 'r2r'


class PlatformWheel(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        if not binary.is_file():
            raise RuntimeError('Build bundled R2R first: python scripts/build_r2r.py')
        self.root_is_pure = False
        if platform.system() == 'Darwin':
            self.plat_name = f'macosx_11_0_{machine}'

    def get_tag(self):
        _, _, plat = super().get_tag()
        return 'py3', 'none', plat


setup(
    name='SMDesigner', version='1.1.0',
    description='RNA structure mutation designer with bundled R2R',
    long_description=(ROOT / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests',)), python_requires='>=3.9',
    include_package_data=False,
    package_data={'SMDesigner': ['test/demo/*.sto', 'R2R_install.sh',
        f'_vendor/{key}/*', '_vendor/licenses/*', '_vendor/source/*']},
    license='GPL-3.0-or-later',
    cmdclass={'bdist_wheel': PlatformWheel},
    entry_points={'console_scripts': ['SMDesigner=SMDesigner.SMDsigner3_test_r2r:starter_function']},
)
