import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import re

# Configure the Flask application
app = Flask(__name__)

# Configure a custom filter to format currency
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Run this function after each request to ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Route to show portfolio of stocks


@app.route("/")
@login_required
def index():
    # Fetch user's stocks from the transactions table
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

    # Get current prices and calculate total value for each stock
    for stock in stocks:
        current_stock = lookup(stock["symbol"])
        stock["price"] = current_stock["price"]
        stock["total_value"] = stock["price"] * stock["total_shares"]

    # Get user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Render the template with stocks and cash information
    return render_template("index.html", stocks=stocks, cash=cash)

# Route to buy shares of stock


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")
        try:
            shares = float(shares_input)
            if not shares.is_integer() or shares <= 0:
                return apology("Shares must be a positive whole number")
            shares = int(shares)  # Convert to integer for further processing
        except ValueError:
            return apology("Invalid number of shares")

        # Look up stock information
        stock = lookup(symbol)

        if not stock:
            return apology("Invalid stock symbol")
        if shares <= 0:
            return apology("Shares must be a positive integer")

        # Calculate cost and check user's cash balance
        cost = stock["price"] * shares
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if user_cash < cost:
            return apology("Not enough funds")

        # Update user's cash and add transaction to transactions table
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, stock["price"])

        return redirect("/")
    else:
        return render_template("buy.html")

# Route to show history of transactions


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)

# Route to log user in


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

# Route to log user out


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Route to get stock quote


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock:
            return render_template("quoted.html", stock=stock)
        else:
            return apology("Invalid stock symbol")
    else:
        return render_template("quote.html")

# Route to register user


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide username")
        elif not password:
            return apology("Must provide password")
        elif password != confirmation:
            return apology("Passwords must match")

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("Username already exists")

        hashed_password = generate_password_hash(password)
        result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        if not result:
            return apology("Registration error")

        session["user_id"] = result
        return redirect("/")
    else:
        return render_template("register.html")

# Route to sell shares of stock


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = int(request.form.get("shares"))
        stock = lookup(symbol)

        if not stock:
            return apology("Invalid stock symbol")

        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
                          session["user_id"], symbol)
        if len(rows) != 1 or rows[0]["total_shares"] < shares_to_sell:
            return apology("Not enough shares")

        revenue = stock["price"] * shares_to_sell

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -shares_to_sell, stock["price"])

        return redirect("/")
    else:
        stocks = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)