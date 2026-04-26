from pathlib import Path

p = Path("app/services/validator.py")
text = p.read_text()

old = '''                    "visa officers", "consular officers", "applicants", "review clerks",
                    "immigration staff", "security reviewers"
                ])'''

new = '''                    "visa officers", "consular officers", "applicants", "review clerks",
                    "immigration staff", "security reviewers",
                    "caseworker", "caseworkers", "benefits office", "eligibility worker",
                    "intake clerk", "intake clerks", "fraud detection unit", "fraud investigators",
                    "application form", "forms", "supporting documents", "documentation review",
                    "eligibility verification", "income threshold", "income thresholds",
                    "residency", "family status", "appeals process", "denial notice",
                    "it infrastructure", "processing backlog", "payment delay", "staff burnout"
                ])'''

if old not in text:
    raise SystemExit("target concreteness actor block not found")

text = text.replace(old, new, 1)

old2 = '''                    "visa queue", "consular interview", "security check", "background screening",
                    "document review", "processing window", "appointment slot", "administrative processing"
                ])'''

new2 = '''                    "visa queue", "consular interview", "security check", "background screening",
                    "document review", "processing window", "appointment slot", "administrative processing",
                    "application queue", "processing backlog", "benefit delay", "payment delay",
                    "eligibility verification", "documentation review", "income verification",
                    "residency verification", "recertification", "administrative hold",
                    "interview slot", "missing documents", "denial review"
                ])'''

if old2 not in text:
    raise SystemExit("target concreteness process block not found")

text = text.replace(old2, new2, 1)

old3 = '''                    "claim denial", "claim delay", "unpaid", "ghosted", "passed over",
                    "withdraws", "drops out", "lost wages", "offer rescinded",
'''

new3 = '''                    "claim denial", "claim delay", "unpaid", "ghosted", "passed over",
                    "withdraws", "drops out", "lost wages", "offer rescinded",
                    "payment delay", "benefit suspension", "benefit cutoff", "denied benefits",
                    "administrative hold", "missing paperwork", "wrongful denial", "delayed disbursement",
'''

if old3 not in text:
    raise SystemExit("target concreteness burden block not found")

text = text.replace(old3, new3, 1)

p.write_text(text)
print("patched", p)
