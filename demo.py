from utils import getWeb3, compileAndDeploy
import time

### Preparation

FILENAME = 'Crowdfunding.sol'
w3 = getWeb3()

### Deploy a 10 Ether crowdsale that lasts 5 seconds
crowdfunding = compileAndDeploy(FILENAME, [3600, w3.toWei(10, 'ether')])

# 3 contributors appear and donate the needed amount
contribution1 = crowdfunding.functions.contribute().transact({'value':w3.toWei(2, 'ether'), 'from': w3.eth.accounts[1]})
contribution2 = crowdfunding.functions.contribute().transact({'value':w3.toWei(5, 'ether'), 'from': w3.eth.accounts[2]})
contribution3 = crowdfunding.functions.contribute().transact({'value':w3.toWei(3, 'ether'), 'from': w3.eth.accounts[3]})

# Wait for the end of the crowdsale
time.sleep(5)
print('Crowdsale owner owns {} ether'.format(w3.eth.getBalance(w3.eth.accounts[0])))
withdraw = crowdfunding.functions.ownerWithdraw().transact({'from': w3.eth.accounts[0]})
print('Crowdsale owner owns {} ether'.format(w3.eth.getBalance(w3.eth.accounts[0])))

