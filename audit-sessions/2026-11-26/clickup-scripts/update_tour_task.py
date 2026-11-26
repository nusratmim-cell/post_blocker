import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
TASK_ID = "z8zyy1ujz7"

body = """### Summary
[Home / Discover Shikho Tour] The "Discover Shikho" guided tour (trip-tour modal) on the non-paid Home is **inescapable** — no skip, no close, Back and outside-tap both fail. **Disable this feature for now** so no user sees it.

### Impact & Severity
* **Severity:** P1 – Critical (Urgent) — the single worst blocker in the audit: a brand-new, high-intent student is trapped on first entry with no escape.
* **User Impact:** On the non-paid Home, the "Start tour" modal appears and cannot be dismissed — only "Start tour" works; Back + outside-tap do nothing; the exit path is demoted/friction. It blocks the student's first real session.
* **Frequency:** 100% reproducible on fresh signup → trial activation; reproduced across classes including HSC.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android (repro on Pixel 7, prod build `tech.shikho.android`)
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12)
* **Account / Test State:** Non-paid account (`accessLevel == ReadOnly`) — fresh signup → free trial activated → lands on the non-paid Home.

### Steps to Reproduce
1. Complete a fresh signup and activate the free trial (or use any non-paid / lapsed account — `accessLevel == ReadOnly`).
2. Land on the non-paid Home — the "Discover Shikho / Start tour" modal appears.
3. Try Back, outside-tap, or close → all fail; only "Start tour" proceeds.

### Expected vs. Actual Behavior
* **Expected (this change):** The guided tour does not appear for any user. The feature is disabled until it is redesigned with a working Skip/Close.
* **Actual:** The tour is forced on the non-paid Home with no way out.

### Impacted User Type (definitive)
* **Impacted — all non-paid users (`accessLevel == ReadOnly` → `FreeUserScreen` home):** Free (no enrollment), Trial, and lapsed/expired users.
  * Evidence: `03_PRODUCT.md` Home Screen Variants — `FreeUserScreen` (`accessLevel == ReadOnly`) lists "Free trial course list, free animated lessons, **discover Shikho**"; Business rule §4.1: *"accessLevel == ReadOnly → Shows FreeUserScreen with discover/trial."*
* **NOT impacted — Paid users (`accessLevel == Full` → `PaidV2Screen`):** `PaidV2Screen` sections are FocusHub, Priority Subjects, Routine, CourseProgress, QuarterCard, ReportCard, PracticeQuiz, BottomCards — **no Discover Shikho section**.

### Evidence & Mechanism
* **Visuals:** Forced-tour screenshot attached.
* **Mechanism (shikho-android spec + codemap):**
  * Component: `DiscoverShikhoComponent.kt` (`ui/feature/compose/home/views/freetrial/`), rendered on the non-paid Home (`FreeUserScreen` / homev2; older `TrialV2Screen.kt:206-207`). `HomeBody.kt:51-104` splits the home by access level.
  * Gate/state: `showTripTourDialog` → AppPreference key `TRIP_TOUR_DIALOG`, **default `TripEnum.FIRST_TIME`** (every fresh install starts in the tour-showing state). After trial activation the state is saved: `TrialSuccessSheetDialog → Save TripTourDialog state → restartDashboardActivity()` (promotion SPEC).
  * Exit blocked: `DISCOVERY_CLOSE_CONFIRMATION` dialog (priority 2) fires when the user tries to exit — the "no skip / friction-to-dismiss" behavior.
  * VM/API: `HomeDiscoveryViewModel`; discovery stat via `AppDiscoveryUseCase` and backend `app_discovery_state` (`GetAppDiscoveryState` / `UpdateAppDiscoveryState`). Completion event `Tour Success` guarded by `discoverTourSuccessEventSent` (SC-1469) at `DiscoverShikhoComponent.kt:397-402`.

### How to Disable (dev notes)
* Short-circuit the trigger so the Discover Shikho section / trip-tour modal never shows on the non-paid Home — e.g. stop defaulting `showTripTourDialog` to `FIRST_TIME` (set it to the seen/disabled state), and/or gate the Discover Shikho section behind a kill switch that is OFF. Skip the `DISCOVERY_CLOSE_CONFIRMATION` path since the tour will not show.
* No remote flag exists today ("cannot remotely disable without an app update" — promotion SPEC); if feasible, add one. Otherwise ship the client change.
* Keep it reversible — temporary disable until the tour is redesigned with a real Skip/Close (related finding: friction-to-dismiss tour exit).

### Acceptance Criteria (Definition of Done)
* [ ] No user sees the "Discover Shikho" guided tour / trip-tour modal on Home — across Free, Trial, and lapsed/expired (`accessLevel == ReadOnly`) accounts, including immediately after trial activation.
* [ ] Confirmed Paid (`accessLevel == Full`) users continue to see no such tour (regression/negative check).
* [ ] Back press and outside-tap behave normally on Home after the change (no residual forced modal).
* [ ] No tour analytics fire while disabled (`Tour Success` / `Tour Exit`); no crash or empty slot where the tour used to render.
* [ ] Change is reversible — the tour can be re-enabled later once it ships with a working Skip/Close.
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
