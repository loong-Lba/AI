import os


qwen_model_name = os.getenv('QWEN_MODEL_NAME', 'qwen3.7-plus')
qwen_api_key = os.getenv("DASHSCOPE_API_KEY")
qwen_base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")