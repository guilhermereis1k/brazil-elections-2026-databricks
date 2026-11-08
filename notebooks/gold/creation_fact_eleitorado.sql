CREATE OR REPLACE TABLE eleicoes2026_brazil.`03_gold`.fact_eleitorado AS

WITH fato_eleitorado AS (
    SELECT
        e.aa_eleicao AS ano_eleicao,
        l.sk_localidade,

        e.cd_genero AS codigo_genero,
        e.ds_genero AS genero,

        e.cd_estado_civil AS codigo_estado_civil,
        e.ds_estado_civil AS estado_civil,

        e.cd_faixa_etaria AS codigo_faixa_etaria,
        e.ds_faixa_etaria AS faixa_etaria,

        e.cd_grau_escolaridade AS codigo_escolaridade,
        e.ds_grau_escolaridade AS grau_escolaridade,

        e.cd_raca_cor AS codigo_raca_cor,
        e.ds_raca_cor AS raca_cor,

        e.cd_identidade_genero AS codigo_identidade_genero,
        e.ds_identidade_genero AS identidade_genero,

        e.cd_quilombola AS codigo_quilombola,
        e.ds_quilombola AS quilombola,

        e.cd_interprete_libras AS codigo_interprete_libras,
        e.ds_interprete_libras AS interprete_libras,

        e.qt_eleitores AS quantidade_eleitores,
        e.qt_eleitores_biometria AS quantidade_eleitores_biometria,
        e.qt_eleitores_deficiencia AS quantidade_eleitores_deficiencia,
        e.qt_eleitores_nome_social AS quantidade_eleitores_nome_social

    FROM eleicoes2026_brazil.`02_silver`.eleitorado e

    LEFT JOIN eleicoes2026_brazil.`03_gold`.dim_localidades l
        ON e.sg_uf = l.sigla_uf
        AND e.cd_municipio = l.codigo_municipio
        AND e.nr_zona = l.numero_zona
)

SELECT *
FROM fato_eleitorado;
