import json
import subprocess
import sys

URL = "http://127.0.0.1:8004/chat"

tests = [
    ("FACT", "what is canonical in religion?"),
    ("HOW_TO", "how to make egg fried rice?"),
    ("EP_ANALYSIS", "Analyze the airport security screening system with Energetic Paradigm."),
    ("LIVE_SOURCE_REQUIRED", "when the US war against Iran will end?"),
]

failures = []

def post(message, session_id=None):
    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id
    raw = subprocess.check_output([
        "curl", "-s", "-X", "POST", URL,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
    ], text=True)
    return json.loads(raw)

for expected, msg in tests:
    data = post(msg)
    routing = data.get("metadata", {}).get("routing", {})
    got = routing.get("control_class")
    mode = data.get("metadata", {}).get("mode")
    print("=" * 80)
    print(msg)
    print("MODE:", mode)
    print("EXPECTED CONTROL:", expected)
    print("GOT CONTROL:", got)
    if got != expected:
        failures.append((msg, expected, got))

# Follow-up memory test
r1 = post("what is canonical in religion?")
sid = r1["metadata"]["session"]["session_id"]
r2 = post("then, what does it mean in computer science?", sid)
routing2 = r2.get("metadata", {}).get("routing", {})
got2 = routing2.get("control_class")
answer2 = r2.get("analysis", "")

print("=" * 80)
print("FOLLOW-UP TEST")
print("GOT CONTROL:", got2)
print("ANSWER:", answer2)

if got2 != "FOLLOW_UP":
    failures.append(("follow-up", "FOLLOW_UP", got2))
if "computer science" not in answer2.lower():
    failures.append(("follow-up answer", "computer science answer", answer2))

print("=" * 80)
if failures:
    print("FAILED")
    for f in failures:
        print(f)
    sys.exit(1)

print("V6 CONTROL SHELL VALIDATION PASSED")
