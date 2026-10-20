"""Validate installed bundle using real R2R with no PATH dependency."""
import os
from pathlib import Path
import tempfile
from SMDesigner import main, r2r


def main_test():
    os.environ.pop('SMDESIGNER_R2R', None)
    os.environ['PATH'] = ''
    executable = Path(r2r.resolve_r2r())
    assert '_vendor' in executable.parts, executable
    with tempfile.TemporaryDirectory(prefix='SMDesigner smoke ') as output:
        results = main.main_test(Path(main.__file__).parent/'test', Path(output), run_r2r=True)
        fasta = list((results/'seq_struc_mu').glob('*.mu.fa'))
        pdfs = list((results/'r2r_meta_pdf').glob('*.pdf'))
        assert fasta and all(p.stat().st_size for p in fasta)
        assert pdfs and all(p.read_bytes().startswith(b'%PDF') for p in pdfs)
        count = sum(p.read_text().count('>') for p in fasta)
        assert count % 3 == 0
        print(f'PASS: bundled {executable}; {len(fasta)} FASTA files, {count} records, {len(pdfs)} PDFs')


if __name__ == '__main__':
    main_test()
