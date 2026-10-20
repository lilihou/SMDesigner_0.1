import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from SMDesigner import main as m
from SMDesigner import r2r
from SMDesigner.SMDsigner3_test_r2r import starter_function
from SMDesigner.r2r_drawing_flag_test import make_meta_file, process_files_for_r2r_pdf

SEQ = 'GGG' + 'A' * 18 + 'CCC'
STRUCT = '<<<' + '.' * 18 + '>>>'
COV = '100' + '.' * 18 + '001'
STO = f'# STOCKHOLM 1.0\nseq1 {SEQ}\n#=GC SS_cons {STRUCT}\n#=GC cov_SS_cons {COV}\n//\n'


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def parse(self, structure, cov=None):
        path = self.root / 'case.cons.sto'
        path.write_text(f'# STOCKHOLM 1.0\nseq1 AAAAAA\n#=GC SS_cons {structure}\n'
                        + (f'#=GC cov_SS_cons {cov}\n' if cov else '') + '//\n')
        return m.process_seq_struc_lines(path, self.root / 'skipped.txt')

    def test_unpaired_is_logged_and_skipped(self):
        self.assertEqual(self.parse('......'), [])
        self.assertIn('no paired structure', (self.root / 'skipped.txt').read_text())

    def test_parentheses_normalize_before_pair_check(self):
        self.assertIn('#=GC SS_cons <<..>>', self.parse('((..))', '00..00'))

    def test_malformed_structure_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unbalanced'):
            self.parse('<<...>', '00...0')

    def test_stem_length_tie_is_numeric(self):
        self.assertEqual(m.pick_stem([('stem_s1_0-9', 2), ('stem_s1_1-10', 2)]), 's1_1')

    def test_compatible_plus_conserved_pair(self):
        result = m.mu_po2('s1_0', '/'.join(['s1_0'] * 6), '100001', 'GGGCCC', '1L/2L/3L/3R/2R/1R')
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[2]), 4)

    def test_insufficient_pairs_do_not_crash(self):
        for func, cov in [(m.mu_po1, '22'), (m.mu_po2, '11'), (m.mu_po3, '00')]:
            self.assertEqual(func('s1_0', 's1_0/s1_0', cov, 'GC', '1L/1R'), ([], [], [], []))

    def test_shell_free_argument_boundaries(self):
        source = self.root / 'input space;literal.sto'
        output = self.root / 'output space.cons.sto'
        def execute(args, **kwargs):
            self.assertEqual(args[2], str(source))
            self.assertFalse(kwargs.get('shell', False))
            output.write_text(STO)
        with patch.object(r2r, 'resolve_r2r', return_value='/fake/r2r'), patch.object(r2r.subprocess, 'run', side_effect=execute):
            r2r.run_consensus(source, output)

    def test_r2r_failure_propagates(self):
        with patch.object(r2r, 'resolve_r2r', return_value='/fake/r2r'), patch.object(r2r.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'r2r', stderr='failed')):
            with self.assertRaisesRegex(RuntimeError, 'R2R failed'):
                r2r.run_consensus(self.root/'input', self.root/'out')

    def test_incompatible_executable_error(self):
        with patch.object(r2r, 'resolve_r2r', return_value='/fake/r2r'), patch.object(r2r.subprocess, 'run', side_effect=OSError('Bad CPU type')):
            with self.assertRaisesRegex(RuntimeError, 'CPU architecture'):
                r2r.run_consensus(self.root/'input', self.root/'out')

    def test_missing_output_is_failure(self):
        with patch.object(r2r, 'resolve_r2r', return_value='/fake/r2r'), patch.object(r2r.subprocess, 'run'):
            with self.assertRaisesRegex(RuntimeError, 'nonempty output'):
                r2r.run_consensus(self.root/'input', self.root/'out')

    def test_pipeline_preserves_existing_data_and_generates_mutants(self):
        source = self.root / 'sample'; source.mkdir(); (source/'sample.sto').write_text(STO)
        for name in ['seq_struc', 'seq_struc_add', 'r2r_cons_sto', 'seq_struc_mu']:
            folder = self.root/name; folder.mkdir(); (folder/'keep.txt').write_text('keep')
        def consensus(src, dst):
            dst.write_text(STO)
        with patch.object(r2r, 'run_consensus', side_effect=consensus), contextlib.redirect_stdout(io.StringIO()):
            first = m.main_sample(source)
            second = m.main_sample(source)
        self.assertNotEqual(first, second)
        records = (first/'seq_struc_mu/sample.mu.fa').read_text().splitlines()
        self.assertEqual(len(records), 6)
        self.assertEqual(records[1], SEQ)
        self.assertEqual(sum(a != b for a,b in zip(records[1], records[3])), 2)
        self.assertEqual(sum(a != b for a,b in zip(records[1], records[5])), 4)
        canonical = {'GC', 'CG', 'AU', 'UA', 'GU', 'UG'}
        for left, right in [(0,23), (1,22), (2,21)]:
            self.assertIn(records[5][left]+records[5][right], canonical)
        self.assertEqual(sum(records[3][i]+records[3][j] not in canonical for i,j in [(0,23),(1,22),(2,21)]), 2)
        for name in ['seq_struc', 'seq_struc_add', 'r2r_cons_sto', 'seq_struc_mu']:
            self.assertEqual((self.root/name/'keep.txt').read_text(), 'keep')

    def test_cli_failure_nonzero_without_success(self):
        source = self.root/'input'; source.mkdir(); (source/'x.sto').write_text(STO)
        stdout = io.StringIO()
        with patch.object(r2r, 'run_consensus', side_effect=RuntimeError('broken R2R')), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            status = starter_function([str(source)])
        self.assertEqual(status, 1)
        self.assertNotIn('finished', stdout.getvalue())
        self.assertEqual(len(list(self.root.glob('SMDesigner_results_*/FAILED.txt'))), 1)

    def test_multidot_drawing_names(self):
        cons=self.root/'cons'; cons.mkdir(); inp=self.root/'input'; inp.mkdir(); meta=self.root/'meta';meta.mkdir();pdf=self.root/'pdf';pdf.mkdir()
        (cons/'family.v2.cons.sto').write_text(STO)
        (inp/'family.v2.sto').write_text(STO)
        make_meta_file(cons, inp, meta)
        target=meta/'family.v2_1.r2r_meta'
        self.assertIn('family.v2.sto', target.read_text())
        with patch('SMDesigner.r2r_drawing_flag_test.run_r2r') as run:
            process_files_for_r2r_pdf(meta, pdf)
        self.assertEqual(run.call_args.args[1], pdf/'family.v2_1.pdf')

    def test_interleaved_stockholm_blocks(self):
        p=self.root/'block.cons.sto'
        p.write_text('seq1 GGG\n#=GC SS_cons <<.\n#=GC cov_SS_cons 00.\n\nseq1 CCC\n#=GC SS_cons .>>\n#=GC cov_SS_cons .00\n//\n')
        rows=m.process_seq_struc_lines(p,self.root/'skip')
        self.assertEqual(rows[0].split(), ['seq1','GGGCCC'])
        self.assertIn('#=GC SS_cons <<..>>',rows)


if __name__ == '__main__':
    unittest.main()
