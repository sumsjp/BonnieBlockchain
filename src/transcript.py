import google.generativeai as genai
import os
from dotenv import load_dotenv
from lib.mylog import setup_logger

# 設定 logger
logger = setup_logger('youtube_update')

load_dotenv()
def make_transcript(video_id: str):
    input_file = f"subtitle/{video_id}.txt"
    output_file = f"../transcript/{video_id}.md"  

    # 1. 設定 Gemini API 金鑰
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    # 2. 選擇 Gemini 模型
    model = genai.GenerativeModel('gemini-2.0-flash')  # 或 'gemini-2.0-pro' 或 'gemini-2.0-flash'

    # 3. 讀取檔案內容
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            input_text = f.read()
    except FileNotFoundError:
        logger.error(f"找不到檔案：{input_file}")
        return
    except Exception as e:
        logger.error(f"讀取檔案時發生錯誤：{e}")
        return

    # 4. 建立 Prompt
    prompt = f"請將以下文字翻譯成繁體中文，保持上文連貫性，並且保持原義。若是已是繁體中文，請重新排版：\n\n{input_text}"

    # 5. 設定 Generate Content Config
    generation_config = genai.types.GenerationConfig(
        temperature=0.1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
    )

    safety_settings = [
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },
    ]

    # 6. 翻譯並寫入檔案 (Streaming 模式)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            response_stream = model.generate_content(
                prompt,
                stream=True,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            for chunk in response_stream:
                # logger.debug(chunk.text)  # 如果需要詳細除錯資訊
                f.write(chunk.text)
        logger.info(f"已寫入 {output_file}")
    except Exception as e:
        os.remove(output_file)  # 如果發生錯誤，刪除部分完成的檔案
        logger.error(f"翻譯或寫入檔案時發生錯誤：{e}")

# 範例用法：
if __name__ == "__main__":
    make_transcript('nku9Du2Zvu8')  # 處理 input/n01.txt
