"""Minimal Jira Cloud REST client for CI (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN from secrets/vars)."""
import base64
import json
import os
import sys
import urllib.request

BASE = os.environ["JIRA_BASE_URL"].rstrip("/")
AUTH = base64.b64encode(f"{os.environ['JIRA_EMAIL']}:{os.environ['JIRA_API_TOKEN']}".encode()).decode()


def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Basic " + AUTH, "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req) as r:
        t = r.read()
        return json.loads(t) if t else None


def adf_text(node):
    """Flatten Atlassian Document Format to plain text (headings and bullets kept)."""
    if node is None:
        return ""
    if node.get("type") == "text":
        return node.get("text", "")
    inner = "".join(adf_text(c) for c in node.get("content", []))
    if node.get("type") in ("paragraph", "heading"):
        return inner + "\n"
    if node.get("type") == "listItem":
        return "- " + inner
    return inner


def get_issue_markdown(key):
    f = call("GET", f"/rest/api/3/issue/{key}?fields=summary,description,status,issuetype")["fields"]
    return f"# {key}: {f['summary']}\nType: {f['issuetype']['name']} · Status: {f['status']['name']}\n\n{adf_text(f['description'])}"


def comment(key, title, rows, footer):
    table = {"type": "table", "attrs": {"layout": "default"}, "content": [
        {"type": "tableRow", "content": [{"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": h, "marks": [{"type": "strong"}]}]}]} for h in ("Acceptance criterion", "Met", "Evidence")]}
    ] + [{"type": "tableRow", "content": [{"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": c}]}]} for c in r]} for r in rows]}
    body = {"type": "doc", "version": 1, "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": title, "marks": [{"type": "strong"}]}]}, table,
        {"type": "paragraph", "content": [{"type": "text", "text": footer}]}]}
    call("POST", f"/rest/api/3/issue/{key}/comment", {"body": body})


def transition(key, to):
    ts = call("GET", f"/rest/api/3/issue/{key}/transitions")["transitions"]
    t = next((t for t in ts if t["to"]["name"].lower() == to.lower()), None)
    if t:
        call("POST", f"/rest/api/3/issue/{key}/transitions", {"transition": {"id": t["id"]}})


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "issue":
        print(get_issue_markdown(sys.argv[2]))
    elif cmd == "transition":
        transition(sys.argv[2], sys.argv[3])
