CREATE OR REPLACE TABLE eleicoes2026_brazil.`03_gold`.dim_candidaturas AS

WITH candidaturas AS (
    SELECT DISTINCT
        sq_candidato AS codigo_candidato,
        cd_eleicao AS codigo_eleicao,
        cd_cargo AS codigo_cargo,
        nr_candidato AS numero_candidato,
        nm_candidato AS nome_candidato,
        nm_urna_candidato AS nome_urna_candidato,
        nm_social_candidato AS nome_social_candidato,

        nr_partido AS numero_partido,
        sg_partido AS sigla_partido,
        nm_partido AS nome_partido,

        nr_federacao AS numero_federacao,
        nm_federacao AS nome_federacao,
        sg_federacao AS sigla_federacao,
        ds_composicao_federacao AS composicao_federacao,

        sq_coligacao AS codigo_coligacao,
        nm_coligacao AS nome_coligacao,
        ds_composicao_coligacao AS composicao_coligacao,

        cd_situacao_candidatura AS codigo_situacao_candidatura,
        ds_situacao_candidatura AS situacao_candidatura,

        cd_detalhe_situacao_cand AS codigo_detalhe_situacao,
        ds_detalhe_situacao_cand AS detalhe_situacao,

        cd_situacao_julgamento AS codigo_situacao_julgamento,
        ds_situacao_julgamento AS situacao_julgamento,

        cd_situacao_cassacao AS codigo_situacao_cassacao,
        ds_situacao_cassacao AS situacao_cassacao,

        cd_situacao_dconst_diploma AS codigo_situacao_diploma,
        ds_situacao_dconst_diploma AS situacao_diploma,

        cd_sit_tot_turno AS codigo_situacao_totalizacao,
        ds_sit_tot_turno AS situacao_totalizacao

    FROM eleicoes2026_brazil.`02_silver`.votacao_nominal
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY codigo_candidato, codigo_eleicao, codigo_cargo
    ) AS sk_candidatura,
    *
FROM candidaturas;
