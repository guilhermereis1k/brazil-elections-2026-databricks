
from pyspark.sql import functions as F

CAMINHO_BRONZE = (
    "/Volumes/eleicoes2026_brazil/01_bronze/arquivos/eleitorado/perfil_eleitorado_2026_BRASIL.csv"
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

    # Data e horário de geração
    "dt_geracao": "date",
    "hh_geracao": "string",

    # Informações da eleição
    "aa_eleicao": "int",

    # Localização
    "sg_uf": "string",
    "cd_municipio": "string",
    "nm_municipio": "string",
    "nr_zona": "int",

    # Gênero
    "cd_genero": "int",
    "ds_genero": "string",

    # Estado civil
    "cd_estado_civil": "int",
    "ds_estado_civil": "string",

    # Faixa etária
    "cd_faixa_etaria": "int",
    "ds_faixa_etaria": "string",

    # Escolaridade
    "cd_grau_escolaridade": "int",
    "ds_grau_escolaridade": "string",

    # Raça e cor
    "cd_raca_cor": "int",
    "ds_raca_cor": "string",

    # Identidade de gênero
    "cd_identidade_genero": "int",
    "ds_identidade_genero": "string",

    # Quilombolas
    "cd_quilombola": "int",
    "ds_quilombola": "string",

    # Intérprete de Libras
    "cd_interprete_libras": "int",
    "ds_interprete_libras": "string",

    # Quantidade de eleitores
    "qt_eleitores": "long",
    "qt_eleitores_biometria": "long",
    "qt_eleitores_deficiencia": "long",
    "qt_eleitores_nome_social": "long"
}

df_silver = df_bronze

for coluna, tipo in schema_silver.items():

    if coluna == "dt_geracao":
        df_silver = df_silver.withColumn(
            coluna,
            F.to_date(F.trim(F.col(coluna)), "dd/MM/yyyy")
        )

    else:
        df_silver = df_silver.withColumn(
            coluna,
            F.trim(F.col(coluna)).cast(tipo)
        )

display(df_silver.limit(20))

df_silver.printSchema()

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("eleicoes2026_brazil.02_silver.eleitorado")
)
