#!/usr/bin/env python3
"""
End-to-end API test script for the FDI system.
- Registers users (level 1 active, level 2 pending)
- Lists pending users
- Approves a pending user
- Changes user level
- Publishes content (to levels/users)
- Fetches history for a user
- Re-sends notification (simulated)
- Deletes a user

Usage:
    source .venv/bin/activate
    python scripts/test_api.py

Environment:
    API_BASE (default: http://127.0.0.1:8000)
"""
import os
import sys
import json
import time
import httpx

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
API = f"{API_BASE}/api"

client = httpx.Client(timeout=10.0)

def p(title: str, data):
    print(f"\n=== {title} ===")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2))
    else:
        print(data)

def post(path, payload):
    r = client.post(f"{API}{path}", json=payload)
    r.raise_for_status()
    return r.json()

def get(path):
    r = client.get(f"{API}{path}")
    r.raise_for_status()
    return r.json()

def delete(path):
    r = client.delete(f"{API}{path}")
    r.raise_for_status()
    return r.json()

def main():
    # Health
    r = get("/health")
    p("Health", r)

    # Register users
    u1 = post("/users/register_user", {
        "telegram_id": 111,
        "first_name": "Mario",
        "last_name": "Rossi",
        "level": 1
    })
    p("Register L1 (active)", u1)

    u2 = post("/users/register_user", {
        "telegram_id": 222,
        "first_name": "Giulia",
        "last_name": "Bianchi",
        "level": 2
    })
    p("Register L2 (pending)", u2)

    # List pending
    pending = get("/users?status=pending")
    p("List pending", pending)

    # Approve Giulia
    if pending:
        giulia_id = u2["id"]
        ok = post("/users/approve_user", {"user_id": giulia_id, "approve": True})
        p("Approve user 2", ok)

    # Change level for Mario to 2
    ch = post(f"/users/change_level?user_id={u1['id']}&level=2", {})
    p("Change level for user 1 to 2", ch)

    # Publish content to level 2 and user 1
    pub = post("/contents/publish_content", {
        "title": "Assemblea Territoriale",
        "body": "Incontro il 10/10 ore 18",
        "link": "https://example.com",
        "targets": {
            "all_levels": False,
            "levels": [2],
            "user_ids": [u1["id"]]
        }
    })
    p("Publish content to L2 and user 1", pub)

    # History for telegram_id 111 (Mario)
    hist1 = get("/contents/history/111")
    p("History for telegram_id 111", hist1)

    # Re-send notification (simulated)
    if pub and "content_id" in pub:
        rn = post("/contents/send_notification", {
            "content_id": pub["content_id"],
            "user_ids": [u1["id"], u2["id"]]
        })
        p("Resend notification (simulated)", rn)

    # Delete Giulia
    d = delete(f"/users/{u2['id']}")
    p("Delete user 2", d)

    # List all users
    all_users = get("/users")
    p("List all users", all_users)

if __name__ == "__main__":
    try:
        main()
    except httpx.HTTPStatusError as e:
        print("HTTP error:", e)
        if e.response is not None:
            print("Response:", e.response.text)
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
