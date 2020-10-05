# ShapeShift-Monero-Transactions

These scripts will query the ShapeShift API for all Monero input transactions within a given block range (i.e. blocks 1500000-165050)

First, run getTxData.py for the block range you wish to check. This script will generate a text file "xmr_txData_{startblock}-{endblock}.txt" 
with a json formatted list on each line in the form ["txid", "pid", "timestamp_utc"]

Next, run querySS.py, which will create a text file "RESULTS_{startblock}-{endblock}" with ShapeShift transactions statistics (txStats) for all Monero transactions that were 
sent to ShapeShift in your given block range. Each txStat will be saved as a json formatted dictionary on a newline of the save file. 
Two new keys -- "timestamp_utc" and "xmr_txid" -- are added which are not included in the original txStat.

pprint example of first ever Monero ShapeShift txStat on April 7, 2015:

{'address': 'a388e23cd2a046159ac765013d7d53021070fb72dd5d59f800cced7d9fe6baff',
 'incomingCoin': 0.1,
 'incomingType': 'XMR',
 'outgoingCoin': '0.00019812',
 'outgoingType': 'BTC',
 'status': 'complete',
 'timestamp_utc': '2015-04-07 22:30:46',
 'transaction': '8c811a1af9e1af5cc51f48fb6f473d02c8aa92e34b2295e8622ce734beaec4d8',
 'transactionURL': 'https://blockchain.info/tx/8c811a1af9e1af5cc51f48fb6f473d02c8aa92e34b2295e8622ce734beaec4d8',
 'withdraw': '1FAX3X2hfhT7bBFwgwYBQcUmDMFpKbScKh',
 'xmr_txid': '36bfbd424a9a1363f3e62776d787a1ba4cd8911b4ac60f1c770ec92e917ff58e'}
