# -*- coding: utf-8 -*-
import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]
B = "https://t24567161.p.clickup-attachments.com/t24567161/"

def img(path, alt):
    return f"![{alt}]({B}{path})\n\n"

cert = img("b6e5dad4-9528-40e2-a888-638a9be9359a/image.png", "Home screen") + """### Problem
On the paid Home, the top card says **"Your certificate is ready — tap to download or share"** even when the student has no half-yearly result. There is no certificate to open, so tapping it leads to an empty screen.

### Who's affected
* **Paid (Premium) students only** — trial and free users don't see this card.
* **Class 5–10 school batches** — shown as a half-yearly certificate for Class 5–9, and a pre-test certificate for Class 10.
* **Not HSC (Class 11–12)** — they have no half-yearly exam and don't see it today. Keep it that way.
* Seen on a Class 7 paid account with no result published.

### Why it matters
This is the most visible spot on Home, and we're using it to promise a certificate that doesn't exist. Students tap it expecting a reward and get nothing.

### What we should do
* Show the card **only when a real certificate exists**. Hide it when there isn't one.
* When a certificate does exist, it should open correctly.
* Result: a paid student only sees "your certificate is ready" when it's true, and students who have one still get it."""

tour = img("40bdb9a5-3bd0-4752-9982-7552566cd892/ev_tour.jpg", "Forced tour") + """### Problem
This is the worst issue in the audit. After signup and starting a trial, the user lands on Home and the **"Discover Shikho" tour** opens. The only button that works is "Start tour" — no skip, no close, and back and tapping outside do nothing. The user is stuck on their first screen.

### Who's affected
* **All non-paid users** — free, trial, and lapsed — on every class including HSC, every time.
* **Paid users never see it.**

### Why it matters
A brand-new student we just paid to bring in is blocked on the very first screen. This is the fastest way to lose them.

### What we should do
* **Turn the tour off for everyone now** — a simple on/off switch, not a redesign.
* Bring it back only after it has a working skip/close (separate task).
* Keep it reversible. When done: no non-paid user sees the tour, paid is unchanged, back and tap-outside work normally, and nothing is left broken where the tour used to be."""

school = img("af50aafc-72bf-4254-b08e-000ee445fef9/ev_wall.jpg", "School wall") + """### Problem
If a user hasn't saved a school, Home opens a school-selection sheet they can't close — the ✕ is invisible and back doesn't work. To reach Home, they're forced to pick **Division → District → School** first. An invisible close is worse than a plain block: it just looks broken.

### Who's affected
* **All users — paid, free, and trial** — whenever their school field is empty.
* **Almost every new account**, because signup collects name, class, group, and batch, but not a school. It comes back on every Home load until they pick one.

### Why it matters
We're blocking the main screen to collect something we don't need before a student can start learning — and the broken-looking close makes the first impression worse.

### What we should do
* **Stop forcing the sheet on Home.** Let users reach Home right away.
* Keep setting a school **optional**, in Profile → Edit where it already is.
* Temporary and reversible. When done: no one is forced into it on Home, Home works on first load, and the optional school edit still works."""

badge = img("55e8185a-51d6-4e9e-ab8d-cd893b967950/ev_congrats.jpg", "Expired user still Premium") + img("f35f3aea-5f99-4033-9a54-ca47dc41dc78/ev_trialprem.jpg", "Trial user shown Premium") + """### Problem
The gold **"Premium" badge** should mean the user is paying for Shikho right now. Instead, it shows for anyone who isn't a brand-new free user — so trial users get it, and so do users whose paid course has expired and who are back in the free/trial section.

### Who's affected
* **Trial users** — see Premium even though they haven't paid.
* **Expired/lapsed buyers** now in free/trial — still see Premium.
* **Active paid users** — correct, and should keep it.

### Why it matters
It tells users they have something they don't, and it weakens our upgrade offer — Premium is harder to sell when non-paying users already look Premium.

### What we should do
* Show the badge **and** the avatar crown **only for active, non-expired paid users**.
* Trial and expired users: no badge. Active paid: keep it.
* The badge and the crown should always match — they mean the same thing."""

notif = img("76ffe1ce-7c70-4833-8226-361dd44857db/ev_notif.jpg", "Notification row") + """### Problem
The **"Notification"** row in the Profile menu doesn't do anything — tapping it sends the user back to Home with no screen. The notifications screen it used to open was removed, and the menu item was left pointing at nothing. "Settings" right below it works, so the broken row stands out.

### Who's affected
* **Every logged-in user** has this row. We hit it 4 times during the audit.

### Why it matters
A button that does nothing makes the app feel broken and lowers trust.

### What we should do
* **Remove or hide the row.** There's nothing to open, so a clean menu is better than a dead link. It can come back if a real notifications screen is built later.
* **Don't touch push notifications** — the ones in the phone's notification tray and their links are a separate system that works. This is only about the dead menu row.
* When done: the dead row is gone (or opens a real screen), the rest of the Profile menu still works, and push notifications are unchanged."""

location = img("8eeb7412-c65c-45a7-8e74-cdcbd8772a79/ev_location.jpg", "Location popup") + """### Problem
Right after login, before the user reaches Home, a full-screen **"Share your location"** card shows up. It has one button — "Proceed." There is no close (✕), no skip, and back doesn't work. The user can't get past it without tapping Proceed. If they decline, or location isn't saved, the card shows again next time they open Home.

### Who's affected
* **All users — paid, free, and trial.** It depends only on whether the account has shared location yet, not on user type.
* **Almost every new user**, because signup never asks for location.
* It's the **first popup on Home**, before anything else.

### Why it matters
A new student's first moment in the app is a popup they can't close, for something that isn't even required. It's an easy way to annoy people and lose trust.

### What we should do
* Show it **once per account, ever** — whether the user accepts, declines, or closes it. Don't show it again.
* Add a **working close** (✕, tap outside, and back should all close it).
* Keep **Proceed as an optional choice**, not the only way out. Nothing changes for users who do want to share location.
* *Side note (not part of this fix):* the reason text "for video quality optimization" is unclear and a bit misleading — worth rewording later."""

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
