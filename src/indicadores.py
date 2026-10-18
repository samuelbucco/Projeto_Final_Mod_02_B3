import pandas as pd


def calcular_indicadores(df):
    partes = []
    resumo = []
    for ticker, dados in df.groupby("ticker"):
        dados = dados.sort_values("data").copy()
        preco = dados["fechamento_ajustado"]
        retorno = preco.pct_change(fill_method=None)
        dados["retorno_diario"] = retorno * 100
        dados["base_100"] = preco / preco.iloc[0] * 100
        dados["drawdown"] = (preco / preco.cummax() - 1) * 100
        volatilidade = retorno.std() * (252 ** 0.5)
        sharpe = retorno.mean() * 252 / volatilidade if volatilidade > 0 else float("nan")
        resumo.append({
            "ticker": ticker,
            "setor": dados["setor"].iloc[0],
            "retorno_acumulado": (preco.iloc[-1] / preco.iloc[0] - 1) * 100,
            "volatilidade_anual": volatilidade * 100,
            "sharpe_rf_zero": sharpe,
            "drawdown_maximo": dados["drawdown"].min(),
            "volume_medio_estimado": dados["volume_financeiro_estimado"].mean(),
        })
        partes.append(dados)
    return pd.concat(partes, ignore_index=True), pd.DataFrame(resumo)


def adicionar_medias_moveis(df):
    partes = []
    for _, dados in df.groupby("ticker"):
        dados = dados.sort_values("data").copy()
        dados["sma_21"] = dados["fechamento_ajustado"].rolling(21).mean()
        dados["sma_50"] = dados["fechamento_ajustado"].rolling(50).mean()
        partes.append(dados)
    return pd.concat(partes, ignore_index=True)
