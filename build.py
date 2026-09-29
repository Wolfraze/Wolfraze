#!/usr/bin/env python3
"""
GitHub profile README generator.

1. Edit CONFIG below with your real details.
2. Run:  python build.py
3. Upload README.md and the assets/ folder to the repo named exactly like
   your GitHub username (github.com/<username>/<username>).

Output: README.md + assets/hero.svg, project-N.svg, footer.svg
"""
import html
import os
import textwrap

# ---------------------------------------------------------------------------
# CONFIG - EDIT EVERYTHING IN THIS BLOCK
# ---------------------------------------------------------------------------
CONFIG = {
    "handle": "your-github-username",
    "name": "Your Name",
    "role": "Software Engineer",
    "summary": "I build reliable backend systems and the tools developers use to ship them.",
    "status": "Open to work",
    "location": "City, Country",
    "bio": [
        "I'm a software engineer focused on backend systems, APIs and developer "
        "tooling. I care about code that is easy to read, easy to test and easy "
        "to delete.",
        "Most of my work sits between product and infrastructure: turning a vague "
        "requirement into a service that stays up under load.",
    ],
    "facts": [
        ("Role", "Software Engineer"),
        ("Based in", "City, Country"),
        ("Focus", "Backend systems, APIs, developer tooling"),
        ("Open to", "Full-time roles, freelance, open source"),
    ],
    # group -> [(label, simple-icons slug, hex color, optional logo color)]
    "stack": {
        "Languages": [
            ("Python", "python", "3776AB"),
            ("TypeScript", "typescript", "3178C6"),
            ("Go", "go", "00ADD8"),
            ("PostgreSQL", "postgresql", "4169E1"),
        ],
        "Frontend": [
            ("React", "react", "20232A", "61DAFB"),
            ("Next.js", "nextdotjs", "000000"),
            ("Tailwind CSS", "tailwindcss", "06B6D4"),
        ],
        "Backend and data": [
            ("FastAPI", "fastapi", "009688"),
            ("Node.js", "nodedotjs", "339933"),
            ("Redis", "redis", "DC382D"),
        ],
        "Infrastructure": [
            ("Docker", "docker", "2496ED"),
            ("GitHub Actions", "githubactions", "2088FF"),
            ("Linux", "linux", "FCC624", "black"),
            ("AWS", "", "232F3E"),
        ],
    },
    # first project is shown large; the rest in a two-column grid (max 7 total)
    # (name, description, [tech], repo url)
    "projects": [
        ("Project One", "A short, specific description of what this does, who it is for and the result it achieved. Mention scale or numbers if you have them.", ["Python", "FastAPI", "PostgreSQL"], "https://github.com/your-github-username/project-one"),
        ("Project Two", "What it does in one or two sentences, and the interesting technical problem you solved.", ["TypeScript", "React"], "https://github.com/your-github-username/project-two"),
        ("Project Three", "What it does in one or two sentences, and the interesting technical problem you solved.", ["Go", "Docker"], "https://github.com/your-github-username/project-three"),
        ("Project Four", "What it does in one or two sentences, and the interesting technical problem you solved.", ["Node.js", "Redis"], "https://github.com/your-github-username/project-four"),
        ("Project Five", "What it does in one or two sentences, and the interesting technical problem you solved.", ["Python", "Docker"], "https://github.com/your-github-username/project-five"),
    ],
    # (period, title, organisation, what you did)
    "experience": [
        ("2024 - Present", "Software Engineer", "Company Name", "Own the payments API. Cut p95 latency by 40% and moved deploys to zero-downtime."),
        ("2022 - 2024", "Junior Developer", "Company Name", "Built internal tooling used by 200+ staff. Introduced automated testing and CI."),
        ("2018 - 2022", "B.Tech, Computer Science", "University Name", "Graduated with honours. Led the campus coding club."),
    ],
    "currently": [
        ("Building", "The next thing on your list"),
        ("Learning", "Distributed systems and Rust"),
        ("Ask me about", "APIs, databases, developer experience"),
    ],
    "links": {
        "LinkedIn": "https://www.linkedin.com/in/your-profile",
        "Email": "mailto:you@example.com",
        "Portfolio": "https://your-site.dev",
        "X": "https://x.com/your-handle",
    },
    "footer": "Thanks for stopping by. If you're building something interesting, get in touch.",
}

# ---------------------------------------------------------------------------
# design tokens
# ---------------------------------------------------------------------------
INK, PANEL, LINE = "#0a1020", "#0d1527", "#22304d"
TEXT, MUTED, SOFT = "#e6ecf7", "#8b9bb8", "#b6c4de"
BLUE, GREEN = "#4c8dff", "#34d399"
ACCENTS = ["#4c8dff", "#2dd4bf", "#a78bfa", "#ffb454", "#fb7185", "#38bdf8", "#84cc16"]
SANS = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Menlo, Consolas, 'Courier New', monospace"
e = html.escape


def clip(s, n):
    return s if len(s) <= n else s[: max(n - 1, 1)].rstrip() + "\u2026"


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{e(label)}">')


# ---------------------------------------------------------------------------
# hero banner
# ---------------------------------------------------------------------------
def build_hero(c):
    W, H = 1280, 440
    name = c["name"]
    size = max(44, min(96, int(620 / (0.57 * max(len(name), 1)))))
    status = clip(c["status"], 28)
    pill_w = 46 + len(status) * 7.6

    summ = textwrap.wrap(c["summary"], 46)[:3]
    summ_svg = "".join(
        f'<text x="80" y="{308 + i * 28}" font-family="{SANS}" font-size="19" fill="{MUTED}">{e(t)}</text>'
        for i, t in enumerate(summ))

    # code window content
    cx, cy, cw, ch = 700, 56, 500, 336
    lx = cx + 30
    stack3 = [k for g in c["stack"].values() for (k, *_r) in g][:3]
    KW, KEY, STR, PUN, TXT = "#c4a7ff", "#7cc4ff", "#9be3b0", MUTED, TEXT
    maxc = 44

    def s(v, used):  # truncated string literal
        return clip(v, maxc - used - 2)

    lines = [
        (0, [("const ", KW), ("dev", TXT), (" = {", PUN)]),
        (1, [("name: ", KEY), (f'"{s(name, 9)}"', STR), (",", PUN)]),
        (1, [("role: ", KEY), (f'"{s(c["role"], 9)}"', STR), (",", PUN)]),
        (1, [("stack: ", KEY), ("[" + ", ".join(f'"{clip(x, 12)}"' for x in stack3) + "]", STR), (",", PUN)]),
        (1, [("location: ", KEY), (f'"{s(c["location"], 13)}"', STR), (",", PUN)]),
        (1, [("status: ", KEY), (f'"{s(c["status"], 11)}"', GREEN), (",", PUN)]),
        (0, [("};", PUN)]),
    ]
    step, y0 = 33, cy + 96
    defs, body = [], []
    t = 0.5
    last_end_x = lx
    last_y = y0
    for i, (ind, segs) in enumerate(lines):
        y = y0 + i * step
        x = lx + ind * 19.2
        tsp = "".join(f'<tspan fill="{col}">{e(txt)}</tspan>' for txt, col in segs)
        chars = sum(len(txt) for txt, _ in segs)
        dur = 0.35 + chars * 0.012
        defs.append(
            f'<clipPath id="k{i}"><rect x="{cx}" y="{y - 22}" width="0" height="32">'
            f'<animate attributeName="width" from="0" to="{cw}" dur="{dur:.2f}s" begin="{t:.2f}s" fill="freeze"/>'
            f'</rect></clipPath>')
        body.append(f'<text x="{x:.1f}" y="{y}" font-family="{MONO}" font-size="16" clip-path="url(#k{i})">{tsp}</text>')
        t += dur + 0.12
        last_end_x, last_y = x + chars * 9.6, y
    cursor = (f'<rect x="{last_end_x + 4:.1f}" y="{last_y - 15}" width="9" height="19" fill="{BLUE}" opacity="0">'
              f'<set attributeName="opacity" to="1" begin="{t:.2f}s"/>'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')

    out = [svg_open(W, H, f"{name} - {c['role']}")]
    out.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="#0f1a33"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.30"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#a9c1ff"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="0.6" stop-color="{BLUE}" stop-opacity="0.15"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.04"/></pattern>
{''.join(defs)}
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<ellipse cx="930" cy="200" rx="560" ry="330" fill="url(#glow)"/>
<rect y="{H - 4}" width="{W}" height="4" fill="url(#edge)"/>''')

    out.append(f'''<rect x="80" y="86" width="{pill_w:.0f}" height="34" rx="17" fill="{PANEL}" stroke="{LINE}"/>
<circle cx="101" cy="103" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="118" y="108" font-family="{SANS}" font-size="14" font-weight="600" fill="{SOFT}">{e(status)}</text>
<text x="76" y="{200 + (size - 84) // 3}" font-family="{SANS}" font-size="{size}" font-weight="800" letter-spacing="-2" fill="url(#nm)">{e(name)}</text>
<text x="80" y="256" font-family="{SANS}" font-size="30" font-weight="600" fill="{SOFT}">{e(c["role"])}</text>
{summ_svg}''')

    out.append(f'''<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<path d="M{cx} {cy + 44}H{cx + cw}" stroke="{LINE}"/>
<circle cx="{cx + 26}" cy="{cy + 22}" r="6" fill="#ff5f57"/><circle cx="{cx + 46}" cy="{cy + 22}" r="6" fill="#febc2e"/><circle cx="{cx + 66}" cy="{cy + 22}" r="6" fill="#28c840"/>
<text x="{cx + cw / 2}" y="{cy + 27}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">profile.ts</text>
{''.join(body)}
{cursor}
</svg>''')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# project cards
# ---------------------------------------------------------------------------
def build_card(idx, proj, featured):
    name, desc, tech, _url = proj
    w, h = (1200, 230) if featured else (590, 216)
    acc = ACCENTS[idx % len(ACCENTS)]
    ns = 34 if featured else 26
    ds = 18 if featured else 16
    cpl = int((w - 90) / (ds * 0.47))
    lines = textwrap.wrap(desc, cpl)
    maxl = 3 if featured else 3
    if len(lines) > maxl:
        lines = lines[:maxl]
        lines[-1] = clip(lines[-1] + "\u2026", cpl)
    dsvg = "".join(
        f'<text x="38" y="{(96 if featured else 88) + i * (ds + 9)}" font-family="{SANS}" font-size="{ds}" fill="{SOFT}">{e(t)}</text>'
        for i, t in enumerate(lines))
    # tech list with coloured dots
    x = 38
    tsvg = []
    for tname in tech[:6]:
        tsvg.append(f'<circle cx="{x + 4}" cy="{h - 31}" r="4" fill="{acc}"/>'
                    f'<text x="{x + 16}" y="{h - 26}" font-family="{SANS}" font-size="14" fill="{MUTED}">{e(tname)}</text>')
        x += 16 + len(tname) * 7.6 + 22
    tag = (f'<text x="{w - 32}" y="52" text-anchor="end" font-family="{SANS}" font-size="14" font-weight="600" fill="{acc}">Featured</text>'
           if featured else "")
    return f'''{svg_open(w, h, name)}
<defs><clipPath id="c"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath></defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<g clip-path="url(#c)"><rect x="1" y="1" width="6" height="{h - 2}" fill="{acc}"/></g>
<text x="38" y="{58 if featured else 54}" font-family="{SANS}" font-size="{ns}" font-weight="700" fill="{TEXT}">{e(clip(name, 40))}</text>
{tag}
{dsvg}
{''.join(tsvg)}
<text x="{w - 32}" y="{h - 26}" text-anchor="end" font-family="{SANS}" font-size="14" font-weight="600" fill="{acc}">View repository</text>
</svg>'''


# ---------------------------------------------------------------------------
# footer
# ---------------------------------------------------------------------------
def build_footer(c):
    W, H = 1280, 150
    lines = textwrap.wrap(c["footer"], 96)[:2]
    txt = "".join(
        f'<text x="{W / 2}" y="{(86 - 15 * (len(lines) - 1)) + i * 30}" text-anchor="middle" font-family="{SANS}" font-size="22" fill="{SOFT}">{e(t)}</text>'
        for i, t in enumerate(lines))
    return f'''{svg_open(W, H, "Footer")}
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="#0f1a33"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.5" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<rect y="0" width="{W}" height="3" fill="url(#edge)"/>
{txt}
</svg>'''


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------
def shield(label, slug, color, logo_color="white", style="for-the-badge"):
    lab = label.replace("-", "--").replace(" ", "_")
    logo = f"&logo={slug}&logoColor={logo_color}" if slug else ""
    return (f'<img src="https://img.shields.io/badge/{lab}-{color}?style={style}{logo}" alt="{e(label)}"/>')


LINK_STYLE = {
    "LinkedIn": ("0A66C2", "linkedin"), "Email": ("D14836", "gmail"),
    "Portfolio": ("4c8dff", "googlechrome"), "X": ("000000", "x"),
    "GitHub": ("181717", "github"), "YouTube": ("FF0000", "youtube"),
    "Blog": ("FF5722", "rss"), "Medium": ("000000", "medium"),
    "Dev.to": ("0A0A0A", "devdotto"), "Instagram": ("E4405F", "instagram"),
}


def link_badges(links):
    out = []
    for name, url in links.items():
        col, slug = LINK_STYLE.get(name, ("334155", ""))
        out.append(f'<a href="{e(url)}">{shield(name, slug, col, style="for-the-badge")}</a>')
    return " ".join(out)


def build_readme(c):
    h = c["handle"]
    md = []
    md.append(f'<div align="center">\n\n<img src="assets/hero.svg" alt="{e(c["name"])} - {e(c["role"])}" width="100%"/>\n\n'
              f'{link_badges(c["links"])}\n\n</div>\n')

    md.append("## About\n")
    md.append("\n\n".join(c["bio"]) + "\n")
    md.append("| | |\n|:--|:--|")
    for k, v in c["facts"]:
        md.append(f"| **{k}** | {v} |")
    md.append("")

    md.append("## Tech stack\n")
    md.append("| | |\n|:--|:--|")
    for group, items in c["stack"].items():
        b = " ".join(shield(i[0], i[1], i[2], i[3] if len(i) > 3 else "white", "flat-square") for i in items)
        md.append(f"| **{group}** | {b} |")
    md.append("")

    md.append("## Featured projects\n")
    projs = c["projects"][:7]
    if projs:
        md.append(f'<a href="{e(projs[0][3])}"><img src="assets/project-1.svg" alt="{e(projs[0][0])}" width="100%"/></a>\n')
        rest = projs[1:]
        if rest:
            md.append('<table width="100%">')
            for r in range(0, len(rest), 2):
                md.append("<tr>")
                for j in (r, r + 1):
                    if j < len(rest):
                        p = rest[j]
                        md.append(f'<td width="50%"><a href="{e(p[3])}"><img src="assets/project-{j + 2}.svg" alt="{e(p[0])}" width="100%"/></a></td>')
                    else:
                        md.append('<td width="50%"></td>')
                md.append("</tr>")
            md.append("</table>\n")
    md.append(f"More on my [GitHub profile](https://github.com/{h}?tab=repositories).\n")

    md.append("## Experience\n")
    md.append("| Period | Role | Highlights |\n|:--|:--|:--|")
    for period, title, org, what in c["experience"]:
        md.append(f"| {period} | **{title}**, {org} | {what} |")
    md.append("")

    md.append("## Currently\n")
    for k, v in c["currently"]:
        md.append(f"- **{k}:** {v}")
    md.append("")

    theme = "bg_color=0d1527&title_color=4c8dff&text_color=c9d5ea&icon_color=4c8dff&ring_color=4c8dff&border_radius=12&hide_border=true"
    md.append("## GitHub activity\n")
    md.append(f'''<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username={h}&show_icons=true&{theme}" width="49%" alt="GitHub stats"/>
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username={h}&layout=compact&{theme}" width="49%" alt="Top languages"/>

<img src="https://streak-stats.demolab.com?user={h}&background=0d1527&ring=4c8dff&fire=ffb454&currStreakLabel=4c8dff&sideLabels=c9d5ea&currStreakNum=e6ecf7&sideNums=e6ecf7&dates=8b9bb8&stroke=22304d&border=22304d&hide_border=true" width="98%" alt="Contribution streak"/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username={h}&bg_color=0a1020&color=8b9bb8&line=4c8dff&point=e6ecf7&area=true&area_color=4c8dff&hide_border=true&title_color=e6ecf7" width="98%" alt="Contribution graph"/>

</div>
''')

    md.append("## Get in touch\n")
    md.append(f'<div align="center">\n\n{link_badges(c["links"])}\n\n<img src="assets/footer.svg" alt="Thanks for stopping by" width="100%"/>\n\n</div>\n')
    return "\n".join(md)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, "assets")
    os.makedirs(assets, exist_ok=True)
    for f in os.listdir(assets):  # clear old generated files
        if f.endswith(".svg"):
            os.remove(os.path.join(assets, f))
    c = CONFIG
    files = {"hero.svg": build_hero(c), "footer.svg": build_footer(c)}
    for i, p in enumerate(c["projects"][:7]):
        files[f"project-{i + 1}.svg"] = build_card(i, p, i == 0)
    for n, data in files.items():
        with open(os.path.join(assets, n), "w", encoding="utf-8") as fh:
            fh.write(data)
    with open(os.path.join(here, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(build_readme(c))
    print(f"Built {len(files)} SVGs + README.md")


if __name__ == "__main__":
    main()
