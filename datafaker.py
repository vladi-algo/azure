from faker import Faker
import random
import json


class LoginData:

    def __init__(self):
        fake = Faker()
        self.password = "password@123"
        self.email = fake.email()
        self.username = fake.first_name()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.phone = random.randint(9000000000, 9999999999)
        self.city = fake.city()
        self.about = "This is a sample text : about"

    def get_json(self):
        p = {
            'password': self.password,
            'email': self.email,
            'username': self.first_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'city': self.city,
            'about': self.about,
            'nested_object':  {
                 
                'val1': "obj1",
                'val2': "obj2",
            
            }    
        }
        return json.dumps(p)





#def main():
#    no_of_input = 5
#    input_data(no_of_input)


#main()