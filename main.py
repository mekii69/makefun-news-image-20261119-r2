#!/usr/bin/env python3
"""Thursday 19 November 2026 -- the whole day on one page.

A 1024 by 1024 newspaper front page drawn with nothing but the Python
standard library, so the program runs offline and renders the same bytes
on every machine. Three generated flat illustrations (summit, world
court, COP31) arrive as raw RGB under zlib; the ten small pictures and
the world map are drawn by hand in code; every letter on the page is set
in a small 5-by-7 bitmap face defined below.

The day, as reported on Thursday 19 November 2026 (each item checked
against a live source the same morning it was drawn):
  BIG 1  Trump, Xi and Putin hold the first three-way summit, APEC
         Shenzhen; 90 minutes, nuclear war "must never be fought".
  BIG 2  The World Court finds Myanmar committed genocide against the
         Rohingya, 9-6; reparations ordered.
  BIG 3  COP31's slimmed draft drops fossil fuels and the $120bn aid
         figure; 144 paragraphs become 80.
  4-13   Kerch Bridge hit a third time in a week; Houthi missiles over
         Riyadh shot down; Cyclone Akvan nears Odisha; Seoul's top
         court clears ex-PM Han; Denmark backs the Arctic pact 109-0;
         Anthropic starts trading on Nasdaq; GTA VI goes on sale;
         Colombia's unions strike; Jepchirchir banned three years;
         Australia's jobless rate hits 4.9%.
  14-33  Twenty one-line briefs, each with its place and its source.
Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC,
RNZ, Xinhua, NDTV, IMD, MEA, PIB, Premium Times, WION, Ukrinform.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024
ART_W, ART_H = 325, 217

# ------------------------------------------------------------ letter face --
# A glyph is seven rows of five dots. Each row is one byte written as two
# hex digits; the top row comes first and the leftmost dot is the high
# bit. Only the capitals, figures and marks this page actually sets.
FACE = {
    "A": "0E11111F111111", "B": "1E11111E11111E", "C": "0E11101010110E",
    "D": "1E11111111111E", "E": "1F10101E10101F", "F": "1F10101E101010",
    "G": "0E11101711110F", "H": "1111111F111111", "I": "0E04040404040E",
    "J": "0702020202120C", "K": "11121418141211", "L": "1010101010101F",
    "M": "111B1515111111", "N": "11191513111111", "O": "0E11111111110E",
    "P": "1E11111E101010", "Q": "0E11111115120D", "R": "1E11111E141211",
    "S": "0F10100E01011E", "T": "1F040404040404", "U": "1111111111110E",
    "V": "11111111110A04", "W": "11111115151B11", "X": "11110A040A1111",
    "Y": "11110A04040404", "Z": "1F01020408101F",
    "0": "0E11131519110E", "1": "040C040404040E", "2": "0E11010608101F",
    "3": "1F02040201110E", "4": "02060A121F0202", "5": "1F101E0101110E",
    "6": "0608101E11110E", "7": "1F010204080808", "8": "0E11110E11110E",
    "9": "0E11110F01020C",
    " ": "00000000000000", ".": "00000000000C0C", ",": "000000000C0408",
    ":": "000C0C000C0C00", ";": "000C0C000C0408", "-": "0000001F000000",
    "'": "04040800000000", "$": "040F140E051E04", "%": "19020508121419",
    "(": "02040404040200", ")": "08040404040800", "/": "01020408102040",
    "!": "04040404040004", "?": "0E110106040004",
}

# ---------------------------------------------------------------- colours --
PAPER = (246, 240, 228)
INK = (22, 28, 40)
NAVY = (16, 32, 60)
GOLD = (198, 160, 40)
RED = (176, 32, 32)
BRICK = (190, 70, 45)
CREAM = (253, 251, 246)
GREY = (118, 124, 136)
STEEL = (70, 86, 110)
OCEAN = (24, 90, 140)
TEAL = (16, 110, 110)
SKY = (140, 180, 205)
SAND = (232, 214, 170)
PINE = (40, 110, 60)
ROSE = (214, 90, 140)
AMBER = (224, 164, 60)


# ----------------------------------------------------------------- canvas --
class Canvas:
    """A flat RGB sheet plus the few strokes needed to draw on it."""

    def __init__(self, ww, hh, bg):
        self.w, self.h = ww, hh
        self.buf = bytearray(bytes(bg) * (ww * hh))

    def _at(self, xx, yy):
        return (yy * self.w + xx) * 3

    def box(self, ox, oy, ww, hh, col):
        x0, y0 = max(0, ox), max(0, oy)
        x1, y1 = min(self.w, ox + ww), min(self.h, oy + hh)
        if x1 <= x0 or y1 <= y0:
            return
        run = bytes(col) * (x1 - x0)
        for yy in range(y0, y1):
            o = self._at(x0, yy)
            self.buf[o:o + len(run)] = run

    def frame(self, ox, oy, ww, hh, col, th=2):
        self.box(ox, oy, ww, th, col)
        self.box(ox, oy + hh - th, ww, th, col)
        self.box(ox, oy, th, hh, col)
        self.box(ox + ww - th, oy, th, hh, col)

    def line(self, x0, y0, x1, y1, col, th=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        xx, yy = x0, y0
        while True:
            self.box(xx, yy, th, th, col)
            if xx == x1 and yy == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                xx += sx
            if e2 < dx:
                err += dx
                yy += sy

    def dot(self, cx, cy, r, col):
        for yy in range(-r, r + 1):
            half = int(math.sqrt(r * r - yy * yy))
            self.box(cx - half, cy + yy, 2 * half + 1, 1, col)

    def oval(self, cx, cy, rx, ry, col):
        for yy in range(-ry, ry + 1):
            half = int(rx * math.sqrt(max(0.0, 1.0 - (yy * yy) / (ry * ry))))
            self.box(cx - half, cy + yy, 2 * half + 1, 1, col)

    def poly(self, pts, col):
        ys = [p[1] for p in pts]
        for yy in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            for i in range(len(pts)):
                ax, ay = pts[i]
                bx, by = pts[(i + 1) % len(pts)]
                if (ay <= yy < by) or (by <= yy < ay):
                    xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.box(int(xs[i]), yy, int(xs[i + 1]) - int(xs[i]) + 1, 1, col)

    def blit(self, raw, ww, hh, ox, oy):
        for row in range(hh):
            o = self._at(ox, oy + row)
            s = row * ww * 3
            self.buf[o:o + ww * 3] = raw[s:s + ww * 3]

    def text(self, s, ox, oy, k, col):
        s = s.upper()
        cx = ox
        for ch in s:
            rows = FACE.get(ch, FACE[" "])
            for r in range(7):
                bits = int(rows[2 * r:2 * r + 2], 16)
                for c, bit in enumerate(f"{bits:05b}"):
                    if bit == "1":
                        self.box(cx + c * k, oy + r * k, k, k, col)
            cx += 6 * k
        return len(s) * 6 * k - k if s else 0

    def text_w(self, s, k):
        return len(s) * 6 * k - k if s else 0

    def text_c(self, s, cx, oy, k, col):
        self.text(s, cx - self.text_w(s, k) // 2, oy, k, col)


# ------------------------------------------------------------ small scenes --
# Each picture fills a 192 by 96 box at (ox, oy), in the same flat style
# as the generated art: bold shapes, cream, navy, rust, ochre.

def sc_bridge(cv, ox, oy):
    cv.box(ox, oy, 192, 96, SKY)
    cv.box(ox, oy + 66, 192, 30, OCEAN)
    cv.box(ox, oy + 60, 192, 6, STEEL)
    for tx in (44, 142):
        cv.box(ox + tx, oy + 22, 8, 40, STEEL)
    cv.line(ox + 48, oy + 24, ox + 96, oy + 52, STEEL, 2)
    cv.line(ox + 96, oy + 52, ox + 144, oy + 24, STEEL, 2)
    for sx in (64, 80, 96, 112, 128):
        cv.line(ox + sx, oy + 44, ox + sx, oy + 60, STEEL, 2)
    cv.dot(ox + 96, oy + 52, 7, RED)
    for dx, dy in ((-12, -6), (12, -8), (-10, 8), (11, 7)):
        cv.line(ox + 96, oy + 52, ox + 96 + dx, oy + 52 + dy, RED, 2)


def sc_missiles(cv, ox, oy):
    cv.box(ox, oy, 192, 96, NAVY)
    for sx, sy in ((20, 14), (60, 26), (120, 12), (160, 30), (90, 8)):
        cv.dot(ox + sx, oy + sy, 2, CREAM)
    for bx in (10, 50, 90, 130, 168):
        cv.box(ox + bx, oy + 62, 16, 34, STEEL)
    cv.line(ox + 30, oy + 40, ox + 70, oy + 70, GOLD, 3)
    cv.line(ox + 160, oy + 36, ox + 120, oy + 68, GOLD, 3)
    cv.dot(ox + 96, oy + 46, 8, RED)
    for dx, dy in ((-14, -8), (14, -9), (-13, 9), (13, 8)):
        cv.line(ox + 96, oy + 46, ox + 96 + dx, oy + 46 + dy, RED, 2)


def sc_cyclone(cv, ox, oy):
    cv.box(ox, oy, 192, 96, SKY)
    cv.box(ox, oy + 74, 192, 22, (120, 150, 110))
    for r, a0 in ((34, 0), (26, 60), (18, 120), (10, 200)):
        for a in range(a0, a0 + 220, 12):
            rad = math.radians(a)
            cv.dot(ox + 96 + int(r * math.cos(rad)),
                   oy + 46 + int(r * 0.7 * math.sin(rad)), 3, CREAM)
    cv.dot(ox + 96, oy + 46, 5, RED)
    cv.box(ox + 150, oy + 74, 42, 22, SAND)


def sc_gavel(cv, ox, oy):
    cv.box(ox, oy, 192, 96, (235, 225, 200))
    for cx in (30, 80, 130, 175):
        cv.box(ox + cx - 5, oy + 22, 10, 56, CREAM)
        cv.box(ox + cx - 7, oy + 78, 14, 6, STEEL)
    cv.box(ox, oy + 14, 192, 8, STEEL)
    cv.line(ox + 60, oy + 66, ox + 130, oy + 30, (120, 84, 52), 7)
    cv.box(ox + 118, oy + 18, 34, 16, (120, 84, 52))
    cv.box(ox + 52, oy + 60, 30, 10, (120, 84, 52))


def sc_mountains(cv, ox, oy):
    cv.box(ox, oy, 192, 96, SKY)
    cv.poly([(ox, oy + 96), (ox + 40, oy + 30), (ox + 80, oy + 96)], STEEL)
    cv.poly([(ox + 60, oy + 96), (ox + 110, oy + 18), (ox + 160, oy + 96)],
            (90, 110, 140))
    cv.poly([(ox + 100, oy + 18), (ox + 110, oy + 30), (ox + 120, oy + 18)],
            CREAM)
    cv.box(ox, oy + 78, 192, 18, CREAM)
    cv.line(ox + 30, oy + 78, ox + 30, oy + 40, (120, 84, 52), 3)
    cv.box(ox + 18, oy + 40, 24, 16, RED)
    cv.box(ox + 18, oy + 40, 24, 6, CREAM)


def sc_chart(cv, ox, oy):
    cv.box(ox, oy, 192, 96, (215, 230, 215))
    for k, bh in enumerate((16, 26, 40, 58)):
        cv.box(ox + 26 + k * 30, oy + 88 - bh, 20, bh, OCEAN)
    cv.line(ox + 16, oy + 80, ox + 150, oy + 16, RED, 4)
    cv.line(ox + 150, oy + 16, ox + 132, oy + 18, RED, 4)
    cv.line(ox + 150, oy + 16, ox + 148, oy + 34, RED, 4)
    cv.box(ox + 158, oy + 20, 26, 18, INK)
    cv.box(ox + 162, oy + 24, 18, 10, TEAL)


def sc_gamepad(cv, ox, oy):
    cv.box(ox, oy, 192, 96, (30, 20, 50))
    cv.dot(ox + 150, oy + 26, 16, ROSE)
    for bx, bh in ((8, 44), (44, 62), (84, 40), (120, 58), (156, 34)):
        cv.box(ox + bx, oy + 88 - bh, 28, bh, (60, 60, 120))
    cv.box(ox, oy + 88, 192, 3, GOLD)
    cv.box(ox + 62, oy + 52, 68, 26, (40, 40, 70))
    cv.box(ox + 70, oy + 58, 14, 14, CREAM)
    cv.dot(ox + 108, oy + 65, 4, RED)
    cv.dot(ox + 122, oy + 65, 4, GOLD)


def sc_crowd(cv, ox, oy):
    cv.box(ox, oy, 192, 96, (235, 225, 200))
    for hx, col in ((30, RED), (60, OCEAN), (90, TEAL), (120, BRICK),
                    (150, PINE), (175, STEEL)):
        cv.dot(ox + hx, oy + 56, 9, col)
        cv.oval(ox + hx, oy + 86, 14, 12, col)
    cv.box(ox + 66, oy + 14, 60, 26, CREAM)
    cv.frame(ox + 66, oy + 14, 60, 26, INK, 2)
    cv.line(ox + 96, oy + 40, ox + 96, oy + 58, (120, 84, 52), 3)


def sc_runner(cv, ox, oy):
    cv.box(ox, oy, 192, 96, (215, 230, 215))
    cv.box(ox, oy + 72, 192, 24, BRICK)
    for lx in range(0, 192, 24):
        cv.box(ox + lx, oy + 82, 12, 3, CREAM)
    cv.dot(ox + 90, oy + 34, 7, INK)
    cv.line(ox + 90, oy + 42, ox + 78, oy + 58, INK, 4)
    cv.line(ox + 78, oy + 58, ox + 66, oy + 72, INK, 4)
    cv.line(ox + 90, oy + 42, ox + 104, oy + 56, INK, 4)
    cv.line(ox + 104, oy + 56, ox + 118, oy + 72, INK, 4)
    cv.line(ox + 90, oy + 46, ox + 108, oy + 38, INK, 4)
    cv.line(ox + 90, oy + 46, ox + 74, oy + 36, INK, 4)
    cv.line(ox + 40, oy + 20, ox + 150, oy + 74, RED, 5)


def sc_jobless(cv, ox, oy):
    cv.box(ox, oy, 192, 96, (235, 225, 200))
    for k, bh in enumerate((52, 42, 30, 18)):
        cv.box(ox + 26 + k * 30, oy + 88 - bh, 20, bh, STEEL)
    cv.line(ox + 16, oy + 28, ox + 150, oy + 76, RED, 4)
    cv.line(ox + 150, oy + 76, ox + 132, oy + 74, RED, 4)
    cv.line(ox + 150, oy + 76, ox + 148, oy + 58, RED, 4)
    for hx in (160, 178):
        cv.dot(ox + hx, oy + 56, 7, OCEAN)
        cv.oval(ox + hx, oy + 82, 11, 10, OCEAN)


# ------------------------------------------------------------------- map ---
# Rough continent outlines in (longitude, latitude); drawn on an
# equirectangular grid, good enough to read at 320 by 150.
LAND = {
    "north_america": [(-168, 66), (-150, 70), (-130, 71), (-115, 73),
                      (-100, 72), (-88, 72), (-80, 73), (-72, 68),
                      (-65, 60), (-58, 50), (-55, 47), (-62, 45),
                      (-70, 42), (-75, 35), (-81, 31), (-88, 29),
                      (-97, 26), (-105, 22), (-112, 25), (-118, 32),
                      (-124, 42), (-128, 52), (-140, 60), (-152, 59),
                      (-162, 58), (-168, 66)],
    "south_america": [(-79, 9), (-77, 4), (-80, -4), (-81, -10),
                      (-77, -18), (-71, -24), (-70, -32), (-67, -40),
                      (-66, -48), (-68, -54), (-62, -52), (-58, -42),
                      (-52, -32), (-46, -26), (-40, -20), (-35, -8),
                      (-38, -3), (-45, -1), (-52, 4), (-58, 7),
                      (-65, 10), (-72, 11), (-79, 9)],
    "europe": [(-10, 36), (-9, 43), (-2, 44), (0, 47), (4, 50), (8, 54),
               (9, 58), (14, 58), (19, 60), (24, 63), (29, 69),
               (35, 68), (40, 64), (38, 57), (34, 51), (30, 46),
               (27, 43), (23, 40), (19, 40), (15, 38), (11, 38),
               (6, 37), (0, 38), (-5, 36), (-10, 36)],
    "africa": [(-10, 31), (-5, 35), (2, 36), (11, 37), (18, 33),
               (25, 32), (31, 31), (35, 28), (39, 22), (43, 14),
               (48, 11), (51, 10), (48, 2), (42, -6), (40, -14),
               (36, -20), (33, -27), (28, -33), (21, -35), (17, -32),
               (14, -24), (12, -16), (10, -5), (9, 0), (6, 5),
               (-2, 5), (-8, 5), (-13, 8), (-16, 12), (-15, 18),
               (-13, 25), (-10, 31)],
    "asia": [(38, 68), (48, 72), (60, 73), (72, 74), (85, 76),
             (98, 77), (110, 77), (122, 74), (135, 72), (148, 71),
             (160, 69), (172, 66), (178, 65), (170, 61), (162, 58),
             (154, 52), (146, 44), (140, 41), (132, 38), (127, 35),
             (121, 30), (114, 23), (109, 18), (105, 10), (101, 6),
             (98, 10), (94, 17), (90, 22), (86, 20), (81, 14),
             (78, 8), (75, 12), (72, 20), (68, 24), (62, 25),
             (57, 26), (52, 28), (49, 30), (45, 31), (41, 35),
             (38, 39), (35, 42), (32, 45), (29, 48), (26, 51),
             (23, 54), (20, 57), (17, 60), (14, 63), (11, 66),
             (8, 69), (5, 70), (2, 69), (0, 68), (38, 68)],
    "greenland": [(-58, 64), (-54, 68), (-50, 71), (-44, 73),
                  (-36, 75), (-28, 76), (-21, 74), (-20, 69),
                  (-24, 65), (-30, 63), (-38, 61), (-46, 60),
                  (-54, 61), (-58, 64)],
    "oceania": [(113, -22), (115, -32), (119, -35), (124, -33),
                (130, -32), (135, -34), (140, -38), (146, -39),
                (150, -37), (153, -28), (150, -22), (146, -19),
                (142, -15), (137, -12), (131, -12), (126, -14),
                (121, -16), (116, -20), (113, -22)],
}

# Story number -> (longitude, latitude) for the map pins.
PINS = [(1, 114, 22), (2, 4.5, 52), (3, 30.7, 36.9), (4, 36.5, 45.3),
        (5, 46.7, 24.6), (6, 85, 20), (7, 127, 37.5), (8, -42, 72),
        (9, -74, 40.7), (10, -80, 26), (11, -74, 4.6), (12, 36.8, -1.3),
        (13, 149, -35.3)]


def draw_map(cv, ox, oy, ww, hh):
    cv.box(ox, oy, ww, hh, (185, 210, 225))
    cv.frame(ox, oy, ww, hh, INK, 2)
    for name, pts in LAND.items():
        proj = [(ox + int((lo + 170) / 360 * ww),
                 oy + int((75 - la) / 130 * hh)) for lo, la in pts]
        cv.poly(proj, SAND)
    for num, lo, la in PINS:
        px = ox + int((lo + 170) / 360 * ww)
        py = oy + int((75 - la) / 130 * hh)
        cv.dot(px, py, 7, RED)
        cv.text(str(num), px - 3 if num < 10 else px - 6, py - 3, 1, CREAM)


# ------------------------------------------------------------------ data ---
# (number, kicker, headline line 1, headline line 2, brief line 1,
#  brief line 2, art file)
BIG = [
    (1, "SHENZHEN - SUMMIT", "TRUMP, XI, PUTIN", "HOLD FIRST SUMMIT",
     "The three leaders meet for 90 minutes in Shenzhen",
     "and vow nuclear war must never be fought. AP",
     "art_summit.bin"),
    (2, "THE HAGUE - JUSTICE", "WORLD COURT FINDS", "MYANMAR GUILTY",
     "By 9 votes to 6 the ICJ finds Myanmar guilty",
     "over the Rohingya and orders reparations. - UN News",
     "art_court.bin"),
    (3, "ANTALYA - CLIMATE", "COP31 DRAFT DROPS", "FOSSIL FUELS",
     "The slimmed text, 144 paras to 80, names no fuel",
     "and no aid figure. Talks end Friday. - Reuters",
     "art_cop31.bin"),
]

# (number, kicker, headline line 1, headline line 2, one-line brief, scene)
SMALL = [
    (4, "KERCH BRIDGE", "UKRAINE HITS", "BRIDGE AGAIN",
     "Third strike in a week. AP", sc_bridge),
    (5, "OVER RIYADH", "SAUDIS DOWN", "HOUTHI MISSILES",
     "Debris falls, none hurt. AP", sc_missiles),
    (6, "ODISHA STORM", "CYCLONE AKVAN", "NEARS INDIA",
     "50,000 evacuated. IMD", sc_cyclone),
    (7, "SEOUL JUSTICE", "COURT CLEARS", "EX-PM HAN",
     "Martial-law verdict void. AP", sc_gavel),
    (8, "GREENLAND SECURITY", "DENMARK BACKS", "ARCTIC PACT",
     "109-0 vote; two new bases. AP", sc_mountains),
    (9, "NEW YORK MARKETS", "ANTHROPIC ON", "NASDAQ: ANT",
     "Opens $111.50, up 34%. AP", sc_chart),
    (10, "WORLDWIDE GAMES", "GTA VI GOES", "ON SALE",
     "13-year wait ends. ABC", sc_gamepad),
    (11, "BOGOTA LABOUR", "COLOMBIA'S", "UNIONS STRIKE",
     "Marches in five cities. CUT", sc_crowd),
    (12, "NAIROBI SPORT", "MARATHON CHAMP", "BANNED 3 YEARS",
     "Jepchirchir took EPO. Reuters", sc_runner),
    (13, "CANBERRA ECONOMY", "AUSTRALIA'S", "JOBLESS 4.9%",
     "Highest since 2021. Reuters", sc_jobless),
]

# One line each: number, place, what happened, source.
BRIEFS = [
    "14 Shenzhen CEOs issue Shenzhen Initiative. Xinhua",
    "15 Shenzhen: Xi urges free, open trade. Al Jazeera",
    "16 Tokyo: PM Takaichi makes first China visit. WION",
    "17 Seoul: President Lee attends APEC. Xinhua",
    "18 Ottawa: Canada, China extend trade talks. Reuters",
    "19 Manila: ASEAN ends; chair to Singapore. PIB",
    "20 Phuket: Fire kills 11; rescue under way. NDTV",
    "21 Tehran: Iran refuses UN nuclear inspection. Reuters",
    "22 Abuja: Nigeria gets US intel support. Reuters",
    "23 Zamfara: Police free 20 abducted. Premium Times",
    "24 Cairo: Egypt, India agree trade working group. PIB",
    "25 New York: Outages hit banks, airlines. Econ Times",
    "26 Washington: Mail-vote order partly stands. Reuters",
    "27 Berlin: Coalition of the Willing meets. Ukrinform",
    "28 Odesa: Russia hits energy sites. Reuters",
    "29 London: Germany, UK spurn Pentagon line. Reuters",
    "30 Kyiv: Zelensky talks aid with partners. Ukrinform",
    "31 Vienna: Rwanda in EU return-hub talks. Reuters",
    "32 Tokyo: India, Japan hold 2+2 defence dialogue. MEA",
    "33 Delhi: Prince, Princess of Wales meet PM Modi. PIB",
]

REGIONS = [("ASIA", 11, (176, 90, 40)), ("MIDDLE EAST", 3, TEAL),
           ("EUROPE", 7, NAVY), ("AFRICA", 5, PINE),
           ("AMERICAS", 5, (150, 110, 30)), ("OCEANIA", 1, OCEAN),
           ("GLOBAL", 1, GREY)]

STATS = [("3", "PRESIDENTS AT ONE TABLE"), ("9-6", "WORLD COURT VOTE"),
         ("$120BN", "AID GOAL CUT"), ("$81BN", "ANTHROPIC IPO"),
         ("109-0", "DANISH ARCTIC VOTE"), ("4.9%", "AUSTRALIAN JOBLESS")]


# ---------------------------------------------------------------- layout ---
def load_art(name):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, name), "rb") as fh:
        return zlib.decompress(fh.read())


def big_story(cv, ox, oy, item):
    num, kick, h1, h2, b1, b2, art = item
    cv.box(ox, oy, 325, 308, CREAM)
    cv.frame(ox, oy, 325, 308, INK, 2)
    cv.blit(load_art(art), ART_W, ART_H, ox + 1, oy + 1)
    cv.dot(ox + 16, oy + 232, 10, RED)
    cv.text(str(num), ox + 13 if num < 10 else ox + 10, oy + 229, 1, CREAM)
    cv.text(kick, ox + 32, oy + 226, 2, RED)
    cv.text(h1, ox + 10, oy + 242, 3, INK)
    cv.text(h2, ox + 10, oy + 264, 3, INK)
    cv.text(b1, ox + 10, oy + 288, 1, INK)
    cv.text(b2, ox + 10, oy + 298, 1, GREY)


def small_story(cv, ox, oy, item):
    num, kick, h1, h2, brief, scene = item
    cv.box(ox, oy, 192, 163, CREAM)
    cv.frame(ox, oy, 192, 163, INK, 2)
    scene(cv, ox + 1, oy + 1)
    cv.dot(ox + 12, oy + 106, 8, RED)
    cv.text(str(num), ox + 9 if num < 10 else ox + 6, oy + 103, 1, CREAM)
    cv.text(kick, ox + 24, oy + 104, 1, RED)
    cv.text(h1, ox + 8, oy + 118, 2, INK)
    cv.text(h2, ox + 8, oy + 134, 2, INK)
    cv.text(brief, ox + 8, oy + 152, 1, GREY)


def compose():
    cv = Canvas(W, H, PAPER)
    # Masthead.
    cv.text_c("Thursday 19 November 2026", W // 2, 6, 6, INK)
    cv.text("TRUMP, XI AND PUTIN SHARE ONE TABLE", 16, 50, 2, RED)
    right = "33 STORIES - EVERY CONTINENT - ALL FROM THIS ONE DAY"
    cv.text(right, 1008 - cv.text_w(right, 1), 52, 1, INK)
    cv.box(0, 66, W, 3, RED)
    # Region strip.
    for i, (name, count, col) in enumerate(REGIONS):
        x = 16 + i * 142
        cv.box(x, 70, 138, 18, col)
        cv.text_c(f"{name} {count}", x + 69, 73, 1, CREAM)
    # Stat strip.
    for i, (val, lab) in enumerate(STATS):
        x = 16 + i * 166
        cv.box(x, 90, 160, 28, CREAM)
        cv.frame(x, 90, 160, 28, INK, 1)
        cv.text_c(val, x + 80, 93, 2, RED)
        cv.text_c(lab, x + 80, 108, 1, INK)
    # Three big stories.
    for k, item in enumerate(BIG):
        big_story(cv, 16 + k * 333, 122, item)
    # Ten small stories, two rows of five.
    for k, item in enumerate(SMALL):
        small_story(cv, 16 + (k % 5) * 200, 438 + (k // 5) * 171, item)
    # Map and index.
    cv.text("WHERE IT HAPPENED", 16, 780, 1, RED)
    cv.text("ALSO ON THURSDAY 19 NOVEMBER 2026", 344, 780, 1, RED)
    draw_map(cv, 16, 794, 320, 170)
    for k, line in enumerate(BRIEFS):
        col = 344 + (k // 10) * 332
        cv.text(line, col, 796 + (k % 10) * 17, 1, INK)
    # Date check and footer.
    cv.text("DATE CHECK - EVERY STORY ON THIS PAGE WAS REPORTED ON "
            "THURSDAY 19 NOVEMBER 2026", 16, 972, 1, PINE)
    cv.text("CLAIMS ATTRIBUTED, NOT STATED AS FACT", 700, 972, 1, GREY)
    cv.text("LEFT OUT - 17 NOV: KERCH ROAD ARCH COLLAPSES - 18 NOV: "
            "ANTHROPIC PRICES IPO AT $83", 16, 983, 1, INK)
    cv.text("20 NOV: COP31'S SCHEDULED CLOSE; CYCLONE AKVAN'S LANDFALL",
            16, 994, 1, INK)
    cv.text_c("SOURCES: REUTERS, AP, AFP, BBC, AL JAZEERA, UN NEWS, "
              "EURONEWS, ABC, RNZ, XINHUA, NDTV, IMD, MEA, PIB, WION "
              "- 2026-11-19", W // 2, 1008, 1, GREY)
    return cv


# -------------------------------------------------------------------- png --
def _chunk(tag, data):
    piece = struct.pack(">I", len(data)) + tag + data
    return piece + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def save_png(cv, path):
    rows = bytearray()
    for yy in range(cv.h):
        rows.append(0)
        start = yy * cv.w * 3
        rows += cv.buf[start:start + cv.w * 3]
    head = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    body = b"\x89PNG\r\n\x1a\n"
    body += _chunk(b"IHDR", head)
    body += _chunk(b"IDAT", zlib.compress(bytes(rows), 9))
    body += _chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(body)


def run():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    save_png(compose(), os.path.join(out_dir, "entry.png"))


run() if __name__ == "__main__" else None
