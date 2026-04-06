#!/usr/bin/env python3
"""
Script principal para executar o LED Strip Visualizer
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from led_visualizer import LEDVisualizer


def main():
    """Função principal"""
    print("Iniciando LED Strip Visualizer...")
    visualizer = LEDVisualizer()
    visualizer.run()


if __name__ == "__main__":
    main()
