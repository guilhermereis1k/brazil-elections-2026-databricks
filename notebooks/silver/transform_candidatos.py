from pyspark.sql import functions as F

CAMINHO_BRONZE = (
    "/Volumes/eleicoes2026_brazil/01_bronze/arquivos/candidatos/consulta_cand_2026_BRASIL.csv"
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
    "dt_nascimento": "date",

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
    "sg_uf_nascimento": "string",

    # Cargo e candidato
    "cd_cargo": "int",
    "ds_cargo": "string",
    "sq_candidato": "string",
    "nr_candidato": "string",
    "nm_candidato": "string",
    "nm_urna_candidato": "string",
    "nm_social_candidato": "string",
    "nr_cpf_candidato": "string",
    "ds_email": "string",
    "nr_titulo_eleitoral_candidato": "string",

    # Situação da candidatura
    "cd_situacao_candidatura": "int",
    "ds_situacao_candidatura": "string",

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

    # Características do candidato
    "cd_genero": "int",
    "ds_genero": "string",
    "cd_grau_instrucao": "int",
    "ds_grau_instrucao": "string",
    "cd_estado_civil": "int",
    "ds_estado_civil": "string",
    "cd_cor_raca": "string",
    "ds_cor_raca": "string",
    "cd_ocupacao": "int",
    "ds_ocupacao": "string",

    # Resultado eleitoral
    "cd_sit_tot_turno": "int",
    "ds_sit_tot_turno": "string"
}

df_silver = df_bronze

for coluna, tipo in schema_silver.items():

    if coluna in ["dt_geracao", "dt_eleicao", "dt_nascimento"]:
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
    .saveAsTable("eleicoes2026_brazil.02_silver.candidatos")

)
