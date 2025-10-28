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
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == 'u':
    for user in (server['users']) : 
        nomid = str(user['id']) + '. ' + user['name'] #nomid=f"{user['id']}. {user['name']}
        print(nomid)
elif choice == 'gp':
    for i in range (len(server['users'])-1) :
        groupe = str(server['channels'][i]['id']) + '. ' + server['channels'][i]['name']
        print(groupe)
else:
    print('Unknown option:', choice)

