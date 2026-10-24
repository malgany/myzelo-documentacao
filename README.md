# Documentação myzelo — Familiar

Site independente, pronto para hospedagem estática. São 18 artigos familiares, a central e a busca. O manual profissional está marcado como **Em breve**. Base visual e revisão dos tutoriais de demonstração: **07/10/2026**. Atualização parcial dos textos de cadastro, primeiro acesso e ajuda sobre ícones: **24/10/2026**.

## Escopo da atualização de 24/10/2026

- O artigo **Criar uma conta familiar** também explica o cadastro pelo convite enviado pela equipe: o titular define a própria senha, e o endereço do convite já fica confirmado ao concluir.
- **Confirmar e-mail e primeiro acesso** diferencia esse convite do cadastro comum e da troca posterior de endereço, que continuam exigindo verificação.
- A validade no e-mail do convite usa apenas data e hora, como `25/10/2026 13:10`, sem o sufixo `-04`; o texto orienta conferir esse prazo e usar **Concluir meu cadastro** na mensagem. Referência: `dd9e60d41a9617ddb5b548c7991cd6be8b2754c3`, com CI e deploy confirmados nesta conversa. O recebimento de um convite novo após o deploy ainda não foi retestado.
- O convite anterior perde a validade quando reenviado; o convite usado não cria outra conta. Contas antigas não foram confirmadas retroativamente.
- A atualização de cadastro foi conferida contra o código `700681250c7610b36ffea75f65ed4b81ea2a16cd`. O reteste manual em produção dos convites ainda está pendente e não foi realizado pela revisão dos ícones.
- A **Ajuda** orienta quem vê o ícone ausente ou um quadrado azul no navegador ou aplicativo de senhas. Referência: correção `55cf4596b8d77cf72d876373f83cd98e084fe390`, com SVG autocontido e alternativas ICO/PNG. O código e os resultados locais foram conferidos, mas a publicação em produção e o resultado no aplicativo de senhas permanecem sem confirmação; não há prazo de cache definido.
- As capturas de 07/10 e os demais tutoriais foram preservados como demonstração histórica. Pagamento simulado e valores de teste não descrevem a prontidão financeira da versão atual em produção. Não houve nova captura nem revisão completa de todos os fluxos.

## Consultar

- Prévia preparada: http://localhost:8010/ (enquanto o servidor local estiver ativo).
- Também é possível abrir `index.html` diretamente no navegador. A busca carrega um índice JavaScript local e não precisa de rede.
- Para iniciar outra prévia, na pasta do projeto execute `python -m http.server 8010 --bind 127.0.0.1` e abra http://localhost:8010/.
- O Home Care não precisa estar ligado para ler o manual.

## Hospedar

Copie `index.html`, `buscar.html`, a pasta `familiar/` e a pasta `assets/` para a raiz da hospedagem estática ou para uma subpasta. Preserve a estrutura e configure `index.html` como página inicial. Não é necessário PHP, Laravel, banco de dados, Node ou Python no servidor. Os arquivos já estão gerados.

Mantenha o crédito com link para Xiaoying Riley no rodapé. Origem e licença estão em `ORIGEM.txt`; mantenha também as licenças das fontes. Não é necessário publicar `content/`, `tools/`, `README.md` nem `VALIDACAO.md`.

## Atualizar textos e busca

1. Edite `content/manual.py`. Cada artigo declara título, seção, objetivo, pré-requisitos, caminho, seções com âncoras, resultado e regras. Os helpers `steps`, `shot`, `note` e `table` padronizam os blocos.
2. Execute `python tools/generate.py`. Esse comando gera todos os HTMLs, o menu, os links anterior/próximo e `assets/js/search-index.js` a partir do mesmo conteúdo. Não edite o índice manualmente.
3. Execute `python tools/check.py` e `node tools/search.test.cjs`.
4. Abra a prévia, confira os artigos afetados em desktop e celular e atualize a data de revisão e a referência de versão.

Para criar um artigo, acrescente uma chamada `page(...)` na ordem desejada em `content/manual.py`. O menu é agrupado pelo nome da seção. Use nomes de arquivo sem acentos. A função `shot` espera imagens em `assets/screenshots/`.

## Atualizar capturas

Use a aplicação local com dados fictícios e sem credenciais visíveis. Capture a interface real, sem a barra de endereço para não expor links individuais. Nunca inclua senhas, tokens, URLs de confirmação ou redefinição. Prefira viewport de 1440 × 1000 e capture a página completa quando o formulário ultrapassar a tela. Confira visualmente o arquivo salvo, pois uma transição de página pode produzir uma captura incompleta. As imagens são JPEG; o diálogo permite ampliá-las e fechá-las por botão ou Esc.

Substitua a imagem mantendo o nome ou ajuste a chamada `shot(...)`; depois gere e valide novamente. Se a proporção mudar, o layout ajusta a altura automaticamente. Mantenha a legenda e o texto alternativo descritivos.

## Estrutura e manutenção

- `assets/css/coderdocs.css`: CSS oficial compilado, incluindo Bootstrap. Preservado sem recompilação.
- `assets/css/myzelo.css`: identidade visual, ajustes responsivos e foco acessível.
- `assets/js/manual.js`: menu móvel, busca sem acentos e ampliação por diálogo nativo.
- `assets/js/search-index.js`: dados gerados, apenas do manual familiar.
- `assets/fonts/`: Poppins local e licença OFL.
- `assets/screenshots/`: capturas reais com dados de demonstração.
- `tools/`: gerador e verificações específicas, usando biblioteca padrão do Python e do Node. Sem dependências para instalar.

A consulta não faz chamadas externas. O link externo no crédito é apenas um link de navegação voluntária. O projeto não contém credenciais nem arquivos de ambiente.

## Referência do sistema

Base das capturas e dos tutoriais de demonstração: Home Care/myzelo no commit `1d2aba5e77bc77d76fc419bf12c645e28bc95ded`, com as alterações locais de interface presentes em 07/10/2026. Referência da atualização parcial de cadastro: `700681250c7610b36ffea75f65ed4b81ea2a16cd`, em 24/10/2026. Referência da orientação sobre ícones: `55cf4596b8d77cf72d876373f83cd98e084fe390`, conferida no worktree `myzelo-site-icons/home-care`; o código antigo do diretório original não foi atualizado por esta edição documental. CoderDocs Bootstrap 5 v3.1, commit `b46485866229821d24c6ba930a4e26e56b5d3acc`. Referência da apresentação da validade no e-mail: `dd9e60d41a9617ddb5b548c7991cd6be8b2754c3`, publicada em 24/10/2026; o mesmo formato foi conferido no código `700681250c7610b36ffea75f65ed4b81ea2a16cd`. Essa referência de publicação é específica do ajuste do convite. Veja `ORIGEM.txt`, `reference.json` e os registros datados em `VALIDACAO.md`.

## Padrão editorial e visual

O site usa a estrutura do CoderDocs: central com cartões, cabeçalho, navegação lateral, artigos por tarefa e rodapé. As cores da myzelo são azul `#1767ae`, azul escuro `#103f6b`, fundo creme `#fdf9f6` e texto `#2b1520`. Fontes locais Poppins, sem serviços externos. O familiar e o profissional devem permanecer em navegações independentes.

Use sempre os rótulos observados no produto, sem inventar funções. Diferencie pagamento de teste e cobrança real; histórico e relatórios; endereço fiscal e de atendimento. Uma mudança de comportamento exige nova conferência do fluxo antes da atualização do texto.
