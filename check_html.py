# -*- coding: utf-8 -*-
import os
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append((tag, list(self.stack[-5:])))


html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "netmon-merged", "app", "index.html"),
            encoding="utf-8").read()
p = P()
p.feed(html)
print("unclosed tags:", p.stack)
print("mismatches:", p.errors[:10])

m = re.search(r"<script>(.*)</script>", html, re.S)
js = m.group(1)
for a, b in [("{", "}"), ("(", ")"), ("[", "]")]:
    ok = js.count(a) == js.count(b)
    print("JS %s%s: %d vs %d %s" % (a, b, js.count(a), js.count(b), "OK" if ok else "MISMATCH"))

for k in ['id="dc-panel"', 'id="dc-auth-overlay"', 'id="dc-today"', 'btn-dc-start',
          '/api/dc/status', 'dcInit()', 'PCDN 业务总览']:
    print(k, "->", html.count(k))
