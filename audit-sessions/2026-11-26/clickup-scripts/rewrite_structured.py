# -*- coding: utf-8 -*-
import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]

location = """### Problem
The first thing a user sees after logging in isn't their home — it's a full-screen **"Share your location"** card with one button ("Proceed"), no ✕, no skip, no way back out. For a request that isn't essential to using the app, we've made it a wall. Decline it (or fail to capture location) and it comes back on the next Home visit.

### Who's affected
* **All cohorts — paid, free, trial.** It's driven only by "has this account shared location yet," not by user type.
* **Effectively every new user** — signup never asks for location, so fresh accounts always hit it.
* It's the **first interruption on Home**, ahead of everything else we show.

### Why it matters
The first impression we hand a brand-new student is a dead-end permission prompt that nags — a cheap, avoidable trust hit for something that's supposed to be optional.

### What we should do
* Ask **once per account, ever** — whether they accept, decline, or close it. No auto-repeat.
* Give it a **real close**: the ✕, tap-outside, and back should all dismiss it.
* Make **"Proceed" the opt-in**, not the only exit. The system permission flow for people who do want to share stays unchanged.
* *Separate, non-blocking:* the "for video quality optimization" reason is vague and a little misleading — worth a product copy pass later, but not part of unblocking this."""

cert = """### Problem
On the paid home, the hero slot tells the student **"Your certificate is ready — tap to download or share,"** even when there's no half-yearly result for their batch. It's a promise with nothing behind it; tapping leads into an empty flow.

### Who's affected
* **Paid (Premium) students only** — trial and free homes don't carry this card.
* **School batches, Class 5–10** — a half-yearly certificate for 5–9, a pre-test certificate for Class 10.
* **Not HSC (11–12)** — no half-yearly exam; they don't see it today and shouldn't start.
* Reproduced on a Class 7 paid account with no result published.

### Why it matters
We're using our most valuable screen slot to over-promise on the results moment students care about most — and then disappoint them with a dead end.

### What we should do
* Show the card **only when a real result/certificate actually exists**; hide it completely otherwise.
* When one does exist, it opens the correct certificate, as intended.
* Net: a paid student never sees "your certificate is ready" unless it genuinely is — and the ones who have a certificate still get the full moment."""

tour = """### Problem
The worst blocker in the audit. After signup → trial → Home, the **"Discover Shikho" tour** throws up a modal whose only working button is "Start tour." No skip, no close; back and tap-outside do nothing. The student is trapped on their very first screen.

### Who's affected
* **Every non-paid user** — free, trial, and lapsed — across all classes including HSC, 100% of the time.
* **Paid users never see it.**

### Why it matters
The one person we paid to acquire, in the moment they're most willing to engage, hits a wall they can't get past. There's no faster way to lose a brand-new student.

### What we should do
* **Kill switch, not a redesign** — turn the tour off for everyone, now.
* It comes back only once it has a working Skip/Close (that's separate work).
* Keep it reversible. Success looks like: no non-paid user meets the tour on Home, paid is unchanged, back and tap-outside behave normally, and nothing breaks or leaves a hole where the tour used to render."""

school = """### Problem
With no school saved, Home opens a selection sheet that **can't be dismissed** — the ✕ is drawn invisible and back doesn't close it — forcing the user through **Division → District → School** just to reach their own home. An invisible close is worse than an honest block: it just looks broken.

### Who's affected
* **All user types — paid, free, trial** — the moment their school field is empty.
* **Effectively every new account:** signup collects name, class, group and batch but never a school. It recurs on every Home load until they give in and pick one.

### Why it matters
We're gating the front door on information we don't need before someone can start learning — with a UI that reads as broken on first impression.

### What we should do
* **Stop force-opening the sheet on Home** for anyone; let users land on Home immediately.
* Keep school collection **voluntary**, where it already lives (Profile → Edit) — not a toll gate on the front door.
* Temporary and reversible if we ever redesign school collection with a real skip. Success: nobody is forced into it on Home, Home is usable on first load, and the voluntary edit path still works."""

badge = """### Problem
The gold **"Premium" badge** is supposed to mean "this person pays for Shikho right now." Today it means "this person isn't brand-new free" — so trial users wear it, and so do lapsed buyers whose paid access has expired and who are now back in the free/trial experience.

### Who's affected
* **Trial (non-paying) users** — shown Premium wrongly.
* **Lapsed/expired buyers** now in free/trial — still shown Premium.
* **Active paid users** — correct, and should stay that way.

### Why it matters
It misleads users about what they currently have, and it undercuts our own upsell — Premium is a weaker thing to sell when half the non-payers already look Premium.

### What we should do
* Show the badge **and** the avatar crown only for a **current, active, non-expired paid enrollment**.
* Trial and expired users lose it; active paid keep it, with no regression.
* The badge and the crown should always follow the same rule — they're making the same claim."""

notif = """### Problem
The **"Notification" row** in the Profile menu goes nowhere — tap it and you bounce straight back to Home, no screen, no feedback. The in-app notifications screen it used to open was removed, and the menu entry was left pointing at nothing. "Settings" right below it works, which makes the dead row obvious.

### Who's affected
* **Every logged-in user** has the row. We hit it 4× during the audit without trying.

### Why it matters
A visible button that does nothing reads as "this app is held together with tape" — a small but steady leak of trust.

### What we should do
* **Remove or hide the row** — there's no working destination to send people to, and a clean menu beats a dead link. It can return if a real notifications screen is ever rebuilt.
* **Do not touch push notifications** — the system-tray pushes and their tap-through deep links are a separate, working system. This is only about the dead in-app menu row.
* Success: the dead row is gone (or opens something real), the rest of the Profile menu is untouched, and push keeps working exactly as it does now."""

tasks = [
    ("z8zyy1ujwy", cert),
    ("z8zyy1ujz7", tour),
    ("z8zyy1uk1b", school),
    ("z8zyy1uk1u", badge),
    ("z8zyy1uqng", notif),
    ("z8zyy1ur0r", location),
]

for tid, body in tasks:
    payload = {"markdown_content": body}
    req = urllib.request.Request(
        f"https://api.clickup.com/api/v2/task/{tid}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": TOKEN, "Content-Type": "application/json"},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
        print("UPDATED", d.get("id"))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, tid); print(e.read().decode())
