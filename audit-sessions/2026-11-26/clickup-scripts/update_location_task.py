import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
TASK_ID = "z8zyy1ur0r"

body = """### What's happening
The moment a user opens the app and lands on Home, a **"Share your location" card** pops up over everything. It has a single button — **"এগিয়ে যাও / Proceed"** — and no way to close or skip it. There is no ✕, and Back doesn't dismiss it. If the user never shares their location, the same card returns on later visits to Home.

This is the **first thing a user sees after logging in** — it sits in front of their own home screen, and it can't be dismissed. It reads as a mandatory wall for something that should be optional.

### Who it affects
* **Every user type — paid, free, and trial.** There is no cohort rule; the card is driven purely by "has this account shared location yet," so everyone who hasn't is shown it.
* **In practice, every new user** — sign-up never asks for location, so a fresh account always hits it on first Home load.
* **Repeat exposure:** anyone who declines (or whose location never gets captured) keeps seeing it on subsequent Home visits, not just once.
* **Timing:** it is the very first interruption on Home — ahead of every other prompt the app might show.

### Why it matters
Forcing an undismissable location ask as the first screen interaction is a bad first impression and an easy trust hit — the user is blocked from their home for a request that isn't essential to using the app. A "Proceed"-only card with no decline gives the feeling of a dark pattern, and showing it repeatedly compounds the annoyance.

### What we want instead
1. **Show it once per account, ever.** It should appear a single time in the lifetime of the account — not on every Home load, and not until location is finally captured. After it's been shown once, it never comes back on its own.
2. **Let people close it.** Add a clear ✕, and allow tapping outside / Back to dismiss.
3. **Never force it.** Dismissing is a real exit — the user goes straight to Home with no re-prompt and no block. "Proceed" stays as the opt-in for users who do want to share location.

### Notes / out of scope
* The card currently explains itself as *"for video quality optimization."* The audit flagged that reason as weak/misleading. **Not part of this ticket** — but if product wants the wording revisited, it's an easy follow-up.
* This is Shikho's own in-app card, shown before the system location prompt. We are only changing how often our card appears and that it can be closed — the underlying location-permission behavior for users who opt in is unchanged.

### Severity
P2 – Major (audit S2). First-run, all cohorts, undismissable. *(Priority set to High — raise to Urgent if it should ship alongside the other home-entry fixes.)*

### Done when
* [ ] The "Share your location" card appears **at most once in the lifetime of an account**, for every user type — it does not return on later Home visits whether or not location was shared.
* [ ] The card has a working ✕ and can be dismissed by tapping outside or pressing Back.
* [ ] Dismissing it goes straight to Home — no re-prompt, no block.
* [ ] "Proceed" still works for users who choose to share location; nothing changes for accounts that already shared it.
* [ ] Other Home prompts (school, profile, results, etc.) still appear normally after this card is handled.
* [ ] The change is reversible.
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
