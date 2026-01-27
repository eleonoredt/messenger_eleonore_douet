from datetime import datetime
import json
import requests
import argparse



class User:
    def __init__(self, name: str, id: int):
            self.name = name
            self.id = id
    def __repr__(self) -> str:
        return f'User(name={self.name})'

class Channels:
    def __init__(self, name: str, id: int, member_ids: list):
            self.name = name
            self.id = id
            self.member_ids = member_ids
    def __repr__(self) -> str:
        return f'Channel(name={self.name})'

class Messages: 
    def __init__(self, id: int, reception_date: str,sender_id: int,channel: int,content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content


class RemoteStorage:
    def __init__(self, chemin: str):
            self.chemin = chemin
    def get_users(self):
        response = requests.get(f"{self.chemin}/users")
        response_text = response.text
        response_dict=json.loads(response_text)
        rep_list:list[User]=[]
        for user in response_dict:
            rep_list.append(User(user['name'], user['id']))
        return rep_list
    def create_user(self, nomnew): 
        nom_dict = {'name': nomnew}
        envoie = requests.post(f"{self.chemin}/users/create", json = nom_dict)
        print(envoie.status_code, envoie.text)
    def get_group(self):
        responsegp = requests.get(f"{self.chemin}/channels")
        responsegp_dict=json.loads(responsegp.text)
        repgp_list:list[Channels]=[]
        for channel in responsegp_dict:
            members = requests.get(f"{self.chemin}/userschannels/{channel['id']}/members")
            #membersid_dict = json.loads(membersid) #pb ICI
            members_list= members.json()
            membersid = [m['id'] for m in members_list]
            repgp_list.append(Channels(channel['name'], channel['id'], membersid))
        return repgp_list
    def create_group(self, nomnewgp: str)->int: 
        nom_gp_dict = {'name': nomnewgp}
        envoie = requests.post(f"{self.chemin}/channels/create", json = nom_gp_dict)
        return envoie.json()['id']
    def join_group(self, idgp, members_id):
        members_id_dict = {'user_id': members_id}
        envoie = requests.post(f"{self.chemin}/channels/{idgp}/join", json = members_id_dict)
        print(envoie.status_code, envoie.text)
    def get_messages(self):
        response_mess = requests.get(f"{self.chemin}/messages")
        response_mess_text = response_mess.text
        response_dict=json.loads(response_mess_text)
        print(response_dict)
        rep_mess_list:list[Messages]=[]
        for message in response_dict:
            rep_mess_list.append(Messages(message['id'], message['reception_date'], message['sender_id'],message['channel_id'],message['content']))
        return rep_mess_list
    def create_message(self, idgp, id_sender, content: str):
        message_dict = {'sender_id': id_sender, 'content': content}
        envoie = requests.post(f"{self.chemin}/channels/{idgp}/messages/post", json = (message_dict))
        print(envoie.status_code, envoie.text)


class LocalStorage:
    def __init__(self, chemin):
            self.chemin = chemin
            self._users: list[User]
            self._channels: list[Channels]
            self._messages: list[Messages]

    def load_server(self):
        with open(self.chemin) as f:
            server = json.load(f)
            user_list:list[User] = [] #je cree une liste vide d'elements de type User 
            for user in server['users']: 
                user_list.append(User(user['name'], user['id'])) #j'ajoute les elements 
            channel_list:list[Channels] = [] #je cree une liste vide d'elements de type Channels 
            for channel in server['channels']:
                channel_list.append(Channels(channel['name'], channel['id'], channel['member_ids']))
            message_list:list[Messages] = [] #je cree une liste vide d'elements de type Messages  
            for mess in server['messages']:
                message_list.append(Messages(mess['id'], mess['reception_date'], mess['sender_id'], mess['channel'], mess['content']))
        self._users=user_list #je transforme le dic dcp par ma liste User 
        self._channels=channel_list
        self._messages=message_list
        return server
    
    def save_server(self, server):  
        server2 = {} #je cree un dico vide pour pas modifier server
        dico_user_list:list[dict] = [] #je cree une liste vide d'elements de type dict, je parcours server 
        for user in self._users: 
            dico_user_list.append({'name': user.name, 'id': user.id})
        server2['users'] = dico_user_list #la dcp j'ajouter a server2 
        dico_channel_list:list[dict] = []
        for channel in self._channels: 
            dico_channel_list.append({'name': channel.name, 'id': channel.id, 'member_ids': channel.member_ids})
        server2['channels'] = dico_channel_list
        dico_mess_list:list[dict] = []
        for mess in self._messages:
            dico_mess_list.append({ "id": mess.id, "reception_date": mess.reception_date, "sender_id": mess.sender_id, "channel": mess.channel, "content": mess.content})
        server2['messages'] = dico_mess_list
        with open(self.chemin, 'w') as fichier: #j'ecris (mode write w) comme d'hab en haut dcp du fichier 
            json.dump(server2, fichier, indent=4)

    def get_users(self):
        server = self.load_server()
        users_list:list[User]=[]
        for user in (self._users) : 
            users_list.append(user)
        return users_list
    
    def create_user(self, nomnew):
        server = self.load_server()
        ident = []
        for user in (self._users) : 
            ident.append(user.id)
        newid = max(ident) + 1
        newuser = User(nomnew, newid)
        self._users.append(newuser)
        self.save_server(server)

    def get_group(self):
        server = self.load_server()
        channel_list:list[Channels] = [] #je cree une liste vide d'elements de type Channels 
        for channel in self._channels:
            channel_list.append(Channels(channel.name, channel.id, channel.member_ids))
        return channel_list
    
    def create_group(self, nomnewgp: str)->int:
        idgp = []
        server = self.load_server()
        for chan in (self._channels) : 
            idgp.append(chan.id) #liste des id de groupes 
        idgpnew = max(idgp) + 1
        gpnew = Channels(nomnewgp, idgpnew, [] ) #je cree nouveau groupe
        self._channels.append(gpnew) #je l'ajoute a json
        self.save_server(server)
        return idgpnew
    
    def join_group(self, idgp, members_id): #c elle vrmt qui va download
        server = self.load_server()
        idpers = []
        for ids in members_id:
            idpers.append(ids)
        for channel in self._channels:
            if channel.id == idgp:
                nomgp = channel.name 
        gpnew = Channels(nomgp, idgp, idpers ) #je cree nouveau groupe
        self._channels.append(gpnew) #je l'ajoute a json
        self.save_server(server)





#if response.status_code = 2 : #Inferieur ou egal a 300
#response.raise_for_status()

class UserInterface: 
    def __init__(self, chemin): 
        self.chemin = chemin
    def menu(self):
        print('=== Messenger ===')
        print('x : Partir')
        print('u : Afficher les utilisateurs')
        print('gp :  Afficher les groupes')
        print('b : Revenir au menu')
        print('ng : Nouveau groupe')
        print('n : Nouvel utilisateur')
        print('m: Afficher les messages')
        print('nm : Nouveau message dans un groupe')
        print('aj : Ajouter des utilisateurs à un groupe existant')
        choice = input('Choisissez une option ')  
        if choice == 'x':
            print('Bye!')
        elif choice == 'u':
            self.users()
            choice3 = input('b : retourner au menu, n: creer un nouvel utilisateur ')
            if choice3 == 'b': 
                self.menu()
            elif choice3 == 'n': 
                self.newuser()
        elif choice == 'gp':
            self.groupe()
            choice2 = int(input('Choisissez un groupe par son identifiant '))
            for channel in (storage.get_group()) :
                if choice2 == channel.id:
                    self.affichegroupe() 
                break 
            else: 
                print('Ce groupe n existe pas')
            choicegp = input('Voulez-vous creer un nouveau groupe? Si oui tapez ng, sinon tapez b pour revenir ')
            if choicegp == 'ng':
                self.newgp()
            else :
                self.menu()
        elif choice == 'nm':
            self.newmessage()
        elif choice== 'm':
            self.affichemessages()
        elif choice == 'b':
            self.menu()
        elif choice == 'ng':
            self.newgp()
        elif choice == 'n':
            self.newuser()
        elif choice == 'd':
            self.suppgp()
        elif choice == 'dm':
            self.supp_message()
        elif choice == 'aj':
            self.newpeople()
        else:
            print('Option inconnue : ', choice)

    def users(self):
        print('Les utilisitateurs sont: ')
        for user in (storage.get_users()) : 
            nomid = str(user.id) + '. ' + user.name #nomid=f"{user['id']}. {user['name']}
            print(nomid)

    def newuser(self):
        nomnew = input('Donner le nom du nouvel utilisateur ')
        storage.create_user(nomnew)

    def groupe(self):
        for channel in (storage.get_group()) :
            groupe = str(channel.id) + '. ' + channel.name
            print(groupe)

    """def affichegroupe():
        for mess in server['messages']:
            message = 'The sender id is ' + str(mess.sender_id)+ '. They said: ' + mess.content
            print(message)"""
        
    def affichemessages(self):
        for message in (storage.get_messages()):
            message =  str(message.sender_id) + 'a envoyé un message.' + ' Iel a dit ' + message.content
            print(message)

    def newgp(self):
        idhh = []
        newnomgp = input('Donnez le nom du groupe:  ')
        a = storage.create_group(newnomgp)
        for user in (storage.get_users()) : 
            idhh.append(user.id) #affiche tous les id des users
        print('Voici la liste des utilisateurs: ')
        self.users()
        nbpers = int(input('Combien d utilisateurs souhaitez vous ajouter? '))
        if nbpers>len(storage.get_users()): 
            print('Il n y a pas assez d utilisateurs, refaite un groupe qui fonctionne')
            self.newgp()
        else: 
            for i in range (nbpers): #je fais apparaitre a chaque fois pour donner l'id
                idpersi = int(input('Donner l id d\'une personnes: '))
                if idpersi not in (idhh):
                    print('Cet id n existe pas, redonnez un groupe qui marche ')
                    self.newgp()
                else:
                    storage.join_group(a ,idpersi)

    def newpeople(self): 
        idhh=[]
        print('Voici la liste des groupes: ')
        self.affichegroupe()
        id_group= input('A quel groupe voulez vous ajoutez des utilisateurs? ')
        for user in (storage.get_users()) : 
            idhh.append(user.id) #affiche tous les id des users
        print('Voici la liste des utilisateurs: ')
        self.users()
        nbpers = int(input('Combien d utilisateurs souhaitez vous ajouter? '))
        if nbpers>len(storage.get_users()): 
            print('Il n y a pas assez d utilisateurs, refaite un groupe qui fonctionne')
            self.newgp()
        else: 
            for i in range (nbpers): #je fais apparaitre a chaque fois pour donner l'id
                idpersi = int(input('Donner l id d\'une personnes: '))
                if idpersi not in (idhh):
                    print('Cet id n existe pas, redonnez un groupe qui marche ')
                    self.newgp()
                else:
                    storage.join_group(id_group ,idpersi)

    """def suppgp(self): 
        gpid = int(input('Donner l id du gp que vous voulez sup '))
        initial_length = len(server['channels'])
        server['channels'] = [
            channel for channel in server['channels'] 
            if channel.id != gpid
        ]
        final_length = len(server['channels'])
        if final_length < initial_length:
            sauvegarderjson()
            print("Groupe supprimé et le fichier a été sauvegardé.")
        else:
            print(" Erreur : Aucun groupe trouvé avec l ID.")

    def supp_message(): 
        messid = int(input('Donner l id du message que vous voulez sup '))
        initial_length = len(server['messages'])
        server['messages'] = [
            mess for mess in server['messages'] 
            if mess.id != messid
        ]
        final_length = len(server['messages'])
        if final_length < initial_length:
            sauvegarderjson()
            print("Message supprimé et le fichier a été sauvegardé.")
        else:
            print(" Erreur : Aucun message trouvé avec l ID.")"""


    def newmessage(self):
        #check il est dans groupe et new mesage 
        sendername = input('Quel est votre nom ')
        list_user = []
        for user in storage.get_users():
            list_user.append(user.name)
        if sendername not in list_user : 
            print('Votre nom n \'existe pas ')
            choix = input('Voulez vous créer un nouvel utilisateur ? Si oui tapez n si vous souhaitez changer de nom tapez j ')
            if choix == 'n': 
                self.newuser()
                self.newmessage()
            elif choix== 'j' : 
                self.newmessage()
            else: 
                self.menu()
        else : 
            senderid = int(self.get_id_from_name(sendername))
            list_member_ids = []
            for channel in storage.get_group():
                list_member_ids += channel.member_ids
            if senderid not in list_member_ids : 
                print(senderid)
                choix2 = input('Vous n\'etes dans aucun groupe, si vous souhaitez créer un groupe tapez ng sinon partez et x ')
                if choix2 == 'ng': 
                    self.newgp()
                    self.newmessage()
                else : 
                    print('Bye')
            else: 
                print('voici les groupes ou vous etes: ')
                for channel in (storage.get_group()): 
                    if senderid in channel.member_ids: 
                        print(channel.id)
                        for id_membre in channel.member_ids:
                            id_membres = self.get_name_from_id(id_membre)
                            print(id_membres)
                #cavousva = input('Un des groupe vous convient ? si oui on continue sinon tapez nn')
            # if cavousva == 'nn' : 
                #    newgp()
                idgp = int(input('Donner l \'indentifiant du groupe '))
                texto = input('Ecrivez votre messsage : ')
                storage.create_message(idgp, senderid, texto)

    def get_id_from_name(self,nom):
        idnom = None 
        for user in storage.get_users():
            if nom == user.name:
                idnom = user.id
                break 
        return idnom

    def get_name_from_id(user_id):
        nom = None 
        for user in storage.get_users():
            if user.id == user_id:
                nom = user.name
                break  
        return nom


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='le programme permet de créer des utilisitateurs et des groupes pour ensuite pouvoir envoyer des messages' \
                        'Vous pouvez soit choisir de télécharger des données depuis votre ordinateur (en local) en faisant --storage-file ou depuis internet en faisant --url'
                        )

    parser.add_argument('--storagefile', type=str, help="Chemin vers le fichier JSON de stockage (ex: server-data.json)")
    parser.add_argument('--url', type=str, help="Chemin vers une url à rentrer")
    args = parser.parse_args()
    if args.storagefile:
        storage = LocalStorage(args.storagefile)
        print(type(storage))
    elif args.url:
        storage = RemoteStorage(args.url)
        print(type(storage))
    else : 
        parser.print_help()
        exit()
                    
    UserInterface(storage).menu()
