import mysql.connector

try:
    mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)
    consulta_sql="select * from produto"
    mycursor = mydb.cursor()
    mycursor.execute(consulta_sql)
    linhas=mycursor.fetchall()
    print(mycursor.rowcount)

    for linha in linhas:
        cp= float(linha[3])
        cf=float("{:.2f}".format(linha[4]/100))
        cv=float("{:.2f}".format(linha[5]/100))
        iv=float("{:.2f}".format(linha[6]/100))
        ml= float("{:.2f}".format(linha[7]/100))
        pv= float("{:.2f}".format(cp/(1-(cf+cv+iv+ml))))
        pvP= 100
        cpP= round(cp/pv*100)
        cfV= float("{:.2f}".format(cf*pv))
        cvV= float("{:.2f}".format(cv*pv))
        ivV= float("{:.2f}".format(iv*pv))
        receita_bruta_V= round(pv-cp,2) 
        receita_bruta_P=pvP-cpP
        cfP=cf*100
        cvP=cv*100
        ivP=iv*100
        outros_custos_V=round(cfV+cvV+ivV,2)
        outros_custos_P=round((cf+iv+cv)*100)
        rent_V=round((receita_bruta_V)-(outros_custos_V))
        rent_P=(receita_bruta_P)-(outros_custos_P)
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
        print("\n")
              
              
except ValueError:
    print()
