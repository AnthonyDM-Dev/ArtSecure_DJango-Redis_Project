from web3 import Web3
from api import wallet


#Per provare ad utilizzare l'indirizzo di Infura (sconsigliato) sostituire i commenti sotto riportati.
def sendTransaction(message):
	w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/77fd47c9024241998f23e3a52dfecc9d'))
	address = wallet.address #Infura address: '0x1FD7d62add9F5576E3079d6D62F144B969E89C7C'
	privateKey = wallet.privateKey #Infura p_key: '0xc78cc5438a27b643da9ffd0faba56eaf9ed721a5226e262ee5788fd81be4979f'
	nonce = w3.eth.getTransactionCount(address)
	gasPrice = w3.eth.gasPrice
	value = w3.toWei(0, 'ether')
	signedTx = w3.eth.account.signTransaction(dict(
		nonce = nonce,
		gasPrice = gasPrice,
		gas = 100000,
		to = '0x0000000000000000000000000000000000000000',
		value = value,
		data = message.encode('utf-8'),
	), privateKey)

	tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
	txId = w3.toHex(tx)
	return txId