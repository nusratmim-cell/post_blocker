import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
TASK_ID = "z8zyy1ujwy"

body = """### Summary
[Home / Yearly-Result Certificate] The "সার্টিফিকেট দেখো এখনই!" (half-yearly result certificate) card appears on the Home screen even when the half-yearly result-collection flag is OFF.

### Impact & Severity
* **Severity:** P1 – Critical (Urgent)
* **User Impact:** A prominent, non-dismissible card ("See your certificate now · tap here to download or share") occupies the #1 Home slot even when no result exists. Tapping it leads students into an empty/broken flow with no workaround. Affects Free, Trial, and Paid users across school batches (Class 5–10).
* **Frequency:** 100% reproducible on a fresh Class 7 (SSC '30) registration with the half-yearly flag off.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android 12, POCO X3
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12)
* **Account / Test State:** Freshly registered Class 7 · SSC '30 · National Ideal School (test profile: `"test Rakesh QA"`). Exam type is `half_yearly` with the result-collection flag set to **OFF**.

### Steps to Reproduce
1. Complete a fresh registration into a school batch (Class 5–10) — reproduced on Class 7, SSC '30.
2. Confirm the half-yearly result-collection flag is OFF for that batch (no half-yearly result published).
3. Open the app and land on the **Home (হোম)** tab.
4. Observe the top card: *"সার্টিফিকেট দেখো এখনই! / ডাউনলোড বা শেয়ার করতে এখানে ক্লিক করো"*.

### Expected vs. Actual Behavior
* **Expected:** When the half-yearly result-collection flag is OFF (or no valid result/certificate exists for the student's batch), the certificate card is hidden.
* **Actual:** The card renders in the top Home slot regardless of the flag being OFF, prompting students to download/share a non-existent certificate.

### Evidence & Scope Notes
* **Visuals:** Home screen screenshot attached (showing the card visible at the top for Class 7 · SSC '30).
* **Regression Context:** Half-yearly and pre-test variants were introduced in **SC-723**. Please verify that flag-off gating works across all affected cohorts:
  * **In Scope:** Classes 5–9 (`half_yearly` branding) and Class 10 (`pre_test` branding) across Free, Trial, and Paid users.
  * **Out of Scope / Negative Check:** HSC (Class 11–12) does not have half-yearly exams and should remain unaffected.

### Acceptance Criteria (Definition of Done)
* [ ] With the half-yearly flag OFF, the certificate card is hidden on Home for all school batches (Class 5–10) across Free, Trial, and Paid cohorts.
* [ ] With the flag ON and a valid result/certificate available, the card displays properly and opens the correct certificate flow.
* [ ] Verified on Class 7 (`half_yearly` variant) and Class 10 (`pre_test` variant).
* [ ] Confirmed HSC (Class 11–12) still does not surface this card, and existing yearly result flows have no regressions.
"""

payload = {"markdown_content": body}
req = urllib.request.Request(
    f"https://api.clickup.com/api/v2/task/{TASK_ID}",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": TOKEN, "Content-Type": "application/json"},
    method="PUT",
)
try:
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    print("UPDATED", d.get("id"), d.get("url"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode())
