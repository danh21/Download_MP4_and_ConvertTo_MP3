import os
import sys
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import yt_dlp


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller onefile exe."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def app_dir():
    """Directory where the exe/script itself lives (for storing cookies/archive/output next to it)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist -> MP3")
        self.root.geometry("720x520")
        self.root.minsize(600, 420)

        self.msg_queue = queue.Queue()
        self.is_running = False
        self.stop_requested = False

        base = app_dir()
        self.default_output = os.path.join(base, "playlist")
        self.default_cookie = os.path.join(base, "www.youtube.com_cookies.txt")
        self.default_archive = os.path.join(base, "downloaded.txt")

        self._build_ui()
        self.root.after(150, self._poll_queue)

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        frm_top = ttk.Frame(self.root)
        frm_top.pack(fill="x", **pad)

        ttk.Label(frm_top, text="Playlist URL:").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(frm_top, textvariable=self.url_var, width=70)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=4)

        ttk.Label(frm_top, text="Output folder:").grid(row=1, column=0, sticky="w")
        self.output_var = tk.StringVar(value=self.default_output)
        ttk.Entry(frm_top, textvariable=self.output_var, width=55).grid(
            row=1, column=1, sticky="we", padx=4
        )
        ttk.Button(frm_top, text="Browse...", command=self._browse_output).grid(
            row=1, column=2, sticky="w"
        )

        ttk.Label(frm_top, text="Cookie file (optional):").grid(row=2, column=0, sticky="w")
        self.cookie_var = tk.StringVar(value=self.default_cookie)
        ttk.Entry(frm_top, textvariable=self.cookie_var, width=55).grid(
            row=2, column=1, sticky="we", padx=4
        )
        ttk.Button(frm_top, text="Browse...", command=self._browse_cookie).grid(
            row=2, column=2, sticky="w"
        )

        self.skip_downloaded_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frm_top,
            text="Skip songs already downloaded before (recommended)",
            variable=self.skip_downloaded_var,
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(4, 0))

        frm_top.columnconfigure(1, weight=1)

        frm_btn = ttk.Frame(self.root)
        frm_btn.pack(fill="x", **pad)
        self.start_btn = ttk.Button(frm_btn, text="Download", command=self._on_start)
        self.start_btn.pack(side="left")
        self.stop_btn = ttk.Button(
            frm_btn, text="Stop", command=self._on_stop, state="disabled"
        )
        self.stop_btn.pack(side="left", padx=6)

        self.progress = ttk.Progressbar(frm_btn, mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True, padx=8)

        self.overall_lbl = ttk.Label(frm_btn, text="")
        self.overall_lbl.pack(side="left")

        frm_log = ttk.Frame(self.root)
        frm_log.pack(fill="both", expand=True, **pad)
        ttk.Label(frm_log, text="Status:").pack(anchor="w")

        self.log_text = tk.Text(frm_log, wrap="word", state="disabled", height=18)
        self.log_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(frm_log, command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

    def _browse_output(self):
        d = filedialog.askdirectory()
        if d:
            self.output_var.set(d)

    def _browse_cookie(self):
        f = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if f:
            self.cookie_var.set(f)

    # ---------- log helpers ----------
    def _log(self, text):
        self.msg_queue.put(("log", text))

    def _set_progress(self, current, total):
        self.msg_queue.put(("progress", (current, total)))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == "log":
                    self.log_text.configure(state="normal")
                    self.log_text.insert("end", payload + "\n")
                    self.log_text.see("end")
                    self.log_text.configure(state="disabled")
                elif kind == "progress":
                    current, total = payload
                    self.progress["maximum"] = max(total, 1)
                    self.progress["value"] = current
                    self.overall_lbl.configure(text=f"{current}/{total}")
                elif kind == "done":
                    self._on_finished(payload)
        except queue.Empty:
            pass
        self.root.after(150, self._poll_queue)

    # ---------- start/stop ----------
    def _on_start(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a playlist URL.")
            return

        output_path = self.output_var.get().strip() or self.default_output
        os.makedirs(output_path, exist_ok=True)
        cookie_path = self.cookie_var.get().strip()
        skip_downloaded = self.skip_downloaded_var.get()

        self.is_running = True
        self.stop_requested = False
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress["value"] = 0
        self.overall_lbl.configure(text="")
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        t = threading.Thread(
            target=self._run_download,
            args=(url, output_path, cookie_path, skip_downloaded),
            daemon=True,
        )
        t.start()

    def _on_stop(self):
        self.stop_requested = True
        self._log("Stop requested — will halt after the current video finishes...")
        self.stop_btn.configure(state="disabled")

    def _on_finished(self, summary):
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self._log(summary)
        messagebox.showinfo("Done", summary)

    # ---------- download worker (runs in background thread) ----------
    def _run_download(self, url, output_path, cookie_path, skip_downloaded):
        outtmpl = os.path.join(output_path, "%(title)s.%(ext)s")
        archive_path = self.default_archive

        def progress_hook(d):
            if self.stop_requested:
                raise yt_dlp.utils.DownloadError("Stopped by user")
            if d.get("status") == "downloading":
                filename = os.path.basename(d.get("filename", ""))
                pct = d.get("_percent_str", "").strip()
                self._log(f"Downloading {filename} ... {pct}")
            elif d.get("status") == "finished":
                self._log(f"Converting {os.path.basename(d.get('filename',''))} to mp3 ...")

        counters = {"index": 0, "total": 0, "ok": 0, "skipped": 0, "failed": 0}

        def postprocessor_hook(d):
            if d.get("status") == "finished":
                counters["ok"] += 1

        class Logger:
            def debug(_self, msg):
                if msg.startswith("[download] Downloading item"):
                    self._log(msg)
                    try:
                        parts = msg.split()
                        idx = int(parts[3])
                        tot = int(parts[5])
                        counters["index"] = idx
                        counters["total"] = tot
                        self._set_progress(idx - 1, tot)
                    except Exception:
                        pass
                elif "has already been recorded in the archive" in msg:
                    counters["skipped"] += 1
                    self._log(msg)

            def info(_self, msg):
                pass

            def warning(_self, msg):
                self._log("WARNING: " + msg)

            def error(_self, msg):
                counters["failed"] += 1
                self._log("ERROR: " + msg)

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "ignoreerrors": True,
            "logger": Logger(),
            "progress_hooks": [progress_hook],
            "postprocessor_hooks": [postprocessor_hook],
        }
        if skip_downloaded:
            ydl_opts["download_archive"] = archive_path
        if cookie_path and os.path.isfile(cookie_path):
            ydl_opts["cookiefile"] = cookie_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self._log(f"Stopped: {e}")

        if counters["total"]:
            self._set_progress(counters["total"], counters["total"])

        summary = (
            f"Finished. Downloaded: {counters['ok']}, "
            f"Skipped (already downloaded): {counters['skipped']}, "
            f"Failed: {counters['failed']}"
        )
        self.msg_queue.put(("done", summary))


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    app = DownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()