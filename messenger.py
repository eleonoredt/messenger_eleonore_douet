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
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == 'u':
    for i in range (len(server['users'])) : 
        nomid= str(server['users'][i]['id']) + '. ' +server['users'][i]['name']
        print(nomid)
elif choice == 'gp':
    groupe= server['channels'][1]
else:
    print('Unknown option:', choice)

