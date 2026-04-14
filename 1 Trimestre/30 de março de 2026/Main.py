import glob
import os
import random
import sys

import pygame


PALETTE = [
	(88, 47, 14),
	(127, 79, 36),
	(147, 102, 57),
	(166, 138, 100),
	(182, 173, 144),
	(194, 197, 170),
	(164, 172, 134),
	(101, 109, 74),
	(65, 72, 51),
	(51, 61, 41),
]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "IMG", "new-mosque-istanbul-3840x2160-15261.jpg")
MUSIC_DIR = os.path.join(BASE_DIR, "Violino Metal")


def load_music_path() -> str:
	music_files = sorted(glob.glob(os.path.join(MUSIC_DIR, "*.mp3")))
	if not music_files:
		raise FileNotFoundError(f"Nenhum arquivo MP3 encontrado em: {MUSIC_DIR}")
	return music_files[0]


def load_background() -> pygame.Surface:
	if not os.path.exists(IMAGE_PATH):
		raise FileNotFoundError(f"Imagem de fundo nao encontrada: {IMAGE_PATH}")
	return pygame.image.load(IMAGE_PATH).convert()


def clamp_volume(volume: float) -> float:
	return max(0.0, min(1.0, round(volume, 1)))


def draw_wrapped_text(surface: pygame.Surface, font: pygame.font.Font, text: str, color: tuple[int, int, int], x: int, y: int, max_width: int, line_gap: int = 4) -> int:
	words = text.split()
	lines = []
	current_line = ""

	for word in words:
		test_line = f"{current_line} {word}".strip()
		if font.size(test_line)[0] <= max_width:
			current_line = test_line
		else:
			if current_line:
				lines.append(current_line)
			current_line = word

	if current_line:
		lines.append(current_line)

	current_y = y
	for line in lines:
		title_surface = font.render(line, True, color)
		surface.blit(title_surface, (x, current_y))
		current_y += title_surface.get_height() + line_gap

	return current_y


def draw_led_frame(surface: pygame.Surface, rect: pygame.Rect, palette: list[tuple[int, int, int]], inset: int = 0) -> None:
	segments = 18
	segment_width = max(8, rect.width // segments)
	segment_height = 8
	colors = [random.choice(palette) for _ in range(segments)]

	top_y = rect.top - segment_height - inset
	bottom_y = rect.bottom + inset
	left_x = rect.left - segment_height - inset
	right_x = rect.right + inset

	for index in range(segments):
		color = colors[index]
		alpha = 190
		left = rect.left + index * segment_width
		top_segment = pygame.Surface((segment_width - 2, segment_height), pygame.SRCALPHA)
		top_segment.fill((*color, alpha))
		surface.blit(top_segment, (left, top_y))

		bottom_segment = pygame.Surface((segment_width - 2, segment_height), pygame.SRCALPHA)
		bottom_segment.fill((*color, alpha))
		surface.blit(bottom_segment, (left, bottom_y))

	vertical_segments = max(10, rect.height // 22)
	segment_height_vertical = max(8, rect.height // vertical_segments)
	for index in range(vertical_segments):
		color = random.choice(palette)
		alpha = 190
		top = rect.top + index * segment_height_vertical
		left_segment = pygame.Surface((segment_height, segment_height_vertical - 2), pygame.SRCALPHA)
		left_segment.fill((*color, alpha))
		surface.blit(left_segment, (left_x, top))

		right_segment = pygame.Surface((segment_height, segment_height_vertical - 2), pygame.SRCALPHA)
		right_segment.fill((*color, alpha))
		surface.blit(right_segment, (right_x, top))


def main() -> None:
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()

	screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
	pygame.display.set_caption("Music Player com Pygame")

	background = load_background()
	music_path = load_music_path()

	pygame.mixer.music.load(music_path)
	pygame.mixer.music.play(-1)

	volume = 0.5
	pygame.mixer.music.set_volume(volume)
	track_name = os.path.splitext(os.path.basename(music_path))[0]

	font = pygame.font.SysFont("monospace", 20)
	font_small = pygame.font.SysFont("monospace", 16)
	font_title = pygame.font.SysFont("monospace", 28, bold=True)
	clock = pygame.time.Clock()
	running = True
	playback_state = "Playing"

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.VIDEORESIZE:
				screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					volume = clamp_volume(volume + 0.1)
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_DOWN:
					volume = clamp_volume(volume - 0.1)
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_p:
					pygame.mixer.music.pause()
					playback_state = "Paused"
				elif event.key == pygame.K_r:
					pygame.mixer.music.unpause()
					playback_state = "Playing"
				elif event.key == pygame.K_s:
					pygame.mixer.music.stop()
					pygame.quit()
					sys.exit()

		width, height = screen.get_size()
		background_scaled = pygame.transform.scale(background, (width, height))
		screen.blit(background_scaled, (0, 0))

		ambient = pygame.Surface((width, height), pygame.SRCALPHA)
		ambient.fill((15, 12, 8, 132))
		screen.blit(ambient, (0, 0))

		stage_width = min(820, max(520, width - 80))
		stage_height = min(460, max(320, height - 140))
		stage_rect = pygame.Rect(0, 0, stage_width, stage_height)
		stage_rect.center = (width // 2, height // 2 + 20)

		stage_shadow = pygame.Surface((stage_rect.width + 24, stage_rect.height + 24), pygame.SRCALPHA)
		pygame.draw.rect(stage_shadow, (0, 0, 0, 110), stage_shadow.get_rect(), border_radius=28)
		screen.blit(stage_shadow, (stage_rect.x - 12, stage_rect.y - 4))

		panel = pygame.Surface((stage_rect.width, stage_rect.height), pygame.SRCALPHA)
		pygame.draw.rect(panel, (32, 25, 18, 224), panel.get_rect(), border_radius=24)
		pygame.draw.rect(panel, (75, 64, 45, 200), panel.get_rect(), width=2, border_radius=24)
		screen.blit(panel, stage_rect.topleft)

		draw_led_frame(screen, stage_rect, PALETTE)

		header_text = font_title.render("MUSIC LOUNGE", True, (194, 197, 170))
		screen.blit(header_text, (stage_rect.x + 24, stage_rect.y + 22))

		track_label = font.render(f"Faixa: {track_name}", True, (194, 197, 170))
		screen.blit(track_label, (stage_rect.x + 24, stage_rect.y + 64))

		player_box = pygame.Rect(stage_rect.x + 24, stage_rect.y + 110, stage_rect.width - 48, 130)
		pygame.draw.rect(screen, (20, 17, 12, 175), player_box, border_radius=18)
		pygame.draw.rect(screen, (194, 197, 170), player_box, width=1, border_radius=18)

		player_label = font_title.render("PLAYER", True, (194, 197, 170))
		screen.blit(player_label, (player_box.x + 20, player_box.y + 18))

		state_text = font.render(f"Estado: {playback_state}", True, (194, 197, 170))
		volume_text = font.render(f"Volume: {int(volume * 100)}%", True, (194, 197, 170))
		screen.blit(state_text, (player_box.x + 20, player_box.y + 56))
		screen.blit(volume_text, (player_box.x + 20, player_box.y + 82))

		status_bar = pygame.Rect(player_box.right - 190, player_box.y + 34, 150, 52)
		pygame.draw.rect(screen, random.choice(PALETTE), status_bar, border_radius=14)
		pygame.draw.rect(screen, (15, 12, 8), status_bar, width=2, border_radius=14)
		status_label = font_small.render("Bem vindo!", True, (255, 255, 255))
		status_value = font_small.render("Pronto", True, (255, 255, 255))
		screen.blit(status_label, (status_bar.x + 16, status_bar.y + 8))
		screen.blit(status_value, (status_bar.x + 16, status_bar.y + 26))

		tutorial_box = pygame.Rect(stage_rect.x + 24, stage_rect.y + 260, stage_rect.width - 48, stage_rect.height - 284)
		pygame.draw.rect(screen, (20, 17, 12, 165), tutorial_box, border_radius=18)
		pygame.draw.rect(screen, (194, 197, 170), tutorial_box, width=1, border_radius=18)

		tutorial_title = font.render("TUTORIAL", True, (194, 197, 170))
		screen.blit(tutorial_title, (tutorial_box.x + 20, tutorial_box.y + 16))

		tutorial_lines = [
			"Seta CIMA: aumenta o volume",
			"Seta BAIXO: diminui o volume",
			"P: pausa a musica",
			"R: volta a tocar",
			"S: encerra o player",
		]
		text_y = tutorial_box.y + 52
		for line in tutorial_lines:
			text_surface = font_small.render(line, True, (194, 197, 170))
			screen.blit(text_surface, (tutorial_box.x + 20, text_y))
			text_y += 24

		footer_text = font_small.render("Pressione F1 para ajuda", True, (194, 197, 170))
		screen.blit(footer_text, (stage_rect.x + 24, stage_rect.bottom - 28))

		pygame.display.flip()
		clock.tick(5)

	pygame.quit()


if __name__ == "__main__":
	main()
