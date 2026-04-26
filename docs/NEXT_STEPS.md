# Next Steps After v2

This version adds the four highest-value missing pieces:

1. a private corpus retriever/distiller
2. a stronger deterministic validity engine
3. an activation benchmark harness
4. a small internal pilot script for a real model endpoint

Recommended sequence:

1. Create `config/private_corpus_registry.yaml` from the example file.
2. Put preprocessed private corpus text files on the server.
3. Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`.
4. Run the API locally.
5. Run `python benchmarks/run_activation_benchmark.py`.
6. Review benchmark and pilot outputs.
7. Tighten retrieval, setup rules, and validity gates where failures cluster.
