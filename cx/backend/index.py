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
protected_table = db["protected"]


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

def get_protects():
    protects = []
    for pr in protected_table.all():
        protects.append(pr["name"])
    return protects

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
        "protects": get_protects(), 
        "messages": get_messages()
    }


@app.route("/attack/<from_usr>/<to_usr>")
def attack(from_usr, to_usr):
    print("attack", from_usr, to_usr)
    attacks_table.insert(dict(
        by=from_usr, 
        on=to_usr
    ))
    return "Angriff wurde durchgeführt."


@app.route("/send/<to_usr>/<message>")
def send(to_usr, message):
    print("send", to_usr, message)
    messages_table.insert(dict(
        to=to_usr, 
        message=message
    ))
    return "Deine Nachricht an " + to_usr + " wurde gesendet."


@app.route("/switch_weapons/<usr_1>/<usr_2>")
def switch_weapons(usr_1, usr_2):
    print("switch_weapons", usr_1, usr_2)
    people = get_people()
    w_1 = people[usr_1]["weapon"]
    w_2 = people[usr_2]["weapon"]
    users_table.update(dict(
        name=usr_1, 
        weapon=w_2
    ), ["name"])
    users_table.update(dict(
        name=usr_2, 
        weapon=w_1
    ), ["name"])
    messages_table.insert(dict(
        to=usr_1, 
        message="Deine Waffenstärke wurde mit " + usr_2 + " getauscht."
    ))
    messages_table.insert(dict(
        to=usr_2, 
        message="Deine Waffenstärke wurde mit " + usr_1 + " getauscht."
    ))
    return "Du hast deine Waffe mit " + usr_2 + " getauscht."


@app.route("/protect/<by_usr>/<usr>")
def protect(by_usr, usr):
    print("protect", by_usr, usr)
    people = get_people()
    if people[by_usr]["role"] == PASTOR:
        if people[usr]["role"] == ZOMBIE:
            messages_table.insert(dict(
                to=by_usr, 
                message="Du hast versucht, als Pastor einen Zombie zu schützen und dich damit geopfert. Du bist jetzt auch ein Zombie."
            ))
    protected_table.insert(dict(
        name=usr, 
        by=by_usr
    ))
    messages_table.insert(dict(
        to=usr, 
        message="Du warst heute Nacht geschützt (" + str(people[by_usr]["role"]) +  ")."
    ))
    return "Du schützt diese Nacht " + usr + " vor Zombies."


ZOMBIE = "Zombie"
PASTOR = "Pastor"
INVENTOR = "Erfinder"
GARDENER = "Gaertner"
all_roles = ["Staatsanwalt", "Apothekerin", "Inspektor", "Hochstapler", ZOMBIE, ZOMBIE, 
             "Detektiv", "Landstreicher", "Psychologe", "Schlafwandler", "Lehrerin", "Raeuber", 
             PASTOR, ZOMBIE, INVENTOR, GARDENER]
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


@app.route("/all_roles")
def get_all_roles():
    return json.dumps(list(set(all_roles)))


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

@app.route("/admin/reset")
def reset():
    day_table.delete()
    users_table.delete()
    attacks_table.delete()
    messages_table.delete()
    protected_table.delete()
    return "reset"

@app.route("/admin/next_day")
def next_day():
    people = get_people()
    new_day = get_day() + 1
    for p in people:
        # increase their weapon score of inventor
        if people[p]["role"] == INVENTOR:
            people[p]["weapon"] += 1
            users_table.update(dict(
                name=p, 
                weapon=people[p]["weapon"]
            ), ["name"])
        # auto-protect gardener every 2nd night
        if people[p]["role"] == GARDENER and new_day % 2 == 0:
            protect(p, p) # protects himself
    # clear data
    attacks_table.delete()
    messages_table.delete()
    protected_table.delete()
    day_table.insert(dict(day=new_day))
    return "Next day started"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=9090, 
        debug=True, 
        use_reloader=True
    )
