import pandas as pd

bd_Rev = pd.read_excel("BD_148.00.xlsx", sheet_name= "prop")


def cpf_Duplicado(arquivo, aba):
    #dataframe
    cpf_fase_1 = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = f"{aba}"))
    #ciando uma lista com os vlores de Cpf que eu quero procurar
    series_cpf_F1 = list(cpf_fase_1["1.1.1.1.a"])
    #checando no meu dataframe da bae se os valores da minha lista, existem na coluna específica
    #split
    erros = bd_Rev[bd_Rev["ID-SGS:"].isin(series_cpf_F1)]
    # criand o a lista de informações que eu quero da base alpem dos cpf duplicados que eu encontrei
    data_erros = erros[["Id-SGC","ID Pessoa", "Pessoa", "Qual é o seu número de CPF?", "Possui ID-SGS-Pessoa? - Sim - ID-SGS-Pessoa:"]]
    cpf_duplicadoF2 = pd.DataFrame(data = data_erros)
    cpf_duplicadoF2.to_excel("CPF_Duplicado_Fase_2.xlsx")
    return cpf_duplicadoF2


cpf_Duplicado("controle_pessoas", "Estrutura")

def carac_especial(arquivo, coluna_df):
    bd_pes = pd.read_excel(arquivo, sheet_name= "pes")
    coluna_df = list(bd_pes["Qual é o nome da sua mãe? - Sabe o nome - Nome:"])
    caract_special = ["!","@","#","$","%","¨","&","<",">",]
    




carac_especial("Pasta.xlsx","Qual é o nome da sua mãe? - Sabe o nome - Nome:")



bd_Rev = pd.read_excel("Pasta.xlsx", sheet_name= "pes")
bdpess = pd.DataFrame(data = bd_Rev)
coluna_de_interesse = bdpess[["ID Pessoa", "Qual é o nome da sua mãe? - Sabe o nome - Nome:"]]
coluna_de_interesse

idsgs = ["0824251-NAAAAAA-0000000-0554793", "0949313-NAAAAAA-0000000-0615965", "0928992-NAAAAAA-0000000-0613876"]
idsgs_dupli = "0949313-NAAAAAA-0000000-0615965"
df = pd.DataFrame(data = idsgs, columns= ["ID-SGS"])
dft = pd.DataFrame()
lista_idsgs = list(df["ID-SGS"])
for i in lista_idsgs:
   i.split('-')
   

print(dft)

