"""Verificações específicas da documentação, sem acessar o Home Care."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self): super().__init__();self.refs=[];self.ids=[];self.images=[];self.h1=0;self.current=[];self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if a.get('aria-current')=='page':self.current.append(a.get('href'))
        if tag=='img':self.images.append(a)
        for key in ('href','src'):
            if a.get(key):self.refs.append((tag,key,a[key]))
errors=[]; documents={}; refs=0
for path in ROOT.rglob('*.html'):
    doc=Page();raw=path.read_text(encoding='utf-8');doc.feed(raw);documents[path.resolve()]=doc
    if doc.lang!='pt-BR':errors.append(f'{path.name}: idioma')
    if doc.h1!=1:errors.append(f'{path.name}: h1={doc.h1}')
    if len(doc.ids)!=len(set(doc.ids)):errors.append(f'{path.name}: IDs duplicados')
    if 'https://themes.3rdwavemedia.com/' not in raw:errors.append(f'{path.name}: crédito ausente')
    if re.search(r'lorem ipsum|Section Item|coderdocs-logo|github code example',raw,re.I):errors.append(f'{path.name}: exemplo restante')
    if re.search(r'signature=|/email/verify/|/reset-password/[0-9a-f]{20}|mundodos12|LOCAL_DEMO_PASSWORD',raw,re.I):errors.append(f'{path.name}: credencial/link individual')
    if path.parent.name=='familiar':
        if doc.current!=[path.name]:errors.append(f'{path.name}: página atual incorreta')
        for token in ['Objetivo:','Antes de começar:','Caminho:','Resultado esperado','Regras que você precisa conhecer','Anterior e próximo','Nesta página']:
            if token not in raw:errors.append(f'{path.name}: falta {token}')
        if not any('screenshots/' in x.get('src','') for x in doc.images):errors.append(f'{path.name}: sem captura')
    for img in doc.images:
        if 'alt' not in img:errors.append(f'{path.name}: imagem sem alt')
for path,doc in documents.items():
    for tag,key,url in doc.refs:
        parts=urlsplit(url);refs+=1
        if parts.scheme or parts.netloc:
            if key=='src' or tag=='link':errors.append(f'{path.name}: recurso externo {url}')
            continue
        if url.startswith('/'):
            errors.append(f'{path.name}: caminho absoluto {url}');continue
        target=(path.parent/unquote(parts.path)).resolve() if parts.path else path
        if not target.exists():errors.append(f'{path.name}: ausente {url}');continue
        if parts.fragment and target.suffix=='.html' and parts.fragment not in documents[target].ids:errors.append(f'{path.name}: âncora ausente {url}')
for path in (ROOT/'assets/css').glob('*.css'):
    for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)',path.read_text(encoding='utf-8')):
        if url.startswith('data:'):continue
        if url.startswith(('http:','https:','//')):errors.append(f'{path.name}: CSS externo {url}')
        elif not (path.parent/url).resolve().exists():errors.append(f'{path.name}: CSS recurso ausente {url}')
data=(ROOT/'assets/js/search-index.js').read_text(encoding='utf-8').split('window.MYZELO_SEARCH = ',1)[1].rstrip(';\n')
entries=json.loads(data)
if len(entries)!=len(list((ROOT/'familiar').glob('*.html'))):errors.append('Índice não cobre todos os artigos')
for entry in entries:
    if not entry['url'].startswith('familiar/') or not (ROOT/entry['url']).exists():errors.append('Índice fora do manual familiar')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print(f'OK: {len(documents)} páginas, {refs} referências e {len(entries)} artigos de busca. Links, âncoras, imagens, recursos locais, estrutura e privacidade verificados.')
