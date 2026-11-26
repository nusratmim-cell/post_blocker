import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Summary
[Home / Location] On home entry a custom in-app **"লোকেশন শেয়ার করো" (Share location)** card is force-shown with a single **"এগিয়ে যাও" (Proceed)** action — no close (✕), no skip, no decline — and it keeps reappearing on later home loads until the user's location is captured. **Make it show once per account lifetime, add a working close (✕), and never force it.**

### Impact & Severity
* **Severity:** P2 – Major (audit S2). *(ClickUp priority set to High — bump to Urgent to sit with the other home-entry disables if preferred.)*
* **User Impact:** This is the highest-priority item in the Home dialog queue (priority 1), so it is the first thing a user meets after launch — ahead of their actual home. The only button is "এগিয়ে যাও"; there is no way to decline or dismiss, so it reads as a mandatory wall. Because the gate is "location stored (success)", a user who never grants/stores location is shown it again on subsequent home entries.
* **Frequency:** Shown on home entry whenever location has not been stored; recurs on later home loads until capture. 100% reproducible on a fresh account.

### Environment & Context
* **Environment:** Production (PROD)
* **Platform / Device:** Android (prod build `tech.shikho.android`, observed build 6.0.13 on Pixel 7)
* **Account / Test State:** Any logged-in account that has not yet stored a location (`isLocationStored` false) — in practice every fresh account.

### Steps to Reproduce
1. Log in (or use an account that has never stored location) and reach the **Home (হোম)** tab.
2. The **"লোকেশন শেয়ার করো"** card opens over Home, reason text *"ভিডিও কোয়ালিটি অপটিমাইজেশনের জন্য তোমার লোকেশন শেয়ার করো"*, with a single **"এগিয়ে যাও"** button.
3. There is no ✕ / Skip / Back dismissal — the only way forward is Proceed (which fires the OS location permission request).
4. If location is not granted/stored, re-enter Home → the card appears again.

### Expected vs. Actual Behavior
* **Expected (this change):**
  * The card appears **at most once per account lifetime** (not on every home load, not gated on capture success).
  * The card has a working **close (✕)** and can be dismissed by tap-outside / Back.
  * Dismissing is a real exit — no re-prompt, no block. "এগিয়ে যাও" remains available but optional.
* **Actual:**
  * The card re-queues on home entry until location is stored.
  * No close affordance — only "এগিয়ে যাও".
  * Effectively a forced, repeatable interruption before the user reaches their own home.

### Impacted User Type (definitive)
* **All user types — Paid, Free, Trial.** The dialog is enqueued on every home load (`onCreate`/`onStart`) gated only by the `isLocationStored` flag, with **no user-type condition**.
  * Evidence: Dashboard dialog priority queue — `LOCATION_PERMISSION_DIALOG` priority **1** (highest), `HomeViewModel.kt:397-403`; queue mechanism `HomeSheetAndDialogType` (dashboard SPEC §5.5, §7.4).

### Evidence & Mechanism (tech spec)
* **Visuals:** Attached (`ev_location.jpg`).
* **Dialog:** `LOCATION_PERMISSION_DIALOG` (`HomeSheetAndDialogType`), priority 1 in the Home `PriorityQueue<HomeSheetAndDialogType>`; processed first before school-input / profile / yearly-result dialogs (dashboard SPEC §5.5).
* **Trigger / gate:** Added to the queue on home entry; gated by persistent flag **`isLocationStored`** (`AppPreference`, UI-state category — `core/datastore` `AppPreference.kt`). Because the gate tracks *successful capture*, not *already shown*, it recurs until location is stored.
* **Proceed action:** `HomeViewModel.invokeLocationAction()` checks fine+coarse permission, then the OS permission request → GPS read → `UpdateUserLocationUseCase` → `HomeViewModel.updateUserLastLocation()` stores lat/lng (dashboard SPEC §6.1, §9).
* **Copy:** reason shown is *"ভিডিও কোয়ালিটি অপটিমাইজেশনের জন্য..."* (for video-quality optimization). *(Optional: the UX audit flagged this reason as weak/misleading; not in scope for this ticket unless product wants the copy revisited.)*
* **Not the OS dialog:** this is Shikho's own in-app card shown *before* the Android location-permission prompt; the OS prompt only appears after "এগিয়ে যাও".

### How to Fix (dev notes)
* **Once per lifetime:** stop gating the card's display on `isLocationStored` (capture success). Gate instead on a persistent *"location prompt already shown"* state that is set the **first time the card is displayed**, so it is enqueued at most once per account — regardless of grant, deny, or dismiss. (Location capture can still be attempted silently later if product wants it, without re-showing the card.)
* **Dismissible:** add a visible, tappable **✕ / close** to the card and allow tap-outside + Back to dismiss. On dismiss, mark the "shown" state and move the dialog queue on.
* **Not forced:** dismissal must fully exit with no re-prompt; "এগিয়ে যাও" stays as the opt-in path.
* Keep OS-permission behavior unchanged — this only changes **when/how often** the in-app card appears and that it can be closed.
* No remote flag exists for this today — client change. Add one if feasible so it can be toggled without a release. Keep it reversible.

### Acceptance Criteria (Definition of Done)
* [ ] The "লোকেশন শেয়ার করো" card is shown **at most once per account lifetime**, for any user type — it does not reappear on later home loads, whether or not location was granted/stored.
* [ ] The card has a working **close (✕)** and can be dismissed via tap-outside / Back.
* [ ] Dismissing the card does not re-prompt, does not block Home, and does not re-queue it.
* [ ] "এগিয়ে যাও" still works (OS permission → location store) for users who opt in; existing stored-location behavior is unaffected.
* [ ] Other Home dialogs (school input, profile completion, yearly result, etc.) still fire in their normal order after this card is handled.
* [ ] Change is reversible.
"""

payload = {
    "name": "[PROD][APP][Home/Location]: 'Share location' card is forced & repeats — show once per lifetime, add close (✕), make it dismissible",
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
