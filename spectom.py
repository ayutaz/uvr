import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import librosa
import argparse

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description='MP3ファイルのFFT解析')
parser.add_argument('file_path', type=str, help='解析するMP3ファイルのパス')
args = parser.parse_args()

# MP3ファイルの読み込み
file_path = args.file_path
data, sample_rate = librosa.load(file_path, sr=None)

# FFTの実行
N = len(data)
fft_data = np.fft.fft(data)
fft_freq = np.fft.fftfreq(N, 1/sample_rate)

# 正の周波数成分のみを抽出
positive_freqs = fft_freq[:N // 2]
positive_fft_data = np.abs(fft_data[:N // 2])

# プロット
plt.figure(figsize=(10, 6))
plt.plot(positive_freqs, positive_fft_data)
plt.xlabel('周波数 [Hz]', fontsize=10)
plt.ylabel('振幅', fontsize=10)
plt.title('FFTによる周波数スペクトル', fontsize=12)
plt.grid(True)
plt.show()