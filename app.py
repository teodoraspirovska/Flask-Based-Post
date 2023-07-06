from flask import Flask, render_template, request
import requests
import smtplib
import os

my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("PASSWORD")
recipient_email = os.environ.get("RECIPIENT_EMAIL")


posts = requests.get('https://api.npoint.io/8a5bf031cddcec2f38b6').json()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", all_posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post, image=requested_post['image'])


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(name=data['name'], email=data['email'], phone=data['phone'], message=data['message'])
        return render_template('contact.html', msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_msg = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage {message} "
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(my_email, recipient_email, email_msg)


if __name__ == "__main__":
    app.run(debug=True)
