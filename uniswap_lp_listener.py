from asyncio import get_event_loop, gather, sleep
from json import load, loads, dump
from web3 import Web3
import boto3
from tempfile import NamedTemporaryFile

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIA2TS3H57BTSIAQAIJ',
    aws_secret_access_key='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'
)

s3_bucket = "rahul-messari-challenge-bucket"

eth = "https://mainnet.infura.io/v3/f5162e359e8b40638e35fd3de96dc85e"
web3 = Web3(Web3.HTTPProvider(eth))

with open("contracts/LP.json") as f:
    ABI = load(f)

with open("contracts/ERC20.json") as f:
    ERC20_ABI = load(f)

async def processing_loop(event_filters):
    while True:
        for event_filter in event_filters:
            for Swap in event_filter.get_new_entries():
                event_json = Web3.toJSON(Swap)
                
                event_json = loads(event_json)
                pool_contract = event_json["address"]
                pool_contract = web3.eth.contract(address=pool_contract, abi=ABI)

                token0_addr = pool_contract.functions.token0().call()
                token1_addr = pool_contract.functions.token1().call()

                token0_contract = web3.eth.contract(address=token0_addr, abi=ERC20_ABI)
                token1_contract = web3.eth.contract(address=token1_addr, abi=ERC20_ABI)

                token0 = token0_contract.functions.symbol().call()
                token0_name = token0_contract.functions.name().call()

                token1 = token1_contract.functions.symbol().call()
                token1_name = token1_contract.functions.name().call()

                event_json["token0"] = token0 + "-----" + token0_name
                event_json["token1"] = token1 + "-----" + token1_name
                event_json["pool"] = token0 + "-" + token1
                
                temp = NamedTemporaryFile(mode="w+")
                dump(event_json, temp)
                temp.flush()

                s3.Bucket(s3_bucket).upload_file(Filename=temp.name, Key=event_json["transactionHash"]+".json")

                temp.close()

                print(event_json, "\n------------")

                await sleep(0.01)
                
            await sleep(0.01)


def track_swaps(contracts):
    filters = []
    for contract in contracts:
        contract = web3.eth.contract(address=contract, abi=ABI)
        filters.append(contract.events.Swap.createFilter(fromBlock='latest'))
    
    loop = get_event_loop()
    try:
        loop.run_until_complete(
            gather(
                processing_loop(filters)))
    finally:
        # close loop to free up system resources
        loop.close()
