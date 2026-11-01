"""Check publication integrity: routes, fragments, sequence, content and downloads."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import collections
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.h1, self.scripts = [], [], 0, 0
        self.canonical = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'script' and a.get('type') != 'application/ld+json': self.scripts += 1
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a['href'])

def resolve(path):
    p = ROOT / unquote(path.lstrip('/'))
    if p.is_file(): return p
    if p.with_suffix('.html').is_file(): return p.with_suffix('.html')
    if (p/'index.html').is_file(): return p/'index.html'
    raise AssertionError(f'Missing local destination: {path}')

catalog = json.loads((ROOT/'docs/building-series-catalog.json').read_text())
assert len(catalog) == 13
assert [c['number'] for c in catalog] == list(range(1,14))
assert len({c['title'] for c in catalog}) == len({c['url'] for c in catalog}) == 13
pages = [ROOT/'how-i-build-from-nigeria.html',ROOT/'build-from-nigeria/project-brief.html'] + [resolve(c['url']) for c in catalog]
count = 0
for file in pages:
    page = Page(file)
    assert page.h1 == 1, (file,'heading')
    assert len(page.ids) == len(set(page.ids)), (file,'duplicate IDs')
    assert len(page.canonical) == 1 and page.canonical[0].startswith('https://naijaos.io/'), (file,'canonical')
    assert page.scripts == 0, (file,'unnecessary executable scripts')
    assert 'main' in page.ids
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc: continue
        target = file if not url.path else resolve(url.path)
        if url.fragment:
            assert unquote(url.fragment) in Page(target).ids, (file,href,'missing fragment')
        count += 1
for index,c in enumerate(catalog):
    text = resolve(c['url']).read_text()
    assert c['words'] > 400, (c['title'],'article too short')
    if index: assert f'rel="prev" href="{catalog[index-1]["url"]}"' in text
    if index < 12: assert f'rel="next" href="{catalog[index+1]["url"]}"' in text

ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [n.text for n in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
assert len(urls) == len(set(urls)), 'duplicate sitemap routes'
for route in ['/how-i-build-from-nigeria','/build-from-nigeria/project-brief']+[c['url'] for c in catalog]:
    assert 'https://naijaos.io'+route in urls, route
dest = ROOT/'downloads/how-i-build-from-nigeria'
with zipfile.ZipFile(dest/'How_I_Build_from_Nigeria.zip') as z:
    assert z.testzip() is None
    assert len(z.namelist()) == 18, z.namelist()
    for name in z.namelist():
        assert z.read(name) == (dest/name).read_bytes(), name
    for c in catalog:
        name=f'{c["number"]:02}-{c["slug"]}.md'
        assert name in z.namelist()
    book = z.read('How_I_Build_from_Nigeria.html').decode()
    assert '<link rel="stylesheet"' not in book, 'offline edition has external CSS dependency'
    assert '<script' not in book, 'offline edition should not require JavaScript'
    assert all(f'id="chapter-{n}"' in book for n in range(1,14))
    assert '<h2 id="your-first-project-brief">' in book
hub = (ROOT/'how-i-build-from-nigeria.html').read_text()
assert hub.count('class="number"') == 13
assert 'Planned evaluation' in resolve(catalog[6]['url']).read_text()
assert 'does not confirm a successful resolution' in resolve(catalog[2]['url']).read_text()
for file in ['index.html','why-cant-we.html','new-possibilities.html']:
    assert '/how-i-build-from-nigeria' in (ROOT/file).read_text()
print(json.dumps({'articles':13,'article_words':sum(c['words'] for c in catalog),'new_html_pages':len(pages),'local_links_and_fragments_checked':count,'zip_entries':18,'sitemap_routes':len(urls),'zip_sha256':hashlib.sha256((dest/'How_I_Build_from_Nigeria.zip').read_bytes()).hexdigest(),'result':'PASS'},indent=2))

# Evidence must survive into the web, text and offline editions.
for index in (4,5,9):
    web = resolve(catalog[index]['url']).read_text()
    assert 'https://github.com/godwillmakeaday/naijaos/' in web
    assert '<a href="https://' in web
    assert '## Case record:' in (dest/f'{index+1:02}-{catalog[index]["slug"]}.md').read_text()
record = json.loads((dest/'Verification_Record_20261101.json').read_text())
assert hashlib.sha256((dest/'Possibility_Lab_Demonstration.txt').read_bytes()).hexdigest() == record['download_sha256']
assert (ROOT/'assets/building-evidence/possibility-lab-demonstration.jpg').stat().st_size > 10000
print('PASS: three evidence-backed cases, linked sources and exact demonstration hash')
