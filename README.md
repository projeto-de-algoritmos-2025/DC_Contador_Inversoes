# Jogo de Contador de Inversões

Um jogo educativo interativo que ensina o conceito de contagem de inversões através do algoritmo Merge Sort. O jogador deve organizar sequências numéricas desordenadas com o menor número de movimentos possível, e ao final pode visualizar como o Merge Sort resolve o problema passo a passo.

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/2021933  |  William Bernardo da Silva |
| 22/2015195  |  Mateus de Castro Santos |

## Requisitos

- Python 3.7 ou superior
- Pygame 2.0+
- Sistema operacional: Windows, macOS ou Linux
- Resolução mínima da tela: 1200x800 pixels

### Dependências Python
- `pygame`: Para interface gráfica e interação
- `random`: Para geração de sequências aleatórias (built-in)
- `sys`: Para controle do sistema (built-in)
- `math`: Para cálculos matemáticos (built-in)

## Instalação

1. Clone ou baixe o repositório do projeto
2. Navegue até o diretório do projeto:
   ```bash
   cd cont_inversoes
   ```
3. Instale as dependências usando pip:
   ```bash
   pip install -r requirements.txt
   ```
   
   Ou instale o Pygame diretamente:
   ```bash
   pip install pygame
   ```

## Como Executar

Execute o jogo com o seguinte comando:

```bash
python jogo.py
```

O jogo abrirá em uma janela de 1200x800 pixels e estará pronto para uso.

## Como Usar

### Menu Principal
1. **Escolha da Dificuldade**: Selecione entre Fácil (6 números), Médio (8 números), Difícil (10 números) ou Customizada
2. **Números Customizados**: Clique em "SEUS NÚMEROS" para inserir sua própria sequência
3. **Iniciar Jogo**: Clique em "INICIAR JOGO" para começar

### Entrada Customizada
1. Digite números separados por vírgula (ex: 7,3,9,1,5,2)
2. Mínimo: 2 números, Máximo: 15 números
3. Use apenas números inteiros únicos
4. Pressione Enter ou clique em "CONFIRMAR"

### Jogabilidade
1. **Objetivo**: Ordenar a sequência em ordem crescente
2. **Controles**: Clique em dois números para trocá-los de posição
3. **Limitações**: Número limitado de movimentos baseado na dificuldade
4. **Progresso**: Acompanhe as inversões restantes e movimentos disponíveis

### Visualização da Solução
1. Após terminar o jogo, clique em "VER SOLUÇÃO"
2. Navigate pelos passos usando "ANTERIOR" e "PRÓXIMO"
3. Observe como o Merge Sort divide e combina os arrays
4. Veja quando as inversões são detectadas e contadas

## Funcionalidades

### Principais
- **4 Níveis de Dificuldade**: Fácil, Médio, Difícil e Customizada
- **Entrada Personalizada**: Defina sua própria sequência de números
- **Sistema de Pontuação**: Baseado em eficiência e inversões eliminadas
- **Visualização Educativa**: Demonstração passo a passo do Merge Sort
- **Interface Intuitiva**: Design limpo e fácil de usar

### Técnicas
- **Contagem de Inversões**: Implementação otimizada O(n log n)
- **Algoritmo Merge Sort**: Versão modificada que captura todos os passos
- **Detecção de Inversões**: Contagem precisa durante o processo de merge
- **Validação de Entrada**: Verificação automática de sequências válidas

### Educativas
- **Explicação do Algoritmo**: Descrição clara do funcionamento do Merge Sort
- **Demonstração Visual**: Arrays sendo divididos e combinados
- **Contagem em Tempo Real**: Visualização de quando inversões são encontradas
- **Feedback Imediato**: Progresso e estatísticas atualizadas constantemente

## Sobre o Algoritmo de Contagem de Inversões

### Conceito
Uma **inversão** em um array é um par de índices (i, j) onde i < j mas array[i] > array[j]. Ou seja, dois elementos que estão fora de ordem.

### Implementação
O algoritmo utiliza uma versão modificada do **Merge Sort** para contar inversões em tempo O(n log n):

1. **Divisão**: O array é dividido recursivamente ao meio
2. **Conquista**: Conta inversões nas metades esquerda e direita separadamente  
3. **Combinação**: Durante o merge, conta inversões entre as duas metades
4. **Contagem**: Quando um elemento da direita é menor que da esquerda, há `len(esquerda) - i` inversões

### Vantagens
- **Eficiência**: O(n log n) vs O(n²) da abordagem ingênua
- **Estabilidade**: Mantém a ordem relativa de elementos iguais
- **Educativo**: Demonstra conceitos de divisão e conquista
- **Visualizável**: Cada passo pode ser mostrado graficamente

### Exemplo
Para o array [5, 2, 8, 1]:
- Inversões: (5,2), (5,1), (2,1), (8,1) = 4 inversões total
- O Merge Sort encontra essas inversões durante o processo de combinação

## Observações

### Limitações
- A visualização da solução mostra apenas os passos principais do algoritmo
- Sequências muito grandes (>15 números) não são suportadas na entrada customizada
- O jogo requer uma resolução mínima de 1200x800 para exibição adequada

### Dicas de Uso
- Experimente diferentes estratégias: tente minimizar movimentos vs. maximizar progresso
- Use a visualização da solução para entender melhor o algoritmo
- A pontuação considera tanto eficiência quanto completude
- Sequências customizadas permitem testar casos específicos

### Performance
- O algoritmo é otimizado para sequências de até 15 elementos
- A interface gráfica roda a 60 FPS para uma experiência fluida
- Todos os cálculos de inversões são feitos em tempo real

## Screenshots

*[Adicionar screenshots das diferentes telas do jogo]*

1. **Menu Principal** - Seleção de dificuldade e opções
2. **Entrada Customizada** - Interface para inserir números próprios  
3. **Tela de Jogo** - Jogabilidade principal com sequência e controles
4. **Resultados** - Estatísticas finais e acesso à solução
5. **Visualização da Solução** - Demonstração passo a passo do Merge Sort

## Outros

### Estrutura do Projeto
```
cont_inversoes/
├── jogo.py              # Arquivo principal do jogo
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

### Contribuições
- Interface gráfica desenvolvida com Pygame
- Algoritmo de contagem de inversões implementado do zero
- Sistema educativo de visualização criado especificamente para este projeto

### Links Úteis
- [Documentação do Pygame](https://www.pygame.org/docs/)
- [Artigo sobre Merge Sort](https://en.wikipedia.org/wiki/Merge_sort)
- [Algoritmos de Divisão e Conquista](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm)

[Video Apresentação](link)