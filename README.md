# oeis-refined-atlas

Public support repository for the refined bracelet atlas OEIS submissions.

Requirements:

- Python 3.11 or newer;
- no third-party runtime dependencies at the moment;
- the repo is run from the existing conda environment `tumm`, not from a dedicated virtualenv.

Current scope:

- shared combinatorial code for the refined bracelet atlas publication track;
- package modules and CLI entrypoints for A396630, A396631, and A396632;
- standalone OEIS programs for A396630, A396631, and A396632;
- short docs that can be extended as the sequence family grows.

## Layout

- `src/oeis_refined_atlas/common.py`: shared combinatorial routines.
- `src/oeis_refined_atlas/a396630.py`: package module for A396630.
- `src/oeis_refined_atlas/a396631.py`: package module for A396631.
- `src/oeis_refined_atlas/a396632.py`: package module for A396632.
- `src/oeis_refined_atlas/a395436.py`: package module for A396633.
- `programs/a396630.py`: self-contained program.
- `programs/a396631.py`: self-contained program.
- `programs/a396632.py`: self-contained program.
- `programs/a395436.py`: self-contained program.
- `docs/A396630.md`: publication note for the active sequence.
- `docs/A396631.md`: publication note for A396631.
- `docs/A396632.md`: publication note for A396632.
- `docs/A395436.md`: publication note for A396632.

## Run

After installation, the package modules can be printed with:

```bash
python -m oeis_refined_atlas.a396630
python -m oeis_refined_atlas.a396631
python -m oeis_refined_atlas.a396632
python -m oeis_refined_atlas.a395436
```

The installed console scripts are `oeis-a396630`, `oeis-a396631`, and `oeis-a396632`.

The standalone OEIS programs can also be run directly:

```bash
python programs/a396630.py
python programs/a396631.py
python programs/a396632.py
python programs/a395436.py
```
