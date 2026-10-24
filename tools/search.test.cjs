const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const {normalize,search}=require('../assets/js/manual.js');
const context={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../assets/js/search-index.js'),'utf8'),context);
const entries=context.window.MYZELO_SEARCH;
assert.equal(normalize('Confirmação, E-MAIL!'),'confirmacao e mail');
for(const query of ['cadastro','pessoa assistida','pagamento','esqueci a senha']) {
  const results=search(query,entries);
  assert.ok(results.length>0,query);
  assert.ok(results.every(x=>x.url.startsWith('familiar/')),query);
}
assert.equal(search('esqueci a senha',entries)[0].url,'familiar/recuperar-acesso.html');
assert.equal(search('pagamento',entries)[0].url,'familiar/pagamento.html');
assert.equal(JSON.stringify(search('conclusão',entries)),JSON.stringify(search('conclusao',entries)));
assert.equal(search('astronautazzz',entries).length,0);
assert.equal(search('',entries).length,0);
assert.equal(search('   ',entries).length,0);
assert.ok(search('Nenhum procedimento',entries).some(x=>x.url==='familiar/solicitar-cuidado.html'));
console.log('OK: buscas obrigatórias, conteúdo, ranking, acentos, vazio, sem resultados e escopo familiar.');
