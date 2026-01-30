from volcenginesdkarkruntime import Ark
import os
import pandas as pd
import openpyxl
from pathlib import Path
from pydantic import BaseModel  # 用于定义响应解析模型

# 初始化方舟SDK客户端
client = Ark(
    # 从环境变量获取方舟API Key（需提前设置环境变量）
    api_key=os.getenv('ARK_API_KEY'),
)

# 定义最终响应模型（包含分步过程和最终答案）
class MathResponse(BaseModel):
    cn_explanation: str
    pos: str

# word="laboratory"
# en_explanation="A laboratory is a room where a scientist works."
# en_example="My mother works in a laboratory."

word="binoculars"
en_explanation="<i>Binoculars</i> are a device used for seeing things that are far away."
en_example="He could see the ship on the horizon only if he used his <b>binoculars</b>."

# 确保输出目录存在
Path("out").mkdir(exist_ok=True)

# 读取Excel文件
df = pd.read_excel("英语单词/4000核心单词（小样儿）.xlsx", header=None, names=["word", "en_explanation", "en_example"])

# 遍历每一行数据
for idx, row in df.iterrows():
    word = row["word"]
    en_explanation = row["en_explanation"]
    en_example = row["en_example"]

    # 调用方舟模型生成响应（自动解析为指定模型）
    completion = client.beta.chat.completions.parse(
        model="doubao-seed-1-6-flash-250828",  # 具体模型需替换为实际可用模型
        messages=[
            {
                "role": "user",
                "content": f"""单词：{word}
                英文解释：{en_explanation}
                例句：{en_example}
                请根据上述信息给出该单词准确的中文解释以及词性，中文解释尽量简明扼要（尽量不超过10个字），词性用中文表示
                """
            }
        ],
        response_format=MathResponse,  # 指定响应解析模型
        extra_body={
             "thinking": {
                 "type": "disabled" # 不使用深度思考能力
                 # "type": "enabled" # 使用深度思考能力
             }
         }
    )

    # 提取解析后的结构化响应
    resp = completion.choices[0].message.parsed

    # 将结果写入新列
    df.at[idx, "cn_explanation"] = resp.cn_explanation
    df.at[idx, "pos"] = resp.pos

# 保存结果到out目录
df.to_excel("out/4000核心单词（小样儿）_with_cn.xlsx", index=False, header=False)




# # 调用方舟模型生成响应（自动解析为指定模型）
# completion = client.beta.chat.completions.parse(
#     model="doubao-seed-1-6-flash-250828",  # 具体模型需替换为实际可用模型
#     messages=[
#         {
#             "role": "user",
#             "content": f"""单词：{word}
#             英文解释：{en_explanation}
#             例句：{en_example}
#             请根据上述信息给出该单词准确的中文解释以及词性，中文解释尽量简明扼要（尽量不超过10个字），词性用中文表示
#             """
#         }
#     ],
#     response_format=MathResponse,  # 指定响应解析模型
#     extra_body={
#          "thinking": {
#              "type": "disabled" # 不使用深度思考能力
#              # "type": "enabled" # 使用深度思考能力
#          }
#      }
# )

# # 提取解析后的结构化响应
# resp = completion.choices[0].message.parsed

# # 打印格式化的JSON结果
# print(resp.model_dump_json(indent=2))