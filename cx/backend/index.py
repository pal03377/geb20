from flask import Flask, render_template, send_from_directory, g, request
from flask_cors import *
import dataset
import json
import random


app = Flask(__name__)
CORS(app)
db = dataset.connect(
    'sqlite:///db.sqlite', engine_kwargs={"connect_args": {'check_same_thread': False}})
day_table = db["day"]
users_table = db["users"]
attacks_table = db["attacks"]
messages_table = db["messages"]


def get_day():
    return day_table.count()

def get_people():
    people = {}
    for user in users_table.all():
        people[user["name"]] = {
            "role": user["role"], 
            "weapon": user["weapon"]
        }
    return people

def get_attacks():
    attacks = []
    for attack in attacks_table.all():
        attacks.append(attack["on"])
    return attacks

def get_messages():
    messages = {}
    for message in messages_table.all():
        if message["to"] in messages:
            messages[message["to"]] += "\n" + message["message"]
        else:
            messages[message["to"]] = message["message"]
    return messages


@app.route("/register_user/<username>")
def register_user(username):
    available = users_table.find_one(name=username) is None
    if not available: return "false"
    users_table.insert(dict(name=username))
    return "true"


@app.route("/data")
def data():
    return {
        "day": get_day(), 
        "people": get_people(), 
        "attacks": get_attacks(), 
        "messages": get_messages()
    }


@app.route("/attack/<from_usr>/<to_usr>")
def attack(from_usr, to_usr):
    attacks_table.insert(dict(
        by=from_usr, 
        on=to_usr
    ))
    return "Angriff wurde durchgeführt."


all_roles = ["Staatsanwalt", "Apothekerin", "Inspektor", "Hochstapler", "Zombie", "Zombie", 
             "Detektiv", "Landstreicher", "Psychologe", "Schlafwandler", "Lehrerin", "Raeuber", 
             "Pastor", "Zombie", "Erfinder", "Gaertner"]
all_weapons = [3, 2, 2, 2, 1, 1, 1, 0, 3, 1, 2, 0, 4, 2, 4, 3]
def assign_roles_and_weapons():
    people = get_people()
    n = len(people.keys())
    while n % 2 == 1 or n > len(all_roles):
        # no even number of / too many users, one has to take a break
        break_user = random.choice(list(people.keys()))
        people[break_user]["role"] = "Aussetzen"
        people[break_user]["weapon"] = 100
        n -= 1
    available_roles = all_roles[:n]
    available_weapons = all_weapons[:n]
    for user in people:
        if people[user]["role"] is None:
            # no role yet
            role = random.choice(available_roles)
            weapon = random.choice(available_weapons)
            people[user]["role"] = role
            people[user]["weapon"] = weapon
            available_roles.remove(role)
            available_weapons.remove(weapon)
        users_table.update({
            "name": user, 
            "role": people[user]["role"], 
            "weapon": people[user]["weapon"]
        }, ["name"])


@app.route("/admin")
def admin():
    return render_template("admin.html", people=get_people())


@app.route("/admin/kick/<username>")
def kick(username):
    return str(users_table.delete(name=username))


@app.route("/admin/start")
def start():
    assign_roles_and_weapons()
    day_table.insert(dict(day=1))
    return "started"

@app.route("/admin/next_day")
def next_day():
    day_table.insert(dict(day=get_day() + 1))
    return "Next day started"
@app.route("/admin/last_day")
def last_day():
    day_table.delete(day=get_day())
    return "Went back to last day"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=9090, 
        debug=True, 
        use_reloader=True
    )
