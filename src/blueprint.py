import base64, json, zlib
from recipe import fluids
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

    def find(self, name, dist, pos):
        found = []
        for e in self.bp["blueprint"]["entities"]:
            if e["name"] == name:
                epos = [e["position"]["x"], e["position"]["y"]]
                xdiff = pos[0] - epos[0]
                ydiff = pos[1] - epos[1]
                d = (xdiff ** 2 + ydiff ** 2) ** 0.5
                if d <= dist:
                    found.append(e["entity_number"])
        return found

    def addEntity(
        self,
        name,
        x,
        y,
        recipe="",
        direction="",
        type="",
        ccitem="",
        mod="",
        mnum=0,
    ):
        o = 0.0 if name in ["substation"] else 0.5
        self.bp["blueprint"]["entities"].append(
            {
                "entity_number": self.entityNumber,
                "name": name,
                "position": {"x": x + o, "y": y + o},
            }
        )
        if recipe != "":
            self.bp["blueprint"]["entities"][-1]["recipe"] = recipe
        if mod != "":
            self.bp["blueprint"]["entities"][-1]["items"] = {mod: mnum}
        if direction != "":
            self.bp["blueprint"]["entities"][-1]["direction"] = direction
        if type != "":
            self.bp["blueprint"]["entities"][-1]["type"] = type
        if ccitem != "":  # create constant combinator with one item in it
            self.bp["blueprint"]["entities"][-1]["control_behavior"] = {
                "filters": [
                    {
                        "count": 1,
                        "index": 1,
                        "signal": {
                            "name": ccitem,
                            "type": "fluid" if ccitem in fluids else "item",
                        },
                    }
                ]
            }
        if name in ["substation"]:
            self.bp["blueprint"]["entities"][-1]["neighbours"] = self.find(
                "substation", 18, [x, y]
            )
        self.entityNumber += 1
        return self.entityNumber - 1


if __name__ == "__main__":
    bp = BP()
    bp.importFromString(
        "0eNqV0MEOgjAMBuB3+c8zgUEA9yqGGKYNNoFC2DASsnd34MWoF29ts35tt8J2M40Ti4dZwZdBHMxpheNWmm6r+WUkGLCnHgrS9FvmZut843kQBAWWKz1g0lArkHj2TC9lT5azzL2lKT741a8wDo73ME6LzKFIFBYYXSTRFuL2Zod52kRdB/Wl6v/UsvpU03pbfD/QvP2Hwp0mtwu6SvPyqMusyPMk0yE8AaRZZwc="
    )
    pprint(bp.bp["blueprint"]["entities"])
