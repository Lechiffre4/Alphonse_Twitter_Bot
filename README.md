# Alphonse_Twitter_Bot

## Installation

### Requirements

- [Python 3.9+](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/)

### Installation steps

1. Clone the repository
    ```sh
    git clone https://github.com/Lechiffre4/Alphonse_Twitter_Bot.git
    cd Alphonse_Twitter_Bot
    ```
2. Install the requirements
    ```sh
    pip install -r requirements.txt
    ```
3. Run the bot
    ```sh
    python3 ./main.py
    ```
4. Additionally, you can run the bot with a cron job
    ```sh
    crontab -e
    m h * * * python3 <PATH_TO_MAIN.PY>/main.py >> <PATH_TO_LOG>/alphonse.log
    ```
    *Replace m an h with the time you want to run the bot.*