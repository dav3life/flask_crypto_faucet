


Flask crypto faucet 



This web app was made so more people can run a faucet of their own
this webapp can be run locally on your linux pc but can also be deployed on a ubuntu virtual server 
the instructions are for getting it running locally on your machine but will only need slight modifications to get it running an a server.

sorry i dont use windows so i do not have instructions for running it on windows 


step 1 open a block.io account and get an api key for the currency that you want to use for the faucet ... blockio allows you to use Bitcoin, Litecoin and Dogecoin . this repository was primarily made for dogecoin but can be modified to run any of the 3 currencies blockio offers 

step1b add your api key to the routes.py file 


step 2 clone the repository type:

git clone  https://github.com/dav3life/flask_crypto_faucet.git

step 3 use pip to install the requirements for the faucet 

pip install -r requirements.txt 

step 4 build the database 

python db_create.py

step 5 run the server 

python __init__.py



donate Bitcoin 19XTdTvyQHZ5LZA1okPnUhNaCDqUWnmHHN

donate Dogecoin DDcxT5wyxt9KtSfH7Whejh5Qrw3qa5Zqb7

donate Litecoin LPx4dRdZ6qHQxL7JdwVh4UtD1kPgFQ2B31# flask_crypto_faucet
