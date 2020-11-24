import hashlib
import os
import random
import re
import pandas as pd
from faker import Faker



def generateData(records):
    fake = Faker()
    User_columns = ['user_id', 'first_name', 'last_name',
                    'email_address', 'telephone', 'dob', 'gender']
    Login_columns = ['user_id', 'username', 'password', 'login_date']
    Friends_columns = ['user_id', 'friend_id']
    Post_columns = ['user_id', 'post_id', 'description']
    Photos_columns = ['user_id', 'photo_id', 'description', 'filename']
    User_data = []
    Login_data = []
    Friends_data = []
    Post_data = []
    Photos_data = []
    s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies",
               "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
    p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats",
               "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
    s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures",
               "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
    p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure",
               "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
    infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.",
                   "for a disease.", "to be able to make toast explode.", "to know more about archeology."]

    for i in range(records):
        id = i+1
        description = ' '.join([random.choice(s_nouns), random.choice(s_verbs), random.choice(
            s_nouns).lower() or random.choice(p_nouns), random.choice(infinitives)])
        profile = fake.simple_profile()
        username = profile["username"]
        first_name = profile["name"].split(" ")[0]
        last_name = profile["name"].split(" ")[1]
        email = profile["mail"]
        dob = profile["birthdate"]
        randnum = random.randint(1, records)
        telephone = fake.phone_number()
        telephone = re.sub(r'[^\d]', '', telephone)
        sex = profile['sex']
        password = hashlib.sha256(os.urandom(24)).hexdigest()
        login_date = fake.date_between('-12y')
        User_data.append([id, first_name, last_name,
                          email, telephone, dob, sex])
        Login_data.append([id, username, password, login_date])
        Friends_data.append([id, randnum])
        Post_data.append([id, randnum, description])

    User_data = remove_dups(User_data, 4)
    pd.DataFrame(User_data, columns=User_columns).to_csv(
        'user.csv', index=False)

    Login_data = remove_dups(Login_data, 1)
    pd.DataFrame(Login_data, columns=Login_columns).to_csv(
        'login.csv', index=False)
    pd.DataFrame(Friends_data, columns=Friends_columns).to_csv(
        'friends.csv', index=False)
    pd.DataFrame(Post_data, columns=Post_columns).to_csv(
        'posts.csv', index=False)


def remove_dups(lst, num):
    found = set()
    keep = []
    add = found.add
    app = keep.append
    for item in lst:
        if item[num] not in found:
            add(item[num])
            app(item)
    return keep


if __name__ == '__main__':
    records = 500000
    generateData(records)
