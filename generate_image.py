from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1080, 1080
img = Image.new('RGB', (W, H), (10, 8, 18))
draw = ImageDraw.Draw(img)

# --- Background: deep romantic gradient (dark navy -> dark rose) ---
for y in range(H):
    t = y / H
    r = int(10 + t * 55)
    g = int(8 + t * 12)
    b = int(18 + t * 28)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Subtle vignette overlay
for y in range(H):
    for step in range(0, W, 4):
        cx, cy = W / 2, H / 2
        dx = (step - cx) / cx
        dy = (y - cy) / cy
        dist = math.sqrt(dx * dx + dy * dy)
        alpha = int(min(dist * 80, 80))
        current = img.getpixel((step, y))
        blended = tuple(max(0, c - alpha) for c in current)
        draw.line([(step, y), (step + 3, y)], fill=blended)

# --- Scattered small sparkles ---
import random
random.seed(42)
for _ in range(180):
    sx = random.randint(30, W - 30)
    sy = random.randint(30, H // 2)
    sr = random.choice([1, 1, 1, 2])
    brightness = random.randint(160, 255)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                 fill=(brightness, brightness - 20, brightness - 10))

# A few larger soft glowing dots
for (gx, gy, gr, gc) in [
    (120, 90,  18, (180, 80, 110)),
    (960, 140, 14, (140, 70, 130)),
    (200, 820, 12, (160, 60, 100)),
    (880, 800, 16, (150, 75, 120)),
    (540, 60,  10, (200, 100, 130)),
]:
    for r_step in range(gr, 0, -1):
        alpha = int(60 * (r_step / gr))
        color = tuple(min(255, c + alpha) for c in gc)
        draw.ellipse([gx - r_step, gy - r_step, gx + r_step, gy + r_step],
                     fill=color)

# ------------------------------------------------------------------ #
# BEAR  –  grey-white, long rabbit-like ears, romantic/sophisticated  #
# ------------------------------------------------------------------ #
bx, by = 540, 430   # bear center

def draw_rounded_shape(draw, cx, cy, rx, ry, color, outline=None, outline_w=3):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color, outline=outline, width=outline_w)

# ---- Long ears ----
ear_color      = (200, 195, 205)
ear_inner_color = (170, 110, 130)   # rosy inner ear
ear_w, ear_h   = 28, 110

for ex_off in [-52, 52]:
    ex = bx + ex_off
    ey = by - 115
    # outer ear
    draw.ellipse([ex - ear_w, ey - ear_h, ex + ear_w, ey + ear_h],
                 fill=ear_color, outline=(140, 135, 145), width=2)
    # inner ear blush
    draw.ellipse([ex - 13, ey - ear_h + 18, ex + 13, ey + ear_h - 18],
                 fill=ear_inner_color)

# ---- Head ----
head_r = 95
head_color = (215, 210, 220)
draw_rounded_shape(draw, bx, by, head_r, head_r, head_color,
                   outline=(170, 165, 175))

# ---- Muzzle ----
muzzle_color = (230, 225, 232)
draw.ellipse([bx - 38, by + 18, bx + 38, by + 72],
             fill=muzzle_color, outline=(180, 175, 185), width=2)

# ---- Eyes  – closed/sleepy romantic look ----
for ex_off in [-33, 33]:
    ex = bx + ex_off
    ey = by - 10
    # eye whites (very subtle)
    draw.ellipse([ex - 14, ey - 9, ex + 14, ey + 9], fill=(245, 242, 248))
    # closed eyelid – thick dark arc
    draw.arc([ex - 13, ey - 8, ex + 13, ey + 8], start=200, end=340,
             fill=(60, 45, 65), width=4)
    # small lash lines
    for lx, ly, angle in [
        (ex - 10, ey - 7, -40),
        (ex,      ey - 10, -90),
        (ex + 10, ey - 7, -140),
    ]:
        la = math.radians(angle)
        draw.line([(lx, ly), (lx + int(5 * math.cos(la)), ly + int(5 * math.sin(la)))],
                  fill=(60, 45, 65), width=2)

# ---- Nose ----
draw.ellipse([bx - 10, by + 28, bx + 10, by + 42],
             fill=(90, 60, 75), outline=(70, 45, 60), width=1)

# ---- Subtle mouth ----
draw.arc([bx - 14, by + 40, bx + 14, by + 58], start=10, end=170,
         fill=(120, 90, 100), width=2)

# ---- Cheek blushes ----
for cx_off in [-48, 48]:
    blush_x = bx + cx_off
    blush_y = by + 30
    for r_step in range(22, 0, -1):
        alpha = int(50 * (r_step / 22))
        draw.ellipse([blush_x - r_step, blush_y - r_step // 2,
                      blush_x + r_step, blush_y + r_step // 2],
                     fill=(220, 130, 150, alpha))

# ---- Body ----
body_color = (210, 205, 215)
draw.ellipse([bx - 75, by + 72, bx + 75, by + 200],
             fill=body_color, outline=(165, 160, 170), width=2)

# ---- Arms ----
arm_color = (205, 200, 210)
# left arm slightly raised
draw.ellipse([bx - 145, by + 95, bx - 65, by + 165],
             fill=arm_color, outline=(160, 155, 165), width=2)
# right arm
draw.ellipse([bx + 65, by + 95, bx + 145, by + 165],
             fill=arm_color, outline=(160, 155, 165), width=2)

# ---- Paws ----
paw_color = (220, 215, 225)
draw.ellipse([bx - 155, by + 148, bx - 68, by + 188],
             fill=paw_color, outline=(170, 165, 175), width=2)
draw.ellipse([bx + 68,  by + 148, bx + 155, by + 188],
             fill=paw_color, outline=(170, 165, 175), width=2)

# ---- Small tummy patch ----
draw.ellipse([bx - 32, by + 95, bx + 32, by + 165],
             fill=(228, 222, 232))

# ---- Legs/feet ----
for fx_off in [-35, 35]:
    draw.ellipse([bx + fx_off - 28, by + 188, bx + fx_off + 28, by + 215],
                 fill=paw_color, outline=(170, 165, 175), width=2)

# ------------------------------------------------------------------ #
# EMOJI  🤙  –  rendered via NotoColorEmoji                           #
# ------------------------------------------------------------------ #
emoji_font_path = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
try:
    efont = ImageFont.truetype(emoji_font_path, 72)
    draw.text((bx + 100, by + 150), '🤙', font=efont, embedded_color=True)
except Exception:
    # fallback: draw a simple hand glyph
    hx, hy = bx + 110, by + 155
    draw.ellipse([hx, hy, hx + 50, hy + 50], fill=(220, 180, 140))
    draw.text((hx + 5, hy + 8), '🤙', fill=(220, 180, 140))

# ------------------------------------------------------------------ #
# TEXT                                                                 #
# ------------------------------------------------------------------ #
serif_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

# Main caption
try:
    main_font = ImageFont.truetype(serif_font_path, 64)
except Exception:
    main_font = ImageFont.load_default()

text = 'Bedankt dat jij jij bent'
# soft glow behind text
for offset in range(8, 0, -1):
    glow_alpha = int(60 * (offset / 8))
    draw.text((W // 2, 730), text, font=main_font, fill=(200, 100, 130),
              anchor='mm', stroke_width=offset, stroke_fill=(200, 100, 130))

draw.text((W // 2, 730), text, font=main_font,
          fill=(245, 235, 245), anchor='mm')

# Decorative line above text
line_y = 695
line_color = (160, 90, 120)
draw.line([(W // 2 - 200, line_y), (W // 2 + 200, line_y)], fill=line_color, width=2)

# Small decorative hearts on the line
for hx_off in [-200, 200]:
    hcx = W // 2 + hx_off
    # tiny heart via two arcs + triangle
    hs = 8
    draw.ellipse([hcx - hs, line_y - hs, hcx,     line_y], fill=line_color)
    draw.ellipse([hcx,      line_y - hs, hcx + hs, line_y], fill=line_color)
    draw.polygon([(hcx - hs, line_y), (hcx + hs, line_y), (hcx, line_y + hs + 2)],
                 fill=line_color)

# Subtle subtitle
try:
    sub_font = ImageFont.truetype(serif_font_path, 30)
except Exception:
    sub_font = ImageFont.load_default()

draw.text((W // 2, 800), '♥', font=main_font, fill=(180, 80, 110), anchor='mm')

# ------------------------------------------------------------------ #
img.save('/home/user/BenTKB/bedankt_whatsapp.png', quality=95)
print('Saved: bedankt_whatsapp.png')
