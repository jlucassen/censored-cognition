from json import loads

import backoff


def load_jsonl(path: str):
    with open(path, "r") as f:
        return [loads(line) for line in f.readlines()]


def complete_with_backoff(client, **kwargs):
    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def complete():
        return client.chat.completions.create(**kwargs)

    return complete()
