# Necessary imports
from asyncio import get_event_loop, gather, sleep
from json import load, loads, dump
from web3 import Web3
import boto3
from tempfile import NamedTemporaryFile
from typing import List, Dict, Tuple

# Configuring AWS S3 bucket
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIA2TS3H57BTSIAQAIJ',
    aws_secret_access_key='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'
)
s3_bucket = "rahul-messari-challenge-bucket"

# Initialize QuickNode Endpoint
eth = "https://convincing-cosmological-frost.discover.quiknode.pro/04919fd9c661084bfdb03783e38267c1868b04c2/"

# Instantiate Web3 object with quicknode endpoint
web3 = Web3(Web3.HTTPProvider(eth))

# Read necessary ABIs - dealing with 2 mainly
# One corresponds to LPs on Uniswap
# Other corresponds to ERC20 tokens that make up the LPs on Uniswap
with open("contracts/LP.json") as f:
    ABI = load(f)

with open("contracts/ERC20.json") as f:
    ERC20_ABI = load(f)

def convert_to_checksum(contracts:List) -> List:
    """
    Function to convert list of contract addresses to checksum addresses.
    Sometimes, addresses might be in all lower case and not in the right, 
    this function fixes such addresses

    :param contracts : list of contract addresses that need to be changed toChecksum
    :type contract : List

    :returns : List of contract addresses with address in checksum format
    :rtype : List
    """
    for i in range(0, len(contracts)):
        # Using inbuilt function to convert non-checksum address to checksum
        contracts[i] = web3.toChecksumAddress(contracts[i])

    return contracts

def track_swaps(contracts:List) -> None:
    """
    Function to track swaps, does not return anything - acts as a route to get to processing_loop
    where all "Swap" events emitted from LPs are listened to. This function acts as a way to initialize
    the event loop

    :param contracts : List of contracts that need to be listened to
    :type contracts : List
    """
    # List to store all filters being created
    filters = [] 

    # Safety check to convert all addresses to checksum
    contracts = convert_to_checksum(contracts)
    for contract in contracts:
        # Initialising contract object for every contract in order to interact with and listen to contract
        contract = web3.eth.contract(address=contract, abi=ABI)

        # Create filter to listen to swap events from the latest blocks
        filters.append(contract.events.Swap.createFilter(fromBlock='latest'))
    
    loop = get_event_loop()
    try:
        # Running loop until completion of processing_loop() function
        loop.run_until_complete(
            gather(
                processing_loop(filters)))
    finally:
        # close loop to free up system resources
        loop.close()


async def processing_loop(event_filters:List) -> None:
    """
    Function that constantly listens to all swap events, processes
    them and pushes the relevant transaction data to s3 buckets. This function
    does not return anything.

    :param event_filters : List of web3 event filters that listens for "Swap" events on 
                           multiple Uniswap LP contracts. Each event filter in the list
                           corresponds to one contract
    :type event_filters : List
    """
    # Runs forever
    while True:
        # Running loop for every contract for which event filter
        # has been created in order to listen to every contract
        # for swap events
        for event_filter in event_filters:
            # Runs accurately most times but faces some issues sometimes - TimeOuts and/or if local machine shuts down
            try:
                for Swap in event_filter.get_new_entries():
                    # Convert eveny swap event's emitted details to json format
                    event_json = Web3.toJSON(Swap)
                    
                    event_json = loads(event_json)

                    # Get pool contract in order to get tokens associated with LP
                    pool_contract = event_json["address"]

                    # Create pool contract object to interact with associated LP's contract
                    pool_contract = web3.eth.contract(address=pool_contract, abi=ABI)

                    # Get address of the 2 ERC20's that make up the LP
                    token0_addr = pool_contract.functions.token0().call()
                    token1_addr = pool_contract.functions.token1().call()

                    # Create 2 separate contract objects for each of the ERC20 tokens to interact with them to get necessary data
                    token0_contract = web3.eth.contract(address=token0_addr, abi=ERC20_ABI)
                    token1_contract = web3.eth.contract(address=token1_addr, abi=ERC20_ABI)

                    # Gather symbol and token names for both ERC20 tokens
                    token0 = token0_contract.functions.symbol().call()
                    token0_name = token0_contract.functions.name().call()

                    token1 = token1_contract.functions.symbol().call()
                    token1_name = token1_contract.functions.name().call()

                    # Store data in the already existing variable that has swap based info
                    event_json["token0"] = token0 + "-----" + token0_name
                    event_json["token1"] = token1 + "-----" + token1_name
                    event_json["pool"] = token0 + "-" + token1
                    
                    # Create a temporary file to dump data into in order to push to S3
                    temp = NamedTemporaryFile(mode="w+")
                    dump(event_json, temp)
                    temp.flush()

                    # Push data to s3 bucket where the file name is <transactionHash>.json
                    # This aspect could be done in a better fashion to reduce time to read data
                    # from s3 buckets. Instead of streaming processing and pushing data immediately after every
                    # transaction, a batch function could be written where after every 10-20 transactions, data is
                    # pushed to s3 bucket. This would reduce time of reading data from s3 drastically. Not done now
                    # due to time contraints.
                    s3.Bucket(s3_bucket).upload_file(Filename=temp.name, Key=event_json["transactionHash"]+".json")

                    # Delete temporary file
                    temp.close()

                    # Print transaction data to stdout - helps keep track of information regularly as well.
                    print(event_json, "\n------------")

                    # Give a small break after every event - increasing time here could help reduce timeouts
                    await sleep(0.01)
            except ValueError:
                #In case event not found - happens in some cases
                print("Event Not Not Found or if local system shuts down --- ValueError: {'code': -32000, 'message': 'filter not found'}")
                continue
                
            await sleep(0.01)
