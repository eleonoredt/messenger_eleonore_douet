import json
from datetime import datetime
import requests
from model import User, Channel, Message

class RemoteStorage:
    def __init__(self, chemin: str):
            self.chemin = chemin
    
    # GET /users
    def get_users(self):
        response = requests.get(f"{self.chemin}/users")
        response_text = response.text
        response_dict=json.loads(response_text)
        rep_list:list[User]=[]
        for user in response_dict:
            rep_list.append(User(user['name'], user['id']))
        return rep_list
    
    # GET /users/{user_id}
    def get_user_from_id(self, user_id):
        response = requests.get(f"{self.chemin}/users/{user_id}")
        response_text = response.text
        response_dict=json.loads(response_text)
        return User(response_dict['name'], response_dict['id'])

    # POST /users/create
    def create_user(self, nomnew): 
        nom_dict = {'name': nomnew}
        envoie = requests.post(f"{self.chemin}/users/create", json = nom_dict)
        print(envoie.status_code, envoie.text)

    # GET /channels
    def get_groups(self):
        responsegp = requests.get(f"{self.chemin}/channels")
        responsegp_dict=json.loads(responsegp.text)
        repgp_list:list[Channel]=[]
        for channel in responsegp_dict:
            # pour éviter trop de requêtes (looong), je remplis les membres dans get_channel_from_id
            repgp_list.append(Channel(channel['name'], channel['id'], []))
        return repgp_list

        #     print(f"{self.chemin}/channels/{channel['id']}/members")
        #     members_resp = requests.get(f"{self.chemin}/channels/{channel['id']}/members")
        #     members_list:list[User]=[]
        #     if members_resp.status_code == 200:
        #         members_dict = json.loads(members_resp.text)
        #         for user in members_dict:
        #             members_list.append(User(user['name'], user['id']))
        #     repgp_list.append(Channel(channel['name'], channel['id'], members_list))
        # return repgp_list
    
    # GET /channels/{channel_id}
    def get_channel_from_id(self, channel_id):
        responsegp = requests.get(f"{self.chemin}/channels/{channel_id}")
        responsegp_dict=json.loads(responsegp.text)
        members = self.get_members_from_channel_id(channel_id)
        return Channel(responsegp_dict['name'], responsegp_dict['id'], members)
    
    # GET /userschannels/{channel_id}/members
    def get_members_from_channel_id(self, channel_id):
        members_resp = requests.get(f"{self.chemin}/channels/{channel_id}/members")
        members_list= members_resp.json()
        membersid = [m['id'] for m in members_list]
        members = [] #je remplis la liste de membres du groupe
        for u in self.get_users():
            if u.id in membersid:
                members.append(u)
        return members
    
    # POST /channels/create
    def create_group(self, nomnewgp: str)->Channel: 
        nom_gp_dict = {'name': nomnewgp}
        envoie = requests.post(f"{self.chemin}/channels/create", json = nom_gp_dict)
        if envoie.status_code == 200:
            print("Groupe créé avec succès.")
            idgp = json.loads(envoie.text)['id']
            group = Channel(nomnewgp, json.loads(envoie.text)['id'], [])
            return group
        else:
            print("Erreur lors de la création du groupe.")
        return None
    
    # POST /channels/{channel_id}/join
    def join_group(self, idgp, user_id):
        members_id_dict = {'user_id': user_id}
        envoie = requests.post(f"{self.chemin}/channels/{idgp}/join", json = members_id_dict)
        if envoie.status_code == 200:
            print("Utilisateur ajouté au groupe avec succès.")
        else:
            print("Erreur lors de l'ajout de l'utilisateur au groupe.", envoie.status_code, envoie.text)

    # GET /channels/{channel_id}/messages
    def get_messages_from_channel_id(self, channel_id):
        response_mess = requests.get(f"{self.chemin}/channels/{channel_id}/messages")
        response_mess_text = response_mess.text
        response_dict=json.loads(response_mess_text)
        rep_mess_list:list[Message]=[]
        for message in response_dict:
            date = datetime.fromisoformat(message['reception_date']) #je convertis en datetime
            rep_mess_list.append(Message(message['id'], date, message['sender_id'],message['channel_id'],message['content']))
        return rep_mess_list    

    # POST /channels/{channel_id}/messages/post
    def create_message(self, idgp, id_sender, content: str):
        message_dict = {'sender_id': id_sender, 'content': content}
        envoie = requests.post(f"{self.chemin}/channels/{idgp}/messages/post", json = (message_dict))
        if envoie.status_code == 200:
            print("Message créé avec succès.")
        else:
            print("Erreur lors de la création du message.", envoie.status_code, envoie.text)
