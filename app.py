from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class List(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.name}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['name']
        detail = request.form['detail']
        list_item = List(name=name, detail=detail)
        db.session.add(list_item)
        db.session.commit()
        return redirect(url_for('hello_world'))  # Redirect to GET request after POST

    if request.method == 'GET' and 'search' in request.args:
        search_term = request.args.get('search')
        allList = List.query.filter(List.name.contains(search_term)).all()
    else:
        allList = List.query.all()

    return render_template('index.html', allList=allList)


@app.route('/products')
def products():
    allList = List.query.all()
    return render_template('products.html', allList=allList)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        detail = request.form['detail']
        list_item = List.query.filter_by(sno=sno).first()
        list_item.name = name
        list_item.detail = detail
        db.session.commit()
        return redirect(url_for('hello_world'))  # Redirect to home page after updating

    list_item = List.query.filter_by(sno=sno).first()
    return render_template('update.html', list_item=list_item)


@app.route('/delete/<int:sno>')
def delete(sno):
    list_item = List.query.filter_by(sno=sno).first()
    db.session.delete(list_item)
    db.session.commit()
    return redirect(url_for('hello_world'))  # Redirect to home page after deleting


if __name__ == "__main__":
    app.run(debug=True, port=8000)
