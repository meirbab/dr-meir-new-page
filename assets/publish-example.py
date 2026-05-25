#!/usr/bin/env python3
"""Publish HA article to dr-meir.com with Rank Math SEO + media + internal links."""
import json, os, sys, base64, urllib.request, urllib.error, urllib.parse

SITE = "https://dr-meir.com"
USER = "2ofnu4"
APP_PW = os.environ["WP_APP_PASSWORD"]
AUTH = base64.b64encode(f"{USER}:{APP_PW}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}

# Media IDs already uploaded
MEDIA = {
    "featured": 53078,    # HA droplet (hero)
    "consistency": 53079, # 3 beakers comparison
    "main_video": 53080,  # Juvederm Vycross rheology comparison
    "panel_video": 53081, # 5-product panel
    "panel_still": 53082, # 5-product still
}

# Internal link targets (slug-based for resilience)
LINKS = {
    "fillers_pillar": "/aesthetics/achieve-a-youthful-look-with-dermal-fillers/",
    "natural_filler": "/aesthetics/natural-filler-advanced-antiaging-treatment-guide/",
    "jawline": "/anti-aging/jawline-contouring-expert-guide/",
    "nasolabial": "/aesthetics/nasolabial-folds-botox-treatment/",
    "stylage": "/aesthetics/stylage-the-perfect-balance-of-volume-and-elasticity/",
    "neauvia": "/aesthetics/neauvia-the-next-generation-of-dermal-fillers/",
    "skin_booster": "/aesthetics/4-3-2024/",  # סקין בוסטר — verify slug
    "collagen": "/aesthetics/restore-youthful-firmness-with-collagen-treatments/",
    "top3": "/aesthetics/top-3-aesthetic-treatments-dr-meir-babaev/",
    "rejuv_offer": "/anti-aging/special-offer-face-neck-rejuvenation-radiesse-hyaluronic-acid/",
    "treatments_index": "/aesthetics/cutting-edge-aesthetic-treatments/",
    "wrinkles": "/aesthetics/fight-the-signs-of-aging-with-wrinkle-solutions/",
}

def L(key, anchor):
    """Internal link helper."""
    href = LINKS[key]
    return f'<a href="{SITE}{href}">{anchor}</a>'

# Build HTML body
HTML = f"""<p class="dm-lead"><strong>אם פעם דיברת עם רופא אסתטי על קמטים, ירידת נפח בלחיים, או טיפול לחות לעור — השם "חומצה היאלורונית" עלה כמעט בוודאות.</strong> זה לא טרנד שיווקי. זו מולקולה אמיתית, שהגוף שלך מייצר בעצמו, וששינתה את פני האסתטיקה הרפואית בעשרים השנים האחרונות.</p>

<p>אבל הנה משהו שרוב המטופלים לא יודעים: לא כל "חומצה היאלורונית" היא אותו דבר. תחת השם הזה מסתתרים עשרות {L("fillers_pillar", "מוצרי פילרים")} שונים, שכל אחד מהם מתנהג אחרת בעור — ובחירה לא נכונה היא אחת הסיבות המרכזיות לתוצאות שלא נראות טבעיות. במאמר הזה תבינו למה.</p>

<h2>מה זה בעצם חומצה היאלורונית</h2>

<p>חומצה היאלורונית (HA, hyaluronic acid) היא <strong>פוליסכריד טבעי</strong> — שרשרת ארוכה של מולקולות סוכר — שמהווה חלק מהותי מהרקמה המחברת בגוף שלנו. בגוף ממוצע יש כ-15 גרם של החומר הזה, ו<strong>מחצית ממנו נמצאת בעור</strong>.</p>

<p>הסיפור שלה מתחיל ב-1934, כשמדענים בידדו אותה לראשונה מתוך הזגוגית של עין השור. שלושים שנה אחר כך, ב-1964, הצליחו לייצר אותה מחוץ לגוף — ומאז היא הפכה לחומר העבודה המרכזי של רפואה אסתטית מודרנית.</p>

<p>תפקידה ביולוגי הוא בעיקרו לקיים את <strong>הסביבה החוץ-תאית</strong> — הג'ל שממלא את החללים בין התאים בעור. בסביבה הזו תאי העור נעים, מתחלקים, מתחדשים. אבל הנכס המרכזי של חומצה היאלורונית הוא יכולת קליטת המים שלה — <strong>מולקולה אחת של חומצה היאלורונית יכולה לקשור עד 1,000 מולקולות מים סביבה</strong>. זו הסיבה שעור עם רמת HA תקינה נראה חי, גמיש, ולח.</p>

<h2>למה הכל משתנה אחרי גיל 25</h2>

<p>ההאטה בייצור הטבעי של חומצה היאלורונית מתחילה כבר בשנות העשרים המוקדמות. עד גיל 30-35, <strong>הצניחה מורגשת</strong>: העור מאבד מהטורגור (היכולת לחזור לצורה אחרי לחיצה), מהאלסטיות, ומהלחות הפנימית. הקמטים הדקים שמופיעים סביב העיניים והפה הם תוצאה ישירה של דילול הג'ל הביו-לוגי הזה — בדיוק אותם {L("wrinkles", "קמטים שאפשר לטפל בהם")} בשלבים מוקדמים יחסית.</p>

<p>תהליך הזדקנות הוא בלתי נמנע, אבל מאיצים אותו גורמים שאפשר לשלוט בהם: עישון, חשיפה מוגזמת לשמש, דיאטות לא מאוזנות, ושינה לקויה. אצל אנשים שחיים בסטרס כרוני או נחשפים לעשרות שעות שמש בלי הגנה, החלוקה בייצור-פירוק של HA נכשלת — והגוף לא מספיק להשלים את החסר.</p>

<p>חשוב להבין: <strong>החזרת HA לעור באמצעות זריקה היא לא "החדרת חומר זר".</strong> הגוף מזהה את המולקולה כמולקולה שלו, פועל איתה באופן רגיל, ובסופו של דבר מפרק אותה לפחמן דו-חמצני ומים. הבטיחות הזו היא מה שהפך את HA למוצר הנפוץ ביותר באסתטיקה.</p>

<h2>שתי משפחות, שני עולמות: HA לא יציבה מול HA יציבה</h2>

<p>זה ההבדל הראשון שכדאי לדעת. תחת המטרייה של "חומצה היאלורונית" יש שני סוגי מוצרים שמתנהגים אחרת לחלוטין:</p>

<h3>חומצה היאלורונית לא יציבה (נטיב)</h3>

<p>קרובה למצב הטבעי של החומר בגוף. היא מתפרקת על-ידי האנזימים שלך תוך <strong>כמה ימים</strong>. מוצרים מהסוג הזה משמשים בעיקר ל:</p>

<ul>
<li><strong>מזותרפיה</strong> — זריקות שטחיות שמטרתן להחזיר לחות וגמישות לעור</li>
<li><strong>ביוריוויטליזציה</strong> — זריקות עמוקות יותר, עם ריכוז גבוה של נטיב HA, שמטרתן לעורר את הפיברובלסטים (התאים שמייצרים קולגן ואלסטין) לעבוד שוב</li>
</ul>

<p>הפעולה כאן היא לא של "מילוי" אלא של <strong>שיקום פיזיולוגי</strong>: מחזירים לעור את הסביבה הביוכימית הטבעית שלו, והעור עצמו מתחדש מבפנים. זה אגב הרציונל מאחורי {L("collagen", "טיפולי הקולגן בקליניקה")} — ההרעלה של תאי העור לייצר את החומרים החיוניים בעצמם.</p>

<h3>חומצה היאלורונית יציבה (פילרים)</h3>

<p>עברה תהליך כימי שמחבר את שרשראות ה-HA זו לזו, כך שהאנזימים בגוף מתקשים לזהות אותה ולפרק אותה. במקום ימים, היא נשארת ברקמה <strong>חודשים עד שנתיים</strong>, תלוי בסוג. מוצרים מהסוג הזה הם ה{L("fillers_pillar", "פילרים")} — מה שמשמש להחזרת נפח, לעיצוב קונטור הפנים, ולמילוי קמטים עמוקים. אצלנו בקליניקה אנחנו עובדים עם {L("natural_filler", "חומרי מילוי מסדרות מוכרות בלבד")}.</p>

<figure class="dm-figure" style="margin:2em 0;text-align:center;">
<img src="{SITE}/wp-content/uploads/2026/05/filler-gel-consistency-comparison.png" alt="שלושה כלים עם ג׳ל פילר בקונסיסטנציות שונות" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;" />
<figcaption style="font-size:0.9em;color:#666;margin-top:0.5em;">פילרים נבדלים בקונסיסטנציה (G' ועמידות) לטובת אזורי טיפול שונים</figcaption>
</figure>

<h2>איך מייצבים HA — ולמה זה משנה לך כמטופל</h2>

<p>תהליך הייצוב הכימי נעשה ברוב המקרים על-ידי מולקולה בשם <strong>BDDE</strong> (1,4-Butanediol diglycidyl ether). היא יוצרת גשרים שמחברים את שרשראות ה-HA זו לזו, ומשנה את המבנה התלת-מימדי של החומר. ככל שכמות הגשרים גדולה יותר — כך הג'ל יציב יותר, צפוף יותר, ונשאר ברקמה זמן ארוך יותר.</p>

<p>אבל יש כאן איזון עדין שהקהילה הרפואית הבינלאומית מדברת עליו יותר ויותר בכנסים בשנים האחרונות: <strong>כמות גדולה מדי של חומר מקשר עלולה לעורר תגובות אלרגיות או דלקתיות אצל חלק מהמטופלים</strong>. הנושא נמצא במחקר פעיל. בקליניקה אנחנו מתעדכנים בספרות המקצועית באופן שוטף, ובוחרים פילרים מיצרנים שהוכחו כבעלי פרופיל בטיחות גבוה — ובכמויות מבוקרות שמתאימות לכל מטופל באופן אישי.</p>

<h2>מונופאזי מול ביפאזי — ההבחנה שמשנה את התוצאה</h2>

<p>זה כבר הופך טכני, אבל זה משפיע על איך הטיפול שלך נראה. פילרים נחלקים לשני סוגים לפי <strong>שיטת הייצור</strong> שלהם:</p>

<h3>ג'ל מונופאזי</h3>
<p>שרשראות ה-HA מקוצצות לחלקיקים בגודל אחיד באמצעות הומוגנייזר. התוצאה: ג'ל <strong>רך, אלסטי, מתפזר באופן אחיד ברקמה</strong>. הוא יוצא בקלות דרך מחט דקה, משתלב כמעט בלתי-נראה ברקמה, ומתפרק באופן אחיד.</p>

<h3>ג'ל ביפאזי</h3>
<p>מיוצר עם חלקיקים בשני גדלים: גסים ועדינים. התוצאה: ג'ל <strong>צפוף יותר, עם יכולת תמיכה מבנית גבוהה</strong>, שמחזיק את הצורה שלו לאורך זמן ארוך יותר.</p>

<p><strong>מתי בוחרים מה?</strong></p>
<ul>
<li><strong>מונופאזי</strong> — כשרוצים תוצאה רכה, טבעית, ב"שכבת מעבר": קמטים שטחיים, גוון עור לא אחיד, או אזורים עם תנועה רבה</li>
<li><strong>ביפאזי</strong> — כשרוצים לעצב קו ברור: {L("jawline", "קו לסת")}, סנטר, מתאר שפתיים — וצריך שהג'ל יישאר במקום שלו ויחזיק את הצורה</li>
</ul>

<p>רופא מנוסה יודע להגיע לתוצאות יפות עם שני הסוגים — הסוד הוא לבחור את הסוג הנכון לאזור הנכון.</p>

<h2>ריאולוגיה — המדע מאחורי הבחירה</h2>

<p>זה אולי החלק הכי לא-מוכר למטופלים, אבל הוא הסיבה האמיתית למה רופא טוב לא משתמש באותו פילר לכל אזור בפנים. <strong>ריאולוגיה</strong> היא תחום שעוסק בהתנהגות זרימה ועיוות של חומרים — ובהקשר של פילרים, היא מתארת שני מאפיינים מרכזיים:</p>

<h3>G' (מודול אלסטיות)</h3>

<p>המידה שבה הג'ל <strong>מתנגד לעיוות ושומר על צורתו</strong> תחת לחץ. ככל שה-G' גבוה יותר, הפילר עומד טוב יותר בלחץ של שרירי הפנים, שינה על הצד, או מסאז'.</p>

<ul>
<li><strong>G' גבוה</strong> — מתאים לאזורים שעובדים קשה: {L("nasolabial", "קמטי האף-שפה (נזולביאליים)")}, זוויות הלסת, סנטר, אזור הלחיים העליונות</li>
<li><strong>G' נמוך</strong> — מתאים לאזורים שדורשים פלסטיות: סביב השפתיים, קמטים שטחיים על המצח או הצוואר, אזור העיניים</li>
</ul>

<h3>קוהזיביות</h3>

<p>כוח ההיצמדות בין חלקיקי הג'ל זה לזה. דמיינו קוביית ג'ל: אם לוחצים עליה מלמעלה, האם היא חוזרת לצורתה? <strong>קוהזיביות גבוהה</strong> = הג'ל חוזר לצורה אחרי לחץ, וגם <strong>לא נודד</strong> מהמקום שבו הזריק אותו הרופא. זה קריטי באזורים כמו עצמות הלחיים והסנטר — שם אנחנו רוצים שהפילר ייצור הרמה אנכית ויישאר שם.</p>

<p>מטופלות שואלות אותנו לעיתים: "למה אצל מישהי אחרת הפילר נדד למקום אחר אחרי כמה חודשים?" התשובה כמעט תמיד קשורה לבחירת מוצר עם קוהזיביות לא מתאימה לאזור.</p>

<h2>הדגמה ויזואלית: כך נראים הבדלים ריאולוגיים</h2>

<p>במקום מילים, ההדגמה הבאה מסבירה את כל מה שדיברנו עליו. בסרטון תראו השוואה מבוקרת של חמשת מוצרי <strong>Juvederm Vycross</strong> — סדרה מהמובילות בעולם — תחת אותו לחץ פיזי. שימו לב להבדלים בתגובה לפעולה הכוחנית:</p>

<figure class="dm-figure dm-video" style="margin:2em 0;text-align:center;">
<video controls preload="metadata" playsinline style="max-width:100%;height:auto;border-radius:8px;" poster="{SITE}/wp-content/uploads/2026/05/juvederm-five-products-still.jpg">
<source src="{SITE}/wp-content/uploads/2026/05/juvederm-vycross-rheology-comparison.mp4" type="video/mp4">
הדפדפן שלכם לא תומך בנגן וידאו.
</video>
<figcaption style="font-size:0.9em;color:#666;margin-top:0.5em;">הדגמת השוואת תכונות ריאולוגיות של פילרי Juvederm Vycross. <small>וידאו: Allergan / Juvederm.</small></figcaption>
</figure>

<p>הקצוות של הספקטרום ברורים: <strong>Volite</strong> (משמאל) הוא הנוזלי ביותר — נטמע בעור באופן הומוגני, אידיאלי לטיפולי לחות; <strong>Volux</strong> (מימין) הוא הצפוף ביותר ושומר על הצורה שלו תחת לחץ — מתאים לעיצוב סנטר וקווי לסת.</p>

<h2>דוגמה מהשטח: סדרת Juvederm כמודל</h2>

<p>אחד מיצרני הפילרים המובילים בעולם הוא חברת Allergan, שמייצרת את סדרת <strong>Juvederm Vycross</strong>. אם תסתכלו על שמות המוצרים בסדרה, תראו טווח שלם של מאפיינים ריאולוגיים שונים, שכל אחד מהם נועד למשימה אחרת:</p>

<table class="dm-table" style="width:100%;border-collapse:collapse;margin:1.5em 0;">
<thead>
<tr style="background:#f5f5f5;">
<th style="padding:10px;border:1px solid #ddd;text-align:right;">מוצר</th>
<th style="padding:10px;border:1px solid #ddd;text-align:right;">אופי הג'ל</th>
<th style="padding:10px;border:1px solid #ddd;text-align:right;">למה הוא משמש</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:10px;border:1px solid #ddd;"><strong>Volux</strong></td><td style="padding:10px;border:1px solid #ddd;">הצפוף ביותר, G' גבוה מאוד</td><td style="padding:10px;border:1px solid #ddd;">עיצוב {L("jawline", "קו לסת וסנטר")}, הרמת קווי מתאר</td></tr>
<tr><td style="padding:10px;border:1px solid #ddd;"><strong>Voluma</strong></td><td style="padding:10px;border:1px solid #ddd;">צפוף, יכולת הרמה גבוהה</td><td style="padding:10px;border:1px solid #ddd;">החזרת נפח ללחיים, עצמות הלחיים</td></tr>
<tr><td style="padding:10px;border:1px solid #ddd;"><strong>Volift</strong></td><td style="padding:10px;border:1px solid #ddd;">בינוני, צפיפות מתונה</td><td style="padding:10px;border:1px solid #ddd;">קמטים עמוקים בינוניים, נזולביאליים</td></tr>
<tr><td style="padding:10px;border:1px solid #ddd;"><strong>Volbella</strong></td><td style="padding:10px;border:1px solid #ddd;">רך, מתפזר בקלות</td><td style="padding:10px;border:1px solid #ddd;">קמטים דקים, אזור השפתיים</td></tr>
<tr><td style="padding:10px;border:1px solid #ddd;"><strong>Volite</strong></td><td style="padding:10px;border:1px solid #ddd;">הנוזלי ביותר, G' נמוך</td><td style="padding:10px;border:1px solid #ddd;">טיפולי לחות עמוקים, אזורים עדינים</td></tr>
</tbody>
</table>

<p>הסדרה הזו היא דוגמה אחת מבין רבות. בשוק יש עשרות מותגי פילרים מובילים — כולל {L("stylage", "Stylage")}, {L("neauvia", "Neauvia")}, Restylane, Belotero, Teosyal, Princess ועוד — וכל אחד מהם בנוי על אותו עיקרון: <strong>מגוון של מוצרים שמתאימים למשימות שונות</strong>.</p>

<figure class="dm-figure" style="margin:2em 0;text-align:center;">
<img src="{SITE}/wp-content/uploads/2026/05/juvederm-five-products-still.jpg" alt="חמשת מוצרי Juvederm Vycross במבט אחד" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;" />
<figcaption style="font-size:0.9em;color:#666;margin-top:0.5em;">חמש דרגות צפיפות בסדרת Juvederm Vycross. <small>תמונה: Allergan / Juvederm.</small></figcaption>
</figure>

<h2>בטיחות — נקודה שחייבים לדבר עליה</h2>

<p>הצד החיובי של חומצה היאלורונית כחומר זריקה: <strong>היא הפיכה.</strong> אם התקבלה תוצאה לא רצויה — הזרקה לא אחידה, נפח עודף, צורה לא טבעית — אפשר להזריק אנזים בשם <strong>היאלורונידאז</strong> שמפרק את הפילר ומחזיר את האזור למצב הקודם. זה לא קיים בשום חומר זריקה אחר באסתטיקה, וזו אחת הסיבות המרכזיות לכך שהאסתטיקה המודרנית בנויה כל-כך סביב HA.</p>

<p>אבל הפיכות לא אומרת חוסר סיכון. סיכונים אפשריים כוללים:</p>
<ul>
<li><strong>חסימת כלי דם</strong> — סיבוך נדיר אבל חמור, שיכול לקרות אם הפילר חודר בטעות לעורק. מבטיחים את ההימנעות ממנו עם הכרה אנטומית מעמיקה והקפדה על טכניקות זריקה נכונות</li>
<li><strong>תגובות דלקתיות</strong> — בדרך כלל קלות וחולפות, אבל לעיתים דורשות טיפול</li>
<li><strong>גרגרים (nodules)</strong> — לעיתים מופיעים אם הפילר הוזרק לא בעומק הנכון</li>
</ul>

<p>הסיכון יורד באופן דרמטי כשהרופא מנוסה, משתמש בפילרים מבית יוצר מוכר, ופועל לפי פרוטוקולים מבוססי ראיות.</p>

<h2>איך בוחרים רופא ומוצר — נקודות לבדיקה</h2>

<p>לפני שאתם מסכימים לטיפול, שווה לבדוק כמה דברים:</p>
<ol>
<li><strong>שאלו איזה מוצר הרופא משתמש בו ולמה דווקא הוא.</strong> תשובה כמו "פילר טוב" היא לא מספיקה. תשובה טובה תכלול את שם המוצר, ולמה הוא מתאים לאזור הספציפי שלכם</li>
<li><strong>בדקו שהמוצר רשום במשרד הבריאות.</strong> בישראל, פילרים מאושרים נמצאים ברשימה הציבורית</li>
<li><strong>שאלו על תכנית טיפול שלמה, לא רק על הזריקה.</strong> אסתטיקה טובה היא תהליך</li>
<li><strong>אל תרדפו אחרי המחיר הזול ביותר.</strong> פילרים זולים מדי לרוב לא מהיצרנים המוכרים, ויש לזה השלכות בטיחות</li>
</ol>

<h2>בשורה התחתונה</h2>

<p>חומצה היאלורונית היא לא חומר אחד — היא משפחה שלמה של מוצרים, שכל אחד מהם תוכנן בקפידה למשימה ספציפית. הבחירה בין נטיב לבין יציב, בין מונופאזי לביפאזי, בין G' גבוה לנמוך — היא לא טכניקלית, היא <strong>הסיבה למה שתי מטופלות שעוברות "אותו טיפול" יכולות לקבל תוצאות שונות לחלוטין</strong>.</p>

<p>הטיפים הכי טובים שאני יכול לתת לכל מי שמתעניין בטיפול עם חומצה היאלורונית:</p>

<ul>
<li><strong>אל תבחרו את המוצר — בחרו את הרופא.</strong> רופא טוב יבחר את המוצר הנכון בשבילכם</li>
<li><strong>שאלו שאלות.</strong> רופא טוב ישמח להסביר מה הוא משתמש בו ולמה</li>
<li><strong>תוצאה טבעית מצריכה זמן.</strong> ההזרקה היא רגע אחד; הטיפול המלא יכול לכלול מספר ביקורים</li>
</ul>

<p>הרבה ממה שאמרתי כאן הופך לאט-לאט לידיעה כללית בקרב מטופלים מתוחכמים — וזה דבר מצוין. ככל שאתם מבינים יותר, הציפיות שלכם מציאותיות יותר, והשיחה איתכם בקליניקה הופכת לשותפות אמיתית.</p>

<h2>קריאה נוספת בקליניקה</h2>
<ul>
<li>{L("fillers_pillar", "המדריך לפילרים — איך עובד הטיפול ולמי הוא מתאים")}</li>
<li>{L("natural_filler", "חומרי מילוי טבעיים — סקירת מוצרים מתקדמים")}</li>
<li>{L("jawline", "מיצוק קו הלסת — מדריך מעמיק")}</li>
<li>{L("nasolabial", "טיפול בקמטי האף-שפה (נזולביאליים)")}</li>
<li>{L("rejuv_offer", "הצערת פנים וצוואר — שילוב חומצה היאלורונית ורדיאס")}</li>
<li>{L("top3", "שלושת הטיפולים האסתטיים הכי פופולריים בקליניקה")}</li>
</ul>

<hr style="margin:3em 0 1em 0;border:0;border-top:1px solid #ddd;" />
<p style="font-size:0.85em;color:#888;font-style:italic;">המאמר מבוסס על תכנים מקצועיים ממודול ההכשרה הראשון בקורס הקונטורולוגיה של ד"ר Olga Buyanova (Faceline School), בתוספת הקשר קליני וניסיון אישי מהקליניקה. וידאו ההמחשה: Allergan / Juvederm Vycross.</p>
"""

# ============ Create Post ============
TITLE = "חומצה היאלורונית — המדריך המלא: למה זה משנה ואיך הרופא בוחר עבורכם"
SLUG = "hyaluronic-acid-complete-guide-fillers-mesotherapy"
EXCERPT = "מדוע חומצה היאלורונית הפכה לחומר המרכזי באסתטיקה רפואית, איך נבדלים פילרים יציבים מטיפולי לחות, מהי ריאולוגיה ולמה אותה זריקה מתאימה לאזור אחד בפנים אבל לא לאחר. מדריך מעמיק לקהל הרחב."

post_payload = {
    "title": TITLE,
    "slug": SLUG,
    "content": HTML,
    "excerpt": EXCERPT,
    "status": "publish",
    "categories": [5],  # aesthetics
    "featured_media": MEDIA["featured"],
    "comment_status": "closed",
    "ping_status": "closed",
    "meta": {
        "rank_math_title": "חומצה היאלורונית: המדריך המלא לפילרים וטיפולי לחות | ד\"ר מאיר באבאיב",
        "rank_math_description": EXCERPT,
        "rank_math_focus_keyword": "חומצה היאלורונית,פילר חומצה היאלורונית,טיפול פנים חומצה היאלורונית",
        "rank_math_robots": ["index", "follow"],
        "rank_math_pillar_content": "off",
    }
}

req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/posts",
    data=json.dumps(post_payload).encode("utf-8"),
    headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.load(r)
        print(f"✓ POST CREATED")
        print(f"  ID: {result['id']}")
        print(f"  URL: {result['link']}")
        print(f"  Status: {result['status']}")
        post_id = result['id']
        post_url = result['link']
except urllib.error.HTTPError as e:
    print(f"✗ HTTP {e.code}: {e.read().decode()}")
    sys.exit(1)

# Save the new post info for next steps
with open(os.path.expanduser("~/Telegram-Material/work/buyanova-contourology/published.json"), "w") as f:
    json.dump({"id": post_id, "url": post_url, "title": TITLE, "slug": SLUG, "media": MEDIA, "links": LINKS}, f, ensure_ascii=False, indent=2)
print(f"\n  Saved to: ~/Telegram-Material/work/buyanova-contourology/published.json")
