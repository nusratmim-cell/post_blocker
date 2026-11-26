# Shikho Android — Post-Onboarding QA & Blocker Audit

**Scope:** Senior-QA blocker hunt on the Shikho EdTech **production** Android app, **after** profile completion (onboarding QA owned by another team).
**Device:** Physical Pixel 7 (1080×2400), prod build `tech.shikho.android`, driven over adb.
**Goal:** Find real blockers (not nitpicks) that break the "proper journey / feel-good" experience, per cohort. Capture every step as a screenshot. Ship a clickable deliverable.
**Last updated:** 2026-11-24

---

## 1. Deliverable

| What | Path | Notes |
|---|---|---|
| **Final report (open this)** | `proto/blocker-report.html` | Interactive phone-on-stage prototype, 16 curated findings, ‹ › stepper + arrow keys, ⤢ enlarge. Uses Shikho app colors (navy `#232C6A` / magenta `#E2008D` / primary `#5468FF`). |
| Live Artifact | `https://claude.ai/artifact/ABWerQVPyq4gb4PYcRqfaR` (v12) | Phone mockup enlarged; highlight rings scale by %. |
| **Evidence images (durable)** | `proto/evidence/*.jpg` | 36 JPEGs — the report's screenshots, copied out of scratchpad so they survive reboot/cleanup. |
| Earlier iterations | `proto/blockers.html`, `proto/clickable.html`, `proto/prototype.html` | Superseded style pivots, kept for reference. |
| Step-by-step QA run | `qa-run/steps/` (103 shots) + `qa-run/steps/INDEX.md` | Numbered 01–99 fresh-account walk-through. |
| Raw captures | `qa-run/shots/`, `screenshots/` | Unsorted adb captures. |

---

## 2. Cohorts explored

Pulled clean single-enrollment representatives from Metabase/Insight (`insight.shikho.com`). Content playback was **never** paywalled — it plays for every cohort; the damage is the surrounding "shell."

| Cohort | Account (internal PII) | What it represents |
|---|---|---|
| **Fresh** | QaTest (Class 8 · SSC'30) | Brand-new signup → trial activation path |
| **Trial** | 01712927705 | Trial user, academic course |
| **Paid** | (active paid, academic) | Currently-paying student |
| **Free / lapsed** | 01785347156 and others | Once-enrolled, now expired access (the true unpaid journey) |
| **HSC cross-check** | — | Confirmed forced-tour, telesales 16780, sales-page-home, Premium badge **all reproduce on HSC too → app-wide across classes** |

> Account numbers are real users' PII (incl. possible minors). Internal to this machine only — never share externally.

---

## 3. The 16 findings (exact, as shipped)

Severity: **S1** critical → **S3** low · **SPACE** = empty/hollow space · **REC** = recommendation.

| # | Sev | Scope | Finding | Evidence |
|---|---|---|---|---|
| 1 | S2 | app | **"View Certificate" button is dead** — prominent home card + arrow do nothing (paid & free). | `ev_cert.jpg` |
| 2 | S2 | app | **Entry popup gauntlet** — notification dialog + full-screen promo + misleading "Share location for video quality" (only "Proceed"). | `ev_location.jpg` |
| 3 | S3 | app | **"Premium" badge shown to lapsed buyers** — tied to lifetime purchase history, not current paid status. | `ev_congrats.jpg` |
| 4 | **S1** | fresh | **Inescapable forced tour** — "Start tour" modal, no skip/close; Back + outside-tap both fail. Reproduces on HSC. | `ev_tour.jpg` |
| 5 | S2 | fresh | **Mandatory school hard-wall** — school-selection sheet covers first home view, no skip. | `ev_wall.jpg` |
| 6 | S3 | fresh | **Friction-to-dismiss tour exit** — exit demoted to a text link; "keep watching" is primary (systemic, also on quiz-exit). | `ev_tourexit.jpg` |
| 7 | S3 | trial | **Trial user wears a "Premium" badge** — blurs trial vs paid. | `ev_trialprem.jpg` |
| 8 | S3 | trial | **Every recorded class tagged "Missed"** — greets a newcomer as already behind. | `ev_missed.jpg` |
| 9 | S2 | trial | **Inherits forced tour + popup gauntlet** — trial path runs the shared entry blockers. | (shared) |
| 10 | S3 | paid | **"Notification" menu row bounces back** — returns to home, no notifications screen (4 tries); "Settings" works. | `ev_notif.jpg` |
| 11 | S3 | free | **False "Congratulations! Course completed!"** — celebratory card while progress below reads 0%. | `ev_congrats.jpg` |
| 12 | S3 | free | **Stranded on an expired batch** — only "course" is an expired Model Test, 0 questions, no path forward. | `ev_expired.jpg` |
| 13 | S2 | free | **"See new courses" is a dead loop** — opens "My Courses" (same expired enrollments), not a catalog. | `ev_newcourses.jpg` |
| 14 | SPACE | app | **Course Progress 0% with a green "complete" tick** — card contradicts itself. | `ev_zeropct.jpg` |
| 15 | SPACE | app | **Empty Routine on home** — "your routine will be added soon", blank central block. | `ev_emptyrt.jpg` |
| 16 | REC | product | **Move Routine from Home → Explore** — content-first Home; Routine gains a purposeful home in Explore. | `ev_emptyrt.jpg` |

**Headline:** #4 (S1) inescapable forced tour is the worst — a brand-new, high-intent student is trapped with no escape.

---

## 4. Excluded (not in the final 16)

Per the user's keep-list, these were found but **deliberately excluded** from the deliverable:
- "View Report Card" (result button) **misrouted** — opens the Animated Lessons subject picker, not a report card (reproduced twice). Evidence: `ev_resultbug.jpg`, `ev_result.jpg`.
- "SSC'24" label-mismatch and wrong-default-class claims — **recanted** after the user showed the class switcher works in one tap; downgraded to minor.

---

## 5. Method & gotchas (for reproducing)

- adb loop: `adb exec-out screencap -p` · `adb shell input tap/swipe/keyevent` · `adb shell dumpsys window | grep mCurrentFocus`.
- **Compose gotcha:** `uiautomator dump` collapses element bounds to full-screen `[0,0][1080,2400]`. Precise taps must use **visual pixel estimates** from screenshots, verified by before/after md5 or a text peek.
- **Device dozing** → all-black screenshots (brightness 0, KeyguardShowing=true). Required the user to unlock.
- Metabase/Insight: native SQL vs database 2, tables `"Students"`, `academic_program_enrollment` (Paid/Trial/**FREE** = comped full access, not unpaid), `programs`, `program_phases`. The first "free" account was actually comped → re-queried for **zero active enrollment** to get the real unpaid journey.

## 6. Constraints honored
- Metabase admin session cookie = the user's own — first-party `insight.shikho.com` only, never shared externally.
- Student phone numbers (real minors' PII) surfaced **only to the user**.
- Never entered login PINs/OTPs — the user handled all auth. Never completed a purchase — buy/checkout only observed.
