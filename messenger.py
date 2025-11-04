from datetime import datetime
import json

with open('servers.json') as f:
    server = json.load(f)

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

idnom = 0

def get_id_from_name(nom):
    for user in (server['users']):
        if nom == user['name']:
            idnom = user['id']
        else:
            idnom
    return idnom


def menu():
    print('=== Messenger ===')
    print('x. Leave')
    print('u. Afficher les utilisateurs')
    print('gp. Afficher les groupes')
    print('b. Back to the menu')
    print('ng: Nouveau groupe')
    print('n : nouvel utilisateur')
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
        choice2 = input('Select a group by its id: ')
        for serv in (server['channels']) :
            if choice2 == serv['id']:
                affichegroupe()  
            else: 
                print('No group')
        choicegp = input('Voulez vous creer un nouveau groupe? si oui tapez ng sinon tapez b pour revenir ')
        if choicegp == 'ng':
            newgp()
        else :
            menu()
    elif choice == 'b':
        menu()
    elif choice == 'ng':
        newgp()
    elif choice == 'n':
        newuser()
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
            idpersi = input('Donner l id des personnes: ')
            for user in (server['users']): 
                if idpersi not in (idhh):
                    print('Cet id n existe pas, redonnez un groupe qui marche ')
                    newgp()
                else:
                    idpers.append(idpersi)
    gpnew = {'id': idgpnew, 'name': newnomgp, 'member_ids': idpers }
    server['channels'].append(gpnew)
    sauvegarderjson()
    

menu()

