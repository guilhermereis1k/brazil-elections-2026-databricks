from pyspark.sql import functions as F

CAMINHO_BRONZE = (
    "/Volumes/eleicoes2026_brazil/01_bronze/arquivos/comparecimento_abstencao/perfil_comparecimento_abstencao_2026_BRASIL.csv"
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

    # Data e horário
    "dt_geracao": "date",
    "hh_geracao": "string",

    # Informações da eleição
    "ano_eleicao": "int",
    "nr_turno": "int",

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
    "cd_grau_instrucao": "int",
    "ds_grau_instrucao": "string",

    # Raça e cor
    "cd_cor_raca": "int",
    "ds_cor_raca": "string",

    # Quilombolas
    "cd_quilombola": "int",
    "ds_quilombola": "string",

    # Intérprete de Libras
    "cd_interprete_libras": "int",
    "ds_interprete_libras": "string",

    # Identidade de gênero
    "cd_identidade_genero": "int",
    "ds_identidade_genero": "string",

    # Idioma indígena
    "cd_idioma_indigena": "int",
    "ds_idioma_indigena": "string",

    # Grupo indígena
    "cd_grupo_indigena": "int",
    "ds_grupo_indigena": "string",

    # Idioma quilombola
    "cd_idioma_quilombola": "int",
    "ds_idioma_quilombola": "string",

    # Quantidade de eleitores
    "qt_aptos": "long",
    "qt_comparecimento": "long",
    "qt_abstencao": "long",

    # Comparecimento e abstenção por deficiência
    "qt_comparecimento_deficiencia": "long",
    "qt_abstencao_deficiencia": "long",

    # Voto em trânsito
    "qt_comparecimento_tte": "long",
    "qt_abstencao_tte": "long",

    # Voto facultativo
    "qt_comparec_facultativo": "long",
    "qt_abst_facultativo": "long",

    # Voto obrigatório
    "qt_comparec_obrigatorio": "long",
    "qt_abst_obrigatorio": "long",

    # Deficiência - voto facultativo
    "qt_comparec_defic_facultativo": "long",
    "qt_abst_defic_facultativo": "long",

    # Deficiência - voto obrigatório
    "qt_comparec_defic_obrigatorio": "long",
    "qt_abst_defic_obrigatorio": "long"
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
    .saveAsTable(
        "eleicoes2026_brazil.02_silver.comparecimento_abstencao"
    )
)
