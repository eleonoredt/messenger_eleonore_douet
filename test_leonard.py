from messenger import User
from messenger import Channels
from messenger import Messages
from messenger import RemoteStorage
from messenger import LocalStorage
import pytest
import pytest_cov
import json

class Test:

    def test_get_users(self):
        data_test = {
            "users": [
                {"name": "Marc", "id": 1},
                {"name": "Bob", "id": 2}
            ],
            "channels": [],
            "messages": []}
        fichier_fictif = "testjson.json"
        with open(fichier_fictif, "w", encoding="utf-8") as f:
            f.write(json.dumps(data_test))
        storage = LocalStorage(str(fichier_fictif))
        resultat = storage.get_users()
        assert len(resultat) == 2
        assert resultat[0].name == "Marc"
        assert resultat[0].id == 1
        assert resultat[1].name == "Bob"
        assert resultat[1].id == 2

    def test_get_channels(self):
        data_test = {
            "users": [],
            "channels": [{
            "name": "channel1",
            "id": 1,
            "member_ids": [1,2,3]},
            {"name": "channel2",
            "id": 2,
            "member_ids": [4,5,6]}],
            "messages": []}
        fichier_fictif = "testjson.json"
        with open(fichier_fictif, "w", encoding="utf-8") as f:
            f.write(json.dumps(data_test))
        storage = LocalStorage('testjson.json')
        resultat = storage.get_group()
        assert len(resultat) == 2
        assert resultat[0].name == 'channel1'
        assert resultat[0].id == 1
        assert resultat[0].member_ids == [1,2,3]