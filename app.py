from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)

@app.route("/")
def index():
    # 説明文、テキストボックス、「実行」ボタンの3つのみをデフォルトで表示する
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    # 閲覧者はテキストボックスに、あるサイトのURLを入れ、「実行」ボタンをクリックする
    url = request.form["url"]

    # 以下の関数にそのURLを入力して実行した結果が、「実行」ボタンの直下に表示される
    result = hoktoscraping(url)
    
    # 結果を HTML にレンダリングして返す
    return render_template("index.html",result=result)


def hoktoscraping(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all('p', class_='hospital-list__title')
    result = []
    res = [element.get_text() for element in elements]
    for scrapingresult in res:
        site = next(search(scrapingresult,num_results = 1))
        result.append(scrapingresult + ':' + site)

    return result

if __name__ == "__main__":
    app.run(debug=True)
