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

notion_api_url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 数据结构根据Notion数据库的设置进行调整
data = {
    "parent": { "database_id": notion_database_id },
    "properties": {
        "title": {
            "title": [
                {
                    "text": {
                        "content": rote_content.get("title", "No Title")
                    }
                }
            ]
        }
    },
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": rote_content.get("content", "No Content")
                        }
                    }
                ]
            }
        }
    ]
}

response = requests.post(notion_api_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Content successfully added to Notion.")
else:
    print("Failed to add content to Notion:", response.status_code, response.text)
