from pathlib import Path

p = Path("app/services/validator.py")
text = p.read_text()

old = '''                "teachers gain order", "students absorb delay", "students absorb sanctions"
            ]),'''

new = '''                "teachers gain order", "students absorb delay", "students absorb sanctions",
                "ordinary users are filtered", "flagged users face extra review",
                "platform operators benefit", "users absorb wrongful removal",
                "creators lose reach", "high-risk content is escalated", "ordinary posts are suppressed",
                "engagement is preserved for the platform", "moderators absorb overload",
                "drivers wait for matches", "riders get faster pickups",
                "surge-priced riders get priority", "drivers absorb idle time",
                "drivers bear fuel cost", "platform takes commission",
                "high-demand zones get priority", "remote riders wait longer",
                "drivers in low-demand areas wait", "customers pay surge fees",
                "platform prioritizes dense routes", "drivers absorb cancellation risk"
            ]),'''

if old not in text:
    raise SystemExit("asymmetry tail block not found")

text = text.replace(old, new, 1)
p.write_text(text)
print("patched", p)
