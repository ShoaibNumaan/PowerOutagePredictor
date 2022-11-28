from turtle import back
import pandas as pd
import numpy as np
import pickle
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

# loading in the model to predict on the data
pickle_in = open('Target_Outage.pkl', 'rb')
classifier = pickle.load(pickle_in)

pickle2_in = open('Cause_Outage.pkl', 'rb')
classifier_cause = pickle.load(pickle2_in)
st.set_page_config(layout="wide")


def welcome():
	return 'welcome all'

# defining the function which will make the prediction using
# the data which the user inputs
def prediction(stateName, date, climateCat):
	YYYY = date.year
	MM = date.month
	DD = date.day	
	prediction = classifier.predict(
		[[stateName[0:2], YYYY, MM, DD, climateCat[1]]])
	print(prediction)

	return prediction
	
def cause_prediction(stateName, date, climateCat, target):
	YYYY = date.year
	MM = date.month
	DD = date.day	
	prediction = classifier_cause.predict(
		[[stateName[0:2], YYYY, MM, DD, climateCat[1], target]])
	print(prediction)
	predList = {
		1 : "Equipment failure",
		2 : "Fuel supply emergency",
		3 : "Intentional attack",
		4 : "Islanding",
		5 : "Public appeal",
		6 : "Severe weather",
		7 : "System operability disruption"
	}
	return predList[prediction[0]]


# this is the main function in which we define our webpage
def main():
	page = st.sidebar.radio('Select page', ['Outage Detection App','US Power Outage Report', "US Outage Heat Map", "US Electricity Consumption Report"])
	
	if page == 'Outage Detection App': 
		# state_list
		statelist = [
			"01 Alabama",
			"02 Alaska",
			"03 Arizona",
			"04 Arkansas",
			"05 California",
			"06 Colorado",
			"07 Connecticut",
			"08 Delaware",
			"09 District of Columbia",
			"10 Florida",
			"11 Georgia",
			"12 Hawaii",
			"13 Idaho",
			"14 Illinois",
			"15 Indiana",
			"16 Iowa",
			"17 Kansas",
			"18 Kentucky",
			"19 Louisiana",
			"20 Maine",
			"21 Maryland",
			"22 Massachusetts",
			"23 Michigan",
			"24 Minnesota",
			"25 Mississippi",
			"26 Missouri",
			"27 Montana",
			"28 Nebraska",
			"29 Nevada",
			"30 New Hampshire",
			"31 New Jersey",
			"32 New Mexico",
			"33 New York",
			"34 North Carolina",
			"35 North Dakota",
			"36 Ohio",
			"37 Oklahoma",
			"38 Oregon",
			"39 Pennsylvania",
			"40 South Carolina",
			"41 South Dakota",
			"42 Tennessee",
			"43 Texas",
			"44 Utah",
			"45 Vermont",
			"46 Virginia",
			"47 Washington",
			"48 West Virginia",
			"49 Wisconsin",
			"50 Wyoming"
		]

		# causeList = [
		# 	"Equipment failure [1]",
		# 	"Fuel supply emergency [2]",
		# 	"Intentional attack [3]",
		# 	"Islanding [4]",
		# 	"public appeal [5]",
		# 	"Severe weather [6]",
		# 	"System operability disruption [7]"
		# ]

		climateList = [
			"01 Cold",
			"02 Normal",
			"03 Warm"
		]


		#


		# giving the webpage a title
		#st.title("Power Outage Prediction")
		
		# here we define some of the front end elements of the web page like
		# the font and background color, the padding and the text to be displayed
		html_temp = """
		<div style ="background-color:#4BE9FF;padding:15px">
		<h2 style ="color:black;text-align:center;">Power Outage Prediction ML App </h2>
		</div>
		"""

		# this line allows us to display the front end aspects we have
		# defined in the above code
		st.markdown(html_temp, unsafe_allow_html = True)
		
		# the following lines create text boxes in which the user can enter
		# the data required to make the prediction
		stateName = st.selectbox("Select a State:",statelist)
		date = st.date_input("Enter the date on which you want to predict the outage")
		climateCat = st.selectbox("Please specify climate category for the selected date", climateList)
		# causeCat = st.selectbox("Select the cause expected?", causeList)
		resultOutage =""
		resultCause =""
		
		# the below line ensures that when the button called 'Predict' is clicked,
		# the prediction function defined above is called to make the prediction
		# and store it in the variable result
		if st.button("Predict"):
			resultOutage = prediction(stateName, date, climateCat)

			if resultOutage == 1:
				resultCause = cause_prediction(stateName, date, climateCat, resultOutage)
				resultOutage = 'YES'
				st.warning('Outage: {}'.format(resultOutage))
				st.warning('Casuse: {}'.format(resultCause))
			else:
				resultOutage = "NO"
				st.success('Outage: {}'.format(resultOutage))
	elif page == "US Power Outage Report":
		# components.iframe("https://app.powerbi.com/reportEmbed?reportId=8eb8542d-e455-40df-bff4-e3ec8221cf61&autoAuth=true&ctid=687f51c3-0c5d-4905-84f8-97c683a5b9d1&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLXdlc3QtdXMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQvIn0%3D",
		# height=600, width=600)
		st.title("Power Outage in the US")
		components.html("""
			<iframe title="Power_Outage_Final - Power Outages in US" width="1024" height="1060" src="https://app.powerbi.com/view?r=eyJrIjoiNzRiNWM1OTQtZmMwOS00N2U3LTgwNTUtYWIwZmQ0NjNiZjlkIiwidCI6IjA5ZTI5ZjE2LWZhZjUtNGQ2OS05YzQyLThjYzYyODQ5OGRjYiJ9&pageName=ReportSection" frameborder="0" allowFullScreen="true"></iframe>""",
			height=585)
		# components.iframe("""https://app.powerbi.com/links/h9q8zhrSb-?ctid=09e29f16-faf5-4d69-9c42-8cc628498dcb&pbi_source=linkShare""",
		# width=1060, height=1024)

	elif page == "US Outage Heat Map":
		st.title("Outage Heat Map")
		components.html("""
			<iframe title="Power_Outage_Final" width="1024" height="1060" src="https://app.powerbi.com/view?r=eyJrIjoiOGE0MzQ0MjAtZGM4Ni00Y2M1LThmZGUtOGY1MmM3ZTk3Yzc4IiwidCI6IjA5ZTI5ZjE2LWZhZjUtNGQ2OS05YzQyLThjYzYyODQ5OGRjYiJ9&pageName=ReportSectionc5c2e6604299466d7abb" frameborder="0" allowFullScreen="true"></iframe>""",
			height=585)

	elif page == "US Electricity Consumption Report":
		st.title("Electricity Consumption")
		components.html("""
			<iframe title="Power_Outage_Final" width="1024" height="1060" src="https://app.powerbi.com/view?r=eyJrIjoiOGE0MzQ0MjAtZGM4Ni00Y2M1LThmZGUtOGY1MmM3ZTk3Yzc4IiwidCI6IjA5ZTI5ZjE2LWZhZjUtNGQ2OS05YzQyLThjYzYyODQ5OGRjYiJ9&pageName=ReportSectionaf571ec8d8c04375884b" frameborder="0" allowFullScreen="true"></iframe>""",
			height=585)

if __name__=='__main__':
	main()
