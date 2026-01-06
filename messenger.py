from datetime import datetime
import json
import requests

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

class Messages: 
    def __init__(self, id: int, reception_date: str,sender_id: int,channel: int,content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content


class RemoteStorage:
    def get_users(self):
        response = requests.get('https://groupe5-python-mines.fr/users')
        response_text = response.text
        response_dict=json.loads(response_text)
        rep_list:list[User]=[]
        for user in response_dict:
            rep_list.append(User(user['name'], user['id']))
        return rep_list
    def create_user(self, nomnew): 
        nom_dict = {'name': nomnew}
        envoie = requests.post('https://groupe5-python-mines.fr/users/create', json = nom_dict)
        print(envoie.status_code, envoie.text)

storage = RemoteStorage()
web_users = storage.get_users()     



with open('servers.json') as f:
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

    server['users']=user_list #je transforme le dic dcp par ma liste User 
    server['channels']=channel_list
    server['messages']=message_list


def sauvegarderjson():  
    server2 = {} #je cree un dico vide pour pas modifier server
    dico_user_list:list[dict] = [] #je cree une liste vide d'elements de type dict, je parcours server 
    for user in server['users']: 
        dico_user_list.append({'name': user.name, 'id': user.id})
    server2['users'] = dico_user_list #la dcp j'ajouter a server2 
    dico_channel_list:list[dict] = []
    for channel in server['channels']: 
        dico_channel_list.append({'name': channel.name, 'id': channel.id, 'member_ids': channel.member_ids})
    server2['channels'] = dico_channel_list
    dico_mess_list:list[dict] = []
    for mess in server['messages']:
        dico_mess_list.append({ "id": mess.id, "reception_date": mess.reception_date, "sender_id": mess.sender_id, "channel": mess.channel, "content": mess.content})
    server2['messages'] = dico_mess_list
    with open('servers.json', 'w') as fichier: #j'ecris (mode write w) comme d'hab en haut dcp du fichier 
        json.dump(server2, fichier, indent=4)



ident = []
idgp = []
idpers = []
idhh = []
mid = []


def get_id_from_name(nom):
    idnom = None 
    for user in server['users']:
        if nom == user.name:
            idnom = user.id
            break 
    return idnom

def get_name_from_id(user_id):
    nom = None 
    for user in server['users']:
        if user.id == user_id:
            nom = user.name
            break  
    return nom


def menu():
    print('=== Messenger ===')
    print('x : Leave')
    print('u : Afficher les utilisateurs')
    print('gp :  Afficher les groupes')
    print('b : Back to the menu')
    print('ng : Nouveau groupe')
    print('n : nouvel utilisateur')
    print('m : nouveau message dans un groupe')
    print('d : supprimer un groupe')
    print('dm : supprimer un message')
    choice = input('Select an option: ')  
    if choice == 'x':
        print('Bye!')
    elif choice == 'u':
        users()
        choice3 = input('b : go back to menu, n: create new user ')
        if choice3 == 'b': 
            menu()
        elif choice3 == 'n': 
            newuser()
    elif choice == 'gp':
        groupe()
        choice2 = int(input('Select a group by its id: '))
        for channel in (server['channels']) :
            if choice2 == channel.id:
                affichegroupe() 
            break 
        else: 
            print('No group')
        choicegp = input('Voulez vous creer un nouveau groupe? si oui tapez ng sinon tapez b pour revenir ')
        if choicegp == 'ng':
            newgp()
        else :
            menu()
    elif choice == 'm':
        newmessage()
        
    elif choice == 'b':
        menu()
    elif choice == 'ng':
        newgp()
    elif choice == 'n':
        newuser()
    elif choice == 'd':
        suppgp()
    elif choice == 'dm':
        supp_message()
    else:
        print('Unknown option:', choice)

def users():
    print('Les utilisitateurs sont: ')
    for user in (web_users) : 
        nomid = str(user.id) + '. ' + user.name #nomid=f"{user['id']}. {user['name']}
        print(nomid)

def newuser():
    nomnew = input('Donner le nom du nouvel utilisateur ')
    storage.create_user(nomnew)

def groupe():
    for channel in (server['channels']) :
        groupe = str(channel.id) + '. ' + channel.name
        print(groupe)

def affichegroupe():
    for mess in server['messages']:
        message = 'The sender id is ' + str(mess.sender_id)+ '. They said: ' + mess.content
        print(message)

def newgp():
    for user in (web_users) : 
        idhh.append(user.id) #affiche tous les id des users
    newnomgp = input('Donnez le nom du groupe  ')
    for channel in (server['channels']) : 
        idgp.append(channel.id) #liste des id de groupes 
    idgpnew = max(idgp) + 1
    print('Voici la liste des utilisateurs: ')
    users()
    nbpers = int(input('Combien d utilisateurs souhaitez vous ajouter? '))
    if nbpers>len(web_users): 
        print('Il n y a pas assez d utilisateurs, refaite un groupe qui fonctionne')
        newgp()
    else: 
        for i in range (nbpers): #je fais apparaitre a chaque fois pour donner l'id
            idpersi = int(input('Donner l id d\'une personnes: '))
            if idpersi not in (idhh):
                print('Cet id n existe pas, redonnez un groupe qui marche ')
                newgp()
            else:
                idpers.append(idpersi)
    gpnew = Channels(newnomgp, idgpnew, idpers ) #je cree nouveau groupe
    server['channels'].append(gpnew) #je l'ajoute a json
    sauvegarderjson()

def suppgp(): 
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
        print(" Erreur : Aucun message trouvé avec l ID.")


def newmessage():
    #check il est dans groupe et new mesage 
    sendername = input('Quel est votre nom ')
    list_user = []
    for user in web_users:
        list_user.append(user.name)
    if sendername not in list_user : 
        print('Votre nom n \'existe pas ')
        choix = input('Voulez vous créer un nouvel utilisateur ? Si oui tapez n si vous souhaitez changer de nom tapez j ')
        if choix == 'n': 
            newuser()
            newmessage()
        else : 
            newmessage()
    else : 
        senderid = int(get_id_from_name(sendername))
        list_member_ids = []
        for channel in server['channels']:
            list_member_ids += channel.member_ids
        if senderid not in list_member_ids : 
            choix2 = input('Vous n\'etes dans aucun groupe, si vous souhaitez créer un groupe tapez ng sinon partez et x ')
            if choix2 == 'ng': 
                newgp()
                newmessage()
            else : 
                print('Bye')
        else: 
            print('voici les groupes ou vous etes:')
            for channel in (server['channels']): 
                if senderid in channel.member_ids: 
                    print(channel.id)
                    for id_membre in channel.member_ids:
                        id_membres = get_name_from_id(id_membre)
                        print(id_membres)
            #cavousva = input('Un des groupe vous convient ? si oui on continue sinon tapez nn')
        # if cavousva == 'nn' : 
            #    newgp()
            gp = int(input('Donner l \'indentifiant du groupe '))
            texto = input('Ecrivez votre messsage : ')
            for channel in (server['channels']) : 
                mid.append(channel.id)
            newmid =  max(mid) + 1
            newmess = Messages( newmid, "04/11/25", senderid,  gp, texto)
            server['messages'].append(newmess)
            sauvegarderjson()
    

menu()
