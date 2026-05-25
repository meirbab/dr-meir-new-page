<?php
/**
 * Plugin Name: DM Inline Keyword Links
 * Description: Replaces the first occurrence of configured keywords in any post's rendered content with an internal anchor link. Bypasses Elementor by filtering the_content at priority 99. Safe: skips text inside <a>, <h1-6>, <script>, <style>, and HTML attributes.
 * Version: 1.0.0
 * Author: Dr. Meir
 *
 * This complements DM Related Links (bottom callout) with inline contextual links —
 * the equivalent of what Rank Math Link Genius would do, but bypassing the broken
 * preview→execute flow.
 */

if (!defined('ABSPATH')) exit;

class DM_Inline_Keyword_Links {

    /**
     * keyword (case-insensitive, exact phrase) => target URL
     * Order matters: longest/most-specific phrases first to avoid conflicts.
     */
    private static $map = [
        'חומצה היאלורונית'    => 'https://dr-meir.com/aesthetics/hyaluronic-acid-complete-guide-fillers-mesotherapy/',
        'Hyaluronic Acid'      => 'https://dr-meir.com/aesthetics/hyaluronic-acid-complete-guide-fillers-mesotherapy/',
    ];

    /** Max inline links injected per page across all keywords. */
    const MAX_PER_PAGE = 2;

    /** Tags whose contents must NOT be linked (skip-context). */
    const SKIP_TAGS = ['a','h1','h2','h3','h4','h5','h6','script','style','button','textarea','option'];

    public static function init() {
        add_filter('the_content', [__CLASS__, 'inject'], 99);
    }

    public static function inject($content) {
        if (is_admin() || !is_singular()) return $content;
        if (!in_the_loop() || !is_main_query()) return $content;
        if (empty($content)) return $content;

        $current_url = get_permalink();
        $injected_count = 0;

        foreach (self::$map as $kw => $url) {
            if ($injected_count >= self::MAX_PER_PAGE) break;
            // Self-link guard — never link the article to itself
            if (untrailingslashit($url) === untrailingslashit($current_url)) continue;
            // Skip if a dm-inline anchor for this keyword already exists (idempotency)
            if (strpos($content, 'data-kw="' . esc_attr($kw) . '"') !== false) continue;

            $new = self::replace_first_in_text($content, $kw, $url);
            if ($new !== $content) {
                $content = $new;
                $injected_count++;
            }
        }
        return $content;
    }

    /**
     * Replace the first text occurrence of $kw with an anchor tag.
     * Walks HTML token-by-token; tracks depth inside SKIP_TAGS.
     */
    private static function replace_first_in_text($html, $kw, $url) {
        $tokens = preg_split('/(<[^>]+>)/u', $html, -1, PREG_SPLIT_DELIM_CAPTURE);
        if (!$tokens) return $html;

        $skip_depth = 0;
        $replaced   = false;

        foreach ($tokens as $i => $t) {
            if ($t === '') continue;

            // Tag token
            if (isset($t[0]) && $t[0] === '<') {
                // Match opening tag, e.g., <h2 class="..."> or <a href="...">
                if (preg_match('/^<(\w+)\b[^>]*?(\/?)>$/u', $t, $m)) {
                    $tag = strtolower($m[1]);
                    $self_closing = $m[2] === '/';
                    if (in_array($tag, self::SKIP_TAGS, true) && !$self_closing) {
                        $skip_depth++;
                    }
                } elseif (preg_match('/^<\/(\w+)\s*>$/u', $t, $m)) {
                    $tag = strtolower($m[1]);
                    if (in_array($tag, self::SKIP_TAGS, true)) {
                        $skip_depth = max(0, $skip_depth - 1);
                    }
                }
                continue;
            }

            // Text token
            if (!$replaced && $skip_depth === 0) {
                // Case-insensitive search — Hebrew is largely case-stable but English
                // variants like "Hyaluronic Acid" need it.
                $pos = mb_stripos($t, $kw);
                if ($pos !== false) {
                    // Word-boundary check for Hebrew/Latin (avoid mid-word replacements
                    // — e.g., if keyword is "פילר", don't match inside "פילרים").
                    // For multi-word phrases this is usually fine; for short ones we
                    // require non-letter chars around the match.
                    $kw_len = mb_strlen($kw);
                    $before_char = $pos > 0 ? mb_substr($t, $pos - 1, 1) : '';
                    $after_char  = mb_substr($t, $pos + $kw_len, 1);
                    $is_letter = function($c) {
                        return $c !== '' && preg_match('/^[\p{L}\p{Nd}]$/u', $c);
                    };
                    if ($is_letter($before_char) || $is_letter($after_char)) {
                        continue; // mid-word match — skip
                    }

                    $before = mb_substr($t, 0, $pos);
                    $match  = mb_substr($t, $pos, $kw_len); // preserves original case
                    $after  = mb_substr($t, $pos + $kw_len);
                    $anchor = '<a href="' . esc_url($url) . '" class="dm-inline-link" data-kw="' . esc_attr($kw) . '">' . esc_html($match) . '</a>';
                    $tokens[$i] = $before . $anchor . $after;
                    $replaced = true;
                }
            }
        }

        return $replaced ? implode('', $tokens) : $html;
    }
}
DM_Inline_Keyword_Links::init();
