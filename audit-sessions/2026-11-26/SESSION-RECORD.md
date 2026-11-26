# Shikho UX Audit → ClickUp — Session Record

**Date:** 2026-11-26
**Owner:** Nusrat Alam Mim (nusrat.mim@shikho.com)
**App:** Shikho Android SuperApp (`tech.shikho.android`), prod build ~6.0.13
**Goal:** Turn UX-audit findings (from `proto/blocker-report.html`) into properly-written ClickUp tickets, one at a time, each verified against the tech spec (shikho-spec MCP) + codemap + live app.

---

## ClickUp context
- **Board (view):** https://app.clickup.com/24567161/v/b/qdqbt-61998
- **List it resolves to:** `901820156009` ("Sprint Backlog") — all tickets created here.
- **Tag on every ticket:** `sprint 10` · **Assignee:** none.
- **API note:** ClickUp API v2 has **no delete-attachment endpoint** (all variants 404) — attachments can only be removed manually in the UI.
- Tokens used this session were personal API tokens (rotated mid-session). **The saved transcript contains those tokens in plaintext** — treat `transcript/full-conversation.jsonl` as sensitive; rotate the token if this folder is ever shared.

---

## Tickets created (8) — Sprint 10

| # | Title | Priority | Link | Status |
|---|-------|----------|------|--------|
| 1 | Half-yearly certificate card appears when there's no result to show | Urgent | https://app.clickup.com/t/z8zyy1ujwy | Fix |
| 2 | Disable the inescapable "Discover Shikho" tour (no skip/close) for all users | Urgent | https://app.clickup.com/t/z8zyy1ujz7 | Disable |
| 3 | Disable the mandatory school-selection wall for all users | Urgent | https://app.clickup.com/t/z8zyy1uk1b | Disable |
| 4 | "Premium" badge shows for trial & expired users — limit to active paid | High | https://app.clickup.com/t/z8zyy1uk1u | Fix |
| 5 | Remove the dead "Notification" menu row (bounces to Home) | High | https://app.clickup.com/t/z8zyy1uqng | Remove |
| 6 | "Share location" popup is forced & repeats — show once, let people close it | High | https://app.clickup.com/t/z8zyy1ur0r | Fix |
| 7 | "See new courses" is a dead loop for returning students — show next courses first | High | https://app.clickup.com/t/z8zyy1urae | Fix (backend + Android) |
| 8 | Hide the empty "নতুন এক্টিভিটি শীঘ্রই দেখা যাবে" routine card when nothing is scheduled | Normal | https://app.clickup.com/t/z8zyy1urd5 | Hide |

---

## What each ticket says (verified mechanisms)

1. **Cert card** — On the paid (Premium) home, the top card promises "certificate ready / download or share" even when no half-yearly result exists → empty flow. Affects **paid students, Class 5–10** (5–9 half-yearly, 10 pre-test); **not HSC 11–12** (no half-yearly), not trial/free homes. Fix: show only when a real result/certificate exists.

2. **Forced tour** — Non-paid home opens the "Discover Shikho" tour modal that can't be dismissed (only "Start tour" works; back/tap-outside/✕ all fail). Affects **all non-paid** (free, trial, lapsed), every class incl. HSC; paid never see it. Worst blocker in the audit. Fix: kill switch now; reinstate only with a working skip/close.

3. **School wall** — With no saved school, home force-opens a school-selection sheet with an invisible ✕ and dead back → must pick Division→District→School to reach home. Affects **all user types**, effectively every new account (signup never collects school). Fix: stop force-opening; keep school optional in Profile → Edit.

4. **Premium badge** — Gold "প্রিমিয়াম" badge shows for anyone not brand-new-free: **trial users** and **expired/lapsed buyers** now in free/trial. Should track current active paid only. Fix: gate badge + avatar crown to active, non-expired paid; same rule for both.

5. **Notification row** — Profile menu "নোটিফিকেশন" row is dead (bounces to Home); its in-app inbox/notifications screen was removed. Affects every logged-in user. Fix: remove/hide the row. **Do NOT touch push notifications** (system tray + deep links = separate working system).

6. **Location popup** — First thing after login: full-screen "Share your location" card, only "Proceed", no ✕/skip/back; repeats until location captured. Affects all users, every new user; first popup on home. Fix: show once per account ever (regardless of accept/decline/close), add a real close, Proceed optional. (Side note: "for video quality optimization" copy is misleading — optional reword.)

7. **See new courses (dead loop)** — On the "course completed" card, "See new courses" opens the **My Courses tab**, scoped to the student's saved (stale, ended) class/batch, so it shows only old, already-enrolled, finished courses — no current batch. Affects **returning students whose batch has fully ended** (high-value re-enrollment / past payers); fresh users are fine. Fix (2 parts): **Backend** serves a current→next **course-mapping** as updatable data (the promotion table is embedded in the ticket as markdown); **Android** restructures the Course tab to show **Next courses** (from mapping) on top, **Your courses** below.

8. **Empty routine card** — The home রুটিন section (shows for **paid + trial** only; not free) displays a large empty "নতুন এক্টিভিটি শীঘ্রই দেখা যাবে" card when a day has nothing scheduled — permanent on skill courses (e.g. Spoken English, no routine). Boss asked to remove this empty part. Fix: hide the empty card; if the course has no routine at all → hide the whole section; if only the selected day is empty (academic) → keep the day strip, drop the empty card. Full Routine calendar ("সব দেখো") untouched.

---

## Ticket-writing style (locked in — see memory `ticket-writing-style`)
- **Five sections, in order:** `### Problem` → `### How to reproduce` (precise numbered steps) → `### Who's affected` → `### Why it matters` → `### What we should do`.
- **Plain English**, short sentences, no clever metaphors, no code internals (file/class/flag names, line numbers) in the body — verify against spec but keep it out of the ticket.
- **No** "Severity / Out of scope / Done when" sections, **no checkbox lists** (the user rejected these).
- **Impact must be spec-derived** (cohorts/classes/states), stated in product terms.
- **Evidence image** embedded right after the Problem (not at the very top) using the bare ClickUp attachment URL `https://t24567161.p.clickup-attachments.com/t24567161/<uuid>/<file>`.
- Prefer a **markdown table** over an attached screenshot for reference data (e.g. the course mapping).

---

## Pending audit findings (not yet ticketed)
From the 16 curated findings in `proto/blocker-report.html` — still open, e.g.:
- #6 Friction-to-dismiss tour exit (related to #2)
- #8 "Missed" recordings
- #9 Trial inherits blockers
- #11 False "course completed" card (the congratulations card itself)
- #12 Stranded on an expired batch
- #14 Course Progress 0% with a green "complete" tick
- #16 Move Routine to Explore
- Entry-popup gauntlet: the **notification-permission dialog** and the **full-screen promo** (only the location card was ticketed)
- Skill-course template mismatch (academic widgets on skill courses) + syllabus-change flow issues

---

## Files in this folder
- `SESSION-RECORD.md` — this file.
- `transcript/full-conversation.jsonl` — complete raw session conversation (~30 MB). **Contains API tokens — sensitive.**
- `clickup-scripts/` — every Python script used to create/update/rewrite the tickets.
- `course-mapping.png` — the current→next course promotion sheet (also transcribed as a table in ticket #7).

## Related project files (durable, outside this folder)
- `proto/blocker-report.html` — the source audit (16 findings + evidence).
- `proto/routine-section-analysis.html` — the "where/when is the Routine section seen" write-up.
- `proto/routine-section-shot.jpeg`, `proto/evidence/ev_*.jpg` — evidence screenshots.
