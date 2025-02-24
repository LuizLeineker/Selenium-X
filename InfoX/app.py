from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from sqlalchemy import delete

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)


def getPost(link, driver, database):
    driver.get(link)
    sleep(4)
    profile = driver.find_element(By.XPATH,
                                  '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/span').text
    sleep(2)

    times = driver.find_element(By.TAG_NAME, 'time').text
    sleep(2)

    try:
        data = driver.find_element(By.XPATH,
                                   '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div[1]/div/article/div/div/div[2]/div[2]/div[2]').text

        if not data.strip():
                data = "Infelizmente não foi possivel carregar a publicação. Para acessar o conteúdo completo acesse o link!"

    except:
        data = "Infelizmente não foi possivel carregar a publicação. Para acessar o conteúdo completo acesse o link!"

    sleep(3)

    urls = link


    with app.app_context():
        db.create_all()
        public = db.session.query(Posts).all()
        for i in public:
            if data == i.content and profile == i.name:
                print("Esse POST o foi inserido!")
                db.session.delete(i)
                db.session.commit()
        new = Posts(name=profile, time=times, content=data, url=urls)
        db.session.add(new)
        db.session.commit()

driver = webdriver.Chrome()
database = []


getPost('https://x.com/LulaOficial', driver, database)
getPost('https://x.com/realDonaldTrump', driver, database)
#getPost('https://x.com/BillGates', driver, database)
driver.close()

with app.app_context():
    public = db.session.query(Posts).all()
    for i in public:
            base = {
                "name": i.name,
                "time": i.time,
                "content": i.content,
                "url": i.url
            }
            database.append(base)

@app.route('/')
def twitter():
    return render_template("index.html", posts=database)




if __name__ == '__main__':
    app.run()

