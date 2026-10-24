const assert=require('node:assert/strict');
function luminance(hex){const rgb=hex.replace('#','').match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];}
function contrast(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
const pairs=[['texto','#605760','#ffffff'],['títulos','#2b1520','#ffffff'],['links','#1767ae','#ffffff'],['links em creme','#1767ae','#fdf9f6'],['botão','#ffffff','#1767ae'],['botão hover','#ffffff','#11528d'],['menu ativo','#103f6b','#f2f7ff'],['aviso','#604414','#fff8e8'],['legendas','#665d66','#ffffff'],['metadados','#706773','#ffffff'],['disponível','#235e42','#e8f5ef'],['em breve','#565866','#f1f2f4']];
for(const [label,fg,bg] of pairs){const value=contrast(fg,bg);assert.ok(value>=4.5,`${label}: ${value}`);console.log(`${label}: ${value.toFixed(2)}:1`);}
console.log('OK: pares de texto da paleta atendem a 4,5:1.');
