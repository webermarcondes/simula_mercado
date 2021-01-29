"""
Simula o funcionamento de um Supermercado.
"""

from random import randint
from time import sleep


def valida_input(msg, respostas_validas, erro):
    """
    Cria um laço de repetição "while True" que só é encerrado quando o usuário fornece uma resposta válida.
    enquanto isso não acontece, uma mensagem de "erro" é mostrada na tela.

    param msg(str): mensagem mostrada ao úsuario no input
    param respostas_validas(list): respostas válidas para o input
    param erro(str): mensagem que será mostrada ao usuário, se ele fornecer um dado inválido
    return(str): o dado fornecido válido
    """
    while True:
        entrada = input(msg).lstrip()
        if entrada in respostas_validas:
            break
        print(f"\n\033[31m{erro}\033[m\n")

    return entrada


def valida_preco(valor):
    """
    Analisa um valor monetário, verificando se ele pode ser convertido para float e se não possui nenhum erro.

    param preco(str): valor fornecido pelo usuário.
    return(bool): True se o valor for válido, False se não for.
    """

    if valor.count(".") <= 1 and not ("." == valor[0] or "." == valor[-1]) and valor.count("+") <= 1 and valor.find("+") <= 0:
        caracteres_removiveis = valor.maketrans({"+": None, ".": None})
        if valor.translate(caracteres_removiveis).isnumeric():
            return True

    return False


def validacao_unidade(dado_caixa, cod_produto):
    """
    Verifica se o dado inserido no caixa para passar um produto vendido em UN(unidade) é válido.

    param dado_caixa(str): dado inserido no caixa.
    param cod_produto(str): código do produto.
    return(bool): True se for válido, False se não for.
    """
    if dado_caixa == cod_produto:
        return True

    elif "*" in dado_caixa and "*" != dado_caixa[0] and "*" != dado_caixa[-1]:
        indice_mult = dado_caixa.index("*")
        numero_multiplicador = dado_caixa[indice_mult + 1:] if dado_caixa[:indice_mult].strip() == cod_produto else dado_caixa[:indice_mult]

        return True if numero_multiplicador.strip().isnumeric() else False

    return False


def formata_moeda(valor):
    """
    Formata um valor para moeada(R$), com duas casas decimais e R$ no final.

    param valor(float): valor que será formatado.
    return(str): valor formatado.
    """
    return f"{valor:.2f}R$".replace(".", ",")


def cria_tabela(titulo, nome_colunas, apresentacao, dados):
    """
    Cria uma tabela para mostrar dados

    param titulo(str): Titulo da tabela
    param nome_colunas(list): nomes das colunas
    param apresentacao(string): formatação para os dados que serão apresentados, deve conter chaves({}) e não aceita nenhum
                                método de string, apenas alinhamento por ":<", ":>",":^".

    param dados(list): dados que serão mostrados.
    """

    msg_coluna = "".join([f"|  {nome_c}  " for nome_c in nome_colunas]) + "|"
    largura_tabela = len(msg_coluna)

    print("=" * largura_tabela)
    print(f"|{titulo.center(largura_tabela - 2)}|")
    print("=" * largura_tabela)
    print(msg_coluna)
    print("=" * largura_tabela)
    for dado in dados:
        print(apresentacao.format(*dado))
    print("=" * largura_tabela)


def cria_menu(*args):
    """
    Cria um menu com opções

    param args: opções que irão aparecer no menu
    """

    print()
    for num, op in enumerate(args):
        print(f"[ {num + 1} ] {op}")
    print()


def atualizar_estoque(dados, modo):
    """
    Abre o arquivo "produtos.txt" e adiciona dados a ele

    param dados(list): dados que seraão adicionados ao arquivo
    param modo(str): modo de abertura do arquivo
    """

    with open('produtos.txt', modo) as estoque:
        for p in dados:
            estoque.write(f"{p['codigo'].ljust(10)}{p['nome'].replace(' ', '-').center(30)}{p['valor'].rjust(7)}{p['vendido_em'].rjust(10)}\n")


produtos = []
try:
    produtos_estoque = open("produtos.txt").readlines()
    if len(produtos_estoque) > 0:
        for linha in produtos_estoque:
            linha = linha.split()
            produtos.append({"codigo": linha[0],
                             "nome": linha[1].replace("-", " "),
                             "valor": linha[2],
                             "vendido_em": linha[3]})
    else:
        print("\033[33mNão hã produtos no estoque, adicione produtos antes de abrir o caixa.\033[m")

except FileNotFoundError:

    produtos = [{'codigo': "135729", "nome": "Pão", "valor": "0.5", "vendido_em": "UN"},
                {'codigo': "345213", "nome": "Leite", "valor": "3.75", "vendido_em": "UN"},
                {'codigo': "423155", "nome": "Bandeja de ovos", "valor": "4.78", "vendido_em": "UN"},
                {'codigo': "123415", "nome": "Mortadela", "valor": "2.45", "vendido_em": "GR"},
                {'codigo': "324778", "nome": "Arroz", "valor": "4.0", "vendido_em": "UN"}]

    atualizar_estoque(produtos, "w")


total = 0
cont_clientes = 0
qtde_produtos = len(produtos)
while True:
    cria_menu("Abrir Caixa", "Gerenciar Estoque", "Sair")
    opcao = valida_input(msg="Opção Desejada: ",
                         respostas_validas=["1", "2", "3"],
                         erro="Erro! essa opção não existe")

    # [ 1 ] Abrir Caixa
    if opcao == "1":
        if qtde_produtos > 0:
            print("\n\033[32;1mCaixa Aberto!\033[m")
            continuar = ""

            while not continuar == "N":
                cont_clientes += 1

                # Simulação da compra de um cliente
                qtde_compra = randint(1, len(produtos))
                compra_cliente = []
                while not len(compra_cliente) == qtde_compra:
                    indice_produto = randint(0, len(produtos) - 1)
                    dados_produto = produtos[indice_produto]

                    if not any(dados_produto['codigo'] == produto['codigo'] for produto in compra_cliente):

                        quantidade = randint(1, 20) if dados_produto['vendido_em'] != "GR" else randint(100, 2000)

                        if dados_produto['vendido_em'] == "GR" and quantidade >= 1000:
                            dados_produto['vendido_em'] = "KG"

                        compra_cliente.append({**dados_produto, "qtde": str(quantidade)})

                # Trabalho do caixa
                produtos_passados = []
                total_compra = 0
                while not len(compra_cliente) == 0:
                    print()
                    cria_tabela(titulo=f"Compra do Cliente {cont_clientes}",
                                nome_colunas=["Código", "Nome do Produto", "Quantidade"],
                                apresentacao="|{0:^10}|{1:^19}|{4:>7}{3:<7}|",
                                dados=[produto.values() for produto in compra_cliente])

                    caixa = input("\nCódigo do produto: ").lstrip().replace("x", "*")

                    # Os dados fornecidos para a variável caixa devem seguir dois padrões:
                    #
                    # 1 - Se o produto for vendido em UN(unidade), a variável deve receber: código do produto x quantidade_comprada
                    # 2 - Se o produto for vendido em GR(gramas), a variável deve receber apenas o código do produto

                    if any(produto['codigo'] in caixa for produto in produtos):
                        for indice, produto in enumerate(compra_cliente):
                            codigo = produto['codigo']

                            if codigo in caixa and produto not in produtos_passados:
                                nome, v_unidade, vendido_em, qtde = produto['nome'], produto['valor'], produto['vendido_em'], produto['qtde']
                                preco = 0

                                if vendido_em == "UN" and validacao_unidade(caixa, codigo):

                                    caixa = eval(caixa.replace(codigo, v_unidade))
                                    if caixa == float(v_unidade) * int(qtde):
                                        del compra_cliente[indice]
                                        preco = caixa
                                        produtos_passados.append({"codigo": codigo,
                                                                  "nome": nome,
                                                                  "quantidade": qtde,
                                                                  "vendido_em": vendido_em,
                                                                  "preço": formata_moeda(preco)})
                                    else:
                                        print("\n\033[31mErro! O valor definido para o produto é diferente do que o cliente deve pagar.\033[m\n")

                                elif vendido_em != "UN" and caixa == codigo:
                                    del compra_cliente[indice]
                                    preco = float(v_unidade) * (int(qtde) / 100)
                                    produtos_passados.append({"codigo": codigo,
                                                              "nome": nome,
                                                              "quantidade": qtde,
                                                              "vendido_em": vendido_em,
                                                              "preço": formata_moeda(preco)})
                                else:
                                    print("\n\033[31mErro! o dado inserido no caixa para passar o produto é inválido, tente novamente.\033[m\n")

                                total_compra += preco
                                break

                        else:

                            if any(produto['codigo'] in caixa for produto in produtos_passados):
                                print("\n\033[31mErro! Este produto já foi passado no caixa\033[m\n")
                            else:
                                print("\n\033[31mErro! O cliente não comprou este produto.\033[m\n")

                    else:
                        print("\n\033[31mErro! não existe nenhum produto com este código.\033[m\n")
                    sleep(2)

                print()
                cria_tabela(titulo="Produtos Passados",
                            nome_colunas=["Nome do Produto", "Quantidade", "Valor Total"],
                            apresentacao="|{1:^19}|{2:>7}{3:<7}|{4:>11}    |",
                            dados=[produto.values() for produto in produtos_passados])
                print(f"Total gasto: {formata_moeda(total_compra)}\n")

                total += total_compra

                continuar = valida_input(msg="Continuar atendendo clientes? sim(S)/não(N): ",
                                         respostas_validas=["S", "N"],
                                         erro="Erro! Resposta inválida, tente novamente.")
                sleep(2)

            print("\n\033[31;1mCaixa Fechado!\033[m\n")

        else:
            print("\n\033[33mNão hã produtos para vender. Antes de abrir o caixa, adicione produtos ao estoque.\033[m")

    # [ 2 ] Gerenciar Estoque
    elif opcao == "2":

        while True:
            qtde_produtos = len(produtos)
            print()
            if qtde_produtos > 0:
                cria_tabela(titulo="Produtos em Estoque",
                            nome_colunas=["Código", "Nome do Produto", "Valor do Produto", "Vendido em"],
                            apresentacao="|{0:^10}|{1:^19}|   {2:>10}       |{3:^14}|",
                            dados=[[p['codigo'], p['nome'], formata_moeda(float(p['valor'])), p['vendido_em']] for p in produtos])

                cria_menu("Adicionar Produtos", "Editar Produtos", "Apagar Produtos", "Voltar")
            else:
                print("\n\033[33mNão Hã produtos no estoque, adicione produtos.\033[m")

                cria_menu("Adicionar Produtos", "Voltar")

            opcao = valida_input(msg="Opção desejada: ",
                                 respostas_validas=["1", "2", "3", "4"] if qtde_produtos > 0 else ["1", "2"],
                                 erro="Erro! essa opção não existe")

            # Adicionar Produtos
            if opcao == "1":
                cont_adicionados = 0
                continuar = ""
                while not continuar == "N":
                    nome_novo = input("\nNome do produto: ").capitalize().lstrip()

                    if nome_novo.replace(" ", "").isalpha() and not nome_novo[-1].isspace():
                        if not any(produto["nome"] == nome_novo for produto in produtos):

                            while True:
                                preco_novo = input("Valor do produto: R$").lstrip().replace(",", ".")
                                if valida_preco(preco_novo):
                                    break

                                print("\n\033[31mErro! O valor definido para o produto é inválido.\033[m\n")

                            vendido_em_novo = valida_input(msg="O novo produto será vendido em UN(unidade) ou GR(gramas): ",
                                                           respostas_validas=["UN", "GR"],
                                                           erro="Erro! Opção inválida, tente novamente.")

                            while True:
                                codigo_novo = ""
                                for n in range(6):
                                    codigo_novo += str(randint(0, 9))
                                if not any(codigo_novo == produto['codigo'] for produto in produtos):
                                    break

                            produtos.append({"codigo": codigo_novo,
                                             "nome": nome_novo,
                                             "valor": str(preco_novo),
                                             "vendido_em": vendido_em_novo})

                            cont_adicionados += 1

                            print(f"\n\033[32m;1O Produto {nome_novo} foi adicionado ao estoque, seu código é {codigo_novo}\033[m\n")

                            continuar = valida_input(msg="Continuar adicionando produtos? sim(S)/não(N): ",
                                                     respostas_validas=["S", "N"],
                                                     erro="Erro! Resposta inválida, tente novamente.")
                            sleep(2)

                        else:
                            print("\n\033[31mErro! Já existe um produto com esse nome.\033[m\n")
                    else:
                        print("\n\033[31mErro! Nome inválido, tente novamente.\033[m\n")

                atualizar_estoque(produtos[-cont_adicionados:], "a")

            # Editar Produtos
            elif opcao == "2" and not qtde_produtos == 0:
                continuar = ""
                while not continuar == "N":

                    pos = 0
                    nome = ""
                    while True:

                        dado_produto = input("\nDigite o Nome ou Código do Produto que deseja editar: ").lstrip()
                        for indice, produto in enumerate(produtos):
                            if dado_produto == produto['codigo'] or dado_produto.capitalize() == produto['nome']:
                                pos = indice
                                nome = produto['nome']
                                break
                        else:
                            print("\n\033[31mErro! Produto não encontrado.\033[m\n")
                            continue
                        break

                    while True:
                        print(f"\nDados do Produto {nome} disponíveis para edição")
                        cria_menu("Valor do Produto", "Forma de Venda", "Finalizar edição do produto")
                        opcao = valida_input(msg="Opção desejada: ",
                                             respostas_validas=["1", "2", "3"],
                                             erro="Erro! essa opção não existe")

                        # [ 1 ] Valor do Produto
                        if opcao == "1":
                            while True:
                                valor_editado = input(f"Digite o novo valor para o Produto {nome}: R$").lstrip().replace(",", ".")
                                if valida_preco(valor_editado):
                                    produtos[pos]['valor'] = valor_editado
                                    break

                                print("\n\033[31mErro! O valor definido para o Produto é inválido\033[m\n")

                            print(f"\n\033[32;1mO valor do produto {nome} foi alterado\033[m")
                            sleep(2)

                        # [ 2 ] Vendido em
                        elif opcao == "2":
                            vendido_em_editado = "UN" if produtos[pos]['vendido_em'] == "GR" else "GR"
                            print(f"\n\033[32;1mO(A) produto {nome}, que era vendido(a) em {'UN(unidade)' if produtos[pos]['vendido_em'] == 'UN' else 'GR(gramas)'}, agora será vendido(a) em {'UN(unidade)' if vendido_em_editado == 'UN' else 'GR(gramas)'}\033[m")
                            produtos[pos]['vendido_em'] = vendido_em_editado
                            sleep(2)

                        # [ 3 ] Finalizar Edição
                        elif opcao == "3":
                            sleep(2)
                            break

                    continuar = valida_input(msg="Continuar editando produtos? sim(S)/não(N): ",
                                             respostas_validas=["S", "N"],
                                             erro="Erro! Resposta inválida, tente novamente.")
                    sleep(2)

                atualizar_estoque(produtos, "w")

            # Apagar Produtos
            elif opcao == "3":
                continuar = ""
                while not continuar == "N" and not qtde_produtos == 0:
                    while True:
                        dado_produto = input("\nDigite o Código ou Nome do Produto que deseja apagar: ").lstrip()
                        for indice, produto in enumerate(produtos):
                            if dado_produto == produto['codigo'] or dado_produto.capitalize() == produto['nome']:
                                print(f"\n\033[33mO produto {produto['nome']} foi removido do estoque\033[m\n")
                                qtde_produtos -= 1
                                del produtos[indice]
                                break
                        else:
                            print("\n\033[31mErro! Produto não encontrado.\033[m\n")
                            continue
                        break

                    if qtde_produtos > 0:
                        continuar = valida_input(msg="Continuar apagando produtos? sim(S)/não(N): ",
                                                 respostas_validas=["S", "N"],
                                                 erro="Erro! Resposta inválida, tente novamente.")
                        sleep(2)
                    else:
                        print("\033[33mNão hã mais produtos para apagar. Saindo", end="")
                        for p in range(4):
                            print(".", end="", flush=True)
                            sleep(0.5)
                        print("\033[m")

                atualizar_estoque(produtos, "w")

            # Voltar
            elif opcao == "4" and qtde_produtos > 0 or opcao == "2" and qtde_produtos == 0:
                sleep(2)
                break

    # [ 3 ] Sair
    elif opcao == "3":
        if cont_clientes > 0:
            print(f"\nCliente(s) atentido(s): {cont_clientes}\nGanhos: {formata_moeda(total)}")
        break
