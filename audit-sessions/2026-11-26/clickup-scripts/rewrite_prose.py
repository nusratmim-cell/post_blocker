# -*- coding: utf-8 -*-
import os, json, urllib.request

TOKEN = os.environ["CU_TOKEN"]

location = """The first thing a user sees after logging in isn't their home — it's a full-screen "Share your location" card they can't get rid of. One button, "Proceed." No ✕, no skip, no way back out. For a request that isn't essential to using the app, we've turned it into a wall. And if someone declines, or location never gets captured, the card is back the next time they open Home. So the first impression we hand a brand-new student is a dead-end permission prompt that nags.

This hits everyone — paid, free, trial — because it's driven purely by whether the account has shared location yet, not by who the user is. Signup never asks for location, so in practice every new user walks straight into it, and it's the very first interruption on Home, ahead of everything else we might show them.

The fix is restraint. Ask once in the entire life of the account and never again — whether they say yes, say no, or just close it. Give the card a real close (the ✕, tap-outside, and back should all work), and let "Proceed" be the opt-in it should always have been instead of the only exit. We're not changing the system permission flow for people who genuinely want to share their location — we're just no longer holding the app hostage to get there.

Separately worth a look, but not blocking this: the card sells itself as "for video quality optimization," which is vague and a bit misleading. That's a copy decision for product, not part of unblocking people."""

cert = """On the paid home, the hero slot — our most valuable screen real estate — tells the student "Your certificate is ready, tap to download or share." Except there's no certificate. For anyone on a batch with no published half-yearly result, that card is a promise with nothing behind it, and tapping it leads into an empty flow. We're spending our best slot to over-promise and then disappoint, on the exact results moment students care about most.

It only lives on the paid (Premium) home, so trial and free users are clear of it. Within paid, it's the school batches — Class 5 through 10, framed as a half-yearly certificate for 5–9 and a pre-test one for Class 10. HSC (11–12) has no half-yearly exam and doesn't show this today; that should stay true. We reproduced it on a Class 7 paid account with no result published.

The card should have to earn its place: show it only when there's a real result to open, and hide it completely when there isn't. When a result does exist, it should work exactly as intended. The whole bar here is simple — a paid student never sees "your certificate is ready" unless it actually is, and the students who do have one still get the full moment."""

tour = """This is the worst thing in the audit. A student finishes signup, starts their trial, lands on Home — and gets trapped. The "Discover Shikho" tour throws up a modal whose only working button is "Start tour." No skip, no close; back and tapping outside do nothing. The one person we paid to acquire, in the single moment they're most willing to engage, is stuck at a wall on their first screen. There is no faster way to lose them.

It's every non-paid user — free, trial, and lapsed — across every class including HSC, 100% of the time. Paid users never see it, so they're not in the picture. And there's no clever middle ground here: the exit is broken, and we can't ship a trap while we think about redesigning it.

So turn it off for everyone, now — a kill switch, not a redesign. The tour only comes back once it has a working Skip/Close, which is its own piece of work. What we're buying is simple: no non-paid user meets this tour on Home anymore, paid stays exactly as it is, back and tap-out behave normally, and nothing breaks or leaves a hole where the tour used to sit. Keep it reversible so the fixed version can return later."""

school = """If a user hasn't saved a school, Home greets them with a selection sheet they can't actually dismiss — the ✕ is drawn invisible and back doesn't close it — so to reach their own home they're forced through Division → District → School first. It's a hard wall for information we don't need before someone can start learning. And because the close is technically there but invisible, it's worse than an honest block: it just looks like the app is broken.

It isn't tied to any user type — paid, free, and trial all hit it the moment their school field is empty. Signup collects name, class, group and batch but never a school, so that's effectively every new account, on every home load, until they give in and pick one.

Take the wall down. Stop force-opening this sheet on Home for anyone and let people land on their home immediately. Collecting school is fine — just make it the voluntary thing it should be, where it already lives in Profile → Edit, instead of a toll gate on the front door. This is a temporary disable we can reverse if we ever redesign school collection with a real skip. Done right, nobody is forced into it on Home, Home is usable on first load, and the voluntary edit path still works."""

badge = """The gold "Premium" badge is supposed to mean "this person pays for Shikho right now." Today it means "this person isn't brand-new free" — so trial users wear it, and so do people whose paid course has expired and who are now back in the free/trial experience. We're handing out the status symbol to people who don't have the status.

Two groups get it wrongly: active trial users, and lapsed buyers whose access has ended. Active paying users see it correctly and should keep seeing it. The damage runs both ways — it misleads the user about what they currently have, and it quietly undercuts our own upsell, because Premium is a weaker thing to sell when half the non-payers already look Premium.

Tie the badge to reality: show it — and the matching crown on the avatar — only for a current, active, non-expired paid enrollment. Trial and expired users lose it; active paid keep it with no regression. And the badge and the crown should always tell the same story, since they're making the same claim."""

notif = """The "Notification" row in the Profile menu goes nowhere — tap it and you bounce straight back to Home, no screen, no feedback. The in-app notifications screen it used to open was removed, and the menu entry was left pointing at nothing. The "Settings" row right under it works fine, which only makes the dead one more obvious. Every logged-in user has this row, and we hit it four times during the audit without trying.

It's small, but it's the kind of small that makes people trust the app a little less — a visible button that does nothing reads as "this is held together with tape."

Pull the row for now; there's no working destination to send people to, and a clean menu beats a dead link. If we ever rebuild a real notifications screen, the row comes back pointing at it. The one thing to be careful about: this is only the in-app menu row. Push notifications — the ones in the system tray and their tap-through deep links — are a completely separate system that works, and must not be touched. Done means the dead row is gone (or opens something real), the rest of the Profile menu is untouched, and push keeps working exactly as it does now."""

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
