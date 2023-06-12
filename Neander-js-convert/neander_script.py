import sys


def ler_arquivo(file1: str) -> list:
    try:
        with open(file1) as arquivo:
            leitura = arquivo.read().splitlines()
            # Divide cada linha em um item de lista
            list = [x.split() for x in leitura]
            # Divide cada item de lista (se tiver mais de uma coisa) em sublista
            return [e for y in list for e in y]
            # Retorna lista com cada string, incluindo das sublistas
    except:
        print("Arquivo não encontrado.")
        sys.exit(1)


def sub_com_dict(txt: str) -> str:
    sub = {
        "STA": "16",
        "LDA": "32",
        "ADD": "48",
        "OR": "64",
        "AND": "80",
        "NOT": "96",
        "JMP": "128",
        "JN": "144",
        "JZ": "160",
        "HLT": "240",
    }
    for x, y in sub.items():
        txt = txt.replace(x, y)
    # Substitui os mnemônicos por seus respectivos códigos de instrução
    return txt


def mnem_para_num(lista: list) -> list:
    for c, item in enumerate(lista):
        lista[c] = sub_com_dict(item)  # Chamar a função de substituição
        if int(lista[c]) < 0:
            lista[c] = str(int(item) + 256)
        # Formata os números negativos para o próximo passo.
        # ex.: -1    -> 255 -> ff
        #      -57   -> 199 -> c7
        #      -128 - > 128 -> 80
    return lista


def lista_para_hex(lista: list) -> list:
    for c, elem in enumerate(lista):
        lista[c] = hex(int(elem)).replace("0x", "")
        if len(elem) == 1:
            lista[c] = f"0{elem}"  # hex(1) = '0x1' -> 1 -> 0100 não 1000
        while len(lista[c]) < 4:
            lista[c] += "0"
        # A formatação do import do Neander.js tem cada valor com 4 caractéres.
    return lista


def concatenar_hex(lista: list) -> str:
    cabeçalho = "034e4452"
    lista.insert(0, cabeçalho)
    return "".join(lista)


def formatar_hex(string: str) -> str:
    return "\n".join(string[i : i + 60] for i in range(0, len(string), 60))
    # O código do NEANDER é dividido em linhas de até 60 caractéres.


def gravar_arquivo(file2: str, conteúdo: str):
    with open(file2, "a") as arquivo:
        arquivo.truncate(0)  # Limpa o arquivo
        print(conteúdo, file=arquivo)
        print("Arquivo escrito.")


def main():
    lista_raw = ler_arquivo(sys.argv[1])
    lista_num = mnem_para_num(lista_raw)
    lista_hex = lista_para_hex(lista_num)
    string_hex = concatenar_hex(lista_hex)
    string_hex_f = formatar_hex(string_hex)

    gravar_arquivo(sys.argv[2], string_hex_f)


if __name__ == "__main__":
    main()
