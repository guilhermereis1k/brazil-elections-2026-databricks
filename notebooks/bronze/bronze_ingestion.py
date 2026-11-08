
import os
import requests
import zipfile
import shutil
import hashlib
from pathlib import Path
from urllib.parse import urlparse

VOLUME = "/Volumes/eleicoes2026_brazil/01_bronze/arquivos"

TEMP = "/tmp/eleicoes2026"
os.makedirs(TEMP, exist_ok=True)

FONTES = {
    "candidatos": [
        "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip",
    ],

    "comparecimento_abstencao": [
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao/perfil_comparecimento_abstencao_2026.zip",
    ],

    "eleitorado": [
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_2026.zip",
    ],

    "votacao": [
        "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2026.zip",
    ]
}

def baixar_zip(url, destino):

    with requests.get(
        url,
        stream=True,
        timeout=(30, 300)
    ) as resposta:

        resposta.raise_for_status()

        with open(destino, "wb") as arquivo:

            for chunk in resposta.iter_content(
                chunk_size=8 * 1024 * 1024
            ):
                if chunk:
                    arquivo.write(chunk)

    return destino


def processar_zip(categoria, url):

    identificador = hashlib.sha256(
        url.encode()
    ).hexdigest()

    nome = os.path.basename(
        urlparse(url).path
    ) or f"{identificador}.zip"

    if not nome.lower().endswith(".zip"):
        nome = f"{identificador}.zip"

    destino = f"{VOLUME}/{categoria}"

    os.makedirs(destino, exist_ok=True)

    marcador = f"{destino}/._{identificador}.done"

    if os.path.exists(marcador):
        print(f"Já processado: {nome}")
        return

    zip_path = f"{TEMP}/{identificador}.zip"
    extract_path = f"{TEMP}/{identificador}"

    print(f"\nIniciando: {nome}")

    try:

        print("Baixando ZIP")
        baixar_zip(url, zip_path)

        print("Extraindo CSV")

        os.makedirs(extract_path, exist_ok=True)

        quantidade = 0

        with zipfile.ZipFile(zip_path, "r") as arquivo_zip:

            for membro in arquivo_zip.infolist():

                caminho = Path(membro.filename)

                if caminho.is_absolute() or ".." in caminho.parts:
                    raise ValueError(
                        f"Caminho inválido: {membro.filename}"
                    )

            for membro in arquivo_zip.infolist():

                if membro.is_dir():
                    continue

                if not membro.filename.lower().endswith(".csv"):
                    continue

                caminho = Path(membro.filename)

                arquivo_destino = os.path.join(
                    extract_path,
                    *caminho.parts
                )

                os.makedirs(
                    os.path.dirname(arquivo_destino),
                    exist_ok=True
                )

                with arquivo_zip.open(membro) as origem:
                    with open(arquivo_destino, "wb") as saida:
                        shutil.copyfileobj(origem, saida)

        print("Gravando no Volume...")

        for raiz, _, arquivos in os.walk(extract_path):

            for arquivo in arquivos:

                origem = os.path.join(raiz, arquivo)

                relativo = os.path.relpath(
                    origem,
                    extract_path
                )

                destino_csv = os.path.join(
                    destino,
                    relativo
                )

                os.makedirs(
                    os.path.dirname(destino_csv),
                    exist_ok=True
                )

                shutil.copy2(
                    origem,
                    destino_csv
                )

                quantidade += 1

        with open(
            f"{TEMP}/{identificador}.done",
            "w"
        ) as arquivo:
            arquivo.write("OK")

        dbutils.fs.cp(
            f"file:/tmp/eleicoes2026/{identificador}.done",
            marcador
        )

        print(f"Concluído: {nome}")
        print(f"CSV extraídos: {quantidade}")

    except Exception as erro:

        print(f"ERRO: {nome}")
        print(str(erro))

        raise

    finally:

        if os.path.exists(zip_path):
            os.remove(zip_path)

        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)

        marcador_temp = f"{TEMP}/{identificador}.done"

        if os.path.exists(marcador_temp):
            os.remove(marcador_temp)


for categoria, urls in FONTES.items():

    print("\n" + "=" * 50)
    print(f"CATEGORIA: {categoria.upper()}")
    print("=" * 50)

    for url in urls:

        if not url or url.startswith("LINK_"):
            continue

        try:
            processar_zip(categoria, url)

        except Exception as erro:
            print(f"Falha no arquivo: {erro}")
