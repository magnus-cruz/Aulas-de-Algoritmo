"""
LED Strip Visualizer com Matplotlib
Visualização interativa de fita de LEDs sincronizados com som
"""

import random
import math
import os
from enum import Enum
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle


class VisualizationMode(Enum):
    """Modos de visualização disponíveis"""
    RAINBOW = "rainbow"
    PULSE = "pulse"
    SPECTRUM = "spectrum"
    RANDOM = "random"
    WAVE = "wave"


class LEDColor:
    """Classe para gerenciar cores RGB"""
    
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
    
    @property
    def normalized(self) -> Tuple[float, float, float]:
        """Retorna RGB normalizado (0-1)"""
        return (self.r / 255, self.g / 255, self.b / 255)
    
    @property
    def tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)
    
    @staticmethod
    def from_hsv(h: float, s: float, v: float) -> 'LEDColor':
        """Converte HSV para RGB"""
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return LEDColor(
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )


class LEDStrip:
    """Representa uma fita de LEDs"""
    
    def __init__(self, num_leds: int = 60):
        self.num_leds = num_leds
        self.colors: List[LEDColor] = [LEDColor() for _ in range(num_leds)]
        self.time = 0.0
    
    def update(self, time_delta: float, mode: VisualizationMode, 
               audio_level: float = 0.5):
        """Atualiza as cores dos LEDs baseado no modo e nível de áudio"""
        self.time += time_delta
        
        if mode == VisualizationMode.RAINBOW:
            self._update_rainbow()
        elif mode == VisualizationMode.PULSE:
            self._update_pulse(audio_level)
        elif mode == VisualizationMode.SPECTRUM:
            self._update_spectrum(audio_level)
        elif mode == VisualizationMode.RANDOM:
            self._update_random()
        elif mode == VisualizationMode.WAVE:
            self._update_wave(audio_level)
    
    def _update_rainbow(self):
        """Modo arco-íris animado"""
        for i in range(self.num_leds):
            hue = (i / self.num_leds * 360 + self.time * 100) % 360
            self.colors[i] = LEDColor.from_hsv(hue, 1.0, 1.0)
    
    def _update_pulse(self, audio_level: float):
        """Modo pulso sincronizado com áudio"""
        brightness = 0.5 + 0.5 * math.sin(self.time * 5) * audio_level
        base_hue = (self.time * 60) % 360
        
        for i in range(self.num_leds):
            hue = (base_hue + i / self.num_leds * 60) % 360
            self.colors[i] = LEDColor.from_hsv(hue, 0.8, brightness)
    
    def _update_spectrum(self, audio_level: float):
        """Modo espectro com áudio"""
        for i in range(self.num_leds):
            freq_ratio = i / self.num_leds
            hue = freq_ratio * 360
            saturation = audio_level
            brightness = 0.3 + 0.7 * audio_level * math.sin(self.time * 3 + i * 0.5)
            self.colors[i] = LEDColor.from_hsv(hue, saturation, brightness)
    
    def _update_random(self):
        """Modo aleatório"""
        if int(self.time * 10) % 5 == 0:
            for i in range(self.num_leds):
                self.colors[i] = LEDColor(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
    
    def _update_wave(self, audio_level: float):
        """Modo onda"""
        for i in range(self.num_leds):
            wave = math.sin(self.time * 3 + i * 0.3) * audio_level
            brightness = 0.4 + 0.6 * (wave + 1) / 2
            hue = (i / self.num_leds * 360 + self.time * 50) % 360
            self.colors[i] = LEDColor.from_hsv(hue, 1.0, brightness)
    
    def get_colors(self) -> List[Tuple[float, float, float]]:
        """Retorna cores normalizadas para matplotlib"""
        return [color.normalized for color in self.colors]


class LEDVisualizer:
    """Aplicação principal do visualizador"""
    
    def __init__(self):
        self.fig, (self.ax_leds, self.ax_info) = plt.subplots(
            2, 1, figsize=(14, 8), 
            gridspec_kw={'height_ratios': [1, 3]}
        )
        
        self.fig.patch.set_facecolor('#141e1e')
        self.ax_leds.set_facecolor('#0a0a0f')
        self.ax_info.set_facecolor('#141e1e')
        
        # Configurar eixos
        self.ax_leds.set_xlim(0, 60)
        self.ax_leds.set_ylim(0, 1)
        self.ax_leds.set_aspect('auto')
        self.ax_leds.axis('off')
        
        self.ax_info.set_xlim(0, 10)
        self.ax_info.set_ylim(0, 10)
        self.ax_info.axis('off')
        
        self.led_strip = LEDStrip(num_leds=60)
        self.mode = VisualizationMode.RAINBOW
        self.modes = list(VisualizationMode)
        self.current_mode_index = 0
        self.audio_level = 0.5
        self.running = True
        self.time = 0.0
        self.fps = 60
        self.frame_count = 0
        
        # Coleções de retângulos para os LEDs
        self.led_rects = []
        for i in range(60):
            rect = Rectangle((i, 0), 0.95, 1, linewidth=1, edgecolor='#333333')
            self.ax_leds.add_patch(rect)
            self.led_rects.append(rect)
        
        # Título
        self.title = self.ax_info.text(
            5, 9.5, "LED Strip Visualizer", 
            ha='center', va='top', fontsize=20, 
            color='#c8c8ff', weight='bold'
        )
        
        # Info texts
        self.mode_text = self.ax_info.text(
            1, 7.5, "Modo: RAINBOW", 
            fontsize=14, color='#64c8ff'
        )
        
        self.music_text = self.ax_info.text(
            1, 6.5, "Música: Parado ■", 
            fontsize=14, color='#64ff64'
        )
        
        self.audio_text = self.ax_info.text(
            1, 5.5, "Nível de Áudio: 0.5", 
            fontsize=14, color='#ffc864'
        )
        
        # Instructions
        instructions = [
            "← → Trocar Modo",
            "↑ ↓ Ajustar Nível",
            "Q Sair"
        ]
        
        y_pos = 4.0
        for instruction in instructions:
            self.ax_info.text(
                1, y_pos, instruction, 
                fontsize=12, color='#999999'
            )
            y_pos -= 0.7
        
        # Conectar eventos de teclado
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        # Animação
        self.anim = animation.FuncAnimation(
            self.fig, self.update_animation, 
            interval=1000/self.fps, blit=True, repeat=True
        )
    
    def on_key_press(self, event):
        """Manipular eventos de teclado"""
        if event.key == 'left':
            self.current_mode_index = (self.current_mode_index - 1) % len(self.modes)
            self.mode = self.modes[self.current_mode_index]
        
        elif event.key == 'right':
            self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
            self.mode = self.modes[self.current_mode_index]
        
        elif event.key == 'up':
            self.audio_level = min(1.0, self.audio_level + 0.1)
        
        elif event.key == 'down':
            self.audio_level = max(0.0, self.audio_level - 0.1)
        
        elif event.key == 'q':
            plt.close(self.fig)
            self.running = False
    
    def update_animation(self, frame):
        """Atualizar frame da animação"""
        delta_time = 1.0 / self.fps
        self.time += delta_time
        
        # Simular nível de áudio variável
        simulated_audio = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(self.time * 3))
        
        # Atualizar LEDs
        self.led_strip.update(delta_time, self.mode, simulated_audio)
        colors = self.led_strip.get_colors()
        
        # Atualizar cores dos retângulos
        for i, rect in enumerate(self.led_rects):
            rect.set_facecolor(colors[i])
        
        # Atualizar textos
        self.mode_text.set_text(f"Modo: {self.mode.value.upper()}")
        self.audio_text.set_text(f"Nível de Áudio: {self.audio_level:.1f}")
        
        return self.led_rects + [
            self.title, self.mode_text, 
            self.music_text, self.audio_text
        ]
    
    def run(self):
        """Executar visualizador"""
        print("LED Strip Visualizer iniciado!")
        print("Use as setas do teclado para controlar")
        print("Pressione 'q' para sair")
        plt.tight_layout()
        plt.show()


def main():
    """Função principal"""
    visualizer = LEDVisualizer()
    visualizer.run()


if __name__ == "__main__":
    main()
