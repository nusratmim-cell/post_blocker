import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Summary
[Home / School Input] The mandatory school-selection bottom sheet (`CustomSchoolInputBottomSheet`) is force-opened over Home and cannot be meaningfully dismissed. **Disable this modal for all users.**

### Impact & Severity
* **Severity:** P2 – Major (audit S2). *(ClickUp priority set to Urgent to match the current disable batch — lower to High if preferred.)*
* **User Impact:** On every Home load with no saved school, the sheet covers Home and blocks the first view. The close (✕) is drawn transparent and Back does not dismiss it, so it reads as a hard wall — the user must pick a Division → District → School before reaching their Home. Hits new users immediately (onboarding does not collect school).
* **Frequency:** 100% reproducible on a fresh account (empty `schoolId` / `schoolName`); recurs on every Home load until a school is saved.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android (repro on Pixel 7, prod build `tech.shikho.android`)
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12)
* **Account / Test State:** Any account with empty saved school (`schoolId` or `schoolName` blank) — in practice a freshly registered account.

### Steps to Reproduce
1. Use an account whose profile has no school saved (e.g. a fresh signup — onboarding collects name/class/group/batch but not school).
2. Open the app and reach the **Home (হোম)** tab.
3. The school-selection bottom sheet opens over Home; the ✕ is invisible and Back does not dismiss it → Home is blocked until a school is chosen.

### Expected vs. Actual Behavior
* **Expected (this change):** The school-selection sheet is **not** force-opened on Home for any user. Home is immediately usable. (Setting a school remains available voluntarily via Profile → Edit.)
* **Actual:** The sheet is forced open on every Home load when school is empty, with a transparent close icon and Back disabled — a mandatory hard-wall.

### Impacted User Type (definitive)
* **All user types — Paid, Free, Trial.** The trigger is purely "school is empty," with **no user-type condition**.
  * Evidence: `HomeViewModel.kt:719-724` — *"The sheet is forced open whenever the saved school id or school name is empty in app preferences, checked on every home load."* It runs in the Home dialog priority queue (`SHOW_SCHOOL_INPUT_BOTTOM_SHEET`, priority 2) on all home variants.
  * In practice it surfaces for **new/fresh users**, since onboarding does not collect school.

### Evidence & Mechanism
* **Visuals:** School hard-wall screenshot attached.
* **Mechanism (shikho-android spec + codemap):**
  * Component: `CustomSchoolInputBottomSheet.kt` (`app/.../ui/feature/compose/home/views/`) — *"the school sheet, shown on home, with the close icon made transparent when the sheet is mandatory"* (`:89-91`).
  * Trigger: `HomeViewModel.kt:719-724` — forced open whenever saved `schoolId` OR `schoolName` is empty, checked on every Home load. Gate flag: `showSchoolInput` (AppPreference). Dialog: `SHOW_SCHOOL_INPUT_BOTTOM_SHEET` (priority 2, dashboard SPEC §5.5).
  * Sheet flow: Division → District → School search (paginated, 1000ms debounce); Save disabled until Division + District + School selected and query non-empty; "Add New School" only if `allowUserToAddTemporarySchool` is true (writes via `AddNewSchoolToDataBase` → `Core.UpsertSchool`, `temp_school: true`).
  * **Note:** The "no close" is cosmetic — the ✕ is drawn transparent but still tappable ("a tappable but invisible escape"). This is a fake hard-wall, not a true block.

### How to Disable (dev notes)
* Stop force-opening the sheet on Home: guard/remove the empty-school trigger at `HomeViewModel.kt:719-724` (do not enqueue `SHOW_SCHOOL_INPUT_BOTTOM_SHEET`), and/or keep `showSchoolInput` off so the sheet is never forced.
* Leave the **voluntary** school-edit path intact (Profile Edit → `SchoolInfoEditScreen`); only the forced Home modal is being disabled.
* No remote feature flag exists for this today — client change. Add one if feasible so it can be toggled without a release. Keep the change reversible.

### Acceptance Criteria (Definition of Done)
* [ ] No user type (Paid, Free, Trial) is shown the forced school-selection bottom sheet on Home — including a fresh account with empty school.
* [ ] Home is fully interactive on first load; Back and normal navigation behave normally (no residual forced sheet).
* [ ] A user can still set/change their school voluntarily via Profile → Edit (that path is unaffected).
* [ ] No crash or empty state where the forced sheet used to appear; no school-sheet analytics regressions.
* [ ] Change is reversible — the sheet can be re-enabled later if school collection is redesigned with a real Skip.
"""

payload = {
    "name": "[PROD][APP][School Input]: Disable the mandatory school-selection modal (hard-wall) on Home for all users",
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
    print("OK", d.get("id"), d.get("url"), "prio", (d.get("priority") or {}).get("priority"), "tags", [t.get("name") for t in d.get("tags", [])])
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode())
