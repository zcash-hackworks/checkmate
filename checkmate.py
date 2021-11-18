#!/usr/bin/python

import sys
import os
import subprocess
import json

from string import Template

def usage():
    return """
Checkmate: your GetTreeState checkpoint mate. 

checkmate.py LIGHTWALLETD_HOST --start-height HEIGHT [--interval BLOCK_INTERVAL] [--to-json]
--start-height the height you want to start pulling tree states from
--to-json exports the outputs to [height].json files instead of just stdout
"""

def main():
    if len(sys.argv) < 4:
        print(" Error: insufficient arguments")
        print(usage())
        return 1
    
    lightwalletd_host = sys.argv[1]

    start_height = int(sys.argv[3])

    block_interval = 10000
    if "--interval" in sys.argv:
        block_interval = int(sys.argv[5])
     
    to_json = "--to-json" in sys.argv

    command_template = Template("grpcurl -d '{ \"height\" : $height }' $host cash.z.wallet.sdk.rpc.CompactTxStreamer/GetTreeState")

    if to_json:
        command_template = Template("grpcurl -d '{ \"height\" : $height }' $host cash.z.wallet.sdk.rpc.CompactTxStreamer/GetTreeState > $height.json")

    latest_height_template = Template("grpcurl $host cash.z.wallet.sdk.rpc.CompactTxStreamer/GetLatestBlock")
    output = subprocess.check_output(latest_height_template.substitute(host=lightwalletd_host), shell=True)

    latest_block = json.loads(output)
    latest_height = int(latest_block['height'])
    

    for h in range(start_height,latest_height,block_interval):
        os.system(command_template.substitute(height=h,host=lightwalletd_host))
    

if __name__ == "__main__":
    main()