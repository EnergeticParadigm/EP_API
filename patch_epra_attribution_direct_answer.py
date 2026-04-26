from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

old1 = """                        "core_reading": f"This is an attribution control problem centered on {target}. The available material contains an explicit authorship signal that supports naming {found}.",
                        "how_the_system_works": f"The system checks the supplied corpus for explicit origin or authorship statements. In this case, the admissible path reaches a named attribution in the record, so the output can stay bounded and specific. The answer is therefore tied to the documented attribution of {found}, rather than to inference or repetition.",
"""

new1 = """                        "core_reading": f"Direct answer: Based on the supplied material, {found} is the supported attributed origin currently identifiable for {target}. This is an attribution control problem centered on {target}.",
                        "how_the_system_works": f"The system checks the supplied corpus for explicit origin or authorship statements. In this case, the admissible path reaches a named attribution in the record, so the output can stay bounded and specific. The answer is therefore tied to the documented attribution of {found}, rather than to inference or repetition.",
"""

old2 = """                        "core_reading": f"This is an attribution control problem centered on {target}, not a generic conceptual explanation. The correct task is to determine whether the available material explicitly identifies an inventor or originating author.",
                        "how_the_system_works": "The source is the available record, including any formal specifications, corpus snippets, and named provenance. The path is to inspect those materials for explicit authorship or origin claims, then restrict the answer to whatever is directly supported. The barrier is that the currently available material does not provide a clear inventor attribution that can be named with confidence. The sink is therefore a bounded conclusion: attribution is indeterminate on the supplied evidence rather than safely assignable to a person.",
"""

new2 = """                        "core_reading": f"Direct answer: Based on the supplied material, the inventor of {target} cannot be determined. This is an attribution control problem centered on {target}, not a generic conceptual explanation.",
                        "how_the_system_works": "The source is the available record, including any formal specifications, corpus snippets, and named provenance. The path is to inspect those materials for explicit authorship or origin claims, then restrict the answer to whatever is directly supported. The barrier is that the currently available material does not provide a clear inventor attribution that can be named with confidence. The sink is therefore a bounded conclusion: attribution is indeterminate on the supplied evidence rather than safely assignable to a person.",
"""

if old1 not in s:
    raise SystemExit("first attribution block not found")
s = s.replace(old1, new1, 1)

if old2 not in s:
    raise SystemExit("second attribution block not found")
s = s.replace(old2, new2, 1)

p.write_text(s)
print("patched attribution direct answer")
