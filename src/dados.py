from pathlib import Path

import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
CAMINHO_CSV = RAIZ / "data" / "processed" / "cotacoes.csv"
NUMERICAS = ["abertura", "maxima", "minima", "fechamento", "fechamento_ajustado", "volume"]


def limpar_dados(df):
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    for coluna in NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    df[NUMERICAS] = df[NUMERICAS].replace([float("inf"), float("-inf")], float("nan"))
    df["ticker"] = df["ticker"].astype("string").str.strip().str.upper().replace("", pd.NA)
    df["setor"] = df["setor"].astype("string").str.strip().replace("", pd.NA)
    df = df.dropna(subset=["data", "ticker", "setor"] + NUMERICAS)
    df = df.drop_duplicates(subset=["ticker", "data"])
    df = df[df["data"].between("2021-01-01", "2023-12-31")]
    df = df[(df[NUMERICAS[:5]] > 0).all(axis=1) & (df["volume"] >= 0)]
    df = df[(df["maxima"] >= df[["abertura", "fechamento", "minima"]].max(axis=1))
            & (df["minima"] <= df[["abertura", "fechamento", "maxima"]].min(axis=1))]
    # Yahoo fornece quantidade negociada, não volume financeiro efetivo.
    df["volume_financeiro_estimado"] = df["fechamento"] * df["volume"]
    return df.sort_values(["ticker", "data"]).reset_index(drop=True)


@st.cache_data(ttl=600)
def consultar_banco():
    conexao = st.connection("postgresql", type="sql")
    df = conexao.query("SELECT * FROM cotacoes_b3 ORDER BY ticker, data", ttl=600)
    df = limpar_dados(df)
    if df.empty:
        raise ValueError("A consulta não retornou cotações válidas.")
    return df


@st.cache_data(ttl=600)
def ler_csv():
    return limpar_dados(pd.read_csv(CAMINHO_CSV, encoding="utf-8"))


def carregar_dados():
    try:
        return consultar_banco(), "Supabase"
    except Exception:
        # A contingência também permite executar sem credenciais de banco.
        return ler_csv(), "CSV local (contingência)"
