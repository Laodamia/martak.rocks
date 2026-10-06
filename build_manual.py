#!/usr/bin/env python3
"""Build manual-of-me.html from ../Manual of Me.md.
Unlisted page: nothing on the site links to it, and it is noindex.
Run from this folder: python3 build_manual.py
"""
import html
import re

import markdown

SRC = "../Manual of Me.md"
OUT = "manual-of-me.html"

EMOJI = re.compile(r"^[^\w*]+")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def split_heading(raw):
    """'💭 **Work Philosophy:** Prioritise deep work' -> ('Work Philosophy', 'Prioritise deep work')."""
    text = EMOJI.sub("", raw.replace("**", "")).strip()
    title, _, tldr = text.partition(":")
    return title.strip(), tldr.strip().rstrip(".")


md = open(SRC, encoding="utf-8").read()

# Notion leftovers: the aside callout, the ToC hint, the H1, and the internal Notion link.
aside = re.search(r"<aside>\s*(.*?)\s*</aside>", md, re.S)
intro_note = re.sub(r"^💡\s*", "", aside.group(1).strip()) if aside else ""
md = re.sub(r"<aside>.*?</aside>\s*", "", md, flags=re.S)
md = re.sub(r"^# .*\n", "", md)
md = re.sub(r"^\s*-\s*👀.*\n", "", md, flags=re.M)
md = re.sub(r"\]\(Manual%20of%20Me[^)]*\.md\)", "](#availability-boundaries)", md)
md = md.replace(
    "feel free to add them directly to the doc or reach out!",
    "feel free to [email me](mailto:marta@martak.rocks)!",
)

# Everything before the first section goes above the contents, under "What is this doc?".
intro_md, _, md = md.partition("\n## ")
md = "## " + md
intro_md = re.sub(r"\n-{3,}\s*$", "", intro_md.strip())
intro_html = markdown.markdown(intro_note + "\n\n" + intro_md)

# Headings: anchor ids + tl;dr line, and collect the table of contents.
toc = []


def heading(m):
    level, raw = len(m.group(1)), m.group(2)
    title, tldr = split_heading(raw)
    sid = slug(title)
    toc.append((level, sid, title, tldr))
    sub = f'<p class="tldr">{html.escape(tldr)}</p>' if tldr else ""
    return f'\n<h{level} id="{sid}"><a href="#{sid}">{html.escape(title)}</a></h{level}>\n{sub}\n'


md = re.sub(r"^(#{2,3})\s+(.*)$", heading, md, flags=re.M)

body = markdown.markdown(md, extensions=["sane_lists"])
body = body.replace("<hr />", '<hr>')

# Notion-style toggles: a bullet with sub-bullets opens on click.
body = re.sub(
    r"<li>((?:(?!</?li>).)*?)<ul>(.*?)</ul>\s*</li>",
    r'<li class="toggle"><details><summary>\1</summary><ul>\2</ul></details></li>',
    body,
    flags=re.S,
)

toc_html = "\n".join(
    f'<li class="l{lvl}"><a href="#{sid}">{html.escape(t)}</a>'
    + (f' <span>{html.escape(d)}</span>' if d else "")
    + "</li>"
    for lvl, sid, t, d in toc
)

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Manual of Me · Marta Krzeminska</title>
<meta name="description" content="How it is to work with Marta Krzeminska.">
<meta property="og:title" content="Manual of Me · Marta Krzeminska">
<meta property="og:description" content="How it is to work with me.">
<meta property="og:image" content="https://martak.rocks/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<style>
:root {{
  --bg: #fdf6ec; --text: #22201d; --muted: #6f675d; --rule: rgba(34, 32, 29, 0.12);
  --accent: #c2471f; --k1: #2f6f62; --k2: #7a4e8c; --k3: #d9542f; --k4: #e9b23f;
  --serif: Fraunces, Georgia, serif;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #1b1a18; --text: #efe9df; --muted: #a39b91; --rule: rgba(239, 233, 223, 0.14); --accent: #e0683f; }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--bg); color: var(--text); font: 17px/1.7 Inter, system-ui, sans-serif; }}
main {{ max-width: 680px; margin: 0 auto; padding: 0 20px 96px; }}
a {{ color: var(--accent); text-underline-offset: 3px; }}

.strip {{ display: flex; gap: 8px; justify-content: center; padding: 40px 0 0; }}
.strip span {{ height: 10px; border-radius: 6px; animation: breathe 9s ease-in-out infinite; }}
.strip span:nth-child(1) {{ width: 64px; background: var(--k1); }}
.strip span:nth-child(2) {{ width: 28px; background: var(--k2); animation-delay: -2s; }}
.strip span:nth-child(3) {{ width: 44px; background: var(--k3); animation-delay: -4s; }}
.strip span:nth-child(4) {{ width: 16px; background: var(--k4); animation-delay: -6s; }}
@keyframes breathe {{ 50% {{ transform: scaleX(1.35); }} }}
@media (prefers-reduced-motion: reduce) {{ .strip span {{ animation: none; }} }}

header {{ text-align: center; padding: 28px 0 8px; }}
header h1 {{ font-family: var(--serif); font-weight: 800; font-size: clamp(36px, 7vw, 52px); line-height: 1.05; margin: 0 0 12px; }}
header .by {{ color: var(--muted); font-size: 15px; margin: 0; }}
header .by a {{ color: inherit; }}
.intro {{ margin-top: 40px; }}
.intro h2 {{ font-family: var(--serif); font-size: 24px; line-height: 1.2; margin: 0 0 12px; }}

nav.toc {{ margin: 40px 0 8px; padding: 22px 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }}
nav.toc h2 {{ font: 600 12px/1 Inter, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin: 0 0 14px; }}
nav.toc ol {{ list-style: none; margin: 0; padding: 0; }}
nav.toc li {{ margin: 0 0 10px; }}
nav.toc li.l3 {{ padding-left: 20px; font-size: 15px; }}
nav.toc a {{ font-weight: 700; text-decoration: none; color: var(--text); }}
nav.toc a:hover {{ color: var(--accent); }}
nav.toc li {{ line-height: 1.5; }}
nav.toc span {{ color: var(--muted); font-size: 14px; }}
nav.toc span::before {{ content: "· "; }}

article h2, article h3 {{ font-family: var(--serif); line-height: 1.2; scroll-margin-top: 24px; }}
article h2 {{ font-size: 30px; margin: 64px 0 4px; }}
article h3 {{ font-size: 22px; margin: 40px 0 4px; }}
article h2 a, article h3 a {{ color: inherit; text-decoration: none; }}
article h2 a:hover::after, article h3 a:hover::after {{ content: " #"; color: var(--accent); }}
.tldr {{ color: var(--muted); font-style: italic; margin: 0 0 18px; }}
article ul {{ padding-left: 22px; }}
article li {{ margin: 6px 0; }}
article li::marker {{ color: var(--accent); }}
article li.toggle {{ list-style: none; margin-left: -22px; }}
summary {{ cursor: pointer; list-style: none; padding-left: 22px; position: relative; }}
summary::-webkit-details-marker {{ display: none; }}
summary::before {{ content: ""; position: absolute; left: 4px; top: .62em; border: 5px solid transparent; border-left: 7px solid var(--accent); transition: transform .15s; transform-origin: 3px 50%; }}
details[open] > summary::before {{ transform: rotate(90deg); }}
summary:hover {{ color: var(--accent); }}
details > ul {{ margin: 4px 0 10px 22px; }}
article hr {{ border: 0; height: 1px; background: var(--rule); margin: 56px 0; }}
article code {{ font-size: .9em; }}
.top {{ display: block; text-align: center; margin-top: 48px; font-size: 14px; color: var(--muted); }}
</style>
</head>
<body>
<div class="strip" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
<main>
<header>
  <h1>Manual of Me</h1>
  <p class="by">How it is to work with <a href="https://martak.rocks">Marta Krzeminska</a></p>
</header>
<section class="intro">
  <h2>What is this doc?</h2>
{intro_html}
</section>
<nav class="toc" aria-label="Contents">
  <h2>Contents</h2>
  <ol>
{toc_html}
  </ol>
</nav>
<article>
{body}
</article>
<a class="top" href="#">Back to top</a>
</main>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(PAGE)
print(f"wrote {OUT}: {len(toc)} headings")
