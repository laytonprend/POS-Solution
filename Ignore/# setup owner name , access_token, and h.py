# setup owner name , access_token, and headers 
owner='laytonprend'
access_token='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' 
headers = {'Authorization':"Token "+access_token}

url='https://raw.githubusercontent.com/laytonprend/POS-Solution/main/products.csv?token=GHSAT0AAAAAACJ4PLXTRKVRZ7IPLXG5K57YZKH73IQ'
repo=requests.get(url,headers=headers).json()

