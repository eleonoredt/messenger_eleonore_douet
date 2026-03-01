from art import text2art
import json
import textwrap
import requests
import argparse
import os
from model import Channel
from local_storage import LocalStorage
from remote_storage import RemoteStorage

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
