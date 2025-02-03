import requests

payload = {
  "mode": "preview",
  "prompt": "a monster mask",
  "art_style": "realistic",
  "should_remesh": True
}

api_key = "msy_pPutuGaeuHDVtvLoiLihmAMFtfwWseTih7iD"

headers = {
  "Authorization": f"Bearer {api_key}"
}

response = requests.post(
  "https://api.meshy.ai/openapi/v2/text-to-3d",
  headers=headers,
  json=payload,
)
response.raise_for_status()
print(response.json())
