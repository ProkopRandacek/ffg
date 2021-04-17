import base64, json, zlib
from pprint import pprint
from copy import deepcopy

bp = "0eNpFjlsOgjAQRfcy34VIKaLdijGGx0SbwJS0A0pI924LiX7OzT3nzgbtMOPkDDHoDUxnyYO+beDNk5ohZbxOCBoW43iOiQBqxhQcjay3DEGAoR4/oItwF4DEhg0eov1YHzSPLbpY+PFva3ukrHuh52idrI+QpTQZRdlF5pWANRKFyquQvIZxjOD/YwELOr9D8lKo+irr8qzUqZQhfAGtj0cm"
emptyBP = json.loads(zlib.decompress(base64.b64decode(bp[1:])).decode("utf8"))
emptyBP["blueprint"]["entities"] = []


class BP:
    bp: dict
    entityNumber = 1

    def __init__(self):
        self.bp = deepcopy(emptyBP)
        self.entityNumber = 1

    def reset(self):
        self.entityNumber = 1
        self.bp = deepcopy(emptyBP)

    def importFromString(self, bpString):
        self.bp = json.loads(
            zlib.decompress(base64.b64decode(bpString[1:])).decode("utf8")
        )

    def export(self):
        return "0" + base64.b64encode(
            zlib.compress(bytes(json.dumps(self.bp), "utf8"))
        ).decode("utf8")

    def addEntity(self, name, x, y, recipe="", direction="", type="", ccitem=""):
        self.bp["blueprint"]["entities"].append(
            {
                "entity_number": self.entityNumber,
                "name": name,
                "position": {"x": x + 0.5, "y": y + 0.5},
            }
        )
        if recipe != "":
            self.bp["blueprint"]["entities"][-1]["recipe"] = recipe
        if direction != "":
            self.bp["blueprint"]["entities"][-1]["direction"] = direction
        if type != "":
            self.bp["blueprint"]["entities"][-1]["type"] = type
        if ccitem != "":  # create constant combinator with one item in it
            self.bp["blueprint"]["entities"][-1]["control_behavior"] = {
                "filters": [
                    {"count": 1, "index": 1, "signal": {"name": ccitem, "type": "item"}}
                ]
            }
        self.entityNumber += 1


if __name__ == "__main__":
    bp = BP()
    bp.importFromString(
        "0eNqNkEtuwzAMRO8yazmoP6lTXaUoAtlhWwIyZch0UMPQ3SvFm6yKLknMvOFwx+BXmiOLwu7gMcgC+75j4S9xvux0mwkWrDTBQNxUpqJTJ1qNYRpYnIaIZMByox/YOn0YkCgr04F7DNtV1mmgmAV/ggzmsGRvkJKfedWlO50NNti+PZ1zzo0jjYegMYWhMfjrQN/uzhmQXZ/sleK/unAMUs3eKZUKY1jLL+rnMqn0eZjs078M7jnhOOJSd/1b07evXffSNin9AmTLcyo="
    )
    pprint(bp.bp["blueprint"]["entities"])
