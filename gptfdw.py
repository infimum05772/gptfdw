import json
import urllib3

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres

BASE_URL = "https://bothub.chat/api/v1/openai/v1/chat/completions"
MODEL = "gpt-3.5-turbo-16k"
DEFAULT_TEMP = 0.7


class gptfdw(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(gptfdw, self).__init__(options, columns)
        self.access_token = options.get('access_token', '')

    def execute(self, quals, columns, sortkeys=None):
        http = urllib3.PoolManager()
        log_to_postgres(quals)

        query = 'Hello! How are you?'
        temp = DEFAULT_TEMP
        for qual in quals:
            if qual.field_name == 'query' and qual.operator == '=':
                query = qual.value
            if qual.field_name == 'temp' and qual.operator == '=':
                temp = qual.value

        if self.access_token == '':
            log_to_postgres('NOT AUTHORIZED')

        body = json.dumps({'model': MODEL,
                           'messages': [{'role': 'user', 'content': query}],
                           'temperature': temp})
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Accept-Charset': 'utf-8',
                   'Authorization': f'Bearer {self.access_token}'}
        r = http.request('POST', BASE_URL, body, headers=headers)
        log_to_postgres(body)

        j = json.loads(r.data)
        rows = []
        try:
            row = {'content': j['choices'][0]['message']['content'],
                   'model': j['model'],
                   'prompt_tokens': j['usage']['prompt_tokens'],
                   'completion_tokens': j['usage']['completion_tokens'],
                   'total_tokens': j['usage']['total_tokens']}
        except KeyError:
            row = {'error': j['error']['message']}
        rows.append(row)
        return rows
