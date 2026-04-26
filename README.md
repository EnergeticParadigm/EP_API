# EPRA API Wrapper v2

EPRA API Wrapper v2 keeps the **full EPRA corpus on your own server** and sends the model only a **minimal derived activation state**.

This version adds:

- a private corpus retriever/distiller
- a stronger deterministic validity engine
- an activation benchmark harness
- a small internal pilot script against a real model endpoint

## Core endpoints

- `GET /healthz`
- `POST /analyze`
- `POST /validate`
- `POST /reconstruct`

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/private_corpus_registry.example.yaml config/private_corpus_registry.yaml
# edit the registry to point at your private server-side text files
export OPENAI_API_KEY=...
uvicorn app.main:app --reload
```

## Environment variables

- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional)
- `EPRA_RUNTIME_CONFIG` (optional)
- `EPRA_PRIVATE_CORPUS_REGISTRY` (optional)

## Benchmark

```bash
python benchmarks/run_activation_benchmark.py
```

## Internal pilot

```bash
python pilot/run_internal_pilot.py
```

## Security model

- Keep full corpus files server-side only.
- Register only preprocessed text paths in the local registry.
- Send only distilled runtime slices to the model.
- Never forward full documents or raw private annotations.
