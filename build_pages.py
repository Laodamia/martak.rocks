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


def page(fname, title, body, script="", current=None):
    links = "".join(f'<a href="{h}"{CURRENT if h == (current or fname) else ""}>{l}</a>' for l, h in NAV)
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
      <li><b>Community</b><span>Running a Women/NB circle in Berlin, and leading women in AI safety meetups at EAGs.</span></li>
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
    'An app full of authentic relating games.',
    'Silly and sometimes poetic Google Maps reviews. Yes, incl. public toilets and grocery stores.',
    'A book about Hebrew grammar & language history.',
    'I have like 8m views on Quora. Yes, a lot of time went into it.',
    'A 10-minute strength workout app.',
    'A blog in Toki Pona, a language with ~130 words.',
    'Bizarre collages, and an art blog to go with them.',
    'A circle for women and non-binary people in Berlin.',
    '100 words of writing a day, every day, on Medium.',
]
deck, script = card_page("Pull a project", PROJECTS)


# Project shelves: one crawling row of cards per section.
# Card: (title, when, two sentences, image slug or None, link or None, cover word if no image).
# Images come from ../project-images/make_images.py (tritone + "-c" colour version for hover).
SECTIONS = [
    ('Community &amp; facilitation', 'k1', 'I care about creating spaces where people feel safe to be vulnerable with each other.', [
        ('Women/NB circle', '2026–now', 'A small sharing circle for women and non-binary people, in Berlin. A sample of topics: body, femininity, leadership, forbidden emotions.', 'women-circle', None, None),
        ('Authentic relating &amp; radical honesty workshops', '2023–now', 'Facilitating workshops for up to 60 people in Berlin, Malaysia, Vietnam and other places. Many words, and even more feelings expressed.', 'ar-rh', None, None),
        ('Facilitation training', '2026', 'Seven days of group facilitation training with Honesty Europe in Finland. I came home with confidence in leading people through processing challenging emotions.', 'parkano', None, None),
        ('Soulful Sunday', '2024', 'A one-day mindfulness festival in Vietnam: 100+ people, eight workshops, two rooms. It was meant to be just a quiet afternoon of two workshops!', 'soulful-sunday', 'https://www.instagram.com/reel/C5nQml-P4HM/', None),
        ('Authentic Relating Games app', '2023', 'Every authentic relating game I found, all in one place. Pick one and play!', 'ar-games', 'https://authentic-relating-games.glide.page', None),
    ]),
    ('Sex &amp; intimacy', 'k3', 'I care about people having informed, unembarrassed sex.', [
        ('A beginner’s guide to anal', '2020', 'A gender-neutral sex-ed book, in print and PDF, in English and Polish. Co-written with A. Clarke, with award-winning illustrations by Mai Tran!', 'anal-book', 'https://beginnersguidetoanal.com/', None),
        ('Snarky Kinkster', '2017–19', 'My old blog about sex and kink. Long gone, still readable in the web archive if you really want to learn how to take a good dick pic.', 'snarky', 'https://web.archive.org/web/20190706103857/http://snarkykinkster.com/', None),
    ]),
    ('Languages &amp; words', 'k4', 'I find languages cool, and sometimes share how I see the world.', [
        ('Quora', '2015–19', 'Answers about languages, Hebrew, rationality and EA, read 8 million times. Top Writer 2018.', 'quora', 'https://www.quora.com/profile/Marta-Krzeminska', None),
        ('Hebrew course for LinguaLift', '2017–19', 'Two levels of an online Hebrew course. I designed the curriculum, wrote the lessons (&amp; had a lot of fun with it tbh).', 'hebrew-course', 'https://www.lingualift.com/', None),
        ('Hebrew Primer', '2018', 'My best Quora answers about Hebrew, edited into a short book. Still on sale.', 'hebrew-primer', 'https://mkrzeminska.gumroad.com/l/Hebrew-Language-Primer', None),
        ('Toki Pona blog', '2020', 'Everything I did and learned in toki pona, a language with about 130 words. I was quite a bit obsessed for a shorter while.', 'toki-pona', 'https://alelipona.wordpress.com/', None),
        ('100 words of bizarre', '2020–now', 'My Substack newsletter: attempts to parse the daily absurd. Still going!', 'bizarre', 'https://100words.substack.com', '?'),
        ('#100Words', '2020', 'A hundred words a day, for a hundred days, on Medium. Writing in public, badly and often.', '100words', 'https://medium.com/100-words-100-days', None),
    ]),
    ('Data', 'k2', 'I had an aim to become a data scientist. Because I like numbers.', [
        ('Data writing', '2020–21', 'Articles on Twitter sentiment, emoji and how people value their time. Is mango sticky rice the key to productivity?', 'data-writing', 'https://towardsdatascience.com/author/krzem-m/', None),
        ('Data portfolio', '2020', 'The projects I built while retraining as a data scientist. Python, statistics and plenty of scatter plots.', 'data-portfolio', 'https://github.com/Laodamia/Data-Portfolio', None),
    ]),
    ('Making things', 'k1', 'I care about doing silly things properly.', [
        ('Review Everything!', '2023–now', 'Silly, narrative, and sometimes poetic Google Maps reviews. 300+ as of now. Ask me about my fav one!', 'reviews', 'https://maps.app.goo.gl/mJYKFWvYLoHwY6i28', None),
        ('Accountability coaching', '2020–21', 'My coaching business, helping entrepreneurs actually finish their projects. The site lives on in the web archive.', 'coaching', 'https://web.archive.org/web/20210418091907/https://www.accountabilitycoa.ch/', None),
        ('10min Strength', '2020', 'A workout app: short home workouts, ten minutes a day. The app has since retired, unlike my biceps.', 'workout', None, None),
        ('Collages', '2020', 'Paper, glue and old magazines. Don’t be scared.', 'collages', 'https://www.instagram.com/sm.art.alicious/', None),
        ('Smartalicious', '2020', 'A blog documenting my arty pursuits. Clay, paper and whatever else was lying around.', 'smartalicious', 'https://smartalicious.wordpress.com/', None),
        ('SalsaMuffins', '2015', 'I danced and taught rueda de casino. This was the first (and lamest) website I ever made, now gone.', 'salsa', None, None),
    ]),
    ('Talks', 'k3', 'I care about a good room and a short slide deck.', [
        ('How I hacked Quora', '2018', 'A talk at London Hack’n’Tell. Spoiler: there are no hacks.', 'talk-quora', 'https://docs.google.com/presentation/d/1eMyH68LD8bbtvTCTu3vcK_3XIl1H8WvCpoi7t8JvvTs/edit?usp=sharing', None),
        ('Dating 3.0: dating as sales', '2018', 'A talk at London Hack’n’Tell. Acquisition, activation, retention.', 'talk-dating', 'https://docs.google.com/presentation/d/1lcs6L1FQbLsYBeOimE2AY1o-a_IiBSnzPnwaJsvsKQw/edit?usp=sharing', None),
        ('How to launch yourself as a brand', '2018', 'A talk at London Hack’n’Tell. How to believe your own hype in four hours.', 'talk-brand', 'https://docs.google.com/presentation/d/1zPcw_VDO_5hZILpKXeItSmQ8kjyxqKfgCqVgpZw1mqw/edit?usp=sharing', None),
        ('Chatbots are the answer', '2018', 'A talk at Nomad Cafe in Las Palmas. To all your woes, apparently.', 'talk-chatbots', 'https://docs.google.com/presentation/d/1bUzzbF59zKYIjSskbBp9FlpjJ1155uITZM1gFDNB0aY/edit?usp=sharing', None),
        ('Research-based career planning', '2019', 'A workshop at Hustler Villa in Bali and Hub53 in Chiang Mai. How to craft a dream career, according to research.', 'talk-career', 'https://docs.google.com/presentation/d/1Ro7wZ1Iejhx01WK3S4Ev-eeympmuOco-dr-6XUDvG6w/edit?usp=sharing', None),
        ('Intro to AI safety', '2024–25', 'Three intro talks on AI safety and alignment, at co-working spaces in Malaysia, Vietnam and Berlin. For people who’d heard the hype and wanted the worry.', None, 'https://docs.google.com/presentation/d/1agGuDVXl2M3aZnrO4LHKAEYsoGN4YUO2s-bh7CPTz98/edit?usp=sharing', 'AI?'),
    ]),
]


def pcard(title, when, text, img, link, cover, hidden=False):
    tag, attrs = ("a", f' href="{link}" target="_blank" rel="noopener"') if link else ("div", "")
    if hidden:
        attrs += ' aria-hidden="true" tabindex="-1"'
    pic = (f'<span class="pic"><img src="img/projects/{img}.jpg" alt="" loading="lazy">'
           f'<img class="c" src="img/projects/{img}-c.jpg" alt="" loading="lazy"></span>') if img else f'<span class="pic cover"><b>{cover}</b></span>'
    arrow = '<span class="go">&nearr;</span>' if link else ""
    date = f'<small class="ongoing">{when}</small>' if when.endswith("now") else f"<small>{when}</small>"
    return (f'<{tag} class="pcard"{attrs}><span class="head">{date}<b>{title}{arrow}</b></span>'
            f'<span class="row"><span class="txt">{text}</span>{pic}</span></{tag}>')


def shelves():
    out = ""
    for i, (name, colour, intro, cards) in enumerate(SECTIONS):
        first = "".join(pcard(*c) for c in cards)
        copy = "".join(pcard(*c, hidden=True) for c in cards)
        out += f"""
  <section class="shelf" style="--sc: var(--{colour})">
    <h2>{name}</h2>
    <p>{intro}</p>
    <div class="rail" data-dir="{-1 if i % 2 == 0 else 1}"><div class="track"><div class="set">{first}</div><div class="set" aria-hidden="true">{copy}</div></div></div>
  </section>
"""
    return out


script += """<script>
  // Shelves crawl sideways (alternating directions) and stop while you hover a card.
  // Touch screens and reduced-motion users get a normal swipeable row instead.
  (function () {
    if (!matchMedia("(hover: hover)").matches || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    document.querySelectorAll(".rail").forEach(rail => {
      const track = rail.firstElementChild, set = track.firstElementChild, dir = +rail.dataset.dir;
      if (set.offsetWidth <= rail.clientWidth) return;  // short shelves just sit still
      let x = dir > 0 ? -set.offsetWidth : 0, speed = 22, boost = 0, last = performance.now(), paused = false;
      rail.classList.add("moving");
      rail.addEventListener("mouseenter", () => paused = true);
      rail.addEventListener("mouseleave", () => paused = false);
      rail.addEventListener("focusin", () => paused = true);
      rail.addEventListener("focusout", () => paused = false);
      rail.addEventListener("wheel", e => {
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) { e.preventDefault(); boost += e.deltaX; }
      }, { passive: false });
      function frame(now) {
        const dt = Math.min((now - last) / 1000, 0.1); last = now;
        x += (paused ? 0 : dir * speed * dt) - boost; boost = 0;
        const w = set.offsetWidth;
        if (-x >= w) x += w;
        if (x > 0) x -= w;
        track.style.transform = `translateX(${x}px)`;
        requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    });
  })();
</script>
"""
PROJECTS_BODY = """
  <section class="hero">
    <div>
      <h1>Projects <i>in progress</i>.</h1>
      <p>Things I made because I wanted to. Pull one from the stack, or browse the shelves below.</p>
    </div>
{deck}
  </section>
{shelves}
"""
page("projects.html", "Projects · MK.AI", PROJECTS_BODY.format(deck=deck, shelves=shelves()), script)

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
