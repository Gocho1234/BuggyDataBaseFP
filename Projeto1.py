# 103124 - Gonçalo Sampaio Bárias - goncalo.barias@tecnico.ulisboa.pt

##########################################################################
##                                                                      ##
##                         Buggy Data Base (BDB)                        ##
##                                                                      ##
##  Projeto 1 - Fundamentos da Programação 21/22                        ##
##  Licenciatura em Engenharia Informática e de Computadores (Alameda)  ##
##  Instituto Superior Técnico                                          ##
##                                                                      ##
##########################################################################


# ##### CORREÇÃO DA DOCUMENTAÇÃO ##### #


def corrigir_palavra(palavra):
    # corrigir_palavra: cad. carateres → cad. carateres
    """Corrige uma palavra, removendo todas as mutações indesejadas.
    
    Percorre a palavra até não haver mais mutações a remover.
    Devolve a palavra com todas as instâncias de letras minúsculas e maiúsculas 
    que entram em contacto (surto de palavras) removidas.
    Nunca gera erros.
    """
    letra, verifica_continuacao = 0, 'start'

    while verifica_continuacao != 'iddle':
        verifica_continuacao = 'iddle'
        while letra + 1 <= len(palavra) - 1:
            if letra >= 0 and palavra[letra] == palavra[letra + 1].swapcase():
                verifica_continuacao = 'run'
                palavra = palavra[:letra] + palavra[letra + 2:]
                letra -= 1
            else:
                letra += 1

        # A redução do contador "letra" é para acomodar casos como "bAaB",
        # removendo tudo de uma vez. 
        # Caso o contador se torne negativo ele faz "reset" para zero.

    return palavra


def eh_anagrama(palavra1, palavra2):
    # eh_anagrama: cad. carateres x cad. carateres → booleano
    """Determina se o segundo argumento é anagrama do primeiro.
    
    Recebe duas palavras e verifica se são anagramas uma da outra (palavras 
    iguais também são consideradas anagramas).
    Nunca gera erros.
    """
    palavra1, palavra2 = palavra1.lower(), palavra2.lower()

    return ''.join(sorted(palavra1)) == ''.join(sorted(palavra2))


def corrigir_doc(documento):
    # corrigir_doc: cad. carateres → cad. carateres
    """Corrige uma cadeia de carateres correspondente a um documento.
    
    Recebe uma cadeia de carateres correspondente a um documento, 
    corrige-o e remove todos os anagramas que correspondem a palavras distintas.
    Devolve um documento corrigido sem qualquer mutação indesejada.
    Cria um ValueError se o seu argumento for inválido. Argumento válido,
    neste caso, é considerado qualquer input que seja string não vazio,
    sem espaços no início e fim, nem dois espaços consecutivos e tenha somente 
    caracteres do alfabeto ou espaços.
    """
    if not (isinstance(documento, str) and documento != ''):
        raise ValueError('corrigir_doc: argumento invalido')

    if documento[0] == ' ' or documento[-1] == ' ':
        raise ValueError('corrigir_doc: argumento invalido')

    LETRAS_DOC = len(documento)
    for letra in range(LETRAS_DOC):
        if not (ord(documento[letra]) == 32 
                or 97 <= ord(documento[letra].lower()) <= 122):
            raise ValueError('corrigir_doc: argumento invalido')

        if (letra + 1 <= LETRAS_DOC - 1 
            and documento[letra + 1] == documento[letra] == ' '):
            raise ValueError('corrigir_doc: argumento invalido')

    palavras = documento.split(' ')

    for palavra in range(len(palavras)):
        palavras[palavra] = corrigir_palavra(palavras[palavra])

    i = 0
    while i < len(palavras):
        for j in range(len(palavras) - 1, i, -1):
            if (palavras[i].lower() != palavras[j].lower()
                and eh_anagrama(palavras[i], palavras[j])):
                del palavras[j]
        i += 1

        # Este ciclo fixa uma dada palavra do documento corrigida e compara-a com
        # todas as outras palavras que ainda não foram comparadas com ela. Caso a
        # segunda palavra seja anagrama da primeira, esta é removida.
            
    documento = ' '.join(palavras)

    return documento


# ##### DESCOBERTA DO PIN ##### #


def obter_posicao(movimento, posicao):
    # obter_posicao: cad. carateres x inteiro → inteiro
    """Realiza um único movimento do teclado e retorna o dígito da posição final.
    
    Recebe um movimento a realizar (Cima, Baixo, Direita ou Esquerda) e um dígito 
    de onde ele inicia esse movimento. O teclado é representado através da constante
    "TECLADO", que é um tuplo em que cada uma das 3 entradas tem um tuplo com 3 
    entradas, que representam linhas do teclado.
    Devolve o dígito do teclado após o movimento.
    Nunca gera erros.
    """
    TECLADO = ((1, 2, 3),
               (4, 5, 6),
               (7, 8, 9))

    if 1 <= posicao <= 3:
        linha = 0
        posicao -= 1
    elif 4 <= posicao <= 6:
        linha = 1
        posicao -= 4
    elif 7 <= posicao <= 9:
        linha = 2
        posicao -= 7

    LIMITES_DO_TECLADO = {'C': linha == 0, 
                          'B': linha == 2, 
                          'D': posicao == 2, 
                          'E': posicao == 0}

    if LIMITES_DO_TECLADO[movimento]:
        pass
    elif movimento == 'C':
        linha -= 1
    elif movimento == 'B':
        linha += 1
    elif movimento == 'D':
        posicao += 1
    elif movimento == 'E':
        posicao -= 1

    return TECLADO[linha] [posicao]


def obter_digito(movimentos, posicao):
    # obter_digito: cad. carateres x inteiro → inteiro
    """Obtém um dígito após a realização de uma cadeia de movimentos no teclado.
    
    Recebe uma cadeia de movimentos a realizar no teclado.
    Devolve o dígito após esses movimentos terem sido efetuados, partindo do 
    dígito representado pelo seu segundo argumento.
    Nunca gera erros.
    """
    movimentos = list(movimentos)
    
    for movimento in movimentos:
        movimento = obter_posicao(movimento, posicao)
        posicao = movimento
    
    return posicao


def obter_pin(pin):
    # obter_pin: tuplo → tuplo
    """Obtém o pin associado ao seu primeiro argumento.
    
    Recebe um pin com vários movimentos para cada dígito do pin.
    Devolve o pin associado a esses movimentos, começando sempre pelo dígito 
    5 no teclado para o primeiro algarismo do pin. Cada algarismo seguinte inicia
    no teclado o movimento, partindo do algarismo anterior no pin.
    Cria um ValueError se o seu argumento for inválido. Para argumentos válidos, são 
    considerados tuplos com 4 a 10 entradas, em que cada entrada contém movimentos
    válidos para obter um algarismo para o pin.
    """
    if not (isinstance(pin, tuple) and 4 <= len(pin) <= 10):
        raise ValueError('obter_pin: argumento invalido')

    COMP_PIN = len(pin)
    digito_antigo = 5
    for movimentos in range(COMP_PIN):
        if pin[movimentos] == '': raise ValueError('obter_pin: argumento invalido')
        
        for movimento in pin[movimentos]:
            if not 66 <= ord(movimento) <= 69:
                raise ValueError('obter_pin: argumento invalido')

        digito = obter_digito(pin[movimentos], digito_antigo)
        pin = pin[:movimentos] + (digito,) + pin[movimentos + 1:]
        digito_antigo = digito

    return pin


# ##### VERIFICAÇÂO DE DADOS ##### #


def eh_entrada(u):
    # eh_entrada: universal → booleano
    """Verifica se o seu input é uma entrada BDB válida.
    
    Recebe qualquer input e inicialmente verifica se é um tuplo com 3 entradas
    e depois vai verificar a validade da cifra, checksum e sequência de segurança.
    Nunca gera erros.
    """
    def cifra(x):
        # cifra: cad. carateres → booleano
        """Verifica se a cifra de uma entrada BDB é válida.
        
        Verifica se o seu argumento é do tipo string não vazio, contendo apenas
        letras minúsculas do alfabeto e/ou o hífen ("-"). Posto isto, também 
        verifica se o seu argumento apenas contém hífens separando os conjuntos de 
        carateres.
        Nunca gere erros.
        """
        COMP_CIFRA = len(x)
        if not isinstance(x, str) or x == '' or x[-1] == '-' or x[0] == '-':
            return False

        for letra in range(COMP_CIFRA):
            if not (ord(x[letra]) == 45 or 97 <= ord(x[letra]) <= 122):
                return False
            
            if letra != len(x) - 1 and x[letra] == x[letra + 1] == '-':
                return False
        
        return True

    def checksum(y):
        # checksum: cad. carateres → booleano
        """Verifica se o checksum de uma entrada BDB é válida.
        
        Verifica se o seu argumento é um checksum válido, sendo apenas considerado 
        como tal, caso seja uma string que contém letras minúsculas do alfabeto
        encapsuladas por parênteses retos, tendo um comprimento de exatamente
        7 carateres.
        Nunca gere erros.
        """
        COMP_CHECKSUM = 7
        if not (isinstance(y, str) and y != ''):
            return False

        if not (y[0] == '[' and y[-1] == ']' and len(y) == COMP_CHECKSUM):
            return False

        for letra in range(1, COMP_CHECKSUM - 1):
            if not 97 <= ord(y[letra]) <= 122:
                return False
        
        return True

    def seq_seguranca(z):
        # seq_seguranca: tuplo → booleano
        """Verifica se a sequência de segurança de uma entrada BDB é válida.
        
        Verifica se o seu argumento corresponde a uma sequência de segurança 
        válida, ou seja, o seu argumento tem de ser um tuplo, com pelo menos dois 
        números inteiros positivos.
        Nunca gere erros.
        """
        if not (isinstance(z, tuple) and len(z) >= 2):
            return False
        
        for num in z:
            if not (isinstance(num, int) and num > 0):
                return False
        
        return True

    return (isinstance(u, tuple) and len(u) == 3 
            and cifra(u[0]) and checksum(u[1]) and seq_seguranca(u[2]))


def validar_cifra(cifra, checksum):
    # validar_cifra: cad. carateres x cad. carateres → booleano
    """Valida se numa entrada BDB a cifra é coerente com o checksum.
    
    Recebe como primeiro argumento uma cifra e como segundo argumento um checksum. 
    Posto isto, a rotina guarda o número de ocorrências de cada letra diferente 
    num dicionário. Por fim cria a checksum coerente com essa cifra e verifica 
    se é igual à checksum real.
    Nunca gera erros.
    """
    letras, ocorrencias = cifra.replace('-', ''), {}
    for letra in letras:
        if letra not in ocorrencias:
            ocorrencias[letra] = 1
        else:
            ocorrencias[letra] += 1

    letras = [letra for letra in ocorrencias]
    letras.sort()
    top_ocorrencias = [ocorrencias[letra] for letra in ocorrencias]
    top_ocorrencias.sort(reverse = True)
        # Separa as letras e as suas ocorrências em duas listas diferentes. Depois
        # organiza a lista das letras por ordem alfabética e a lista das 
        # ocorrências por ordem decrescente.

    verificar_controlo = ''
    for ocorrencia in top_ocorrencias:
        for letra in letras:
            if (len(verificar_controlo) < 5 and letra not in verificar_controlo 
                and ocorrencias[letra] == ocorrencia):
                verificar_controlo += letra
    
    return ('[' + verificar_controlo + ']') == checksum


def filtrar_bdb(entradas_bdb):
    # filtrar_bdb: lista → lista
    """Filtra uma lista, removendo as entradas BDB corretas.
    
    A função verifica cada instância da lista que recebe e filtra todas as 
    entradas consideradas corretas pela função "eh_entrada" e depois devolve 
    uma lista somente com as entradas BDB incorretas.
    Cria um ValueError se o seu argumento for inválido. Um argumento válido é 
    considerado uma lista não vazia em que cada entrada BDB é válida.
    """
    if not (isinstance(entradas_bdb, list) and entradas_bdb != []):
        raise ValueError('filtrar_bdb: argumento invalido')

    COMP_ENTRADAS_BDB = len(entradas_bdb)
    for entrada in range(COMP_ENTRADAS_BDB - 1, -1, -1):
        if not eh_entrada(entradas_bdb[entrada]):
            raise ValueError('filtrar_bdb: argumento invalido')

        if validar_cifra(entradas_bdb[entrada] [0], entradas_bdb[entrada] [1]):
            entradas_bdb.remove(entradas_bdb[entrada])

    return entradas_bdb


# ##### DESENCRIPTAÇÃO DE DADOS ##### #


def obter_num_seguranca(seq_seguranca):
    # obter_num_seguranca: tuplo → inteiro
    """Calcula o número de segurança de uma determinada sequência de segurança
    
    Esta rotina faz a diferença entre todos os números da sequência de segurança, 
    guardando essas diferenças numa lista que no final é organizada de modo a 
    que valor da menor diferença esteja em primeiro lugar.
    Devolve no final essa menor diferença.
    Nunca gera erros.
    """
    COMP_SEQ_SEQURANCA = len(seq_seguranca)
    diferencas = []

    for j in range(COMP_SEQ_SEQURANCA):
        for i in range(j + 1, COMP_SEQ_SEQURANCA):
            diferencas.append(abs(seq_seguranca[j] - seq_seguranca[i]))
    
    diferencas.sort()
  
    return diferencas[0]


def decifrar_texto(cifra, int):
    # decifrar_texto: cad. carateres x inteiro → cad. carateres
    """Decifra uma cifra, dependendo do número de segurança.
    
    Esta rotina recebe uma cifra de troca e decifra-a. A maneira que a rotina 
    decifra as letras é através do número de segurança correspondente ao segundo 
    argumento e depois o valor real dessa letra depende se esta se encontra numa 
    posição par ou ímpar na string do texto.
    Nunca gera erros.
    """
    texto = [' ' if x == '-' else x for x in cifra]
    COMP_TEXTO = len(texto)

    for letra in range(COMP_TEXTO):
        if texto[letra] != ' ':
            if letra % 2 == 0:
                texto[letra] = chr((ord(texto[letra]) - 97 + (int + 1)) % 26 + 97)
            else:
                texto[letra] = chr((ord(texto[letra]) - 97 + (int - 1)) % 26 + 97)
        
        # A subtração por 97 é para ter as letras organizadas de 0 a 25, fazer as
        # mudanças e depois voltar a adicionar 97. Isto para poder fazer o resto
        # da divisão por 26 após a adição do número inteiro, obtendo a letra desejada.

    texto = ''.join(texto)

    return texto


def decifrar_bdb(entradas):
    # decifrar_bdb: lista → lista
    """Decifra todas as entradas BDB numa determinada lista.
    
    Recebe uma lista com várias entradas BDB e vai decifrando as cifras de cada 
    entrada, utilizando as funções já definidas, mostrando no final uma lista 
    com todas as entradas BDB válidas devidamente decifradas.
    Cria um ValueError caso o seu argumento se encontre inválido. Um argumento 
    válido, neste caso, tem de ser uma lista não vazia, que contenha pelo menos
    um tuplo com 3 ou mais entradas cada um.
    """
    if not (isinstance(entradas, list) and entradas != []):
        raise ValueError('decifrar_bdb: argumento invalido')
    
    COMP_ENTRADAS = len(entradas)
    for entrada in range(COMP_ENTRADAS):
        if not (isinstance(entradas[entrada], tuple) 
                and len(entradas[entrada]) >= 3):
            raise ValueError('decifrar_bdb: argumento invalido')
        
        num_seguranca = obter_num_seguranca(entradas[entrada] [2])
        entradas[entrada] = decifrar_texto(entradas[entrada] [0], num_seguranca)
            # Usa as rotinas já definidas para obter o número de segurança e
            # utiliza-o para corrigir cada cifra das entradas.
    
    return entradas


# ##### DEPURAÇÃO DE SENHAS ##### #


def eh_utilizador(u):
    # eh_utilizador: universal → booleano
    """Verifica se o seu input corresponde a utilizador válido.
    
    Esta rotina verifica se o seu argumento é válido de acordo
    com as regras estabelecidas.
    Nunca gera erros.
    """
    if not (isinstance(u, dict) and len(u) == 3):
        return False

    if not ('name' in u and 'pass' in u and 'rule' in u):
        return False
    
    # Verifica se o argumento principal é um dicionário com 3 entradas
    # ('name', 'pass' e 'rule').

    if not (isinstance(u['name'], str) and len(u['name']) >= 1):
        return False

    if not (isinstance(u['pass'], str) and len(u['pass']) >= 1):
        return False

    if not (isinstance(u['rule'], dict) and len(u['rule']) == 2):
        return False
    
    # Verifica se o tipo de cada key é o correto e se cada um está construído
    # corretamente.

    if not (isinstance(u['rule'] ['vals'], tuple)):
        return False

    if not (len(u['rule'] ['vals']) == 2):
        return False

    if not (isinstance(u['rule'] ['vals'] [0], int)):
        return False

    if not (isinstance(u['rule'] ['vals'] [1], int)):
        return False

    if not (u['rule'] ['vals'] [1] >= u['rule'] ['vals'] [0] > 0):
        return False
    
    # Verifica se os argumentos dentro de "rule" em "vals" estão corretos, ou seja,
    # se este último é igual a um tuplo com números inteiros em que o segundo é
    # maior que o primeiro.

    if not (isinstance(u['rule'] ['char'], str)):
        return False

    if not (len(u['rule'] ['char']) == 1):
        return False
    
    # Verifica se o argumento de "char" dentro de "rule" está de acordo com o
    # pedido.

    return True


def eh_senha_valida(senha, regra):
    # eh_senha_valida: cad. carateres x dicionário → booleano
    """Verifica se uma senha é válida, tendo em consideração a sua regra.
    
    A rotina verifica se a senha tem pelo menos 3 vogais, 2 carateres iguais 
    consecutivamente e o carater especial um número de vezes que esteja dentro 
    do intervalo de valores da regra.
    Nunca gera erros.
    """
    VOGAIS = ['a', 'e', 'i', 'o', 'u']
    INTERVALO_VALORES = range(regra['vals'] [0], regra['vals'] [1] + 1)
    vogal, consecutivo, verifica_regra, prev_letra = 0, 1, 0, ''

    for letra in senha:
        if letra in VOGAIS: vogal += 1

        if letra == prev_letra: consecutivo += 1
        prev_letra = letra

        if letra == regra['char']: verifica_regra += 1

    return vogal >= 3 and consecutivo >= 2 and verifica_regra in INTERVALO_VALORES


def filtrar_senhas(utilizadores):
    # filtrar_senhas: lista → lista
    """Mostra somente os utilizadores com senhas incorretas.
    
    Esta rotina verifica cada elemento de uma lista com vários utilizadores
    e elimina todos os utilizadores com senhas válidas e no final retorna uma lista
    com os nomes dos indivíduos com senhas incorretas por ordem alfabética, ignorando
    maiúsculas e minúsculas.
    Cria um ValueError caso o seu argumento se encontre inválido. Um argumento 
    válido tem de ser uma lista não vazia, que contém um ou mais dicionários.
    """
    if not (isinstance(utilizadores, list) and utilizadores != []):
        raise ValueError('filtrar_senhas: argumento invalido')
    
    for utilizador in utilizadores:
        if not isinstance(utilizador, dict):
            raise ValueError('filtrar_senhas: argumento invalido')

        if eh_senha_valida(utilizador['pass'], utilizador['rule']): 
            utilizadores.remove(utilizador)
    
    utilizadores = [utilizador['name'] for utilizador in utilizadores]
    utilizadores.sort(key = str.casefold)

    return utilizadores