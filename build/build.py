"""Builds the Firebase site (index.html) from the app source (src/app.html). Run from the repo root: python3 build/build.py"""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(R, p), encoding="utf-8").read()
src, head, shim, authh = rd("src/app.html"), rd("build/fb_head.html"), rd("build/fb_shim.js"), rd("build/fb_auth.html")
def rep(s, a, b):
    assert s.count(a) == 1, (a, s.count(a)); return s.replace(a, b)
s = rep(src, '</head>\n<body>', head + '<script>\n' + shim + '</script>\n</head>\n<body>\n' + authh)
s = rep(s, '} else if (tries++ < 20) {', '} else if (window.KB_FIREBASE || tries++ < 20) {')
s = rep(s, '"העוזר לא זמין בתצוגה הזו"', '(window.KB_FIREBASE ? "עוזר ה-AI יחובר בשלב הבא" : "העוזר לא זמין בתצוגה הזו")')
open(os.path.join(R, "index.html"), "w", encoding="utf-8").write(s)
print("wrote index.html", len(s))
