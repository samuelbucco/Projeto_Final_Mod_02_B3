# Verificação da versão inicial

Verificações realizadas em 17/10/2026, com Python 3.14, Pandas 3.0.3 e Streamlit 1.64.0.

## Base e reprodução

- ETL executado com dados reais do Yahoo Finance.
- Tratamento refeito com `python -m src.etl --local`, sem novo acesso à rede.
- EDA executada com `python -m notebooks.analise_exploratoria`.
- 5.960 registros, oito ações, 745 pregões por ação, de 04/01/2021 a 28/12/2023.
- Sem campos brutos essenciais nulos nem duplicatas por ticker/data na base tratada.
- Todas as datas da coleta são comuns aos oito ativos.

## Cálculos

Conferência controlada com preços 100, 120 e 90: base 100 igual a 100/120/90, retornos de 20% e -25%, retorno acumulado de -10% e drawdown máximo de -25%. A volatilidade foi comparada ao desvio padrão amostral desses retornos multiplicado por √252.

As médias móveis foram verificadas em uma sequência de 50 observações, incluindo a ausência esperada de resultados nas primeiras 20 e 49 linhas. A limpeza foi exercitada com duplicatas, datas inválidas, preços zero/infinito, volume negativo, preços OHLC incoerentes e ticker vazio.

## Aplicação

- quatro KPIs e cinco gráficos;
- seleção vazia de ativos e de setores;
- opções de ativos limitadas pelo setor;
- seleção de apenas uma data e de fim de semana sem pregão;
- restauração dos filtros;
- visualização das oito ações;
- troca da ação para detalhar as médias móveis.

O carregamento também foi exercitado simulando falha da função de consulta e um retorno SQL válido, confirmando a escolha entre banco e CSV.

Após a configuração das credenciais locais, a conexão real ao Supabase foi validada em 17/10/2026. As consultas retornaram oito registros em `dim_ativos`, 5.960 em `fato_cotacoes` e 5.960 na view `cotacoes_b3`, de 04/01/2021 a 28/12/2023.

## Versão publicada

Em 18/10/2026, o estudante confirmou o funcionamento de https://samuel-bucco-projeto-final-b3.streamlit.app/: fonte Supabase, filtros, restauração e download do CSV. Também forneceu sete capturas de KPIs, cinco gráficos e resumo de retorno e risco, salvas em `docs/imagens` e incluídas no README. O gráfico de drawdown apresenta os títulos curtos “Queda (%)” sem a sobreposição anterior. A validação funcional em produção foi informada pelo estudante; as capturas foram examinadas pelo assistente.
