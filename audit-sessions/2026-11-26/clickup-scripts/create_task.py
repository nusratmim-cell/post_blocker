import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Summary
`[Home / Yearly-Result Certificate]` The **"সার্টিফিকেট দেখো এখনই!"** (half-yearly result certificate) card renders on the Home screen even when the half-yearly result-collection flag is **OFF**.

### Impact & Severity
* **Severity:** P1 – Critical  *(ClickUp priority set to Urgent / Highest per request)*
* **User Impact:** Every SSC-track student (Class 5–10) across **Free, Trial and Paid** cohorts sees a prominent, top-of-Home card — *"See your certificate now · tap here to download or share"* — when no half-yearly result/certificate exists for them (flag off). It is a false, non-dismissible promise sitting in the #1 Home slot; tapping it leads into an empty/partial yearly-result flow. No user workaround.
* **Frequency:** 100% reproducible on a fresh Class-7 (SSC '30) registration with the half-yearly flag off.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android 12, POCO X3
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12 — report-card / dashboard). Exact build number not captured on device — please confirm from the test device.
* **Account / Test State:** Freshly registered **Class 7 · SSC '30 · National Ideal School** (profile "test Rakesh QA"). `resultCollectionExamType = half_yearly`; result-collection flag (`yearlyResultCollectionEnabled` / `enable_final_year_result_collection`) = **OFF**.

### Steps to Reproduce
1. Complete a fresh registration into a Class 5–10 (SSC-track) batch — reproduced on **Class 7, SSC '30**.
2. Ensure the half-yearly result-collection flag is **OFF** for that batch (no half-yearly result published; `yearlyResultCollectionEnabled` = false).
3. Open the app and land on the **Home (হোম)** tab.
4. Observe the top card: **"সার্টিফিকেট দেখো এখনই! / ডাউনলোড বা শেয়ার করতে এখানে ক্লিক করো"**.

### Expected vs. Actual Behavior
* **Expected:** When the half-yearly result-collection flag is OFF (or no certificate/result is available for the student's batch), the certificate card is **hidden**. The card appears only when the flag is ON **and** the student has a valid half-yearly result/certificate.
* **Actual:** The card is shown on Home **regardless of the flag being OFF**, for Class 5–10 students (Free / Trial / Paid). It occupies the top Home slot and invites download/share of a certificate that does not exist.

### Evidence & Diagnostics
* **Visuals:** Home screenshot — Class 7 · SSC '30 · National Ideal School, certificate card visible at top (**attached to this task**).
* **Code / flag references (shikho-android spec — report-card & dashboard features):**
  * Card visibility gate: `AppPreference.yearlyResultCollectionEnabled` **&&** `isValidBatchForYearlyResult()` — rendered from `PaidUserScreen.kt`, `TrialUserScreen.kt`, `FreeUserScreen.kt`; click event `AcademicProgramEvent.OnYearlyResultCardClicked`.
  * Exam-type flag: `AppPreference.resultCollectionExamType` (`half_yearly` / `pre_test` / yearly) — half-yearly variant added under **SC-723**.
  * Class gate (sibling dialog `SHOW_YEARLY_RESULT_BOTTOM_SHEET`): `enable_final_year_result_collection` + **class 5–10** (dashboard SPEC §5.5 dialog priority queue).
* **Likely cause:** The card render path evaluates `isValidBatchForYearlyResult()` (batch/class validity) but does **not** correctly honour the OFF state of `yearlyResultCollectionEnabled` / `resultCollectionExamType = half_yearly`. The flag value from the splash API is not gating the card for the half-yearly variant.
* **Regression Check:** Half-yearly exam type was introduced under **SC-723** (report-card SPEC, v6.0.3 → v6.0.12 window). The flag-off gating for the half-yearly variant is the regression surface — verify against the SC-723 change set.

### Impacted Classes (investigation result)
* **Directly reproduced:** Class 7 (SSC '30).
* **Impacted range:** **Class 5–10** — the valid-batch range for yearly/half-yearly result collection (same range that gates `SHOW_YEARLY_RESULT_BOTTOM_SHEET`). The card is hosted on all three home screens, so **Free, Trial and Paid** cohorts are affected.
* **Not impacted:** Classes 1–4 (outside the result-collection batch range) and HSC / Class 11–12 (separate HSC-feedback flow, `SHOW_HSC_FEEDBACK_BOTTOM_SHEET`).

### Acceptance Criteria (Definition of Done)
* [ ] With the half-yearly flag **OFF**, the certificate card is **not** shown on Home for any Class 5–10 student across Free, Trial, and Paid cohorts.
* [ ] With the flag **ON** and a valid half-yearly result/certificate present, the card **is** shown and the tap opens the correct certificate/result flow.
* [ ] Card visibility is driven by `yearlyResultCollectionEnabled` (+ `resultCollectionExamType`) **and** a valid certificate/result — not by batch/class validity alone.
* [ ] Verified on the Class 7 (SSC '30) repro above **plus** one other class in the 5–10 range, on a PROD-config build.
* [ ] No regression to the yearly and pre-test result-collection card variants.
"""

payload = {
    "name": "[PROD][APP][Half yearly Result Certificate]: Half Yearly certificate card is appearing in Homepage when half yearly flag is off",
    "markdown_content": body,
    "priority": 1,
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
    print("OK")
    print("TASK_ID", d.get("id"))
    print("URL", d.get("url"))
    print("PRIORITY", (d.get("priority") or {}))
    print("TAGS", [t.get("name") for t in d.get("tags", [])])
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode())
