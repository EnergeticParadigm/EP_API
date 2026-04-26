# Private Corpus Layout

The full EPRA corpus should remain on your own server.

Recommended practice:

- Convert long PDFs into high-quality `.txt` or `.md` files offline.
- Register each file in `config/private_corpus_registry.yaml`.
- Keep the registry and corpus directory outside any public repo.
- Expose only distilled runtime slices to the model.

Suggested private directory:

```text
/srv/epra/private_corpus/
  EP_FCS_v0.txt
  EP_Methodology_FULL.txt
  EP_FCS_D1_Completion_Block_v1.txt
  EP_FCS_D2_Theorem_Block_v1.txt
  EP_FCS_D3_Theorem_Block_v1.txt
  EP_FCS_D4_Theorem_Block_v1.txt
  EPRA_Bootstrap_Specification_v1.txt
```

The wrapper should **never** send full documents to the model. It should retrieve and distill only the smallest task-relevant slices.
