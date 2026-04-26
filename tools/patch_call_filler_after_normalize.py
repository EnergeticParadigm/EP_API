from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

old = """            payload = _normalize_payload(payload, runtime=runtime)
            validation_text = _render_validation_text(payload)
"""
new = """            payload = _normalize_payload(payload, runtime=runtime)
            payload = _fill_structural_commitments(payload)
            validation_text = _render_validation_text(payload)
"""

count_before = text.count(new)
count_old = text.count(old)

if count_old == 0:
    raise SystemExit("no remaining normalize->validation blocks found")

text = text.replace(old, new)

p.write_text(text)
print(f"patched {p}")
print(f"replaced {count_old} remaining blocks")
print(f"existing filled blocks before patch: {count_before}")
