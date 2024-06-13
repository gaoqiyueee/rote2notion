import os
import requests
import json

# 获取环境变量
notion_api_key = os.getenv('NOTION_API_KEY')
notion_database_id = os.getenv('NOTION_DATABASE_ID')
rote_api_key = os.getenv('ROTE_API_KEY')

# 从“rote.ink”获取内容
rote_api_url = "https://api.rote.ink/v1/api/openkey/onerote"
params = {
    "openkey": rote_api_key
}

response = requests.get(rote_api_url, params=params)

if response.status_code == 200:
    rote_content = response.json()
else:
    print("Failed to retrieve content from rote.ink:", response.status_code)
    exit(1)

# 假设rote_content是一个包含多个条目的列表
# 这里需要根据实际API返回的格式进行调整
# 假设API返回的是一个单条目（字典）

notion_api_url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 数据结构根据Notion数据库的设置进行调整
# 假设Notion数据库中有 "Content" 和 "Tags" 两个属性

data = {
    "parent": { "database_id": notion_database_id },
    "properties": {
        "Content": {
            "rich_text": [
                {
                    "text": {
                        "content": rote_content.get("content", "No Content")
                    }
                }
            ]
        },
        "Tags": {
            "multi_select": [
                {"name": tag} for tag in rote_content.get("tag", [])
            ]
        }
    }
}

response = requests.post(notion_api_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Content successfully added to Notion.")
else:
    print("Failed to add content to Notion:", response.status_code, response.text)
