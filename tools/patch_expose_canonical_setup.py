from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

old = '''                metadata={
                    "task_system": target,
                    "active_forms": payload["compact_ep_setup"]["active_forms"],
                    "structured_setup": payload["compact_ep_setup"],
                    "analysis_sections": payload.get("analysis_sections"),
                    "distilled_corpus": distilled,
                    "validity": validity,
                },'''

new = '''                metadata={
                    "task_system": target,
                    "active_forms": payload["compact_ep_setup"]["active_forms"],
                    "structured_setup": payload["compact_ep_setup"],
                    "canonical_setup": payload.get("canonical_setup"),
                    "analysis_sections": payload.get("analysis_sections"),
                    "distilled_corpus": distilled,
                    "validity": validity,
                },'''

count = text.count(old)
if count == 0:
    raise SystemExit("target metadata block not found")

text = text.replace(old, new)

old2 = '''            metadata={
                "task_system": runtime.task_system,
                "active_forms": runtime.active_forms,
                "structured_setup": payload["compact_ep_setup"],
                "analysis_sections": payload.get("analysis_sections"),
                "distilled_corpus": distilled,
                "validity": validity,
            },'''

new2 = '''            metadata={
                "task_system": runtime.task_system,
                "active_forms": runtime.active_forms,
                "structured_setup": payload["compact_ep_setup"],
                "canonical_setup": payload.get("canonical_setup"),
                "analysis_sections": payload.get("analysis_sections"),
                "distilled_corpus": distilled,
                "validity": validity,
            },'''

if old2 not in text:
    raise SystemExit("runtime metadata block not found")

text = text.replace(old2, new2, 1)

p.write_text(text)
print("patched", p)
