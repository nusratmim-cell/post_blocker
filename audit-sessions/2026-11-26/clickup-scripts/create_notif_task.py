import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Summary
[Profile / Notification] The "নোটিফিকেশন" (Notification) row in the Profile menu is **dead** — tapping it bounces back to Home instead of opening any notifications screen. **Disable/remove this row for now**, since it has no working destination.

### Impact & Severity
* **Severity:** P3 – Minor (audit S3). *(ClickUp priority set to High; lower to Normal if preferred.)*
* **User Impact:** Any user who opens Profile and taps "নোটিফিকেশন" (সর্বশেষ আপডেট দেখো / "see latest updates") is dropped back to Home with no screen and no feedback. "Settings" in the same sheet works, so the row reads as plainly broken.
* **Frequency:** 100% reproducible (reproduced 4× in the audit).

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android (prod build `tech.shikho.android`, build 6.0.13 observed on device)
* **Account / Test State:** Any logged-in user (the Profile menu row is shown to all); observed on account nus (paid, Class 7).

### Steps to Reproduce
1. On Home, tap the profile avatar (top-right) to open the Profile menu.
2. Tap the first row: **"নোটিফিকেশন"** (subtitle "সর্বশেষ আপডেট দেখো").
3. The sheet closes and returns to **Home** — no notifications screen opens (repeat taps behave the same).

### Expected vs. Actual Behavior
* **Expected (this change):** The "Notification" row is removed/hidden from the Profile menu (it has no working destination), so there is no dead entry.
* **Actual:** The row is present but navigates nowhere — it bounces straight back to Home.

### Evidence & Mechanism (tech spec + codemap)
* **Visuals:** Attached (`ev_notif.jpg`).
* The in-app notification surface is the **Inbox / One-Way Messages** (`ui/feature/compose/inbox/` — `InboxFragment` / `InboxScreen`, `GetOneWayMessages`). The code still exists but is **orphaned**:
  * Its real entry point — the bottom-nav **Inbox tab** — was removed **end-to-end in ST-29661** (commit `a41742eb3e`); Explore replaced it (dashboard SPEC; codemap `Nav3Host.kt:331-339`).
  * Even before removal the tab was `visible="false"` by default, with **no code path to make it visible** (notifications SPEC — flagged High-risk).
  * The leftover **Profile "Notification" row** (`ProfileActionHandler`) still targets the removed Inbox route, so the navigation no-ops and returns to Home — exactly this bug.
  * Backend: one-way messages (`notification_type: "OneWayMessage"`) are now web-portal-only; there is no surviving Android surface.
* **Do NOT touch push notifications** — FCM/CleverTap system-tray notifications and their deep links are a separate, working system (`FirebaseMessagingService`, `FcmServiceHelper`). Only the dead in-app Inbox/Notification menu entry is affected.

### How to Disable (dev notes)
* Remove/hide the **"Notification" row** from the Profile menu (its item in `ProfileScreen` / `ProfileActionHandler` `clickActions["notification"]`) so it no longer appears, since the Inbox destination it points to was removed in ST-29661.
* Leave the rest of the Profile menu (Settings, Profile Edit, Subscription, etc.) and all push notifications untouched.
* Keep it reversible — re-add the entry when a working notification center / inbox is reintroduced.

### Acceptance Criteria (Definition of Done)
* [ ] The "নোটিফিকেশন" row no longer appears in the Profile menu for any user type (or, if kept, it opens a working notifications screen — never a bounce to Home).
* [ ] No regression to the rest of the Profile menu — Settings, Profile Edit, Syllabus Change, Subscription, etc. still work.
* [ ] Push notifications (system-tray + deep links) are unaffected.
* [ ] Change is reversible — the entry can be restored when an in-app notification center is rebuilt.
"""

payload = {
    "name": "[PROD][APP][Profile/Notification]: Disable the dead 'Notification' menu row (bounces to Home, Inbox removed in ST-29661)",
    "markdown_content": body,
    "priority": 2,
    "tags": ["sprint 10"],
}
req = urllib.request.Request(
    f"https://api.clickup.com/api/v2/list/{LIST_ID}/task",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": TOKEN, "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    print("OK", d.get("id"), d.get("url"), "prio", (d.get("priority") or {}).get("priority"), "tags", [t.get("name") for t in d.get("tags", [])])
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode())
