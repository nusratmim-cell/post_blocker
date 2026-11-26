import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
TASK_ID = "z8zyy1ujwy"

body = """### Summary
`[Home / Yearly-Result Certificate]` The **"সার্টিফিকেট দেখো এখনই!"** (half-yearly result certificate) card renders on the Home screen even when the half-yearly result-collection flag is **OFF**.

### Impact & Severity
* **Severity:** P1 – Critical  *(ClickUp priority set to Urgent / Highest per request)*
* **User Impact:** A prominent, top-of-Home card — *"See your certificate now · tap here to download or share"* — is shown when no half-yearly result/certificate exists for the student (flag off). It is a false, non-dismissible promise in the #1 Home slot; tapping it leads into an empty/partial yearly-result flow. No user workaround. The card is wired on all three home screens (`FreeUserScreen`, `TrialUserScreen`, `PaidUserScreen`), so Free, Trial and Paid cohorts can all hit it. **Exact affected class range is still to be confirmed on-device — see "Impacted Classes" below; do not assume a range before verifying.**
* **Frequency:** 100% reproducible on a fresh Class-7 (SSC '30) registration with the half-yearly flag off.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android 12, POCO X3
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12 — report-card / dashboard). Exact build number not captured on device — please confirm from the test device.
* **Account / Test State:** Freshly registered **Class 7 · SSC '30 · National Ideal School** (profile "test Rakesh QA"). `resultCollectionExamType = half_yearly`; result-collection flag (`yearlyResultCollectionEnabled` / `enable_final_year_result_collection`) = **OFF**.

### Steps to Reproduce
1. Complete a fresh registration — reproduced on **Class 7, SSC '30**.
2. Ensure the half-yearly result-collection flag is **OFF** for that batch (no half-yearly result published; `yearlyResultCollectionEnabled` = false).
3. Open the app and land on the **Home (হোম)** tab.
4. Observe the top card: **"সার্টিফিকেট দেখো এখনই! / ডাউনলোড বা শেয়ার করতে এখানে ক্লিক করো"**.

### Expected vs. Actual Behavior
* **Expected:** When the half-yearly result-collection flag is OFF (or no certificate/result is available for the student's batch), the certificate card is **hidden**. The card appears only when the flag is ON **and** the student has a valid half-yearly result/certificate.
* **Actual:** The card is shown on Home **regardless of the flag being OFF** (verified on Class 7, SSC '30). It occupies the top Home slot and invites download/share of a certificate that does not exist.

### Evidence & Diagnostics
* **Visuals:** Home screenshot — Class 7 · SSC '30 · National Ideal School, certificate card visible at top (**attached to this task**).
* **Code / flag references (shikho-android spec — report-card & dashboard features):**
  * Card visibility gate: `AppPreference.yearlyResultCollectionEnabled` **&&** `isValidBatchForYearlyResult()` — rendered from `PaidUserScreen.kt`, `TrialUserScreen.kt`, `FreeUserScreen.kt`; click event `AcademicProgramEvent.OnYearlyResultCardClicked`.
  * Exam-type flag: `AppPreference.resultCollectionExamType` (`half_yearly` / `pre_test` / yearly) — half-yearly variant added under **SC-723**.
  * Related dialog gate (NOT the card): the sibling `SHOW_YEARLY_RESULT_BOTTOM_SHEET` bottom sheet is gated on `enable_final_year_result_collection` + **class 5–10** (dashboard SPEC §5.5). This is a *different* gate from the card and is cited only as a reference point.
* **Likely cause:** The card render path evaluates `isValidBatchForYearlyResult()` (batch/class validity) but does **not** correctly honour the OFF state of `yearlyResultCollectionEnabled` / `resultCollectionExamType`. The flag value from the splash API is not gating the card for the half-yearly variant.
* **Regression Check:** Half-yearly / pre-test exam types were introduced under **SC-723** (report-card SPEC, v6.0.3 → v6.0.12 window). The flag-off gating for the half-yearly variant is the regression surface — verify against the SC-723 change set.

### Impacted Classes (investigation — partially verified)
* **Confirmed impacted:** Class 7 (SSC '30) — directly reproduced in the attached screenshot.
* **Range NOT yet confirmed.** The card's gate `isValidBatchForYearlyResult()` is referenced by name in the spec but its exact class/batch range is **not documented**, so the full impacted range cannot be stated from spec alone.
  * The sibling yearly-result **bottom sheet** is gated on class 5–10 — a plausible lower-bound reference, but it is a different gate.
  * Because the card now also serves `resultCollectionExamType = pre_test` / `half_yearly` (SC-723), and "pre-test" is an HSC/SSC pre-board exam type, **HSC (Class 11–12) may also be affected and must not be assumed safe.**
* **Action for dev/QA:** Verify on-device with the flag OFF across **Class 5–10 and HSC (Class 11–12)**, on Free, Trial and Paid accounts, and confirm the true range from `isValidBatchForYearlyResult()` in code. Update this ticket with the confirmed range.

### Acceptance Criteria (Definition of Done)
* [ ] The exact affected class/batch range is confirmed from `isValidBatchForYearlyResult()` and recorded on this ticket (explicitly state whether HSC 11–12 is in scope).
* [ ] With the half-yearly flag **OFF**, the certificate card is **not** shown on Home for any affected class across Free, Trial, and Paid cohorts.
* [ ] With the flag **ON** and a valid half-yearly result/certificate present, the card **is** shown and the tap opens the correct certificate/result flow.
* [ ] Card visibility is driven by `yearlyResultCollectionEnabled` (+ `resultCollectionExamType`) **and** a valid certificate/result — not by batch/class validity alone.
* [ ] Verified on the Class 7 (SSC '30) repro above **plus** at least one other class and one HSC account, on a PROD-config build.
* [ ] No regression to the yearly and pre-test result-collection card variants.
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
