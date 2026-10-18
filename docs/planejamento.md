# Planejamento e pendências da entrega

Referência: roteiro de avaliação em `docs/Roteiro Projeto Final.pdf`.

## Escopo

Linha B3, oito ações, três anos de histórico diário, cinco gráficos e quatro KPIs. Interface nativa do Streamlit, com sidebar, estado, reset, cache, abas e download. A base local permite a execução sem credenciais; o banco é opcional e possui modelo SQL preparado.

## Cards sugeridos para o Trello

Crie um quadro pessoal público com **Backlog**, **A fazer**, **Em andamento** e **Concluído**. Atribua cada card a Samuel Bucco, descreva a entrega e mantenha apenas uma tarefa em andamento. Esta lista não representa movimentações já realizadas no Trello.

| Card | Critério para concluir |
|---|---|
| Definir o problema e as oito ações | Explicar as cinco perguntas e a escolha da amostra |
| Coletar e tratar as cotações | Reproduzir a base e conferir cobertura, nulos e duplicatas |
| Conferir cálculos financeiros | Verificar manualmente retorno, base 100 e drawdown |
| Construir os filtros e KPIs | Testar seleção, período, reset e deltas |
| Criar os cinco gráficos | Conferir rótulos, unidades e relação com cada pergunta |
| Documentar método e resultados | Revisar README, fórmulas, números e limitações |
| Revisar o código com autonomia | Explicar e adaptar as funções do guia de estudo |
| Revisar o app visualmente | Conferir as quatro abas no navegador e capturar telas reais |
| Publicar no Streamlit Cloud | Abrir o link público e testar filtros/exportação |
| Preparar a entrega final | Gravar vídeo, incluir Trello e capturas no README, enviar links no AVA |

## Estado verificável desta versão

- Implementados: ETL, dados locais, cálculos, cinco gráficos, quatro KPIs, filtros, cache, reset, abas, exportação, modelo SQL, EDA e documentação inicial.
- Verificados: execução pelo AppTest do Streamlit, filtros cruzados, ausência de seleção, período sem pregões e restauração. Cálculos conferidos com uma série controlada.
- Supabase validado: conexão real, oito ativos, 5.960 cotações e execução do painel via banco, com quatro KPIs e cinco gráficos sem exceções.
- Pendente: validação visual e capturas da interface, deploy, quadro Trello público e sua captura, gravação do vídeo, LinkedIn e revisão pessoal.
- A integração de navegador apresentou falha de inicialização nesta sessão; não há captura real da aplicação anexada.

## Versionamento

Use `feature/*` a partir de `develop`; integre em `develop` e, após revisão, em `main`. Preserve as branches após os merges, conforme o roteiro. Faça commits reais por etapa, sem reconstruir atividades ou datas que não aconteceram.

## Links que faltam no README

Aplicação Streamlit Cloud, quadro Trello público, captura do quadro, capturas do app, vídeo e LinkedIn do estudante.

O roteiro informa entrega até **03/11/2026 às 22h**. Confira também o prazo exibido no AVA. Após submeter a versão final, o roteiro orienta não alterar o repositório até receber a nota.
