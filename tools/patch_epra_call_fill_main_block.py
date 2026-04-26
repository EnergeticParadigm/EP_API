from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

old = """        payload = _normalize_payload(payload, runtime=runtime)
        validation_text = _render_validation_text(payload)
"""

new = """        payload = _normalize_payload(payload, runtime=runtime)
        payload = _fill_structural_commitments(payload)
        validation_text = _render_validation_text(payload)
"""

count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly 1 remaining main normalize->validation block, found {count}")

text = text.replace(old, new, 1)
p.write_text(text)
print("patched", p)
