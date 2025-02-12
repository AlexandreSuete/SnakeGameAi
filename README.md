# 🐍 Snake Game AI

Este projeto é uma implementação do clássico jogo Snake com uma inteligência artificial (IA) que joga de forma autônoma. A IA utiliza o algoritmo A* para encontrar o caminho até a comida, garantindo um comportamento inteligente e desafiador.

---

## 🚀 Como Funciona?

O jogo Snake tradicional foi aprimorado com uma IA que toma decisões baseadas em:
- **Algoritmo A*:** Para encontrar o caminho mais curto até a comida.
- **Lógica de Fallback:** Quando não há caminho disponível, a cobra se move de forma inteligente para evitar colisões.
- **Componentes Reutilizáveis:** Uma biblioteca de mais de 100 componentes em Angular foi utilizada para criar interfaces consistentes e eficientes.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

- **Python 3.8 ou superior**  
  [Baixe o Python aqui](https://www.python.org/downloads/).

- **Pygame**  
  Pygame é uma biblioteca de desenvolvimento de jogos para Python. Para instalá-la, execute o seguinte comando:

  ```bash
  pip install pygame
  ```

---

## 🛠️ Como Executar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/AlexandreSuete/SnakeGameAi
   cd SnakeGameAi
   ```

2. **Execute o jogo:**

   ```bash
   python SnakeGameAi.py
   ```

3. **Acompanhe o jogo:**  
   A IA controlará a cobra automaticamente. Acompanhe a estratégia e veja como ela evolui!

---

## 🎮 Funcionalidades

- **IA Autônoma:** A cobra é controlada por uma inteligência artificial que utiliza o algoritmo A* para encontrar a comida.
- **Interface Gráfica:** Desenvolvida com Pygame, oferece uma experiência visual agradável e responsiva.
- **Sistema de Pontuação:** A cada comida coletada, a cobra cresce e a pontuação aumenta.
- **Vitória Automática:** Quando a cobra preenche todo o grid, uma mensagem de vitória é exibida.

---

## 🧠 Detalhes Técnicos

### Algoritmo A*
O algoritmo A* é utilizado para encontrar o caminho mais curto entre a cobra e a comida. Ele combina:
- **Custo do caminho atual (g-score):** Distância percorrida desde o início.
- **Heurística (h-score):** Estimativa da distância até o objetivo (distância de Manhattan).

### Estrutura do Projeto
- **Grid Dinâmico:** O grid é gerado dinamicamente, permitindo que a cobra se mova em um ambiente controlado.
- **Componentes Reutilizáveis:** A biblioteca de componentes em Angular foi utilizada para garantir consistência e eficiência no desenvolvimento.

---

## 📂 Estrutura do Projeto

```
snake-game-ai/
├── SnakeGameAi.py          # Código principal do jogo
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
```

---

## 📝 Como Contribuir

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Commit suas mudanças:
   ```bash
   git commit -m 'Adicionando nova funcionalidade'
   ```
4. Envie a branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

## 👏 Créditos

- Desenvolvido por Alexandre Morales Suete(https://github.com/AlexandreSuete).
- Inspirado no clássico jogo Snake.

---

## 📞 Contato

Se tiver dúvidas ou sugestões, sinta-se à vontade para entrar em contato:

- **Email:** alexandre.suete@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/alexandre-morales/

---