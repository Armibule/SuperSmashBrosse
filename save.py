from threading import Thread
from time import sleep
import json


class Save:
    def __init__(self, gvars):
        self.gvars = gvars
        # self.load()     # []

    # fonctionnement: {token:[pseudo]}
    # format json
    def load(self):
        return
        defaultValues = []

        try:
            f = open("assets/save", "r")
            js = f.read()
            f.close()
            values = json.loads(js)

        except FileNotFoundError:
            f = open("assets/save", "w")
            f.write(json.dumps(defaultValues, separators=(',', ':')))
            values = defaultValues

        self.gvars.SOMETHING = values

    def save(self):
        return
        print("saving")
        f = open("assets/save", "r")
        gardeFou = f.read()
        f.close()
        values = [self.gvars.firstTime, self.gvars.isAuthenticated, self.gvars.editingServerId]
        try:
            f = open("assets/save", "w")
            f.write(json.dumps(values, separators=(',', ':')))  # encodage compact
            f.close()
        except:
            open("assets/save", "w").write(gardeFou)

            print(r"/!\ crash des données intercepté !")
            print(rf"/!\ save qui a crash {values}")
            print(rf"/!\ code de récupération {gardeFou}")
