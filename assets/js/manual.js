/* Interações locais: sem requisições, bibliotecas ou serviços externos. */
(function () {
  'use strict';
  const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  function search(query, entries) {
    const q = normalize(query);
    if (!q) return [];
    const terms = q.split(' ').filter(word => !['a','o','e','de','do','da','os','as','um','uma','para','com'].includes(word));
    if (!terms.length) return [];
    return entries.map(entry => {
      const title = normalize(entry.title), text = normalize(entry.text+' '+(entry.keywords || ''));
      const match = terms.every(term => text.includes(term) || title.includes(term));
      const score = (title.includes(q) ? 100 : 0) + terms.reduce((sum,t) => sum + (title.includes(t) ? 20 : 0), 0) + (normalize(entry.description).includes(q) ? 10 : 0) + (normalize(entry.keywords || '').includes(q) ? 40 : 0);
      return {entry, score, match};
    }).filter(result => result.match).sort((a,b) => b.score-a.score).map(result => result.entry);
  }
  // Exporta somente a função pura para verificações isoladas do manual.
  if (typeof module !== 'undefined' && module.exports) module.exports = {normalize,search};
  if (typeof document === 'undefined') return;
  const toggler = document.querySelector('#docs-sidebar-toggler');
  const sidebar = document.querySelector('#docs-sidebar');
  const shade = document.querySelector('.mobile-shade');
  if (toggler && sidebar) {
    const narrow = window.matchMedia('(max-width:1199px)');
    const setMenu = (open,restore=false) => {
      sidebar.classList.toggle('sidebar-visible',open);
      shade.classList.toggle('is-open',open && narrow.matches);
      toggler.setAttribute('aria-expanded',String(open));
      toggler.setAttribute('aria-label',open ? 'Fechar menu do familiar' : 'Abrir menu do familiar');
      sidebar.inert=narrow.matches && !open;
      if (restore) toggler.focus();
    };
    toggler.addEventListener('click',()=>setMenu(toggler.getAttribute('aria-expanded')!=='true'));
    shade.addEventListener('click',()=>setMenu(false,true));
    narrow.addEventListener('change',()=>setMenu(false));
    document.addEventListener('keydown',event=>{
      if (event.key==='Escape' && toggler.getAttribute('aria-expanded')==='true') setMenu(false,true);
    });
    setMenu(false);
  }
  const dialog=document.querySelector('#image-dialog');
  if (dialog) {
    let trigger=null;
    const close=()=>dialog.close();
    document.querySelectorAll('.zoom-image').forEach(anchor=>anchor.addEventListener('click',event=>{
      event.preventDefault(); trigger=anchor;
      dialog.classList.remove('zoom-original');
      dialog.querySelector('.lightbox-zoom').setAttribute('aria-pressed','false');
      dialog.querySelector('.lightbox-zoom').textContent='Tamanho original';
      const img=anchor.querySelector('img');
      dialog.querySelector('#expanded-image').src=anchor.href;
      dialog.querySelector('#expanded-image').alt=img.alt;
      dialog.querySelector('#image-caption').textContent=img.alt;
      dialog.querySelector('#image-title').textContent='Captura ampliada';
      dialog.showModal();
      dialog.querySelector('.lightbox-close').focus();
    }));
    dialog.querySelector('.lightbox-close').addEventListener('click',close);
    dialog.querySelector('.lightbox-zoom').addEventListener('click',event=>{
      const original=dialog.classList.toggle('zoom-original');
      event.currentTarget.setAttribute('aria-pressed',String(original));
      event.currentTarget.textContent=original?'Ajustar à tela':'Tamanho original';
    });
    dialog.addEventListener('click',event=>{if(event.target===dialog)close();});
    dialog.addEventListener('close',()=>{if(trigger)trigger.focus();});
  }
  const results=document.querySelector('#search-results');
  if (results) {
    const input=document.querySelector('#search-input'), status=document.querySelector('#search-status');
    const form=input.closest('form');
    const render=query=>{
      results.replaceChildren();
      const matches=search(query,window.MYZELO_SEARCH || []);
      if(!normalize(query)){status.textContent='Digite um termo para buscar no manual familiar.';return;}
      status.textContent=matches.length ? `${matches.length} ${matches.length===1?'resultado encontrado':'resultados encontrados'} para “${query}”.` : `Nenhum resultado para “${query}”. Tente menos palavras, como “cadastro” ou “pagamento”.`;
      matches.forEach(entry=>{
        const li=document.createElement('li'), group=document.createElement('span'), h=document.createElement('h2'), a=document.createElement('a'), p=document.createElement('p');
        group.className='result-group';group.textContent=entry.group;
        a.href=entry.url; a.textContent=entry.title; h.append(a);
        const normalized=normalize(query), titleMatch=normalize(entry.title).includes(normalized);
        p.textContent=entry.description;
        if(!titleMatch){
          const first=normalized.split(' ').find(t=>t.length>3);
          // Índice normalizado somente para localizar um trecho; texto original preservado.
          const pos=first ? normalize(entry.text).indexOf(first) : -1;
          if(pos>0)p.textContent='…'+entry.text.slice(Math.max(0,pos-50),Math.min(entry.text.length,pos+200))+'…';
        }
        li.append(group,h,p);results.append(li);
      });
    };
    input.value=new URLSearchParams(window.location.search).get('q') || '';
    render(input.value);
    input.addEventListener('input',()=>render(input.value));
    form.addEventListener('submit',event=>{
      event.preventDefault();render(input.value);
      const url=new URL(window.location.href);url.searchParams.set('q',input.value);
      try {window.history.replaceState(null,'',url);} catch (_) { /* file:// continua utilizável */ }
    });
  }
})();
