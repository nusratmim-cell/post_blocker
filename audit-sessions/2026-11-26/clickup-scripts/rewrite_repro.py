# -*- coding: utf-8 -*-
import os, json, urllib.request
TOKEN = os.environ["CU_TOKEN"]
B = "https://t24567161.p.clickup-attachments.com/t24567161/"
def im(path, alt): return f"![{alt}]({B}{path})"

cert = f"""### Problem
On the paid Home, the top card says **"Your certificate is ready — tap to download or share"** even when the student has no half-yearly result. There is no certificate to open, so tapping it leads to an empty screen.

{im("b6e5dad4-9528-40e2-a888-638a9be9359a/image.png","Certificate card on Home")}

### How to reproduce
1. Log in with a **paid (Premium)** account on a school batch between **Class 5 and Class 10** (seen on Class 7, SSC '30).
2. Make sure that account has **no half-yearly result published** yet.
3. Open the app and go to the **Home (হোম)** tab.
4. Look at the top card — it reads *"See your certificate now / tap to download or share"*.
5. Tap the card → it opens an empty screen; there is no certificate.

### Who's affected
* **Paid (Premium) students only** — trial and free users don't see this card.
* **Class 5–10 school batches** — shown as a half-yearly certificate for Class 5–9, and a pre-test certificate for Class 10.
* **Not HSC (Class 11–12)** — they have no half-yearly exam and don't see it today. Keep it that way.

### Why it matters
This is the most visible spot on Home, and we're using it to promise a certificate that doesn't exist. Students tap it expecting a reward and get nothing.

### What we should do
* Show the card **only when a real certificate exists**. Hide it when there isn't one.
* When a certificate does exist, it should open correctly.
* Result: a paid student only sees "your certificate is ready" when it's true, and students who have one still get it."""

tour = f"""### Problem
This is the worst issue in the audit. After signup and starting a trial, the user lands on Home and the **"Discover Shikho" tour** opens. The only button that works is "Start tour" — no skip, no close, and back and tapping outside do nothing. The user is stuck on their first screen.

{im("40bdb9a5-3bd0-4752-9982-7552566cd892/ev_tour.jpg","Inescapable Discover Shikho tour")}

### How to reproduce
1. Create a **fresh account** (or use any non-paid account — free, trial, or lapsed).
2. If new: finish signup and **start the free trial**.
3. Land on the **Home (হোম)** tab — the **"Discover Shikho"** tour appears with a "Start tour" button.
4. Try to leave it: press **back**, **tap outside** the modal, look for a **✕ / skip** — none of them work.
5. Confirm the only thing that does anything is "Start tour".

### Who's affected
* **All non-paid users** — free, trial, and lapsed — on every class including HSC, every time.
* **Paid users never see it.**

### Why it matters
A brand-new student we just paid to bring in is blocked on the very first screen. This is the fastest way to lose them.

### What we should do
* **Turn the tour off for everyone now** — a simple on/off switch, not a redesign.
* Bring it back only after it has a working skip/close (separate task).
* Keep it reversible. When done: no non-paid user sees the tour, paid is unchanged, back and tap-outside work normally, and nothing is left broken where the tour used to be."""

school = f"""### Problem
If a user hasn't saved a school, Home opens a school-selection sheet they can't close — the ✕ is invisible and back doesn't work. To reach Home, they're forced to pick **Division → District → School** first. An invisible close is worse than a plain block: it just looks broken.

{im("af50aafc-72bf-4254-b08e-000ee445fef9/ev_wall.jpg","Mandatory school-selection sheet")}

### How to reproduce
1. Use an account with **no school saved** (a fresh signup works — signup never asks for a school).
2. Open the app and go to the **Home (হোম)** tab.
3. A school-selection sheet opens over Home (**Division → District → School**).
4. Try to close it: tap the **✕** area (it's drawn invisible) and press **back** — neither dismisses it.
5. Confirm you must select Division, District, and School before you can reach Home.

### Who's affected
* **All users — paid, free, and trial** — whenever their school field is empty.
* **Almost every new account**, because signup collects name, class, group, and batch, but not a school. It comes back on every Home load until they pick one.

### Why it matters
We're blocking the main screen to collect something we don't need before a student can start learning — and the broken-looking close makes the first impression worse.

### What we should do
* **Stop forcing the sheet on Home.** Let users reach Home right away.
* Keep setting a school **optional**, in Profile → Edit where it already is.
* Temporary and reversible. When done: no one is forced into it on Home, Home works on first load, and the optional school edit still works."""

badge = f"""### Problem
The gold **"Premium" badge** should mean the user is paying for Shikho right now. Instead, it shows for anyone who isn't a brand-new free user — so trial users get it, and so do users whose paid course has expired and who are back in the free/trial section.

{im("f35f3aea-5f99-4033-9a54-ca47dc41dc78/ev_trialprem.jpg","Trial user shown Premium")}
{im("55e8185a-51d6-4e9e-ab8d-cd893b967950/ev_congrats.jpg","Expired user still shown Premium")}

### How to reproduce
**Case A — Trial user**
1. Use an account on a **free trial** (not paid).
2. Open the **Home (হোম)** tab.
3. The header shows the gold **"প্রিমিয়াম" (Premium)** badge, even though the user hasn't paid.

**Case B — Expired / lapsed buyer**
1. Use an account that **bought a course which has since expired** and is now back in the free/trial section.
2. Open the **Home (হোম)** tab.
3. The Premium badge **still** shows, even though the paid access has ended.

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

notif = f"""### Problem
The **"Notification"** row in the Profile menu doesn't do anything — tapping it sends the user back to Home with no screen. The notifications screen it used to open was removed, and the menu item was left pointing at nothing. "Settings" right below it works, so the broken row stands out.

{im("76ffe1ce-7c70-4833-8226-361dd44857db/ev_notif.jpg","Dead Notification row in Profile menu")}

### How to reproduce
1. Log in with **any** account.
2. On Home, tap the **profile avatar** (top-right) to open the Profile menu.
3. Tap the **"নোটিফিকেশন" (Notification)** row.
4. The menu closes and you land back on **Home** — no notifications screen opens.
5. Tap it again → same thing every time. (For contrast, "Settings" right below it works.)

### Who's affected
* **Every logged-in user** has this row. We hit it 4 times during the audit.

### Why it matters
A button that does nothing makes the app feel broken and lowers trust.

### What we should do
* **Remove or hide the row.** There's nothing to open, so a clean menu is better than a dead link. It can come back if a real notifications screen is built later.
* **Don't touch push notifications** — the ones in the phone's notification tray and their links are a separate system that works. This is only about the dead menu row.
* When done: the dead row is gone (or opens a real screen), the rest of the Profile menu still works, and push notifications are unchanged."""

location = f"""### Problem
Right after login, before the user reaches Home, a full-screen **"Share your location"** card shows up. It has one button — "Proceed." There is no close (✕), no skip, and back doesn't work. The user can't get past it without tapping Proceed. If they decline, or location isn't saved, the card shows again next time they open Home.

{im("8eeb7412-c65c-45a7-8e74-cdcbd8772a79/ev_location.jpg","Forced Share-location card on Home")}

### How to reproduce
1. Use an account that **hasn't shared its location yet** (a fresh signup works — signup never asks for location).
2. Open the app and reach the **Home (হোম)** tab.
3. A full-screen **"Share your location"** card appears, with only an **"এগিয়ে যাও / Proceed"** button.
4. Try to close it: look for a **✕**, **tap outside**, press **back** — none dismiss it.
5. Without tapping Proceed, close and reopen the app to Home → the card **appears again**.

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

tasks = [("z8zyy1ujwy",cert),("z8zyy1ujz7",tour),("z8zyy1uk1b",school),
         ("z8zyy1uk1u",badge),("z8zyy1uqng",notif),("z8zyy1ur0r",location)]
for tid, body in tasks:
    req=urllib.request.Request(f"https://api.clickup.com/api/v2/task/{tid}",
        data=json.dumps({"markdown_content":body}).encode(),
        headers={"Authorization":TOKEN,"Content-Type":"application/json"}, method="PUT")
    try:
        d=json.load(urllib.request.urlopen(req)); print("UPDATED", d.get("id"))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, tid); print(e.read().decode()[:200])
