# NaijaOS Decision Lab — Evidence ledger and paired-test specification
Reviewed: 2026-11-03. Project: WordPress-led publishing versus Next.js deployed on Vercel.
Status: draft research; no head-to-head benchmark or verified vendor quote.

## Evidence classifications
**Source-backed facts** — grounded in official provider documentation, checked November 3, 2026:
1. WordPress exposes predefined roles and editing/publishing permissions: https://wordpress.org/documentation/article/roles-and-capabilities/
2. WordPress provides updates for plugins/themes; backups and rollback matter for maintenance: https://wordpress.org/documentation/article/plugins-themes-auto-updates/
3. Next.js has server rendering, prerendering and navigation functionality: https://nextjs.org/docs/app/getting-started/linking-and-navigating
4. Vercel Hobby is restricted to personal noncommercial use: https://vercel.com/docs/plans/hobby
5. Vercel's Pro plan is advertised from $20 USD per month (before applicable taxes and variable resources); not a complete website ownership price: https://vercel.com/pricing
6. Google recommends original, people-first and demonstrably experienced content; it warns against changing dates merely for apparent freshness: https://developers.google.com/search/docs/fundamentals/creating-helpful-content

**Qualitative editorial hypotheses, not yet tested:** WordPress may be more convenient when nontechnical editors primarily publish content; a Next.js solution may be preferable for bespoke software; a hybrid may fit a mixed publishing/product organization. Neither has been proven faster, safer, cheaper or better ranked in this pilot.

**Original evidence actually produced so far:** a working qualitative five-question decision model; an unindexed 24-month cost estimator; basic structural review; and independently reviewable arithmetic test fixtures. There has been no genuine paired site-build benchmark.

## Paired experiment to obtain original evidence
Build a matched 700–900-word article and one five-field interactive worksheet using two implementations, with the same content, assets, editorial requirements, performance budget and data protection requirements. Record the **exact build/hosting configurations**, versions, date, browser, device and network conditions.

Run five tests for each approach:
- An editor independently creates, publishes and corrects the sample article.
- The maintainer adds a user-facing worksheet and demonstrates input validation and keyboard access.
- The team creates a backup and rehearses a restoration.
- The team exports article content and documents switching providers.
- The team records three equivalent performance runs, noting caveats for caching, template and network differences.

Evidence table to complete only after real execution:

| Test | WordPress time, observation, screenshot | Next.js time, observation, screenshot | Reviewer/date |
|---|---|---|---|
| Publish and correct an article | Not tested | Not tested | Pending |
| Add interactive worksheet | Not tested | Not tested | Pending |
| Backup and restore | Not tested | Not tested | Pending |
| Export and portability | Not tested | Not tested | Pending |
| Repeatable performance | Not tested | Not tested | Pending |

## 24-month cost model
Each implementation requires quoted figures for: initial build; one-time migration; monthly hosting; monthly software/services; support hours each month; support hourly rate. The reader chooses months (default 24), currency (NGN or USD, **no conversion**) and a contingency (default 10%). Calculator input is processed in the user's browser without sending or storing it.

Formula:
- One-time cost = build + migration
- Monthly cost = hosting + software + support hours × hourly rate
- Subtotal = one-time cost + months × monthly cost
- Estimated allowance = subtotal × contingency percentage
- Total estimate = subtotal + allowance

**Completely fictional arithmetic fixture** (not Nigerian vendor pricing or a quoted estimate): WordPress amounts 100000 setup, 10000 monthly hosting, 5000 monthly software and 2 hours × 8000 per hour monthly support, with zero migration, produce 928400 after 24 months and a 10% allowance. Next.js amounts 400000 setup, 20000 monthly hosting, 5000 monthly software and 4 hours × 8000 per hour support, with zero migration, produce 1944800 under the same conditions. All numbers are in one hypothetical currency; they are **not** proposed prices or user spending.

Run: `node scripts/test-decision-cost-model.cjs` to recheck the computation and validation behavior. The model deliberately omits taxes, VAT, changing exchange rates, financing, present-value discounting, and unforeseen scope changes. Actual vendor quotations must include commercial eligibility, usage and future support.

## Release gates
- Confirm actual human author and subject matter reviewer, any AI assistance, affiliation disclosures and real publication/modification dates.
- Verify and cite individual claims; add genuine field notes and images with rights.
- Validate mobile, keyboard navigation, screen reader use and the cost calculator with Chrome/Android, Safari/iOS and desktop browsers.
- Check no tracking and no data exfiltration. Confirm that the amount input remains in-browser.
- No fabricated case studies, dates, screenshots, testimonials or vendor rankings.
- Resolve existing draft PR #11 sitemap mismatch as a separate change before starting public indexable search experiment.
- After owner editorial and legal/commercial approval, choose a canonical production URL, remove noindex, link from relevant existing content and document Search Console baseline and experimental AI citation sampling.
