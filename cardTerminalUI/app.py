from flask import Flask, render_template, Response
import time as t
import nfc
import sqlite3

tempConnection = sqlite3.connect("../website/main.db")
tempCursor = tempConnection.cursor()
tempCursor.execute("SELECT * FROM studentCardIDs")
studentCardIDs = {i[1]:i[0] for i in tempCursor.fetchall()}
tempConnection.close()


connection = sqlite3.connect("studentTimes.db")
cursor = connection.cursor()

app = Flask(__name__)


def connected(tag):
    return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getdata")
def getData():
    def gen():
        with nfc.ContactlessFrontend("usb") as clf:
            while True:
                tagRet = clf.connect(rdwr={"on-connect": connected})
                # Format data
                cardId = str(tagRet).split()[1][3:]
                time = int(t.mktime(t.localtime()))
                # SQL
                cursor.execute("INSERT INTO cardTimes (card_id, time) VALUES (?, ?)", (cardId, time))
                connection.commit()
                if cardId in studentCardIDs:
                    output = str(studentCardIDs[cardId])
                else:
                    output = "unknown student"
                yield("data: {}\n\n".format(output)
                t.sleep(2.0)
    return Response(gen(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
