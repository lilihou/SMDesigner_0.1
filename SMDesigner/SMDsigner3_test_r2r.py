"""Command-line entry point; mutation logic lives in main.py."""
import argparse
import sys
from pathlib import Path
from SMDesigner.main import main_test, main_sample


def starter_function(argv=None):
    parser = argparse.ArgumentParser(description='Design disruptive and restorative RNA mutations.')
    parser.add_argument('input', nargs='?', help="Stockholm folder, or 'test' for the bundled demo")
    parser.add_argument('--run-r2r', action='store_true', help='Also generate structure PDFs')
    parser.add_argument('--output-dir', type=Path, help='Parent directory for a new results folder')
    args = parser.parse_args(argv)
    try:
        value = args.input
        if value is None:
            value = input("Enter 'test', an input folder, or 'exit': ").strip()
        if value.lower() == 'exit':
            return 0
        if value == 'test':
            main_test(Path(__file__).parent / 'test', args.output_dir, args.run_r2r)
        else:
            main_sample(Path(value), args.output_dir, args.run_r2r)
    except (Exception, KeyboardInterrupt) as exc:
        print(f'SMDesigner failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(starter_function())
