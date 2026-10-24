# Roteiro de gravação — Ações B3

Objetivo: apresentar o problema, a preparação dos dados, o painel publicado e as conclusões em 3 a 5 minutos. Este roteiro é uma base para ensaio.

## Preparação

- Abra o painel publicado: https://samuel-bucco-projeto-final-b3.streamlit.app/.
- Confirme a fonte Supabase e clique em **Restaurar filtros**. Os exemplos abaixo usam PETR4, VALE3, ITUB4 e WEGE3, no período completo.
- Deixe outra aba com o repositório e outra com o quadro Trello.
- No editor, deixe preparados `src/etl.py`, `src/dados.py` e `src/modelo.sql`. Não execute uma nova coleta durante a gravação.
- Feche a aba `secrets.toml` e telas com credenciais. Não mostre os Secrets do Cloud.
- Faça um teste curto de áudio e confira se textos e gráficos estão legíveis.

## 0:00–0:35 — Apresentação e problema

**Tela:** cabeçalho do painel publicado, com endereço e KPIs visíveis.

**Fala sugerida:**

> Olá, sou Samuel Bucco. Este é meu projeto final do módulo de Visualização de Dados e Business Intelligence. O painel compara retorno e risco de oito ações negociadas na B3 entre 2021 e 2023. A pergunta principal é: quais ações tiveram melhor desempenho e quais oscilações e quedas ocorreram nesse caminho?

## 0:35–1:15 — Coleta e tratamento

**Tela:** mostre a chamada `yf.download` em `src/etl.py`; depois, a função `limpar_dados` em `src/dados.py`.

**Fala sugerida:**

> A coleta foi feita no Yahoo Finance com a biblioteca yfinance. A base contém 5.960 registros, com 745 pregões por ação. Usei Pandas para converter datas e números, verificar nulos e duplicatas e conferir a coerência dos preços. Os dados foram salvos em CSV para permitir a reprodução do tratamento. Os cálculos de desempenho utilizam o fechamento ajustado fornecido pelo provedor.

## 1:15–1:45 — Banco, contingência e organização

**Tela:** mostre brevemente as tabelas e o JOIN em `src/modelo.sql`; em seguida, a pasta `src` e o quadro Trello.

**Fala sugerida:**

> No Supabase, separei o cadastro dos ativos e as cotações diárias. Uma view reúne essas informações para o painel. Se a consulta falhar, a aplicação utiliza o CSV de contingência. O código está organizado em módulos de coleta, dados e indicadores. O versionamento ficou no GitHub e as entregas estão registradas neste quadro Trello.

## 1:45–2:20 — Interatividade e componentes do Streamlit

**Tela:** volte ao painel. Confirme **Fonte em uso: Supabase**. Selecione somente ITUB4 e depois clique em **Restaurar filtros**.

**Fala sugerida:**

> Na barra lateral, posso selecionar setores, ações e período. Os filtros atualizam os quatro indicadores e os gráficos. O estado da sessão preserva a seleção, e este botão restaura o padrão. Para evitar consultas repetidas, a leitura dos dados utiliza cache de dez minutos. Isso reaproveita a base histórica; não representa uma atualização de cotações em tempo real.

## 2:20–3:00 — Desempenho e médias móveis

**Tela:** aba **Desempenho**. Mostre a base 100; depois selecione PETR4 no gráfico de médias móveis.

**Fala sugerida:**

> A base 100 coloca as ações no mesmo ponto inicial, permitindo comparar a evolução relativa. No período completo, PETR4 teve retorno ajustado de aproximadamente 228,69%, enquanto WEGE3 teve 3,51%. O segundo gráfico apresenta o preço e as médias de 21 e 50 pregões. Essas médias suavizam as oscilações e ajudam a observar a trajetória do ativo.

## 3:00–3:50 — Risco, distribuição e drawdown

**Tela:** aba **Risco**. Percorra dispersão, histograma e drawdown; mostre o resumo se houver tempo.

**Fala sugerida:**

> O gráfico de risco e retorno relaciona a volatilidade anualizada com o retorno acumulado. As bolhas representam uma estimativa do volume financeiro. O histograma mostra a distribuição dos retornos diários, e os boxplots ajudam a identificar dispersão e valores extremos. Já o drawdown mede a queda em relação ao maior preço alcançado no recorte. PETR4, apesar do maior retorno, sofreu queda máxima de cerca de 39,10%. Em WEGE3, a queda chegou a 49,51%. Portanto, o resultado final não mostra sozinho o risco enfrentado durante o período.

## 3:50–4:15 — Dados e exportação

**Tela:** aba **Dados**. Mostre a tabela e clique em **Baixar dados filtrados**. Não é necessário abrir o arquivo baixado.

**Fala sugerida:**

> A aba Dados permite consultar os registros e exportar o recorte em CSV. Assim, os números apresentados nos gráficos podem ser conferidos e utilizados em outra análise. A interface foi organizada em abas para separar desempenho, risco, dados e explicação do método.

## 4:15–4:50 — Limitações e encerramento

**Tela:** aba **Sobre a análise**; ao final, mostre o README com os links.

**Fala sugerida:**

> A análise considera uma amostra de ações e um período histórico específico. Custos e inflação não foram descontados. O volume financeiro é estimado, e o Sharpe utiliza taxa livre de risco zero. O painel apoia a comparação histórica, mas não garante retornos futuros. O projeto reúne coleta, tratamento, SQL e visualização interativa. O código, o painel e o quadro de tarefas estão disponíveis pelos links do README.

## Pontos para lembrar durante o ensaio

| Assunto | Explicação correta |
|---|---|
| Fonte | Yahoo Finance via yfinance; não é uma coleta direta da B3 |
| Atualização | Coleta e importação preparadas anteriormente; abrir o app não executa o ETL |
| Banco | O Supabase armazena os dados; a view reúne fato e dimensão |
| Cache | Reaproveita a consulta por até dez minutos; a tela não atualiza automaticamente a cada dez minutos |
| Retorno médio | Média dos retornos acumulados das ações selecionadas |
| Volatilidade média | Média dos riscos individuais, não o risco de uma carteira |
| Drawdown | Queda desde o topo do recorte; difere do retorno desde o início |
| Sharpe | Média diária anualizada dividida pela volatilidade anual, com taxa livre de risco zero |
| Volume | Fechamento multiplicado pela quantidade negociada; é uma estimativa financeira |

## Como ensaiar

1. Leia as falas em voz alta, usando suas palavras e executando os cliques.
2. Cronometre do início ao fim. Se passar de cinco minutos, reduza as explicações dos arquivos e mantenha as demonstrações essenciais.
3. Confira se os valores citados correspondem ao recorte da tela. Restaure os filtros antes de cada ensaio.
4. Faça uma gravação curta de teste para conferir som e legibilidade.
5. Após o ensaio aprovado, conclua o card **Preparar roteiro do vídeo** e mova **Gravar e publicar o vídeo** para Em andamento.

Depois da publicação, registrar o link do vídeo no README e conferir seu acesso em uma janela anônima.
