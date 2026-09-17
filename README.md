# PARSEME Diagnostic

Python scripts for computing structural statistics and inter-MWE diagnostics on corpora in PARSEME CUPT format.

PARSEME Diagnostic provides sentence-, token-, and MWE-level statistics, with particular attention to structural relations between verbal multiword expressions (VMWEs), including token sharing, crossing, and nesting patterns.

## Overview

The software was developed to analyse the structural characteristics of the PARSEME VMWE corpora. It can process a single language or multiple languages and reports statistics separately for the `train.cupt`, `dev.cupt`, and `test.cupt` files. A `system.cupt` file is also processed when available.

The analysis includes:

* sentence distributions according to sentence length and number of MWEs;
* token-level statistics;
* MWE distributions according to length and category;
* crossing and nesting relations between MWEs;
* token-sharing patterns between MWEs.

When several languages are analysed simultaneously, the corresponding statistics are combined into comparative tables.

## Repository structure

The repository contains three Python files:

* `do_count.py`: command-line entry point for running the analysis;
* `counter.py`: functions for computing and displaying corpus statistics and inter-MWE diagnostics;
* `tools.py`: auxiliary functions for reading and processing CUPT files.

## Requirements

PARSEME Diagnostic requires Python 3.

No installation procedure is required. Download or clone the repository and run the scripts directly from the command line.

## Input data

The input corpus must be organised into subdirectories corresponding to language codes. Each language directory may contain the standard PARSEME CUPT files:

```text
corpus/
├── EN/
│   ├── train.cupt
│   ├── dev.cupt
│   └── test.cupt
├── ES/
│   ├── train.cupt
│   ├── dev.cupt
│   └── test.cupt
└── ...
```

If present, `system.cupt` files are also processed.

The corpus files themselves are not distributed with this repository.

## Usage

To analyse a specific language:

```bash
python do_count.py <corpus_folder> <language>
```

For example:

```bash
python do_count.py /path/to/corpus ES
```

To analyse all languages contained in the corpus directory:

```bash
python do_count.py /path/to/corpus ALL
```

The language argument may also be omitted to process all available languages:

```bash
python do_count.py /path/to/corpus
```

## Output

The results are printed to standard output and are organised separately for the available `train.cupt`, `dev.cupt`, `test.cupt`, and `system.cupt` files.

The reported statistics include distributions at sentence, token, and MWE levels, as well as diagnostics concerning structural relations between MWEs, such as crossing, nesting, and token sharing.

## Citation

If you use PARSEME Diagnostic in your research, please cite the following paper:

> Fernández Lanza, S., Darriba Bilbao, V. M., & Fernández-González, D. (2026). *A diagnostic and evaluative analysis of PARSEME corpora complexity*. Research Square (preprint). https://doi.org/10.21203/rs.3.rs-9023725/v1

The manuscript is currently under review at *Language Resources and Evaluation*.

A DOI for PARSEME Diagnostic will also be provided through Zenodo.

## License

See the `LICENSE` file for information about reuse and redistribution.
