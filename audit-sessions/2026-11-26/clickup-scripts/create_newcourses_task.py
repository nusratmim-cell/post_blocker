# -*- coding: utf-8 -*-
import os, json, urllib.request
TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

# Body without image embeds yet; images get embedded after upload (two markers)
body = """### Problem
When a student's batch is fully over, the home shows a "Congratulations, course completed" card with a **"See new courses"** button. But it doesn't open a catalog of new courses — it just opens the **Course (আমার কোর্স)** tab, which shows the student's **old, already-finished enrollments**. For a returning student (say last year's SSC '25), there is no current batch to join anywhere on that screen, so the one button meant to move them forward loops back to dead, already-owned courses.

{{BUG_IMG2}}

### How to reproduce
1. Use an account whose enrolled batch has **fully ended** (e.g. a Class 10 / SSC '25 account from a past year, now enrolled only in finished batches).
2. Open the app and go to **Home (হোম)**.
3. On the "course completed" card, tap **"See new courses"**.
4. You land on the **Course (কোর্স)** tab — every course is marked "ভর্তি হয়েছো" (already enrolled), all old/finished batches.
5. There is no current or joinable batch anywhere — no way forward except searching/buying manually.

### Who's affected
* **Returning / continuing students whose enrolled batch has fully ended** — e.g. last year's SSC students who haven't moved to this year's batch. This is a **high-value re-enrollment group** (past payers), and the one button meant to re-sell them is broken.
* **Not affected: brand-new users** — their class is current, so this screen already shows real courses to join.

### Why it matters
This is our clearest re-enrollment moment — a student just finished a course and we're inviting them to continue. Instead we send them to a dead end and lose the easiest paid renewal we have, right when the student is most ready to continue.

### What we should do
Make the Course (কোর্স) tab show, in this order:
1. **Next courses (top):** the course(s) this student should move on to, based on their current/finished enrollment — using the promotion mapping below (current course → proposed next course). Some audiences map to more than one option (e.g. Class 8 → Class 9 Science / Humanities / Commerce), so show all of them as cards they can enroll in.
2. **Your courses (below):** their existing/finished enrollments as they are now, for reference and continued access.

{{MAP_IMG}}

This needs two parts:

**Backend (mapping source)**
* The current→next mapping changes every academic year, so it should live in the **backend as updatable data** (served through the Explore / course API), not hardcoded in the app — so it can be updated each year **without an app release**.
* Backend returns the proposed next course(s) for a student based on their current/finished enrollment (the audience → proposed-course rules in the sheet above).

**Android**
* The Course (কোর্স) tab renders a **"Next courses"** section on top (from the mapping API), then **"Your courses"** below.
* "See new courses" on the completed-course card lands here.
* Each "Next course" card opens that program's enroll / detail screen.

When done: a returning student taps "See new courses" (or opens the Course tab) and immediately sees the right next batch(es) to join on top, with their old courses below — no dead loop."""

payload = {
    "name": "[PROD][APP][Course]: \"See new courses\" is a dead loop for returning students — show their next courses first",
    "markdown_content": body,
    "priority": 2,
    "tags": ["sprint 10"],
}
req = urllib.request.Request(f"https://api.clickup.com/api/v2/list/{LIST_ID}/task",
    data=json.dumps(payload).encode(), headers={"Authorization":TOKEN,"Content-Type":"application/json"}, method="POST")
try:
    d=json.load(urllib.request.urlopen(req))
    print("OK", d.get("id"), d.get("url"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode()[:300])
