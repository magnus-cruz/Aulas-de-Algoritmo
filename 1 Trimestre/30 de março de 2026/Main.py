import glob
import math
import os

import pygame


DARK_BG = (26, 26, 46)
DARK_BG_2 = (15, 18, 32)
CARD_GLASS = (255, 255, 255, 22)
CARD_FILL = (20, 24, 40, 170)
CARD_BORDER = (255, 255, 255, 45)
TEXT_PRIMARY = (245, 247, 251)
TEXT_SECONDARY = (177, 183, 196)
ACCENT = (212, 168, 83)
ACCENT_SOFT = (164, 128, 54)
PLAYING_GREEN = (57, 214, 138)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "IMG", "cyborg-green-grass-3840x2160-15996.jpg")
MUSIC_DIR = os.path.join(BASE_DIR, "Violino Metal")


def load_music_list() -> list[str]:
	music_files = sorted(glob.glob(os.path.join(MUSIC_DIR, "*.mp3")))
	if not music_files:
		raise FileNotFoundError(f"Nenhum arquivo MP3 encontrado em: {MUSIC_DIR}")
	return music_files


def load_background() -> pygame.Surface:
	if not os.path.exists(IMAGE_PATH):
		raise FileNotFoundError(f"Imagem de fundo nao encontrada: {IMAGE_PATH}")
	return pygame.image.load(IMAGE_PATH).convert()


def clamp_volume(volume: float) -> float:
	return max(0.0, min(1.0, round(volume, 2)))


def clamp_seek(value: float, total: float) -> float:
	if total <= 0:
		return max(0.0, value)
	return max(0.0, min(total, value))


def pick_font(preferred: list[str], size: int, bold: bool = False) -> pygame.font.Font:
	for name in preferred:
		if pygame.font.match_font(name):
			return pygame.font.SysFont(name, size, bold=bold)
	return pygame.font.SysFont("Segoe UI", size, bold=bold)


def format_time(seconds_value: float) -> str:
	total = max(0, int(seconds_value))
	minutes = total // 60
	seconds = total % 60
	return f"{minutes:02d}:{seconds:02d}"


def seek_music(position: float, volume: float) -> float:
	try:
		pygame.mixer.music.play(-1, position)
		pygame.mixer.music.set_volume(volume)
		return position
	except (TypeError, pygame.error):
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(volume)
		return 0.0


def get_track_title(file_path: str) -> str:
	return os.path.splitext(os.path.basename(file_path))[0]


def get_track_duration(file_path: str) -> float:
	try:
		return pygame.mixer.Sound(file_path).get_length()
	except pygame.error:
		return 0.0


def load_track(music_files: list[str], track_index: int, volume: float, start_at: float = 0.0) -> tuple[float, str]:
	# Carrega a faixa atual da playlist e inicia reproducao.
	track_path = music_files[track_index]
	pygame.mixer.music.load(track_path)
	played_from = seek_music(start_at, volume)
	duration = get_track_duration(track_path)
	if played_from > 0 and duration > 0 and played_from >= duration:
		played_from = seek_music(0.0, volume)
	return duration, get_track_title(track_path)


def draw_vertical_gradient(surface: pygame.Surface, top_color: tuple[int, int, int, int], bottom_color: tuple[int, int, int, int]) -> None:
	width, height = surface.get_size()
	if height <= 1:
		return
	gradient = pygame.Surface((width, height), pygame.SRCALPHA)
	for y in range(height):
		ratio = y / (height - 1)
		r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
		g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
		b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
		a = int(top_color[3] + (bottom_color[3] - top_color[3]) * ratio)
		pygame.draw.line(gradient, (r, g, b, a), (0, y), (width, y))
	surface.blit(gradient, (0, 0))


def draw_soft_orbs(surface: pygame.Surface, phase: float) -> None:
	width, height = surface.get_size()
	orb_layer = pygame.Surface((width, height), pygame.SRCALPHA)
	x1 = int(width * 0.2 + math.sin(phase * 0.4) * 24)
	y1 = int(height * 0.28)
	x2 = int(width * 0.82 + math.cos(phase * 0.3) * 20)
	y2 = int(height * 0.72)
	pygame.draw.circle(orb_layer, (212, 168, 83, 38), (x1, y1), max(120, width // 6))
	pygame.draw.circle(orb_layer, (91, 110, 191, 36), (x2, y2), max(140, width // 5))
	surface.blit(orb_layer, (0, 0))


def draw_glass_panel(surface: pygame.Surface, rect: pygame.Rect, radius: int = 22) -> None:
	panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
	pygame.draw.rect(panel, CARD_FILL, panel.get_rect(), border_radius=radius)
	pygame.draw.rect(panel, CARD_GLASS, pygame.Rect(2, 2, rect.width - 4, rect.height // 2), border_radius=radius)
	pygame.draw.rect(panel, CARD_BORDER, panel.get_rect(), width=1, border_radius=radius)
	surface.blit(panel, rect.topleft)
	inner_shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
	pygame.draw.rect(inner_shadow, (0, 0, 0, 42), inner_shadow.get_rect(), width=2, border_radius=radius)
	surface.blit(inner_shadow, rect.topleft)


def draw_header_icon(surface: pygame.Surface, center: tuple[int, int]) -> None:
	x, y = center
	pygame.draw.arc(surface, ACCENT, pygame.Rect(x - 16, y - 16, 12, 24), 1.2, 5.1, 3)
	pygame.draw.arc(surface, ACCENT, pygame.Rect(x + 4, y - 16, 12, 24), -2.0, 2.0, 3)
	pygame.draw.line(surface, ACCENT, (x - 4, y + 6), (x + 4, y + 6), 3)
	pygame.draw.circle(surface, ACCENT, (x - 10, y + 6), 5)
	pygame.draw.circle(surface, ACCENT, (x + 10, y + 6), 5)


def draw_album_cover(surface: pygame.Surface, rect: pygame.Rect, phase: float) -> None:
	shadow = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
	pygame.draw.rect(shadow, (0, 0, 0, 90), shadow.get_rect(), border_radius=16)
	surface.blit(shadow, (rect.x - 8, rect.y + 4))

	cover = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
	for y in range(rect.height):
		ratio = y / max(1, rect.height - 1)
		r = int(28 + (60 - 28) * ratio)
		g = int(33 + (48 - 33) * ratio)
		b = int(52 + (86 - 52) * ratio)
		pygame.draw.line(cover, (r, g, b), (0, y), (rect.width, y))
	pygame.draw.rect(cover, (255, 255, 255, 22), cover.get_rect(), width=1, border_radius=12)
	pygame.draw.circle(cover, (212, 168, 83, 140), (rect.width // 2, rect.height // 2), 18 + int(abs(math.sin(phase)) * 4))
	pygame.draw.circle(cover, (14, 16, 26), (rect.width // 2, rect.height // 2), 7)
	surface.blit(cover, rect.topleft)


def draw_progress_bar(surface: pygame.Surface, rect: pygame.Rect, progress: float) -> None:
	progress = max(0.0, min(1.0, progress))
	pygame.draw.rect(surface, (45, 51, 72), rect, border_radius=8)
	filled = pygame.Rect(rect.x, rect.y, int(rect.width * progress), rect.height)
	if filled.width > 0:
		pygame.draw.rect(surface, ACCENT, filled, border_radius=8)
	thumb_x = rect.x + int(rect.width * progress)
	thumb_x = max(rect.x + 6, min(rect.right - 6, thumb_x))
	pygame.draw.circle(surface, TEXT_PRIMARY, (thumb_x, rect.centery), 7)
	pygame.draw.circle(surface, ACCENT_SOFT, (thumb_x, rect.centery), 3)


def draw_volume_slider(surface: pygame.Surface, rect: pygame.Rect, volume: float, font: pygame.font.Font) -> None:
	pygame.draw.polygon(surface, TEXT_SECONDARY, [(rect.x, rect.y + 8), (rect.x + 9, rect.y + 2), (rect.x + 9, rect.y + 14)])
	pygame.draw.rect(surface, TEXT_SECONDARY, (rect.x + 9, rect.y + 4, 4, 8), border_radius=2)
	pygame.draw.arc(surface, TEXT_SECONDARY, pygame.Rect(rect.x + 10, rect.y + 1, 12, 14), -0.8, 0.8, 2)

	slider = pygame.Rect(rect.x + 28, rect.y + 7, rect.width - 84, 4)
	pygame.draw.rect(surface, (74, 80, 101), slider, border_radius=4)
	fill = pygame.Rect(slider.x, slider.y, int(slider.width * volume), slider.height)
	if fill.width > 0:
		pygame.draw.rect(surface, ACCENT, fill, border_radius=4)
	thumb_x = slider.x + int(slider.width * volume)
	thumb_x = max(slider.x + 5, min(slider.right - 5, thumb_x))
	pygame.draw.circle(surface, TEXT_PRIMARY, (thumb_x, slider.centery), 6)

	vol_text = font.render(f"{int(volume * 100)}%", True, TEXT_SECONDARY)
	surface.blit(vol_text, (slider.right + 12, rect.y - 1))


def draw_button(surface: pygame.Surface, center: tuple[int, int], radius: int, label: str, active: bool, font: pygame.font.Font) -> None:
	fill = (40, 46, 66)
	border = (95, 104, 130)
	if active:
		fill = (72, 58, 30)
		border = ACCENT
	pygame.draw.circle(surface, fill, center, radius)
	pygame.draw.circle(surface, border, center, radius, 1)
	text = font.render(label, True, TEXT_PRIMARY)
	surface.blit(text, text.get_rect(center=center))


def led_color(phase: float, index: int) -> tuple[int, int, int]:
	wave = (math.sin(phase + index * 0.45) + 1.0) * 0.5
	r = int(90 + wave * 122)
	g = int(70 + wave * 98)
	b = int(40 + wave * 43)
	return r, g, b


def draw_led_frame(surface: pygame.Surface, rect: pygame.Rect, phase: float, inset: int = 0) -> None:
	segments = 24
	segment_width = max(8, rect.width // segments)
	segment_height = 7

	top_y = rect.top - segment_height - inset
	bottom_y = rect.bottom + inset
	left_x = rect.left - segment_height - inset
	right_x = rect.right + inset

	for index in range(segments):
		color = led_color(phase, index)
		left = rect.left + index * segment_width
		top_segment = pygame.Surface((segment_width - 2, segment_height), pygame.SRCALPHA)
		top_segment.fill((*color, 205))
		surface.blit(top_segment, (left, top_y))

		bottom_segment = pygame.Surface((segment_width - 2, segment_height), pygame.SRCALPHA)
		bottom_segment.fill((*color, 205))
		surface.blit(bottom_segment, (left, bottom_y))

	vertical_segments = max(12, rect.height // 20)
	segment_height_vertical = max(8, rect.height // vertical_segments)
	for index in range(vertical_segments):
		color = led_color(phase * 1.15, index + 4)
		top = rect.top + index * segment_height_vertical
		left_segment = pygame.Surface((segment_height, segment_height_vertical - 2), pygame.SRCALPHA)
		left_segment.fill((*color, 205))
		surface.blit(left_segment, (left_x, top))

		right_segment = pygame.Surface((segment_height, segment_height_vertical - 2), pygame.SRCALPHA)
		right_segment.fill((*color, 205))
		surface.blit(right_segment, (right_x, top))


def draw_kbd(surface: pygame.Surface, rect: pygame.Rect, key: str, desc: str, font: pygame.font.Font, small_font: pygame.font.Font) -> None:
	pygame.draw.rect(surface, (28, 34, 54, 210), rect, border_radius=10)
	key_rect = pygame.Rect(rect.x + 10, rect.y + 6, 84, rect.height - 12)
	pygame.draw.rect(surface, (48, 56, 82), key_rect, border_radius=10)
	pygame.draw.rect(surface, (122, 132, 164), key_rect, 1, border_radius=10)
	key_text = font.render(key, True, TEXT_PRIMARY)
	surface.blit(key_text, key_text.get_rect(center=key_rect.center))

	desc_text = small_font.render(desc, True, TEXT_SECONDARY)
	surface.blit(desc_text, (key_rect.right + 14, rect.y + (rect.height - desc_text.get_height()) // 2))


def handle_key_input(
	event: pygame.event.Event,
	volume: float,
	playback_state: str,
	elapsed: float,
	total_duration: float,
	shortcuts_expanded: bool,
	track_shift: int,
) -> tuple[float, str, bool, float, bool, int]:
	running = True

	if event.key == pygame.K_UP:
		volume = clamp_volume(volume + 0.1)
		pygame.mixer.music.set_volume(volume)
	elif event.key == pygame.K_DOWN:
		volume = clamp_volume(volume - 0.1)
		pygame.mixer.music.set_volume(volume)
	elif event.key == pygame.K_p:
		pygame.mixer.music.pause()
		playback_state = "Paused"
	elif event.key == pygame.K_t:
		elapsed = seek_music(0.0, volume)
		playback_state = "Playing"
	elif event.key == pygame.K_LEFT:
		elapsed = clamp_seek(elapsed - 5.0, total_duration)
		elapsed = seek_music(elapsed, volume)
		playback_state = "Playing"
	elif event.key == pygame.K_RIGHT:
		elapsed = clamp_seek(elapsed + 5.0, total_duration)
		elapsed = seek_music(elapsed, volume)
		playback_state = "Playing"
	elif event.key == pygame.K_n:
		# Proxima faixa da playlist.
		track_shift = 1
	elif event.key == pygame.K_b:
		# Faixa anterior da playlist.
		track_shift = -1
	elif event.key == pygame.K_r:
		pygame.mixer.music.unpause()
		playback_state = "Playing"
	elif event.key == pygame.K_SPACE:
		if playback_state == "Paused":
			pygame.mixer.music.unpause()
			playback_state = "Playing"
		else:
			pygame.mixer.music.pause()
			playback_state = "Paused"
	elif event.key == pygame.K_h:
		shortcuts_expanded = not shortcuts_expanded
	elif event.key == pygame.K_s:
		running = False

	return volume, playback_state, running, elapsed, shortcuts_expanded, track_shift


def main() -> None:
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()

	screen = pygame.display.set_mode((900, 640), pygame.RESIZABLE)
	pygame.display.set_caption("Music Lounge")

	background = load_background()
	music_files = load_music_list()
	track_index = 0

	volume = 0.5
	pygame.mixer.music.set_volume(volume)
	total_duration, track_name = load_track(music_files, track_index, volume)

	# Mantem o subtitulo que o usuario pediu no design premium.
	featured_track_line = "Faixa 01 - Silent Screams, Violent Strings"
	artist_name = "Violino Metal Ensemble"

	font = pick_font(["Inter", "DM Sans", "Segoe UI"], 20)
	font_small = pick_font(["Inter", "DM Sans", "Segoe UI"], 15)
	font_title = pick_font(["Inter", "DM Sans", "Segoe UI"], 40, bold=True)
	font_subtitle = pick_font(["Inter", "DM Sans", "Segoe UI"], 23, bold=True)
	font_controls = pick_font(["Inter", "DM Sans", "Segoe UI"], 18, bold=True)

	clock = pygame.time.Clock()
	running = True
	playback_state = "Playing"
	shortcuts_expanded = True
	led_phase = 0.0
	ui_phase = 0.0
	elapsed = 0.0
	track_shift = 0

	while running:
		dt = clock.tick(60) / 1000.0
		ui_phase += dt
		if playback_state == "Playing":
			elapsed += dt
			led_phase += dt * 5.0
			if total_duration > 0 and elapsed >= total_duration:
				# Auto avanca quando a faixa atual termina.
				track_shift = 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.VIDEORESIZE:
				new_width = max(360, event.w)
				new_height = max(600, event.h)
				screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
			elif event.type == pygame.KEYDOWN:
				track_shift = 0
				volume, playback_state, running, elapsed, shortcuts_expanded, track_shift = handle_key_input(
					event,
					volume,
					playback_state,
					elapsed,
					total_duration,
					shortcuts_expanded,
					track_shift,
				)

		if track_shift != 0 and music_files:
			track_index = (track_index + track_shift) % len(music_files)
			total_duration, track_name = load_track(music_files, track_index, volume)
			elapsed = 0.0
			playback_state = "Playing"

		width, height = screen.get_size()
		background_scaled = pygame.transform.scale(background, (width, height))
		screen.blit(background_scaled, (0, 0))

		draw_vertical_gradient(screen, (*DARK_BG, 170), (*DARK_BG_2, 228))
		draw_soft_orbs(screen, ui_phase)

		stage_width = min(940, max(320, width - 48))
		stage_height = min(640, max(560, height - 38))
		stage_rect = pygame.Rect(0, 0, stage_width, stage_height)
		stage_rect.center = (width // 2, height // 2)

		stage_shadow = pygame.Surface((stage_rect.width + 34, stage_rect.height + 34), pygame.SRCALPHA)
		pygame.draw.rect(stage_shadow, (0, 0, 0, 130), stage_shadow.get_rect(), border_radius=30)
		screen.blit(stage_shadow, (stage_rect.x - 17, stage_rect.y + 6))

		draw_glass_panel(screen, stage_rect, radius=28)
		draw_led_frame(screen, stage_rect, led_phase)

		draw_header_icon(screen, (stage_rect.x + 42, stage_rect.y + 44))
		header_text = font_title.render("Music Lounge", True, TEXT_PRIMARY)
		screen.blit(header_text, (stage_rect.x + 72, stage_rect.y + 20))

		track_label = font_subtitle.render(featured_track_line, True, TEXT_PRIMARY)
		screen.blit(track_label, (stage_rect.x + 24, stage_rect.y + 78))

		player_box = pygame.Rect(stage_rect.x + 24, stage_rect.y + 124, stage_rect.width - 48, 250)
		draw_glass_panel(screen, player_box, radius=24)

		cover_rect = pygame.Rect(player_box.x + 20, player_box.y + 24, 104, 104)
		draw_album_cover(screen, cover_rect, ui_phase)

		title_text = font_subtitle.render(track_name, True, TEXT_PRIMARY)
		artist_text = font_small.render(artist_name, True, TEXT_SECONDARY)
		state_text = font_small.render(f"Estado: {playback_state}", True, TEXT_SECONDARY)
		screen.blit(title_text, (cover_rect.right + 20, player_box.y + 24))
		screen.blit(artist_text, (cover_rect.right + 20, player_box.y + 60))
		screen.blit(state_text, (cover_rect.right + 20, player_box.y + 82))

		progress = elapsed / total_duration if total_duration > 0 else 0.0
		progress_bar_rect = pygame.Rect(player_box.x + 20, player_box.y + 144, player_box.width - 40, 12)
		draw_progress_bar(screen, progress_bar_rect, progress)

		cur_time = format_time(elapsed)
		total_time = format_time(total_duration)
		time_left = font_small.render(cur_time, True, TEXT_SECONDARY)
		time_right = font_small.render(total_time, True, TEXT_SECONDARY)
		screen.blit(time_left, (progress_bar_rect.x, progress_bar_rect.bottom + 6))
		screen.blit(time_right, (progress_bar_rect.right - time_right.get_width(), progress_bar_rect.bottom + 6))

		control_y = player_box.y + 202
		center_x = player_box.centerx
		draw_button(screen, (center_x - 130, control_y), 16, "S", False, font_small)
		draw_button(screen, (center_x - 78, control_y), 20, "<<", False, font_small)
		draw_button(screen, (center_x, control_y), 28, "||" if playback_state == "Playing" else ">", True, font_controls)
		draw_button(screen, (center_x + 78, control_y), 20, ">>", False, font_small)
		draw_button(screen, (center_x + 130, control_y), 16, "R", False, font_small)

		volume_rect = pygame.Rect(player_box.right - 270, player_box.y + 28, 245, 22)
		draw_volume_slider(screen, volume_rect, volume, font_small)

		badge = pygame.Rect(player_box.right - 216, player_box.y + 64, 190, 42)
		pygame.draw.rect(screen, (36, 44, 67), badge, border_radius=14)
		pygame.draw.rect(screen, (95, 108, 140), badge, width=1, border_radius=14)
		is_playing = playback_state == "Playing"
		dot_radius = 5 + int(abs(math.sin(ui_phase * 5.0)) * 2) if is_playing else 5
		dot_color = PLAYING_GREEN if is_playing else (200, 127, 118)
		pygame.draw.circle(screen, dot_color, (badge.x + 16, badge.centery), dot_radius)
		badge_text = "Agora tocando" if is_playing else "Pausado"
		badge_label = font_small.render(badge_text, True, TEXT_PRIMARY)
		screen.blit(badge_label, (badge.x + 30, badge.y + 11))

		collapsed_height = 62
		expanded_height = 210
		shortcut_height = expanded_height if shortcuts_expanded else collapsed_height
		tutorial_box = pygame.Rect(stage_rect.x + 24, stage_rect.y + 390, stage_rect.width - 48, shortcut_height)
		draw_glass_panel(screen, tutorial_box, radius=18)

		tutorial_title = font.render("Controles e Atalhos", True, TEXT_PRIMARY)
		toggle_text = font_small.render("[H] expandir/recolher", True, TEXT_SECONDARY)
		screen.blit(tutorial_title, (tutorial_box.x + 20, tutorial_box.y + 14))
		screen.blit(toggle_text, (tutorial_box.right - toggle_text.get_width() - 18, tutorial_box.y + 18))

		if shortcuts_expanded:
			items = [
				("ESPACO", "play / pause"),
				("N / B", "proxima / anterior"),
				("T", "reinicia faixa"),
				("P / R", "pausa / retoma"),
				("<- / ->", "retrocede / avanca 5s"),
				("UP / DOWN", "volume"),
				("S", "sair"),
			]
			row_y = tutorial_box.y + 52
			for key_name, desc in items:
				row_rect = pygame.Rect(tutorial_box.x + 14, row_y, tutorial_box.width - 28, 24)
				draw_kbd(screen, row_rect, key_name, desc, font_small, font_small)
				row_y += 28

		footer_text = font_small.render(f"Playlist: {track_index + 1}/{len(music_files)} | Visual premium responsivo", True, TEXT_SECONDARY)
		screen.blit(footer_text, (stage_rect.x + 24, stage_rect.bottom - 28))

		pygame.display.flip()

	pygame.mixer.music.stop()
	pygame.quit()


if __name__ == "__main__":
	main()
