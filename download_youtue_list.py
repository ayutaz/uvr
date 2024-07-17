import yt_dlp
import os

def download_playlist_audio(url, output_path='./%(playlist)s/%(title)s.%(ext)s'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'ignoreerrors': True,  # エラーが発生しても続行
        'nooverwrites': True,  # 既存のファイルを上書きしない
        'playlist_items': '',  # すべての動画をダウンロード
        'writethumbnail': False,  # サムネイルも保存
        'embed-thumbnail': False,  # サムネイルを音声ファイルに埋め込む
        
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            playlist_title = info['title']
            print(f"プレイリスト '{playlist_title}' のダウンロードを開始します。")
            
            ydl.download([url])
            print(f"プレイリスト '{playlist_title}' のダウンロードが完了しました。")
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")

# 使用例
playlist_url = input("YouTubeプレイリストのURLを入力してください: ")
download_playlist_audio(playlist_url)