import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Summary
[Home / Hero] The "প্রিমিয়াম" (Premium) badge — crown + label — is shown from an `isPremium` flag that is true for *any* non-free user (trial or ever-purchased), not *current active paid* status. So **trial users** and **lapsed/expired buyers now back in free/trial** both wrongly wear the Premium badge.

### Impact & Severity
* **Severity:** P2 – Major (audit S3). *(ClickUp priority set to High — bump to Urgent if you want it in the same lane as the others.)*
* **User Impact:**
  * **Trial (non-paying) users** see the Premium crown/badge → blurs trial vs paid and dilutes the real upgrade.
  * **Users whose purchase has expired** and who are now in the free/trial section **still** see the Premium badge → misleading; it implies an active entitlement they no longer have.
* **Frequency:** 100% for the affected states (active trial; expired/lapsed buyer).

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android (prod build `tech.shikho.android`)
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12)
* **Account / Test State:** (A) an active trial account; (B) an account that purchased a course which has since **expired** (no active paid enrollment), now shown in the free/trial section.

### Steps to Reproduce
**Case A — Trial user:**
1. Activate a trial.
2. Open Home.
3. The hero shows the "প্রিমিয়াম" crown badge.

**Case B — Expired / lapsed buyer:**
1. Use an account that purchased a course that has since expired (no active paid access), now in the free/trial section.
2. Open Home.
3. The hero still shows the "প্রিমিয়াম" crown badge.

### Expected vs. Actual Behavior
* **Expected:** The Premium badge (crown + "প্রিমিয়াম") shows **only** for users with a current, active, non-expired **PAID** enrollment. Trial users and lapsed/expired buyers do **not** see it.
* **Actual:** The badge shows for trial users and for expired/lapsed buyers — it tracks "has an enrollment / ever purchased," not current paid status.

### Evidence & Mechanism
* **Visuals:** Attached — trial account showing Premium badge; lapsed/expired state.
* **UI component:** `GreetingRow.kt` (homev2 hero) renders `PremiumTag` ("Crown icon + 'প্রিমিয়াম' label badge") and a premium **crown overlay** on `UserAvatar`; both driven by the `isPremium` boolean parameter (14_COMPONENT_MAP). `GreetingRow` is invoked at `HomeV2Screen.kt:491-498`.
* **Root cause:** `isPremium` currently resolves true for **trial AND paid** students. Codemap: FocusHub is gated on `isPremium` (`HomeV2Screen.kt:311-312`) and *"only runs for trial and paid students."* The flag does not require active, non-expired paid access, so trial users and expired buyers evaluate as premium.
* **Already-available signal to reuse:** `shouldSuppressFocusHub` (`HomeV2Screen.kt:316-320`) already detects *"an expired trial, an expired paid subscription or an overdue installment"* and removes the hero card + streak pill — but it does **not** gate the Premium badge, so the badge persists for expired users. The same active/expired signal should gate `PremiumTag` + the avatar crown.

### How to Fix (dev notes)
* Compute the badge's `isPremium` from **current active paid access only**: require an active, non-expired **Paid** enrollment (e.g. `accessLevel == Full` AND not `isExpired` AND enrollment type Paid — not trial). Exclude trial users, expired/lapsed paid, and overdue/ReadOnly.
* Apply the same gate to **both** `PremiumTag` (label) and the `UserAvatar` **crown overlay** in `GreetingRow.kt` so they stay consistent.
* Reuse the expired/overdue detection already used by `shouldSuppressFocusHub` so the badge, FocusHub card and streak pill agree.

### Acceptance Criteria (Definition of Done)
* [ ] The Premium badge (crown + "প্রিমিয়াম") and the avatar crown overlay show **only** for users with a current, active, non-expired paid enrollment.
* [ ] **Trial** users do NOT see the Premium badge.
* [ ] Users with an **expired/lapsed purchase** (now in free/trial, no active paid access) do NOT see the Premium badge.
* [ ] Active paid users **still** see it (no regression).
* [ ] Both the `PremiumTag` label and the avatar crown overlay are gated by the same rule.
"""

payload = {
    "name": "[PROD][APP][Home/Hero]: 'Premium' badge shown to trial users and expired/lapsed buyers — gate it to current active paid only",
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
