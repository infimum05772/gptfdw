import json
import urllib3

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres

BASE_URL = "https://bothub.chat/api/v1/openai/v1/chat/completions"
MODEL = "gpt-3.5-turbo-16k"


class gptfdw(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(gptfdw, self).__init__(options, columns)
        self.access_token = options.get('access_token', '')

    def execute(self, quals, columns, sortkeys=None):
        http = urllib3.PoolManager()
        log_to_postgres(quals)

        query = 'Hello! How are you?'
        for qual in quals:
            if qual.field_name == 'query' and qual.operator == '=':
                query = qual.value

        body = json.dumps({'messages': [{'role': 'user', 'content': query}], 'model': MODEL})
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Accept-Charset': 'utf-8',
                   'Authorization': f'Bearer {self.access_token}'}
        r = http.request('POST', BASE_URL, body, headers=headers)
        log_to_postgres(body)

        j = json.loads(r.data)
        rows = []
        row = {'content': j['choices'][0]['message']['content']}
        rows.append(row)
        return rows
