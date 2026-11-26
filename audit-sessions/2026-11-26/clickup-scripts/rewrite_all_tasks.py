import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]

cert = """### What's happening
On the paid (Premium) Home screen, the top card invites the student to **"See your certificate now — tap to download or share"** even when there is **no half-yearly result** for their batch. Tapping it drops them into an empty/broken flow — there's nothing to download or share.

### Who it affects
* **Paid (Premium) students on school batches, Class 5–10.** This certificate card only lives on the Premium home, so trial and free users never see it.
  * Classes 5–9 show it as a half-yearly result certificate; Class 10 shows it as a pre-test certificate.
* **Not affected:** HSC (Class 11–12) — they don't have half-yearly exams and shouldn't see this card at all. Trial and free homes don't carry it.
* Reproduced on a Class 7 (SSC '30) paid account that has no published half-yearly result.

### Why it matters
It's the #1 slot on Home, and it's a broken promise — a prominent call-to-action for a certificate that doesn't exist. Students tap it expecting a reward and hit a dead end, which erodes trust in the whole results experience.

### What we want instead
* When there is **no published half-yearly result** for the student's batch (nothing to show), the certificate card is **hidden**.
* When a real result/certificate **is** available, the card shows and opens the correct certificate.

### Severity
P1 – Critical (Urgent). Top-of-home, paid users, broken call-to-action.

### Done when
* [ ] With no half-yearly result available, the certificate card does not appear on the paid Home for any affected batch (Class 5–10).
* [ ] With a valid result available, the card shows and opens the correct certificate.
* [ ] Verified for both the Class 5–9 (half-yearly) and Class 10 (pre-test) variants, on paid accounts.
* [ ] HSC (Class 11–12) still never shows this card, and existing results flows are unaffected.
"""

tour = """### What's happening
When a non-paid user lands on Home, a **"Discover Shikho" guided-tour modal** ("Start tour") appears and **cannot be dismissed** — there's no skip, no close, and both Back and tapping outside do nothing. The only button that works is "Start tour." The student is trapped before they reach their own home. **We want to turn this tour off entirely for now.**

### Who it affects
* **All non-paid users — free (no enrollment), trial, and lapsed/expired.** This is exactly the audience we most want to activate: brand-new, high-intent students on their very first session.
* **Not affected:** paid users — the paid home has no Discover Shikho tour.
* Reproduced 100% of the time on fresh signup → trial activation, across classes (including HSC).

### Why it matters
This is the single worst blocker in the audit. A new student's first real moment in the app is a wall they can't get past — the fastest possible way to lose someone we just acquired.

### What we want instead
* The Discover Shikho guided tour **does not appear for anyone** until it's redesigned with a working Skip/Close.
* Temporary and reversible — it can be switched back on once the exit is fixed (related finding: the tour's dismiss friction).

### Severity
P1 – Critical (Urgent). First-run, non-paid, fully inescapable.

### Done when
* [ ] No user sees the Discover Shikho tour on Home — free, trial, and lapsed/expired — including right after trial activation.
* [ ] Paid users continue to see no such tour (unchanged).
* [ ] Back and outside-tap behave normally on Home, with no leftover forced modal.
* [ ] No tour-related analytics fire while it's off, and there's no empty gap where the tour used to be.
* [ ] The change is reversible.
"""

school = """### What's happening
When a user has no school saved, Home opens a **school-selection sheet that can't be meaningfully dismissed** — the close (✕) is there but drawn invisible, and Back doesn't close it. To reach their own Home, the user is forced to pick **Division → District → School** first. **We want to turn this forced sheet off for all users.**

### Who it affects
* **All user types — paid, free, and trial.** The only trigger is "no school saved," with no other condition, so anyone missing a school hits it.
* **In practice, every new user** — sign-up collects name/class/group/batch but never a school, so fresh accounts always get walled.
* Recurs on every Home load until a school is finally chosen.

### Why it matters
It blocks the first view of Home behind a multi-step form for information that isn't required to start learning. The invisible close makes it feel like a hard wall (even though the ✕ is technically tappable), which is a confusing, trust-damaging first experience.

### What we want instead
* The school-selection sheet is **not force-opened on Home** for any user — Home is immediately usable.
* Setting a school stays available **voluntarily** via Profile → Edit (that path is unchanged).
* Temporary and reversible — the sheet can be reintroduced later if school collection is redesigned with a real Skip.

### Severity
P2 – Major. (Priority set to Urgent to ship with the other home-entry disables.)

### Done when
* [ ] No user type (paid, free, trial) is shown a forced school-selection sheet on Home — including a fresh account with no school.
* [ ] Home is fully usable on first load; Back and normal navigation behave normally.
* [ ] Users can still set/change their school voluntarily from Profile → Edit.
* [ ] No empty state or crash where the forced sheet used to be.
* [ ] The change is reversible.
"""

badge = """### What's happening
The gold **"প্রিমিয়াম" (Premium) badge** (crown + label) on the Home header is shown to **anyone who isn't a brand-new free user** — including trial users and people whose paid course has since **expired** and who are now back in the free/trial experience. It tracks "has ever had access," not "has active paid access right now."

### Who it affects
* **Trial (non-paying) users** — they wear the Premium badge despite not having paid.
* **Lapsed/expired buyers** — someone whose purchase has ended, now in the free/trial section, still shows Premium.
* Active paid users correctly show it (and should keep showing it).

### Why it matters
The badge is supposed to signal active paid status. Showing it to trial and expired users blurs the line between paid and unpaid, misleads the user about what they currently have, and **dilutes the value of the real upgrade** — it's harder to sell Premium when non-paying users already look Premium.

### What we want instead
* The Premium badge (and the matching crown on the avatar) shows **only** for users with a **current, active, non-expired paid enrollment**.
* Trial users and lapsed/expired buyers do **not** see it.
* Active paid users still see it — no change for them.

### Severity
P2 – Major (High).

### Done when
* [ ] The Premium badge and avatar crown show only for users with active, non-expired paid access.
* [ ] Trial users do not see the Premium badge.
* [ ] Lapsed/expired buyers (now in free/trial, no active paid) do not see it.
* [ ] Active paid users still see it (no regression).
* [ ] The badge and the avatar crown always agree (both follow the same rule).
"""

notif = """### What's happening
In the Profile menu, the **"নোটিফিকেশন" (Notification)** row is **dead** — tapping it just bounces back to Home with no screen and no feedback. The in-app notifications/inbox screen it used to open has been removed, so the row now points nowhere. "Settings" right below it works, which makes the broken row stand out. **We want to remove (or hide) this row for now.**

### Who it affects
* **Any logged-in user** — the Profile menu, and this row, is shown to everyone.
* 100% reproducible (hit 4× during the audit).

### Why it matters
A visible menu item that leads nowhere reads as the app being broken. It's a small thing that quietly undermines confidence, and there's no working destination to send people to.

### What we want instead
* Remove or hide the **"Notification" row** from the Profile menu, since it has no working destination. (If a real notifications screen is ever rebuilt, the row can come back pointing at it.)
* **Important — leave push notifications untouched.** System-tray push notifications and their tap-through deep links are a **separate, working system** and must not be affected. This is only about the dead in-app menu row.
* Reversible.

### Severity
P3 – Minor. (Priority set to High.)

### Done when
* [ ] The "Notification" row no longer appears in the Profile menu for any user (or, if kept, it opens a real screen — never a bounce to Home).
* [ ] The rest of the Profile menu (Settings, Profile Edit, Subscription, etc.) still works.
* [ ] Push notifications (system-tray + deep links) are completely unaffected.
* [ ] The change is reversible.
"""

tasks = [
    ("z8zyy1ujwy", "[PROD][APP][Home]: Half-yearly certificate card appears when there's no result to show", cert),
    ("z8zyy1ujz7", "[PROD][APP][Home]: Disable the inescapable 'Discover Shikho' tour (no skip or close) for all users", tour),
    ("z8zyy1uk1b", "[PROD][APP][Home]: Disable the mandatory school-selection wall for all users", school),
    ("z8zyy1uk1u", "[PROD][APP][Home]: 'Premium' badge shows for trial and expired users — limit it to active paid", badge),
    ("z8zyy1uqng", "[PROD][APP][Profile]: Remove the dead 'Notification' menu row (bounces to Home)", notif),
]

for tid, name, body in tasks:
    payload = {"name": name, "markdown_content": body}
    req = urllib.request.Request(
        f"https://api.clickup.com/api/v2/task/{tid}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": TOKEN, "Content-Type": "application/json"},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
        print("UPDATED", d.get("id"), "->", name[:55])
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, tid); print(e.read().decode())
