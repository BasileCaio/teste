import pandas as pd

pesquisadores = pd.read_excel(f'PESQUISADORES_PLANTOES_01-8-2022.xlsx', sheet_name=None)
plantao = pd.read_excel(f'PLANTAO 01-08-2022_CONFIRMACOES.xlsx', sheet_name=None) 



aba_plantao = list(plantao.items())[2][1]
aba_plantao = aba_plantao[aba_plantao['STATUS (LIGAÇÃO CONFIRMAÇÃO)'] == 'Confirmado'].sort_values(by='Codigo Pessoa').reset_index(drop=True)
colunas_plantao = aba_plantao.columns.to_list()
df_provisorio = pd.DataFrame(columns=colunas_plantao)
#aqui realoco os cadastros duplicados (mais de uma propriedade), pra um dataframe provisório. 
# dessa forma, posso atribuir a lista de pesquisadores a todos os horários, para depois adicionar as propriedades extras aos pesquisadores corretos.
lista_index_dropar = []
for index, value in enumerate(aba_plantao['Codigo Pessoa']):
    try:
        if aba_plantao['Codigo Pessoa'][index] == aba_plantao['Codigo Pessoa'][index + 1]:
            df_provisorio=pd.concat([df_provisorio, aba_plantao.iloc[[index + 1]]])
            lista_index_dropar.append(index + 1)
    except KeyError:
        pass

aba_plantao['HORÁRIO'] = aba_plantao['HORÁRIO'].apply(lambda x: x.strftime('%H:%M') if (type(x) != str) else x)
aba_plantao.drop(lista_index_dropar,axis=0, inplace=True)
aba_plantao = aba_plantao.reset_index(drop = True)


aba_plantao = aba_plantao.sort_values(by='HORÁRIO')
serie_pesquisadores = list(pesquisadores.items())[3][1]
serie_pesquisadores = serie_pesquisadores.iloc[:,0]
aba_plantao['PESQUISADOR']  = np.tile(serie_pesquisadores, len(aba_plantao) // len(serie_pesquisadores) + 1)[:len(aba_plantao)]
aba_plantao = aba_plantao.reset_index(drop=True)

#concatenando dfs, para dps atribuir os cadastros de propriedade extra aos devidos pesquisadores.
aba_plantao=pd.concat([aba_plantao, df_provisorio])
aba_plantao['HORÁRIO'] = aba_plantao['HORÁRIO'].apply(lambda x: x.strftime('%H:%M') if (type(x) != str) else x)
aba_plantao = aba_plantao.sort_values(by='Codigo Pessoa').reset_index(drop=True) 


dict_cod_pessoas = {}
for index, value in enumerate(aba_plantao['PESQUISADOR']):
    if type(value) == str:
        dict_cod_pessoas[aba_plantao['Codigo Pessoa'][index]] = value

for index, value in enumerate(aba_plantao['PESQUISADOR']):
    if value == NaN:
        aba_plantao['PESQUISADOR'].replace(index, dict_cod_pessoas[aba_plantao['Codigo Pessoa'][index]])
        #aba_plantao.loc[index,"PESQUISADOR"] = dict_cod_pessoas[aba_plantao['Codigo Pessoa'][index]]