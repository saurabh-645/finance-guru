import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

    # User reached route via GET (as by clicking a link or via redirect)

    # Query database for all the stocks held by the user
    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", session[
            "user_id"]
    )

    # Calculate the combined total current value of all the stocks owned by the user
    total = 0
    for stock in stocks:
        if stock["shares"] > 0:
            stock["price"] = lookup(stock["symbol"])["price"]
            stock["total"] = stock["price"] * stock["shares"]
            total += stock["total"]

    # Query database for the cash owned by the user
    rows = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )

    # Add the cash to total
    total += rows[0]["cash"]

    return render_template("index.html", stocks=stocks, cash=rows[0]["cash"], total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("mising symbol")

        # Ensure shares was submitted
        if not shares:
            return apology("missing shares")

        # Typecast shares to integer
        try:
            shares = int(shares)
        except ValueError:
            return apology("invalid shares")

        # Ensure shares were a positive integer
        if shares < 1:
            return apology("invalid shares")

        # Lookup for the price of the stock
        quoted = lookup(symbol)

        # Ensure the symbol submitted is valid
        if not quoted:
            return apology("invalid symbol")

        # Calculate the total price of the stocks
        total_price = shares * quoted["price"]

        # Deduct the cash value
        try:
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_price, session["user_id"])
        except  ValueError:
            # If the try code gives a ValueError that means that the user does not have enough money
            return apology("can't afford")

        # Insert the buying transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], quoted["symbol"], shares, quoted["price"])

        # Redirect to the home page
        return redirect("/")

    # User reached route via GET (as by clicking a link)
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # User reached route via GET (as by clicking a link)

    # Query database for user's transactions
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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("mising symbol")

        # Lookup for the price of the stock
        quoted = lookup(symbol)

        # Ensure the symbol submitted is valid
        if not quoted:
            return apology("invalid symbol")

        # Render the quoted page
        return render_template("quoted.html", symbol=quoted["symbol"], price=quoted["price"])

    # User reached route via GET (as by clicking a link)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("missing username")

        # Ensure password was submitted
        elif not password:
            return apology("missing password")

        # Ensure both passwords match
        elif request.form.get("confirmation") != password:
            return apology("passwords don't match")

        # Remember registrant
        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(
                    password)
            )
        except ValueError:
            return apology("username taken")

        # Log the user in by setting the session
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Query database for the stocks and the number of their shares held by the user
    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", session[
            "user_id"]
    )

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("missing symbol")

        # Ensure shares was submitted
        if not shares:
            return apology("missing shares")

        # Typecast shares to integer
        try:
            shares = int(shares)
        except ValueError:
            return apology("invalid shares")

        # Ensure valid shares submitted
        if shares < 1:
            return apology("invalid shares")

        # Find the number of shares owned by the user
        for stock in stocks:
            if stock["symbol"] == symbol:
                owned_shares = stock["shares"]

        # Ensure the user owns that many shares of the stock
        if owned_shares < shares:
            return apology("too many shares")

        # Lookup for the current price of the stock
        quoted = lookup(symbol)

        # Calculate the total_price of the stock
        total_price = shares * quoted["price"]

        # Update cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_price, session["user_id"])

        # Insert the selling transaction
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], quoted["symbol"], -shares, quoted["price"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link)
    return render_template("sell.html", stocks=stocks)
