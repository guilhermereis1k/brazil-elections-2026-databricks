from pyspark.sql import functions as F

CAMINHO_BRONZE = (
    "/Volumes/eleicoes2026_brazil/01_bronze/arquivos/votacao/votacao_candidato_munzona_2026_BRASIL.csv"
)

df_bronze = (
    spark.read
    .format("csv")
    .option("header", True)
    .option("sep", ";")
    .option("encoding", "ISO-8859-1")
    .option("inferSchema", False)
    .load(CAMINHO_BRONZE)
)

print(f"Quantidade de colunas: {len(df_bronze.columns)}")

for coluna in df_bronze.columns:
    df_bronze = df_bronze.withColumnRenamed(
        coluna,
        coluna.strip().lower()
    )

schema_silver = {

    # Datas e horários
    "dt_geracao": "date",
    "hh_geracao": "string",
    "dt_eleicao": "date",

    # Informações da eleição
    "ano_eleicao": "int",
    "cd_tipo_eleicao": "int",
    "nm_tipo_eleicao": "string",
    "nr_turno": "int",
    "cd_eleicao": "int",
    "ds_eleicao": "string",
    "tp_abrangencia": "string",

    # Localização
    "sg_uf": "string",
    "sg_ue": "string",
    "nm_ue": "string",
    "cd_municipio": "string",
    "nm_municipio": "string",
    "nr_zona": "int",

    # Cargo e candidato
    "cd_cargo": "int",
    "ds_cargo": "string",
    "sq_candidato": "string",
    "nr_candidato": "string",
    "nm_candidato": "string",
    "nm_urna_candidato": "string",
    "nm_social_candidato": "string",

    # Situação da candidatura
    "cd_situacao_candidatura": "int",
    "ds_situacao_candidatura": "string",
    "cd_detalhe_situacao_cand": "int",
    "ds_detalhe_situacao_cand": "string",
    "cd_situacao_julgamento": "int",
    "ds_situacao_julgamento": "string",
    "cd_situacao_cassacao": "int",
    "ds_situacao_cassacao": "string",
    "cd_situacao_dconst_diploma": "int",
    "ds_situacao_dconst_diploma": "string",

    # Partido, federação e coligação
    "tp_agremiacao": "string",
    "nr_partido": "string",
    "sg_partido": "string",
    "nm_partido": "string",
    "nr_federacao": "string",
    "nm_federacao": "string",
    "sg_federacao": "string",
    "ds_composicao_federacao": "string",
    "sq_coligacao": "string",
    "nm_coligacao": "string",
    "ds_composicao_coligacao": "string",

    # Votação
    "st_voto_em_transito": "string",
    "qt_votos_nominais": "long",
    "nm_tipo_destinacao_votos": "string",
    "qt_votos_nominais_validos": "long",

    # Resultado
    "cd_sit_tot_turno": "int",
    "ds_sit_tot_turno": "string"
}

df_silver = df_bronze

for coluna, tipo in schema_silver.items():

    if coluna == "dt_geracao":
        df_silver = df_silver.withColumn(
            coluna,
            F.to_date(F.col(coluna), "dd/MM/yyyy")
        )

    elif coluna == "dt_eleicao":
        df_silver = df_silver.withColumn(
            coluna,
        F.to_date(F.col(coluna), "dd/MM/yyyy")
    )

    else:
        df_silver = df_silver.withColumn(
            coluna,
            F.trim(F.col(coluna)).cast(tipo)
        )


for coluna, tipo in schema_silver.items():

    if tipo == "string":
        df_silver = df_silver.withColumn(
            coluna,
            F.trim(F.col(coluna))
        )


display(df_silver.limit(20))

df_silver.printSchema()

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("eleicoes2026_brazil.02_silver.votacao_nominal")
)

