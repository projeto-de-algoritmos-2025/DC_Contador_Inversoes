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
    
    @staticmethod
    def merge_sort_e_conta(arr):
        """Versão original para compatibilidade"""
        if len(arr) <= 1:
            return arr, 0
        
        meio = len(arr) // 2
        esquerda, inv_esq = ContadorInversoes.merge_sort_e_conta(arr[:meio])
        direita, inv_dir = ContadorInversoes.merge_sort_e_conta(arr[meio:])
        
        resultado, inv_split = ContadorInversoes.merge_e_conta(esquerda, direita)
        
        return resultado, inv_esq + inv_dir + inv_split
    
    @staticmethod
    def merge_e_conta(esquerda, direita):
        """Versão original para compatibilidade"""
        resultado = []
        inversoes = 0
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                inversoes += len(esquerda) - i
                j += 1
        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado, inversoes

class ElementoNumero:
    """Classe para representar um número na sequência"""
    
    def __init__(self, valor, posicao, largura, altura):
        self.valor = valor
        self.posicao_inicial = posicao
        self.posicao_atual = posicao
        self.largura = largura
        self.altura = altura
        self.selecionado = False
        self.animando = False
        self.target_pos = posicao
        
    def desenhar(self, tela, x, y, cor_customizada=None):
        """Desenha o elemento na tela"""
        if cor_customizada:
            cor = cor_customizada
        else:
            cor = AMARELO if self.selecionado else AZUL
            if self.animando:
                cor = VERDE
            
        # Desenha o retângulo
        pygame.draw.rect(tela, cor, (x, y, self.largura, self.altura))
        pygame.draw.rect(tela, PRETO, (x, y, self.largura, self.altura), 2)
        
        # Desenha o número
        texto = FONTE_MEDIA.render(str(self.valor), True, BRANCO)
        texto_rect = texto.get_rect(center=(x + self.largura//2, y + self.altura//2))
        tela.blit(texto, texto_rect)
    
    def contem_ponto(self, x, y, pos_x, pos_y):
        """Verifica se um ponto está dentro do elemento"""
        return (pos_x <= x <= pos_x + self.largura and 
                pos_y <= y <= pos_y + self.altura)

class JogoOrganizadorCaos:
    """Classe principal do jogo"""
    
    def __init__(self):
        self.modo_dificuldade = "FACIL"  # FACIL, MEDIO, DIFICIL, CUSTOM
        self.configuracoes_dificuldade = {
            "FACIL": {"tamanho": 6, "movimentos": 20, "multiplicador": 1.0},
            "MEDIO": {"tamanho": 8, "movimentos": 15, "multiplicador": 1.5},
            "DIFICIL": {"tamanho": 10, "movimentos": 12, "multiplicador": 2.0},
            "CUSTOM": {"tamanho": 0, "movimentos": 0, "multiplicador": 1.0}
        }
        
        self.sequencia_customizada = []
        self.entrada_texto = ""
        self.texto_ativo = False
        self.passos_solucao = []
        self.passo_atual_solucao = 0
        self.mostrar_solucao = False
        
        self.reset_jogo()
        self.tela_atual = "MENU"  # MENU, CUSTOM, JOGO, RESULTADO, SOLUCAO
        
    def reset_jogo(self):
        """Reinicia o jogo com base na dificuldade atual"""
        if self.modo_dificuldade == "CUSTOM" and self.sequencia_customizada:
            self.sequencia_original = self.sequencia_customizada.copy()
            self.tamanho_sequencia = len(self.sequencia_customizada)
            # Movimentos baseados no tamanho da sequência customizada
            self.movimentos_restantes = max(10, self.tamanho_sequencia * 2)
        else:
            config = self.configuracoes_dificuldade[self.modo_dificuldade]
            self.tamanho_sequencia = config["tamanho"]
            self.movimentos_restantes = config["movimentos"]
            
            # Gera sequência desordenada
            self.sequencia_original = list(range(1, self.tamanho_sequencia + 1))
            random.shuffle(self.sequencia_original)
        
        self.sequencia_atual = self.sequencia_original.copy()
        self.movimentos_usados = 0
        
        # Calcula inversões iniciais e passos da solução
        _, self.inversoes_iniciais = ContadorInversoes.merge_sort_e_conta(self.sequencia_atual.copy())
        self.inversoes_atuais = self.inversoes_iniciais
        
        # Gera solução completa
        _, _, self.passos_solucao = ContadorInversoes.merge_sort_e_conta_com_passos(self.sequencia_original.copy())
        self.passo_atual_solucao = 0
        self.mostrar_solucao = False
        
        # Cria elementos visuais
        self.criar_elementos()
        
        self.elemento_selecionado = None
        self.jogo_terminado = False
        self.pontuacao = 0
        
    def criar_elementos(self):
        """Cria os elementos visuais da sequência"""
        self.elementos = []
        largura_elemento = min(80, (LARGURA - 200) // max(1, self.tamanho_sequencia))
        altura_elemento = 60
        espacamento = 5
        
        for i, valor in enumerate(self.sequencia_atual):
            elemento = ElementoNumero(valor, i, largura_elemento, altura_elemento)
            self.elementos.append(elemento)
    
    def processar_entrada_customizada(self, texto):
        """Processa a entrada de números customizados"""
        try:
            # Remove espaços e separa por vírgula
            numeros_str = [n.strip() for n in texto.split(',') if n.strip()]
            numeros = [int(n) for n in numeros_str]
            
            # Validações
            if len(numeros) < 2:
                return False, "Digite pelo menos 2 números"
            if len(numeros) > 15:
                return False, "Máximo de 15 números"
            if len(set(numeros)) != len(numeros):
                return False, "Números devem ser únicos"
                
            self.sequencia_customizada = numeros
            return True, "Sequência válida!"
            
        except ValueError:
            return False, "Digite apenas números inteiros separados por vírgula"
    
    def atualizar_inversoes(self):
        """Atualiza o número de inversões da sequência atual"""
        _, self.inversoes_atuais = ContadorInversoes.merge_sort_e_conta(self.sequencia_atual.copy())
        
    def calcular_pontuacao(self):
        """Calcula a pontuação baseada nas inversões e eficiência"""
        if self.inversoes_iniciais == 0:
            return 1000
            
        # Percentual de redução de inversões
        reducao_inversoes = max(0, (self.inversoes_iniciais - self.inversoes_atuais) / self.inversoes_iniciais)
        
        # Eficiência dos movimentos (penaliza uso excessivo)
        eficiencia = max(0.1, 1 - (self.movimentos_usados / (self.movimentos_restantes + self.movimentos_usados)))
        
        # Multiplicador por dificuldade
        multiplicador = self.configuracoes_dificuldade[self.modo_dificuldade]["multiplicador"]
        
        # Bonus por completar
        bonus_completo = 500 if self.inversoes_atuais == 0 else 0
        
        pontuacao_base = reducao_inversoes * 500 * eficiencia * multiplicador + bonus_completo
        return int(pontuacao_base)
    
    def trocar_elementos(self, pos1, pos2):
        """Troca dois elementos na sequência"""
        if pos1 != pos2 and self.movimentos_restantes > 0:
            self.sequencia_atual[pos1], self.sequencia_atual[pos2] = \
                self.sequencia_atual[pos2], self.sequencia_atual[pos1]
            
            self.elementos[pos1].valor, self.elementos[pos2].valor = \
                self.elementos[pos2].valor, self.elementos[pos1].valor
            
            self.movimentos_restantes -= 1
            self.movimentos_usados += 1
            self.atualizar_inversoes()
            
            # Verifica se o jogo terminou
            if self.inversoes_atuais == 0 or self.movimentos_restantes == 0:
                self.jogo_terminado = True
                self.pontuacao = self.calcular_pontuacao()
    
    def desenhar_menu(self):
        """Desenha a tela do menu"""
        TELA.fill(BRANCO)
        
        # Título
        titulo = FONTE_GRANDE.render("ORGANIZADOR DE CAOS", True, AZUL)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 80))
        TELA.blit(titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = FONTE_MEDIA.render("Contagem de Inversões com Merge Sort", True, PRETO)
        subtitulo_rect = subtitulo.get_rect(center=(LARGURA//2, 120))
        TELA.blit(subtitulo, subtitulo_rect)
        
        # Instruções
        instrucoes = [
            "Como jogar:",
            "• Clique em dois números para trocá-los de posição",
            "• Objetivo: ordenar a sequência em ordem crescente",
            "• Você tem um número limitado de movimentos",
            "• Pontuação baseada na eficiência e inversões eliminadas",
            "• Ao final, veja a solução com merge sort passo a passo!"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            cor = ROXO if i == 0 else PRETO
            fonte = FONTE_MEDIA if i == 0 else FONTE_PEQUENA
            texto = fonte.render(instrucao, True, cor)
            TELA.blit(texto, (50, 170 + i * 25))
        
        # Seleção de dificuldade
        y_dificuldade = 320
        texto_dif = FONTE_MEDIA.render("Escolha a dificuldade:", True, ROXO)
        TELA.blit(texto_dif, (50, y_dificuldade))
        
        # Botões de dificuldade
        botoes_dificuldade = []
        for i, (modo, config) in enumerate(self.configuracoes_dificuldade.items()):
            if modo == "CUSTOM":
                x = 50 + i * 180
                y = y_dificuldade + 50
                cor = VERDE if modo == self.modo_dificuldade else CINZA
                
                pygame.draw.rect(TELA, cor, (x, y, 160, 80))
                pygame.draw.rect(TELA, PRETO, (x, y, 160, 80), 2)
                
                texto_modo = FONTE_PEQUENA.render("CUSTOMIZADA", True, BRANCO)
                texto_rect = texto_modo.get_rect(center=(x + 80, y + 25))
                TELA.blit(texto_modo, texto_rect)
                
                info = "Seus números"
                texto_info = FONTE_MUITO_PEQUENA.render(info, True, BRANCO)
                texto_info_rect = texto_info.get_rect(center=(x + 80, y + 45))
                TELA.blit(texto_info, texto_info_rect)
                
                if self.sequencia_customizada:
                    seq_str = str(self.sequencia_customizada[:5])[1:-1]
                    if len(self.sequencia_customizada) > 5:
                        seq_str += "..."
                    texto_seq = FONTE_MUITO_PEQUENA.render(seq_str, True, BRANCO)
                    texto_seq_rect = texto_seq.get_rect(center=(x + 80, y + 60))
                    TELA.blit(texto_seq, texto_seq_rect)
                
                botoes_dificuldade.append((x, y, 160, 80, modo))
            else:
                x = 50 + i * 180
                y = y_dificuldade + 50
                cor = VERDE if modo == self.modo_dificuldade else CINZA
                
                pygame.draw.rect(TELA, cor, (x, y, 160, 80))
                pygame.draw.rect(TELA, PRETO, (x, y, 160, 80), 2)
                
                texto_modo = FONTE_PEQUENA.render(modo, True, BRANCO)
                texto_rect = texto_modo.get_rect(center=(x + 80, y + 25))
                TELA.blit(texto_modo, texto_rect)
                
                info = f"{config['tamanho']} nums"
                texto_info = FONTE_MUITO_PEQUENA.render(info, True, BRANCO)
                texto_info_rect = texto_info.get_rect(center=(x + 80, y + 45))
                TELA.blit(texto_info, texto_info_rect)
                
                info2 = f"{config['movimentos']} movs"
                texto_info2 = FONTE_MUITO_PEQUENA.render(info2, True, BRANCO)
                texto_info2_rect = texto_info2.get_rect(center=(x + 80, y + 60))
                TELA.blit(texto_info2, texto_info2_rect)
                
                botoes_dificuldade.append((x, y, 160, 80, modo))
        
        # Botões principais
        botao_iniciar = pygame.Rect(LARGURA//2 - 250, 500, 200, 60)
        pygame.draw.rect(TELA, VERDE, botao_iniciar)
        pygame.draw.rect(TELA, PRETO, botao_iniciar, 3)
        
        texto_iniciar = FONTE_MEDIA.render("INICIAR JOGO", True, BRANCO)
        texto_iniciar_rect = texto_iniciar.get_rect(center=botao_iniciar.center)
        TELA.blit(texto_iniciar, texto_iniciar_rect)
        
        # Botão números customizados
        botao_custom = pygame.Rect(LARGURA//2 + 50, 500, 200, 60)
        pygame.draw.rect(TELA, ROXO, botao_custom)
        pygame.draw.rect(TELA, PRETO, botao_custom, 3)
        
        texto_custom = FONTE_MEDIA.render("SEUS NÚMEROS", True, BRANCO)
        texto_custom_rect = texto_custom.get_rect(center=botao_custom.center)
        TELA.blit(texto_custom, texto_custom_rect)
        
        return botoes_dificuldade, botao_iniciar, botao_custom
    
    def desenhar_tela_customizada(self):
        """Desenha a tela para entrada de números customizados"""
        TELA.fill(BRANCO)
        
        # Título
        titulo = FONTE_GRANDE.render("NÚMEROS CUSTOMIZADOS", True, AZUL)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 100))
        TELA.blit(titulo, titulo_rect)
        
        # Instruções
        instrucoes = [
            "Digite os números que você quer organizar:",
            "• Separar os números por vírgula (ex: 5,2,8,1,3)",
            "• Mínimo: 2 números, Máximo: 15 números",
            "• Use apenas números inteiros únicos",
        ]
        
        for i, instrucao in enumerate(instrucoes):
            cor = ROXO if i == 0 else PRETO
            fonte = FONTE_MEDIA if i == 0 else FONTE_PEQUENA
            texto = fonte.render(instrucao, True, cor)
            TELA.blit(texto, (50, 180 + i * 30))
        
        # Campo de entrada
        campo_entrada = pygame.Rect(50, 320, LARGURA - 100, 50)
        cor_campo = AZUL_CLARO if self.texto_ativo else CINZA
        pygame.draw.rect(TELA, cor_campo, campo_entrada)
        pygame.draw.rect(TELA, PRETO, campo_entrada, 2)
        
        # Texto digitado
        texto_entrada = FONTE_MEDIA.render(self.entrada_texto, True, PRETO)
        TELA.blit(texto_entrada, (campo_entrada.x + 10, campo_entrada.y + 15))
        
        # Cursor piscando
        if self.texto_ativo and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = campo_entrada.x + 10 + texto_entrada.get_width()
            pygame.draw.line(TELA, PRETO, (cursor_x, campo_entrada.y + 10), 
                           (cursor_x, campo_entrada.y + 40), 2)
        
        # Exemplo
        exemplo = FONTE_PEQUENA.render("Exemplo: 7,3,9,1,5,2", True, CINZA)
        TELA.blit(exemplo, (50, 380))
        
        # Validação em tempo real
        if self.entrada_texto:
            valido, mensagem = self.processar_entrada_customizada(self.entrada_texto)
            cor_msg = VERDE if valido else VERMELHO
            texto_msg = FONTE_PEQUENA.render(mensagem, True, cor_msg)
            TELA.blit(texto_msg, (50, 410))
        
        # Botões
        botao_confirmar = pygame.Rect(LARGURA//2 - 220, 500, 180, 60)
        cor_confirmar = VERDE if self.entrada_texto and self.processar_entrada_customizada(self.entrada_texto)[0] else CINZA
        pygame.draw.rect(TELA, cor_confirmar, botao_confirmar)
        pygame.draw.rect(TELA, PRETO, botao_confirmar, 3)
        
        texto_confirmar = FONTE_MEDIA.render("CONFIRMAR", True, BRANCO)
        texto_confirmar_rect = texto_confirmar.get_rect(center=botao_confirmar.center)
        TELA.blit(texto_confirmar, texto_confirmar_rect)
        
        botao_voltar = pygame.Rect(LARGURA//2 + 40, 500, 180, 60)
        pygame.draw.rect(TELA, VERMELHO, botao_voltar)
        pygame.draw.rect(TELA, PRETO, botao_voltar, 3)
        
        texto_voltar = FONTE_MEDIA.render("VOLTAR", True, BRANCO)
        texto_voltar_rect = texto_voltar.get_rect(center=botao_voltar.center)
        TELA.blit(texto_voltar, texto_voltar_rect)
        
        return campo_entrada, botao_confirmar, botao_voltar
    
    def desenhar_array(self, array, x_inicio, y, cor_fundo=AZUL, largura_elem=50, altura_elem=40):
        """Desenha um array na tela"""
        for i, valor in enumerate(array):
            x = x_inicio + i * (largura_elem + 5)
            pygame.draw.rect(TELA, cor_fundo, (x, y, largura_elem, altura_elem))
            pygame.draw.rect(TELA, PRETO, (x, y, largura_elem, altura_elem), 2)
            
            texto = FONTE_PEQUENA.render(str(valor), True, BRANCO)
            texto_rect = texto.get_rect(center=(x + largura_elem//2, y + altura_elem//2))
            TELA.blit(texto, texto_rect)
        
        return len(array) * (largura_elem + 5)

    def desenhar_visualizacao_solucao(self):
        """Desenha a visualização passo a passo da solução"""
        TELA.fill(BRANCO)
        
        # Título
        titulo = FONTE_GRANDE.render("SOLUÇÃO - MERGE SORT", True, AZUL)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 50))
        TELA.blit(titulo, titulo_rect)
        
        # Controles
        controles = f"Passo {self.passo_atual_solucao + 1} de {len(self.passos_solucao)}"
        texto_controles = FONTE_MEDIA.render(controles, True, PRETO)
        TELA.blit(texto_controles, (50, 100))
        
        # Passo atual
        if self.passo_atual_solucao < len(self.passos_solucao):
            passo = self.passos_solucao[self.passo_atual_solucao]
            y_atual = 150
            
            if passo['tipo'] == 'divisao':
                # Mostra a divisão
                texto_divisao = FONTE_MEDIA.render("DIVISÃO:", True, ROXO)
                TELA.blit(texto_divisao, (50, y_atual))
                y_atual += 40
                
                # Array original
                texto_original = FONTE_PEQUENA.render("Array:", True, PRETO)
                TELA.blit(texto_original, (50, y_atual))
                self.desenhar_array(passo['array'], 150, y_atual - 5, AZUL)
                y_atual += 60
                
                # Divisão
                texto_esq = FONTE_PEQUENA.render("Esquerda:", True, PRETO)
                TELA.blit(texto_esq, (50, y_atual))
                self.desenhar_array(passo['esquerda'], 150, y_atual - 5, VERDE)
                y_atual += 50
                
                texto_dir = FONTE_PEQUENA.render("Direita:", True, PRETO)
                TELA.blit(texto_dir, (50, y_atual))
                self.desenhar_array(passo['direita'], 150, y_atual - 5, LARANJA)
                
            elif passo['tipo'] == 'merge_inicio':
                # Mostra o início do merge
                texto_merge = FONTE_MEDIA.render("MERGE - COMBINAR:", True, ROXO)
                TELA.blit(texto_merge, (50, y_atual))
                y_atual += 40
                
                texto_esq = FONTE_PEQUENA.render("Esquerda:", True, PRETO)
                TELA.blit(texto_esq, (50, y_atual))
                self.desenhar_array(passo['esquerda'], 150, y_atual - 5, VERDE)
                y_atual += 50
                
                texto_dir = FONTE_PEQUENA.render("Direita:", True, PRETO)
                TELA.blit(texto_dir, (50, y_atual))
                self.desenhar_array(passo['direita'], 150, y_atual - 5, LARANJA)
                
            elif passo['tipo'] == 'merge_fim':
                # Mostra o resultado do merge
                texto_resultado = FONTE_MEDIA.render("RESULTADO DO MERGE:", True, ROXO)
                TELA.blit(texto_resultado, (50, y_atual))
                y_atual += 40
                
                # Arrays originais
                texto_esq = FONTE_PEQUENA.render("Esquerda era:", True, CINZA)
                TELA.blit(texto_esq, (50, y_atual))
                # Pegar do passo anterior se disponível
                if self.passo_atual_solucao > 0:
                    passo_ant = self.passos_solucao[self.passo_atual_solucao - 1]
                    if 'esquerda' in passo_ant:
                        self.desenhar_array(passo_ant['esquerda'], 180, y_atual - 5, CINZA, 40, 30)
                y_atual += 40
                
                texto_dir = FONTE_PEQUENA.render("Direita era:", True, CINZA)
                TELA.blit(texto_dir, (50, y_atual))
                if self.passo_atual_solucao > 0:
                    passo_ant = self.passos_solucao[self.passo_atual_solucao - 1]
                    if 'direita' in passo_ant:
                        self.desenhar_array(passo_ant['direita'], 180, y_atual - 5, CINZA, 40, 30)
                y_atual += 50
                
                # Resultado
                texto_resultado_array = FONTE_PEQUENA.render("Resultado ordenado:", True, PRETO)
                TELA.blit(texto_resultado_array, (50, y_atual))
                self.desenhar_array(passo['resultado'], 220, y_atual - 5, VERDE_CLARO)
                y_atual += 60
                
                # Inversões encontradas
                if passo['inversoes'] > 0:
                    texto_inv = FONTE_PEQUENA.render(f"Inversões encontradas: {passo['inversoes']}", True, VERMELHO)
                    TELA.blit(texto_inv, (50, y_atual))
        