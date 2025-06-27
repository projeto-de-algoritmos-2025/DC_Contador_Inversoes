import pygame
import random
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 1200
ALTURA = 800
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Organizador de Caos - Contagem de Inversões")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (70, 130, 180)
VERDE = (50, 205, 50)
VERMELHO = (220, 20, 60)
AMARELO = (255, 215, 0)
CINZA = (128, 128, 128)
ROXO = (138, 43, 226)
LARANJA = (255, 165, 0)
AZUL_CLARO = (173, 216, 230)
VERDE_CLARO = (144, 238, 144)

# Fontes
FONTE_GRANDE = pygame.font.Font(None, 48)
FONTE_MEDIA = pygame.font.Font(None, 36)
FONTE_PEQUENA = pygame.font.Font(None, 24)
FONTE_MUITO_PEQUENA = pygame.font.Font(None, 18)

class ContadorInversoes:
    """Classe para contar inversões usando merge sort modificado"""
    
    @staticmethod
    def merge_sort_e_conta_com_passos(arr, profundidade=0, posicao_inicial=0):
        """Merge sort que conta inversões e captura todos os passos para visualização"""
        passos = []
        
        def merge_sort_recursivo(arr_local, prof, pos_inicial):
            if len(arr_local) <= 1:
                return arr_local, 0, []
            
            meio = len(arr_local) // 2
            esquerda = arr_local[:meio]
            direita = arr_local[meio:]
            
            # Registra a divisão
            passo_divisao = {
                'tipo': 'divisao',
                'array': arr_local.copy(),
                'esquerda': esquerda.copy(),
                'direita': direita.copy(),
                'profundidade': prof,
                'posicao': pos_inicial
            }
            passos_locais = [passo_divisao]
            
            # Recursão para as metades
            esq_ordenada, inv_esq, passos_esq = merge_sort_recursivo(esquerda, prof + 1, pos_inicial)
            dir_ordenada, inv_dir, passos_dir = merge_sort_recursivo(direita, prof + 1, pos_inicial + meio)
            
            # Merge das duas metades
            resultado, inv_split, passos_merge = ContadorInversoes.merge_e_conta_com_passos(
                esq_ordenada, dir_ordenada, prof, pos_inicial
            )
            
            # Combina todos os passos
            passos_locais.extend(passos_esq)
            passos_locais.extend(passos_dir)
            passos_locais.extend(passos_merge)
            
            return resultado, inv_esq + inv_dir + inv_split, passos_locais
        
        resultado_final, inversoes_total, todos_passos = merge_sort_recursivo(arr, profundidade, posicao_inicial)
        return resultado_final, inversoes_total, todos_passos
    
    @staticmethod
    def merge_e_conta_com_passos(esquerda, direita, profundidade, posicao):
        """Merge que conta inversões e registra os passos"""
        resultado = []
        inversoes = 0
        i = j = 0
        passos_merge = []
        
        # Estado inicial do merge
        passo_inicial = {
            'tipo': 'merge_inicio',
            'esquerda': esquerda.copy(),
            'direita': direita.copy(),
            'profundidade': profundidade,
            'posicao': posicao
        }
        passos_merge.append(passo_inicial)
        
        comparacoes = []
        
        while i < len(esquerda) and j < len(direita):
            comparacao = {
                'elemento_esq': esquerda[i],
                'elemento_dir': direita[j],
                'posicao_esq': i,
                'posicao_dir': j
            }
            
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                comparacao['escolhido'] = 'esquerda'
                comparacao['inversoes_adicionadas'] = 0
                i += 1
            else:
                resultado.append(direita[j])
                comparacao['escolhido'] = 'direita'
                comparacao['inversoes_adicionadas'] = len(esquerda) - i
                inversoes += len(esquerda) - i
                j += 1
            
            comparacoes.append(comparacao)
        
        # Adiciona elementos restantes
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        # Passo final do merge
        passo_final = {
            'tipo': 'merge_fim',
            'resultado': resultado.copy(),
            'inversoes': inversoes,
            'comparacoes': comparacoes,
            'profundidade': profundidade,
            'posicao': posicao
        }
        passos_merge.append(passo_final)
        
        return resultado, inversoes, passos_merge
   