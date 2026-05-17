from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

W, H = 1080, 1080
random.seed(42)

# ── 1. Warm sunset gradient background ─────────────────────────────
bg = Image.new('RGB', (W, H))
bg_draw = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    r = int(255)
    g = int(200 - t * 100)
    b = int(120 - t * 70)
    bg_draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 2. Bokeh layer ──────────────────────────────────────────────────
bokeh = Image.new('RGB', (W, H), (0, 0, 0))
bd = ImageDraw.Draw(bokeh)

def draw_bokeh_heart(draw, cx, cy, size, color):
    hw = size
    draw.ellipse([cx - hw, cy - hw // 2, cx,      cy + hw // 2], fill=color)
    draw.ellipse([cx,      cy - hw // 2, cx + hw,  cy + hw // 2], fill=color)
    draw.polygon([(cx - hw, cy + hw // 4),
                  (cx + hw, cy + hw // 4),
                  (cx, cy + hw + hw // 2)], fill=color)

# soft circle bokeh
for _ in range(80):
    bx = random.randint(0, W)
    by = random.randint(0, H)
    br = random.randint(18, 90)
    iv = random.randint(160, 255)
    c  = random.random()
    if   c < 0.30: col = (iv, iv - 10, 60)       # golden yellow
    elif c < 0.55: col = (iv, iv // 2 + 30, 60)  # warm orange
    elif c < 0.75: col = (iv, 130, 140)           # rose pink
    else:          col = (iv, iv, iv)             # white glow
    bd.ellipse([bx - br, by - br, bx + br, by + br], fill=col)

# heart-shaped bokeh
for _ in range(20):
    bx = random.randint(40, W - 40)
    by = random.randint(40, H - 40)
    bs = random.randint(12, 38)
    iv = random.randint(190, 255)
    draw_bokeh_heart(bd, bx, by, bs, (iv, 80, 110))

bokeh = bokeh.filter(ImageFilter.GaussianBlur(radius=30))
img   = Image.blend(bg, bokeh, alpha=0.45)
draw  = ImageDraw.Draw(img)

# ── 3. Extra warm vignette (edges slightly darker/richer) ───────────
vig = Image.new('RGB', (W, H), (0, 0, 0))
vd  = ImageDraw.Draw(vig)
for r in range(700, 0, -20):
    alpha = int(90 * (1 - r / 700))
    vd.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
               fill=(alpha, alpha // 4, alpha // 6))
img = Image.blend(img, vig, alpha=0.18)
draw = ImageDraw.Draw(img)

# ── 4. Floating hearts (sharp, crisp) ──────────────────────────────
def draw_heart(draw, cx, cy, size, color):
    hw = size
    draw.ellipse([cx - hw, cy - hw // 2, cx,      cy + hw // 2], fill=color)
    draw.ellipse([cx,      cy - hw // 2, cx + hw,  cy + hw // 2], fill=color)
    draw.polygon([(cx - hw, cy + hw // 4),
                  (cx + hw, cy + hw // 4),
                  (cx, cy + hw + hw // 2)], fill=color)

hearts = [
    (870, 190, 26, (220, 50, 80)),
    (920, 310, 16, (230, 80, 100)),
    (820, 390, 20, (200, 40, 70)),
    (160, 220, 18, (220, 60, 90)),
    (110, 370, 12, (230, 80, 100)),
    (950, 490, 14, (210, 50, 80)),
    (180, 560, 22, (220, 50, 80)),
    (850, 650, 10, (230, 90, 110)),
    (130, 720, 14, (215, 55, 85)),
]
for hx, hy, hs, hc in hearts:
    draw_heart(draw, hx, hy, hs, hc)
    # tiny glow
    for _ in range(3):
        draw_heart(draw,
                   hx + random.randint(-2, 2),
                   hy + random.randint(-2, 2),
                   hs - 6, (255, 160, 170))

# ── 5. BEAR ────────────────────────────────────────────────────────
bx, by = 560, 500

# shadow under bear
for sr in range(80, 0, -5):
    alpha = int(30 * (sr / 80))
    draw.ellipse([bx - sr, by + 200 - sr // 5,
                  bx + sr, by + 220 + sr // 5],
                 fill=(180, 100, 60))

# -- Long ears --
ear_col   = (215, 208, 218)
ear_in    = (195, 130, 145)   # warm rosy inner

for ex_off in [-58, 58]:
    ex = bx + ex_off
    ey = by - 125
    # outer ear
    draw.ellipse([ex - 30, ey - 115, ex + 30, ey + 105],
                 fill=ear_col, outline=(170, 162, 172), width=3)
    # inner ear
    draw.ellipse([ex - 14, ey - 95, ex + 14, ey + 85],
                 fill=ear_in)
    # ear highlight
    draw.ellipse([ex - 6, ey - 85, ex + 2, ey - 40],
                 fill=(230, 200, 210))

# -- Head --
head_r  = 100
hcol    = (222, 216, 226)
hcol_s  = (195, 188, 200)   # shadow side

# shadow side (slightly darker ellipse offset)
draw.ellipse([bx - head_r + 15, by - head_r,
              bx + head_r + 15, by + head_r],
             fill=hcol_s)
# main head
draw.ellipse([bx - head_r, by - head_r,
              bx + head_r, by + head_r],
             fill=hcol)
# highlight
draw.ellipse([bx - 55, by - 70, bx + 10, by - 15],
             fill=(240, 236, 244))

# -- Muzzle --
muz_col = (235, 228, 236)
draw.ellipse([bx - 42, by + 20, bx + 42, by + 78],
             fill=muz_col, outline=(185, 178, 188), width=2)
draw.ellipse([bx - 30, by + 25, bx + 5,  by + 55],
             fill=(242, 238, 245))   # muzzle highlight

# -- Eyes: warm sleepy/romantic --
for ex_off in [-36, 36]:
    ex = bx + ex_off
    ey = by - 12
    draw.ellipse([ex - 15, ey - 10, ex + 15, ey + 10], fill=(248, 244, 250))
    # closed eyelid arc
    draw.arc([ex - 14, ey - 9, ex + 14, ey + 9],
             start=195, end=345, fill=(55, 38, 55), width=5)
    # lashes
    for angle, length in [(-50, 6), (-90, 7), (-130, 6)]:
        la = math.radians(angle)
        draw.line([(ex + int(12 * math.cos(math.radians(angle + 180))),
                    ey + int(9  * math.sin(math.radians(angle + 180)))),
                   (ex + int((12 + length) * math.cos(math.radians(angle + 180))),
                    ey + int((9  + length) * math.sin(math.radians(angle + 180))))],
                  fill=(55, 38, 55), width=2)

# -- Nose --
draw.ellipse([bx - 11, by + 30, bx + 11, by + 44],
             fill=(100, 60, 72), outline=(75, 45, 58), width=1)
# -- Mouth --
draw.arc([bx - 16, by + 44, bx + 16, by + 60],
         start=15, end=165, fill=(130, 90, 105), width=2)

# -- Cheek blushes (warm rosy) --
for cx_off in [-52, 52]:
    for sr in range(26, 0, -2):
        alpha = int(55 * (sr / 26))
        r, g, b_ = 230, 120, 130
        blended = (min(255, r + alpha // 2), max(0, g - alpha // 4), max(0, b_ - alpha // 4))
        draw.ellipse([bx + cx_off - sr, by + 28 - sr // 2,
                      bx + cx_off + sr, by + 28 + sr // 2],
                     fill=blended)

# -- Body --
bcol = (218, 212, 222)
draw.ellipse([bx - 80, by + 78, bx + 80, by + 215],
             fill=(195, 188, 200))   # shadow
draw.ellipse([bx - 82, by + 75, bx + 75, by + 210],
             fill=bcol)
draw.ellipse([bx - 40, by + 82, bx + 20, by + 160],
             fill=(235, 230, 240))   # body highlight

# tummy patch
draw.ellipse([bx - 35, by + 100, bx + 35, by + 178],
             fill=(232, 226, 236))

# -- Arms --
acol = (213, 207, 218)
# left arm (slightly raised, welcoming)
draw.ellipse([bx - 155, by + 88, bx - 58, by + 165],
             fill=(195, 188, 200))
draw.ellipse([bx - 158, by + 85, bx - 62, by + 160],
             fill=acol)
# right arm
draw.ellipse([bx + 58, by + 90, bx + 155, by + 165],
             fill=(195, 188, 200))
draw.ellipse([bx + 60, by + 87, bx + 150, by + 160],
             fill=acol)

# paws
pcol = (228, 222, 232)
draw.ellipse([bx - 168, by + 152, bx - 62, by + 196],
             fill=pcol, outline=(175, 168, 178), width=2)
draw.ellipse([bx + 62,  by + 152, bx + 168, by + 196],
             fill=pcol, outline=(175, 168, 178), width=2)
# paw pads
for px_off in [-115, 115]:
    for pi, (ppo, ppsize) in enumerate([(-12, 7), (0, 8), (12, 7)]):
        draw.ellipse([bx + px_off + ppo - ppsize // 2, by + 170,
                      bx + px_off + ppo + ppsize // 2, by + 178],
                     fill=(195, 175, 185))

# legs
draw.ellipse([bx - 55, by + 200, bx - 5,  by + 230],
             fill=pcol, outline=(175, 168, 178), width=2)
draw.ellipse([bx + 5,  by + 200, bx + 55, by + 230],
             fill=pcol, outline=(175, 168, 178), width=2)

# small heart on bear's chest
heart_x, heart_y = bx - 8, by + 130
hs = 10
draw.ellipse([heart_x - hs, heart_y - hs // 2, heart_x,      heart_y + hs // 2], fill=(210, 70, 100))
draw.ellipse([heart_x,      heart_y - hs // 2, heart_x + hs, heart_y + hs // 2], fill=(210, 70, 100))
draw.polygon([(heart_x - hs, heart_y + hs // 4),
              (heart_x + hs, heart_y + hs // 4),
              (heart_x, heart_y + hs + hs // 2)], fill=(210, 70, 100))

# ── 6. Emoji 🤙 ─────────────────────────────────────────────────────
emoji_font_path = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
try:
    efont = ImageFont.truetype(emoji_font_path, 80)
    draw.text((bx - 195, by + 130), '🤙', font=efont, embedded_color=True)
except Exception:
    pass

# ── 7. TEXT ─────────────────────────────────────────────────────────
serif_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
serif_reg  = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

try:
    font_big  = ImageFont.truetype(serif_bold, 86)
    font_mid  = ImageFont.truetype(serif_bold, 86)
    font_name = ImageFont.truetype(serif_bold, 100)
except Exception:
    font_big = font_mid = font_name = ImageFont.load_default()

tx = 100   # left-aligned like reference

def draw_text_shadow(draw, pos, text, font, fill, shadow=(80, 40, 40), offset=4):
    draw.text((pos[0] + offset, pos[1] + offset), text, font=font, fill=shadow)
    draw.text(pos, text, font=font, fill=fill)

# "Bedankt"
draw_text_shadow(draw, (tx, 100), 'Bedankt', font_big,
                 fill=(35, 20, 25))

# "dat"
draw_text_shadow(draw, (tx, 188), 'dat', font_mid,
                 fill=(35, 20, 25))

# "jij jij"  – warm red/rose
draw_text_shadow(draw, (tx, 276), 'jij jij', font_name,
                 fill=(195, 40, 65), shadow=(100, 20, 30))

# "bent"
draw_text_shadow(draw, (tx, 378), 'bent', font_big,
                 fill=(35, 20, 25))

# small decorative heart after "bent"
try:
    bbox = draw.textbbox((tx, 378), 'bent', font=font_big)
    hafter_x = bbox[2] + 16
    draw_heart(draw, hafter_x, 420, 14, (195, 40, 65))
except Exception:
    pass

# ── 8. Save ────────────────────────────────────────────────────────
img.save('/home/user/BenTKB/bedankt_whatsapp.png', quality=96)
print('Saved.')
