---
name: dr-meir-new-page
description: End-to-end pipeline that turns medical-aesthetic course material (videos for doctors, usually Russian, sourced from Telegram channels with download restrictions) into Hebrew public-facing content pages on dr-meir.com. Inputs accepted from two sources in this preference order — (1) MacDroid-mounted Samsung S23+ Telegram cache at `~/Library/CloudStorage/MacDroid-*/storage/emulated/0/Android/data/org.telegram.messenger/files/Telegram/Telegram Video/` (preferred — no upload step), (2) Google Drive folder per course (fallback). Either way, each video must have a matching `.txt` from TurboScribe.ai. The skill writes an engaging Hebrew article, generates aesthetic-clinic-style supporting images (nano-banana), downloads + cuts higher-resolution reference video clips when available (YouTube), uploads everything to WP, publishes via REST, sets Rank Math SEO + focus keyword via WP-CLI/SSH, submits to Google Indexing (Rank Math Instant Indexing + IndexNow), and deploys bidirectional internal linking via two mu-plugins (bottom callout + inline keyword replacement) that bypass Elementor. Use when user says "פרסם את הקורס", "process course X", "publish from phone", "publish from drive folder", "המשך עם הקורס", or provides a path to Telegram course material.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__claude_ai_Google_Drive__search_files, mcp__claude_ai_Google_Drive__get_file_metadata, mcp__claude_ai_Google_Drive__list_recent_files, mcp__claude_ai_Google_Drive__read_file_content, mcp__nano-banana__generate_image, mcp__nano-banana__edit_image
---

# dr-meir-new-page — Telegram course → Hebrew dr-meir.com article

End-to-end content pipeline. Designed for Dr. Meir Babaev's aesthetic-medicine clinic (dr-meir.com): takes professional course material that the doctor consumes for training, and produces engaging, SEO-optimized public articles for the clinic's website — while preserving topic authority and avoiding direct copying of source material.

**Validated on 2026-05-24:** post 53084 "חומצה היאלורונית — המדריך המלא" published at https://dr-meir.com/aesthetics/hyaluronic-acid-complete-guide-fillers-mesotherapy/ from the Buyanova contourology course module 1.

## When to invoke

- User says: "פרסם את הקורס [שם]", "publish course X", "process the course folder", "המשך עם הקורס הזה"
- User provides a Google Drive folder URL/path containing course assets
- User mentions specific course name + asks for article (e.g., "תכתוב מאמר מהקובץ של בויאנובה")
- Hebrew triggers: "תהפוך את הקורס למאמר", "צור עמוד תוכן מהקורס", "תוציא תוכן לציבור הרחב מהמודול"

## When NOT to invoke

- No transcript (.txt) in the Drive folder yet — ask user to run TurboScribe first
- User wants to edit an EXISTING post (use `dr-meir-content-update` skill instead)
- User wants visuals-only (use `dr-meir-visuals`)
- The course material isn't medical-aesthetic-related (out of scope for dr-meir.com publishing)

---

## Source profile (memorize)

- **Input — PRIMARY (preferred):** MacDroid-mounted Samsung S23+ Telegram cache at
  `~/Library/CloudStorage/MacDroid-samsungSM-S916B/storage/emulated/0/Android/data/org.telegram.messenger/files/Telegram/Telegram Video/`
  (sibling `Telegram Documents/` for PDFs). See `~/.claude/projects/-Users-meirbabaev/memory/macdroid-telegram-paths.md`.
  - Requires MacDroid app running + phone connected via USB
  - Bypasses scoped storage that blocks AirDroid/OpenMTP from seeing `/Android/data/`
  - Files are processed in place — no copy needed
- **Input — FALLBACK:** Google Drive folder `My Drive/courses/<course-name>/` (when phone unavailable, or user pre-staged there). Contains the same `.mp4` + `.txt` pairs.
- **Transcript source:** `.txt` files come from TurboScribe.ai (user runs them externally — see `turboscribe-transcription.md`)
- **Source language:** typically Russian (most doctor courses), occasionally English
- **Target language:** Hebrew, RTL
- **Target audience:** general public, dr-meir.com patients (NOT other doctors)
- **Target site:** dr-meir.com (WordPress + Hello Elementor + Rank Math PRO + WP Rocket — see `dr-meir-com-site.md`)

## Source discovery order (apply in skill Step 1)

1. **Check MacDroid first** — `ls ~/Library/CloudStorage/MacDroid-*/storage/emulated/0/Android/data/org.telegram.messenger/files/Telegram/Telegram\ Video/ 2>/dev/null`. Use glob because mount-name embeds the phone model. If files exist, ask user which course (by recent-modified or by description) and proceed from there.
2. **Else check Google Drive** — `~/Library/CloudStorage/GoogleDrive-doctor@dr-meir.com/My Drive/courses/<course>/` per old pattern.
3. **Else ask user** — for the explicit path or course name.

## Key prior knowledge — DO NOT relitigate

Always check memory before improvising:

- `dr-meir-com-site.md` — WP login `2ofnu4` NOT admin, stack
- `dr-meir-com-local-files.md` — `~/.dr-meir/credentials.env`, `~/.dr-meir/lib/`
- `dr-meir-ssh-access.md` — Cloudways SSH via sshpass + `~/.dr-meir/lib/ssh.sh` (`drssh`/`drwp`/`drscp_to`)
- `dr-meir-rank-math.md` — RM PRO 3.0.110, IndexNow key `522e9d9ad1964a168272e0064978047f`, application slug `ncptzeczks`
- `dr-meir-rate-limit-rules.md` — **max 1 concurrent, 2s delay between requests, 30 req/session**. Aggressive WAF.
- `wp-rest-api-gotchas.md` — App Password format, slug ≠ login
- `seo-content-expansion-approach.md` — Don't copy competitor text; extract facts + write original synthesis with named-tech comparisons + Schema
- `user-aesthetic-medicine-doctor.md` — Dr. Meir = cosmetic medicine. Default visuals: white/minimal, no stethoscope/ENT props
- `transcript-processing-preserve-content.md` — Keep ALL content from transcript by default; only fix errors + add headings. Condense ONLY if user says "תסכם"/"summarize"
- `turboscribe-transcription.md` — Paid unlimited, RU+EN. Workflow uses TurboScribe externally (already done), skill reads the resulting .txt
- `dr-meir-related-links-plugin.md` — Two mu-plugins (callout + inline) for internal linking; bypass Elementor

---

## Architecture

```
Google Drive: courses/<course-name>/
  ├── *.mp4              ← source video (low-res, from Telegram cache)
  └── *.txt              ← TurboScribe transcript (.txt next to .mp4)
       │
       ▼
[1] Scan Drive          → list assets, identify primary video + transcript pairing
[2] Read transcript     → understand content (RU/EN), identify key concepts
[3] Inspect video       → scene-change frames (ffmpeg) — confirm topic visually
[4] Reference video     → if a higher-res original exists on YouTube (e.g.,
                          product demo from manufacturer), prefer THAT for clips.
                          ASK USER for YouTube link if low-res lecture has embedded demos.
[5] Write article       → Hebrew, public audience, ~1800-2200 words. Style:
                          - Engaging hook
                          - Clear H2/H3 hierarchy
                          - Bold key insights
                          - Comparison tables for named technologies
                          - "How to choose" practical section
                          - NO direct translation from source — original synthesis
                          - Inline outbound internal links to existing dr-meir.com posts
[6] Generate images     → nano-banana, aesthetic-clinic style (warm beige, white,
                          minimal, NO syringes/medical equipment unless requested)
[7] Cut video clips     → ffmpeg, web-optimized mp4 (libx264 crf 22, faststart)
[8] Upload media        → WP REST `/wp/v2/media` with alt/title/caption in Hebrew
[9] Publish post        → WP REST `/wp/v2/posts` (status=publish, category=aesthetics=5)
[10] Set Rank Math meta → via wp-cli SSH (REST doesn't expose rank_math_* keys)
[11] Submit indexing    → Rank Math `/in/submitUrls` (Google) + IndexNow (Bing)
[12] Update inbound mu-plugins → add source posts to callout map + keyword to inline map
[13] Deploy + purge     → drscp_to + Varnish bust via blogname touch
[14] Verify             → curl checks for both link types on 5+ sample pages
```

---

## Step-by-step playbook

### Step 0 — Duplicate-content check (MANDATORY before any transcription work)

**Why this exists:** Telegram message_id is NOT a stable identifier for a video. The same source video can appear in the user's Telegram cache under DIFFERENT file IDs (e.g., `2_5285506910462687404.mp4` and `2_5285506910462687410.mp4` were the SAME Buyanova module 1 video — once on May 24, once on May 28 — caused by the user re-watching or the channel re-posting). A different file ID does NOT mean different content.

**Failure mode learned 2026-05-28:** I uploaded `..410.mp4` to TurboScribe without checking existing transcripts. After ~12 minutes of upload + transcription, content turned out identical to `..404.mp4` already published at /aesthetics/hyaluronic-acid-complete-guide-fillers-mesotherapy/. Wasted user time and produced duplicate clutter in TurboScribe library.

**Rule:** Before clicking TRANSCRIBE in TurboScribe (or any equivalent), do ALL of:

1. **Duration match:** read the duration of the new file (`ffprobe -show_entries format=duration`). Then check `~/Telegram-Material/work/*/published.json` for any existing course with a video of duration within ±90 seconds. If a match exists, STOP and ask user: "Found `<existing-course>` (post #<id>) with video of same duration — is this the same content?"
2. **TurboScribe history check:** when the upload dialog is open, the dashboard list is still visible. Read the durations of recent files (especially in topic-related folders). If any match the new file's duration within ±90s, STOP and ask the same question.
3. **Folder hint:** if the user has a TurboScribe folder name that already contains the file ID family (e.g., `הרב עמרמי` folder containing `...404`), and the new file ID is in the same family (`...410` differs only in last 3 digits, OR same date range), flag it.
4. **First-page-of-transcript spot check:** if uncertain after the above, after transcription finishes, read the first paragraph of the new `.txt` and grep `~/Telegram-Material/work/*/transcripts/*.txt` (or the assets folder of the skill) for a near-duplicate first sentence before continuing to the writing step.

When in doubt, ASK BEFORE TRANSCRIBING. Re-transcription is harmless (free on user's unlimited plan) but re-publication or re-spending tokens on writing is not.

### Step 1 — Locate source assets

**Order of precedence (try each before falling back to the next):**

**A. MacDroid mount (preferred — direct from phone, no upload):**
```bash
# Glob because mount-name embeds phone model (currently samsungSM-S916B)
MACDROID_BASE=$(ls -d ~/Library/CloudStorage/MacDroid-*/storage/emulated/0/Android/data/org.telegram.messenger/files/Telegram 2>/dev/null | head -1)
if [ -n "$MACDROID_BASE" ]; then
    ls -la "$MACDROID_BASE/Telegram Video/" 2>/dev/null   # videos
    ls -la "$MACDROID_BASE/Telegram Documents/" 2>/dev/null  # PDFs etc.
fi
```
If MacDroid is mounted, **show the user the list of recent files and ask which course/file to process**. The `.txt` transcripts are NOT alongside the videos here — user generates them via TurboScribe.ai separately and drops them next to the work directory OR on Drive.

**B. Google Drive (fallback — when user pre-staged):**
```python
# Via Drive MCP
search_files(query=f"title contains '{course_name}'", pageSize=20)
search_files(query=f"parentId = '{folder_id}'", pageSize=50)
```

**C. Ask user** for an explicit path.

### Transcript expectations

- A `.txt` from TurboScribe is required for content writing. Each `.mp4` should have a sibling/companion `.txt` SOMEWHERE the user points us to.
- If transcript is missing, **STOP and ask the user to run TurboScribe first** — do not transcribe locally.
- For MacDroid sources, the user typically uploads the video to TurboScribe, downloads the `.txt`, and either places it in the same work folder OR shares it via Drive.

### Step 2 — Set up local working dir

```bash
WORK=~/Telegram-Material/work/<course-slug>
mkdir -p "$WORK"/{frames,clips,images,final-media}
```

### Step 3 — Read + understand transcript

Read the `.txt` file (it's already on the local Drive sync path: `~/Library/CloudStorage/GoogleDrive-doctor@dr-meir.com/My Drive/...`). Identify:
- Main topic / focus keyword (in Hebrew + English)
- 5-8 key concepts that would interest the public audience
- Named technologies/products to compare in a table
- Safety considerations to surface (medical responsibility)

### Step 4 — Inspect source video

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_type,codec_name,width,height -of default "$VIDEO"
# Scene-change frame extraction (slides usually change at scene cuts)
ffmpeg -y -i "$VIDEO" -vf "select='gt(scene,0.25)',metadata=print:file=$WORK/frames/ts.txt" -vsync vfr "$WORK/frames/f_%04d.png"
```

Use Read tool on a few frames to confirm what's in the lecture. If embedded product demos (e.g., Juvederm rheology comparison) appear — flag to user that the lecture's quality is low (typical: 640x360) and **ask if a higher-res original exists** (manufacturer YouTube channel, etc.).

### Step 5 — Get higher-resolution reference clip (optional)

If user provides a YouTube URL with the higher-res original:

```bash
yt-dlp -f 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' --merge-output-format mp4 \
       -o "$WORK/yt/<filename>.%(ext)s" "$YT_URL"
# Then cut meaningful sections:
ffmpeg -y -ss <start> -to <end> -i "$YT_URL_FILE" -c:v libx264 -crf 22 -preset slow \
       -c:a aac -movflags +faststart "$WORK/clips/<seo-name>.mp4"
```

Always credit source in caption (e.g., "Source: Allergan / <Brand>").

### Step 6 — Write the Hebrew article

Constraints:
- Length: **~1800-2200 words**
- Voice: doctor-to-patient, clear, warm, NOT condescending
- Audience: general public (laypeople), but assume basic curiosity about how things work
- Tone: confident but honest about uncertainty/safety
- Structure (recommended baseline; deviate when appropriate):
  1. Hook paragraph (`<p class="dm-lead">`) — strong opening sentence in `<strong>`
  2. "What is X" — basic definition + biology if relevant
  3. "Why it matters" — what changes with age / why patients care
  4. Two-three main concept sections with H2
  5. Named-product comparison table (Stylage, Neauvia, Juvederm, etc.)
  6. "How to choose" practical section
  7. Safety section (mandatory for any medical-aesthetic content)
  8. "Bottom line" recap
  9. "Related reading" link list at the end
- Inline outbound internal links: 8-15 to existing dr-meir.com posts (use the search step below to find them)
- DO NOT copy translated chunks from the source. Synthesize.
- Use bold for one key insight per section
- Use lists/tables where they help; not just walls of text

See `assets/article-example.md` for the validated voice/structure.

### Step 7 — Find outbound link targets

```bash
# Search existing dr-meir.com posts for topical overlap
source ~/.dr-meir/credentials.env
AUTH=$(printf '%s:%s' "$WP_USERNAME" "$WP_APP_PASSWORD" | base64)
curl -s "$WP_SITE/wp-json/wp/v2/posts?search=<HEBREW_KEYWORD>&per_page=15&_fields=id,title,link" \
     -H "Authorization: Basic $AUTH" --max-time 15
```

Search 3-5 keyword variations. Rate-limit: 2s sleep between requests (see `dr-meir-rate-limit-rules.md`).

### Step 8 — Generate supporting images

Use `mcp__nano-banana__generate_image`. Two images minimum:
1. **Featured (hero):** macro / luxury skincare editorial photography style. Subject relates to article topic (e.g., serum droplet on skin, glass containers with different gel consistencies). 16:9 ideal but nano-banana defaults to 1024x1024 square.
2. **Inline:** topical visualization that complements the H2 about products/comparisons.

Style anchors (per `user-aesthetic-medicine-doctor.md`):
- ✅ White / warm beige minimalist backgrounds
- ✅ Soft natural light
- ✅ Hyper-realistic, editorial photography
- ✅ Subtle pink / nude tones
- ❌ NO syringes/needles unless contextually demanded
- ❌ NO ENT/general medical props
- ❌ NO text/watermarks
- ❌ NO Soul 2.0 for portraits (drifts — use nano_banana_2; here we don't need portraits)

### Step 9 — Upload all media

Use WP REST `/wp/v2/media` with `Content-Type: <mime>` and `Content-Disposition` header. SEO-friendly filenames (kebab-case English).

**Pitfall:** Hebrew with apostrophes (`ג'לי`) inline-quoted in Python bash heredocs breaks. Write metadata to a JSON file and POST `--data @file.json` instead. See `assets/publish-example.py`.

For each: set `alt_text`, `title`, `caption` in Hebrew via a follow-up POST to `/wp/v2/media/{id}`.

### Step 10 — Build + publish post

See `assets/publish-example.py` — fully working reference for post 53084. Key things:
- `slug` in English (SEO + URL hygiene)
- `categories: [5]` for `/aesthetics/` (verify with `?slug=aesthetics`)
- `featured_media: <hero_id>`
- `meta` block with `rank_math_*` keys (note: REST may NOT persist these — see Step 11)
- `<video>` HTML5 tag with `<source>` and `poster` for clips
- `<figure>` + `<figcaption>` for images with credit
- Use `<a>` for all outbound internal links — naturally inline, not in a list

### Step 11 — Set Rank Math meta (REST workaround)

REST API on this site does NOT persist `rank_math_*` post meta even when included in the `meta` block of the POST request. Use wp-cli SSH:

```bash
. ~/.dr-meir/lib/ssh.sh
PID=<new_post_id>
echo 'SEO TITLE | ד״ר מאיר באבאיב' | drwp "post meta update $PID rank_math_title"
echo 'META DESCRIPTION' | drwp "post meta update $PID rank_math_description"
echo 'FOCUS KEYWORD' | drwp "post meta update $PID rank_math_focus_keyword"
drwp "post meta update $PID rank_math_robots --format=json '[\"index\",\"follow\"]'"
```

Stdin form (echo + drwp without value arg) safely handles Hebrew + quotes.

### Step 12 — Submit URL to indexing

```bash
# Rank Math Instant Indexing (pings Google's Indexing API)
curl -s -X POST "$WP_SITE/wp-json/rankmath/v1/in/submitUrls" \
     -H "Authorization: Basic $AUTH" -H "Content-Type: application/json" \
     --data '{"urls":"<NEW_URL>"}' --max-time 30
# Direct IndexNow (Bing/Yandex) — RM also does this automatically on publish
curl -s -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json" \
     -d '{"host":"dr-meir.com","key":"522e9d9ad1964a168272e0064978047f",
          "keyLocation":"https://dr-meir.com/522e9d9ad1964a168272e0064978047f.txt",
          "urlList":["<NEW_URL>"]}' --max-time 30
```

Google `/ping?sitemap=` is deprecated since 2023 — don't bother.

### Step 13 — Update inbound mu-plugins (CRITICAL)

This is the SEO equity multiplier. Edit BOTH mu-plugins to add the new pillar:

**`~/.dr-meir/mu-plugins/dm-related-links.php`** — append source post IDs:
```php
private static $map = [
    ...existing pairs...
    <SOURCE_POST_ID> => <NEW_PILLAR_POST_ID>,
];
```
Choose 10-20 high-relevance source posts via the search you ran in Step 7.

**`~/.dr-meir/mu-plugins/dm-inline-keyword-links.php`** — append keyword pairs:
```php
private static $map = [
    ...existing pairs...
    'main hebrew keyword phrase'  => 'https://dr-meir.com/<category>/<slug>/',
    'shorter variant'             => 'https://dr-meir.com/<category>/<slug>/',
    'English Term'                => 'https://dr-meir.com/<category>/<slug>/',
];
```
Longest phrase first to win regex priority.

Deploy:
```bash
. ~/.dr-meir/lib/ssh.sh
drscp_to ~/.dr-meir/mu-plugins/dm-related-links.php applications/ncptzeczks/public_html/wp-content/mu-plugins/dm-related-links.php
drscp_to ~/.dr-meir/mu-plugins/dm-inline-keyword-links.php applications/ncptzeczks/public_html/wp-content/mu-plugins/dm-inline-keyword-links.php
# Varnish purge via blogname touch
CURRENT=$(drwp "option get blogname" 2>/dev/null | tail -1)
drwp "option update blogname \"$CURRENT \""; sleep 1; drwp "option update blogname \"$CURRENT\""
```

Verify both layers work — use the `Cache-Control: no-cache` + `?cb=$RANDOM$RANDOM` trick and grep FILE not echo (Hebrew breaks zsh echo piping):

```bash
RND=$RANDOM$RANDOM
curl -s -H "Cache-Control: no-cache" "https://dr-meir.com/<source-post-url>/?cb=$RND" > /tmp/p.html
echo "inline: $(grep -c 'dm-inline-link' /tmp/p.html)"
echo "callout: $(grep -c 'data-marker=\"dm-related-<NEW_PILLAR_ID>\"' /tmp/p.html)"
```

### Step 14 — Self-link guard

Confirm the new pillar article itself shows ZERO inbound markers (self-link is bug — would link the article to itself).

---

## Common pitfalls (learned the hard way)

1. **`zsh: character not in range` warnings + grep returns 0** — happens when piping Hebrew content through `echo`. Always write to a temp file, then grep the file.
2. **REST media upload silently succeeds, then metadata UPDATE breaks on Hebrew apostrophes** — use JSON file `--data @f.json` instead of inline `-d "{...}"`. Watch for duplicate uploads if you retry naively (WP appends `-1` to filename).
3. **Rank Math meta NOT saved via REST `meta` block** — use wp-cli over SSH with stdin form.
4. **`?nocache=$(date +%s)` insufficient for Cloudways Varnish** — use `?cb=$RANDOM$RANDOM` plus `Cache-Control: no-cache` header.
5. **Elementor target posts have empty `content` field in REST** — direct edits to inject inbound links would require touching `_elementor_data` (RISKY, see chin-template batch artifact memory). USE the mu-plugins instead.
6. **Link Genius preview-then-execute is BROKEN** — preview reports 214 opportunities but execute returns "no_results_found". Don't waste time. Use the mu-plugins.
7. **`source` doesn't propagate env to Python** — use `set -a; source ...; set +a` to export everything.

---

## State persistence

Per course, save final state at `~/Telegram-Material/work/<course-slug>/published.json`:
```json
{
  "id": 53084,
  "url": "https://dr-meir.com/...",
  "title": "...",
  "slug": "...",
  "media": {"featured": 53078, "consistency": 53079, "main_video": 53080, ...},
  "links_outbound": ["49024", "49429", ...],
  "links_inbound_callout": [49024, 49429, 51316, ...],
  "links_inbound_inline_keywords": ["חומצה היאלורונית", "Hyaluronic Acid"]
}
```

When user says "המשך עם הקורס" (continue with this course), read this file to know where to pick up — typically processing the NEXT `.mp4`/`.txt` pair in the same Drive folder.

---

## Repo layout

```
dr-meir-new-page/
├── SKILL.md                          (this file)
├── README.md                         (quick start for humans)
├── assets/
│   ├── article-example.md            (validated voice/structure — HA module 1)
│   └── publish-example.py            (working WP REST publishing reference)
├── mu-plugins/
│   ├── dm-related-links.php          (bottom callout, source→target map)
│   └── dm-inline-keyword-links.php   (inline keyword replacement, kw→url map)
├── templates/
│   └── article-skeleton.md           (blank Hebrew structure template)
└── workflow/
    └── (per-step deep dives if needed)
```

The mu-plugins here are the canonical SOURCE — the deployed copies live at `applications/ncptzeczks/public_html/wp-content/mu-plugins/` on Cloudways. Always edit here first, then `drscp_to` to deploy.
