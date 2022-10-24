from flask import Flask,render_template,request
import joblib
import logging
import numpy as np
logging.basicConfig(filename="logfile.log",format=f'%(asctime)s %(levelname)s - %(message)s',filemode='a',datefmt="%Y-%m-%d %H:%M:%S")
popular = joblib.load("popular_info.joblib")
books = joblib.load("books_info.joblib")
pt = joblib.load("pt.joblib")
similarity_score = joblib.load("similarity_score.joblib")


app = Flask(__name__)
@app.route('/')
def index_page():
    return render_template("index.html",
                            book_name = list(popular['Book-Title'].values),
                            author = list(popular['Book-Author'].values),
                            image = list(popular['Image-URL-M'].values),
                            votes = list(popular['num_rating'].values),
                            rating = list(popular['avg_rating'].values)
    )

@app.route('/recommend')
def recommend_page():
    return render_template("recommend.html")


@app.route('/recommend_books',methods=['POST'])
def recommend():
    try:
        book_name_input = request.form.get("book_name_input")
        index = np.where(pt.index == book_name_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])),key = lambda x:x[1],reverse = True)[1:13]
        recommend_data = []
        for i in similar_items:
            item = []
            temp = books[books['Book-Title']== pt.index[i[0]]]
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
            recommend_data.append(item)
    # except error as e:
    #     logging.error(e)
    except Exception as e:
        logging.exception(e)
    return render_template("recommend.html",data = recommend_data)
if __name__=="__main__":
    app.run(debug=True)
