CREATE OR REPLACE TABLE eleicoes2026_brazil.`03_gold`.dim_eleicao AS

WITH eleicao AS (
    SELECT DISTINCT
        cd_eleicao AS codigo_eleicao,
        ano_eleicao,
        cd_tipo_eleicao AS codigo_tipo_eleicao,
        nm_tipo_eleicao AS tipo_eleicao,
        ds_eleicao AS descricao_eleicao,
        dt_eleicao AS data_eleicao,
        nr_turno AS numero_turno
    FROM eleicoes2026_brazil.`02_silver`.votacao_nominal
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY codigo_eleicao, numero_turno
    ) AS sk_eleicao,
    *
FROM eleicao;
