import json
import subprocess
import sys

URL = "http://127.0.0.1:8002/chat"

def post(payload):
    cmd = [
        "curl", "-s", "-X", "POST", URL,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
    ]
    raw = subprocess.check_output(cmd, text=True)
    return json.loads(raw)

tests = [
    ("PROJECT_ATTRIBUTION", {"message": "who invented Energetic Paradigm"}),
    ("WORLD_ATTRIBUTION", {"message": "who invented printer"}),
    ("WORLD_FACT", {"message": "who is max weber"}),
    ("HOW_TO", {"message": "how to make egg fried rice?"}),
    ("SYSTEM_ANALYSIS", {"message": "Analyze the airport security screening system with Energetic Paradigm."}),
    ("FORECAST_THESIS", {"message": "when will the US war against Iran end?"}),
]

failures = []

for expected, payload in tests:
    data = post(payload)
    mode = data.get("metadata", {}).get("mode") or data.get("metadata", {}).get("routing", {}).get("task_type")
    status = data.get("validity_status")
    print("=" * 80)
    print(payload["message"])
    print("EXPECTED:", expected)
    print("GOT:", mode)
    print("STATUS:", status)
    acceptable = {expected}
    if expected == "PROJECT_ATTRIBUTION":
        acceptable.add("ATTRIBUTION")

    if mode not in acceptable:
        failures.append((payload["message"], expected, mode))
    if status != "Valid EP":
        failures.append((payload["message"], "Valid EP", status))

# Memory test
r1 = post({"message": "when will the US war against Iran end?"})
sid = r1["metadata"]["session"]["session_id"]

r2 = post({
    "session_id": sid,
    "message": "it is too long. just one sentence"
})
mode2 = r2.get("metadata", {}).get("mode")
answer2 = r2.get("analysis", "")
print("=" * 80)
print("MEMORY FOLLOW-UP")
print("SESSION:", sid)
print("GOT:", mode2)
print("ANSWER:", answer2)

if mode2 != "FOLLOW_UP_REWRITE":
    failures.append(("memory follow-up", "FOLLOW_UP_REWRITE", mode2))

if len(answer2.split(".")) > 3:
    failures.append(("memory follow-up length", "roughly one sentence", answer2))

print("=" * 80)
if failures:
    print("FAILED")
    for f in failures:
        print(f)
    sys.exit(1)

print("V4 FINAL VALIDATION PASSED")
