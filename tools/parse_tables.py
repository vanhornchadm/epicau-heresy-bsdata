"""Extract headings, paragraphs and wikitables from archived MediaWiki pages into JSON."""
import sys, os, re, json, html
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []; self.in_content = False; self.depth = 0
        self.heading = None; self.htext = ''
        self.tables = []  # stack of tables
        self.cell = None; self.para = None; self.skip = 0; self.captions = {}
    def handle_starttag(self, tag, a):
        a = dict(a)
        if a.get('id') == 'mw-content-text': self.in_content = True
        if not self.in_content: return
        if self.skip:
            if tag == 'div': self.skip += 1
            return
        if tag == 'div' and a.get('id') == 'toc':
            self.skip = 1
            return
        if False:
            if tag == 'div': self.skip += 1
            return
        if tag in ('script', 'style'): self.skip_tag = tag
        if re.fullmatch(r'h[1-6]', tag): self.heading = int(tag[1]); self.htext = ''
        elif tag == 'table': self.tables.append([])
        elif tag == 'caption' and self.tables:
            self.cell = {'text': '', 'caption': True}
        elif tag == 'tr' and self.tables: self.tables[-1].append([])
        elif tag in ('td', 'th') and self.tables:
            self.cell = {'text': '', 'th': tag == 'th', 'colspan': int(a.get('colspan', 1) or 1), 'rowspan': int(a.get('rowspan', 1) or 1)}
        elif tag == 'br' or tag == 'li' or tag == 'p':
            self._add('\n')
        if tag == 'p' and not self.tables and self.heading is None: self.para = ''
    def handle_endtag(self, tag):
        if not self.in_content: return
        if self.skip:
            if tag == 'div': self.skip -= 1
            return
        if re.fullmatch(r'h[1-6]', tag) and self.heading:
            t = re.sub(r'\s+', ' ', self.htext.replace('[edit]', '')).strip()
            self.out.append({'h': self.heading, 'text': t}); self.heading = None
        elif tag == 'caption' and self.cell is not None and self.tables:
            self.captions[len(self.tables)] = re.sub(r'\s+', ' ', self.cell['text']).strip(); self.cell = None
        elif tag in ('td', 'th') and self.cell is not None and self.tables:
            if not self.tables[-1]: self.tables[-1].append([])
            self.cell['text'] = re.sub(r'[ \t\xa0]+', ' ', self.cell['text'])
            self.cell['text'] = '\n'.join(l.strip() for l in self.cell['text'].split('\n') if l.strip())
            self.tables[-1][-1].append(self.cell); self.cell = None
        elif tag == 'table' and self.tables:
            t = self.tables.pop()
            rows = [r for r in t if r]
            if self.tables:  # nested table: flatten into parent cell text
                if self.cell is not None:
                    self.cell['text'] += '\n' + '\n'.join(' | '.join(c['text'] for c in r) for r in rows)
            else:
                self.out.append({'table': rows, 'caption': self.captions.pop(1, '')})
        elif tag == 'p' and self.para is not None:
            t = re.sub(r'\s+', ' ', self.para).strip()
            if t: self.out.append({'p': t})
            self.para = None
        elif tag in ('li',) and not self.tables and self.para is None:
            pass
        if tag == 'div' and self.depth: pass
    def _add(self, t):
        if self.heading is not None: self.htext += t
        elif self.cell is not None: self.cell['text'] += t
        elif self.para is not None: self.para += t
    def handle_data(self, d):
        if not self.in_content or self.skip: return
        self._add(d)

def parse(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<(script|style)\b.*?</\1>', '', s, flags=re.S)
    m = s.find('id="mw-content-text"'); e = s.find('class="printfooter"')
    s = s[s.rfind('<', 0, m):e] if m > 0 else s
    p = P(); p.feed(s)
    # also gather list items as paragraphs
    return p.out

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if not f.endswith('.html'): continue
        out = parse(os.path.join(src, f))
        json.dump(out, open(os.path.join(dst, f[:-5] + '.json'), 'w'), indent=1, ensure_ascii=False)
        print(f, sum(1 for x in out if 'table' in x), 'tables')
