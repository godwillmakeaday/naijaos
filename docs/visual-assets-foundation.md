# NaijaOS visual assets foundation

Three static responsive SVG illustrations have been added under `public/assets/`.

- `naijaos-system-map.svg`: conceptual illustration linking five economic signals to reorder, reprice, and wait decisions.
- `naijaos-corridor-lens.svg`: illustrative network of Abuja, Keffi, Akwanga and Lafia. **Not a geographically accurate map**; must not be used for navigation, actual route risk, or route metrics.
- `naijaos-civic-atlas.svg`: high-level associations of civic concepts, **not a statement of constitutional legal relationships**.

Proposed visual palette: navy `#101B27`, paper `#F0EEE5`, gold `#D3A65D`, teal `#45938D`, alert `#C96C5D`.

This PR adds standalone visual assets only, so existing homepage and production behavior remain unchanged. Wire into corresponding pages after layout, performance, and accessibility review. Meaningful accessible alt text is required. No generated example data should be published as fact.

## Integration and review

Visual assets now use `/assets/` paths in this static website. The homepage includes economic, civic and corridor diagrams; the distributor brief includes economic and corridor diagrams; the interactive atlas includes the civic diagram. Their shared styles are in `visual-assets.css`.

Responsive figures include keyboard-focusable horizontal panning at narrow widths, alt text, accessible captions, full-size links, reduced-motion and print styling. All geographic, economic and institutional content is **illustrative**, not verified data, route guidance or constitutional analysis. Confirm actual Vercel preview asset responses, desktop/mobile layout, accessibility and interaction before merging.
