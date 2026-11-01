"""Validate published income routes, content completeness and portable package."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.h1=0;self.canonical=[];self.schemas=[];self.json_script=False;self.css=[];self.executable_scripts=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        if tag=='link' and a.get('rel')=='stylesheet':self.css.append(a['href'])
        if tag=='script':
            if a.get('type')!='application/ld+json':self.executable_scripts+=1
            self.json_script=a.get('type')=='application/ld+json'
    def handle_endtag(self,tag):
        if tag=='script':self.json_script=False
    def handle_data(self,data):
        if self.json_script:self.schemas.append(json.loads(data))

def resolve(path):
    p=ROOT/unquote(path.lstrip('/'))
    if p.is_file():return p
    if p.with_suffix('.html').is_file():return p.with_suffix('.html')
    if (p/'index.html').is_file():return p/'index.html'
    raise AssertionError('Missing route: '+path)

catalog=json.loads((ROOT/'docs/income-library-catalog.json').read_text())
assert len(catalog)==9
assert len({c['url'] for c in catalog})==9
pages=[ROOT/'earning-from-nigeria.html']+[resolve(c['url']) for c in catalog]+[resolve(k['url']) for c in catalog for k in c['children']]
dest=ROOT/'downloads/earning-from-nigeria'
pages.append(dest/'Earning_from_Nigeria.html')
count=0
for file in pages:
    text=file.read_text();page=Page(text)
    assert page.executable_scripts==0,(file,'Unexpected executable script')
    assert page.h1==1,(file,'h1')
    assert len(page.ids)==len(set(page.ids)),(file,'duplicate IDs')
    assert len(page.canonical)==1,(file,'canonical')
    assert 'main' in page.ids,(file,'main landmark')
    for css in page.css:assert resolve(css).is_file()
    for href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=file if not u.path else resolve(u.path)
        if u.fragment:assert unquote(u.fragment) in Page(target.read_text()).ids,(file,href)
        count+=1
    assert 'href="javascript:' not in text
for c in catalog:
    text=resolve(c['url']).read_text();source=(ROOT/c['source']).read_text()
    assert c['words']>1000,(c['slug'],'truncated article')
    for heading in re.findall(r'^## (.+)$',source,re.M):
        slug=re.sub(r'[^a-z0-9]+','-',heading.lower()).strip('-')
        assert '<h2 id="'+slug+'">' in text,(c['slug'],heading)
    assert 'Paul A. Magaji' in text
    assert (dest/Path(c['source']).name).read_text()==source,c['slug']
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
assert len(urls)==len(set(urls))
for route in ['/earning-from-nigeria']+[c['url'] for c in catalog]:assert 'https://naijaos.io'+route in urls
for path in ['index.html','new-possibilities.html','how-i-build-from-nigeria.html','build-from-nigeria/earning-by-creating-global-value.html']:
    assert 'href="/earning-from-nigeria"' in (ROOT/path).read_text(),path
with zipfile.ZipFile(dest/'Earning_from_Nigeria.zip') as z:
    assert z.testzip() is None
    assert len(z.namelist())==12
    for name in z.namelist():assert z.read(name)==(dest/name).read_bytes(),name
    book=z.read('Earning_from_Nigeria.html').decode()
    assert '<link rel="stylesheet"' not in book
    assert '@import' not in book and '<script' not in book
    assert all('id="chapter-'+str(i)+'"' in book for i in range(1,10))
package=json.loads((ROOT/'docs/income-library-package.json').read_text())
assert package['archive_sha256']==hashlib.sha256((dest/'Earning_from_Nigeria.zip').read_bytes()).hexdigest()
print(json.dumps({'result':'PASS','pillar_articles':9,'article_words':sum(c['words'] for c in catalog),'pages_checked':len(pages),'local_links_and_fragments':count,'zip_entries':12,'published_children':sum(len(c['children']) for c in catalog)},indent=2))
