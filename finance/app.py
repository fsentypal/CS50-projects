import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import re

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

    # Get current prices and calculate total value for each stock
    for stock in stocks:
        current_stock = lookup(stock["symbol"])
        stock["price"] = current_stock["price"]
        stock["total_value"] = stock["price"] * stock["total_shares"]

    # Get user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    return render_template("index.html", stocks=stocks, cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock = lookup(symbol)

        if not stock:
            return apology("Invalid stock symbol")
        if shares <= 0:
            return apology("Shares must be a positive integer")

        cost = stock["price"] * shares
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if user_cash < cost:
            return apology("Not enough funds")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, shares, stock["price"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock:
            return render_template("quoted.html", stock=stock)
        else:
            return apology("Invalid stock symbol")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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

        # Check if username already exists
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

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = int(request.form.get("shares"))
        stock = lookup(symbol)

        if not stock:
            return apology("invalid stock symbol")

        # Check if user owns the stock and has enough shares to sell
        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        if len(rows) != 1 or rows[0]["total_shares"] < shares_to_sell:
            return apology("not enough shares")

        # Calculate total revenue from selling
        revenue = stock["price"] * shares_to_sell

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])

        # Insert transaction into the transactions table with negative shares to indicate a sale
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, -shares_to_sell, stock["price"])

        return redirect("/")

    else:
        # Get the stocks the user owns to populate the dropdown in the sell form
        stocks = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)