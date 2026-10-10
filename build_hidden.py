#!/usr/bin/env python3
"""Build the unlisted long-read pages from ../content/*.md:
date-me.html (+ date-me-clicked.html, date-me-is-this.html), marketing-consulting.html,
codex-vitae.html (+ codex-vitae-YEAR.html).
Nothing on the site links to them, and they are noindex. Same look as manual-of-me.html (reading.css).
Run from this folder: python3 build_hidden.py
"""
import csv
import glob
import html
import os
import re

import markdown
from bs4 import BeautifulSoup

C = "../content"
IMG_DIR = "img/date-me"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{title} · Marta Krzeminska</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="stylesheet" href="reading.css">
</head>
<body>
<div class="strip" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
<main>
{cover}<header>
  <h1>{title}</h1>
  <p class="by">{by}</p>
</header>
"""
FOOT = """<a class="top" href="#">Back to top</a>
</main>
{script}</body>
</html>
"""
BY = 'by <a href="https://martak.rocks">Marta Krzeminska</a>'


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def write(fname, title, body, by=BY, script="", cover="", listed=False):
    robots = "" if listed else '<meta name="robots" content="noindex, nofollow">\n'
    with open(fname, "w", encoding="utf-8") as f:
        f.write(HEAD.format(title=html.escape(title), by=by, cover=cover, robots=robots) + body + FOOT.format(script=script))
    print("wrote", fname)


def media_src(path):
    """Notion image path -> our resized copy (GIFs became looping mp4s)."""
    stem = os.path.splitext(os.path.basename(path.replace("%20", " ")))[0].replace(" ", "_")
    for ext in (".jpg", ".png", ".mp4"):
        if os.path.exists(f"{IMG_DIR}/{stem}{ext}"):
            return f"{IMG_DIR}/{stem}{ext}"
    return path


def render(md, toc_levels=(2, 3)):
    """Notion-export markdown -> (intro_html, toc_html, body_html)."""
    md = re.sub(r"^[ \t]*-[ \t]*(Table of Contents|\*\*🧭\s+Navigation aka ToC\*\*)[ \t]*\n?", "", md, flags=re.M)
    md = re.sub(r"<aside>\s*(?:💡\s*)?(.*?)\s*</aside>", r'<div class="callout" markdown="1">\n\n\1\n\n</div>', md, flags=re.S)

    # Shift top-level headings so the biggest one becomes <h2>, and collect the ToC.
    levels = [len(m) for m in re.findall(r"^(#{1,6})\s", md, flags=re.M)]
    shift = 2 - min(levels) if levels else 0
    toc = []

    def heading(m):
        level = min(len(m.group(1)) + shift, 4)
        inner = markdown.markdown(m.group(2).replace("**", "").strip())[3:-4]  # keep *italics* and links
        text = BeautifulSoup(inner, "html.parser").get_text()
        sid = slug(text) or f"s{len(toc)}"
        if level in toc_levels:
            toc.append((level, sid, text))
        if "<a " in inner:
            return f'\n<h{level} id="{sid}">{inner}</h{level}>\n'
        return f'\n<h{level} id="{sid}"><a href="#{sid}">{inner}</a></h{level}>\n'

    md = re.sub(r"^(#{1,6})\s+(.*)$", heading, md, flags=re.M)

    intro_md, sep, rest = md.partition('\n<h')
    body_md = sep.lstrip("\n") + rest if sep else ""
    if not sep:
        intro_md, body_md = "", md
    intro_md = re.sub(r"\n-{3,}\s*$", "", intro_md.strip())

    def to_html(s):
        out = markdown.markdown(s, extensions=["sane_lists", "md_in_html", "tables"])
        return polish(out)

    toc_html = "\n".join(f'<li class="l{lvl}"><a href="#{sid}">{html.escape(t)}</a></li>' for lvl, sid, t in toc)
    return to_html(intro_md), toc_html, to_html(body_md)


def polish(out):
    soup = BeautifulSoup(out, "html.parser")
    # Images: Notion puts the caption as the next paragraph, repeating the alt text.
    for img in soup.find_all("img"):
        src = media_src(img["src"])
        alt = img.get("alt", "")
        p = img.parent
        nxt = p.find_next_sibling() if p.name == "p" else None
        fig = soup.new_tag("figure")
        if src.endswith(".mp4"):
            media = soup.new_tag("video", src=src, autoplay=True, loop=True, muted=True, playsinline=True)
            media["aria-label"] = alt
        else:
            media = soup.new_tag("img", src=src, alt=alt, loading="lazy")
        fig.append(media)
        caption = alt if alt and not re.search(r"\.(jpe?g|png|gif)$", alt, re.I) else ""
        if caption:
            cap = soup.new_tag("figcaption")
            cap.append(BeautifulSoup(markdown.markdown(caption)[3:-4], "html.parser"))
            fig.append(cap)
            if nxt is not None and nxt.name == "p" and nxt.get_text(strip=True) == BeautifulSoup(markdown.markdown(caption), "html.parser").get_text(strip=True):
                nxt.decompose()
        (p if p.name == "p" and len(p.contents) == 1 else img).replace_with(fig)

    # Runs of 2+ images next to each other become a mosaic, like Notion's image columns.
    for fig in soup.find_all("figure"):
        if fig.parent is None or (fig.parent.name == "div" and "mosaic" in fig.parent.get("class", [])):
            continue
        run, nxt = [fig], fig.find_next_sibling()
        while nxt is not None and nxt.name == "figure":
            run.append(nxt)
            nxt = nxt.find_next_sibling()
        if len(run) > 1 and all(str(x).strip() == "" for f in run[:-1] for x in [f.next_sibling] if x is not None and not getattr(x, "name", None)):
            box = soup.new_tag("div", attrs={"class": "mosaic"})
            fig.insert_before(box)
            for f in run:
                box.append(f.extract())

    # A list followed by a single image: put them side by side, like Notion's two columns.
    for fig in soup.find_all("figure"):
        prev = fig.find_previous_sibling()
        if fig.parent.name in ("li", "div") or prev is None or prev.name != "ul":
            continue
        box = soup.new_tag("div", attrs={"class": "side"})
        prev.insert_before(box)
        box.append(prev.extract())
        box.append(fig.extract())

    # Notion toggles: a bullet with paragraphs/images/headings under its first line opens on click.
    for li in reversed(soup.find_all("li")):
        kids = [k for k in li.children if getattr(k, "name", None) or str(k).strip()]
        blocks = [k for k in kids if getattr(k, "name", None) in ("p", "figure", "h2", "h3", "h4", "div", "ol", "ul")]
        has_rich = any(getattr(k, "name", None) in ("figure", "h2", "h3", "h4", "div") for k in kids) or \
            sum(1 for k in kids if getattr(k, "name", None) == "p") >= 2
        if not has_rich or not kids:
            continue
        first = kids[0]
        rest = kids[1:]
        details = soup.new_tag("details")
        summary = soup.new_tag("summary")
        if getattr(first, "name", None) == "p":
            for c in list(first.contents):
                summary.append(c.extract())
            first.decompose()
        else:
            # Bare text before the first block
            for c in list(li.contents):
                if getattr(c, "name", None) in ("p", "figure", "h2", "h3", "h4", "div", "ol", "ul"):
                    break
                summary.append(c.extract())
            rest = [k for k in li.children if getattr(k, "name", None)]
        more = soup.new_tag("div", attrs={"class": "more"})
        for k in rest:
            more.append(k.extract())
        details.append(summary)
        details.append(more)
        li.clear()
        li.append(details)
        li["class"] = li.get("class", []) + ["toggle"]
    return str(soup).replace("<hr/>", "<hr>")


def page_body(intro, toc, body, extra=""):
    parts = []
    if intro.strip():
        parts.append(f'<section class="intro">\n{intro}\n</section>')
    if toc.strip():
        parts.append(f'<nav class="toc" aria-label="Contents">\n  <h2>Contents</h2>\n  <ol>\n{toc}\n  </ol>\n</nav>')
    parts.append(f"<article>\n{body}\n{extra}</article>")
    return "\n".join(parts) + "\n"


def read(path):
    md = open(path, encoding="utf-8").read()
    md = re.sub(r"^# .*\n", "", md, count=1)                 # title goes in the header
    md = re.sub(r"^\*(Hidden page draft|Draft to).*\*\s*\n", "", md, flags=re.M)  # our own notes
    return md


# ---------- Date Me ----------
SELF = r"\(Date%20Me%2017435416720c439b8d6725d690808f55\.md\)"
md = read(f"{C}/date-me.md")
md = md.replace("Emotional_overwhelm_(1)", "Emotional_overwhelm_1")
md = re.sub(r"\[here\]" + SELF, "[here](#what-now-contact)", md)
for n in (1, 2, 3):
    md = re.sub(r"\[\[%d\]\]%s|\[\[%d\]%s\]" % (n, SELF, n, SELF),
                f'<sup id="ref-{n}"><a href="#fn-{n}">[{n}]</a></sup>', md, count=1)
    md = re.sub(r"^\[%d\] (.*)$" % n, lambda m, n=n: f'<span id="fn-{n}"></span>[{n}] ' + re.sub(SELF, f"(#ref-{n})", m.group(1)), md, flags=re.M)
md = re.sub(r"\(date-me/You%20clicked%20it!%20[0-9a-f]+\.md\)", "(date-me-clicked.html)", md)
md = re.sub(r"\n\[You clicked it!\]\(date-me-clicked\.html\)\s*$", "\n", md)
intro, toc, body = render(md)
COVER = '<figure class="cover"><img src="img/date-me/cover.jpg" alt="Comic: I understand now. There\'s no choir of angels when you meet the right person. It\'s about growing out of your fears to realize what you have is what you want. I do. I do. Trumpeting angels appear for a stranger. Well, shit." width="1804" height="420"><figcaption>Comic: <a href="https://xkcd.com">xkcd</a></figcaption></figure>\n'
write("date-me.html", "Date Me", page_body(intro, toc, body), cover=COVER)

sub = f"{C}/date-me"
md = read(glob.glob(f"{sub}/You clicked it! *.md")[0])
md = re.sub(r"\(You%20clicked%20it!/Is%20this%E2%80%A6%20[0-9a-f]+\.md\)", "(date-me-is-this.html)", md)
md = re.sub(r"\n\[Is this…\]\(date-me-is-this\.html\)\s*$", "\n", md)
md = re.sub(r"\(\.\./Date%20Me%20[0-9a-f]+\.md\)", "(date-me.html)", md)
intro, toc, body = render(md, toc_levels=())
write("date-me-clicked.html", "You clicked it!", page_body(intro, "", body), by='<a href="date-me.html">← back to the Date Me doc</a>')

md = read(glob.glob(f"{sub}/You clicked it!/Is this* *.md")[0])
md = re.sub(r"\(\.\./\.\./Date%20Me%20[0-9a-f]+\.md\)", "(date-me.html)", md)
intro, toc, body = render(md, toc_levels=())
write("date-me-is-this.html", "Is this…", page_body(intro, "", body), by='<a href="date-me.html">← back to the Date Me doc</a>')


# ---------- Marketing Consulting ----------
md = read(f"{C}/marketing-consulting.md")
md = re.sub(r"!\[digital\.png\]\(marketing-consulting/digital\.png\)\s*", "", md)
md = re.sub(r"\(Marta-bot%20Projects%20[0-9a-f]+\.md\)", "(mailto:marta@martak.rocks)", md)
md = re.sub(r"^\[Marketing Competencies\]\(.*\)\s*$", "", md, flags=re.M)
md = re.sub(r"^sort:.*\n(\s*\n)*Proficiency: descending\s*$", "", md, flags=re.M)
md = md.replace("as as a", "as a")
intro, toc, body = render(md, toc_levels=())
rows = list(csv.DictReader(open(glob.glob(f"{C}/marketing-consulting/*_all.csv")[0], encoding="utf-8-sig")))
JOY = {"High": 3, "Medium": 2, "Low": 1}
items = []
for r in rows:
    prof = int(r["Proficiency"].rstrip("%") or 0)
    tasks = [re.sub(r"^\d+\.\s*", "", t).strip() for t in r["Example tasks"].split("\n") if t.strip()]
    task_html = "".join(f"<li>{html.escape(t)}</li>" for t in tasks)
    items.append(f"""<li class="comp" data-name="{html.escape(r['Competence'])}" data-prof="{prof}" data-joy="{JOY.get(r['Enjoyment'], 0)}">
  <div class="row">
    <b>{html.escape(r['Competence'])}</b>
    <div class="bar"><div class="track"><div class="fill" style="width:{prof}%"></div></div><small><span>{prof}% proficiency</span><span class="joy-{r['Enjoyment']}">{r['Enjoyment']} fun</span></small></div>
    <p class="desc">{html.escape(r['Description'])}</p>
  </div>
  {f'<details><summary>Example tasks</summary><ol>{task_html}</ol></details>' if tasks else ''}
</li>""")
comps = f"""<div class="sorter">Sort by
  <button data-sort="prof" aria-pressed="true">Proficiency</button>
  <button data-sort="joy" aria-pressed="false">Enjoyment</button>
  <button data-sort="name" aria-pressed="false">A–Z</button>
</div>
<ul class="comps" id="comps">
{chr(10).join(items)}
</ul>
"""
SORT_JS = """<script>
(function () {
  var list = document.getElementById('comps'), buttons = document.querySelectorAll('.sorter button');
  function sort(key) {
    var items = Array.prototype.slice.call(list.children);
    items.sort(function (a, b) {
      if (key === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      var d = (+b.dataset[key]) - (+a.dataset[key]);
      return d || (+b.dataset.prof) - (+a.dataset.prof);
    });
    items.forEach(function (li) { list.appendChild(li); });
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.sort === key); });
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { sort(b.dataset.sort); }); });
  sort('prof');
})();
</script>
"""
hero = '<figure><img src="img/marketing/digital.png" alt="" width="1500" height="600"></figure>'
write("marketing-consulting.html", "Marketing Consulting", page_body(hero + intro, "", body + comps), script=SORT_JS)


# ---------- Codex Vitae ----------
years = sorted((re.search(r"(\d{4})", p).group(1), p) for p in glob.glob(f"{C}/codex-vitae/codex-vitae-*.md"))
tiles = []
for i, (y, p) in enumerate(years):
    md = read(p)
    words = len(re.findall(r"\w+", md))
    intro, toc, body = render(md)
    prev_l = f'<a href="codex-vitae-{years[i-1][0]}.html">← {years[i-1][0]}</a>' if i > 0 else "<span></span>"
    next_l = f'<a href="codex-vitae-{years[i+1][0]}.html">{years[i+1][0]} →</a>' if i < len(years) - 1 else "<span></span>"
    pager = f'<nav class="pager">{prev_l}<a href="codex-vitae.html">All versions</a>{next_l}</nav>\n'
    write(f"codex-vitae-{y}.html", f"Codex Vitae {y}", page_body(intro, toc, body, pager),
          by=f'{BY} · <a href="codex-vitae.html">all versions</a>')
    tiles.append(f'<li><a href="codex-vitae-{y}.html">{y}<small>{round(words, -2):,} words</small></a></li>')
index_md = open(f"{C}/codex-vitae.md", encoding="utf-8").read()
blurb = re.search(r"^INTRO: (.*)$", index_md, flags=re.M)
blurb = blurb.group(1) if blurb else "The beliefs, principles and lessons I live by, rewritten every year or so. Newest first."
write("codex-vitae.html", "Codex Vitae",
      f'<section class="intro"><p>{html.escape(blurb)}</p></section>\n<ul class="years">\n' + "\n".join(reversed(tiles)) + "\n</ul>\n")


# ---------- Worldview in 5 books (linked from the Me page) ----------
md = open(f"{C}/worldview.md", encoding="utf-8").read()
title = re.search(r"^# (.*)$", md, flags=re.M).group(1)
md = read(f"{C}/worldview.md")
# Intro is written one sentence per line: questions become an italic list, other lines their own paragraphs.
head, sep, tail = md.partition("\n---")
lines = [l.strip() for l in head.strip().split("\n") if l.strip()]
head = "\n\n".join(f"- *{l}*" if l.endswith("?") else l for l in lines).replace("*\n\n- *", "*\n- *")
md = head + "\n" + sep + tail
covers = re.findall(r"!\[\]\(worldview/([^)]+)\)", md)        # one cover per book, in book order
md = re.sub(r"^!\[\]\(worldview/[^)]+\)\s*$\n?", "", md, flags=re.M)
intro, toc, body = render(md, toc_levels=())
soup = BeautifulSoup(body, "html.parser")
for h, cover in zip(soup.find_all("h2"), covers):   # wrap each book: cover + heading + text up to the next book or rule
    box = soup.new_tag("div", attrs={"class": "book"})
    h.insert_before(box)
    box.append(soup.new_tag("img", attrs={"class": "bookcover", "src": f"img/worldview/{cover}", "alt": "", "loading": "lazy"}))
    node = h
    while node is not None and (node is h or node.name not in ("h2", "hr")):
        nxt = node.next_sibling
        box.append(node.extract())
        node = nxt
body = str(soup)
write("worldview.html", title, page_body(intro, "", body), listed=True)


# ---------- Causes Worth Your Support (linked from the Me page) ----------
md = open(f"{C}/causes.md", encoding="utf-8").read()
title = re.search(r"^# (.*)$", md, flags=re.M).group(1)
intro, toc, body = render(read(f"{C}/causes.md"), toc_levels=())
CAUSES_COVER = '<figure class="cover"><img src="img/causes/cover-painting.jpg" alt="Painting of a sleeping baby in a glass box, captioned: Tú dices que estás bien, pero no es cierto (You say you are fine, but it is not true)." width="1800" height="652"><figcaption>Julio Gal&aacute;n, <em>You say you are okay, but that isn&rsquo;t true</em>, 1986. <a href="https://www.stedelijk.nl/nl/collectie/maker/8458-julio-galan">Stedelijk Museum Amsterdam</a>. Photo: me</figcaption></figure>\n'
write("causes.html", title, page_body(intro, "", body), cover=CAUSES_COVER, listed=True)
