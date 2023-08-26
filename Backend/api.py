import requests
import pandas as pd

def get_realtime(user):
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap" 
    response = requests.request("GET", url) 
    data = response.json()
    res = [] 
    for p in data["data"]["cryptoCurrencyList"]: 
        res.append(p)
    df = pd.json_normalize(res)
    df = df[['name','symbol','cmcRank','ath','atl','high24h','low24h']]
    high24h = df[df["name"]==user]["high24h"].values[0]
    low24h  = df[df["name"]==user]["low24h"].values[0]
    ath = df[df["name"]==user]["ath"].values[0]
    atl = df[df["name"]==user]["atl"].values[0]
    output = {"high24h":high24h,"low24h":low24h,"ath":ath,"atl":atl}
    return output

