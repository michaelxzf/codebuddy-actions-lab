"""Turn CodeBuddy's structured findings into GitHub workflow annotations + a job summary."""
import json
import os
import sys

events = json.load(open(sys.argv[1]))
res = next(e for e in reversed(events) if e.get("type") == "result")
data = res["structured_output"]
def esc(s):
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
for f in data["findings"]:
    print(f"::{f['severity']} file={f['file'].lstrip('./')},line={f['line']},title={esc(f['title'])}::{esc(f['detail'])}")
with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as s:
    s.write(f"## 🤖 CodeBuddy annotations\n\n{data['summary']}\n\n| Severity | Location | Finding |\n|---|---|---|\n")
    for f in data["findings"]:
        s.write(f"| {f['severity']} | `{f['file']}:{f['line']}` | {f['title']} |\n")
    s.write(f"\n<sub>{res.get('num_turns')} turns · {round(res.get('duration_ms', 0) / 1000)} s</sub>\n")
sys.exit(1 if any(f["severity"] == "error" for f in data["findings"]) else 0)
