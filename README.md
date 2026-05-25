# dr-meir_new_page

End-to-end pipeline that turns medical-aesthetic course material (Telegram-sourced videos transcribed via TurboScribe) into Hebrew public-facing articles on dr-meir.com — with SEO, supporting media, and bidirectional internal linking via two mu-plugins that bypass Elementor.

## Quick start

```
# In Claude Code:
"פרסם את הקורס Buyanova contourology — קח את הוידאו הראשון"
```

or English:

```
"Publish the Buyanova contourology course — start with video 1"
```

The skill expects:

1. A Google Drive folder under `My Drive/courses/<course-name>/`
2. At least one `.mp4` (Telegram-sourced course video)
3. A matching `.txt` next to it (transcript from TurboScribe.ai — do this externally first)

It produces:

- One published Hebrew article on dr-meir.com (`/aesthetics/...` URL)
- 1 featured image + 1-2 inline images (nano-banana, aesthetic-clinic style)
- 1-2 video clips (web-optimized mp4)
- 8-15 outbound internal links to existing dr-meir.com posts
- Inbound links from ~50-90 existing posts (via inline keyword mu-plugin)
- A prominent "מאמר מומלץ" callout box on ~15 strategic source posts
- Rank Math SEO meta (title, description, focus keyword) set via WP-CLI/SSH
- URL submitted to Google (Rank Math Instant Indexing) + Bing (IndexNow)
- Sitemap regenerated, Cloudways Varnish purged

## See also

- `SKILL.md` — the full operational spec read by Claude
- `assets/article-example.md` — validated voice + structure (HA module 1)
- `assets/publish-example.py` — working WP REST publish reference
- `mu-plugins/` — the two source mu-plugins (callout + inline). These are the canonical source; deployed copies live on Cloudways at `applications/ncptzeczks/public_html/wp-content/mu-plugins/`.

## Validated history

- 2026-05-24: First production run — Buyanova contourology module 1 → post 53084
  ([https://dr-meir.com/aesthetics/hyaluronic-acid-complete-guide-fillers-mesotherapy/](https://dr-meir.com/aesthetics/hyaluronic-acid-complete-guide-fillers-mesotherapy/))
