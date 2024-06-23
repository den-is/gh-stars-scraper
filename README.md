# GitHub Stars scraper

Primitive web-scraper for your own GitHub Stars for further analysis or to recall long-time agi forgotten repos.

This script is extremly plain and primitive.

Script utilizes [selenium](https://www.selenium.dev/) web automation library.

Contributions are welcome.

## Requirements
- Chrome Browser
- chromedriver
- python 3.9+

## Installation
Instructions shown for Unix based Operating Systems (specifically MacOS)

Download stable [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/).
Better if version matches to version of your Chrome Browser.

```sh
cd ~/Downloads
curl -OL https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.63/mac-x64/chrome-mac-x64.zip
unzip chrome-mac-x64.zip

# on MacOS you might need to run
cd chromedriver-mac-x64
xattr -d com.apple.quarantine chromedriver
```

Scraper setup
```sh
git clone https://github.com/den-is/gh-stars-scraper.git

cd gh-stars-scraper

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Running scraper
- Create `.env` file with correct values from provided `.env.example`.
- Run script `python3 main.py`
- Wait script to open browser window and open login page
- Provide OTP code (I hope you have protected your github account with 2FA authentication)
- Watch magic to happen
- Do not interact with the web page

## Known-issues
- For some reason, rarely script is not able to fetch lists some specific repo belongs to.
