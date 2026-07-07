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
