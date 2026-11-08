CREATE OR REPLACE TABLE eleicoes2026_brazil.`03_gold`.fact_votacao AS

WITH fato_votacao AS (
    SELECT
        e.sk_eleicao,
        ca.sk_candidatura,
        c.sk_cargo,
        l.sk_localidade,
        v.qt_votos_nominais,
        v.qt_votos_nominais_validos

    FROM eleicoes2026_brazil.`02_silver`.votacao_nominal v

    INNER JOIN eleicoes2026_brazil.`03_gold`.dim_eleicao e
        ON v.cd_eleicao = e.codigo_eleicao
        AND v.nr_turno = e.numero_turno

    INNER JOIN eleicoes2026_brazil.`03_gold`.dim_cargo c
        ON v.cd_cargo = c.codigo_cargo

    INNER JOIN eleicoes2026_brazil.`03_gold`.dim_localidades l
        ON v.sg_uf = l.sigla_uf
        AND v.cd_municipio = l.codigo_municipio
        AND v.nr_zona = l.numero_zona

    INNER JOIN eleicoes2026_brazil.`03_gold`.dim_candidaturas ca
        ON v.sq_candidato = ca.codigo_candidato
        AND v.cd_eleicao = ca.codigo_eleicao
        AND v.cd_cargo = ca.codigo_cargo
)

SELECT *
FROM fato_votacao;
