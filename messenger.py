from datetime import datetime
import json

class User:
    def __init__(self, name: str, id: int):
            self.name = name
            self.id = id

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

with open('servers.json') as f:
    server = json.load(f)
    user_list:list[User]=[]
    for user in server['users']: 
         user_list.append(user)
    server['users']=user_list
print(type(server['users']))

def sauvegarderjson():  
    with open('servers.json', 'w') as fichier:
        json.dump(server, fichier, indent=4)

#class User:
    #def __init__(self, nom, id):
       # for user in (server['users']) :
        #    nom = user['name']
         #   id = user['id']
        


ident=[]
idgp=[]
idpers=[]
idhh=[]
mid = []


def get_id_from_name(nom):
    idnom = None 
    for user in server['users']:
        if nom == user.name:
            idnom = user.id
            break 
    return idnom
print(get_id_from_name('Bob'))
def get_name_from_id(user_id):
    nom = None 
    for user in server['users']:
        if user['id'] == user_id:
            nom = user['name']
            break  
    return nom


def menu():
    print('=== Messenger ===')
    print('x. Leave')
    print('u. Afficher les utilisateurs')
    print('gp. Afficher les groupes')
    print('b. Back to the menu')
    print('ng: Nouveau groupe')
    print('n : nouvel utilisateur')
    print('m : nouveau message dans un groupe')
    print('d : supprimer un groupe')
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
        for serv in (server['channels']) :
            if choice2 == serv['id']:
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
    else:
        print('Unknown option:', choice)

def users():
    print('Les utilisitateurs sont: ')
    for user in (server['users']) : 
        nomid = str(user['id']) + '. ' + user['name'] #nomid=f"{user['id']}. {user['name']}
        print(nomid)

def newuser():
    nomnew = input('Donner le nom du nouvel utilisateur ')
    for user in (server['users']) : 
        ident.append(user['id'])
    newid = max(ident) + 1
    newuser = {'id':newid , 'name': nomnew}
    server['users'].append(newuser)
    sauvegarderjson()

def groupe():
    for serv in (server['channels']) :
        groupe = str(serv['id']) + '. ' + serv['name']
        print(groupe)

def affichegroupe():
    for mess in server['messages']:
        message = 'The sender id is ' + str(mess['sender_id'])+ '. They said: ' + mess['content']
        print(message)

def newgp():
    for user in (server['users']) : 
        idhh.append(user['id'])
    newnomgp = input('Donnez le nom du groupe  ')
    for user in (server['channels']) : 
        idgp.append(user['id'])
    idgpnew = max(idgp) + 1
    print('Voici la liste des utilisateurs: ')
    users()
    nbpers = int(input('Combien d utilisateurs souhaitez vous ajouter? '))
    if nbpers>len(server['users']): 
        print('Il n y a pas assez d utilisateurs, refaite un groupe qui fonctionne')
        newgp()
    else: 
        for i in range (nbpers): 
            idpersi = int(input('Donner l id des personnes: '))
            if idpersi not in (idhh):
                print('Cet id n existe pas, redonnez un groupe qui marche ')
                newgp()
            else:
                idpers.append(idpersi)
        print(idpers)
    gpnew = {'id': idgpnew, 'name': newnomgp, 'member_ids': idpers }
    server['channels'].append(gpnew)
    sauvegarderjson()

def suppgp(): 
    gpid = int(input('Donner l id du gp que vous voulez sup '))
    initial_length = len(server['channels'])
    server['channels'] = [
        channel for channel in server['channels'] 
        if channel['id'] != gpid
    ]
    final_length = len(server['channels'])
    if final_length < initial_length:
        sauvegarderjson()
        print("Groupe supprimé et le fichier a été sauvegardé.")
    else:
        print(" Erreur : Aucun groupe trouvé avec l ID.")


def newmessage():
    #check il est dans groupe et new mesage 
    sendername = input('Quel est votre nom ')
    senderid = int(get_id_from_name(sendername))
    print('voici les groupes ou vous etes:')
    for channel in (server['channels']): 
        if senderid in channel['member_ids']: 
            print(channel['id'])
            for id_membre in channel['member_ids']:
                id_membres=get_name_from_id(id_membre)
                print(id_membres)
    #cavousva = input('Un des groupe vous convient ? si oui on continue sinon tapez nn')
   # if cavousva == 'nn' : 
    #    newgp()
    gp = int(input('Donner l \'indentifiant du groupe '))
    texto = input('Ecrivez votre messsage : ')
    for channel in (server['channels']) : 
        mid.append(channel['id'])
    newmid =  max(mid) + 1
    newmess = {'id': newmid, "reception_date": "04/11/25", "sender_id": senderid, "channel": gp,
            "content": texto}
    server['messages'].append(newmess)
    sauvegarderjson()
    

menu()

