import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
TASK_ID = "z8zyy1ujwy"

body = """### Summary
`[Home / Yearly-Result Certificate]` The **"সার্টিফিকেট দেখো এখনই!"** (half-yearly result certificate) card renders on the Home screen even when the half-yearly result-collection flag is **OFF**.

### Impact & Severity
* **Severity:** P1 – Critical  *(ClickUp priority set to Urgent / Highest per request)*
* **User Impact:** A prominent, top-of-Home card — *"See your certificate now · tap here to download or share"* — is shown when no half-yearly result/certificate exists for the student (flag off). It is a false, non-dismissible promise in the #1 Home slot; tapping it leads into an empty/partial yearly-result flow. No user workaround. The card is wired on all three home screens (`FreeUserScreen`, `TrialUserScreen`, `PaidUserScreen`), so Free, Trial and Paid cohorts of the affected **school batches (Class 5–10)** can all hit it.
* **Frequency:** 100% reproducible on a fresh Class-7 (SSC '30) registration with the half-yearly flag off.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android 12, POCO X3
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12 — report-card / dashboard). Exact build number not captured on device — please confirm from the test device.
* **Account / Test State:** Freshly registered **Class 7 · SSC '30 · National Ideal School** (profile "test Rakesh QA"). `resultCollectionExamType = half_yearly`; result-collection flag (`yearlyResultCollectionEnabled` / `enable_final_year_result_collection`) = **OFF**.

### Steps to Reproduce
1. Complete a fresh registration into a school batch (Class 5–10) — reproduced on **Class 7, SSC '30**.
2. Ensure the half-yearly result-collection flag is **OFF** for that batch (no half-yearly result published; `yearlyResultCollectionEnabled` = false).
3. Open the app and land on the **Home (হোম)** tab.
4. Observe the top card: **"সার্টিফিকেট দেখো এখনই! / ডাউনলোড বা শেয়ার করতে এখানে ক্লিক করো"**.

### Expected vs. Actual Behavior
* **Expected:** When the half-yearly result-collection flag is OFF (or no certificate/result is available for the student's batch), the certificate card is **hidden**. The card appears only when the flag is ON **and** the student has a valid result/certificate.
* **Actual:** The card is shown on Home **regardless of the flag being OFF** (verified on Class 7, SSC '30). It occupies the top Home slot and invites download/share of a certificate that does not exist.

### Evidence & Diagnostics
* **Visuals:** Home screenshot — Class 7 · SSC '30 · National Ideal School, certificate card visible at top (**attached to this task**).
* **Code / flag references (shikho-android spec — report-card & dashboard features):**
  * Card visibility gate: `AppPreference.yearlyResultCollectionEnabled` **&&** `isValidBatchForYearlyResult()` — rendered from `PaidUserScreen.kt`, `TrialUserScreen.kt`, `FreeUserScreen.kt`; click event `AcademicProgramEvent.OnYearlyResultCardClicked`.
  * Exam-type flag: `AppPreference.resultCollectionExamType` (`half_yearly` / `pre_test` / yearly) — half-yearly variant added under **SC-723**.
* **Likely cause:** The card render path evaluates `isValidBatchForYearlyResult()` (batch/class validity) but does **not** correctly honour the OFF state of `yearlyResultCollectionEnabled` / `resultCollectionExamType`. The flag value from the splash API is not gating the card.
* **Regression Check:** Half-yearly / pre-test exam types were introduced under **SC-723** (report-card SPEC, v6.0.3 → v6.0.12 window). The flag-off gating for the half-yearly variant is the regression surface — verify against the SC-723 change set.

### Impacted Classes (scoped from code + certificate cron)
* **Confirmed impacted:** Class 7 (SSC '30), half-yearly variant — reproduced in the attached screenshot.
* **In scope — school result-collection batches, Class 5–10:**
  * Classes 5–9 → `half_yearly` branded card (the reported case).
  * Class 10 → same card but **pre-test** branded (`resultCollectionExamType = pre_test`). Evidence: cert cron special-cases class code `"C10"` for pre-test copy — `notification/cmd/scheduler.finalYearResultCertificate.go:44`; *"half yearly for Class 10 gets pre-test branding, half yearly for every other batch gets half-yearly branding."*
  * (Class range aligns with the sibling `SHOW_YEARLY_RESULT_BOTTOM_SHEET` gate: class 5–10, dashboard SPEC §5.5.)
* **NOT impacted — HSC (Class 11–12):** HSC has no half-yearly exam, so these batches never get `resultCollectionExamType = half_yearly` and do not surface this card. Evidence: enrollment CRM tags class as `SSC-` for C9/C10 vs `HSC-` for C11/C12 — HSC is a separate track; the half-yearly/pre-test certificate cron path is school-batch only. (HSC's own prompt is `SHOW_HSC_FEEDBACK_BOTTOM_SHEET`.)
* **Confirm during fix:** exact lower bound (Class 5 vs 6) of the valid-batch range in `isValidBatchForYearlyResult()`, and that the Class 10 pre-test variant shares the same flag-gating defect.

### Acceptance Criteria (Definition of Done)
* [ ] With the half-yearly flag **OFF**, the certificate card is **not** shown on Home for any affected school batch (Class 5–10) across Free, Trial, and Paid cohorts.
* [ ] With the flag **ON** and a valid result/certificate present, the card **is** shown and the tap opens the correct certificate/result flow.
* [ ] Card visibility is driven by `yearlyResultCollectionEnabled` (+ `resultCollectionExamType`) **and** a valid certificate/result — not by batch/class validity alone.
* [ ] Verified on the Class 7 (SSC '30) repro **plus** a Class 10 (pre-test) account; and confirmed that HSC (11–12) still shows no such card (negative check).
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
