<h1 align="center">Hi, I'm Mateus</h1>

- 🌱 I’m currently learning **Python**

- 👯 I’m looking to collaborate on **any cool project envolving automation or bots**

- 👨‍💻 All of my projects are available at [https://github.com/mateusorn](https://github.com/mateusorn)

- 📫 How to reach me **eumateusorn@gmail.com**

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://instagram.com/mateusorn" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="mateusorn" height="30" width="40" /></a>
<a href="https://discord.gg/Mateus Ørn#3136" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg" alt="Ørn#8958" height="30" width="40" /></a>
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://www.arduino.cc/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/arduino-1.svg" alt="arduino" width="40" height="40"/> </a> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://golang.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/go/go-original.svg" alt="go" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://unity.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/unity3d/unity3d-icon.svg" alt="unity" width="40" height="40"/> </a> </p>

# Stop Win-Loss Binance Bot
 If you are reading needs I want to make you clear that It's my first "big" project with Python and I still learning a lot, and since we are talking about money, I'm not responsible for your money, this bot can help you a lot, but it can also fail and end up not setting up the stop loss on your trades and you can end up losing money! be aware of it!
 
# Requirements
```
pip install python-binance
pip install binance
pip install colorama
```
# How to use
>[How to create your API on Binance (YouTube Video)](https://youtu.be/JqqcqxXTR40)

 First of all, open your config.json and fill according to description:
 ```
{
  "public_api": "6xqLf73fLLuLAwBo95QhqMqan195e0gUr1y6sKhabznsAHELmShz7pwiUDskxAIR",  #Don't know how to create your API?
  "private_api": "hjplYxrnyuQ7ya2Jzd3NOPpjhSpwciPYqfwTR53WOqEsai5ZGZmAxWHJfinPqiC",  #Check the video above!
  "stop_gain": 1.05, 
  "stop_loss": 0.98
}
# For some people it's hard to understand, so I'll let some examples here and hope you get it! 
# [0.90 - 10% LOSS] [1.10 - 10% GAIN] [1.04 - 4% GAIN] [0.98 - 2% LOSS]
# 'stop_gain' needs to be more then 1.01 and 'stop_loss' needs to be smaller than 0.99
```
 Remember, this bot isn't made for instant transactions, if you create a order and it gett instantly filled, the bot may not capture the order and a stop loss isn't going to be created.
