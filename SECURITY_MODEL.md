# Security Model

## Goal

Protect the full EPRA corpus while still allowing EPRA behavior to be served through a model endpoint.

## Boundary

- Full corpus stays on your server.
- Private corpus registry stays on your server.
- Wrapper performs retrieval and distillation locally.
- Model sees only distilled runtime slices.

## Main controls

1. No raw full-document forwarding.
2. Distillation caps per snippet.
3. Private registry kept out of public repositories.
4. Deterministic validity checks after model output.
5. Benchmark and pilot evaluation before external release.

## Residual risk

The model still sees a compact derivative of the corpus. This is much smaller than sharing the full documents, but it is not the same as zero exposure. Reduce risk further by tightening distillation and keeping the wrapper server private.
