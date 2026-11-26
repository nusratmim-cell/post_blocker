# -*- coding: utf-8 -*-
import os, json, urllib.request
TOKEN = os.environ["CU_TOKEN"]
LIST_ID = "901820156009"

body = """### Problem
On the Home screen, the রুটিন (Routine) section shows a big empty placeholder — **"নতুন এক্টিভিটি শীঘ্রই দেখা যাবে"** ("new activity will show up soon") — whenever the day has nothing scheduled. On skill courses like Spoken English, which never have a class routine, this empty card shows **permanently**, taking up the middle of the home for no reason.

{{IMG}}

### How to reproduce
1. Open the app with a **paid or trial** account enrolled in a course with no routine for the day — e.g. a skill course like **Spoken English (স্পোকেন ইংলিশ)**.
2. Go to the **Home (হোম)** tab.
3. In the **রুটিন** section, a day with nothing scheduled shows the empty card **"নতুন এক্টিভিটি শীঘ্রই দেখা যাবে"**.
4. On a skill course this never goes away — there is no routine to ever fill it.

### Who's affected
* **Paid and trial students** — the Routine section only shows for them; free / unenrolled users never see it.
* **Most visible on skill courses** (e.g. Spoken English) that have no routine at all — it is empty every single day. On academic programs it appears on off-days (days with no class or exam).

### Why it matters
It's dead space in the most valuable part of the home — a large empty card that promises activity and delivers nothing, and on skill courses it's there permanently.

### What we should do
* When a day has nothing scheduled, **don't show the empty "নতুন এক্টিভিটি শীঘ্রই দেখা যাবে" card** — hide it so the home flows straight to the next section.
* If the course has **no routine at all** (e.g. a skill course like Spoken English), hide the **whole Routine section** on home — header, day strip and all — since there's nothing to navigate to.
* If only the **selected day** is empty but the week still has classes on other days (academic programs), **keep the day strip** so the student can still reach those days; just drop the empty card.
* Leave the Routine section exactly as-is whenever there's real content (classes / exams). The full Routine calendar ("সব দেখো") is not touched.
* Reversible — this only hides an empty state; no data or navigation is removed."""

payload = {
    "name": "[PROD][APP][Home]: Hide the empty \"নতুন এক্টিভিটি শীঘ্রই দেখা যাবে\" routine card when nothing is scheduled",
    "markdown_content": body,
    "priority": 3,
    "tags": ["sprint 10"],
}
req = urllib.request.Request(f"https://api.clickup.com/api/v2/list/{LIST_ID}/task",
    data=json.dumps(payload).encode(), headers={"Authorization":TOKEN,"Content-Type":"application/json"}, method="POST")
try:
    d=json.load(urllib.request.urlopen(req)); print("OK", d.get("id"), d.get("url"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode()[:300])
