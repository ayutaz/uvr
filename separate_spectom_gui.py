import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd
import tempfile
import os
import matplotlib
import threading
matplotlib.use('TkAgg')
matplotlib.rcParams['font.family'] = 'MS Gothic'  # 日本語フォントの設定

playing = False
current_audio_type = None
play_thread = None
stop_flag = False

def process_audio():
    input_file = file_path.get()
    low_freq = int(low_freq_entry.get())
    high_freq = int(high_freq_entry.get())

    global sample_rate, original_data, filtered_data
    sample_rate, data = wavfile.read(input_file)
    
    # データを-1.0から1.0の範囲に正規化し、float32に変換
    original_data = (data.astype(np.float32) / np.max(np.abs(data))).astype(np.float32)
    
    if original_data.ndim == 2:
        original_data = original_data.mean(axis=1)

    N = len(original_data)
    fft_data = np.fft.rfft(original_data)
    fft_freq = np.fft.rfftfreq(N, 1/sample_rate)

    # バンドパスフィルタを作成
    filter_mask = (fft_freq >= low_freq) & (fft_freq <= high_freq)

    # フィルタを適用
    filtered_fft = fft_data * filter_mask

    # 逆フーリエ変換を適用
    filtered_data = np.fft.irfft(filtered_fft)

    # フィルタリング後のデータを-1.0から1.0の範囲に正規化
    filtered_data = (filtered_data / np.max(np.abs(filtered_data))).astype(np.float32)

    # スペクトルのプロット用データを準備
    positive_fft_data = np.abs(fft_data)
    filtered_positive_fft_data = np.abs(filtered_fft)

    plot_spectrum(fft_freq, positive_fft_data, filtered_positive_fft_data)

def plot_spectrum(freqs, orig_fft_data, filt_fft_data):
    for widget in frame.winfo_children():
        widget.destroy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(freqs, orig_fft_data)
    ax1.set_xlabel('周波数 [Hz]')
    ax1.set_ylabel('振幅')
    ax1.set_title('元のスペクトル')
    ax1.grid(True)

    ax2.plot(freqs, filt_fft_data)
    ax2.set_xlabel('周波数 [Hz]')
    ax2.set_ylabel('振幅')
    ax2.set_title('フィルタリング後のスペクトル')
    ax2.grid(True)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ボタンを追加
    button_frame = tk.Frame(frame)
    button_frame.pack(fill=tk.X, expand=True)
    
    global original_button, filtered_button
    original_button = tk.Button(button_frame, text="元の音声を再生", command=lambda: play_stop('original'))
    original_button.pack(side=tk.LEFT, expand=True)
    
    filtered_button = tk.Button(button_frame, text="処理後の音声を再生", command=lambda: play_stop('filtered'))
    filtered_button.pack(side=tk.RIGHT, expand=True)

def select_file():
    filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    file_path.set(filename)

def play_audio(data):
    global playing, stop_flag
    # データを float32 に変換
    data = data.astype(np.float32)
    with sd.OutputStream(samplerate=sample_rate, channels=1, dtype=np.float32) as stream:
        stream.start()
        chunk_size = 1024
        for i in range(0, len(data), chunk_size):
            if stop_flag:
                break
            chunk = data[i:i+chunk_size]
            stream.write(chunk)
    playing = False
    stop_flag = False
    root.after(0, audio_finished)

def play_stop(audio_type):
    global playing, current_audio_type, play_thread, stop_flag
    if not playing:
        if 'original_data' in globals() and 'filtered_data' in globals():
            playing = True
            current_audio_type = audio_type
            data = original_data if audio_type == 'original' else filtered_data
            update_button_text(audio_type, "停止")
            stop_flag = False
            play_thread = threading.Thread(target=play_audio, args=(data,))
            play_thread.start()
        else:
            messagebox.showwarning("警告", "まず音声を処理してください。")
    else:
        stop_flag = True
        sd.stop()

def audio_finished():
    global playing, current_audio_type
    playing = False
    update_button_text(current_audio_type, "再生")
    current_audio_type = None

def update_button_text(audio_type, text):
    if audio_type == 'original':
        original_button.config(text=f"元の音声を{text}")
    else:
        filtered_button.config(text=f"処理後の音声を{text}")

# メインウィンドウの作成
root = tk.Tk()
root.title("音声スペクトル編集")

file_path = tk.StringVar()

tk.Label(root, text="音声ファイル:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=file_path, width=50).grid(row=0, column=1)
tk.Button(root, text="参照", command=select_file).grid(row=0, column=2)

tk.Label(root, text="周波数下限:").grid(row=1, column=0, sticky="e")
low_freq_entry = tk.Entry(root)
low_freq_entry.grid(row=1, column=1)
low_freq_entry.insert(0, "500")

tk.Label(root, text="周波数上限:").grid(row=2, column=0, sticky="e")
high_freq_entry = tk.Entry(root)
high_freq_entry.grid(row=2, column=1)
high_freq_entry.insert(0, "2500")

tk.Button(root, text="処理開始", command=process_audio).grid(row=3, column=0, columnspan=3)

frame = tk.Frame(root)
frame.grid(row=4, column=0, columnspan=3)

root.mainloop()