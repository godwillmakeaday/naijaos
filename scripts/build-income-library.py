"""Build the income pillar library and portable editions from reviewed Markdown.

Add published child articles in CHILDREN to grow a pillar without changing its URL.
"""
from pathlib import Path
import hashlib
import html
import importlib.util
import json
import math
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('building', ROOT/'scripts/build-building-series.py')
building = importlib.util.module_from_spec(spec)
spec.loader.exec_module(building)
render, esc = building.render, html.escape
BASE = 'https://naijaos.io'
HUB = '/earning-from-nigeria'
PARENT = '/build-from-nigeria/earning-by-creating-global-value'
DATE = '2026-11-01'
DEST = ROOT/'downloads/earning-from-nigeria'
# slug, label, question, buyer pays for, next exploration prompts
META = [
('services','Services','What task can you do well for a particular buyer?','A defined piece of work and your judgment.', ['Define a first service','Prepare a relevant sample','Estimate the full delivery effort']),
('digital-products','Digital products','What can someone purchase and use independently?','A resource that helps complete a task.', ['Choose one recurring task','Test a small resource','Plan corrections and updates']),
('teaching','Teaching','What should a learner become able to do?','Explanation, practice and appropriate feedback.', ['Define a learning outcome','Design a practical exercise','Test a short workshop']),
('subscriptions','Subscriptions','Which need continues after the first month?','Continuing access, research or participation.', ['Identify a recurring need','Choose a sustainable schedule','Learn from renewal and departure']),
('licensing','Licensing','Who could use your original work in their own activities?','Permission for an agreed use of existing work.', ['Identify an organisational use','Describe adaptation and reuse','Prepare an identifiable resource version']),
('advertising','Advertising','Which business has a relevant reason to reach your readers?','An agreed opportunity to present a commercial message.', ['Understand the readership','Define a placement','Report only what the evidence supports']),
('sponsorship','Sponsorship','What useful project could an organisation help make possible?','A defined association and agreed project benefits.', ['Define one sponsorable project','Budget the full commitment','Set editorial responsibilities']),
('affiliate-referrals','Affiliate referrals','Can your experience help a reader assess a tool?','The programme rewards qualifying referrals under its terms.', ['Document actual experience','Check eligibility and programme terms','Explain incentives and limitations']),
('speaking','Speaking','What can your perspective contribute to a particular audience?','A prepared contribution to an event or discussion.', ['Define a talk and its audience','Prepare a representative recording','Clarify preparation, recording and reuse']),
]
# Future entries: {'pillar':'services','slug':'first-offer','title':'...',
# 'source':'content/earning-from-nigeria/services/first-offer.md',
# 'description':'...', 'date':'YYYY-MM-DD'}
# Only completed, reviewed articles belong here. An empty list creates no links.
CHILDREN = []
RELATED = {
 'services':[('/tools/customer-definition','Define the person you want to help'),('/essays/the-price-of-precision','The Price of Precision')],
 'digital-products':[('/new-possibilities#lab','Try the Possibility Lab'),('/build-from-nigeria/project-brief','Use the project brief')],
 'teaching':[('/build-from-nigeria/learning-programming-through-projects','Learning with a project in mind')],
 'subscriptions':[('/build-from-nigeria/finding-an-audience','Finding an audience')],
 'licensing':[('/earning-from-nigeria/digital-products','Develop useful digital products')],
 'advertising':[('/essays/the-price-of-precision','The Price of Precision'),('/earning-from-nigeria/sponsorship','Understand sponsorship')],
 'sponsorship':[('/earning-from-nigeria/advertising','Understand advertising')],
 'affiliate-referrals':[('/build-from-nigeria/why-i-use-hostinger','A personal hosting account and its limits')],
 'speaking':[('/earning-from-nigeria/teaching','Explore teaching as a separate offer')],
}
NOTE = 'These are explorations of possible income routes. The collection does not claim established earnings, customers, sponsors or approved affiliate relationships.'

def link(url, title):
    return f'<a href="{esc(url,quote=True)}">{esc(title)}</a>'

def shell(title, desc, path, body, schema=None, offline=False):
    if offline:
        styles=(ROOT/'assets/possibility-essays.css').read_text()+(ROOT/'assets/building-series.css').read_text()+(ROOT/'assets/income-library.css').read_text()
        styles=re.sub(r"@import[^;]+;",'',styles)
        css='<style>'+styles+'</style><meta name="robots" content="noindex">'
    else:
        css='<link rel="stylesheet" href="/assets/income-library.css">'
    data='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>' if schema and not offline else ''
    nav=f'<header><nav class="wrap" aria-label="Main navigation">{link("/", "naijaOS")}<div class="navlinks">{link(HUB,"Earning from Nigeria")}{link("/how-i-build-from-nigeria","How I Build")}{link("/new-possibilities","New Possibilities")}</div></nav></header>' if not offline else ''
    foot=f'<footer class="wrap"><p>By Paul A. Magaji · {link("/editorial","Editorial standards")} · {link(HUB,"Earning from Nigeria")}</p><p>© 2026 naijaOS · Creating value from Nigeria for the world.</p></footer>' if not offline else ''
    return f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | naijaOS</title><meta name="description" content="{esc(desc,quote=True)}"><link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(desc,quote=True)}"><meta property="og:type" content="{"website" if path==HUB else "article"}"><meta property="og:url" content="{BASE}{path}">{css}{data}</head><body><a class="skip" href="#main">Skip to content</a>{nav}{body}{foot}</body></html>\n'

def downloads():
    return f'<div class="actions">{link("/downloads/earning-from-nigeria/Earning_from_Nigeria.zip","Download the collection · ZIP")}{link("/downloads/earning-from-nigeria/Earning_from_Nigeria.html","Open the reading & print edition")}{link("/downloads/earning-from-nigeria/Earning_from_Nigeria.md","Download the complete text")}</div>'

def build():
    DEST.mkdir(parents=True, exist_ok=True)
    (ROOT/'earning-from-nigeria').mkdir(exist_ok=True)
    chapters=[]
    for n,(slug,label,question,value,prompts) in enumerate(META,1):
        source=ROOT/f'content/earning-from-nigeria/{n:02}-{slug}.md'
        text=source.read_text().strip()
        title,_,body=text.partition('\n')
        body=body.strip()
        if slug=='services': body=body.split('By Paul A. Magaji',1)[1].strip()
        else: body=body.removeprefix('By Paul A. Magaji').strip()
        c=dict(number=n,slug=slug,label=label,title=title.removeprefix('# '),description=question,value=value,prompts=prompts,body=body,url=HUB+'/'+slug,source=str(source.relative_to(ROOT)),minutes=math.ceil(len(body.split())/200),words=len(body.split()),children=[])
        chapters.append(c)
        (DEST/source.name).write_text(text+'\n')
    for child in CHILDREN:
        parent=next(c for c in chapters if c['slug']==child['pillar'])
        assert re.fullmatch(r'[a-z0-9-]+',child['slug'])
        text=(ROOT/child['source']).read_text().strip()
        body=text.partition('\n')[2].strip().removeprefix('By Paul A. Magaji').strip()
        url=parent['url']+'/'+child['slug']
        dest=ROOT/(url.lstrip('/')+'.html');dest.parent.mkdir(parents=True,exist_ok=True)
        schema={'@context':'https://schema.org','@type':'Article','headline':child['title'],'author':{'@type':'Person','name':'Paul A. Magaji'},'isPartOf':{'@type':'CollectionPage','url':BASE+parent['url']},'mainEntityOfPage':BASE+url,'datePublished':child['date']}
        dest.write_text(shell(child['title'],child['description'],url,f'<main id="main" class="reading"><nav class="breadcrumb" aria-label="Breadcrumb">{link(HUB,"Earning from Nigeria")} / {link(parent["url"],parent["label"])}</nav><article><h1>{esc(child["title"])}</h1><p class="byline">By Paul A. Magaji</p><div class="prose">{render(body)}</div></article></main>',schema))
        parent['children'].append({'title':child['title'],'url':url})
    book=[]
    for i,c in enumerate(chapters):
        heads=re.findall(r'^## (.+)$',c['body'],re.M)
        toc='<details class="contents"><summary>In this article</summary><ol>'+''.join(f'<li>{link("#"+building.heading_id(h),h)}</li>' for h in heads)+'</ol></details>'
        further=RELATED[c['slug']]
        related='<section class="article-tools" aria-labelledby="further-reading"><h2 id="further-reading">Continue the inquiry</h2><ul>'+''.join(f'<li>{link(u,t)}</li>' for u,t in further)+'</ul></section>'
        if c['children']:
            related+='<section class="article-tools"><h2>More on '+esc(c['label'].lower())+'</h2><ul>'+''.join('<li>'+link(k['url'],k['title'])+'</li>' for k in c['children'])+'</ul></section>'
        related+='<details class="contents"><summary>Questions to develop next</summary><ul>'+''.join('<li>'+esc(p)+'</li>' for p in c['prompts'])+'</ul><p>These are directions for further inquiry.</p></details>'
        prev=chapters[i-1] if i else None
        nxt=chapters[i+1] if i+1<len(chapters) else None
        sequence='<nav class="sequence" aria-label="Reading sequence">'+(link(prev['url'],'← '+prev['label']) if prev else link(HUB,'← All nine routes'))+(link(nxt['url'],nxt['label']+' →') if nxt else link(HUB,'Back to all nine routes →'))+'</nav>'
        breadcrumb=f'<nav class="breadcrumb" aria-label="Breadcrumb">{link("/","NaijaOS")} / {link(HUB,"Earning from Nigeria")} / <span>{esc(c["label"])}</span></nav>'
        body=f'<main id="main" class="reading">{breadcrumb}<article><p class="kicker">{c["number"]:02} / 09 · {esc(c["label"])}</p><h1>{esc(c["title"])}</h1><p class="deck">{esc(c["description"])}</p><p class="byline">By Paul A. Magaji <span>· {c["minutes"]} min read · Commercial exploration</span></p>{toc}<div class="prose">{render(c["body"])}</div>{related}<aside class="article-tools"><h2>Keep this article</h2><p><a href="/downloads/earning-from-nigeria/{c["number"]:02}-{c["slug"]}.md" download>Download this article · Markdown</a></p><p>{link("/downloads/earning-from-nigeria/Earning_from_Nigeria.html#chapter-"+str(c["number"]),"Open this article in the reading & print edition")}</p></aside></article>{sequence}</main>'
        schema={'@context':'https://schema.org','@type':'Article','headline':c['title'],'description':c['description'],'author':{'@type':'Person','name':'Paul A. Magaji'},'mainEntityOfPage':BASE+c['url'],'datePublished':DATE,'dateModified':DATE,'inLanguage':'en','isPartOf':{'@type':'CreativeWorkSeries','name':'Earning from Nigeria','url':BASE+HUB}}
        (ROOT/(c['url'].lstrip('/')+'.html')).write_text(shell(c['title'],c['description'],c['url'],body,schema))
        # Prefix heading IDs in the combined edition so the nine chapters remain unique.
        content=render(c['body'],1)
        content=re.sub(r'id="([^"]+)"',lambda m:f'id="chapter-{c["number"]}-{m[1]}"',content)
        book.append(f'<article class="book-chapter" id="chapter-{c["number"]}"><p class="kicker">{c["number"]:02} / {esc(c["label"])}</p><h2>{esc(c["title"])}</h2><div class="prose">{content}</div></article>')
    nav=''.join(f'<a href="#route-{c["slug"]}"><span>{c["number"]:02}</span> {esc(c["label"])}</a>' for c in chapters)
    cards=''.join(f'<section class="pillar-card" id="route-{c["slug"]}" aria-labelledby="title-{c["slug"]}"><p class="kicker">{c["number"]:02} / {esc(c["label"])}</p><h3 id="title-{c["slug"]}">{link(c["url"],c["title"])}</h3><p>{esc(c["description"])}</p><p class="meta">{c["minutes"]} min read · Pillar article</p>{link(c["url"],"Explore "+c["label"].lower()+" →")}</section>' for c in chapters)
    table='<div class="table-scroll" role="region" aria-label="Compare the nine income routes" tabindex="0"><table><caption>What is being paid for?</caption><thead><tr><th scope="col">Route</th><th scope="col">The commercial exchange</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+link(c['url'],c['label'])+'</th><td>'+esc(c['value'])+'</td></tr>' for c in chapters)+'</tbody></table></div>'
    body=f'''<main id="main"><div class="wrap"><nav class="breadcrumb hub-crumb" aria-label="Breadcrumb">{link('/', 'NaijaOS')} / <span>Earning from Nigeria</span></nav><section class="hero income-hero"><div><p class="kicker">A growing collection / By Paul A. Magaji</p><h1>Useful work.<br><em>Wider possibilities.</em></h1><p class="deck">Earning from Nigeria by creating value for the world.</p><p class="intro">Nine ways knowledge, judgment and practical skills could become income. Explore what someone pays for, the work each route requires and a manageable way to begin.</p><div class="actions"><a class="button" href="{HUB}/services">Start with services →</a>{link('#pillars','Choose a route ↓')}</div></div><aside class="hero-note"><p>What would make someone elsewhere willing to pay for something I create?</p><div class="edition">09 pillar articles<br>Services · Resources · Audiences<br>November 2026</div></aside></section><aside class="evidence"><b>Commercial possibilities, examined at their actual scope.</b><p>{NOTE}</p></aside><div class="library-layout"><aside class="route-sidebar"><nav aria-label="Nine income pillars"><p class="kicker">Explore the routes</p>{nav}{link('#keep-the-collection','Download the collection ↓')}</nav></aside><div class="library-main"><section class="collection" id="reading-guide"><p class="kicker">Choose a starting point</p><h2>Begin with the value you can provide.</h2><div class="routes">{link(HUB+'/services','I can help with a particular task → Services')}{link(HUB+'/digital-products','I can create a reusable resource → Digital products')}{link(HUB+'/teaching','I can explain and demonstrate → Teaching')}{link(HUB+'/subscriptions','I can serve a continuing need → Subscriptions')}</div><p>Want the full picture first? {link(PARENT,'Read the parent essay: Earning from Nigeria by Creating Value for the World')}.</p></section><section class="collection" id="pillars"><p class="kicker">The nine pillars</p><h2>One question. Nine routes to explore.</h2><div class="pillar-grid">{cards}</div></section><section class="collection"><p class="kicker">Compare the possibilities</p><h2>Each route makes a different promise.</h2>{table}<p class="note">Choose a route you can deliver responsibly. Developing several possibilities does not require launching them all at once.</p></section><section class="collection" id="keep-the-collection"><p class="kicker">A portable edition</p><h2>Read here. Keep the complete collection.</h2><p>All nine articles in individual text files, a combined Markdown edition and a self-contained reading edition with print styling. No account is required.</p>{downloads()}</section><section class="collection"><p class="kicker">Put the questions to work</p><h2>Define who you want to help.</h2><p>Use the Customer Definition Canvas to examine one audience and one need. Then give the first experiment a boundary with the project brief.</p><div class="actions">{link('/tools/customer-definition','Open the Customer Definition Canvas →')}{link('/build-from-nigeria/project-brief','Use the project brief →')}</div><p>{link('/essays/the-price-of-precision','Read The Price of Precision')} · {link('/how-i-build-from-nigeria','Explore How I Build from Nigeria')}</p></section></div></div></div></main>'''
    schema={'@context':'https://schema.org','@type':'CollectionPage','name':'Earning from Nigeria','description':'Nine pillar articles on creating value for the world from Nigeria.','url':BASE+HUB,'author':{'@type':'Person','name':'Paul A. Magaji'},'mainEntity':{'@type':'ItemList','numberOfItems':9,'itemListElement':[{'@type':'ListItem','position':c['number'],'name':c['title'],'url':BASE+c['url']} for c in chapters]}}
    (ROOT/'earning-from-nigeria.html').write_text(shell('Earning from Nigeria','Explore nine income routes: services, products, teaching, subscriptions, licensing, advertising, sponsorship, affiliate referrals and speaking.',HUB,body,schema))
    guide='# Earning from Nigeria\n\n## Creating value for the world\n\nBy Paul A. Magaji\n\n'+NOTE+'\n\nRead in order or choose the route closest to work you can deliver. These are general commercial explorations, with examples and plans described at their actual scope.\n\n## Reading order\n\n'+'\n'.join(f'{c["number"]}. {c["title"]}' for c in chapters)+'\n'
    (DEST/'Earning_from_Nigeria.md').write_text(guide+'\n\n'+'\n\n---\n\n'.join((ROOT/c['source']).read_text().strip() for c in chapters)+'\n')
    toc='<nav aria-label="Reading order"><h2>Reading order</h2><ol>'+''.join('<li>'+link('#chapter-'+str(c['number']),c['title'])+'</li>' for c in chapters)+'</ol></nav>'
    bookbody='<main id="main" class="reading book"><p class="kicker">NaijaOS / Complete reading edition</p><h1>Earning from Nigeria</h1><p class="deck">Creating value for the world</p><p>By Paul A. Magaji</p><p>'+NOTE+'</p><p>This edition opens offline. Use your browser’s Print command to print or save as PDF.</p>'+toc+''.join(book)+'</main>'
    (DEST/'Earning_from_Nigeria.html').write_text(shell('Earning from Nigeria — Reading Edition','Nine complete pillar articles by Paul A. Magaji.',HUB,bookbody,offline=True))
    (DEST/'README.md').write_text(guide+'\nOpen Earning_from_Nigeria.html in a browser to read offline or print. The individual Markdown files contain all nine articles. No accounts, scripts or external stylesheets are required by the reading edition.\n')
    archive=DEST/'Earning_from_Nigeria.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DEST.iterdir()):
            if p.suffix in ('.md','.html'):
                info=zipfile.ZipInfo(p.name,(2026,11,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
    catalogue=[{k:v for k,v in c.items() if k!='body'} for c in chapters]
    (ROOT/'docs/income-library-catalog.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'docs/income-library-package.json').write_text(json.dumps({'date':DATE,'articles':9,'words':sum(c['words'] for c in chapters),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2)+'\n')
    sitemap=ROOT/'sitemap.xml';text=sitemap.read_text()
    for url in [HUB]+[c['url'] for c in chapters]+[k['url'] for c in chapters for k in c['children']]:
        if f'<loc>{BASE}{url}</loc>' not in text:
            text=text.replace('</urlset>',f'<url><loc>{BASE}{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
    sitemap.write_text(text)
    print(f'Built {len(chapters)} pillars, collection hub and portable editions; {sum(c["words"] for c in chapters):,} words; {archive.stat().st_size:,}-byte archive.')

if __name__=='__main__':
    build()
