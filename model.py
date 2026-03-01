from datetime import datetime




class User:
    def __init__(self, name: str, id: int):
            self.name = name
            self.id = id
    def __repr__(self) -> str:
        return f'User(name={self.name})'
    
    def affiche_user(self):
        print(f"{self.id}. {self.name}")


class Channel:
    def __init__(self, name: str, id: int, members: list[User]):
            self.name = name
            self.id = id
            self.members = members
    def __repr__(self) -> str:
        return f'Channel(name={self.name})'
    
    def affiche_groupe(self, storage):
        print('Nom du groupe : \t' + self.name)
        print('Membres du groupe : \t', end="")
        if len(self.members) > 0:
            member_names = []
            for membre in self.members:
                if membre:
                    member_names.append(membre.name)
            print(", ".join(member_names))
            print("Discussion".center(100, '-'))
            for mess in storage.get_messages_from_channel_id(self.id):
                if mess.channel == self.id:
                    mess.affiche_message(storage)
            print("-"*100)
        else:
            print("Aucun membre")


class Message: 
    def __init__(self, id: int, reception_date: datetime, sender_id: int, channel: int, content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
    
    def affiche_message(self, storage):
        sender_name = storage.get_user_from_id(self.sender_id).name
        message = f'[{self.reception_date.strftime("%Y-%m-%d %H:%M")}] [{sender_name}] \t: {self.content}'
        print(message)