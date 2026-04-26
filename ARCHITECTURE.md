# Architecture

## High-level flow

1. User task arrives at the wrapper.
2. Runtime builder classifies the task system.
3. Private corpus retriever fetches only server-side relevant sources.
4. Distiller compresses those sources into small runtime slices.
5. Wrapper sends only the distilled activation state to the model endpoint.
6. Deterministic validity engine scores the output.
7. Benchmark and pilot harnesses evaluate activation reliability.

## Components

- `app/services/corpus.py` — private retrieval and distillation
- `app/services/runtime.py` — runtime-state construction
- `app/services/validator.py` — deterministic validity engine
- `app/services/openai_client.py` — Responses API gateway
- `benchmarks/run_activation_benchmark.py` — benchmark harness
- `pilot/run_internal_pilot.py` — small internal pilot

## Design principle

The model should never become the storage location of the full EPRA corpus. The model receives only the smallest task-relevant slices required to activate EPRA behavior.
