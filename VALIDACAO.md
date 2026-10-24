# Registro da entrega familiar

Revisão: 07/10/2026. Aplicação de referência: Home Care/myzelo em `localhost:8000`, revisão `1d2aba5e77bc77d76fc419bf12c645e28bc95ded`, incluindo as alterações locais de interface já presentes. PostgreSQL e Mailpit locais. Fonte do template e licença em `ORIGEM.txt`.

## Material entregue

- 20 páginas HTML: central, busca e 18 artigos do familiar.
- 31 capturas reais, com dados fictícios. A jornada principal vai de cadastro e primeiro acesso até Concluído.
- Fontes, CSS, JavaScript, logotipo e capturas locais. Nenhum recurso externo é necessário para consultar o manual.
- Busca por títulos e conteúdo, sem distinção de acentos, restrita aos artigos familiares.
- Menu responsivo, indicação da página atual, sumário, anterior/próximo, link para pular ao conteúdo e ampliação com botão Fechar, Esc e tamanho original.

## Jornada e evidências da aplicação

Conta adicional de documentação: Marina Oliveira, identificada nas capturas pelo e-mail fictício `familia.documentacao@example.test`. Os acessos familiar e profissional preparados anteriormente foram preservados. Nenhuma senha foi incluída neste projeto.

1. A conta adicional foi criada pela ação existente `CreateNewUser`, com sua validação normal e evento `Registered`. O formulário de cadastro foi inspecionado e capturado com nome e e-mail, sem senha visível. Nenhuma regra de autenticação foi desativada.
2. Login realizado pelo navegador, primeiro acesso preenchido e salvo com nome e WhatsApp.
3. Antes da confirmação do e-mail, foi possível salvar as cinco etapas do rascunho. A revisão mostrou o envio desabilitado e o aviso de confirmação.
4. Pessoa assistida Helena Oliveira e endereço fictício cadastrados pela própria solicitação. Agenda: quarta-feira, quatro horas, início em 07/10/2026 às 09:00. Necessidades: independente, sem auxílio, companhia e supervisão, nenhum procedimento.
5. Validação negativa observada na agenda: enviar sem marcar dias retornou “O campo dias da semana é obrigatório.” O dia foi preenchido e o fluxo avançou normalmente.
6. Rascunho retomado pelo botão Continuar, com os dados preservados. Etapa anterior aberta para conferir a agenda salva. A janela Excluir foi aberta e cancelada; a irreversibilidade e a restrição a rascunhos foram conferidas na interface e na ação existente. O rascunho principal não foi excluído.
7. Confirmação de e-mail executada pelo link real da mensagem local no Mailpit. A revisão passou a permitir Enviar solicitação. Links individuais não foram incluídos nas capturas nem nos HTMLs.
8. Envio realizado pelo navegador. A solicitação #1 passou para Buscando profissional e recebeu uma oportunidade compatível.
9. Reserva preparada com o profissional de teste pela ação existente `AcceptCareOpportunity`, mantendo verificações de titularidade, compatibilidade e disponibilidade. A tela familiar mostrou Aguardando pagamento e a janela de 30 minutos.
10. A tela de pagamento foi capturada antes do cadastro fiscal: pendência exibida, autorização desabilitada. Dados fiscais fictícios preenchidos e salvos no navegador, sem intervenção no banco.
11. Autorizar pagamento de teste executado pelo navegador. A aplicação confirmou Atendimento autorizado, sem cobrança real.
12. O início e o relato de conclusão pelo profissional foram realizados pelas ações existentes `StartCareAssignment` e `ReportCareAssignmentCompletion`. Os estados Em atendimento e Aguardando confirmação foram capturados na área familiar.
13. Confirmar conclusão executado no navegador pela família. Estado Concluído e linha do tempo completa conferidos. O cartão concluído permaneceu no histórico com Visualizar.
14. Adicionar pessoa e Editar conferidos no cadastro auxiliar. Paulo Oliveira foi adicionado como segundo cadastro fictício; Helena foi aberta para edição e salva.
15. Meu perfil e Senha e segurança inspecionados e capturados. Regras de alteração de e-mail e senha confrontadas com os controladores e validações atuais. Não foi alterada a senha dos acessos existentes.
16. Recuperação de senha enviada pelo formulário real e recebida no Mailpit. A tela Reset password foi aberta pelo link da mensagem e capturada sem senhas; a redefinição não foi submetida. Os rótulos em inglês foram preservados no tutorial.

## Preparação local e restauração

Foi utilizado um auxiliar local ignorado pelo Git em `home-care/.codex/docs-demo.php` para criar a conta e chamar as três ações do profissional. O auxiliar verifica o ambiente local e o uso do Mailpit, recebe a senha por variável de ambiente e não a grava no arquivo. Ações e validações existentes permaneceram ativas. Não foram usados SQL direto, alteração de estados por UPDATE, bypass de Stripe ou patches temporários na aplicação. Portanto, não houve código do produto a restaurar. O cenário de demonstração permanece no banco local para consulta.

As alterações já existentes no repositório Home Care foram preservadas. Nenhum commit, push ou deploy foi realizado.

## Verificações específicas da documentação

- `python tools/check.py`: 20 páginas, 798 referências. Verifica destinos de links, âncoras, imagens e recursos CSS; idioma, título principal, página atual, blocos editoriais, crédito, ausência de exemplos do template e padrões de links individuais/credenciais.
- `node tools/search.test.cjs`: cadastro, pessoa assistida, pagamento, esqueci a senha, conteúdo das etapas, equivalência com/sem acentos, consulta vazia, nenhum resultado e restrição familiar.
- `node tools/contrast.test.cjs`: 12 pares da paleta de texto; menor relação verificada de 5,42:1, acima de 4,5:1. Isso é uma verificação da paleta usada, não uma certificação geral de acessibilidade das imagens do produto.
- Navegador: central e artigos em desktop; busca executada com todos os termos pedidos, “confirmacao” sem acento e “astronautazzz” sem resultados. “Cadastro” prioriza Criar uma conta familiar; “pagamento” prioriza Reserva e pagamento simulado.
- Navegador: os 18 artigos percorridos em 390 px, sem estouro horizontal e com uma única página marcada como atual. Central e busca também conferidas em 320 px.
- Teclado: âncora do sumário, imagem aberta por Enter, Esc fecha o diálogo e devolve foco ao link; Fechar também funciona. Zoom original confirmado com a largura real da captura. Menu móvel abre, navega e fecha com Esc.
- Console da documentação sem erros durante a passagem pelos artigos.

Somente verificações novas e específicas deste projeto estático foram executadas. Não foram executados testes preexistentes, suíte completa, build, lint, análise estática, verificação de tipos ou formatadores do Home Care.

## Limites da versão documentada

- Pagamento explicitamente simulado; orçamento temporário de teste. Não há cobrança real, repasse, disputa operacional ou emissão de nota fiscal neste fluxo.
- Histórico é a consulta de solicitações, sem inventar relatórios ou exportações.
- Contestar atendimento e login com Google aparecem como Em breve.
- Recuperação e redefinição de senha ainda têm rótulos em inglês.
- A gestão de endereços é ensinada pela etapa Endereço da solicitação, que é o caminho exposto na navegação atual.
- O profissional só foi usado para avançar a jornada familiar. Seu manual e a hospedagem definitiva permanecem para outra entrega.

## Ajustes visuais após revisão — 07/10/2026

- Menu: removido o deslocamento vertical herdado do CoderDocs e centralizadas as três linhas no botão de 44 × 44 px. Conferido no navegador em 1115 px e 390 px, com centros do botão e da marca em y=40 px; abertura e fechamento por teclado preservados.
- Ajuda: refeita a captura `agenda-validacao.jpg` diretamente no aplicativo local, em 1280 × 720 px e JPEG com qualidade 100. A captura anterior estava comprimida lateralmente e não mostrava a mensagem de validação. A nova exibe a etapa Agenda e o erro real “O campo dias da semana é obrigatório.”
- Captura produzida com a conta Familiar Teste, pessoa e endereço fictícios, em um novo rascunho local (solicitação 2). Nenhuma solicitação foi enviada; não houve alteração de código do sistema.
- SHA-256 da captura atualizado em `reference.json`. Conferida a exibição da imagem na Ajuda e sua ampliação por teclado.

## Atualização documental — 24/10/2026 — Ícones do site

- A fonte `content/manual.py` recebeu uma pergunta em [Ajuda](familiar/ajuda.html#faq) sobre ícone quebrado ou quadrado azul no navegador e no aplicativo de senhas. A orientação indica conferir o domínio, atualizar a página e relatar o aplicativo e o contexto se o problema persistir, sem definir prazo para seu cache.
- A seção [Sobre esta entrega](familiar/index.html#versao) e o `README.md` identificam o alcance parcial da atualização. A referência é o código Myzelo `55cf4596b8d77cf72d876373f83cd98e084fe390`, conferido no worktree `myzelo-site-icons/home-care`, com SVG autocontido e alternativas ICO/PNG.
- A implementação, o commit, o push e os resultados locais da correção foram conferidos em fontes e saídas de ferramentas desta conversa. O acompanhamento detalhado está em [Validação de produção do aplicativo](../home-care/docs/validacao-producao.md). A execução do CI, o deploy da revisão corrigida e a exibição no aplicativo de senhas não foram confirmados.
- `tools/generate.py` regenerou 20 páginas e o índice de 18 artigos. A comparação dos hashes anteriores e posteriores mostrou mudanças somente em `familiar/ajuda.html`, `familiar/index.html` e `assets/js/search-index.js`; os demais HTMLs permaneceram iguais.
- `tools/check.py` aprovou 20 páginas, 804 referências e 18 artigos de busca, incluindo links, âncoras, imagens, recursos locais, estrutura e verificações de privacidade previstas pelo verificador.
- Verificação específica em navegador Edge headless, em 1440 × 1000 e 390 × 844 px: a nova resposta da Ajuda abre e fica visível, sem estouro horizontal; buscar por “ícone” encontra a Ajuda; nenhum erro JavaScript foi observado nesses percursos.
- Os nove links relativos dos guias Markdown afetados no aplicativo foram conferidos, incluindo suas âncoras, sem erros. O diff desses guias também passou pela conferência de espaços em branco.
- As capturas de 07/10 e o registro histórico acima foram preservados. Não houve nova captura do produto, reteste de convites em produção nem revalidação dos demais fluxos ou do manual profissional.
- Nesta atualização documental não foram executados testes, build, lint, análise estática, verificação de tipos ou formatadores da aplicação. Não houve novo commit, push, deploy ou publicação do manual.
