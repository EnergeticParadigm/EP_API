from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

old = """            validation_text = _render_validation_text(payload)
            provisional = self.validator.validate_text(validation_text + "\\nValidity Label: Weak EP")
            final_text = validation_text + f"\\nValidity Label: {provisional['label']}"
            validity = self.validator.validate_text(final_text)
"""

new = """            validation_text = _render_validation_text(payload)
            canonical = payload.get("canonical_setup") or {}
            provisional = self.validator.validate_canonical(canonical) if canonical else self.validator.validate_text(validation_text + "\\nValidity Label: Weak EP")
            final_text = validation_text + f"\\nValidity Label: {provisional['label']}"
            validity = self.validator.validate_canonical(canonical) if canonical else self.validator.validate_text(final_text)
"""

count = text.count(old)
if count == 0:
    raise SystemExit("target validation block not found")

text = text.replace(old, new)
p.write_text(text)
print("patched", p)
