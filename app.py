from datetime import datetime
from email.policy import default
from enum import unique
from re import A
from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Khatabook_Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Khatabook_Database(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    date_of_transaction = db.Column(db.DateTime, default=datetime.utcnow) 
    customer_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    customer_aadhar_no = db.Column(db.String(12), nullable=False)
    amount = db.Column(db.Integer, nullable=False)



class Customer_Database(db.Model):
    customer_name=db.Column(db.String(30), nullable=False)
    aadhar_card=db.Column(db.String(12),unique=True,primary_key=True)
    phnumber=db.Column(db.String(10),nullable=True)

db.create_all()


@app.route("/",methods=["GET","POST"])
def login_page():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username=="Harsh" and password=="Harsh@123":
            return redirect(url_for("infotable"))
    return render_template("index.html")




@app.route("/infotable",methods=["GET","POST"])
def infotable():
    allrows=Khatabook_Database.query.all()
    return render_template("infotable.html",kdb=allrows)



@app.route("/modifydetails",methods=["GET","POST"])
def modifydetails():
    try:
        if request.method=="POST":
            aadhar=request.form["aadharnumber"]
            all_rows=Customer_Database.query.filter_by(aadhar_card=aadhar).first()
            all_rows.customer_name=request.form["name"]
            all_rows.phnumber=request.form["phonenumber"]
            all_rows.aadhar_card=request.form["newaadharnumber"]
            db.session.add(all_rows)
            db.session.commit()
            modifingkhatabook(aadhar)
            return redirect(url_for("showcustomerlist"))
        else:
            return render_template("modifydetails.html")
    except:
        return redirect(url_for("modifydetails"))
        

def modifingkhatabook(ad):
    all_irows=Khatabook_Database.query.filter_by(customer_aadhar_no=ad).all()
    for rows in all_irows:
        rows.customer_name=request.form["name"]
        rows.customer_aadhar_no=request.form["newaadharnumber"]
        rows.phone_number=request.form["phonenumber"]
        db.session.add(rows)
        db.session.commit()


# @app.route("/modify_details",methods=["GET","POST"])
# def modify_details(aadhar):
#     try:
#         if request.method=='POST':
#             all_rows=Customer_Database.query.filter_by(aadhar_card=aadhar).first()
#             all_rows.customer_name=request.form["name"]
#             all_rows.phnumber=request.form["phonenumber"]
#             all_rows.aadhar_card=request.form["aadharnumber"]
#             db.session.add(all_rows)
#             db.session.commit()
#             return redirect(url_for("showcustomerlist"))
#     except:
#         return render_template("modify_details.html")

#     return render_template("modify_details.html")



@app.route("/balanceremaining",methods=["GET","POST"])
def balanceremaining():
    try:
        if request.method=='POST':
            ad=request.form["aadhar"]
            rows=Khatabook_Database.query.filter_by(customer_aadhar_no=ad).all()
            su=0
            for row in rows:
                su+=row.amount
                name=row.customer_name
                pno=row.phone_number
            return redirect(url_for("balancedetails",name=name,ad=ad,pno=pno,su=su))
    except:
        return render_template("balanceremaining.html")
    return render_template("balanceremaining.html")

@app.route("/balancedetails/<name>/<ad>/<pno>/<su>",methods=["GET","POST"])
def balancedetails(name,ad,pno,su):
    return render_template("balancedetails.html",name=name,ad=ad,pno=pno,su=su)

@app.route("/amountreceived",methods=["GET","POST"])
def amountreceived():
    return render_template("amountreceived.html")


@app.route("/addnewtransaction",methods=["GET","POST"])
def addnewtransaction():
    try:
        if request.method=='POST':
            ad=request.form["aadhar"]
            am=request.form["amount"]
            row=Customer_Database.query.filter_by(aadhar_card=ad).first()
            new_entry=Khatabook_Database(customer_name=row.customer_name,phone_number=row.phnumber,customer_aadhar_no=ad,amount=am)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for("infotable"))
    except:
        return redirect(url_for("addnewcustomer"))

    return render_template("addnewtransaction.html")    



@app.route("/debtcleared",methods=["GET","POST"])
def debtcleared():
    return render_template("debtcleared.html")



@app.route("/daywisebreakup",methods=["GET","POST"])
def daywisebreakup():
    return render_template("daywisebreakup.html")



@app.route("/addnewcustomer",methods=["GET","POST"])
def addnewcustomer():
    try:
        if request.method=='POST':
            name=request.form["name"]
            pnumber=request.form["phonenumber"]
            caadhar=request.form["aadharnumber"]
            row = Customer_Database(customer_name=name,phnumber=pnumber,aadhar_card=caadhar)
            db.session.add(row)
            db.session.commit()
            return redirect(url_for("showcustomerlist"))
    except:
        return redirect(url_for("infotable"))
    return render_template("addnewcustomer.html")



@app.route("/showcustomerlist",methods=["GET","POST"])
def showcustomerlist():
    allrow=Customer_Database.query.all()
    return render_template("showcustomerlist.html",cdb=allrow)



if __name__=="__main__":
    app.run(debug=True)
