# SatisEngine

SatisEngine is a lightweight multimedia interface layer built for automating short-form content generation, typically used for creating vertical videos with overlays, timed transitions, and YouTube segment integration.

Designed with modularity and clarity in mind, it's optimized for developers building creative or automated media pipelines. All rendering and orchestration is driven through Python scripts with detailed logs and multithreaded UI updates.

## Description

SatisEngine lets you script the creation of short video content using YouTube segments, bounce animations, and overlays. It's especially useful for automating TikTok or Shorts-style clips, with preconfigured timings and visual effects.

The engine handles:
- Downloading and clipping YouTube videos
- Adding custom animations or bounce effects
- Compositing overlays
- Rendering the final result via [MoviePy](https://zulko.github.io/moviepy/)

## Notable Technologies Used

- [`pytubefix`](https://github.com/pytube/pytube) – A maintained fork of PyTube, used for downloading YouTube videos with support for patched endpoints.
- [`moviepy`](https://zulko.github.io/moviepy/) – Python video editing, compositing and effects.
- [`threading`](https://docs.python.org/3/library/threading.html) – Used to handle UI responsiveness during render/download operations.

## Project Structure

```
.
├── ui_launcher.py
├── render_bounce.py
├── assets/
│   ├── images/
│   └── fonts/
├── segments/
├── output/
├── temp/
└── config/
```

### Directory Breakdown

- `assets/`: Holds static resources such as overlay images or custom fonts.
- `segments/`: Stores trimmed video segments pulled from YouTube.
- `output/`: Final exported videos.
- `temp/`: Working files during rendering; auto-cleaned after session.
- `config/`: Optional JSON or INI files for defining sequences or parameters


### This readme will be used as a roadmap.
