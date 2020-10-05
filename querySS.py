
import requests, json, time, random
from collections import Counter

data_file = "xmr_txData_788100-789099.txt"
save_blocks = data_file.split("_")[2]
save_file = f"RESULTS_{save_blocks}" # automate save file to eliminate naming mistakes
#save_file = "SS_TEST_RESULTS2.txt"
proxy = [{'https': 'https://Drewski:YHpxE4ZFFUZhQ8q@us-wa.proxymesh.com:31280'}, {'https': 'https://Drewski:YHpxE4ZFFUZhQ8q@fr.proxymesh.com:31280'}]

def load_txData(data_file):

    with open(data_file) as f:
        txData = []

        for line in f:
            data = json.loads(line.strip())
            txData.append(data)

    return txData

def removeDuplicatePIDs(txData):
    # discard duplicate PIDs (only unique PIDs yield results in ShapeShift

    pid_count = Counter(data[1] for data in txData)
    unique_txData = [data for data in txData if pid_count[data[1]]==1]

    print("\nPIDs to check:", len(unique_txData), "\n")
    return unique_txData

def checkSS(unique_txData):

    total_queries = 0
    speed_log = 0
    start_time = time.time()
    txStats = []
    errors = []

    for data in unique_txData:
        txid, pid, timestamp = data
        url = f"https://shapeshift.io/txstat/{pid}"
        response = requests.get(url=url, proxies=random.choice(proxy))
        total_queries += 1
        speed_log += 1

        if response.status_code == 200:
            response_json = response.json()
            if response_json["status"] != "error":
                response_json["xmr_txid"] = txid; response_json["timestamp_utc"] = timestamp
                print(response_json, "\n")
                txStats.append(json.dumps(response_json))
        else:
            print("\nError:", url)
            errors.append(url)

        if speed_log == 100:
            print("\t\t\t\tSpeed:", round(total_queries / (time.time() - start_time) * 3600, 1), "queries / hr\n")
            speed_log = 0

    return txStats, total_queries, errors

def save(txStats, save_file):
    with open(save_file, "w") as file:
        for txStat in txStats:
            file.write((txStat)+'\n')

def main():

    start_time = time.time()

    txData = load_txData(data_file)
    unique_txData = removeDuplicatePIDs(txData)
    txStats, total_queries, errors = checkSS(unique_txData)
    save(txStats, save_file)

    finish_time = round((time.time() - start_time) / 60, 2)
    avg_speed = round(total_queries / finish_time * 60, 1)
    finished_alert ="\a"
    print("\nTotal Queries:", total_queries, "\nResults Found:", len(txStats), "\nErrors:", len(errors), errors,
    "\nTime Elapsed (min):", finish_time, "\nAverage Speed:", avg_speed, "queries per hour\n", finished_alert)
    print("Save File:", save_file)

if __name__ == "__main__":
    main()
