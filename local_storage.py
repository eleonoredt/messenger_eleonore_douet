import json
from datetime import datetime
from model import User, Channel, Message



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
