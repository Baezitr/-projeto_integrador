import mysql.connector
mydb = mysql.connector.connect(
host = "", 
user = "",
password ="",
database ="" 
)
mycursor = mydb.cursor()

def umTexto (solicitacao, mensagem, valido):
    digitouDireito=False
    while not digitouDireito:
        txt = input(solicitacao)

        if txt not in valido:
            print(mensagem, '- Favor redigitar...')
        else:
            digitouDireito=True

    return txt
          
def opcaoEscolhida (mnu):
  print ()

  opcoesValidas=[]
  posicao=0
  while posicao<len(mnu):
      print (posicao+1,') ',mnu[posicao],sep='')
      opcoesValidas.append(str(posicao+1))
      posicao+=1
  return umTexto('Qual é a sua opção? ', 'Opção inválida', opcoesValidas)

def listar():
  consulta_sql = "select * from produto" #nome da tabela
  mycursor.execute(consulta_sql)
  linhas = mycursor.fetchall() 
  for linha in linhas:
      cp = float(linha[3])
      cf = float("{:.2f}".format(linha[4]/100))
      cv = float("{:.2f}".format(linha[5]/100))
      iv = float("{:.2f}".format(linha[6]/100))
      ml = float("{:.2f}".format(linha[7]/100))
      try:
        pv= float("{:.2f}".format(cp/(1-(cf + cv + iv + ml))))
      except ZeroDivisionError:
        print(f"Valores inválidos para calcular o preço de venda do produto {linha[1], linha[2]}")
      else:
        pvP = 100
        cpP = round(cp/pv*100)
        cfV = float("{:.2f}".format(cf * pv))
        cvV = float("{:.2f}".format(cv * pv))
        ivV = float("{:.2f}".format(iv * pv))
        receita_bruta_V = round(pv-cp,2) 
        receita_bruta_P =pvP-cpP
        cfP = cf*100
        cvP = cv*100
        ivP = iv*100
        outros_custos_V = round(cfV + cvV + ivV,2)
        outros_custos_P = round((cf + iv + cv) * 100)
        rent_V = round((receita_bruta_V) - (outros_custos_V))
        rent_P = (receita_bruta_P) - (outros_custos_P)
        print("Código:", linha[0])
        print("Nome:", linha[1])
        print("Descrição:", linha[2])
        print("A. Preço de venda " + "R$",pv,   pvP,"%")
        print("B. Custo do produto"+ "R$", cp,   cpP,"%")
        print("C. Receita Bruta (A-B)", "R$",receita_bruta_V,   receita_bruta_P,"%")
        print("D. Custo Fixo/Administrativo", "R$",cfV,   cfP,"%")
        print("E. Comissão de Vendas ", "R$",cvV,   cvP,"%")
        print("F. Impostos sobre venda", "R$",ivV,   ivP,"%")
        print("G. Outros custos(D+E+F)", "R$",outros_custos_V,   outros_custos_P,"%")
        print("H. Rentabilidade (C-G)", "R$",rent_V,   rent_P,"%") 
        print()
        if rent_P>20:
            print("O lucro obtido é alto!")
        elif rent_P>10:
            print("O lucro obtido é médio!")
        elif rent_P>0:
            print("O lucro obtido é baixo!")
        elif rent_P==0:
            print("Não houve lucro!")
        elif rent_P<0:
            print("Houve pejuízo!")
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
  values = (cod,nome,descricao,cp,cf,cv,iv,ml)
  mycursor.execute(insert_sql, values)
  mydb.commit()
  print(values, "foi inserido com sucesso")

def excluir():
  e = True
  while e:
    try:
      codigo = int(input("digite o código do produto: "))
      delete_sql= "DELETE FROM produtos where cod = %s" 
      cod = codigo 
      mycursor.execute(delete_sql, (cod,))
      mydb.commit()
      e=False
    except ValueError:
      print("Digite somente números!")






escolha = 69
menu=['Inserir produto',\
      'Alterar produto',\
      'Excluir produto',\
      'Listar produtos',\
      'Sair do Programa']

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
            
      
