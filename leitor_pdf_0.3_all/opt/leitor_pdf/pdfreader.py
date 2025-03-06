#!/usr/bin/env python

#
# leitorPDF.py (Python)
#
# Objetivo: Extrai o texto dos arquivos PDFs.
#
# Site https://github.com/edmartineznunes
#
# Versão 0.1
#
# Programador: Eduardo Martinez 11/02/2025
#
# Email: eduardomartineznunes@gmail.com
#
# Licença: GPL-3.0 <https://www.gnu.org/licenses/gpl-3.0.txt


from pypdf import PdfReader
import sqlite3        

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


caminho="/opt/leitor_pdf/"

def Seleciona_Pontos():
    lin=750
    col=60 
    pdf = canvas.Canvas("decimoquarto.pdf",pagesize=letter)
    pdf.setTitle("Pontuação para o Décimo Quarto Ano:2024")
    pdf.setFont("Helvetica-Bold",12)
    pdf.drawString(col,lin,"Lista de Pontuação dos Agentes\
 de Mobilidade SEMOB-JP Ano: 2025" )
    pdf.setFont("Helvetica-Oblique",10)
    
    lin-=30
    conn=sqlite3.connect(caminho+"decimo_quarto.db")
    cursor=conn.cursor()
    cursor.execute("SELECT Pontos from decimo")
    conj_pontos=set()
    for ponto in cursor.fetchall():
        conj_pontos.add(ponto[0])

    list_pontos=list(conj_pontos)
    list_pontos.sort(reverse=True)
    num_ordem = 1
    
    for pontuacao in list_pontos:
        cursor.execute("SELECT Nome from decimo where\
                Pontos='"+str(pontuacao)+"' ")
        print("Pontuação de:",pontuacao)
        pdf.setFont("Helvetica-Bold",10)
        pdf.drawString(col-40,lin,f'Pontuação de: {pontuacao} {"="*60}')
        lin-=20
        pdf.setFont("Helvetica-Oblique",10)
        for nome in cursor.fetchall():
            print(f'{num_ordem}. {nome[0]}')
            pdf.drawString(col,lin, f'{num_ordem}. {nome[0]}')
            num_ordem+=1
            lin-=18
            
            if lin < 20:
                
                pdf.showPage()
                lin=750
                pdf.setFont("Helvetica-Oblique",10)


    pdf.showPage()
    pdf.save()
    print("PDF criado com Sucesso !!!")



def Gravar_Db (nome,pontos_ac,conn):
    #### sqlite #####
    print (nome,pontos_ac)
    ### Inserindo dados na tabela ###
    cursor = conn.cursor()
    if mes == "JANEIRO":
        cursor.execute("INSERT INTO decimo (Nome,Pontos) \
                VALUES ('"+nome+"','"+pontos_ac+"') ")
        conn.commit()
        
        
    else:
        ### Atualizar dados na tabela ###
        cursor.execute("SELECT Pontos from decimo WHERE Nome = '"+nome+"' ")
        novo_ponto_ac = 0
        for valor in cursor.fetchall():
            novo_ponto_ac = valor[0] + float(pontos_ac)
        #input(novo_ponto_ac)
        print(f"Atualizado para:{novo_ponto_ac}")
        cursor.execute("UPDATE decimo SET Pontos = '"+str(novo_ponto_ac)+"' \
                WHERE Nome = '"+nome+"'  ")
        conn.commit()
        print("Dados Atualizados com Sucesso !!!")



#Extrai o nome e Pontos Acumulados
def Agentes(conteudo="",pagina=0,sub_tot=0):
    
    nome=""
    pontos=""
    
    if conteudo:
        conn =sqlite3.connect(caminho+'decimo_quarto.db')
        if conn:
            print("Conexão com DB feita com Sucesso !!!")
            for nome in conteudo:
            
                pontos=nome.split()
                nome=nome[0:5]+" "+nome[5:22]
   
                Gravar_Db(nome,pontos[-1]\
                        .replace(",",".")\
                        .replace("0.00#","")\
                        .replace("40.02#","")\
                        .replace("40.02###","")\
                        .replace("#",""),conn)
    

        else:
            print("Error ao Abrir o DB !!!")
            exit()
           
        #print(agentes) 
        print("pagina:",pagina+1,"total:",sub_tot)
        print("----------------")
        conn.close()

def Extrair_PDF():
    
    page_1=page_2=page_3=""
    conteudo=""
    sub_tot=0
    total=0
    
    for n_page, pdf_page in enumerate(pdf_leitor.pages):
        if n_page == 0:
            page_1+=pdf_page.extract_text()
            conteudo=page_1.split("\n")
            #print(conteudo[10:55]) # 45 agentes
            conteudo=conteudo[10:55] 
            sub_tot=(len(conteudo))     
    
        elif n_page == 1:
            page_2+=pdf_page.extract_text()
            conteudo=page_2.split("\n")
            conteudo=conteudo[7:68] # 61 agentes
            sub_tot=(len(conteudo))     
       
        else:
            page_3+=pdf_page.extract_text()
            conteudo=page_3.split("\n")
            conteudo=conteudo[7:43] # 36 agentes
            sub_tot=(len(conteudo))     
        

        Agentes(conteudo,n_page,sub_tot)
        
        # total de agentes 142 

       
print ("==== Escolha a Opção ====")
print ("""
        1- Atualizar Pontuação do Mês
        2- Imprimir Lista de Agentes
        3- Sair

        """ )
op= int(input("Escolha a opção: "))
if op == 1: 
    
    n_mes = input("Mês(somente números):")

    meses={'1':"JANEIRO",'2':"FEVEREIRO",'3':"MARÇO",'4':"ABRIL",\
        '5':"MAIO",'6':"JUNHO",'7':"JULHO",'8':"AGOSTO",\
        '9':"SETEMBRO",'10':"OUTUBRO",'11':"NOVEMBRO",'12':"DEZEMBRO"}
    
    caminho_av="/opt/leitor_pdf/Avaliacoes/"
    


    mes=meses[n_mes]
    print(f'A avaliação do Mês: {mes} será Salvo no DB!!!')
    input()
    pdf_leitor =PdfReader(caminho_av+mes)
    
    Extrair_PDF()

elif op == 2:
    Seleciona_Pontos()
elif op == 3:
    exit(0)
else:
    print("opção invalida !!!")
    exit(1)



