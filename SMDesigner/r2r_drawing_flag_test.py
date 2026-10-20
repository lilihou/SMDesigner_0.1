"""Generate per-sequence R2R drawings inside the current run directory."""
from pathlib import Path
from SMDesigner.r2r import run_r2r


def process_files_for_r2r_draw1(input_folder, output_folder):
    for source in sorted(Path(input_folder).glob('*.cons.sto')):
        text = source.read_text()
        if '//' not in text:
            raise ValueError(f'Missing Stockholm terminator: {source}')
        text = text.replace('//', '#=GF R2R SetDrawingParam autoBreakPairs true\n//', 1)
        (output_folder / source.name).write_text(text)


def make_meta_file(input_folder1, input_folder2, output_folder):
    for source in sorted(Path(input_folder1).glob('*.cons.sto')):
        stem = source.name[:-len('.cons.sto')]
        original = (Path(input_folder2) / (stem + '.sto')).resolve()
        if not original.is_file():
            raise ValueError(f'Missing original Stockholm input: {original}')
        names = list(dict.fromkeys(line.split()[0] for line in source.read_text().splitlines()
                                  if line.strip() and not line.startswith(('#', '//'))))
        for number, name in enumerate(names, 1):
            text = (str(source.resolve()) + '\n') if number == 1 else ''
            text += f'{original}\toneseq\t{name}\n'
            (output_folder / f'{stem}_{number}.r2r_meta').write_text(text)


def process_files_for_r2r_pdf(input_folder, output_folder):
    for source in sorted(Path(input_folder).glob('*.r2r_meta')):
        output = output_folder / (source.stem + '.pdf')
        run_r2r(['--disable-usage-warning', source, output], output)


def draw_structures(input_folder, run_dir):
    drawing = run_dir / 'r2r_cons_add'
    meta = run_dir / 'r2r_meta'
    pdf = run_dir / 'r2r_meta_pdf'
    for folder in (drawing, meta, pdf):
        folder.mkdir(parents=True, exist_ok=True)
    process_files_for_r2r_draw1(run_dir / 'r2r_cons_sto', drawing)
    make_meta_file(drawing, input_folder, meta)
    process_files_for_r2r_pdf(meta, pdf)
