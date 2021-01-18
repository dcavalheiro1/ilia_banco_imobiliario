#!/usr/bin/env python
# coding: utf-8

from numpy import random

class Propriedade:
    compra = 0
    aluguel = 0
    vendido = 0
    perfil = 0
    proprietario = -1

    def __init__(self, compra, aluguel):
        self.compra = compra
        self.aluguel = aluguel
        self.vendido = 0
        self.perfil = 0
        self.proprietario = -1

class Jogador:
    posicao = 0
    saldo = 0
    perfil = 0
    venceu = 0

    def __init__(self, perfil):
        self.perfil = perfil
        self.venceu = 0

# Montando os jogadores

jogadores = []

jogadores.append(Jogador(0)) # impulsivo
jogadores.append(Jogador(1)) # exigente
jogadores.append(Jogador(2)) # cauteloso
jogadores.append(Jogador(3)) # aleatorio

# Define a proxima posicao de propriedade no tabuleiro para um determinado jogador

def nova_posicao(posicao_atual, novo_valor):
    nova_posicao = posicao_atual + novo_valor
    
    if(nova_posicao >= 20):
        nova_posicao = nova_posicao - 20

    return nova_posicao

# Define se a compra  pode ser feita de acordo com o perfil de cada jogador e o saldo de que dispoe

def define_compra(perfil, compra, aluguel, saldo):
    if(perfil == 0):
        e_compra = 1
        saldo = saldo - compra
    elif(perfil == 1):
        if(aluguel > 50):
            saldo = saldo - compra
            e_compra = 1
        else:
            e_compra = 0
    elif(perfil == 2):
        if(saldo - compra > 80):
            saldo = saldo - compra
            e_compra = 1
        else:
            e_compra = 0
    elif(perfil == 3):
        escolha = random.randint(2)
        
        if(escolha == 1):
            saldo = saldo - compra
            e_compra = 1
        else:
            e_compra = 0
    return e_compra, saldo

# Define o valor do saldo quando se tem que pagar aluguel

def define_aluguel(aluguel, saldo):
    saldo = saldo - aluguel
    return saldo

# Construindo as propriedades do tabuleiro

# Assumindo que todas as propriedades custam 100 para venda e 30 para aluguel

propriedades = []

for i in range(0, 19):
    prop = Propriedade(100, 30)
    propriedades.append(prop)

# Distribuindo o saldo inicial aos jogadores

jogadores[0].saldo = 300
jogadores[1].saldo = 300
jogadores[2].saldo = 300
jogadores[3].saldo = 300

partidas_timeout = 0
partidas = []
jogadores_fora = 0
i = 0

# Admitindo que uma rodada comeca com o primeiro jogador e termina com o ultimo

N = 4000 # 1000 rodadas vezes 4 jogadores

# Falta considerar as 300 simulacoes

for i in range(N):
    index = i % 4
    
    # Verifica se o jogador ainda esta ativo
    
    if(jogadores[index].saldo < 0):
        continue

    # Joga o dado
    
    dado = random.randint(6) + 1
    
    # Encontra nova posicao para o jogador
    
    pos = nova_posicao(jogadores[index].posicao, dado)
    
    saldo_atual = jogadores[index].saldo
    
    # Verifica se a nova posicao ja foi vendida antes
    
    if(propriedades[pos].vendido == 0):
        e_compra, saldo = define_compra(jogadores[index].perfil, propriedades[pos].compra, propriedades[pos].aluguel, saldo_atual)
        if(e_compra == 1):
            # Compra a propriedade e desconta do saldo
      
            propriedades[pos].vendido = 1
            propriedades[pos].proprietario = jogadores[index].perfil
            propriedades[pos].perfil = jogadores[index].perfil
            jogadores[index].saldo = saldo

    # Se ja foi vendida, resta pagar aluguel ao proprietario
    
    else:        
        saldo = define_aluguel(propriedades[pos].aluguel, saldo_atual)
        jogadores[index].saldo = saldo
        jogadores[propriedades[pos].proprietario].saldo = jogadores[propriedades[pos].proprietario].saldo + propriedades[pos].aluguel
  
    # Se o saldo ficou negativo, o jogador sai do jogo e um contador incrementa de 1

    if(jogadores[index].saldo < 0):
        jogadores_fora = jogadores_fora + 1

        # Quando o numero de jogadores fora e 3, e porque ja temos o campeao
        
        if(jogadores_fora == 3):

            # Encontrar o campeao e increntar o contador de vitorias
            
            for jog in jogadores:
                if(jog.saldo > 0):
                    jog.venceu = jog.venceu + 1

                    # Falta contabilizar o numero de turnos desta partida para fazer uma media no final
            
            # Reiniciar propriedades e jogadores para a proxima partida
            
            for i in range(0, 19):
                prop = Propriedade(100, 30)
                propriedades[i] = prop
            
            jogadores[0].saldo = 300
            jogadores[1].saldo = 300
            jogadores[2].saldo = 300
            jogadores[3].saldo = 300
            
            jogadores_fora = 0
        
        # O jogador perdedor devolve suas propriedades para o jogo
        
        for prop in propriedades:
            if(prop.perfil == jogadores[index].perfil):
                prop.vendido = 0
                prop.proprietario = -1

# Estamos na 1000a rodada e, assim, atingiu-se o limite estabelecido para o timeout

if(i > N):
    partidas_timeout = partidas_timeout + 1

print("Foram", partidas_timeout, "partidas terminadas por timeout")

# Consolidar o resultado em termos percentuais para o numero de vitorias de cada jogador

total_vitorias = 0

for jog in jogadores:
    total_vitorias = total_vitorias + jog.venceu

a = jogadores[0].venceu
b = jogadores[1].venceu
c = jogadores[2].venceu
d = jogadores[3].venceu

print("Percentual de vitorias do impulsivo:", a * 100 / total_vitorias)
print("Percentual de vitorias do exigente: ", b * 100 / total_vitorias)
print("Percentual de vitorias do cauteloso:", c * 100 / total_vitorias)
print("Percentual de vitorias do aleatorio:", d * 100 / total_vitorias)

# Apontar o jogador que mais venceu de acordo com o numero de vitorias

if(a >= b and a >= c and a >= d):
    print("Quem mais venceu foi o impulsivo")
elif(b > a and b >= c and b >= d):
    print("Quem mais venceu foi o exigente")
elif(c > a and c > b and c >= d):
    print("Quem mais venceu foi o cauteloso")
elif(d > a and d > b and d > c):
    print("Quem mais venceu foi o aleatorio")
