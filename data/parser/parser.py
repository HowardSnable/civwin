import json
from mgz.model import parse_match, serialize

with open('./test1.aoe2record', 'rb') as h:
    match = parse_match(h)
    print(json.dumps(serialize(match), indent=2))