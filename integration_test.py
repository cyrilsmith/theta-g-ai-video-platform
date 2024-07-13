import requests
import json
from web3 import Web3

def test_generate_and_mint():
    # Step 1: Login to get JWT token
    response = requests.post(
        'http://localhost:5000/login',
        json={'username': 'testuser', 'password': 'testpassword'}
    )
    assert response.status_code == 200
    access_token = response.json()['access_token']

    # Step 2: Upload a sample video file to generate video
    video_file_path = 'sample_video.mp4'  # Ensure this file exists for testing
    with open(video_file_path, 'rb') as video_file:
        response = requests.post(
            'http://localhost:5000/generate',
            headers={'Authorization': f'Bearer {access_token}'},
            files={'file': video_file}
        )
    assert response.status_code == 200
    data = response.json()
    video_uri = data['video_uri']
    assert video_uri.startswith('ipfs://')

    # Step 3: Use the video URI to mint an NFT
    contract_abi = json.load(open('client/src/contractABI.json'))
    web3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    contract_address = '0xYourContractAddress'
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    accounts = web3.eth.get_accounts()
    tx_hash = contract.functions.createNFT(video_uri).transact({'from': accounts[0]})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    assert receipt.status == 1  # Ensure transaction was successful

if __name__ == '__main__':
    test_generate_and_mint()
    print("Integration test passed!")
