#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

DEV = "/tmp/claude-1000/-home-shikho-Explore-shikho-ux-audit/e3eddc46-902c-44e9-83aa-f87dd1a1253c/scratchpad/dev"
OUT = "/home/shikho/Explore/shikho-ux-audit/proto/syllabus-and-skillcourse-issues.gif"

W = 560                     # target width
SCALE = W / 1080.0
BANNER_H = 250              # caption banner height
BG = (249, 248, 245)        # off-white
INK = (26, 29, 38)
INK2 = (75, 80, 96)
RED = (200, 40, 55)
GREEN = (30, 130, 70)
AMBER = (150, 95, 10)

def font(sz, bold=False):
    base = "/usr/share/fonts/truetype/dejavu/"
    p = base + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    if not os.path.exists(p):
        p = "/usr/share/fonts/truetype/liberation/" + ("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf")
    return ImageFont.truetype(p, sz)

F_TITLE = font(30, True)
F_SUB = font(19)
F_CAPN = font(21, True)
F_CAP = font(20)
F_CHIP = font(16, True)
F_NUM = font(22, True)

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def scalebox(b):
    return [int(v * SCALE) for v in b]

def chip(draw, xy, text, color):
    x, y = xy
    tw = draw.textlength(text, font=F_CHIP)
    draw.rounded_rectangle([x, y, x + tw + 20, y + 28], 8, fill=color)
    draw.text((x + 10, y + 5), text, font=F_CHIP, fill=(255, 255, 255))
    return tw + 20

def slide(img_name, box, num, cap_head, cap_body, verdict, vcolor):
    src = Image.open(os.path.join(DEV, img_name)).convert("RGB")
    src = src.resize((W, int(src.height * SCALE)))
    H = src.height + BANNER_H
    canvas = Image.new("RGB", (W, H), BG)
    canvas.paste(src, (0, 0))
    d = ImageDraw.Draw(canvas)
    if box:
        x0, y0, x1, y1 = scalebox(box)
        for i in range(4):  # thick outline
            d.rounded_rectangle([x0 - i, y0 - i, x1 + i, y1 + i], 10, outline=vcolor)
        # number badge
        bx, by = x0 - 6, y0 - 6
        d.ellipse([bx - 20, by - 20, bx + 20, by + 20], fill=vcolor)
        n = str(num)
        d.text((bx - d.textlength(n, font=F_NUM) / 2, by - 15), n, font=F_NUM, fill=(255, 255, 255))
    # banner
    by0 = src.height
    d.rectangle([0, by0, W, H], fill=BG)
    d.line([0, by0, W, by0], fill=(225, 222, 214), width=2)
    y = by0 + 16
    cw = chip(d, (18, y), verdict, vcolor)
    if num:
        d.text((18 + cw + 14, y + 3), f"Issue #{num}", font=F_CAPN, fill=INK)
    y += 40
    for ln in wrap(d, cap_head, F_CAPN, W - 36):
        d.text((18, y), ln, font=F_CAPN, fill=INK); y += 27
    for ln in wrap(d, cap_body, F_CAP, W - 36):
        d.text((18, y), ln, font=F_CAP, fill=INK2); y += 25
    return canvas

CARD_H = 1494   # must equal slide canvas height (1244 + 250 banner)

def textcard(title, lines, sub=None):
    H = CARD_H
    canvas = Image.new("RGB", (W, H), (24, 28, 44))
    d = ImageDraw.Draw(canvas)
    y = 480
    for ln in wrap(d, title, F_TITLE, W - 60):
        d.text(((W - d.textlength(ln, font=F_TITLE)) / 2, y), ln, font=F_TITLE, fill=(255, 255, 255)); y += 42
    y += 20
    if sub:
        for ln in wrap(d, sub, F_SUB, W - 70):
            d.text(((W - d.textlength(ln, font=F_SUB)) / 2, y), ln, font=F_SUB, fill=(174, 184, 243)); y += 28
    y += 20
    for ln in lines:
        for seg in wrap(d, ln, F_CAP, W - 80):
            d.text((40, y), seg, font=F_CAP, fill=(225, 228, 240)); y += 28
        y += 6
    return canvas

frames, durations = [], []

def add(img, ms):
    frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=128)); durations.append(ms)

# Title
add(textcard("Shikho App — UX Issues",
     ["Account: nus  (PROD build 6.0.13)",
      "Program: Spoken English (a skill course)",
      "Shown live on Pixel 7 via adb"],
     sub="Skill-course template mismatch + Syllabus-change flow"), 2600)

# Issue 1 — certificate card on skill course
add(slide("r4_reverted.png", (40,855,1040,1120), 1,
     "Academic 'result certificate' card on a SKILL course",
     "'See your certificate' belongs to academic classes — not Spoken English.",
     "BUG", RED), 3200)

# Issue 2 — academic widgets empty/0%
add(slide("s8_scroll.png", (55,1195,525,1640), 2,
     "Academic widgets are empty / 0% here",
     "Total Score 0%, Report Card, Course Progress 'Full course 0%' — inert on a skill course.",
     "BUG", RED), 3200)

# Issue 3 — empty routine
add(slide("r4_reverted.png", (40,1700,1040,2150), 3,
     "Empty 'Routine' (class 0 / exam 0)",
     "A blank class calendar sits in the middle of a Spoken English home.",
     "BUG", RED), 3000)

# Verified: Premium legit
add(slide("subs.png", (40,700,1040,840), 0,
     "Note: the 'Premium' badge is CORRECT here",
     "nus has an ACTIVE PAID enrollment (valid 31 Jan 2027) — verified in-app.",
     "VERIFIED OK", GREEN), 3000)

# Issue 4 — blank class list on syllabus change
add(slide("s3_change.png", (40,380,1040,1150), 4,
     "Change Syllabus: class list is BLANK for ~5s",
     "No loading spinner — the screen looks frozen before options appear.",
     "BUG", RED), 3000)

# Issue 5 — current class not preselected
add(slide("s3b_change.png", (40,490,1040,920), 5,
     "Your current class is NOT pre-selected",
     "You start from nothing each time — easy to mis-pick a class.",
     "BUG", AMBER), 3000)

# Issue 6a — class 8 batches
add(slide("s4_class8.png", (40,1030,1000,1210), 6,
     "Class 8 offers batches: 2027, 2028, 2029, 2030",
     "Batch isn't derived from class — raw year chips.",
     "BUG", RED), 3000)

# Issue 6b — class 7 batches overlap
add(slide("r2_class7.png", (40,1030,1000,1210), 6,
     "Class 7 offers: 2028, 2029, 2030, 2031",
     "'SSC 2029' is valid for BOTH Class 7 and Class 8 -> class/batch mismatch allowed.",
     "BUG", RED), 3400)

# Issue 7 — restart on change
add(slide("s6_proceed.png", (40,1830,1040,2150), 7,
     "Every syllabus change forces a full APP RESTART",
     "Confirming reloads the whole app.",
     "BUG", AMBER), 3000)

# Issue 8 — mismatch header after change
add(slide("s7_after.png", (40,435,900,515), 8,
     "After change: 'Class 8 · SSC 2029' on Spoken English",
     "Class/batch changed, but the Spoken English home is unchanged — academic template persists.",
     "BUG", RED), 3400)

# End card
add(textcard("Account restored",
     ["Reverted to the original:",
      "Class 7 · SSC 2029", "", "No data lost — paid enrollment intact."],
     sub=""), 2600)

assert all(f.size == frames[0].size for f in frames), [f.size for f in frames]
frames[0].save(OUT, save_all=True, append_images=frames[1:],
               duration=durations, loop=0, disposal=2, optimize=False)
print("WROTE", OUT, os.path.getsize(OUT), "bytes,", len(frames), "frames")
