<?php
/**
 * Plugin Name: DM Related Links Injector
 * Description: Injects "מאמר מומלץ" callout boxes at the end of specific posts to drive internal-link equity to chosen pillar articles. Bypasses Elementor by filtering the_content at priority 99.
 * Version: 1.0.0
 * Author: Dr. Meir
 *
 * Mapping: post_id_to_inject_into => target_post_id (the article to link TO)
 * Edit the $map to add/remove pairs.
 */

if (!defined('ABSPATH')) exit;

class DM_Related_Links {

    /**
     * Map of source_post_id => target_post_id
     * When the source post is rendered, a callout linking to target post is injected.
     */
    private static $map = [
        // === Hyaluronic acid pillar (post 53084) ===
        49024 => 53084, // פילרים (pillar)
        49429 => 53084, // חומר מילוי טבעי
        51316 => 53084, // מיצוק קו הלסת
        51146 => 53084, // קמטי נזולביאל בוטוקס
        51026 => 53084, // הצערת פנים וצוואר (radiesse + HA)
        43266 => 53084, // סטילאז'
        43264 => 53084, // נאוויה
        32248 => 53084, // סקין בוסטר
        8175  => 53084, // רדיאס
        8065  => 53084, // טיפול בקמטים
        7660  => 53084, // חומרי מילוי בקליניקה
        49034 => 53084, // קולגן לפנים
        49022 => 53084, // קמטים
        49026 => 53084, // טיפולי אסתטיקה
        49008 => 53084, // כהויות מתחת לעיניים
        51619 => 53084, // שלושת הטיפולים הכי פופולריים
    ];

    private static $css_printed = false;

    public static function init() {
        add_filter('the_content', [__CLASS__, 'inject'], 99);
    }

    public static function inject($content) {
        if (is_admin() || !is_singular()) return $content;
        if (!in_the_loop() || !is_main_query()) return $content;

        $source_id = get_the_ID();
        if (!isset(self::$map[$source_id])) return $content;

        $target_id = self::$map[$source_id];
        if ($target_id === $source_id) return $content; // never self-link

        $target = get_post($target_id);
        if (!$target || $target->post_status !== 'publish') return $content;

        // Prevent double-injection (e.g. if the_content runs twice)
        $marker = 'dm-related-' . $target_id;
        if (strpos($content, $marker) !== false) return $content;

        $url = get_permalink($target_id);
        $title = get_the_title($target_id);
        $excerpt = self::short_excerpt($target);
        $thumb = self::thumb_url($target_id, 'medium');

        $html = self::render($url, $title, $excerpt, $thumb, $marker);

        $css = self::$css_printed ? '' : self::css();
        self::$css_printed = true;

        return $content . $css . $html;
    }

    private static function short_excerpt($post) {
        $raw = $post->post_excerpt;
        if (empty($raw)) {
            $raw = wp_strip_all_tags($post->post_content);
        }
        $raw = wp_strip_all_tags($raw);
        if (mb_strlen($raw) > 160) {
            $raw = mb_substr($raw, 0, 157) . '…';
        }
        return $raw;
    }

    private static function thumb_url($post_id, $size) {
        $tid = get_post_thumbnail_id($post_id);
        if (!$tid) return '';
        $img = wp_get_attachment_image_src($tid, $size);
        return $img ? $img[0] : '';
    }

    private static function render($url, $title, $excerpt, $thumb, $marker) {
        $url = esc_url($url);
        $title = esc_html($title);
        $excerpt = esc_html($excerpt);
        $thumb_html = '';
        if ($thumb) {
            $thumb_html = '<div class="dm-rl-thumb"><img src="' . esc_url($thumb) . '" alt="" loading="lazy" /></div>';
        }
        return <<<HTML
<aside class="dm-rl-box" data-marker="{$marker}" dir="rtl" lang="he">
  <a href="{$url}" class="dm-rl-link" aria-label="קריאה נוספת: {$title}">
    {$thumb_html}
    <div class="dm-rl-body">
      <span class="dm-rl-label">מאמר מומלץ</span>
      <h3 class="dm-rl-title">{$title}</h3>
      <p class="dm-rl-excerpt">{$excerpt}</p>
      <span class="dm-rl-cta">קראו את המדריך המלא <span class="dm-rl-arrow">←</span></span>
    </div>
  </a>
</aside>
HTML;
    }

    private static function css() {
        return <<<CSS
<style id="dm-related-links-css">
.dm-rl-box{margin:2.5em 0 1.5em;padding:0;border:1px solid #e8dfd6;background:#fdfaf6;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.04);transition:box-shadow .25s ease,transform .25s ease;direction:rtl}
.dm-rl-box:hover{box-shadow:0 6px 20px rgba(0,0,0,.08);transform:translateY(-2px)}
.dm-rl-link{display:flex;align-items:stretch;text-decoration:none;color:inherit;gap:1.25em;padding:1.25em}
.dm-rl-link:hover{text-decoration:none;color:inherit}
.dm-rl-thumb{flex:0 0 140px;align-self:center}
.dm-rl-thumb img{width:140px;height:140px;object-fit:cover;border-radius:10px;display:block}
.dm-rl-body{flex:1;display:flex;flex-direction:column;justify-content:center;text-align:right}
.dm-rl-label{display:inline-block;font-size:11px;font-weight:700;color:#a17f59;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.5em}
.dm-rl-title{font-size:1.25em;line-height:1.35;margin:0 0 .5em;color:#222;font-weight:700}
.dm-rl-excerpt{font-size:.95em;line-height:1.55;color:#555;margin:0 0 .85em}
.dm-rl-cta{display:inline-flex;align-items:center;gap:.4em;font-size:.95em;font-weight:600;color:#a17f59}
.dm-rl-arrow{display:inline-block;transition:transform .25s ease;font-size:1.1em}
.dm-rl-box:hover .dm-rl-arrow{transform:translateX(-4px)}
@media (max-width:600px){
  .dm-rl-link{flex-direction:column;gap:.85em;padding:1em}
  .dm-rl-thumb{flex:0 0 auto;align-self:center}
  .dm-rl-thumb img{width:100%;max-width:280px;height:180px}
  .dm-rl-body{text-align:right}
  .dm-rl-title{font-size:1.15em}
}
</style>
CSS;
    }
}
DM_Related_Links::init();
