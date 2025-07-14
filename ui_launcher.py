import tkinter as tk
from tkinter import ttk
import threading
from render_bounce import generate_video

from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx
import os



def download_youtube_segment(url, start_time, end_time, crop_mode):
    print(f"[DEBUG] Téléchargement : {url}")
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.get_highest_resolution()
    print(f"[DEBUG] Stream sélectionné : {stream}")
    stream.download(filename="yt_video.mp4")

    clip = VideoFileClip("yt_video.mp4").subclip(start_time, end_time)
    clip = clip.resize(width=1080)

    if crop_mode == "Centered":
        clip = clip.fx(vfx.crop, height=960, y_center=clip.h / 2)
    elif crop_mode == "Top":
        clip = clip.fx(vfx.crop, height=960, y1=0)
    else:
        
        pass

    clip.write_videofile("video_top.mp4", codec="libx264")
    return "video_top.mp4"

def assemble_final_video(video_top_path, render_path):
    top = VideoFileClip(video_top_path)
    bottom = VideoFileClip(render_path)

    final = CompositeVideoClip([
        top.set_position(("center", "top")),
        bottom.set_position(("center", "bottom"))
    ], size=(1080, 1920))

    final.write_videofile("output_tiktok.mp4", codec="libx264", audio_codec="aac")

def start_render():
    button.config(state="disabled")
    status_var.set("🎬 Téléchargement et génération en cours...")
    progress_bar["value"] = 0

    def run():
        try:
            yt_link = yt_var.get().strip()
            start_time = start_time_var.get().strip()
            end_time = end_time_var.get().strip()
            crop_mode = crop_mode_var.get()

            
            status_var.set("Downloading Video...")
            video_path = download_youtube_segment(yt_link, start_time, end_time, crop_mode)

            
            status_var.set("Rendering...")
            params = {
                'gravity': float(gravity_var.get()),
                'velocity': float(velocity_var.get()),
                'radius': int(radius_var.get()),
                'growth': float(growth_var.get()),
                'duration': int(duration_var.get()),
                'fps': 60
            }

            def update_progress(val):
                progress_bar["value"] = val
                status_var.set(f"Progression : {val}%, encodage en cours...")

            def done_callback():
                status_var.set("Encoding...")
                assemble_final_video("video_top.mp4", "render.mp4")
                status_var.set("Video is ready...")
                button.config(state="normal")

            generate_video(params, progress_callback=update_progress, done_callback=done_callback)

        except Exception as e:
            status_var.set(f"Error: {e}")
            button.config(state="normal")

    threading.Thread(target=run, daemon=True).start()

# === INTERFACE ===

root = tk.Tk()
root.title("SatisEngine Beta")
root.geometry("700x760")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.configure("TEntry", font=("Segoe UI", 12))
style.configure("TProgressbar", thickness=20)

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

def add_field(label, var):
    ttk.Label(frame, text=label).pack(anchor="w")
    ttk.Entry(frame, textvariable=var).pack(fill="x", pady=5)


yt_var = tk.StringVar()
start_time_var = tk.StringVar(value="00:00")
end_time_var = tk.StringVar(value="00:20")
add_field("Youtube Link", yt_var)
add_field("Start time (ex: 00:30)", start_time_var)
add_field("End time (ex: 00:50)", end_time_var)


ttk.Label(frame, text="Video cropping :").pack(anchor="w", pady=(10,0))
crop_mode_var = tk.StringVar(value="Centered")
crop_combo = ttk.Combobox(frame, textvariable=crop_mode_var, values=["Centered", "Top"], state="readonly")
crop_combo.pack(fill="x", pady=5)


gravity_var = tk.StringVar(value="0.1")
velocity_var = tk.StringVar(value="2")
radius_var = tk.StringVar(value="15")
growth_var = tk.StringVar(value="1.5")
duration_var = tk.StringVar(value="20")

ttk.Label(frame, text="--- Ball parameters ---").pack(pady=5)
add_field("Gravity", gravity_var)
add_field("Default speed", velocity_var)
add_field("Default size", radius_var)
add_field("Growing by impact", growth_var)
add_field("Video length (seconds)", duration_var)

button = ttk.Button(frame, text="Start Rendering", command=start_render)
button.pack(pady=10)

progress_bar = ttk.Progressbar(frame, maximum=100, mode='determinate')
progress_bar.pack(fill="x", pady=10)

status_var = tk.StringVar()
status_label = ttk.Label(frame, textvariable=status_var, font=("Segoe UI", 10))
status_label.pack()

root.mainloop()

