# Wothon MAteus de Araujo
# 12111BSI262
# CONCLUIDO DIA 05/11

from math import log
from math import sqrt
from os import remove, write
import nltk
import sys

if __name__ == "__main__":
    arq = open(sys.argv[1])
    linhas = arq.readlines() #le o arquivo e armazena as linhas

    arquivos = {}
    i = 0
    for linha in linhas:
        linha = [p for p in linha if p not in ("\n")] #tira o \n da separação das linhas
        linha = "".join(linha) #transforma em string
        arquivos[i] = linha

        i+=1

    arq.close() # fecha arquio base.txt

    str_arquivo = {}
    i = 0
    while i < len(linhas):
        str_arq = open(arquivos[i])
        str_arquivo[i] = str_arq.readlines()
        str_arquivo[i] = "".join(str_arquivo[i])
        str_arquivo[i] = str_arquivo[i].lower()
        str_arq.close()
        i = i + 1

    def limpaTexto(texto): # tira a pontuação e cria uma nova lista
        texto_filtrado_stopwords = []
        texto_filtrado_token = nltk.word_tokenize(texto)
        texto_filtrado = [p for p in texto_filtrado_token if p not in ("!", ".", ",", "?", "...")] #cria uma nova lista sem a pontuação
        texto_filtrado = [i for i in texto_filtrado if i not in nltk.corpus.stopwords.words("portuguese")]
        sentencas_etiquetadas = nltk.corpus.mac_morpho.tagged_sents()
        etiquetador_unigram = nltk.tag.UnigramTagger(sentencas_etiquetadas)
        classificação = etiquetador_unigram.tag(texto_filtrado)
        i = 0 
        while i < len(classificação):
            if classificação[i][1] not in ("PREP", "KC", "KS", "ART"):
                texto_filtrado_stopwords.append(classificação[i][0])
            i = i + 1

        texto_filtrado = texto_filtrado_stopwords
        stemmer = nltk.stem.RSLPStemmer()
        i = 0
        while i < len(texto_filtrado):
            texto_filtrado[i] = stemmer.stem(texto_filtrado[i])
            i = i + 1

        return texto_filtrado

    def contaCaracteres(texto):
        freqs = {} #dicionário vazio
        for c in texto:
            if c not in freqs: #verifica se c já é chave
                freqs[c] = 1
            else:
                freqs[c] = freqs[c] + 1
        return freqs

    str_arquivo_filtrado = {}
    i = 0
    while i < len(linhas):
        str_arquivo_filtrado[i] = limpaTexto(str_arquivo[i])
        i = i + 1

    palavras = set()
    #adicionar todas as palavras em um conjunto

    i = 0
    while i < len(linhas):
        for c in str_arquivo_filtrado[i]:
            if c not in palavras:
                palavras.add(c)
        i = i + 1

    palavras = sorted(palavras) # deixa o conjunto em ordem alfabética(ascii)

    indice = {}
    i = 0
    while i < len(linhas):
        indice[i + 1] = contaCaracteres(str_arquivo_filtrado[i]) #faz a contagem de vezes que a palavra apareceu na frase
        i = i + 1

    indice_invert = dict()
    indice_a_dict = dict()
    indice1 = set()
    indice2 = set()
    indice3 = set()

    j = 0
    for c in palavras: #for na lista das palavras criada em ordem ascii
        indice_invertido = []
        i = 1 #contador de indíce do dicionário
        while i <= len(indice): 
            if c in indice[i]: # se a palavra existe no indice imprime qual o indice e quantas vezes apareceu
                indice_invertido.append((i, indice[i][c]))
            i = i + 1
        indice_invert[c] = indice_invertido
        j = j + 1
    # Indice invertido --------------------------------------

    def calc_tfidf(qtd_Ki, termo):
        tf = 1 + log(qtd_Ki, 10) # calculo TF
        idf = log(len(linhas)/len(indice_invert[termo]), 10) # calculo IDF
        tfidf = tf * idf # calculo TFIDF
        return tfidf

    palavras_e_log = dict()
    
    # Calculando TFIDF
    i = 1
    while i <= len(linhas):
        log_por_indice = []
        for c in palavras:
            j = 0
            tfidf = 0
            t = 0
            while j < len(indice_invert[c]):
                if indice_invert[c][j][0] == i:
                    tfidf = calc_tfidf(indice_invert[c][j][1], c)
                    log_por_indice.append((c, tfidf)) # adiciona ao final da lista do indice
                    t = 1
                j = j + 1
            if t == 0:
                log_por_indice.append((c, tfidf))
        palavras_e_log[i] = log_por_indice # adiciona no dicionário com o número correspondente ao indice
        i = i + 1

    arquivo_pesos = open("pesos.txt", "w")
    i = 0
    while i < len(linhas):
        documento = linhas[i].strip()
        arquivo_pesos.write("{}:  " .format(documento))
        j = 0
        while j < len(palavras_e_log[i+1]):
            if palavras_e_log[i+1][j][1] != 0:    
                arquivo_pesos.write("{}, {:.4f}" .format(palavras_e_log[i+1][j][0], palavras_e_log[i+1][j][1])) 
                arquivo_pesos.write("   ")# adiciona TAB
            j = j + 1
        if i+1 != len(linhas):
            arquivo_pesos.write("\n")# adiciona ENTER
        i = i + 1
    arquivo_pesos.close()



    i = 1
    while i <= len(indice):
        indice_a = set()
        for c in palavras:
            if c in indice[i]:
                indice_a.add(c)
                
        indice_a_dict[i] = indice_a
        i = i + 1


    consulta = open(sys.argv[2]) # lê o arquivo 
    consulta_read = consulta.readline() #lê a linha do arquivo
    consulta_read = consulta_read.lower()
    consulta_read_filter = consulta_read.split() # separa a frase por palavra

    i = 0
    while i < len(consulta_read_filter):
            if consulta_read_filter[i][0] == '!' or consulta_read_filter[i].isalpha(): #identifica se é letra ou palavra negativa
                stemmer = nltk.stem.RSLPStemmer() #retira o radical da palavra
                consulta_read_filter[i] = stemmer.stem(consulta_read_filter[i]) #salva na variável
            i = i + 1


    consulta_read_filter_radical = " ".join(consulta_read_filter) # junta novamente a string já com o radical da palavra
    pesos_consulta = [p for p in consulta_read_filter if p.isalpha() or p[0] == "!"]
    palavras_e_log_consulta = dict()
   
    consulta_log = []
    i = 0
    while i < len(palavras):
        if palavras[i] in pesos_consulta:
            consulta_log = (palavras[i], calc_tfidf(pesos_consulta.count(palavras[i]), palavras[i]))
        else: 
            consulta_log = (palavras[i], 0)
        palavras_e_log_consulta[i] = consulta_log

        i = i + 1
    similiaridade = dict()

    raiz_consulta = 0
    soma_consulta = 0
    r = 0
    while r < len(palavras):
        soma_consulta = soma_consulta + (palavras_e_log_consulta[r][1] ** 2)
        raiz_consulta = sqrt(soma_consulta)
        r = r + 1

    i = 1
    while i <= len(linhas):
        j = 0
        soma_numerador = 0
        soma_denominador = 0
        result_denominador = 0
        while j < len(palavras):
            soma_numerador = soma_numerador + (palavras_e_log[i][j][1] * palavras_e_log_consulta[j][1])
            soma_denominador = soma_denominador + (palavras_e_log[i][j][1] ** 2)
            j = j + 1 
        
        raiz_doc = sqrt(soma_denominador)
        result_denominador = raiz_doc * raiz_consulta
        resultado_similiaridade = soma_numerador/result_denominador
        similiaridade[i] = resultado_similiaridade
        i = i + 1
        
    similiaridade_resposta = dict()

    i = 1 
    while i <= len(linhas):
        if similiaridade[i] >= 0.001:
            similiaridade_resposta[i] = (linhas[i-1].strip(), similiaridade[i])

        i = i + 1
    
    vetor_decrescente = sorted(similiaridade_resposta.items(), key=lambda kv: kv[1][1], reverse=True)
    # --------------------------------------------------
    # gerando arquivo 
    arquivo_resposta = open("resposta.txt", "w") #cria o arquivo
    arquivo_resposta.write("{}" .format(len(vetor_decrescente)))
    arquivo_resposta.write("\n")# adiciona ENTER
    i = 0
    while i < len(vetor_decrescente):
        arquivo_resposta.write("{}  {:.4f}" .format(vetor_decrescente[i][1][0], vetor_decrescente[i][1][1]))
        arquivo_resposta.write("\n")# adiciona ENTER
        i = i + 1
    arquivo_resposta.close() #fecha arquivo resposta.txt
else:
    print("Programa não está sendo executado como principal!")