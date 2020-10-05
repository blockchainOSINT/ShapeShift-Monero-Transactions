# getTxData.py
# if Monero tx has a payment ID, save txid, PID, and timestamp to file

import requests, json, time

"""another valid url: https://blox.minexmr.com/api/block/{block_height}"""

def getTxData(block_height):

    txData = []
    payment_ids = [] # to keep track of duplicate pids; ShapeShift requires a unique pid, thus duplicates do not need to be saved **verified
    error = []
    url = f"https://www.xmrchain.net/api/block/{block_height}"
    response = requests.get(url=url)
    if response.status_code == 200:
        response_json = response.json()
        # if block has more than one transaction, disregard the coinbase transaction at index 0
        if len(response_json['data']['txs']) > 1:
            timestamp_utc = response_json['data']['timestamp_utc']
            for tx in response_json['data']['txs'][1:]:
                # if tx has a PID, add txid, pid, and timestamp to list
                if tx["payment_id"] != '':
                    txData.append((tx['tx_hash'], tx['payment_id'], timestamp_utc))
    else:
        print("\aError:", response.content)
        error.append((response.content, block_height))

    return txData, error

def saveData(txData, block_height, speed, startblock, endblock):

    percent_complete = round((block_height - startblock) / (endblock - startblock) * 100, 1)
    print(f"\nSaving...\nSpeed: {speed} blocks per hour", f"\n{percent_complete}% complete\n")

    with open(f"xmr_txData_{startblock}-{endblock}.txt", "a") as file:
        for data in txData:
            file.write(json.dumps(data)+"\n")

    with open(f"saveLog-{startblock}-{endblock}.txt", "a") as saveLog:
        saveLog.write(f"Last saved at Block: {block_height}\n")

def main():

    STARTBLOCK = 1146000 # remember, already have blocks 1515000 - 1520000
    ENDBLOCK   = 1176999 # highest 980000

    save_interval = 100
    last_save = STARTBLOCK # keeps track of blocks already written to file, in case of disconnection
    start_time = time.time()
    save_txData = [] # resets after each save
    total_txData = [] # keeps track of total number of saved datapoints
    errors = [] # keep track of blocks with errors, if any
    print() # add space to terminal for aesthetics

    for block_height in range(STARTBLOCK, ENDBLOCK+1):
        print(block_height)
        txData, error = getTxData(block_height)
        # if error, add error to list
        if error != []:
            errors.append(error)

        save_txData += txData
        total_txData += txData

        if block_height - last_save == save_interval:
            speed = round((block_height - STARTBLOCK) / (time.time() - start_time) * 3600 , 1)
            saveData(save_txData, block_height, speed, STARTBLOCK, ENDBLOCK)
            last_save = block_height
            save_txData = []
        elif block_height == ENDBLOCK:
            speed = round((block_height - STARTBLOCK) / (time.time() - start_time) * 3600 , 1)
            saveData(save_txData, block_height, speed, STARTBLOCK, ENDBLOCK)

    save_file_name = f"xmr_txData_{STARTBLOCK}-{ENDBLOCK}.txt"
    print("\nSaved Transactions:", len(total_txData), "\nSave File:", save_file_name)

    time_elapsed = round((time.time() - start_time) / 60, 1) # minutes
    avg_speed = round(((ENDBLOCK - STARTBLOCK) / time_elapsed), 1) * 60 # bloxks per hour
    finished_alert ="\a"
    print('\nTime Elapsed (mins):', time_elapsed, "\nFinished at:", time.asctime(), "\nAverage Speed:", avg_speed, "blocks per hour\n",
    "\nErrors:", len(errors), errors, finished_alert)


if __name__ == "__main__":
    main()
