import yt_dlp

def download_playlist(url, output_path='./%(playlist)s/%(title)s.%(ext)s'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'ignoreerrors': True,  # エラーが発生しても続行
        'nooverwrites': True,  # 既存のファイルを上書きしない
        'playlist_items': '',  # すべての動画をダウンロード
        'writethumbnail': True,  # サムネイルも保存
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("プレイリストのダウンロードが完了しました。")
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")

# 使用例
playlist_url = input("YouTubeプレイリストのURLを入力してください: ")
download_playlist(playlist_url)