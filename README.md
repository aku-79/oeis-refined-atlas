# oeis-refined-atlas

Public support repository for the refined bracelet atlas OEIS submissions.

Requirements:

- Python 3.11 or newer;
- no third-party runtime dependencies at the moment;
- the repo is run from the existing conda environment `tumm`, not from a dedicated virtualenv.

Current scope:

- shared combinatorial code for the active publication track;
- the A396630 module and its data/CLI entrypoint;
- short docs that can be extended when the next sequences are added.

## Layout

- `src/oeis_refined_atlas/common.py`: shared combinatorial routines.
- `src/oeis_refined_atlas/a396630.py`: active sequence module.
- `docs/A396630.md`: publication note for the active sequence.

## Run

After installation, the current sequence can be printed with:

```bash
python -m oeis_refined_atlas.a396630
```