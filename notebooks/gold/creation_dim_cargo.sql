CREATE OR REPLACE TABLE eleicoes2026_brazil.`03_gold`.dim_cargo AS

WITH cargos AS (
    SELECT DISTINCT
        cd_cargo AS codigo_cargo,
        ds_cargo AS descricao_cargo
    FROM eleicoes2026_brazil.`02_silver`.candidatos
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY codigo_cargo
    ) AS sk_cargo,
    *
FROM cargos;
