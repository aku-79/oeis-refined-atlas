# oeis-refined-atlas

Public support repository for the refined bracelet atlas OEIS submissions.

Requirements:

- Python 3.11 or newer;
- no third-party runtime dependencies;

Current scope:

- package modules and CLI entrypoints;
- standalone OEIS programs;
- short docs that can be extended as the sequence family grows.

## Layout

- `src/oeis_refined_atlas/common.py`: shared combinatorial routines.
- `src/oeis_refined_atlas`: package modules for the sequences.
- `programs`: self-contained programs.
- `docs`: publication notes.

## Run

After installation, the package modules can be printed with:

```bash
python -m oeis_refined_atlas.a396630
python -m oeis_refined_atlas.a396631
python -m oeis_refined_atlas.a396632
python -m oeis_refined_atlas.a395436
python -m oeis_refined_atlas.a396085
python -m oeis_refined_atlas.a396051
```

The standalone OEIS programs can also be run directly:

```bash
python programs/a396630.py
python programs/a396631.py
python programs/a396632.py
python programs/a395436.py
python programs/a396085.py
python programs/a396051.py
```

## Acknowledgements

This repository contains code, computational experiments and resources related to a research project in number theory, including integer sequences submitted to OEIS. The main contributors are:

- [Andrea Cutri](https://orcid.org/0009-0007-6158-3501) — project lead, mathematical research, sequences discovery and OEIS submissions.
- **Giulio Casu** — contributions to mathematical research and investigation.
- **Anselmo Casu** — contributions to mathematical research, computational experiments and implementation.
- [Francesca Sotgiu](https://github.com/fran-00) — software development, computational methods, implementation and technical support.
