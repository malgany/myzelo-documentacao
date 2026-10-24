"""Gera HTML estático e índice local. Requer apenas Python 3 (biblioteca padrão)."""
from pathlib import Path
import sys, json, re
from html import escape, unescape
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
from manual import pages

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,d): self.parts.append(d)
def plain(html):
    x=Text(); x.feed(html); return re.sub(r'\s+',' ',' '.join(x.parts)).strip()
def footer(doc=False):
    return '<footer class="footer'+(' doc-footer' if doc else '')+'"><p>myzelo · Manual do familiar · Base visual: 07/10/2026 · Cadastro: atualização parcial em 24/10/2026</p><p>Template CoderDocs — Designed with ♥ by <a href="https://themes.3rdwavemedia.com/" rel="noopener">Xiaoying Riley</a> for developers.</p></footer>'
def head(title,depth=0,description='Documentação da myzelo: manual familiar com tarefas e capturas reais.'):
    base='../' if depth else ''
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | myzelo · Documentação</title><meta name="description" content="{escape(description,quote=True)}"><link rel="icon" href="{base}assets/images/myzelo.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/css/coderdocs.css"><link rel="stylesheet" href="{base}assets/css/myzelo.css"><script defer src="{base}assets/js/search-index.js"></script><script defer src="{base}assets/js/manual.js"></script></head>'''
def header(depth=0,doc=False):
    base='../' if depth else ''
    toggle='<button id="docs-sidebar-toggler" class="docs-sidebar-toggler" aria-label="Abrir menu do familiar" aria-controls="docs-sidebar" aria-expanded="false"><span></span><span></span><span></span></button>' if doc else ''
    return f'''<a class="skip-link" href="#conteudo">Ir para o conteúdo</a><header class="header fixed-top"><div class="branding docs-branding"><div class="header-inner"><div class="d-flex align-items-center gap-3">{toggle}<div class="site-logo"><a class="navbar-brand" href="{base}index.html" aria-label="myzelo — central de documentação"><img class="logo-icon" src="{base}assets/images/myzelo.svg" alt="" width="34" height="34"><span>myzelo</span></a></div><span class="header-note">Central de documentação</span></div><nav class="header-actions" aria-label="Navegação da central"><a class="header-home-link" href="{base}index.html">Todos os manuais</a><a class="docs-search-link" href="{base}buscar.html">Buscar no manual</a></nav></div></div></header>'''
def sidebar(current):
    rows=[]; group=None
    for item in pages:
        if item['group']!=group:
            group=item['group']; rows.append(f'<li class="nav-item section-title">{group}</li>')
        active=' aria-current="page"' if item['slug']==current else ''
        rows.append(f'<li class="nav-item"><a class="nav-link" href="{item["slug"]}.html"{active}>{item["title"]}</a></li>')
    return '<button class="mobile-shade" aria-label="Fechar menu" tabindex="-1"></button><aside id="docs-sidebar" class="docs-sidebar"><div class="sidebar-title">Manual do familiar</div><a class="sidebar-home" href="../index.html">← Trocar de manual</a><nav id="docs-nav" class="docs-nav" aria-label="Tópicos do familiar"><ul class="section-items list-unstyled nav flex-column">'+''.join(rows)+'</ul></nav></aside>'
def lightbox():
    return '<dialog class="lightbox" id="image-dialog" aria-labelledby="image-title"><div class="lightbox-head"><h2 id="image-title">Captura da aplicação</h2><div class="lightbox-actions"><button class="lightbox-zoom" type="button" aria-pressed="false">Tamanho original</button><button class="lightbox-close" type="button" autofocus>Fechar ×</button></div></div><div class="lightbox-image" tabindex="0" aria-label="Imagem ampliada; use as setas para rolar no tamanho original"><img id="expanded-image" alt=""></div><p id="image-caption"></p></dialog>'

index=[]
for i,item in enumerate(pages):
    slug=item['slug']; title=item['title']; sections=item['sections']
    toc='<nav class="toc" aria-label="Nesta página"><h2>Nesta página</h2><ul>'+''.join(f'<li><a href="#{sid}">{name}</a></li>' for sid,name,_ in sections)+'<li><a href="#resultado">Resultado e regras</a></li></ul></nav>'
    body=f'<div class="breadcrumb-line"><a href="../index.html">Central</a> / <a href="index.html">Familiar</a> / {escape(item["group"])}</div><header class="docs-header"><div class="eyebrow">{item["group"]}</div><h1 class="docs-heading">{title}</h1><div class="docs-intro"><p>{item["description"]}</p></div><p class="review-meta">Manual do familiar · Base visual: 07/10/2026 · Cadastro atualizado parcialmente em 24/10/2026 · Telas com dados fictícios</p></header><div class="tutorial-meta"><p><strong>Objetivo:</strong> {item["description"]}</p><p><strong>Antes de começar:</strong> {item["prereq"]}</p><p class="path"><strong>Caminho:</strong> {item["path"]}</p></div>{toc}'
    body+=''.join(f'<section class="docs-section" id="{sid}"><h2 class="section-heading">{name}</h2>{html}</section>' for sid,name,html in sections)
    body+='<section class="docs-section" id="resultado"><h2 class="section-heading">Resultado esperado</h2><p>'+item['result']+'</p><h3>Regras que você precisa conhecer</h3><ul>'+''.join('<li>'+r+'</li>' for r in item['rules'])+'</ul></section>'
    prev=pages[i-1] if i else None; nxt=pages[i+1] if i+1<len(pages) else None
    body+='<nav class="page-nav" aria-label="Anterior e próximo">'+(f'<a href="{prev["slug"]}.html" rel="prev"><small>← Anterior</small>{prev["title"]}</a>' if prev else '<a href="../index.html"><small>← Central</small>Todos os manuais</a>')+(f'<a href="{nxt["slug"]}.html" rel="next"><small>Próximo →</small>{nxt["title"]}</a>' if nxt else '<a href="index.html"><small>Voltar ao início →</small>Manual do familiar</a>')+'</nav>'
    html=head(title,1,item['description'])+'<body class="docs-page" data-root="../">'+header(1,True)+'<div class="docs-wrapper">'+sidebar(slug)+'<main id="conteudo" class="docs-content" tabindex="-1"><div class="container"><article class="docs-article">'+body+'</article></div></main></div>'+footer(True)+lightbox()+'</body></html>'
    (ROOT/'familiar'/f'{slug}.html').write_text(html,encoding='utf-8')
    keywords={'criar-conta':'cadastro cadastrar conta registro familiar','pessoas-assistidas':'pessoa assistida cadastro de pessoas','recuperar-acesso':'esqueci a senha recuperar senha'}.get(slug,'')
    index.append(dict(title=title,group=item['group'],url=f'familiar/{slug}.html',description=item['description'],keywords=keywords,text=plain(item['description']+' '+item['prereq']+' '+item['path']+' '+' '.join(x[1]+' '+x[2] for x in sections)+' '+item['result']+' '+' '.join(item['rules']))))

def search_form(action='buscar.html'):
    return f'<form class="search-form" action="{action}" method="get" role="search"><label class="search-label" for="search-input">O que você precisa fazer?</label><input id="search-input" class="form-control search-input" type="search" name="q" placeholder="Ex.: pessoa assistida, pagamento…" autocomplete="off"><button class="btn search-btn" type="submit">Buscar</button></form>'
home=head('Central de documentação')+'<body data-root="">'+header()+f'''<main id="conteudo" tabindex="-1"><section class="page-header text-center"><div class="container"><p class="eyebrow">Ajuda para cada etapa do cuidado</p><h1 class="page-heading">Como podemos ajudar?</h1><p class="page-subtitle">Aprenda a usar a myzelo com orientações por tarefa, exemplos e telas do sistema.</p>{search_form()}<p class="search-note">A busca consulta o manual do familiar.</p></div></section><section class="cards-section"><div class="container home-container"><div class="row g-4"><div class="col-md-6"><article class="card audience-card"><div class="card-body"><div class="d-flex justify-content-between align-items-start"><div class="audience-icon" aria-hidden="true">♡</div><span class="badge-available">Manual disponível</span></div><h2 class="card-title">Sou familiar</h2><p>Para quem procura cuidado para si ou para alguém da família. Do cadastro ao atendimento concluído.</p><a class="btn btn-primary" href="familiar/index.html">Acessar manual do familiar →</a></div></article></div><div class="col-md-6"><article class="card audience-card inactive"><div class="card-body"><div class="d-flex justify-content-between align-items-start"><div class="audience-icon" aria-hidden="true">＋</div><span class="badge-soon">Em breve</span></div><h2 class="card-title">Sou profissional</h2><p>Uma área própria para quem oferece cuidado. Os tutoriais profissionais serão publicados em outra entrega.</p><span class="text-muted small">Manual ainda não disponível</span></div></article></div></div><div class="start-strip"><div><h2 class="h5">É seu primeiro contato com a myzelo?</h2><p>Comece pelo cadastro ou acompanhe uma jornada fictícia completa.</p></div><a class="btn btn-outline-primary" href="familiar/exemplo-completo.html">Ver exemplo de uso →</a></div><div class="overview-grid"><a href="familiar/solicitar-cuidado.html"><strong>Solicitar cuidado</strong><span>As cinco etapas, com capturas e regras de preenchimento.</span></a><a href="familiar/ajuda.html"><strong>Preciso de ajuda</strong><span>Problemas comuns, perguntas frequentes e glossário.</span></a></div></div></section></main>'''+footer()+'</body></html>'
(ROOT/'index.html').write_text(home,encoding='utf-8')
search=head('Buscar no manual familiar')+'<body data-root="">'+header()+f'''<main id="conteudo" tabindex="-1"><section class="page-header"><div class="container home-container"><p class="eyebrow">Manual do familiar</p><h1 class="page-heading" style="margin-left:0">Buscar uma orientação</h1><p>Pesquise por tarefas, campos ou mensagens do sistema. A busca aceita palavras com ou sem acento.</p>{search_form()}</div></section><div class="container home-container py-4"><noscript><p class="no-js-notice">Ative o JavaScript para pesquisar ou consulte o <a href="familiar/index.html">índice do manual familiar</a>.</p></noscript><p id="search-status" class="result-message" role="status" aria-live="polite">Digite um termo para buscar no manual familiar.</p><div class="search-suggestions" aria-label="Sugestões de busca"><a href="buscar.html?q=cadastro">Cadastro</a><a href="buscar.html?q=pessoa+assistida">Pessoa assistida</a><a href="buscar.html?q=pagamento">Pagamento</a><a href="buscar.html?q=esqueci+a+senha">Esqueci a senha</a></div><ul id="search-results" class="search-results"></ul></div></main>'''+footer()+'</body></html>'
(ROOT/'buscar.html').write_text(search,encoding='utf-8')
(ROOT/'assets/js/search-index.js').write_text('/* Gerado por tools/generate.py; contém somente o manual familiar. */\nwindow.MYZELO_SEARCH = '+json.dumps(index,ensure_ascii=False)+';\n',encoding='utf-8')
print(f'{len(pages)+2} páginas HTML e índice de {len(index)} artigos gerados.')
