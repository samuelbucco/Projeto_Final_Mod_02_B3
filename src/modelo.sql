CREATE TABLE IF NOT EXISTS dim_ativos (
    ticker TEXT PRIMARY KEY,
    setor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fato_cotacoes (
    ticker TEXT REFERENCES dim_ativos(ticker),
    data DATE NOT NULL,
    abertura DOUBLE PRECISION NOT NULL,
    maxima DOUBLE PRECISION NOT NULL,
    minima DOUBLE PRECISION NOT NULL,
    fechamento DOUBLE PRECISION NOT NULL,
    fechamento_ajustado DOUBLE PRECISION NOT NULL,
    volume BIGINT NOT NULL,
    PRIMARY KEY (ticker, data)
);

CREATE OR REPLACE VIEW cotacoes_b3 AS
SELECT f.*, d.setor
FROM fato_cotacoes f JOIN dim_ativos d ON f.ticker = d.ticker;
