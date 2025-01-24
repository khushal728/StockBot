import yfinance as yf
import nltk
from nltk.chat.util import Chat, reflections
import streamlit as st
import re  # For better handling of user input

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define patterns and responses for the chatbot
# Define patterns and responses for the chatbot
patterns = [
    (r'hi|hello|hey', ['Hello! 👋', 'Hi there! 😊', 'Hey! 👋']),
    (r'how are you', ['I am doing well, thank you! 😊', 'I\'m great, how are you? 😀']),
    (r'what is your name', ['I am StockBot, your friendly stock market assistant! 🤖']),
    (r'bye|goodbye', ['Goodbye! 👋', 'See you later! 😊', 'Have a great day! 🌞']),
    (r'stock price of (.*)', ['Let me check the stock price for %1... 💸']),
    (r'help', ['I can help you with:\n- Stock prices 📈\n- Market information 💼\n- Basic conversation 🗣️\nJust ask!']),
    (r'(.*)', ['I\'m not sure how to respond to that. 🤔', 'Could you please rephrase that? 🤷‍♂️'])
]


# Create chatbot instance
chatbot = Chat(patterns, reflections)


def get_bot_response(user_input):
    try:
        return chatbot.respond(user_input)
    except Exception as e:
        return "I encountered an error. Could you please try again?"


# Fetch real-time stock price using yfinance
def fetch_stock_data(ticker):
    try:
        # Fetch data using yfinance
        stock = yf.Ticker(ticker)

        # Get the latest stock price
        stock_info = stock.history(period="1d")

        # If the stock data is available, return the last price
        if not stock_info.empty:
            last_price = stock_info['Close'].iloc[-1]
            return last_price
        else:
            return None
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None


# Create Streamlit chat interface
st.subheader("StockBot 🤖")
user_input = st.text_input("You:", "")

if user_input:
    response = get_bot_response(user_input)
    st.text_area("StockBot:", value=response, height=100, disabled=True)

    # If user asks about stock price, show the relevant stock information
    if "stock price" in user_input.lower():
        try:
            # Extract ticker symbol using regex (handling more variations in input)
            match = re.search(r"stock price of (\w+)", user_input.lower())
            if match:
                ticker = match.group(1).upper()  # Extract the ticker symbol from the input

                # Fetch stock price
                stock_price = fetch_stock_data(ticker)

                if stock_price is not None:
                    st.metric(f"{ticker} Current Price 💵 ", f"{stock_price:.2f} USD 💰")
                else:
                    st.warning(f"Could not fetch stock price for {ticker}. Please check the ticker symbol ⚠️.")
            else:
                st.warning("Please provide a valid stock ticker, like 'AAPL' or 'GOOGL'. 🧐")

        except Exception as e:
            st.warning("Could not fetch stock price. Please check the ticker symbol or try again later. 😞")
