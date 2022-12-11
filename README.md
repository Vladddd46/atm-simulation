<h1>ATM SIMULATION</h1>
<h3>Folder structure overview</h3>
<p>server - implementation of server part<p>
<p>client - implementation of client part<p>
<p>card_simulation - contains  .json files, that simulate bank cards. Each file has .json representation of 1 card. These files are needed in order to be inserted for enrty in atm-simulation<p>

<h3>Quickstart</h3>
<p>1. Install python3. To check, that python3 is installed: python3 --version</p>
<p>2. Install requirements: pip3 install -r requirements.txt</p>
<p>2.1 if you have errors during start like "No module [module_name], you should install this module: pip3 install module_name"</p>
<p>3. start server(syntax: main.py ip port): cd server; python3 main.py 127.0.0.1 5000</p>
<p>4. start client(syntax: gui.py port): cd client; python3 gui.py 5000</p>

<h3>Overview</h3>
<p>Simulation of atm. First of all you need to insert card. Card is .json file(./card_simulation). In case of wrong card insert, "Invalid card inserted" message displated After that user should enter pin for inserted card. (for all cards from ./card_simulation pin is 0000). In case of wrong pin, user will get message "Invalid pin". After user entered correct pin, there will be options menu with 4 options ["check balance", "get cash", "send money", "exit"]<br><b>check balance</b> - does request to server, that gets current balance of user card<br><b>get cash</b> - substracts amount of money from user card. immitates getting cash from atm.<br><b>send money</b> - send amount of money from user card to inputed receiver card<br><b>exit</b> - returns to entry screen.</p>