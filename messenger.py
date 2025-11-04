from datetime import datetime

server = {
    'users': [
        {'id': 41, 'name': 'Alice'},
        {'id': 23, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 12, 'name': 'Town square', 'member_ids': [41, 23]}
    ],
    'messages': [
        {
            'id': 18,
            'reception_date': datetime.now(),
            'sender_id': 41,
            'channel': 12,
            'content': 'Hi '
        }
    ]
}

ident=[]
idgp=[]
idpers=[]

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
    else:
        print('Unknown option:', choice)

def users():
    for user in (server['users']) : 
        nomid = str(user['id']) + '. ' + user['name'] #nomid=f"{user['id']}. {user['name']}
        print(nomid)

def newuser():
    nomnew = input('Donner le nom du nouvel utilisateur entre guillemets ')
    for user in (server['users']) : 
        ident.append(user['id'])
    newid = max(ident) + 1
    newuser = {'id':newid , 'name': nomnew}
    server['users'].append(newuser)

def groupe():
    for serv in (server['channels']) :
        groupe = str(serv['id']) + '. ' + serv['name']
        print(groupe)

def affichegroupe():
    for mess in server['messages']:
        message = 'The sender id is ' + str(mess['sender_id'])+ '. They said: ' + mess['content']
        print(message)

def newgp():
    newnomgp = input('Donnez le nom du groupe  ')
    for user in (server['channels']) : 
        idgp.append(user['id'])
    idgpnew = max(idgp) + 1
    print('voici la liste des utilisateurs ')
    users()
    nbpers = int(input('Combien d utilisateurs? '))
    for i in range (nbpers): 
        idpersi = input('Donner lid des personnes: ')
        idpers.append(idpersi)
    gpnew= {'id': idgpnew, 'name': newnomgp, 'member_ids': idpers}
    server['channels'].append(gpnew)
    

menu()

