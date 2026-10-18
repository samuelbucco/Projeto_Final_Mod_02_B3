"""Análise preliminar simples. Na raiz, execute: python -m notebooks.analise_exploratoria."""

import pandas as pd

from src.dados import CAMINHO_CSV, RAIZ
from src.indicadores import calcular_indicadores

df = pd.read_csv(CAMINHO_CSV, parse_dates=["data"])
serie, resumo = calcular_indicadores(df)
print("Tipos das colunas:\n", df.dtypes)
print("\nValores nulos:\n", df.isna().sum())
print("\nDuplicatas por data e ativo:", df.duplicated(["data", "ticker"]).sum())
print("\nResumo por ação:\n", resumo.round(2).to_string(index=False))
print("\nEstatísticas dos retornos diários (%):\n",
      serie.groupby("ticker")["retorno_diario"].agg(["mean", "std", "min", "max", "skew"]).round(3))
resumo.to_csv(RAIZ / "notebooks" / "resumo_ativos.csv", index=False)
