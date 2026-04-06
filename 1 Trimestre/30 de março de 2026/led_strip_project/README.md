# LED Strip Visualizer

Um visualizador interativo de fita de LEDs com sincronização de áudio usando Pygame.

## 🎨 Características

- **5 Modos de Visualização:**
  - 🌈 Rainbow (Arco-íris animado)
  - 💓 Pulse (Pulso sincronizado com áudio)
  - 📊 Spectrum (Espectro de cores)
  - 🎲 Random (Aleatório)
  - 〰️ Wave (Onda)

- **Sincronização com Áudio**: Nível de áudio responsivo que afeta a intensidade das cores
- **Interface Intuitiva**: Controle via teclado
- **60 LEDs Simulados**: Fita visual realista

## 🎮 Controles

| Tecla | Função |
|-------|--------|
| `←` / `→` | Trocar modo de visualização |
| `↑` / `↓` | Aumentar/Diminuir nível de áudio |
| `SPACE` | Play/Pause música |
| `ESC` | Sair |

## 📦 Dependências

- Python 3.8+
- pygame
- numpy (opcional, para análise avançada de áudio)

## 🚀 Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uso

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
led_strip_project/
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
└── src/
    ├── __init__.py
    ├── led_visualizer.py  # Classe principal
    └── config.py          # Configurações
```

## 🎵 Adicionando Música

Coloque arquivos de música na pasta `music/` e o programa tentará carregá-los automaticamente.

Formatos suportados:
- MP3
- WAV
- OGG
- FLAC

## 📝 Licença

MIT

## 👨‍💻 Autor

Desenvolvimento educacional para praticar Python, Pygame e visualização de dados.
