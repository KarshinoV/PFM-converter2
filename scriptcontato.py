import re
import os
import pandas as pd
from datetime import datetime

def limpar_telefone(numero):
    if not numero:
        return ""

    # Remove tudo que não for número
    numero = re.sub(r"\D", "", numero)

    # Regras
    if numero.startswith("015"):
        numero = numero[3:]

    if numero.startswith("55"):
        numero = numero[2:]

    if numero.startswith("0"):
        numero = numero[1:]

    return numero


def obter_nome(caminho_origin):
    # Gera timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Monta nome final
    pasta = os.path.dirname(caminho_origin)
    nome_final = f"contatos_{timestamp}.xlsx"
    caminho_xlsx = os.path.join(pasta, nome_final)
    return caminho_xlsx



def vcf_para_xlsx(caminho_vcf):
    nomes = []
    telefones = []

    with open(caminho_vcf, "r", encoding="utf-8", errors="ignore") as f:
        nome_atual = None
        tel_atual = None

        for linha in f:
            linha = linha.strip()

            if linha.startswith("FN:"):
                nome_atual = linha.replace("FN:", "").strip()

            if linha.startswith("TEL"):
                partes = linha.split(":")
                if len(partes) == 2:
                    tel_atual = limpar_telefone(partes[1])

                if nome_atual is not None and tel_atual is not None:
                    nomes.append(nome_atual)
                    telefones.append(tel_atual)
                    tel_atual = None

    df = pd.DataFrame({
        "nome": nomes,
        "telefone": telefones
    })

    
    caminho_xlsx = obter_nome(caminho_vcf)

    df.to_excel(caminho_xlsx, index=False)

    print("Arquivo gerado:", caminho_xlsx)
    return caminho_xlsx


def iniciar(caminho):
    caminho_xlsx = vcf_para_xlsx(caminho)
    return caminho_xlsx
