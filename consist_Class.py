import pandas as pd
from datetime import datetime 
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class Consistencia():
#criando um datarame vazio para inserir os erros encontrados na base de dados
    def __init__(self):
        self.df_resultado = pd.DataFrame(columns = ['ID-SGC', 'ID-P', 'P', 'C1', 'Data da Entrevista', 
        'Entrevistador(a)', 'Cód. Questão', 'Rót. Questão', 'Erro']) 
#crianddo uma lista de colunas de interesse nas abas de pessoas e de propriedades. Mudar de  acordo com o proeto
        self.colunas_de_interesse = ['ID-SGC','C1', 'C2', '1.1.1'] 
        self.colunas_de_interesse_pessoas = ['ID-SGC', 'C1', 'C2', 'ID-P', 'P']

    def abrir_bases(self, arquivo):
        print("Iniciando...")
        print("Carregando aba de Propriedade...")
        self.dfpropriedade = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = "propriedade"))
        print("Carregando aba de Pessoas...")
        self.dfpessoas = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = "pessoas"))
        print("Tudo pronto!")

    def valida_missing_propriedades (self, df, value):
        missing_prop = []
        #checar misings na aba propriedades / retorna um df com valores boleanos True (caso encontre o valor procurao) or False (caso não encontre )
        checkprop = df.isin([value])
        #checando em quais colunas tem o valor procurado (missing)
        seriesObj = checkprop.any()
        #salvando em uma lista, o nome da coluna aonde foi encontrado o valor procurado
        colErrosProp = list(seriesObj[seriesObj == True].index)
        #looping para identificar o index aonde o valor procurado existe no dataframe e salvar em uma lista chamada linhas esta indicação
        for col in colErrosProp:
            rows = list(checkprop[col][checkprop[col] == True].index)
        #looping para pegar o IDSGC o dataframe de propriedades na linha aonde o valor procurado (missing) foi encontrado
        #e a coluna que o valor procurado está salvando em uma lista de tuplas com [('IDSGC', 'código da coluna'),('IDSGC', 'código da coluna')]
            for row in rows:
                missing_prop.append((self.dfpropriedade['ID-SGC'][row], self.dfpropriedade['C1'][row], self.dfpropriedade['1.1.1'][row],self.dfpropriedade['1.1.18'][row], col, value))
        #crindo um DF com as informações basicas da pesquisa (mudar a depender do projeto), código das colunas e a resposa erro inserida no campo "Value" da função
        self.errosprop = pd.DataFrame(data = missing_prop, columns= ['ID-SGC', 'Indexador', 'ID-SGS', 'Data da criação', 'Rótulo da Questão', 'Erro de resposta encontrado'])   
        return self.errosprop
    #Mesma coisa feita em propriedades
    def valida_missing_pessoas (self, df, value):
        missing_pess = []
        checkarpess = df.isin([value])
        seriesObjPess = checkarpess.any()
        colErrosPessoas = list(seriesObjPess[seriesObjPess == True].index)
        for col in colErrosPessoas:
            rows = list(checkarpess[col][checkarpess[col]==True].index)
            for row in rows:
                missing_pess.append((self.dfpessoas["ID-SGC"][row], self.dfpessoas["C1"][row], self.dfpessoas["ID-P"][row], self.dfpessoas["P"][row], col, value))
        self.errospess = pd.DataFrame(data = missing_pess, columns= ["ID-SGC", "Indexador", "ID Pessoa", "Pessoa", "Rótulo da Questão", "Erro de resposta encontrado"])
        return self.errospess

    #Validação de indexadores
    def Duplicidade_indexadores_na_Base (self, df):
    #Criei uma lista com o nome das colunas que eu quer dabase inteira, para esta validação
        colunas_procuradas = ["ID-SGC","C1", "1.1.1"]
    #pegei o mesmo df que criei e usei nas validações de missing
        df = self.dfpropriedade
        base_de_dados = pd.DataFrame(data = df, columns= colunas_procuradas)
    #Duplicated procura por valores duplicados com o referencial das ([colunas que se passa dentro do colchetes]), 
    #Por padrão preserva o primeiro valor e aponta os outros (keep='first') ou preserva o ultimo e aponta os anteriores (keep='last')
        self.duplicidade_indexador_BD_F2 = base_de_dados[base_de_dados.duplicated(["C1"], keep="first")]
        #self.duplicidade_indexador_BD_F2[["ID-P", "P", "2.2.6", "2.2.22.1.a"]] = "Não tem esses dados na aba de propriedades"
        self.duplicidade_indexador_BD_F2["Erro encontrado"] = "Indexador já existe - Duplicado"
        return self.duplicidade_indexador_BD_F2
    #procurando por cpf que ja existem na F1
    #esta função recebe 2 parâmetros, nome do arquivo primero e aba depois. Ambas, strings.

    def duplicidade_CPF_na_Base (self, df):
        #Criei uma lista com o nome das colunas que eu quer dabase inteira, para esta validação
        colunas_procuradas = ["ID-SGC","C1", "2.2.6"]
        #pegei o mesmo df que criei e usei nas validações de missing
        df = self.dfpessoas
        base_de_dados = pd.DataFrame(data = df, columns= colunas_procuradas)
        #Duplicated procura por valores duplicados com o referencial das ([colunas que se passa dentro do colchetes]), 
        #Por padrão preserva o primeiro valor e aponta os outros (keep='first') ou preserva o ultimo e aponta os anteriores (keep='last')
        self.duplicidade_cpf_BD_F2 = base_de_dados[base_de_dados.duplicated(["2.2.6"], keep="first")]
        #self.duplicidade_indexador_BD_F2[["ID-P", "P", "2.2.6", "2.2.22.1.a"]] = "Não tem esses dados na aba de propriedades"
        self.duplicidade_cpf_BD_F2["Erro encontrado"] = "CPF Duplicado"
        return self.duplicidade_cpf_BD_F2
    
    def indexador_Duplicado_F1xF2(self, arquivo, aba):
        indexador_F1 = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = f"{aba}"))
        series_indexador_F1 = list(indexador_F1["C1"])
        verifica_indexadores = self.dfpropriedade[self.dfpropriedade["C1"].isin(series_indexador_F1)]
        indexadores_Duplicados = verifica_indexadores[["ID-SGC", "C1", "1.1.1", "1.1.18"]]
        self.duplicidade_indexadorF1xF2 = pd.DataFrame(data = indexadores_Duplicados)
        self.duplicidade_indexadorF1xF2["Erro Encontrado"] = "Indexador encontrado na Fase 1 - Duplicado"
        return self.duplicidade_indexadorF1xF2
        
    def cpf_Duplicado_F1xF2(self, arquivo, aba):
        cpf_fase_1 = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = f"{aba}"))
        series_cpf_F1 = list(cpf_fase_1["CPF"])
        verifica_CPF = self.dfpessoas[self.dfpessoas["2.2.6"].isin(series_cpf_F1)]
        cpf_Duplicados = verifica_CPF[["ID-SGC","ID-P", "P", "2.2.6", "2.2.22.1.a"]]
        self.duplicidade_CPF_F1xF2 = pd.DataFrame(data = cpf_Duplicados)
        self.duplicidade_CPF_F1xF2["Erro Encontrado"] = "CPF encontrado na Fase 1 - Duplicado"
        return self.duplicidade_CPF_F1xF2

    def idsgc_DuplicadoF1xF2(self, arquivo, aba):
        idsgc_fase_1 = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = f"{aba}"))
        series_idsgc_F1 = list(idsgc_fase_1["ID-SGC"])
        verifica_IDSGC = self.dfpropriedade[self.dfpropriedade["ID-SGC"].isin(series_idsgc_F1)]
        idsgc_duplicados = verifica_IDSGC[["ID-SGC", "C1", "1.1.1", "1.1.18"]]
        self.df_IDGSC_dupliF1xF2 = pd.DataFrame(data = idsgc_duplicados)
        self.df_IDGSC_dupliF1xF2["Erro encontrado"] = "ID-SGC consta na Fase 1 - Duplicado"
        return self.df_IDGSC_dupliF1xF2
    
    def idsgs_DuplicadoF1xF2(self, arquivo, aba):
        idsgs_fase_1 = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = f"{aba}"))
        series_idsgs_F1 = list(idsgs_fase_1["ID SGS pessoa"])
        verifica_IDSGS = self.dfpessoas[self.dfpessoas["2.2.22.1.a"].isin(series_idsgs_F1)]
        idsgs_duplicados = verifica_IDSGS[["ID-SGC", "C1", "2.2.22.1.a", "C3"]]
        self.df_IDGSS_dupliF1xF2 = pd.DataFrame(data = idsgs_duplicados)
        self.df_IDGSS_dupliF1xF2["Erro encontrado"] = "Código Pessoa consta na Fase 1 - Duplicado"
        return self.df_IDGSS_dupliF1xF2
   
    def idsgs_Duplicado(self, arquivo, aba):
        idsgs_fase_1 = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = f"{aba}"))
        series_idsgs_F1 = list(idsgs_fase_1["ID SGS pessoa"])
        verifica_IDSGS = self.dfpessoas[self.dfpessoas["2.2.22.1.a"].isin(series_idsgs_F1)]
        idsgs_duplicados = verifica_IDSGS[["ID-SGC", "C1", "2.2.22.1.a", "C3"]]
        self.df_IDGSS_dupliF2 = pd.DataFrame(data = idsgs_duplicados)
        self.df_IDGSS_dupliF2["Erro encontrado"] = "Código Pessoa consta na Fase 1 - Duplicado"
        return self.df_IDGSS_dupliF2

    def valida_idsgc_propriedades_pessoas(self):
        x = 0
        resultado_Idsgcs_com_pesquisa_aplicada = []
        idsgc_n_abre_pessoas = []
        pesquisa_aplicada =self.dfpropriedade[["ID-SGC", "1.1.22"]]
        for i in pesquisa_aplicada["1.1.22"]:
                x+=1
                if i == "Não":
                        resultado_Idsgcs_com_pesquisa_aplicada.append(pesquisa_aplicada.loc[x-1,"ID-SGC"])

                if i == "Sim":
                        idsgc_n_abre_pessoas.append(pesquisa_aplicada.loc[x-1,"ID-SGC"])
        
        encontrados = self.dfpessoas.loc[self.dfpessoas["ID-SGC"].isin(resultado_Idsgcs_com_pesquisa_aplicada), "ID-SGC"].tolist()
        df_encontrados = pd.DataFrame(data = encontrados, columns= ["ID-SGC"])
        df_encontrados["STATUS"] = "ID-SGC CORRETO, ENCONTRADO"
        nao_encontrados = list(set(resultado_Idsgcs_com_pesquisa_aplicada) - set(encontrados))
        df_nao_encontrados= pd.DataFrame(data = nao_encontrados, columns= ["ID-SGC"])
        df_nao_encontrados["STATUS"] = "ID-SGC DEVERIA ESTAR EM PESSOAS MAS NÃO FOI ENCONTRADO"
        encontrados_n_deveria_abrir_pessoas = self.dfpessoas.loc[self.dfpessoas["ID-SGC"].isin(idsgc_n_abre_pessoas), "ID-SGC"].tolist()
        df_encontrados_n_deveria_abrir_pessoas = pd.DataFrame(data = encontrados_n_deveria_abrir_pessoas, columns= ["ID-SGC"])
        df_encontrados_n_deveria_abrir_pessoas["STATUS"] = "ID-SGC NÃO DEVERIA ESTAR EM PESSOAS"
        resultados_lista = [df_encontrados,df_nao_encontrados,df_encontrados_n_deveria_abrir_pessoas]
        resultado_idsgc_df = pd.concat(resultados_lista)
        return resultado_idsgc_df

    def planilha_Erros(self):
        hoje = dt.now().date()
        lista_dupli = [self.duplicidade_indexador_BD_F2, self.duplicidade_indexadorF1xF2, self.duplicidade_CPF_F1xF2, self.df_IDGSC_dupliF1xF2, self.df_IDGSS_dupliF1xF2, self.df_IDGSS_dupliF2]
        lista_mising = [self.errospess, self.errosprop]
        df_resultados_duplicidade = pd.concat(lista_dupli)
        df_resultado_missing = pd.concat(lista_mising)
        writer = pd.ExcelWriter(f'Consistência{hoje}.xlsx', engine='openpyxl')
        df_resultados_duplicidade.to_excel(writer, sheet_name='Erros de Duplicidade', index=False)
        df_resultado_missing.to_excel(writer, sheet_name='Missings Encontrados', index=False)
        writer.save()
    def valida_datas_nascmento(self):
        x = 0
        formato_data = "%d/%m/%Y"
        resultado_datas_para_validacao = {}
        listagem_Idsgcs_com_pesquisa_aplicada = []
        listagem_datas_com_pesquisa_aplicada = []
        pesquisa_aplicada =self.dfpropriedade[["ID-SGC","C1","1.1.1", "1.1.18", "1.1.22"]]
        pesquisa_aplicada
        for i in pesquisa_aplicada["1.1.22"]:
                x+=1
                if i == "Não":
                        listagem_Idsgcs_com_pesquisa_aplicada.append(pesquisa_aplicada.loc[x-1,"ID-SGC"])
                        listagem_datas_com_pesquisa_aplicada.append(pesquisa_aplicada.loc[x-1,"1.1.18"])
        datas_corrigidas = []
        for i in listagem_datas_com_pesquisa_aplicada:
                datas_formatadas = datetime.strptime(i,formato_data)
                datas_formatadas
                datas_corrigidas.append(datas_formatadas)
        resultado_datas_para_validacao = dict(zip(listagem_Idsgcs_com_pesquisa_aplicada, datas_corrigidas))
        lista_idsgc = []
        lista_indexador = []
        lista_idp = []
        lista_data_aniversário = []
        lista_idade = []
        datas_pessoas = []
        for i in self.dfpessoas["2.2.4"]:
                x+=1
                datas_pessoas.append(i)
                for i in datas_pessoas:
                        formatando_dt_pessoas = datetime.strptime(i,formato_data)
                        formatando_dt_pessoas
        for i in formatando_dt_pessoas:
        #transformar as datas de string para datetime no formato data_format
                if i > datetime.today:
                        lista_idsgc.append(self.dfpessoas.loc[x-1,"ID-SGC"])
                        lista_indexador.append(self.dfpessoas.loc[x-1,"C1"])
                        lista_idp.append(self.dfpessoas.loc[x-1,"ID-P"])
                        lista_data_aniversário.append(self.dfpessoas.loc[x-1,"2.2.4"])
                        lista_idade.append(self.dfpessoas.loc[x-1,"2.2.5"])
                df_data = [lista_idsgc, lista_indexador, lista_idp, lista_data_aniversário, lista_idade]
        df_datas_de_nasc_maior_que_data_da_entrevista = pd.DataFrame(data = df_data, columns= ["ID-SGC", "Indexador", "ID-Pessoa", "Data de Aniversário", "Idade Informada"])
        return df_datas_de_nasc_maior_que_data_da_entrevista
    

objeto = Consistencia()
#lerbase de pessoas e propridades
objeto.abrir_bases("BD_Teste")
#procurar os missings em propriedades 
objeto.valida_missing_propriedades(objeto.dfpropriedade, '[missing]')
#procurarmissings em pessoas
objeto.valida_missing_pessoas(objeto.dfpessoas, '[missing]')
#procurar indexadores duplicados na base
objeto.Duplicidade_indexadores_na_Base(objeto.dfpropriedade)
objeto.indexador_Duplicado_F1xF2("SGS_controle_fases", "Estrutura")
#validar se os cpf's da Fase 1 são diferentes dos cpf's da Fase 2 e apontar caso sejam iguais 
objeto.cpf_Duplicado_F1xF2("controle_pessoas", "Estrutura")                                                                                                                                                                                                                                                                                
objeto.idsgc_DuplicadoF1xF2("SGS_controle_fases", "Estrutura")
objeto.idsgs_DuplicadoF1xF2("controle_pessoas", "Estrutura")
objeto.idsgs_Duplicado("controle_pessoas", "Estrutura")
#objeto.data_de_nascimento_invalida()
objeto.duplicidade_CPF_na_Base(objeto.dfpessoas)
objeto.valida_idsgc_propriedades_pessoas()
objeto.planilha_Erros()
#Olhar as questões .a, validar respostas de complemento 