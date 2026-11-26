import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Summary
[Home / Discover Shikho Tour] The post-trial-activation "Discover Shikho" guided tour (trip-tour modal) is **inescapable** — no skip, no close, Back and outside-tap both fail. **Disable this feature for now**; no user type (Paid, Free, Trial) should see it.

### Impact & Severity
* **Severity:** P1 – Critical (Urgent) — the single worst blocker in the audit: a brand-new, high-intent student is trapped on first entry with no escape.
* **User Impact:** After trial activation the "Start tour" modal appears and cannot be dismissed — only "Start tour" works; Back + outside-tap do nothing; the exit path is demoted/friction. It blocks the student's first real session.
* **Frequency:** 100% reproducible on fresh signup → trial activation; reproduced across classes including HSC.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android (repro on Pixel 7, prod build `tech.shikho.android`)
* **App Version / Build:** Latest PROD build (spec baseline v6.0.12)
* **Account / Test State:** Fresh signup → free trial activated → lands on trial Home.

### Steps to Reproduce
1. Complete a fresh signup and activate the free trial.
2. Land on the trial Home — the "Discover Shikho / Start tour" modal appears.
3. Try Back, outside-tap, or close → all fail; only "Start tour" proceeds.

### Expected vs. Actual Behavior
* **Expected (this change):** The guided tour does not appear for any user type (Paid, Free, Trial). The feature is disabled until it is redesigned with a working Skip/Close.
* **Actual:** The tour is forced on the trial Home with no way out.

### Evidence & Scope Notes
* **Visuals:** Forced-tour screenshot attached.
* **Mechanism (shikho-android spec + codemap):**
  * Component: `DiscoverShikhoComponent.kt` (`ui/feature/compose/home/views/freetrial/`), rendered by the trial home body `TrialV2Screen.kt:206-207`. `HomeBody.kt:51-104` splits the home into free / trial / paid bodies.
  * Gate/state: `showTripTourDialog` → AppPreference key `TRIP_TOUR_DIALOG`, **default `TripEnum.FIRST_TIME`** (every fresh install starts in the tour-showing state). After trial activation the state is saved: `TrialSuccessSheetDialog → Save TripTourDialog state → restartDashboardActivity()` (promotion SPEC).
  * Exit blocked: `DISCOVERY_CLOSE_CONFIRMATION` dialog (priority 2) fires when the user tries to exit — this is the "no skip / friction-to-dismiss" behavior.
  * VM/API: `HomeDiscoveryViewModel`; discovery stat via `AppDiscoveryUseCase` and backend `app_discovery_state` (`GetAppDiscoveryState` / `UpdateAppDiscoveryState`). Completion event `Tour Success` guarded by `discoverTourSuccessEventSent` (SC-1469) at `DiscoverShikhoComponent.kt:397-402`.
* **Scope of visibility (from the data):**
  * **Confirmed:** Trial users (post-activation) — the tour is wired into the trial home body.
  * **Not found** on the Free (`FreeUserScreen.kt:43-53`) or Paid (`PaidV2Screen.kt:56`) bodies in spec/codemap — so Paid/Free likely do not render it.
  * **Caveat:** `TRIP_TOUR_DIALOG` defaults to `FIRST_TIME` for every fresh install and there is **no remote feature flag** for this ("cannot remotely disable without an app update" — promotion SPEC). The explicit user-type guard was not located. Therefore the disable must be enforced globally and verified by a negative check on all three cohorts.

### How to Disable (dev notes)
* Short-circuit the trigger so `DiscoverShikhoComponent` / the trip-tour modal never shows — e.g. stop defaulting `showTripTourDialog` to `FIRST_TIME` (set it to the seen/disabled state), and/or gate the trial-home tour section behind a kill switch that is OFF. Skip the `DISCOVERY_CLOSE_CONFIRMATION` path since the tour will not show.
* No remote flag exists today; if feasible, add one so this can be toggled without a release. Otherwise ship the client change.
* Keep it reversible — this is a temporary disable until the tour is redesigned with a real Skip/Close (see related finding: friction-to-dismiss tour exit).

### Acceptance Criteria (Definition of Done)
* [ ] No user type (Paid, Free, Trial) sees the "Discover Shikho" guided tour / trip-tour modal on Home — including immediately after trial activation.
* [ ] Back press and outside-tap behave normally on Home after the change (no residual forced modal).
* [ ] Verified on: fresh signup → trial activation (primary repro), a Free (no-enrollment) account, and a Paid account.
* [ ] No tour analytics fire while disabled (`Tour Success` / `Tour Exit`); no crash or empty slot where the tour used to render.
* [ ] Change is reversible — the tour can be re-enabled later once it ships with a working Skip/Close.
"""

payload = {
    "name": "[PROD][APP][Discover Tour]: Disable the inescapable 'Discover Shikho' guided tour for all user types (no skip / no close / back disabled)",
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
    print("OK", d.get("id"), d.get("url"))
    print("PRIORITY", (d.get("priority") or {}).get("priority"))
    print("TAGS", [t.get("name") for t in d.get("tags", [])])
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode())
