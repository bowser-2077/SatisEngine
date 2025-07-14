import pygame
import math
from moviepy.editor import ImageSequenceClip

def rgb_color(t):
    r = int(127 + 128 * math.sin(t))
    g = int(127 + 128 * math.sin(t + 2))
    b = int(127 + 128 * math.sin(t + 4))
    return (r, g, b)

def generate_video(params, progress_callback=None, done_callback=None):
    WIDTH, HEIGHT = 1000, 1000
    CENTER = WIDTH // 2, HEIGHT // 2
    ARENA_RADIUS = 500
    FPS = params['fps']

    pygame.init()
    screen = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball_pos = [CENTER[0], CENTER[1] - 100]
    ball_vel = [params['velocity'], 0]
    ball_radius = params['radius']
    ball_growth = params['growth']
    gravity = params['gravity']

    frames = []
    duration = params['duration']
    total_frames = duration * FPS

    for frame_num in range(total_frames):
        t = frame_num / FPS
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), CENTER, ARENA_RADIUS, 2)
        ball_vel[1] += gravity
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        dx = ball_pos[0] - CENTER[0]
        dy = ball_pos[1] - CENTER[1]
        dist = math.hypot(dx, dy)

        if dist + ball_radius >= ARENA_RADIUS:
            nx = dx / dist
            ny = dy / dist
            overlap = (dist + ball_radius) - ARENA_RADIUS
            ball_pos[0] -= nx * overlap
            ball_pos[1] -= ny * overlap

            dot = ball_vel[0]*nx + ball_vel[1]*ny
            ball_vel[0] -= 2 * dot * nx
            ball_vel[1] -= 2 * dot * ny

            ball_radius += ball_growth

        color = rgb_color(t * 3)
        pygame.draw.circle(screen, color, (int(ball_pos[0]), int(ball_pos[1])), int(ball_radius))

        frame = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        frames.append(frame)

        if progress_callback:
            progress_callback(int((frame_num + 1) / total_frames * 100))

    clip = ImageSequenceClip(frames, fps=FPS)
    clip.write_videofile("render.mp4", codec="libx264", audio=False)

    if done_callback:
        done_callback()
