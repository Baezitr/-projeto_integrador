import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()


def umTexto(solicitacao, mensagem, valido):
    digitouDireito = False
    while not digitouDireito:
        txt = input(solicitacao)

        if txt not in valido:
            print(mensagem, '- Favor redigitar...')
        else:
            digitouDireito = True

    return txt


def opcaoEscolhida(mnu):
    print()

    opcoesValidas = []
    posicao = 0
    while posicao < len(mnu):
        opcoesValidas.append(str(posicao + 1))
        posicao += 1
    return umTexto('Qual é a sua opção? ', 'Opção inválida', opcoesValidas)


def listar():
    consulta_sql = "select * from produto"
    mycursor.execute(consulta_sql)
    linhas = mycursor.fetchall()
    for linha in linhas:
        cp = float(linha[3])
        cf = float("{:.2f}".format(linha[4] / 100))
        cv = float("{:.2f}".format(linha[5] / 100))
        iv = float("{:.2f}".format(linha[6] / 100))
        ml = float("{:.2f}".format(linha[7] / 100))
        try:
            pv = float("{:.2f}".format(cp / (1 - (cf + cv + iv + ml))))
        except ZeroDivisionError:
            print(f"Valores inválidos para calcular o preço de venda do produto {linha[1], linha[2]}")
        else:
            pvP = 100
            cpP = round(cp / pv * 100)
            cfV = float("{:.2f}".format(cf * pv))
            cvV = float("{:.2f}".format(cv * pv))
            ivV = float("{:.2f}".format(iv * pv))
            receita_bruta_V = round(pv - cp, 2)
            receita_bruta_P = pvP - cpP
            cfP = cf * 100
            cvP = cv * 100
            ivP = iv * 100
            outros_custos_V = round(cfV + cvV + ivV, 2)
            outros_custos_P = round((cf + iv + cv) * 100)
            rent_V = round((receita_bruta_V) - (outros_custos_V))
            rent_P = (receita_bruta_P) - (outros_custos_P)
            print()
            print()
            dados = [
        [linha[1], "Valor", " %",],
        ["Código:", linha[0]],
        ["Descrição:", linha[2]],
        ["A. Preço de venda ", pv, pvP,"%"],
        ["B. Custo do produto", cp, cpP,"%"],
        ["C. Receita Bruta (A-B)", receita_bruta_V, receita_bruta_P,"%"],
        ["D. Custo Fixo/Administrativo", cfV, cfP, "%"],
        ["E. Comissão de Vendas ", cvV, cvP, "%"],
        ["F. Impostos sobre venda", ivV, ivP, "%"],
        ["G. Outros custos(D+E+F)", outros_custos_V, outros_custos_P, "%"],
        ["H. Rentabilidade (C-G)", rent_V, rent_P, "%"],
            ]
            tabela = tabulate(dados, headers="firstrow", tablefmt="fancy_grid")
            print (tabela)
            if rent_P > 20:
                print("O lucro obtido é alto!")
            elif rent_P > 10:
                print("O lucro obtido é médio!")
            elif rent_P > 0:
                print("O lucro obtido é baixo!")
            elif rent_P == 0:
                print("Não houve lucro!")
            elif rent_P < 0:
                print("Houve prejuízo!")
            print()


def inserir():
    t = True
    while t:
        try:
            cod = int(input("Digite o código do produto:  "))
            nome = input("Digite o nome do produto:  ")
            descricao = input("Digite a descrição do produto:  ")
            cp = float(input("Digite o custo do produto em reais:  "))
            cf = int(input("Digite o custo fixo do produto em porcentagem:  "))
            cv = int(input("Digite a comissão de vendas do produto em porcentagem:  "))
            iv = int(input("Digite o imposto sobre venda do produto em porcentagem :  "))
            ml = int(input("Digite a margem de lucro do produto em porcentagem :  "))
        except ValueError:
            print("Digite somente números!")
        t = False

    insert_sql = "INSERT INTO produto (cod, nome, descricao, cp, cf, cv, iv, ml) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (cod, nome, descricao, cp, cf, cv, iv, ml)
    mycursor.execute(insert_sql, values)
    mydb.commit()
    print(values, "foi inserido com sucesso")


def excluir():
    try:
        cod = -1
        while cod < 0:
            cod = int(input("Digite o código do produto que deseja excluir: ")) 
            consulta_sql = "SELECT * FROM produto WHERE cod = %s"
            mycursor.execute(consulta_sql, (cod,))
            produto = mycursor.fetchone()
            if produto is None:
                print("Produto não encontrado")
                return
            else:
                query = "DELETE from produto WHERE cod = %s"
                values = cod 
                mycursor.execute(query, (values,))
                mydb.commit()
                print("Deletado com sucesso!")
    except ValueError:
        print("Digite somente números!")


def alterar():
    try:
        codigo = int(input("Digite o código do produto que deseja alterar: "))
        consulta_sql = "SELECT * FROM produto WHERE cod = %s"
        mycursor.execute(consulta_sql, (codigo,))
        produto = mycursor.fetchone()

        if produto is None:
            print("Produto não encontrado.")
            return

        print("Produto encontrado. Detalhes atuais:")
        print("Nome:", produto[1])
        print("Descrição:", produto[2])
        print("Custo do Produto:", produto[3])
        print("Custo Fixo:", produto[4])
        print("Comissão de Vendas:", produto[5])
        print("Imposto sobre Vendas:", produto[6])
        print("Margem de Lucro:", produto[7])

        opcoes_validas = ['1', '2', '3', '4', '5', '6', '7', '8']
        while True:
            print("\nO que você deseja alterar?")
            print("1. Nome")
            print("2. Descrição")
            print("3. Custo do Produto")
            print("4. Custo Fixo")
            print("5. Comissão de Vendas")
            print("6. Imposto sobre Vendas")
            print("7. Margem de Lucro")
            print("8. Voltar ao menu principal")
            escolha = umTexto("Escolha a opção: ", "Opção inválida", opcoes_validas)

            if escolha == '8':
                return
            elif escolha == '1':
                novo_nome = input("Digite o novo nome do produto: ")
                update_sql = "UPDATE produto SET nome = %s WHERE cod = %s"
                mycursor.execute(update_sql, (novo_nome, codigo))
                mydb.commit()
                print("Nome atualizado com sucesso.")
            elif escolha == '2':
                nova_descricao = input("Digite a nova descrição do produto: ")
                update_sql = "UPDATE produto SET descricao = %s WHERE cod = %s"
                mycursor.execute(update_sql, (nova_descricao, codigo))
                mydb.commit()
                print("Descrição atualizada com sucesso.")
            elif escolha == '3':
                novo_custo = float(input("Digite o novo custo do produto: "))
                update_sql = "UPDATE produto SET cp = %s WHERE cod = %s"
                mycursor.execute(update_sql, (novo_custo, codigo))
                mydb.commit()
                print("Custo do produto atualizado com sucesso.")
            elif escolha == '4':
                novo_cf = int(input("Digite o novo custo fixo do produto: "))
                update_sql = "UPDATE produto SET cf = %s WHERE cod = %s"
                mycursor.execute(update_sql, (novo_cf, codigo))
                mydb.commit()
                print("Custo fixo atualizado com sucesso.")
            elif escolha == '5':
                novo_cv = int(input("Digite a nova comissão de vendas do produto: "))
                update_sql = "UPDATE produto SET cv = %s WHERE cod = %s"
                mycursor.execute(update_sql, (novo_cv, codigo))
                mydb.commit()
                print("Comissão de vendas atualizada com sucesso.")
            elif escolha == '6':
                novo_iv = int(input("Digite o novo imposto sobre vendas do produto: "))
                update_sql = "UPDATE produto SET iv = %s WHERE cod = %s"
                mycursor.execute(update_sql, (novo_iv, codigo))
                mydb.commit()
                print("Imposto sobre vendas atualizado com sucesso.")
            elif escolha == '7':
                nova_ml = int(input("Digite a nova margem de lucro do produto: "))
                update_sql = "UPDATE produto SET ml = %s WHERE cod = %s"
                mycursor.execute(update_sql, (nova_ml, codigo))
                mydb.commit()
                print("Margem de lucro atualizada com sucesso.")

    except ValueError:
        print("Digite um número válido.")

escolha = 69
dados = ''
menu = ['Inserir produto',\
      'Alterar produto',\
      'Excluir produto',\
      'Listar produtos',\
      'Sair do Programa']
tabela = tabulate(dados, headers= ['1.Inserir produto', '2.Excluir Produto', '3.Alterar produto', '4.Listar produtos', '5.Sair do programa'], tablefmt="grid")

while escolha != 5:
    escolha = int(opcaoEscolhida(menu))
    if escolha == 1:
        inserir()
    if escolha == 2:
        alterar()
    if escolha == 3:
        excluir()
    if escolha == 4:
        listar()

print('OBRIGADO POR USAR ESTE PROGRAMA!')

