import time
from os.path import basename
from solc import compile_source

def getWeb3(endpoint=None):
    if endpoint is None:
        from web3.auto import w3
        return w3
    else:
        from web3 import Web3, HTTPProvider
        return Web3(HTTPProvider(endpoint))


def waitForTransactionReceipt(w3, tx_hash):
    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt is not None:
            break
        time.sleep(1)
    return tx_receipt


def compileContract(fname):
    '''Compile & get Contract's Application Binary Interface & Bytecode'''
    with open(fname, 'r') as f:
        contract_source = f.read()
        name = basename(fname).strip('.sol')
        contract = '<stdin>:{}'.format(name)

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:{}'.format(fname.rstrip('.sol'))]

    contract_bytecode = contract_interface['bin']
    contract_abi = contract_interface['abi']


    return(contract_bytecode, contract_abi)


def deployContract(bytecode, abi, args=[], endpoint=None):
    ''' Compiles and deploys a contract given abi, bytecode and arguments'''
    w3 = getWeb3(endpoint)
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = contract.deploy(args=args, transaction={'from': w3.eth.accounts[0]})

    # Wait until transaction is mined
    tx_receipt = waitForTransactionReceipt(w3, tx_hash)
    contract_address = tx_receipt['contractAddress']

    # Create web3 contract object
    print('Contract ABI {}'.format(abi))
    print('Contract Bytecode {}'.format(bytecode))
    print('Transaction Hash: {}'.format(w3.toHex(tx_hash)))
    print('Contract deployed at: {}'.format(contract_address))

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)

    return contract_instance


def compileAndDeploy(fname, args, endpoint=None):
    bytecode, abi = compileContract(fname)
    return deployContract(bytecode, abi, args, endpoint)

