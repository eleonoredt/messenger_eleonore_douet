from art import text2art
import json
import textwrap
import requests
import argparse
import os
from datetime import datetime




class User:
    def __init__(self, name: str, id: int):
            self.name = name
            self.id = id
    def __repr__(self) -> str:
        return f'User(name={self.name})'
    
    def affiche_user(self):
        print(f"{self.id}. {self.name}")


class Channel:
    def __init__(self, name: str, id: int, members: list[User]):
            self.name = name
            self.id = id
            self.members = members
    def __repr__(self) -> str:
        return f'Channel(name={self.name})'
    
    def affiche_groupe(self, storage):
        print('Nom du groupe : \t' + self.name)
        print('Membres du groupe : \t', end="")
        if len(self.members) > 0:
            member_names = []
            for membre in self.members:
                if membre:
                    member_names.append(membre.name)
            print(", ".join(member_names))
            print("Discussion".center(100, '-'))
            for mess in storage.get_messages_from_channel_id(self.id):
                if mess.channel == self.id:
                    mess.affiche_message(storage)
            print("-"*100)
        else:
            print("Aucun membre")


class Message: 
    def __init__(self, id: int, reception_date: datetime, sender_id: int, channel: int, content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
    
    def affiche_message(self, storage):
        sender_name = storage.get_user_from_id(self.sender_id).name
        message = f'[{self.reception_date.strftime("%Y-%m-%d %H:%M")}] [{sender_name}] \t: {self.content}'
        print(message)


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


class LocalStorage:
    def __init__(self, chemin):
            self.chemin = chemin
            self._users: list[User]
            self._channels: list[Channel]
            self._messages: list[Message]

    def load_server(self):
        with open(self.chemin) as f:
            server = json.load(f)
            user_list:list[User] = [] #je cree une liste vide d'elements de type User 
            for user in server['users']: 
                user_list.append(User(user['name'], user['id'])) #j'ajoute les elements 
            channel_list:list[Channel] = [] #je cree une liste vide d'elements de type Channel 
            for channel in server['channels']:
                members_list = []
                for member_id in channel['member_ids']: #je remplis la liste de membres du groupe
                    for user in user_list:
                        if user.id == member_id:
                            members_list.append(user)
                new = Channel(channel['name'], channel['id'], members_list)
                channel_list.append(new)
            message_list:list[Message] = [] #je cree une liste vide d'elements de type Message  
            for mess in server['messages']:
                try:
                    date = datetime.fromisoformat(mess['reception_date']) #je convertis en datetime
                except ValueError:
                    date = datetime(2025,11,4)
                message_list.append(Message(mess['id'], date, mess['sender_id'], mess['channel'], mess['content']))
        self._users=user_list #je transforme le dic dcp par ma liste User 
        self._channels=channel_list
        self._messages=message_list
        return server
    
    def save_server(self):  
        server = {} #je cree un dico vide pour pas modifier server 
        dico_user_list:list[dict] = [] #je cree une liste vide d'elements de type dict, je parcours server 
        for user in self._users: 
            dico_user_list.append({'name': user.name, 'id': user.id})
        server['users'] = dico_user_list #la dcp j'ajouter a server 
        dico_channel_list:list[dict] = []
        for channel in self._channels: 
            member_ids = [member.id for member in channel.members] # je save seulement les id des membres
            dico_channel_list.append({'name': channel.name, 'id': channel.id, 'member_ids': member_ids})
        server['channels'] = dico_channel_list
        dico_mess_list:list[dict] = []
        for mess in self._messages:
            dico_mess_list.append({ "id": mess.id, "reception_date": str(mess.reception_date), "sender_id": mess.sender_id, "channel": mess.channel, "content": mess.content})
        server['messages'] = dico_mess_list
        with open(self.chemin, 'w') as fichier: #j'ecris (mode write w) comme d'hab en haut dcp du fichier 
            json.dump(server, fichier, indent=4)

    def get_users(self):
        self.load_server()
        users_list:list[User]=[]
        for user in (self._users) : 
            users_list.append(user)
        return users_list
    
    def get_user_from_id(self, user_id):
        user = None
        users_list = self.get_users() 
        for one in users_list:
            if one.id == user_id:
                user = one
                break
        return user

    def create_user(self, nomnew):
        self.load_server()
        newid = max([user.id for user in self._users]) + 1
        newuser = User(nomnew, newid)
        self._users.append(newuser)
        self.save_server()

    def get_groups(self):
        self.load_server()
        channel_list:list[Channel] = [] #je cree une liste vide d'elements de type Channels
        for channel in self._channels:
            members_list = []
            for member in channel.members: #je remplis la liste de membres du groupe
                member = self.get_user_from_id(member.id)
                members_list.append(member)
            channel_list.append(Channel(channel.name, channel.id, members_list))
        return channel_list
    
    def get_channel_from_id(self, channel_id):
        channel = None 
        for chan in self.get_groups():
            if chan.id == channel_id:
                channel = chan
                break  
        return channel

    def create_group(self, nomnewgp: str)->Channel:
        idgp = []
        self.load_server()
        for chan in (self._channels) : 
            idgp.append(chan.id) #liste des id de groupes 
        idgpnew = max(idgp) + 1
        members: list[User] = []
        gpnew = Channel(nomnewgp, idgpnew, members) #je cree nouveau groupe sans membres
        self._channels.append(gpnew) #je l'ajoute a json
        self.save_server()
        return gpnew
    
    def join_group(self, channel_id, member_id): #c elle vrmt qui va download
        self.load_server()
        channel = self.get_channel_from_id(channel_id)
        member = self.get_user_from_id(member_id)
        if channel and member:
            channel.members.append(member)
        # remplacer le channel dans la liste des channels par le channel modifié
        self._channels = [channel if c.id == channel.id else c for c in self._channels]
        self.save_server()
    
    def get_messages_from_channel_id(self, channel_id):
        mess_list:list[Message] = []
        for mess in self.get_messages():
            if mess.channel == channel_id:
                mess_list.append(mess)
        return mess_list

    def create_message(self, idgp, id_sender, content: str):
        self.load_server()
        idmess = max([mess.id for mess in self._messages]) + 1
        message = Message(idmess, datetime.now(), id_sender, idgp, content)
        self._messages.append(message)
        self.save_server()
  
    def get_messages(self):
        self.load_server()
        mess_list:list[Message]=[]
        for mess in self._messages:
            mess_list.append(mess)
        return mess_list




#if response.status_code = 2 : #Inferieur ou egal a 300
#response.raise_for_status()

class UserInterface: 
    def __init__(self, storage: LocalStorage | RemoteStorage): 
        self._storage = storage
    def menu(self):
        MENU_TITLE = text2art("Messenger Eleonore", font='slant')
        choice = ''
        while choice != 'x' and choice != 'X':
            os.system('cls' if os.name == 'nt' else 'clear') #nettoie le terminal pour lisibilité        
            print(MENU_TITLE)
            print(' MENU '.center(100, '='))
            print('u \t: Afficher les utilisateurs')
            print('gp \t: Afficher les groupes')
            print('x \t: Quitter')
            print("="*100)
            choice = input('Choisissez une option --> ')
            match choice:
                # QUITTER
                case 'x' | 'X':
                    print("="*100)
                    print('Bye!')
                    print("="*100)
                # AFFICHER LES UTILISATEURS
                case 'u' | 'U':
                    choice_user = 'n'
                    while len(choice_user) > 0:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("="*100)
                        self.users()
                        print("="*100)
                        print('n: Créer un nouvel utilisateur \t [autre]: Menu Principal')
                        print("="*100)
                        choice_user = input('--> ')
                        if choice_user == 'n':
                            self.newuser()
                # AFFICHER LES GROUPES
                case 'gp' | 'GP':
                    choicegp = ' '
                    while len(choicegp) > 0:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("="*100)
                        self.affiche_groupes()
                        print("="*100)
                        print('[entrer id]: Afficher un groupe \t ng: Créer un nouveau groupe \t [autre]: Menu Principal')
                        print("="*100)
                        choicegp = input('--> ')
                        if (choicegp.isdigit()):
                            # AFFICHE UN GROUPE
                            if int(choicegp) in [channel.id for channel in self._storage.get_groups()]:
                                channel = self._storage.get_channel_from_id(int(choicegp))
                                while len(choicegp) > 0: 
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    print("="*100)
                                    channel.affiche_groupe(self._storage)
                                    print("="*100)
                                    print('nm: Nouveau message dans ce groupe \taj: Ajouter un membre \t[autre]: Menu Principal')
                                    print("="*100)
                                    choicegp = input('--> ')
                                    if choicegp == 'nm':
                                        self.newmessage(channel)
                                        channel = self._storage.get_channel_from_id(channel.id) #je redownload le channel pour que les messages soient à jour
                                    if choicegp == 'aj':
                                        self.newpeople(channel)
                                        channel = self._storage.get_channel_from_id(channel.id)
                            else:
                                print('Ce groupe n\'existe pas, essayez à nouveau.')
                        if choicegp == 'ng':
                            self.newgp()
                case _:
                    print('Option inconnue.', choice)

    def users(self):
        print('Les utilisitateurs sont: ')
        users_list = self._storage.get_users()
        for user in (users_list) : 
            nomid = str(user.id) + '. ' + user.name #nomid=f"{user['id']}. {user['name']}
            print(nomid)

    def newuser(self):
        nomnew = input('Donner le nom du nouvel utilisateur: ')
        self._storage.create_user(nomnew)

    def affiche_groupes(self):
        groups = self._storage.get_groups()
        for channel in groups :
            groupe = str(channel.id) + '. ' + channel.name
            print(groupe)        

    def newgp(self):
        newnomgp = input('Donnez le nom du groupe:  ')
        a = self._storage.create_group(newnomgp)
        self.newpeople(a)
        
    def newpeople(self, group): 
        self.users()
        choice_id = 'n'
        while len(choice_id) > 0:
            print('[id] Entrer un id d\'utilisateur à ajouter au groupe. [Enter] Terminer.')
            choice_id = input('--> ')
            if choice_id.isdigit():
                user_id = int(choice_id)
                if user_id not in [user.id for user in self._storage.get_users()] or user_id in [user.id for user in group.members]:
                    print('Cet id n\'existe pas ou est déjà dans le groupe, réessayez.')
                else:
                    new_member = self._storage.get_user_from_id(user_id)
                    self._storage.join_group(group.id, new_member.id)

    def affiche_membres(self, channel):
        print('Membres du groupe :')
        if len(channel.members) > 0:
            for membre in channel.members:
                if membre:
                    membre.affiche_user()
        else:
            print("Aucun membre")

    def newmessage(self, channel: Channel):
        print("="*100)
        self.affiche_membres(channel)
        print("="*100)
        choice_id = 'n'
        while len(choice_id) > 0:
            print('[id] Entrer l\'id de l\'émetteur. [Enter] Terminer.')
            choice_id = input('--> ')
            if choice_id.isdigit():
                sender_id = int(choice_id)
                if sender_id not in [user.id for user in self._storage.get_users()]:
                    print('Cet id n\'existe pas, réessayez.')
                elif sender_id not in [member.id for member in channel.members]:
                    print('Cet utilisateur n\'est pas dans le groupe, réessayez.')
                else:
                    content = input('Ecrivez votre message: ')
                    self._storage.create_message(channel.id, sender_id, content)
                    return
    
    
parser = argparse.ArgumentParser(
    prog='messenger.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
    Ce programme permet de créer des utilisitateurs et des groupes pour ensuite pouvoir envoyer des messages.
    
    Vous pouvez soit choisir de télécharger des données depuis :
    
        --> votre ordinateur (en local) en utilisant --storage-file
        --> serveur internet (en remote) en utilisant --url
    '''))
parser.add_argument('--storage-file', type=str, help="Chemin vers le fichier JSON de stockage (ex: server-data.json)")
parser.add_argument('--url', type=str, help="Chemin vers une url à rentrer")
args = parser.parse_args()

if args.storage_file:
    storage = LocalStorage(args.storage_file)
    print(type(storage))
elif args.url:
    if args.url[-1] == '/':
        args.url = args.url[:-1]
    storage = RemoteStorage(args.url)
    print(type(storage))
else : 
    parser.print_help()
    exit()
                
UserInterface(storage).menu()
