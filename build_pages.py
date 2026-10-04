#!/usr/bin/env python3
"""Generate the live pages (index, work, projects, me) from the content below.
Run from this folder: python3 build_pages.py
"""
import json

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Marta Krzeminska builds systems and communities for AI safety.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
  <nav><a class="name" href="index.html">Marta Krzeminska</a><div>{links}</div></nav>
"""
FOOT = """
  <footer><a href="https://www.linkedin.com/in/krzeminskamarta/">LinkedIn</a><a href="https://github.com/Laodamia">GitHub</a><a href="https://www.admonymous.co/marta-krzeminska">Anonymous feedback</a></footer>
</div>
{script}</body>
</html>
"""
NAV = [("Work", "work.html"), ("Projects", "projects.html"), ("Me", "me.html")]
BLOCKS = '<div class="blocks" aria-hidden="true"><span class="k1"></span><span class="k2"></span><span class="k3"></span><span class="k4"></span></div>'
CURRENT = ' aria-current="page"'


def page(fname, title, body, script=""):
    links = "".join(f'<a href="{h}"{CURRENT if h == fname else ""}>{l}</a>' for l, h in NAV)
    with open(fname, "w") as f:
        f.write(HEAD.format(title=title, links=links) + body + FOOT.format(script=script))


def card_page(front, items):
    deck = f"""    <div class="deck">
      {BLOCKS}
      <button class="qcard" id="qcard" aria-label="{front}">
        <div class="face front"><div><b>{front}</b><small>tap the card</small></div></div>
        <div class="face back"><p id="q"></p></div>
      </button>
      <button class="again" id="again">Another one</button>
    </div>"""
    script = f'<script>window.CARD_ITEMS = {json.dumps(items, ensure_ascii=False, indent=2)};</script>\n<script src="card.js"></script>\n'
    return deck, script


# Home. Placeholder prompts; swap in ones from the AR games / 365 Questions material.
QUESTIONS = [
    "What's something you believe that most people around you don't?",
    "What are you pretending not to know right now?",
    "When did you last change your mind about something important?",
    "What would you do this year if you knew it couldn't fail?",
    "What's a compliment you got years ago that you still think about?",
    "What are you avoiding saying to someone?",
    "What does a really good day look like for you?",
]
deck, script = card_page("Draw a question", QUESTIONS)
page("index.html", "Marta Krzeminska", f"""
  <section class="hero">
    <div>
      <h1>I build systems and communities for <i>AI safety</i>.</h1>
      <p>Outside work, I facilitate authentic relating and radical honesty events. Which is why there's a card here for you.</p>
      <p>Before this? Start-ups: growth marketing, data analysis, and coaching entrepreneurs to finish what they started.</p>
    </div>
{deck}
  </section>

  <section class="now">
    <h2>Now</h2>
    <ul>
      <li><b><a href="https://futureimpact.group">FIG</a></b><span>Building the systems behind AI safety fellowships.</span></li>
      <li><b>Mentoring</b><span>Women in AI safety, through Magnify Mentoring.</span></li>
      <li><b>Community</b><span>Women in AI Safety meetup at EAG London, and a women's circle in Berlin.</span></li>
    </ul>
  </section>
""", script)

# Work: a progress bar you can push, which never reaches 100%
page("work.html", "Work · Marta Krzeminska", f"""
  <section class="hero">
    <div>
      <h1>Works <i>in progress</i>.</h1>
      <p>This page is being built. In the meantime, you can help it along.</p>
    </div>
    <div class="deck">
      {BLOCKS}
      <div class="progress">
        <div class="pct"><span id="pct">0</span>%</div>
        <div class="bar"><div id="bar"></div></div>
        <p class="status" id="status">Nothing written yet. Very calm.</p>
      </div>
      <button class="again" id="push">Help it along</button>
    </div>
  </section>
""", """<script>
  // Each click closes half the remaining gap, so it never quite gets to 100%.
  const STATUS = [
    "Nothing written yet. Very calm.",
    "Opened a blank document. Stared at it.",
    "Made a plan for the plan.",
    "Wrote a first draft. Deleted the first draft.",
    "Asked for feedback. Got feedback.",
    "Nearly there. Adding one more section.",
    "Removing the extra section.",
    "Final touches. Then more final touches.",
    "Very, very nearly done."
  ];
  let progress = 0, clicks = 0;
  document.getElementById("push").addEventListener("click", () => {
    clicks++;
    progress += (100 - progress) / 2;
    document.getElementById("bar").style.width = progress + "%";
    document.getElementById("pct").textContent = progress >= 99 ? progress.toFixed(4) : Math.floor(progress);
    document.getElementById("status").textContent = STATUS[Math.min(clicks, STATUS.length - 1)];
  });
</script>
""")

# Projects: pull a random project teaser
PROJECTS = [
    "An app full of authentic relating games.",
    "Long, sincere Google Maps reviews of public toilets and grocery stores.",
    "A Hebrew primer that started as Quora answers.",
    "A 10-minute strength workout app.",
    "A blog in Toki Pona, a language with about 130 words.",
    "Collages, and an art blog to go with them.",
    "A circle for women and non-binary people in Berlin.",
    "100 words of writing a day, every day, on Medium.",
    "A seven-year Anki habit: 146,000 flashcard reviews since 2019. Current streak: {streak} days.",
]
deck, script = card_page("Pull a project", PROJECTS)
# Streak counted from its start date (10 Aug 2026), so the number stays current.
script = script.replace('<script src="card.js">', """<script>
  const streak = Math.floor((Date.now() - new Date(2026, 7, 10)) / 86400000) + 1;
  window.CARD_ITEMS = window.CARD_ITEMS.map(t => t.replace("{streak}", streak));
</script>
<script src="card.js">""")
page("projects.html", "Projects · Marta Krzeminska", f"""
  <section class="hero">
    <div>
      <h1>Projects <i>in progress</i>.</h1>
      <p>Things I made because I wanted to! The proper write-ups are coming. Until then, pull one from the stack.</p>
    </div>
{deck}
  </section>
""", script)

# Me: pull a random fact
FACTS = [
    "I like being on trains and on bridges.",
    "I'm in bed by 10.15 pm, seven days a week.",
    "I find the smell of most cosmetics more distracting than pleasant.",
    "My favourite snack is thin corn cakes.",
    "My recurring nightmare is being almost late for a train, a plane or a bus.",
]
deck, script = card_page("Pull a fact", FACTS)
page("me.html", "Me · Marta Krzeminska", f"""
  <section class="hero">
    <div>
      <h1>Me, <i>permanently in progress</i>.</h1>
      <p>The full page is on its way. For now, a few random facts.</p>
    </div>
{deck}
  </section>
""", script)
