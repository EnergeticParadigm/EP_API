from pathlib import Path

p = Path("app/services/epra.py")
lines = p.read_text().splitlines()

target = 'payload = _normalize_payload(payload, runtime=runtime)'
insert = 'payload = _fill_structural_commitments(payload)'

out = []
inserted = 0

for i, line in enumerate(lines):
    out.append(line)
    if target in line:
        # look ahead to next few non-empty lines
        j = i + 1
        next_nonempty = None
        while j < len(lines):
            if lines[j].strip():
                next_nonempty = lines[j].strip()
                break
            j += 1
        if next_nonempty != insert:
            indent = line[:len(line) - len(line.lstrip())]
            out.append(indent + insert)
            inserted += 1

p.write_text("\n".join(out) + "\n")
print("patched", p)
print("inserted", inserted, "new filler call(s)")
