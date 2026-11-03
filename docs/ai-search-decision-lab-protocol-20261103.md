# NaijaOS AI Search Decision Lab — Pilot protocol (3 November 2026)

## Objective
Test whether an honest, evidence-led decision page plus a working worksheet helps readers make a more useful choice, and whether it earns discoverability and qualified interest. **No claim of guaranteed rankings or AI citations.**

## Working page
`/experiments/wordpress-vs-nextjs-nigeria.html` (draft, intentionally `noindex,nofollow`).
Static HTML, no tracking, no backend, no form submission. The comparison and algorithm are qualitative hypotheses—not measured results.

## Editorial evidence gates before indexability
- [ ] A named human author/editor confirms authorship and demonstrable experience.
- [ ] Collect real, consented screenshots from sample WordPress and Next.js implementations; identify build versions and test dates.
- [ ] Document matched requirements (editing, hosting, security, feature complexity, backups, portability).
- [ ] Collect real quoted 24-month cost examples (NGN where appropriate); include exchange-rate date and vendor assumptions, no invented prices.
- [ ] Run at least one representative user workflow on both approaches and document findings and weaknesses.
- [ ] Verify primary URLs and all claims; add accessed dates, conflict disclosures and meaningful corrections.
- [ ] Review mobile, keyboard, screen reader, reduced-motion, offline and no-JavaScript presentation.
- [ ] Determine a legitimate user action/CTA with a real destination and a privacy statement.
- [ ] Review proposed byline, canonical route, sitemap entry, index/noindex decision and internal links.
- [ ] Owner approves indexability and publication. Only then remove `noindex` and document the actual publishing date.

## Test design
**Baseline before publishing**: URL index status, domain impressions/clicks and query inventory in Search Console, existing pages for similar intents, 12 grounded AI-query checks (provider, query, date, country, result, cited URL, screenshot when feasible).

**Weeks 1–2 after approved release**: verify canonical, indexing, sitemap, crawlability, mobile accessibility and worksheet behavior.

**Weeks 3–4**: impressions, clicks, ranking queries, CTR, worksheet completions (only with consent-respecting analytics), relevant CTA interactions and sampled AI citations. Do not interpret manual AI answers as stable rankings.

**Weeks 5–8**: update with genuine firsthand evidence, monitor comparable metrics, run a small reader usability check and consider a second page only if the first is trustworthy and useful.

## Reproducible citation log
| Date | Provider | Query | Region/language | Cites our URL? | Exact URL | Notes/evidence |
|---|---|---|---|---|---|---|
| | | | | | | |

## Outcome criteria
Primary: a real visitor can make a clearer choice and explain why; worksheet remains correct and accessible. Secondary: verified search discoverability and useful qualified actions. Failure is informative—report missing indexing, weak impressions or low engagement without claiming a ranking victory.

## Open dependencies
The separate draft PR #11 fixes a sitemap-domain discrepancy and describes a wider SEO authority program. Resolve it before approving any new indexable search page; this experimental PR does not edit robots.txt, sitemap.xml, the home page or production navigation.
