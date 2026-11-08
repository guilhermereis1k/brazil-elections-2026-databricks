CREATE OR REPLACE TABLE eleicoes2026_brazil.`03_gold`.dim_localidades AS

WITH localidades AS (

    SELECT
        sg_uf AS sigla_uf,
        cd_municipio AS codigo_municipio,
        nm_municipio AS nome_municipio,
        nr_zona AS numero_zona
    FROM eleicoes2026_brazil.`02_silver`.votacao_nominal

    UNION

    SELECT
        sg_uf AS sigla_uf,
        cd_municipio AS codigo_municipio,
        nm_municipio AS nome_municipio,
        nr_zona AS numero_zona
    FROM eleicoes2026_brazil.`02_silver`.eleitorado

)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY sigla_uf, codigo_municipio, numero_zona
    ) AS sk_localidade,
    *
FROM localidades;
