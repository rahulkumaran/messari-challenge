from asyncio import get_event_loop
from uniswap_lp_listener import track_swaps

contracts = ["0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640", "0x5777d92f208679DB4b9778590Fa3CAB3aC9e2168", "0xCBCdF9626bC03E24f779434178A73a0B4bad62eD", "0x4585FE77225b41b697C938B018E2Ac67Ac5a20c0"] #Univ3 Pairs Contract

if __name__ == "__main__":
    loop = get_event_loop()
    loop.create_task(track_swaps(contracts))
    loop.run_forever()