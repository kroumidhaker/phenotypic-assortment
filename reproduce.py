"""Run the notebook calculations without starting Jupyter."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results'),
                        help='output directory (default: results)')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    output = args.output.resolve()
    reference = root / 'reference_results'
    if output == reference or reference in output.parents:
        parser.error('Choose an output directory outside reference_results.')

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.show = lambda *a, **k: None

    notebook = json.loads((root / 'reproduce_figures.ipynb').read_text(encoding='utf-8'))
    namespace = {'__name__': '__main__', 'RUN_OUTPUT_DIR': output}
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        source = cell['source']
        source = ''.join(source) if isinstance(source, list) else source
        source = '\n'.join(line for line in source.splitlines()
                           if line.strip() != '%matplotlib inline')
        exec(compile(source, f'reproduce_figures.ipynb:cell_{index}', 'exec'), namespace)
        plt.close('all')
    print('Finished. Outputs:', output)


if __name__ == '__main__':
    main()
