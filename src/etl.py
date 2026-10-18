import argparse
import json
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from src.dados import RAIZ, CAMINHO_CSV, limpar_dados

# Agrupamento econômico didático, fixo e documentado; não é classificação oficial B3.
ATIVOS = {
    "WEGE3": "Indústria",
    "VALE3": "Materiais básicos", "GGBR4": "Materiais básicos",
    "PETR4": "Petróleo e gás", "EGIE3": "Energia elétrica",
    "ITUB4": "Financeiro",
    "ABEV3": "Bebidas", "RENT3": "Locação de veículos",
}


def executar(usar_local=False):
    pasta_raw = RAIZ / "data" / "raw"
    pasta_raw.mkdir(parents=True, exist_ok=True)
    if not usar_local:
        # O cache da biblioteca fica dentro do projeto, fora dos arquivos versionados.
        yf.set_tz_cache_location(str(RAIZ / "data" / "cache"))
        base = yf.download(
            [ticker + ".SA" for ticker in ATIVOS], start="2021-01-01", end="2024-01-01",
            auto_adjust=False, group_by="ticker", threads=False, progress=False, timeout=30,
        )
        if base is None or base.empty:
            raise ValueError("Não foi possível obter os dados. A base anterior foi preservada.")
        partes = []
        for ticker, setor in ATIVOS.items():
            dados = base[ticker + ".SA"].dropna(how="all").reset_index()
            if dados.empty:
                raise ValueError(f"Sem dados para {ticker}. A base anterior foi preservada.")
            dados = dados.rename(columns={
                "Date": "data", "Open": "abertura", "High": "maxima", "Low": "minima",
                "Close": "fechamento", "Adj Close": "fechamento_ajustado", "Volume": "volume",
            })
            dados["ticker"] = ticker
            dados["setor"] = setor
            partes.append(dados)
        bruto = pd.concat(partes, ignore_index=True)
    else:
        bruto = pd.read_csv(pasta_raw / "cotacoes_yahoo.csv", encoding="utf-8")

    tratado = limpar_dados(bruto)
    if set(tratado["ticker"]) != set(ATIVOS):
        raise ValueError("A limpeza deixou ativos sem dados; verifique a extração.")
    # Todos os ativos precisam cobrir os três anos solicitados.
    cobertura = tratado.groupby("ticker")["data"].agg(["min", "max"])
    if (cobertura["min"] > pd.Timestamp("2021-01-10")).any() or (cobertura["max"] < pd.Timestamp("2023-12-20")).any():
        raise ValueError("Há ativos com cobertura incompleta de 2021 a 2023.")
    CAMINHO_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not usar_local:
        bruto.to_csv(pasta_raw / "cotacoes_yahoo.csv", index=False, encoding="utf-8")
        (pasta_raw / "origem.json").write_text(json.dumps({
            "fonte": "Yahoo Finance, via yfinance (não é extração direta da B3)",
            "extraido_em_utc": datetime.now(timezone.utc).isoformat(),
            "inicio": "2021-01-01", "fim_exclusivo": "2024-01-01",
            "auto_adjust": False, "yfinance": yf.__version__, "ativos": list(ATIVOS),
        }, indent=2, ensure_ascii=False), encoding="utf-8")
    tratado.to_csv(CAMINHO_CSV, index=False, encoding="utf-8")
    tratado[["ticker", "setor"]].drop_duplicates().to_csv(
        CAMINHO_CSV.parent / "dim_ativos.csv", index=False, encoding="utf-8")
    fato = tratado.drop(columns=["setor", "volume_financeiro_estimado"]).copy()
    fato["volume"] = fato["volume"].astype("int64")
    fato.to_csv(CAMINHO_CSV.parent / "fato_cotacoes.csv", index=False, encoding="utf-8")
    print(f"Registros brutos: {len(bruto)} | Tratados: {len(tratado)} | Removidos: {len(bruto) - len(tratado)}")
    print(tratado.groupby("ticker")["data"].agg(["min", "max", "count"]).to_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="store_true", help="Refaz o tratamento do CSV bruto, sem rede.")
    executar(parser.parse_args().local)
