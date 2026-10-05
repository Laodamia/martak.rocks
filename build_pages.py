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
<meta property="og:type" content="website">
<meta property="og:site_name" content="MK.AI">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="Marta Krzeminska builds systems and communities for AI safety.">
<meta property="og:image" content="https://martak.rocks/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="I build systems and communities for AI safety. Marta Krzeminska, martak.rocks">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
  <nav><a class="name" href="index.html">Marta Krzeminska</a><div>{links}</div></nav>
"""
FOOT = """
  <footer><a href="mailto:marta@martak.rocks">Email</a><a href="https://www.linkedin.com/in/krzeminskamarta/">LinkedIn</a><a href="https://github.com/Laodamia">GitHub</a><a href="https://www.admonymous.co/marta-krzeminska">Anonymous feedback</a></footer>
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
        f.write(HEAD.format(title=title, og_title=title.replace("MK.AI", "Marta Krzeminska"), links=links) + body + FOOT.format(script=script))


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
page("index.html", "MK.AI", f"""
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

# Work: three expandable roles, a one-line "before that", and a career you can push along.
CAREER = [
    "Finished a BA at Oxford. Oriental Studies, a first.",
    "Finished a master's in translation.",
    "Got my first job: ranking lawyers.",
    "Discovered I don't like office jobs.",
    "Did another master's, in endangered languages. Completely useless. No regrets.",
    "Started working in start-ups.",
    "Discovered effective altruism.",
    "Did a CFAR workshop.",
    "Fell in love with language start-ups.",
    "Got into the rationality community.",
    "Did a career review.",
    "Decided to become a data scientist.",
    "Was a digital nomad. Retrained as a data scientist.",
    "Relearned stats. Picked up Python.",
    "Started freelancing.",
    "Oh my God, COVID.",
    "Started an accountability coaching business.",
    "Got my first EA job, at Mind Ease.",
    "Lots of marketing.",
    "Data analytics.",
    "Oh my God, ChatGPT is out.",
    "Decided to pivot to AI safety.",
    "Got rejected from a BlueDot course. Did it anyway.",
    "Ran a marathon. Budapest.",
    "Did another BlueDot course.",
    "Joined the High Impact Professionals accelerator.",
    "Got career coaching from 80,000 Hours.",
    "Landed the perfect job.",
    "Burned out.",
    "Took six months off. Saw a lot of tea houses. Did a lot of aerial hammock.",
    "Freelanced for AI safety orgs.",
    "Got a part-time job.",
    "Ran another marathon. Istanbul.",
    "Put myself on a contract. It's part of my job.",
    "Ran another marathon. Rome.",
]
# Shown in order after the last step; the final one stays put.
AFTER = [
    "Still in progress.",
    "Very nearly done?",
    "Is it ever done?",
    "How long, exactly?",
    "How long are your timelines?",
    "This seems to be a long timeline.",
    "What now?",
    "Am I retired yet?",
    "No going back now.",
    "I hope at least I'm happy.",
]

def role(title, org, when, line, bullets, extra=""):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""      <details class="role">
        <summary><span class="r-head"><b>{title}</b><span class="r-org">{org}</span></span><span class="r-when">{when}</span><span class="r-line">{line}</span></summary>
        <ul>{lis}</ul>{extra}
      </details>
"""


ROLES = (
    role("Programme Operations Lead", '<a href="https://futureimpact.group">Future Impact Group</a>', "2025 to now",
         "I'm the backend. I rebuilt how the fellowship picks people. Now I'm rebuilding the ops.", [
             "Built a three-stage selection process that lets a three-person team get through 7,000+ applications for 30 research projects.",
             "Set up compliance for our UK trading entity.",
             "Make sure everyone gets paid, legally and on time. Also: contracts, bookkeeping, and automating anything that happens twice.",
         ])
    + role("Operations Support &amp; AI Policy Researcher", '<a href="https://www.longtermresilience.org">Centre for Long-Term Resilience</a>', "2024&ndash;25",
           "I helped a UK AI policy unit punch above its weight.", [
               'Co-authored <a href="https://www.longtermresilience.org/reports/frontier-ai-safety-frameworks-need-to-include-risk-governance/">Why frontier AI safety frameworks need to include risk governance</a>.',
               "Managed the inbox and calendar of Jess Whittlestone, head of the AI Policy Unit.",
               "Guided the team to structure their tasks and priorities.",
           ])
    + role("Freelance marketer and writer", "EA and AI safety orgs", "2020&ndash;25",
           "Short projects, many hats, one direction.", [
               'Designed a knowledge base for the <a href="https://condor.camp">Condor Initiative</a>.',
               'Got tonnes of people applying to <a href="https://bluedot.org/">BlueDot</a>\'s biosecurity course, through LinkedIn.',
               'Had fun leading two cohorts of <a href="https://bluedot.org/">BlueDot</a>\'s AI governance course.',
           ], '<p class="r-also">Also worked with: <a href="https://simoninstitute.ch/">Simon Institute for Longterm Governance</a>, <a href="https://givingmultiplier.org/">Giving Multiplier</a>, <a href="https://quantifieduncertainty.org/">QURI</a></p>')
)

# Newest first, to match the roles above.
BEFORE = " &bull; ".join([
    "Operations Lead at Arkose (2023)",
    "Head of Marketing, then Data Analyst at Mind Ease (2021&ndash;23)",
    "Computational Linguist at Tisane Labs (2021)",
    "Marketing Lead at JAM (2018&ndash;21)",
    "CX Manager at Strong Fitness (2019&ndash;20)",
    "Marketing Director, then Content Editor at HelloTalk (2018)",
    "VP of Content at Leaf (2017&ndash;18)",
    "Director of Outreach at LinguaLift (2015&ndash;18)",
    "Translator at Mi Polin (2016&ndash;17)",
    "Content Editor at The Wellbeing Network (2014&ndash;15)",
    "Assistant Curator at the Endangered Languages Archive (2014)",
    "Researcher at Chambers and Partners (2012&ndash;13)",
    "Translator at Brandbank (2012)",
    "Intern on the Dead Sea Scrolls Project (2008&ndash;09)",
])

page("work.html", "Work · MK.AI", f"""
  <section class="hero">
    <div>
      <h1>I make small teams look <i>suspiciously big</i>.</h1>
      <p>Mostly for AI safety: the systems, processes and quiet automations that mean nobody does the boring bit twice.</p>
    </div>
    <div class="deck">
      {BLOCKS}
      <div class="progress">
        <div class="pct">Step <span id="step">0</span></div>
        <div class="bar"><div id="bar"></div></div>
        <p class="status" id="status">Career: not started. Very calm.</p>
      </div>
      <button class="again" id="push">Advance my career</button>
    </div>
  </section>

  <section class="now roles">
    <h2>Work</h2>
{ROLES}  </section>

  <section class="now before">
    <h2>Before that</h2>
    <div class="ticker" id="ticker"><div class="track" id="track"><span>{BEFORE} &bull;&nbsp;</span><span aria-hidden="true">{BEFORE} &bull;&nbsp;</span></div></div>
  </section>
""", f"""<script>
  // One career step per click. The bar closes 12% of the remaining gap each time, so it never reaches 100%.
  const CAREER = {json.dumps(CAREER, ensure_ascii=False)};
  const AFTER = {json.dumps(AFTER, ensure_ascii=False)};
  let progress = 0, step = 0;
  document.getElementById("push").addEventListener("click", () => {{
    step++;
    progress += (100 - progress) * 0.12;
    document.getElementById("bar").style.width = progress + "%";
    document.getElementById("step").textContent = step;
    document.getElementById("status").textContent = step <= CAREER.length
      ? CAREER[step - 1]
      : AFTER[Math.min(step - CAREER.length - 1, AFTER.length - 1)];
  }});

  // "Before that" ticker: drifts left forever; faster on hover, and horizontal scrolling pushes it along.
  (function () {{
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ticker = document.getElementById("ticker"), track = document.getElementById("track");
    const loop = track.firstElementChild;
    let x = 0, speed = 40, boost = 0, last = performance.now();
    ticker.addEventListener("mouseenter", () => speed = 160);
    ticker.addEventListener("mouseleave", () => speed = 40);
    ticker.addEventListener("wheel", e => {{
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {{ e.preventDefault(); boost += e.deltaX; }}
    }}, {{ passive: false }});
    function frame(now) {{
      const dt = Math.min((now - last) / 1000, 0.1); last = now;
      x -= speed * dt + boost; boost = 0;
      const w = loop.offsetWidth;
      if (-x >= w) x += w;
      if (x > 0) x -= w;
      track.style.transform = `translateX(${{x}}px)`;
      requestAnimationFrame(frame);
    }}
    ticker.classList.add("moving");
    requestAnimationFrame(frame);
  }})();
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
page("projects.html", "Projects · MK.AI", f"""
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
page("me.html", "Me · MK.AI", f"""
  <section class="hero">
    <div>
      <h1>Me, <i>permanently in progress</i>.</h1>
      <p>The full page is on its way. For now, a few random facts.</p>
    </div>
{deck}
  </section>
""", script)
