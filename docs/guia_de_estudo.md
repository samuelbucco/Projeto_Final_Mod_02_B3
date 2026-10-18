# Guia para entender e apresentar o projeto

A ideia é conseguir explicar o que cada etapa faz, alterar um filtro ou gráfico e reproduzir os principais números. Este guia não substitui a revisão do código nem a interpretação pessoal dos resultados.

## Caminho de leitura

1. `src/etl.py`: de onde vêm os dados e como são salvos.
2. `src/dados.py`: limpeza, cache e leitura com contingência.
3. `src/indicadores.py`: fórmulas em séries do Pandas.
4. `app.py`: como os controles da tela filtram os dados e alimentam os gráficos.

## O que acontece ao abrir a aplicação

O Streamlit executa `app.py` de cima para baixo. O app busca os dados, monta os filtros, aplica a seleção e calcula os indicadores. Depois desenha os KPIs e as abas. Quando você altera um widget, o script executa novamente, reaproveitando os dados em cache e os filtros armazenados no estado da sessão.

## Conceitos que precisam estar claros

| Recurso | Como explicar com suas palavras |
|---|---|
| DataFrame | Uma tabela em memória, com colunas de tipos definidos |
| `pd.to_datetime` e `pd.to_numeric` | Convertem texto em datas e números para permitir filtros e cálculos |
| `dropna` | Retira registros sem campos essenciais; não preenche preços inventados |
| `drop_duplicates` | Mantém uma observação por ticker e data |
| `@st.cache_data(ttl=600)` | Reaproveita o resultado por até dez minutos |
| `try/except` | Tenta o banco e usa o CSV se ocorrer uma falha |
| `st.session_state` | Guarda os filtros entre execuções da mesma sessão |
| Callback de reset | Atualiza o estado antes de redesenhar os widgets |
| Filtros cruzados | O setor escolhido limita as ações disponíveis |
| `groupby` | Aplica cálculos separadamente em cada ativo |
| `pct_change` | Compara cada preço com o anterior |
| `rolling` | Calcula uma estatística sobre uma janela de pregões |
| `cummax` | Guarda o maior preço encontrado até cada data |
| `st.tabs` | Separa temas na mesma página; os blocos de Python executam mesmo nas abas não selecionadas |

## Fórmulas com um exemplo pequeno

Imagine três fechamentos ajustados: **100, 120, 90**.

- Retornos diários: sem valor no primeiro dia, **20%**, **-25%**.
- Base 100: **100, 120, 90**.
- Retorno acumulado: `90 / 100 - 1 = -10%`.
- Topos acumulados: **100, 120, 120**.
- Drawdown: **0%, 0%, -25%**. Portanto, a queda máxima é **-25%**.

Volatilidade é o desvio padrão dos retornos: indica dispersão, não a direção do preço. A anualização multiplica o desvio padrão diário por √252. O Sharpe didático divide a média diária anualizada pela volatilidade anual, assumindo taxa livre de risco zero. Não é um Sharpe descontando a Selic.

O volume do Yahoo é uma quantidade, não um valor em reais. Multiplicar quantidade por fechamento aproxima o volume financeiro, mas não recupera o preço de cada negócio do dia.

## Exercícios para fazer antes de gravar

1. Selecione somente ITUB4 e explique por que o melhor e o menor desempenho são a mesma ação.
2. Filtre Energia elétrica e veja como as opções de ações mudam. Depois restaure os filtros.
3. Troque o início do período e explique por que a base 100 e o drawdown mudam.
4. Compare PETR4 e EGIE3: qual teve maior retorno, qual oscilou menos e qual sofreu menor queda?
5. Baixe o CSV e confira manualmente o retorno acumulado de uma ação com o primeiro e o último preço ajustado.
6. Altere o título de um gráfico no código e execute novamente. Identifique o comando que faz a mudança.
7. Explique por que volatilidade média não mede o risco de uma carteira diversificada.

## Sugestão de demonstração de 3 a 5 minutos

- **0:00 a 0:45:** apresente o problema, o período e a amostra.
- **0:45 a 1:30:** mostre fonte, CSV bruto, limpeza e saída tratada.
- **1:30 a 3:45:** apresente filtros, KPIs, base 100, médias, risco, drawdown e exportação. Restaure os filtros ao final.
- **3:45 a 5:00:** comente um resultado que você conferiu, explique as limitações e indique os links.

Use suas palavras e os resultados que você verificou. O vídeo da entrega deve mostrar o app publicado, não somente a execução local.
