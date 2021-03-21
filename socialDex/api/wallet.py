from web3 import Web3
import requests

#Ho disattivato la possibilità di ricevere Ether da faucet.Ropsten.be per continui errori dovuti allo spam sul loro sito
#w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/77fd47c9024241998f23e3a52dfecc9d'))
#account = w3.eth.account.create()
#privateKey = account.privateKey.hex()
#address = account.address

#Ho deciso quindi di creare un nuovo account su MetaMask.io
address = '0x1FD7d62add9F5576E3079d6D62F144B969E89C7C'
privateKey = '0xc78cc5438a27b643da9ffd0faba56eaf9ed721a5226e262ee5788fd81be4979f'

def your_data():
	print(f'Your address: {address}\nYour key: {privateKey}')

your_data()