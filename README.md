# naijaOS static site

This is a clean static HTML/CSS deployment pack for naijaOS.

## Structure

- `index.html` — public home/index page
- `assets/naijaos.css` — shared naijaOS chrome and article styling
- `naijaos-*.html` — shipped article pages

## Notes

- The uploaded Chrome Specification was used as the design reference and was **not shipped as a normal article page**.
- Duplicate/non-naijaOS `cluster-architecture-ep04` files were not included in this clean naijaOS pack.
- Some internal article links point to `index.html#planned` because the referenced pages were not in the uploaded zip.

## Deploy

```bash
git init
git branch -M main
git add .
git commit -m "Initial naijaOS static site"
git remote add origin https://github.com/YOUR-USERNAME/naijaos.git
git push -u origin main
```

Then connect that GitHub repo to the existing Vercel project.

## How I Build from Nigeria

The 13-article companion collection is at `/how-i-build-from-nigeria`; article pages live under `/build-from-nigeria/`.

- Source: `content/how-i-build-from-nigeria/series.md` (13 chapters separated by `---ARTICLE---`).
- Generator and editorial metadata: `scripts/build-building-series.py`.
- Rebuild: `python scripts/build-building-series.py`.
- Verify: `python scripts/check-building-series.py`.
- Downloads: `downloads/how-i-build-from-nigeria/` (individual Markdown, combined Markdown, self-contained offline HTML, project brief and ZIP).

The source and generated edition are committed together. Rebuild after editorial changes. The collection uses the existing paper/forest styling through a separate stylesheet and adds no executable browser script, form submission, tracking or affiliate links. The Lovable chapter is explicitly a planned evaluation; the historical Truehost account does not claim a confirmed fix.
