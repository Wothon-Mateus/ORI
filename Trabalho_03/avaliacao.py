# Wothon Mateus de Araujo 12111BS1262
# Conclusão : 25/11/2023


import matplotlib.pyplot as plt
import sys
import copy

if __name__ == "__main__":
    
    # Verifica se o nome do arquivo de entrada foi fornecido como argumento
    if len(sys.argv) < 2:
        print("Erro: Forneça o nome do arquivo de entrada como argumento.")
        sys.exit(1)
        
    arq = open(sys.argv[1])
    arq_linhas = arq.readlines()

    arquivos = {}
    i = 0
    for linha in arq_linhas:
        linha = [p for p in linha if p not in ("\n")] #tira o \n da separação das linhas
        linha = "".join(linha) #transforma em string
        arquivos[i] = linha.split(" ") #coloca em lista separando pelos espaços
        i+=1

    qtd_consultas = int(arquivos[0][0]) # pega a primeira linha do arquivo e passa para inteiro(estava string) e determina a quantidade de consultas referências

    res_ideal = {}
    res_sistema = {}
    i = 0
    while i < qtd_consultas:
        res_ideal[i] = arquivos[i+1] # coloca os arquivos da resposta ideal em um dicionário só
        res_sistema[i] = arquivos[i+1+qtd_consultas] # coloca os arquivos do sistema em um dicionário só
        i = i + 1


    def precisao(consulta_sistema, consulta_ideal): # função para retornar a precisão
        contem = [] # salva documentos que estão nos ideais
        precisão = dict() # salva as precisões calculadas
        i = 0
        while i < len(consulta_sistema): # passa por toda a consulta solicitada um por um
            if consulta_sistema[i] in consulta_ideal: # se o documento estiver na consulta dos ideais acontece a condição
                contem.append(consulta_sistema[i]) #adiciona para manter controle e ser utilizado na conta de precisão      
                revocação = (len(contem)/len(consulta_ideal)) * 100
                prec = (len(contem)/(i+1)) * 100 # adiciona a lista de precisões, já calculado e arredondado
                precisão[len(contem) - 1] = [(revocação), (prec)]
            i = i + 1
        return precisão # retorna a lista

    def maior(valor_revocacao, precisao):
        i = 0
        a = {}
        prec = []
        a = copy.deepcopy(precisao)
        while i < len(precisao):
            if valor_revocacao > a[i][0]:
                del a[i]
            else:
                prec.append(a[i][1])              
            i = i + 1

        if len(a) > 0:
            teste = max(prec)
            return teste
        else: 
            return 0
        
    def media(precisoes, qtd_consulta):
        soma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0 
        while i < len(precisoes):
            j = 0
            while j < len(precisoes[i]):
                soma[j] = soma[j] + precisoes[i][j]
                j = j + 1
            i = i + 1

        media_consultas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        while i < len(soma):
            if ((soma[i]/qtd_consulta)) == 0:
                media_consultas[i] = int(soma[i]/qtd_consulta)
            else:
                media_consultas[i] = float("{:.2f}".format((soma[i]/qtd_consulta)/100))
            i = i + 1

        return media_consultas

    i = 0
    precisões = dict() # cria dicionário para salvar as precisões de todas as consultas feitas
    while i < qtd_consultas: 
        precisões[i] = precisao(res_sistema[i], res_ideal[i]) # chama a função para o calculo da precisão
        i = i + 1

    revocacao_padrão = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    precisao_revocacao_padrao = dict()
    i = 0
    while i < qtd_consultas:
        maior_prec = []
        for x in revocacao_padrão:
            maior_prec.append(maior(x, precisões[i]))
        precisao_revocacao_padrao[i] = maior_prec
        i = i + 1
    
    media_consultas = media(precisao_revocacao_padrao, qtd_consultas)
    
    arquivo_media = open("media.txt", "w")
    i = 0
    while i < len(media_consultas):
        arquivo_media.write("{} " .format(media_consultas[i]))
        i = i + 1

    i = 0
    while i < len(precisao_revocacao_padrao):
        plt.plot(revocacao_padrão, precisao_revocacao_padrao[i]) #gráfico consultas
        plt.show()
        i = i + 1

    #gráfico média
    plt.plot(revocacao_padrão, media_consultas)
    plt.show()