"""Compare regenerated numerical data with the supplied reference results."""
import argparse
import json
from pathlib import Path
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=Path('results'))
    args = parser.parse_args()
    reference = Path(__file__).resolve().parent / 'reference_results'
    results = args.results.resolve()
    if not (results / 'data').is_dir():
        parser.error('No result data found. Run python reproduce.py first.')
    if results == reference:
        parser.error('Supply newly generated results, not reference_results itself.')

    count = 0
    largest = 0.0
    for path in sorted((reference / 'data').glob('*.csv')):
        target = results / 'data' / path.name
        expected = np.genfromtxt(path, delimiter=',', names=True)
        actual = np.genfromtxt(target, delimiter=',', names=True)
        if expected.dtype.names != actual.dtype.names or expected.shape != actual.shape:
            raise AssertionError(f'Columns or rows differ: {path.name}')
        for field in expected.dtype.names:
            np.testing.assert_allclose(actual[field], expected[field], rtol=5e-11,
                                       atol=5e-13, err_msg=f'{path.name}: {field}')
            relative = np.abs(actual[field]-expected[field])/np.maximum(np.abs(expected[field]), 1e-300)
            largest = max(largest, float(np.max(relative)))
        count += len(expected)

    for path in sorted((reference / 'data').glob('*.npz')):
        with np.load(path) as expected, np.load(results / 'data' / path.name) as actual:
            if set(expected.files) != set(actual.files):
                raise AssertionError(f'Array names differ: {path.name}')
            for field in expected.files:
                np.testing.assert_allclose(actual[field], expected[field], rtol=5e-11,
                                           atol=5e-13, err_msg=f'{path.name}: {field}')

    expected_summary = json.loads((reference / 'checks/run_summary.json').read_text())
    summary = json.loads((results / 'checks/run_summary.json').read_text())
    if summary['figures'] != expected_summary['figures'] or summary['data_tables'] != expected_summary['data_tables']:
        raise AssertionError('The figure or data-table list differs.')
    checks = json.loads((results / 'checks/validation_results.json').read_text())
    if len(checks) != expected_summary['validation_comparisons']:
        raise AssertionError('The number of numerical checks differs.')
    if not all(np.isfinite(row['relative_difference']) and row['relative_difference'] < 2e-11 for row in checks):
        raise AssertionError('A numerical check did not pass.')
    bounds = json.loads((results / 'checks/series_certificates.json').read_text())
    if not bounds or not all(np.isfinite(row['relative_truncation_bound']) and
                             row['relative_truncation_bound'] <= 1e-12 for row in bounds):
        raise AssertionError('A series truncation bound did not pass.')
    for stem in (Path(name).stem for name in summary['figures']):
        for suffix in ('.png', '.pdf'):
            path = results / 'figures' / (stem + suffix)
            if not path.is_file() or path.stat().st_size == 0:
                raise AssertionError(f'Missing figure: {path.name}')
    print(f'PASS: {count:,} data rows, two saved grids, seven figures, and numerical checks.')
    print(f'Maximum relative difference from the reference data: {largest:.3e}')
    print('Image bytes are not compared; rendering can vary with fonts and software versions.')


if __name__ == '__main__':
    main()
