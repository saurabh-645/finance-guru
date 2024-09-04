# Finance Guru

## Description

Finance Guru is a web application that allows users to simulate buying and selling stocks, manage their investment portfolios, and monitor real-time stock prices. Built with Flask and SQLite, Finance Guru provides a user-friendly interface for tracking virtual investments, viewing transaction history, and accessing up-to-date stock information via the Yahoo Finance API.

## Features

- **User Registration and Authentication**: Create an account, log in, and securely manage your profile. Each new user starts with $10,000 in virtual cash.
- **Buy Stocks**: Purchase stocks by entering the stock symbol and the number of shares. The app verifies your cash balance and updates your portfolio accordingly.
- **Sell Stocks**: Sell shares of stocks you own by selecting the stock and specifying the number of shares to sell. Your portfolio and cash balance are updated based on the sale.
- **View Portfolio**: Access a comprehensive view of your current holdings, including the number of shares owned, current stock prices, and the total value of each investment.
- **Stock Quotes**: Retrieve real-time stock prices by entering a stock symbol.
- **Transaction History**: Review a detailed history of all your transactions, including buys and sells, along with the date and time of each action.
- **Responsive Design**: Enjoy a seamless experience across different devices with a mobile-friendly interface built using Bootstrap.

## Getting Started

### Prerequisites

- **Python 3.x**
- **Flask**: A lightweight WSGI web application framework.
- **SQLite**: A C library that provides a lightweight disk-based database.
- **CS50’s SQL Module**: Facilitates interaction with the SQLite database.
- **Yahoo Finance API Key**: Required to fetch real-time stock data.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/finance-guru.git
    cd finance-guru
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the SQLite database**:
    ```bash
    sqlite3 finance.db < schema.sql
    ```

5. **Configure environment variables**:
    Create a `.env` file in the project root:
    ```env
    FLASK_APP=app.py
    FLASK_ENV=development
    ```

6. **Run the Flask development server**:
    ```bash
    flask run
    ```

7. **Access the application**:
    Open your web browser and navigate to the URL provided by Flask (usually `http://127.0.0.1:5000/`).

## Project Structure

- **app.py**: The main Flask application file containing route definitions and application logic.
- **helpers.py**: Helper functions used throughout the application, including user authentication and stock lookup.
- **requirements.txt**: Lists the Python packages required to run the app.
- **schema.sql**: SQL script to set up the initial database schema.
- **static/**: Contains static files like CSS (`styles.css`).
- **templates/**: Contains HTML templates for rendering the web pages.
  - **layout.html**: Base template with the navigation bar and structure.
  - **login.html**: User login form.
  - **register.html**: User registration form.
  - **quote.html**: Stock quote form.
  - **quoted.html**: Display of stock quote results.
  - **buy.html**: Stock purchase form.
  - **sell.html**: Stock selling form.
  - **history.html**: Transaction history display.
  - **index.html**: User portfolio overview.
  - **apology.html**: Error message display.
- **finance.db**: SQLite database file storing user information, stock transactions, and portfolio data.

## Usage

1. **Register**: Create a new user account by providing a unique username and a secure password.
2. **Log In**: Access your account using your credentials.
3. **Buy Stocks**: Enter the stock symbol and the number of shares you wish to purchase. The app will verify your cash balance and update your portfolio.
4. **Sell Stocks**: Select a stock from your portfolio and specify the number of shares to sell. Your portfolio and cash balance will be updated accordingly.
5. **View Portfolio**: Check your current holdings, including the number of shares owned, current stock prices, and the total value of each investment.
6. **Get Stock Quotes**: Enter a stock symbol to retrieve the latest stock price.
7. **View Transaction History**: Review all your past transactions, including buys and sells, with details such as date, time, stock symbol, price, and number of shares.

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository**: Click the "Fork" button at the top of the repository page.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Commit your changes**:
    ```bash
    git commit -m "Add your descriptive commit message"
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Submit a pull request**: Navigate to your forked repository on GitHub and click "New pull request."

Please ensure your code follows the project's coding standards and includes appropriate documentation.

## Contact

**Saurabh   Gupta**  
[saurabhgupta89691@gmail.com](mailto:saurabhgupta89691@gmail.com)  

Project Link: [https://github.com/saurabh-645/finance-guru](https://github.com/saurabh-645/finance-guru)
