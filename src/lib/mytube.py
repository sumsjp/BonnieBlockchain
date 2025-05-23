from yt_dlp import YoutubeDL
import requests
import re
import os
import whisper
import torch
from .mylog import setup_logger

# 設定 logger
logger = setup_logger('youtube_update')

def get_video_list(channel_url):
    """
    取得 YouTube 頻道的影片清單
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'dump_single_json': True,
        'playlistend': 10  # 只取最新的10筆
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            channel_info = ydl.extract_info(channel_url, download=False)
        
        video_info = channel_info.get('entries', [])
        logger.info(f"成功取得頻道影片清單，共 {len(video_info)} 部影片")
        return video_info
    except Exception as e:
        logger.error(f"取得影片清單失敗: {str(e)}")
        return []

def format_date(date):
    return f"{date[:4]}-{date[4:6]}-{date[6:]}" if date != 'unknown' else date

def get_upload_date(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'quiet': True,  # 不顯示多餘的日誌
        'extract_flat': True  # 只提取影片資訊，不下載
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        date = info.get("upload_date", "unknown")        
        return format_date(date)

def download_subtitle(video_id, preferred_langs):
    info_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,  # 若無手動字幕則下載自動字幕
        'subtitleslangs': preferred_langs,  # 指定字幕語言（可調整）
        'subtitlesformat': 'json3',  # 使用json3 (srv3) 格式
    }
            
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    with YoutubeDL(info_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        
    title = video_info.get('title')
    upload_date = video_info.get('upload_date')
    formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}" if upload_date else '未知日期'

    logger.info(f"影片標題：{title}")
    logger.info(f"上傳日期：{formatted_date}")

    subtitles = video_info.get('subtitles', {}) or video_info.get('automatic_captions', {})
    if not subtitles:
        logger.warning(f"無可用字幕：{video_id}")
        return "", ""
    
    selected_lang = None
    for lang in preferred_langs:
        if lang in subtitles:
            selected_lang = lang
            break

    if not selected_lang:
        selected_lang = list(subtitles.keys())[0]
        
    sub_url = subtitles[selected_lang][0]['url']
    subtitle_json = requests.get(sub_url).json()

    # 從JSON中抽取完整句子且避免重複
    subtitle_text = ''
    last_text = ''
    for event in subtitle_json['events']:
        if 'segs' in event:
            line_text = ''.join(seg.get('utf8', '') for seg in event['segs']).strip()
            
            # 避免重複
            if line_text and line_text != last_text:
                line_text = re.sub(r'\s+', ' ', line_text).strip() 
                subtitle_text += line_text + '\n'
                last_text = line_text

    return subtitle_text, formatted_date

def download_video_file(video_id, video_dir):
    """
    下載 YouTube 影片檔案
    Args:
        video_id (str): YouTube 影片 ID
    Returns:
        str: 影片檔案路徑，失敗則返回空字串
    """
    # 設定下載選項
    video_opts = {
        'format': 'bestaudio[ext=webm]/bestaudio/best',  # 優先選擇 webm 格式
        'outtmpl': '%(id)s.%(ext)s',  # 輸出檔案名稱格式
        'quiet': True
    }

    try:
        # 確保影片目錄存在
        os.makedirs(video_dir, exist_ok=True)

        # 設定完整的輸出路徑
        video_opts['outtmpl'] = os.path.join(video_dir, video_opts['outtmpl'])
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        with YoutubeDL(video_opts) as ydl:
            ydl.download([video_url])
            
        output_file = os.path.join(video_dir, f"{video_id}.webm")
        logger.info(f"download_video_file: 影片下載完成：{output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"download_video_file: 影片下載失敗 {video_id}: {str(e)}")
        return ""

def convert_script(video_file, output_file):
    """
    使用 Whisper 將影片檔案轉換為文字稿
    """
    try:
        # 檢查 CUDA 是否可用
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"使用設備: {device}")
        
        # 載入 Whisper 模型
        model = whisper.load_model("medium").to(device)
        
        # 執行轉換
        logger.info(f"開始轉換影片：{video_file}")
        result = model.transcribe(
            video_file,
            task="transcribe",
            verbose=True,
            fp16=(device == "cuda")
        )
            
        # 儲存文字稿
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        logger.info(f"文字稿已儲存：{output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"轉換失敗 {video_file}: {str(e)}")
        return ""


