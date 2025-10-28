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



print('=== Messenger ===')
print('x. Leave')
print('u. Afficher les utilisateurs')
print('gp. Afficher les groupes')
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == 'u':
    for user in (server['users']) : 
        nomid = str(user['id']) + '. ' + user['name'] #nomid=f"{user['id']}. {user['name']}
        print(nomid)
elif choice == 'gp':
    for serv in (server['channels']) :
        groupe = str(serv['id']) + '. ' + serv['name']
        print(groupe)
    choice2 = input('Select a group by its id: ')
    for serv in (server['channels']) :
        if choice2 == serv['id']:
            for mess in server['messages']:
                message= 'The sender id is ' + str(mess['sender_id'])+ '. They said: ' + mess['content']
                print(message)
        else: 
            print('No group')
else:
    print('Unknown option:', choice)

