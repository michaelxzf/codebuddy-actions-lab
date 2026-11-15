"""Post CodeBuddy's acceptance-criteria verdict to the PR (gh) and to the Jira issue."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import jira  # noqa: E402

key, events = sys.argv[1], json.load(open(sys.argv[2]))
res = next(e for e in reversed(events) if e.get("type") == "result")
d = res["structured_output"]
icon = {"meets": "✅ Meets", "partially_meets": "🟠 Partially meets", "does_not_meet": "⛔ Does not meet"}[d["verdict"]]
met = sum(c["met"] for c in d["criteria"])
url = f"{os.environ['JIRA_BASE_URL']}/browse/{key}"
md = [f"## 🤖 CodeBuddy · Jira [{key}]({url}) acceptance check — {icon} ({met}/{len(d['criteria'])})", "", d["summary"], "",
      "| Acceptance criterion | Met | Evidence |", "|---|---|---|"]
md += [f"| {c['criterion']} | {'✅' if c['met'] else '❌'} | {c['evidence']} |" for c in d["criteria"]]
subprocess.run(["gh", "pr", "comment", os.environ["PR"], "--body", "\n".join(md)], check=True)
pr_url = f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/pull/{os.environ['PR']}"
jira.comment(key, f"CodeBuddy acceptance check for PR #{os.environ['PR']}: {icon} ({met}/{len(d['criteria'])})",
             [[c["criterion"], "yes" if c["met"] else "NO", c["evidence"]] for c in d["criteria"]], f"{d['summary']} · {pr_url}")
jira.transition(key, "In Progress")
print(f"posted to PR #{os.environ['PR']} and {key}: {d['verdict']} {met}/{len(d['criteria'])}")
