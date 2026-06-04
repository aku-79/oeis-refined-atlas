# oeis-refined-atlas

Public support repository for the refined bracelet atlas OEIS submissions.

Requirements:

- Python 3.11 or newer;
- no third-party runtime dependencies at the moment;
- the repo is run from the existing conda environment `tumm`, not from a dedicated virtualenv.

Current scope:

- shared combinatorial code for the refined bracelet atlas publication track;
- the A396630 module and its data/CLI entrypoint;
- standalone OEIS programs for A396630, A396631, and A396632;
- short docs that can be extended as the sequence family grows.

## Layout

- `src/oeis_refined_atlas/common.py`: shared combinatorial routines.
- `src/oeis_refined_atlas/a396630.py`: active sequence module.
- `programs/a396630.py`: self-contained program suitable for linking from OEIS.
- `programs/a396631.py`: self-contained program suitable for linking from OEIS.
- `programs/a396632.py`: self-contained program suitable for linking from OEIS.
- `docs/A396630.md`: publication note for the active sequence.
- `docs/A396631.md`: publication note for A396631.
- `docs/A396632.md`: publication note for A396632.

## Run

After installation, the current sequence can be printed with:

```bash
python -m oeis_refined_atlas.a396630
```

The standalone OEIS program can also be run directly:

```bash
python programs/a396630.py
```

The companion standalone programs are:

```bash
python programs/a396631.py
python programs/a396632.py
```
