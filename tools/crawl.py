import re, os, sys, time, urllib.request, urllib.parse, json
RAW = sys.argv[1]
TS = "20201111221247"
BASE = "https://web.archive.org/web/2020/http://epicau.com/mw/index.php/"
SKIP = re.compile(r'^(Special|File|Talk|User|Help|Category|MediaWiki|Template|Image|EpicAU|Epicau)(_talk)?:', re.I)
def fname(p): return re.sub(r'[^A-Za-z0-9_.-]', '_', urllib.parse.unquote(p)) + '.html'
def fetch(page):
    path = os.path.join(RAW, fname(page))
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return open(path, encoding='utf-8', errors='replace').read()
    url = BASE + page
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (research archive reader)'})
            data = urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'replace')
            open(path, 'w', encoding='utf-8').write(data)
            time.sleep(3)
            return data
        except Exception as e:
            print('  retry', page, e, file=sys.stderr); time.sleep(5)
    return None
def links(s):
    m = re.search(r'id="mw-content-text"(.*?)class="printfooter"', s, re.S)
    body = m.group(1) if m else ''
    out = []
    for h in re.findall(r'href="[^"]*?epicau\.com/mw/index\.php/([^"#?]+)', body):
        h = urllib.parse.unquote(h)
        if not SKIP.match(h) and h != 'Main_Page': out.append(h)
    return out
seen = {}; queue = [('Main_Page', 0)]
while queue:
    p, d = queue.pop(0)
    if p in seen: continue
    s = fetch(p); seen[p] = d
    if s is None: print('FAILED', p, flush=True); continue
    print(d, p, len(s), flush=True)
    if d < 3:
        for l in links(s):
            if l not in seen: queue.append((l, d + 1))
json.dump(seen, open(os.path.join(RAW, '_pages.json'), 'w'), indent=1)
