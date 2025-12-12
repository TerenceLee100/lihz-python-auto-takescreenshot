import os
from volcenginesdkarkruntime import Ark
import json
import datetime, os, pathlib

# 安装依赖：pip install 'volcengine-python-sdk[ark]'
# Get API Key：https://console.volcengine.com/ark/region:ark+cn-beijing/apikey
api_key = '' # os.getenv('ARK_API_KEY')

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=api_key,
)
word="laboratory"
en_explanation="A laboratory is a room where a scientist works."
en_example="My mother works in a laboratory."
# Create the first-round conversation request
# Doubao-Seed-1.6-flash     0.00007 - 0.0003            貌似这个最便宜
model = "doubao-seed-1-6-flash-250828"
# Doubao-Seed-1.6           0.0004 - 0.0012 元/千tokens                     
# model = "doubao-seed-1-6-251015"



response = client.response.create(
    model=model,
    input=f"""单词：{word}
    英文解释：{en_explanation}
    例句：{en_example}
    请根据上述信息给出该单词准确的中文解释以及词性，中文解释和词性用;隔开
    """
)
output = json.dumps(completions.model_dump(), ensure_ascii=False, indent=2)
print(output)

out_dir = pathlib.Path("out")
out_dir.mkdir(exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = out_dir / f"{timestamp}.json"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(output)


# response_format = {
#     "type": "json_object",
#     "json_schema": {
#         "type": "object",
#         "properties": {
#             "cn_explanation": {"type": "string", "description": "中文解释"},
#             "pos": {"type": "string", "description": "词性"}
#         },
#         "required": ["cn_explanation", "pos"]
#     }
# }
# completions = client.chat.completions.parse(
#     model=model,
#     messages=[
#         {
#             "role": "user",
#             "content": f"""单词：{word}
#             英文解释：{en_explanation}
#             例句：{en_example}
#             请根据上述信息给出该单词准确的中文解释以及词性，中文解释和词性用;隔开
#             """
#         }
#     ],
#     response_format=response_format,
#     extra_body={
#          "thinking": {
#              "type": "disabled" # 不使用深度思考能力
#              # "type": "enabled" # 使用深度思考能力
#          }
#      }
# )
# output = json.dumps(completions.model_dump(), ensure_ascii=False, indent=2)
# print(output)

# out_dir = pathlib.Path("out")
# out_dir.mkdir(exist_ok=True)
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# file_path = out_dir / f"{timestamp}.json"
# with open(file_path, "w", encoding="utf-8") as f:
#     f.write(output)

