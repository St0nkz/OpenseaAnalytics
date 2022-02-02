import json,requests,signal,sys
import streamlit as st
import pandas as pd
from time import sleep                         # Allow sleep
from datetime import datetime                  # Allow the printing of current time
from IPython.display import clear_output       # Clears output

# Ether Scan Api Key
apikey = '1VYJVVGJ18M8WSQ5HUSR2YJKP94BP4FDAG'
wei = 1/(10**18)

# Graceful Exit                     
terminate = False                            
def signal_handling(signum,frame):           
    global terminate                         
    terminate = True                         

# Format numbers to shorten for thousands and millions
def formatnumber(value_int):
	if value_int >= 1000000 :
		value = "%.1f%s" % (value_int/1000000.00, 'M')
	elif value_int >= 1000 :
		value = "%.1f%s" % (value_int/1000.0, 'k')
	return value

# Sort array to biggest to smallest
def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li


# Side Bar Contents
selection = st.sidebar.selectbox("Endpoints",["Collection", "Rarity", "Events", "Assets"])

st.sidebar.write("Sidebar contents")


st.title("Opensea NFT API Explorer - " + selection)


collection=st.sidebar.text_input("Enter the name of the Collection")
if st.sidebar.button("cool-cats-nft"):
	collection="cool-cats-nft";
if st.sidebar.button("azuki"):
	collection="azuki";
if st.sidebar.button("doodles-official"):
	collection="doodles-official";
if st.sidebar.button("clonex"):
	collection="clonex"


# Main Collection Body
if selection == "Collection":

	if collection:
		collectionUrl = 'https://api.opensea.io/api/v1/collection/'+collection

		try:
			response = requests.get(collectionUrl)
			response_json = json.loads(response.content)
			if not len(response_json):
			   st.write("Issue with the name of the Collection input. Please re-enter.")
			else:

				#General Colleciton Banner images
				st.image(response_json["collection"]["banner_image_url"])
				st.title(response_json["collection"]["name"])
				
				
				totalSupply=response_json["collection"]["stats"]["total_supply"]
				#Show the general Stats of the Collection
				col1, col2, col3, col4, col5 = st.columns(5)
				col1.image(response_json["collection"]["image_url"])
				col2.metric(label="Total Supply", value=formatnumber(totalSupply))
				col3.metric(label="Owners", value=formatnumber(response_json["collection"]["stats"]["num_owners"]))
				col4.metric(label="Floor Price", value=response_json["collection"]["stats"]["floor_price"])
				col5.metric(label="Volume Traded", value=formatnumber(response_json["collection"]["stats"]["total_volume"]))

				st.write(response_json)
		except Exception as e: 
			st.write("Issue with the name of the Collection input. Please re-enter.")
			st.write(e)


# Main Rarity Body
if selection == "Rarity":
	



	if collection:
		collectionUrl = 'https://api.opensea.io/api/v1/collection/'+collection

		try:
			response = requests.get(collectionUrl)
			response_json = json.loads(response.content)
			if not len(response_json):
			   st.write("Issue with the name of the Collection input. Please re-enter.")
			else:
				
				#General Colleciton Banner images
				st.image(response_json["collection"]["banner_image_url"])
				st.title(response_json["collection"]["name"])
				
				
				totalSupply=response_json["collection"]["stats"]["total_supply"]
				#Show the general Stats of the Collection
				col1, col2, col3, col4, col5 = st.columns(5)
				col1.image(response_json["collection"]["image_url"])
				col2.metric(label="Total Supply", value=formatnumber(totalSupply))
				col3.metric(label="Owners", value=formatnumber(response_json["collection"]["stats"]["num_owners"]))
				col4.metric(label="Floor Price", value=response_json["collection"]["stats"]["floor_price"])
				col5.metric(label="Volume Traded", value=formatnumber(response_json["collection"]["stats"]["total_volume"]))

				# Query the list of traits for the collection
				traitsList = response_json["collection"]["traits"]
				st.header(str(len(traitsList)) + " Traits:")
				count=0
				col1, col2= st.columns(2)
				# Sort the traits in ascending order
				for traits in traitsList:
					sortedTraits=dict(sorted(traitsList[traits].items(), key=lambda item: item[1]))
					totalTraitSum=sum(sortedTraits.values())
					
					for i in sortedTraits:
						traitPercent= "{:.2%}".format(sortedTraits[i]/totalSupply)
						totalTraitPercent= "{:.2%}".format(totalTraitSum/totalSupply)
						sortedTraits[i]=[sortedTraits[i],traitPercent]
					if count%2==0:
						col1.write(traits + " (" +str(totalTraitSum) + ", "+totalTraitPercent+")")
						col1.write(pd.DataFrame.from_dict(sortedTraits, orient='index', columns=['Count', 'Percentage']))
					else :
						col2.write(traits + " (" +str(totalTraitSum) + ", "+totalTraitPercent+")")
						col2.write(pd.DataFrame.from_dict(sortedTraits, orient='index', columns=['Count', 'Percentage']))
					count+=1


		except Exception as e: 
			st.write("Issue with the name of the Collection input. Please re-enter.")
			st.write(e) 



# Main Assets Body
if selection == "Assets":
	params = {
    		'collection': 'azuki'
	}

	response = requests.get("https://api.opensea.io/api/v1/assets", params=params)
	response_json = json.loads(response.content)    

	st.write(response_json)
