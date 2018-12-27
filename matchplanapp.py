from flask import Flask, render_template
import json

app = Flask(__name__)

scheme = [ ]


def get_user_data(username):
    user_scheme = []

    for round_nr, _round in enumerate(scheme):
        for field_nr, match in enumerate(_round):
            if username in match:
                other_index = 1 - match.index(username)
                user_scheme.append((field_nr, match[other_index]))
                break
        else:
            user_scheme.append(None)

    return user_scheme


@app.route("/schema")
def show_schema():
    return render_template("schema.html", data=scheme)


@app.route("/schema/<username>")
def show_user_schema(username):
    data = get_user_data(username)
    return render_template("user_schema.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    #app.run(debug=True)
