# Bitly url shorterer

The program give you short link when you enter long link.
If you enter a short link you will get the number of clicks on a short link for all time.
If you enter incorrect link or short link and HTTP answer will not equal 2xx the program raise exception

### How to install

You should get a token from [bit.ly](https://bit.ly/).
Here the [instruction](https://dev.bitly.com/get_started.html).

You need to create `.env` file and write `TOKEN=<Your token from [bit.ly](https://bit.ly)>`
Token is a long combinations of symbols letters and numbers (about 40 symbols).

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use
Open command line (in windows `Win+R` and write `cmd` and `Ok`). Go to directory with program or just write in cmd:

`python <PATH TO PROGRAM>\bitly-url-shorterer.py <Web-link (with/without http:// or https:// or www.)>`

For helping you can write in cmd:

`python <PATH TO PROGRAM>\bitly-url-shorterer.py -h`

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).