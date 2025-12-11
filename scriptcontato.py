#Commmit 02
import re
import pandas as pd

def limpar_numero(num):
    if not num:
        return ""
    
    # remove tudo que não for número
    n = re.sub(r'\D', '', num)
    
    # remove prefixos repetidamente
    prefixos = ["015", "55", "0"]
    mudou = True
    while mudou:
        mudou = False
        for p in prefixos:
            if n.startswith(p):
                n = n[len(p):]
                mudou = True
    return n


def vcf_para_xlsx(vcf_path, xlsx_path):
    nomes = []
    numeros = []

    with open(vcf_path, "r", encoding="utf-8", errors="ignore") as f:
        nome_atual = None
        numero_atual = None

        for linha in f:
            linha = linha.strip()

            # Nome
            if linha.startswith("FN:"):
                nome_atual = linha[3:].strip()

            # Número (pode ter formato TEL;CELL;VOICE:xxxx)
            if linha.startswith("TEL"):
                numero_raw = linha.split(":")[-1].strip()
                numero_atual = limpar_numero(numero_raw)

            # Fim do contato
            if linha == "END:VCARD":
                if nome_atual and numero_atual:
                    nomes.append(nome_atual)
                    numeros.append(numero_atual)
                nome_atual = None
                numero_atual = None

    df = pd.DataFrame({
        "nome": nomes,
        "numero": numeros
    })

    df.to_excel(xlsx_path, index=False)
    print(f"Arquivo criado: {xlsx_path}")
