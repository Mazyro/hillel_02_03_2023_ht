from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if check_users(email) and request.form.get('email') is not None:
            return redirect('/login')
        else:
            add_to_file(email, password)
            render_template('login.html')
    return render_template('registration.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if check_users(email):
            if check_users2(email, password):
                return render_template('dashboard.html')
            else:
                return render_template('dashboard2.html')
    return render_template('login.html')


def check_users(email):
    with open('users.txt', 'r') as f:
        for line in f:
            if email is not None:
                if email in line:
                    return True
        return False


def add_to_file(email, password):
    # Open a file with access mode 'a'
    with open("users.txt", "a") as file_object:
        if email is not None:
            file_object.write(f"email: {email}, password: {password}\n")


def check_users2(email, password):
    with open('users.txt', 'r') as f:
        if password is not None:
            for line in f:
                if email in line:
                    if password in line:
                        return True
            return False


if __name__ == '__main__':
    pass
    # add_to_file('maz3@gmail.com',123)
    # print(check_users('qqq@fff.com'))
    # print(check_users2('rep88@yahoo.com1', '88'))
