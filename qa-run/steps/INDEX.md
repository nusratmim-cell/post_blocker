# Shikho QA Run — Fresh account (01876287536), post-profile — step-by-step

Device: Pixel 7 · Account: nusrat QaTest · Class 8 · SSC'30 · Udayon Residential School
Severity: S1 Critical → S4 Low

| # | Screenshot | What it shows | Issue |
|---|---|---|---|
| 01 | login-otp | OTP verification | — |
| 02 | signup-step1-usertype | Student/Guardian select | — |
| 03 | signup-step1-student-selected | Student chosen, copy → informal | ok |
| 04 | signup-step2-personalinfo | name* + gender + class* | — |
| 05 | signup-step2-name-filter-test | name field strips digits/symbols | ok |
| 06 | success-popup BACK-TO-SCHOOL | promo popup on success screen | **S2 — no close button; only Back dismisses** |
| 07 | registration-success | "Congrats, registration complete" | — |
| 08 | home MANDATORY-SCHOOL-WALL | school sheet covers home | **S2 — hard wall, no skip** |
| 09 | school-division-dropdown | Division list | — |
| 10 | school-district-dropdown | District list | — |
| 11 | school-search | school name search | — |
| 12 | home-after-school CLASS MISMATCH | home loads | **S2 — Class 8 account sold Class 7 course** |
| 13 | home-full-salespage | 3-day free + buy ৳12,000 | sales page, no free content up front |
| 14 | course-detail-buy-page | Class 7 program, quarters, pricing | — |
| 15 | trial-activated call-16780 | trial on; "call 16780 to enrol" | telesales funnel |
| 16 | BLOCKER forced-tour | "Start tour" modal | **S1 — no skip, Back + outside-tap both fail; only "Start tour"** |
| 17 | tour-step-1of4 | coach-mark, "না, এখন নয়" appears | decline only AFTER starting |
| 18 | tour-exit-confirm friction | "exit tutorial?" | **S3 — exit demoted to text link** |
| 19 | trial-home | 4 tabs now; Premium badge on trial | S4 — misleading badge |
| 20 | course-tab | My Courses (trial) + Free courses | — |
| 21 | course-content-quarter4 | Q4, 8 subjects, 0% | — |
| 22 | math-subject | chapters, play buttons, no locks | — |
| 23 | chapter-lectures-missed | 5 recorded classes, "Missed" | — |
| 24 | lecture-detail-playable | teacher card + playable video | — |
| 25 | recorded-class-PLAYS | video loads/plays | **✓ not blocked — trial content plays** |

## Blockers summary
- **S1** — #16 Inescapable forced tour (no skip/back/outside-tap)
- **S2** — #06 popup no-close · #08 school hard-wall · #12 class mismatch (Class 8 → Class 7) · (root) invalid class+batch combo accepted at signup
- **S3** — #18 friction-to-dismiss tour
- **S4** — #19 trial "Premium" badge
- **✓ works** — #25 trial content access/playback
