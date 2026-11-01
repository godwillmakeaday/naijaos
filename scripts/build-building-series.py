"""Build the NaijaOS collection and portable reading edition using Python stdlib."""
from pathlib import Path
import html
import json
import math
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/how-i-build-from-nigeria/series.md'
DEST = ROOT / 'downloads/how-i-build-from-nigeria'
BASE = 'https://naijaos.io'
HUB = '/how-i-build-from-nigeria'
DATE = '2026-11-01'

# slug, description, reading section, evidence classification, evidence note
META = [
('building-from-nigeria-for-the-world', 'Give your knowledge a public home and a practical purpose.', 0, 'Personal reflection', ''),
('why-i-use-hostinger', 'A personal account of affordability, responsiveness and the limits of a recommendation.', 1, 'Personal account', 'Subjective experience, not a hosting benchmark. No current prices or server location are asserted.'),
('my-truehost-domain-experience', 'What an unresolved domain connection taught me about evidence and technical responsibility.', 1, 'Historical account', 'Provider corrected from Bluehost to Truehost in the recovered conversation record. The record does not confirm a successful resolution or establish the cause.'),
('domain-troubleshooting-lessons', 'A more orderly approach to recording failures, changes and results.', 1, 'Retrospective method', 'A companion to an unresolved investigation, not a verified fix or a current DNS configuration guide.'),
('using-ai-to-build-websites', 'Move from an idea to a bounded brief, a visible version and a checked result.', 2, 'Documented project case', 'Includes the live Possibility Lab, fixed source links and a dated synthetic browser demonstration. Not an independent outcome study.'),
('building-with-chatgpt', 'Purpose, technical assistance and the decisions that remain mine.', 2, 'Documented collaboration', 'Distinguishes author direction from AI-assisted drafting, implementation and checking. Source records do not independently attribute every contribution.'),
('evaluating-lovable', 'The questions I would test before committing a project to another platform.', 2, 'Planned evaluation', 'No completed Lovable test is documented here. This is an evaluation plan, not a product review or a claim about current capabilities.'),
('learning-react-with-ai', 'Technical understanding as a way to direct, assess and maintain the work.', 3, 'Learning direction', 'A learning goal, not a claim of React proficiency or a technical tutorial.'),
('learning-programming-through-projects', 'Use a manageable project to give study, practice and questions a direction.', 3, 'Learning approach', ''),
('from-preview-to-live-website', 'The work between a convincing first version and a maintained public website.', 4, 'Documented release case', 'Links to a fixed release, reproducible checks and dated publication results. Availability checks do not establish reader impact or full accessibility.'),
('finding-an-audience', 'Make useful work recognisable and learn why readers return.', 4, 'Audience development plan', 'An approach to test, not evidence of a large audience or proven traffic growth.'),
('earning-by-creating-global-value', 'Develop a clear offer, demonstrate capability and plan dependable delivery.', 5, 'Commercial direction', 'No international earnings, paid customers or active affiliate partnership are claimed.'),
('learning-to-use-ai-well', 'Context, evidence and growing capability in a Nigerian builder’s account.', 5, 'Closing reflection', ''),
]
GROUPS = [
('The ambition', 'Begin with useful work and give it somewhere to live.'),
('Platforms & real difficulties', 'Examine experience, attribution and the limits of what the record proves.'),
('Building with AI', 'Define the task, direct the collaboration and evaluate new tools.'),
('Learning for greater control', 'Connect technical study with something you want to build.'),
('Publication & audience', 'Make the work dependable, discoverable and worth returning to.'),
('Value & responsibility', 'Explore commercial possibilities while developing your own capability.'),
]

def esc(text):
    return html.escape(text, quote=True)

def inline(text):
    # Allow only ordinary HTTPS links. Escape all prose and attributes.
    out, start = [], 0
    for match in re.finditer(r'\[([^\]\n]+)\]\((https://[^\s)]+)\)', text):
        out.append(esc(text[start:match.start()]))
        out.append('<a href="' + esc(match.group(2)) + '">' + esc(match.group(1)) + '</a>')
        start = match.end()
    out.append(esc(text[start:]))
    return ''.join(out)

def heading_id(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def render(md, offset=0):
    out, paragraphs, items = [], [], []
    def flush():
        if paragraphs:
            out.append('<p>' + inline(' '.join(paragraphs)) + '</p>')
            paragraphs.clear()
        if items:
            out.append('<ul>' + ''.join('<li>' + inline(s) + '</li>' for s in items) + '</ul>')
            items.clear()
    for line in md.splitlines():
        if line.startswith('#'):
            flush()
            n = len(line) - len(line.lstrip('#'))
            text = line[n:].strip()
            level = min(6, n + offset)
            out.append(f'<h{level} id="{heading_id(text)}">{esc(text)}</h{level}>')
        elif line.startswith('- '):
            if paragraphs:
                flush()
            items.append(line[2:])
        elif not line.strip():
            flush()
        else:
            if items:
                flush()
            paragraphs.append(line.strip())
    flush()
    return '\n'.join(out)

def shell(title, description, path, body, schema=None):
    structured = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('</', '<\\/') + '</script>' if schema else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | naijaOS</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="{'article' if '/build-from-nigeria/' in path else 'website'}"><meta property="og:url" content="{BASE}{path}">
<link rel="stylesheet" href="/assets/building-series.css">{structured}</head>
<body><a class="skip" href="#main">Skip to content</a><header><nav class="wrap" aria-label="Main navigation"><a class="brand" href="/">naija<b>OS</b></a><div class="navlinks"><a href="{HUB}">How I Build</a><a href="/why-cant-we">Possibility essays</a><a href="/new-possibilities">New Possibilities</a></div></nav></header>
{body}
<footer class="wrap"><p><a href="{HUB}">How I Build from Nigeria</a> · By Paul A. Magaji · <a href="/editorial">Editorial standards</a></p><p>Personal accounts, working methods and clearly identified plans. No affiliate purchase links or sponsored partnerships are included in this collection. Any later paid relationship should be disclosed beside the relevant recommendation.</p><p>© 2026 naijaOS · <a href="/">Back to NaijaOS</a></p></footer></body></html>'''

def download_links():
    return '<div class="actions"><a class="button" href="/downloads/how-i-build-from-nigeria/How_I_Build_from_Nigeria.zip" download>Download the collection · ZIP</a><a href="/downloads/how-i-build-from-nigeria/How_I_Build_from_Nigeria.html">Open the reading &amp; print edition</a><a href="/downloads/how-i-build-from-nigeria/How_I_Build_from_Nigeria.md" download>Download text · Markdown</a></div>'

def build():
    DEST.mkdir(parents=True, exist_ok=True)
    (ROOT / 'build-from-nigeria').mkdir(exist_ok=True)
    chunks = SOURCE.read_text().strip().split('\n---ARTICLE---\n')
    assert len(chunks) == len(META) == 13
    chapters = []
    for number, (chunk, meta) in enumerate(zip(chunks, META), 1):
        title, _, content = chunk.strip().partition('\n')
        slug, deck, group, status, note = meta
        chapters.append(dict(number=number, title=title.removeprefix('# '), content=content.strip(), slug=slug, description=deck, group=group, status=status, note=note, url='/build-from-nigeria/' + slug, words=len(content.split()), minutes=max(2, math.ceil(len(content.split())/200))))
    guide = '''# How I Build from Nigeria
## Websites, AI, learning and an international presence
By Paul A. Magaji

I am exploring how someone working from Nigeria can turn knowledge, professional experience and ideas into useful work that reaches people elsewhere. This series follows the process: platforms, attempts, learning, publication and the commercial possibilities that may follow.

Read in sequence or begin with the question that brought you here. For a first website, start with articles 1, 2 and 10. For AI-assisted building, read 5 and 6. For technical learning, turn to 8 and 9. For audience and income, read 11 and 12. Article 13 draws the method together.

These are edited personal accounts and working approaches, not independently benchmarked product reviews. The Truehost account remains unresolved in the recovered record. Lovable is a planned evaluation. Audience and commercial articles describe directions to test, not established traffic or earnings.

The collection contains no affiliate purchase links or sponsored partnerships. Any later paid relationship should be disclosed beside the relevant recommendation.
'''
    source_book = guide + '\n\n## Reading order\n\n' + '\n'.join(f'{c["number"]}. {c["title"]}' for c in chapters)
    blocks = []
    for c in chapters:
        n, title = c['number'], c['title']
        md = '# ' + title + '\n\nBy Paul A. Magaji\n\n' + (('Editorial context: ' + c['note'] + '\n\n') if c['note'] else '') + c['content'] + '\n'
        (DEST / f'{n:02}-{c["slug"]}.md').write_text(md)
        source_book += '\n\n---\n\n' + md
        sections = re.findall(r'^## (.+)$', c['content'], re.M)
        toc = '<details class="contents"><summary>In this article</summary><ol>' + ''.join(f'<li><a href="#{heading_id(s)}">{esc(s)}</a></li>' for s in sections) + '</ol></details>'
        note = f'<aside class="evidence" aria-label="Editorial context"><b>{esc(c["status"])}</b><p>{esc(c["note"])}</p></aside>' if c['note'] else ''
        prev = chapters[n-2] if n > 1 else None
        nxt = chapters[n] if n < 13 else None
        previous = f'<a rel="prev" href="{prev["url"]}"><span>← Previous / {prev["number"]:02}</span>{esc(prev["title"])}</a>' if prev else f'<a href="{HUB}"><span>← The collection</span>Introduction &amp; reading guide</a>'
        following = f'<a rel="next" href="{nxt["url"]}"><span>Next / {nxt["number"]:02} →</span>{esc(nxt["title"])}</a>' if nxt else f'<a href="/build-from-nigeria/project-brief"><span>Put the series to work →</span>Your first project brief</a>'
        figure = '<figure class="project-evidence"><img src="/assets/building-evidence/possibility-lab-demonstration.jpg" alt="Possibility Lab showing fictional shop entries and the resulting user-authored brief" width="1348" height="926" loading="lazy"><figcaption>Desktop demonstration, 1 November 2026. Fictional entries and generated brief; no customer study. <a href="/downloads/how-i-build-from-nigeria/Verification_Record_20261101.json">Read the verification record</a>.</figcaption></figure>' if n == 5 else ''
        income_collection = '<aside class="article-tools"><h2>Explore the nine income routes</h2><p>Services, digital products, teaching, subscriptions, licensing, advertising, sponsorship, affiliate referrals and speaking each have a full pillar article.</p><p><a href="/earning-from-nigeria">Open Earning from Nigeria →</a></p></aside>' if n == 12 else ''
        body = f'''<main id="main" class="reading"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HUB}">How I Build from Nigeria</a><span aria-hidden="true"> / </span><span>Article {n:02}</span></nav><article><p class="kicker">{esc(GROUPS[c['group']][0])} / {n:02} of 13</p><h1>{esc(title)}</h1><p class="deck">{esc(c['description'])}</p><p class="byline">By Paul A. Magaji <span>· {c['minutes']} min read · {esc(c['status'])}</span></p>{note}{toc}<div class="prose">{render(c['content'])}</div>{figure}{income_collection}<aside class="article-tools"><h2>Keep the work</h2><p><a href="/downloads/how-i-build-from-nigeria/{n:02}-{c['slug']}.md" download>Download this article · Markdown</a></p><p><a href="/build-from-nigeria/project-brief">Use the companion project brief</a> or <a href="/downloads/how-i-build-from-nigeria/How_I_Build_from_Nigeria.html#chapter-{n}">open the print edition at this article</a>.</p></aside></article><nav class="sequence" aria-label="Reading sequence">{previous}{following}</nav></main>'''
        schema = {'@context':'https://schema.org','@type':'Article','headline':title,'description':c['description'],'author':{'@type':'Person','name':'Paul A. Magaji'},'isPartOf':{'@type':'CreativeWorkSeries','name':'How I Build from Nigeria','url':BASE+HUB},'mainEntityOfPage':BASE+c['url'],'dateModified':DATE,'inLanguage':'en'}
        (ROOT / ('build-from-nigeria/' + c['slug'] + '.html')).write_text(shell(title,c['description'],c['url'],body,schema))
        blocks.append(f'<article class="book-chapter" id="chapter-{n}"><p class="kicker">Article {n:02} / {esc(c["status"])}</p><h2>{esc(title)}</h2>{("<p class=\"evidence\">"+esc(c["note"])+"</p>") if c["note"] else ""}<div class="prose">{render(c["content"],1)}</div></article>')
    (DEST / 'How_I_Build_from_Nigeria.md').write_text(source_book+'\n')
    cards = []
    for group, (name, description) in enumerate(GROUPS):
        rows = ''.join(f'<li><a href="{c["url"]}"><span class="number">{c["number"]:02}</span><div><span class="status">{esc(c["status"])}</span><h3>{esc(c["title"])}</h3><p>{esc(c["description"])}</p><span class="meta">{c["minutes"]} min read · Full article</span></div><span aria-hidden="true">↗</span></a></li>' for c in chapters if c['group']==group)
        cards.append(f'<section class="collection" id="part-{group+1}"><p class="kicker">Part {group+1:02}</p><h2>{esc(name)}</h2><p class="section-deck">{esc(description)}</p><ol class="essay-list" start="{next(c["number"] for c in chapters if c["group"]==group)}">{rows}</ol></section>')
    nav = ''.join(f'<a href="#part-{i+1}">{i+1:02} / {esc(g[0])}</a>' for i,g in enumerate(GROUPS))
    body = f'''<main id="main"><div class="wrap"><section class="hero"><div><p class="kicker">NaijaOS / A builder’s notebook</p><h1>How I Build<br><em>from Nigeria.</em></h1><p class="deck">Websites, AI, learning and an international presence.</p><p class="intro">Thirteen articles by Paul A. Magaji on turning knowledge into work people can find, use and assess. The platforms, the difficulties, the learning—and the commercial possibilities still to test.</p><div class="actions"><a class="button" href="{chapters[0]['url']}">Start with the first article →</a><a href="#reading-guide">Choose your reading route ↓</a></div></div><aside class="hero-note"><span class="kicker">The working question</span><p>How does useful work travel from where I am to the people who need it?</p><div class="edition">13 articles<br>By Paul A. Magaji<br>Edited collection · November 2026</div></aside></section><nav class="parts" aria-label="Collection sections">{nav}</nav><section class="collection"><p class="kicker">Continue the commercial inquiry</p><h2>Earning from Nigeria</h2><p>Nine pillar articles examine services, products, teaching, subscriptions, licensing and earning through an audience. Each begins with the value someone receives.</p><a href="/earning-from-nigeria">Explore the nine income routes →</a></section><section class="case-studies" aria-labelledby="case-studies-title"><p class="kicker">Three accounts with an inspectable trail</p><h2 id="case-studies-title">See what was built.<br>Examine what was checked.</h2><div class="routes"><a href="/build-from-nigeria/using-ai-to-build-websites#case-record-the-possibility-lab"><b>05 / An idea becomes a working worksheet</b><span>Live task · source · demonstration · download</span></a><a href="/build-from-nigeria/building-with-chatgpt#case-record-preserving-naijaos-while-adding-a-section"><b>06 / Author direction and AI-assisted work</b><span>Project decisions · source trail · attribution limits</span></a><a href="/build-from-nigeria/from-preview-to-live-website#case-record-publishing-this-collection"><b>10 / Drafts become a public collection</b><span>Release record · reproducible checks · limits</span></a></div><p class="meta">Project documentation supports these accounts. Independent reader outcomes, audience growth and commercial results remain unestablished.</p></section><section class="reading-guide" id="reading-guide"><p class="kicker">Introduction &amp; reading guide</p><h2>Begin with the question you have.</h2><p>I am exploring how someone working from Nigeria can turn knowledge, professional experience and ideas into useful work that reaches people elsewhere. These articles connect the ambition to the ordinary work of building, checking, learning and maintaining.</p><div class="routes"><a href="{chapters[0]['url']}"><b>I want to build a first website</b><span>Read 1 → 2 → 10</span></a><a href="{chapters[4]['url']}"><b>I want to understand AI-assisted work</b><span>Read 5 → 6 → 13</span></a><a href="{chapters[7]['url']}"><b>I want to learn enough to take control</b><span>Read 8 → 9</span></a><a href="{chapters[10]['url']}"><b>I am thinking about audience and income</b><span>Read 11 → 12</span></a></div></section><aside class="evidence collection-note"><b>Read the experience at its actual scope.</b><p>These are personal accounts, working methods and plans. The Truehost investigation has no confirmed resolution in the recovered record. Lovable is a planned evaluation. No hosting benchmark, large audience or international earnings are claimed.</p></aside>{''.join(cards)}<section class="collection" id="reading-edition"><p class="kicker">The complete edition</p><h2>Read it here. Keep it with you.</h2><p>The ZIP contains all 13 articles as individual text files, the introduction and reading order in a combined Markdown edition, an offline HTML edition with print styling, a companion project brief, and the dated worksheet demonstration and verification record. No account or email address is needed.</p>{download_links()}<p class="meta">The HTML file inside the ZIP opens offline. Use your browser’s Print command to print or save it as PDF.</p></section><section class="collection"><p class="kicker">From reading to a first attempt</p><h2>Give your next project a boundary.</h2><p>Define one audience, one task and the evidence that would show a useful result. Keep track of costs, changes and unresolved questions.</p><div class="actions"><a class="button" href="/build-from-nigeria/project-brief">Open the project brief →</a><a href="/new-possibilities#lab">Explore the Possibility Lab</a></div><p class="meta">Continue the wider inquiry through <a href="/why-cant-we">Why can’t we?</a> and <a href="/new-possibilities">New Possibilities</a>.</p></section></div></main>'''
    schema = {'@context':'https://schema.org','@type':'CollectionPage','name':'How I Build from Nigeria','description':'Thirteen personal essays on websites, AI, learning, publishing and creating useful work from Nigeria.','url':BASE+HUB,'author':{'@type':'Person','name':'Paul A. Magaji'},'mainEntity':{'@type':'ItemList','numberOfItems':13,'itemListElement':[{'@type':'ListItem','position':c['number'],'name':c['title'],'url':BASE+c['url']} for c in chapters]}}
    (ROOT / 'how-i-build-from-nigeria.html').write_text(shell('How I Build from Nigeria','Thirteen articles by Paul A. Magaji on websites, AI, learning, publishing and creating value from Nigeria.',HUB,body,schema))
    brief = '''# Your First Project Brief

Companion to How I Build from Nigeria, by Paul A. Magaji.

Use this on paper or copy it into a document. This page does not collect or save answers.

## Purpose
Who is the project for? What difficulty are they trying to address? What should they be able to do after using it?

## The smallest useful version
What is the single task you will support first? What will you deliberately leave for later? Which existing work must be preserved?

## Resources and costs
Which skills, tools, time and assistance are needed? Record initial and continuing costs separately. Date any prices or terms you check.

## Evidence and responsibility
Which claims need sources? What information must remain private? Who might rely on the result, and what limitations should be visible?

## The first test
Describe the exact task you will attempt. What observable result would count as success? What would make you revise or stop?

## Change record
Record the date, starting state, reason for the change, intervention and observed result. Keep unresolved questions separate from confirmed findings.

## Publication and maintenance
Which version is being reviewed? Check the links, main tasks, mobile use and any downloads. What remains unverified? Who will correct problems, and how can the change be withdrawn if necessary?

## Reflection
What can you now do or explain? What still requires help? What is the next useful step?
'''
    (DEST / 'Project_Brief.md').write_text(brief)
    brief_body = f'<main id="main" class="reading"><p class="kicker">How I Build from Nigeria / Companion</p><h1>Your first project brief</h1><p class="deck">One audience. One task. An observable result.</p><p>Print this page or copy the prompts into a document. There is no form, no account and no collection of answers on this page.</p><div class="actions"><a class="button" href="/downloads/how-i-build-from-nigeria/Project_Brief.md" download>Download the brief · Markdown</a><a href="{HUB}">Back to the series</a></div><div class="prose brief-prompts">{render("## Purpose"+brief.split("## Purpose",1)[1])}</div><p class="note">Use your browser’s Print command to print or save as PDF.</p></main>'
    (ROOT / 'build-from-nigeria/project-brief.html').write_text(shell('Your first project brief','A printable companion for defining, testing and maintaining a small digital project.','/build-from-nigeria/project-brief',brief_body))
    # This edition deliberately embeds its styles and uses fragment links so it works offline.
    book_css = '''body{max-width:780px;margin:auto;padding:32px 24px;color:#172c25;background:#f4f3ec;font:19px/1.75 Georgia,serif}a{color:inherit;text-underline-offset:3px}a:focus-visible{outline:3px solid #9b580b;outline-offset:4px}h1{font-size:clamp(36px,7vw,62px);line-height:1.1}h2{font-size:32px;line-height:1.25}h3{font-size:24px;line-height:1.3;margin-top:32px}h1,h2,h3{overflow-wrap:anywhere}.book-chapter{border-top:1px solid #ccd2c2;margin-top:60px;padding-top:28px}.kicker,.evidence,.book-nav{font:14px/1.7 Arial,sans-serif}.evidence{padding:16px;border-left:3px solid #51685e}.book-nav li{margin-bottom:12px}.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:12px;background:white;padding:12px}@media print{body{max-width:none;padding:0;background:white;color:black;font-size:11pt}.book-chapter{break-before:page;border:0}h2,h3{break-after:avoid}.web-only,.skip{display:none}a{color:black;text-decoration:none}}'''
    book_toc = ''.join(f'<li><a href="#chapter-{c["number"]}">{esc(c["title"])}</a></li>' for c in chapters)
    book = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>How I Build from Nigeria — Reading Edition</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{HUB}"><style>{book_css}</style></head><body><a class="skip" href="#main">Skip to content</a><main id="main">{render(guide)}<p class="web-only">This edition opens offline. Use your browser’s Print command to print or save as PDF. <a href="{BASE}{HUB}">Visit the online collection</a>.</p><nav class="book-nav" aria-label="Reading order"><h2>Reading order</h2><ol>{book_toc}</ol><a href="#project-brief">Companion project brief</a></nav>{"".join(blocks)}<section class="book-chapter" id="project-brief">{render(brief,1)}</section></main></body></html>'
    (DEST / 'How_I_Build_from_Nigeria.html').write_text(book)
    catalogue = [{k:v for k,v in c.items() if k != 'content'} for c in chapters]
    (ROOT / 'docs/building-series-catalog.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n')
    archive = DEST / 'How_I_Build_from_Nigeria.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DEST.iterdir()):
            if p.suffix in ('.md','.html','.txt','.json'):
                info = zipfile.ZipInfo(p.name, (2026,11,1,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info,p.read_bytes())
    print(f'Built {len(chapters)} articles, collection, companion brief and offline edition; {sum(c["words"] for c in chapters):,} article words; {archive.stat().st_size:,}-byte ZIP.')

if __name__ == '__main__':
    build()
