# Replication Package for “Taming the Energy Consumption of LLM-based Distributed Trace Analysis”

This repository contains the replication package for our study on reducing the energy consumption of LLM-based distributed trace analysis. It includes TraceBench’s test set: 9,120 instances across 38 tasks based on traces from the TrainTicket microservice application. The tasks cover four analysis scopes: a single node, a pair of nodes, one trace, or a pair of traces. Test traces are available in JSON, Markdown, TRON, TOON, and CSV.

The package includes scripts for the full experimental pipeline: trace-format conversion, LLM inference and its energy measurement, PoT program generation and execution, execution-energy measurement, and result analysis. It also includes the collected energy measurements and raw run outputs. The post-processing scripts regenerate the paper’s tables and figures.

## 1. Requirements

- **Python 3.10**
- For LLM inference: an NVIDIA GPU with NVML access and local weights for Qwen3-8B, Llama-3.1-8B-Instruct, or Ministral-8B-Instruct-2410. Our runs used one H100 per job.
- For execution-energy measurement: Linux with `perf` and RAPL access.
- Dependencies are listed in `requirements.txt` (inference and PoT) and `requirements-postprocess.txt` (post-processing only).

### Installation

Install dependencies for inference and PoT:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To regenerate tables and figures, install the post-processing dependencies. If you are using the supplied outputs and do not need inference or PoT, these are the only dependencies you need:

```bash
pip install -r requirements-postprocess.txt
```

Download the selected model weights from Hugging Face. Before running inference or PoT, set `llm_name`, `llm_path`, and `job_model_name` in `config.yaml` and `configPoT.yaml` to match the model.

## 2. Directory Structure

```plaintext
├── config.yaml                   # Direct prompting configuration (model, trace format, parts)
├── configPoT.yaml                # PoT configuration (model, energy repetitions)
├── requirements.txt              # Python dependencies for inference and PoT
├── requirements-postprocess.txt  # Python dependencies for post-processing
├── dataset/TraceBench/           # 38 trace-analysis tasks and 9,120 test instances in five formats
├── Format_Conversion/            # JSON to TOON/TRON/CSV/Markdown conversion and token statistics
├── src/
│   ├── DirectPrompting/          # Inference, energy measurement, and prompt templates
│   ├── PoT/                      # Script generation, execution, and execution-energy measurement
│   ├── energy/                   # GPU (NVML) and CPU (RAPL) energy measurement
│   └── utils/                    # Post-processing pipeline
├── scripts/                      # SLURM job scripts and the figure script
├── output/                       # Raw results of our runs
├── output_processed/             # Accuracy results, statistics, paper tables, and figures
└── logs/                         # Cluster job logs
```

## 3. Running the Experiments

Choose the steps based on what you want to reproduce:

- To regenerate the paper’s tables and figures from the included run outputs, run Step 4. You can skip Steps 0–3.
- To rerun direct prompting, run Step 1. To rerun PoT generation and correctness evaluation, run Step 2; run Step 3 as well to measure program execution energy.
- Step 0 is optional. The converted test inputs are included in `dataset/TraceBench/test/preprocessed/`; run Step 0 only to regenerate the format-conversion statistics.

Run commands from the repository root unless a step says otherwise.

The SLURM scripts in `scripts/` reflect our cluster. Adapt the partition, GPU request, and `module load` line to your cluster. They activate the conda environment named by `CONDA_ENV` (a name or a path, default `traceEnv`), which applies to Steps 1 and 2.

### Step 0: Convert trace formats (optional)

The code in `Format_Conversion/` converts the JSON test traces to TOON, TRON, CSV, and Markdown. It also calculates token and character savings compared with JSON.

- `shared_format/converter.py` reads `shared_format/test_tasks_preprocessed_Graph2Text_raw_spans_desc_with_step.json` and writes converted instances and summaries to `shared_format/output/`.
- `toon-python/` and `tron-python/` contain the TOON and TRON encoders.
- Token counts use `tiktoken` with its default `o200k_base` encoding.

```bash
pip install tiktoken
python Format_Conversion/shared_format/converter.py
```

**Outputs:** Saved in `Format_Conversion/shared_format/output/`.

### Step 1: Run direct prompting

Set the model and trace format in `config.yaml` (`job_model_name`, `input_data_format`, and `job_parts`), then submit the jobs from the repository root. One submission runs one model and one trace format; change `config.yaml` and submit again for each other combination.

```bash
export CONDA_ENV=/path/to/conda/env      # name or path of your environment
bash scripts/direct_prompting/submit_all_parallel.sh     # or submit_all_sequential.sh
```

To run one part without SLURM:

```bash
python3 -u src/DirectPrompting/app_inference_with_measure.py dataset/TraceBench/test/parts/part_1_ids.json
```

**Outputs:** Responses and energy records in `output/`.

### Step 2: Generate and run Program-of-Thought scripts

Set the model in `configPoT.yaml`, then submit the generation and execution jobs from the repository root. Both jobs loop over all six settings (zero-shot and one to five examples).

```bash
sbatch scripts/PoT/run_scripts_Generator.sh    # generates the programs
sbatch scripts/PoT/run_scripts_Runner.sh       # executes them on the test instances
```

To run a single setting, for example two examples, run `cd src/PoT && python3 01_generate_scripts.py --shots 2` and then `python3 02_execute_scripts.py --shots 2`. Accuracy is computed in Step 4.

**Outputs:** `output/generated_scripts/` and `output/executed_scripts_results/`.

### Step 3: Measure execution energy

Run this step on a dedicated Linux machine with RAPL access through `perf`. Run the command from `src/PoT`:

```bash
cd src/PoT && python3 03_measure_execution_energy.py
```

**Output:** `output/execution_energy/execution_energy_<host>.csv`.

### Step 4: Regenerate results

Run the post-processing pipeline from the repository root:

```bash
python3 src/utils/run_all_postprocess.py
```

**Outputs:** Accuracy results in `output_processed/accuracy*/`, statistics in `output_processed/analysis/`, paper tables in `output_processed/tables/`, and figures in `output_processed/figures/`.

## 4. Data Availability

The large data files, namely `dataset/` and `Format_Conversion/shared_format/test_tasks_preprocessed_Graph2Text_raw_spans_desc_with_step.json`, are hosted on Zenodo: [https://doi.org/10.5281/zenodo.24476334](https://doi.org/10.5281/zenodo.24476334). If they are missing from your copy of the package, download `data.zip` from that record and extract it in the repository root. Steps 0 and 4 read from these files.

## 5. Replication Scope

The raw outputs of our runs are included. Step 4 can therefore regenerate all paper tables and figures without a GPU. Re-running Steps 1 to 3 requires the hardware listed above.

