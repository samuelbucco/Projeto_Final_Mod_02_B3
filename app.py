"""Dashboard do módulo 02: componentes nativos do Streamlit e gráficos Plotly Express."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dados import carregar_dados
from src.indicadores import adicionar_medias_moveis, calcular_indicadores

st.set_page_config(page_title="Ações B3 | 2021 a 2023", page_icon="📈", layout="wide")
st.title("Ações B3: retorno e risco")
st.write("Como as ações selecionadas se comportaram entre 2021 e 2023?")

try:
    df, origem = carregar_dados()
except (OSError, ValueError, KeyError):
    st.error("A base não está disponível. Execute: python -m src.etl")
    st.stop()
if df.empty:
    st.warning("A base não contém cotações válidas.")
    st.stop()

# As médias usam o histórico disponível antes de aplicar o período da tela.
df = adicionar_medias_moveis(df)
setores = sorted(df["setor"].unique())
inicio, fim = df["data"].min().date(), df["data"].max().date()
ativos_padrao = ["PETR4", "VALE3", "ITUB4", "WEGE3"]


def resetar_filtros():
    st.session_state["setores"] = setores
    st.session_state["ativos"] = ativos_padrao
    st.session_state["periodo"] = (inicio, fim)


if "setores" not in st.session_state:
    resetar_filtros()

with st.sidebar:
    st.header("Filtros")
    st.caption(f"Fonte em uso: {origem}")
    st.multiselect("Setores", setores, key="setores")
    disponiveis = sorted(df.loc[df["setor"].isin(st.session_state["setores"]), "ticker"].unique())
    # O filtro de setor limita as opções do filtro de ações.
    st.session_state["ativos"] = [t for t in st.session_state["ativos"] if t in disponiveis]
    ativos = st.multiselect("Ações", disponiveis, key="ativos")
    periodo = st.date_input("Período", min_value=inicio, max_value=fim, key="periodo")
    st.button("Restaurar filtros", on_click=resetar_filtros)

if not ativos:
    st.info("Selecione ao menos uma ação na barra lateral.")
    st.stop()
if len(periodo) != 2:
    st.info("Selecione a data inicial e a data final.")
    st.stop()

filtrado = df[df["ticker"].isin(ativos) & df["data"].between(pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1]))]
# Para comparar retornos, todos os ativos usam os mesmos pregões disponíveis.
contagens = filtrado.groupby("data")["ticker"].nunique()
datas_comuns = contagens[contagens == len(ativos)].index
filtrado = filtrado[filtrado["data"].isin(datas_comuns)]
if len(datas_comuns) < 3:
    st.info("Escolha um período com pelo menos três pregões em comum entre as ações.")
    st.stop()

serie, resumo = calcular_indicadores(filtrado)
_, anterior = calcular_indicadores(filtrado[filtrado["data"] < filtrado["data"].max()])
melhor = resumo.loc[resumo["retorno_acumulado"].idxmax()]
pior = resumo.loc[resumo["retorno_acumulado"].idxmin()]
media = resumo["retorno_acumulado"].mean()
volatilidade = resumo["volatilidade_anual"].mean()
st.caption(f"{len(ativos)} ações · {len(datas_comuns)} pregões · "
           f"{filtrado['data'].min():%d/%m/%Y} a {filtrado['data'].max():%d/%m/%Y}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Retorno médio dos ativos", f"{media:.2f}%",
            f"{media - anterior['retorno_acumulado'].mean():+.2f} p.p. vs. pregão anterior")
col2.metric("Melhor desempenho", melhor["ticker"],
            f"{melhor['retorno_acumulado'] - media:+.2f} p.p. vs. média")
col3.metric("Menor desempenho", pior["ticker"],
            f"{pior['retorno_acumulado'] - media:+.2f} p.p. vs. média")
col4.metric("Volatilidade média anual", f"{volatilidade:.2f}%",
            f"{volatilidade - anterior['volatilidade_anual'].mean():+.2f} p.p. vs. pregão anterior",
            delta_color="inverse")
st.info(f"No recorte, {melhor['ticker']} teve o maior retorno ({melhor['retorno_acumulado']:.2f}%) "
        f"e {pior['ticker']} o menor ({pior['retorno_acumulado']:.2f}%). "
        "Compare também volatilidade e quedas antes de avaliar o desempenho.")

aba1, aba2, aba3, aba4 = st.tabs(["Desempenho", "Risco", "Dados", "Sobre a análise"])
rotulos = {"data": "Data", "ticker": "Ação", "base_100": "Índice (base 100)",
           "retorno_diario": "Retorno diário (%)", "drawdown": "Queda desde o topo (%)",
           "retorno_acumulado": "Retorno acumulado (%)", "volatilidade_anual": "Volatilidade (% a.a.)",
           "volume_medio_estimado": "Volume financeiro médio estimado (R$)", "setor": "Setor"}

with aba1:
    st.subheader("1. Evolução comparativa em base 100")
    grafico = px.line(serie, x="data", y="base_100", color="ticker", labels=rotulos)
    grafico.add_hline(y=100, line_dash="dash")
    st.plotly_chart(grafico, width="stretch")
    st.caption("100 é o fechamento ajustado do primeiro pregão do recorte; 120 representa alta de 20%.")

    st.subheader("2. Preço ajustado e médias móveis")
    ativo_detalhe = st.selectbox("Ação para detalhar", ativos)
    detalhe = serie[serie["ticker"] == ativo_detalhe]
    longo = detalhe.melt(id_vars="data", value_vars=["fechamento_ajustado", "sma_21", "sma_50"],
                         var_name="serie", value_name="preco")
    grafico = px.line(longo, x="data", y="preco", color="serie",
                      labels={"data": "Data", "preco": "Preço ajustado (R$)", "serie": "Série"})
    st.plotly_chart(grafico, width="stretch")
    st.caption("SMA 21 e 50: médias de 21 e 50 pregões. O início de 2021 não possui histórico suficiente.")

with aba2:
    st.subheader("3. Risco e retorno")
    grafico = px.scatter(resumo, x="volatilidade_anual", y="retorno_acumulado", color="setor",
                         size="volume_medio_estimado", hover_name="ticker", text="ticker", labels=rotulos)
    st.plotly_chart(grafico, width="stretch")
    st.caption("Bolhas: fechamento × quantidade negociada, uma aproximação do volume financeiro.")

    st.subheader("4. Distribuição dos retornos diários")
    grafico = px.histogram(serie.dropna(subset=["retorno_diario"]), x="retorno_diario", color="ticker",
                           marginal="box", barmode="overlay", opacity=0.5, nbins=50, labels=rotulos)
    grafico.update_layout(yaxis_title="Frequência (pregões)")
    st.plotly_chart(grafico, width="stretch")

    st.subheader("5. Queda em relação ao topo do período")
    grafico = px.area(serie, x="data", y="drawdown", facet_row="ticker", labels=rotulos,
                      height=max(300, 150 * len(ativos)))
    st.plotly_chart(grafico, width="stretch")
    resiliente = resumo.loc[resumo["drawdown_maximo"].idxmax()]
    st.write(f"A menor queda máxima foi de {resiliente['drawdown_maximo']:.2f}% ({resiliente['ticker']}).")
    st.caption("O topo reinicia no primeiro pregão do filtro. Não considera picos anteriores ao recorte.")
    st.subheader("Resumo de retorno e risco")
    st.dataframe(resumo, hide_index=True, width="stretch", column_config={
        "retorno_acumulado": st.column_config.NumberColumn("Retorno (%)", format="%.2f"),
        "volatilidade_anual": st.column_config.NumberColumn("Volatilidade (% a.a.)", format="%.2f"),
        "sharpe_rf_zero": st.column_config.NumberColumn("Sharpe (rf = 0)", format="%.2f"),
        "drawdown_maximo": st.column_config.NumberColumn("Queda máxima (%)", format="%.2f"),
        "volume_medio_estimado": st.column_config.NumberColumn("Volume médio estimado (R$)", format="%.2f"),
    })
    sharpes_validos = resumo.dropna(subset=["sharpe_rf_zero"])
    if not sharpes_validos.empty:
        destaque = sharpes_validos.loc[sharpes_validos["sharpe_rf_zero"].idxmax()]
        st.write(f"Maior Sharpe empírico no recorte: {destaque['ticker']} ({destaque['sharpe_rf_zero']:.2f}).")
    st.caption("Sharpe empírico: média diária × 252 / volatilidade anual, com taxa livre de risco igual a zero. "
               "É uma simplificação didática, sem descontar a Selic.")

with aba3:
    st.subheader("Cotações e indicadores do recorte")
    st.dataframe(serie, hide_index=True, width="stretch")
    st.download_button("Baixar dados filtrados", serie.to_csv(index=False).encode("utf-8-sig"),
                       file_name="cotacoes_b3_filtradas.csv", mime="text/csv")

with aba4:
    st.write("Dados do Yahoo Finance obtidos por yfinance para oito ações negociadas na B3, de 2021 a 2023. "
             "A base é histórica: não representa cotações atuais.")
    st.write("Os cálculos usam fechamento ajustado pelo provedor. A volatilidade considera o desvio padrão "
             "amostral dos retornos diários e 252 pregões por ano. O retorno médio atribui o mesmo peso inicial "
             "a cada ação; a volatilidade média é a média dos riscos individuais, não o risco da carteira.")
    st.write("O período filtrado reinicia base 100, retornos e drawdown. As médias móveis usam os pregões "
             "disponíveis desde janeiro de 2021. Datas sem cotação em alguma ação selecionada são excluídas "
             "da comparação. Setores são agrupamentos didáticos.")
    st.write("A amostra não representa toda a bolsa. Custos, impostos e inflação não foram descontados. "
             "Os resultados descrevem o passado e não estabelecem causas nem garantem retornos futuros.")
