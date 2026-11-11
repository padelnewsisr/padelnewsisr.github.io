# מעדכן את הכותרות הקבועות בדף (בשביל מנועי חיפוש) ואת מפת האתר, לפי news.json
import json, html, datetime, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((root / 'news.json').read_text(encoding='utf-8'))
items = [i for i in d.get('items', []) if i.get('category') != 'opinion'][:12] + \
        [i for i in d.get('items', []) if i.get('category') == 'opinion'][:4]
rows = []
for it in items:
    t = html.escape(it.get('title', ''))
    s = html.escape((it.get('summary', '') or '')[:220])
    rows.append(f'<article class="item seo-item"><h2><a href="#n-{html.escape(it.get("id",""))}">{t}</a></h2><p>{s}</p></article>')
block = ('<!--SEO-START--><div class="seo-static"><p class="empty">טוען חדשות…</p>'
         + ''.join(rows) + '</div><!--SEO-END-->')
p = root / 'index.html'
s = p.read_text(encoding='utf-8')
s = re.sub(r'<!--SEO-START-->.*?<!--SEO-END-->', lambda m: block, s, flags=re.S)
p.write_text(s, encoding='utf-8')
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
(root / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>https://padelnewsisr.github.io/</loc><lastmod>{today}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>\n'
    '</urlset>\n', encoding='utf-8')
print('seo ok', len(rows))
