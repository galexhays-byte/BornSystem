import json
import urllib.request
import urllib.parse

query = 'security automation agent tool'
url = 'https://api.github.com/search/repositories?q=' + urllib.parse.quote(query) + '+in:name,description&sort=stars&order=desc&per_page=15'
req = urllib.request.Request(url, headers={'User-Agent': 'GitHubSearch'})
with urllib.request.urlopen(req, timeout=15) as response:
    data = json.load(response)
for item in data.get('items', []):
    print(item['full_name'] + ' | ' + item['html_url'] + ' | ' + (item.get('description') or '').replace('\n', ' '))
