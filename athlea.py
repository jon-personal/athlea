
from ast import literal_eval
import streamlit as st
import pandas as pd 

schools = pd.read_csv('public_3635.csv',  converters={'State Ranking': literal_eval,'National Ranking':literal_eval, 'Distribution': literal_eval, 'Age':literal_eval,'Income':literal_eval,'Housing':literal_eval,'Race':literal_eval,'Crime Status':literal_eval,'Police':literal_eval,'Population Density':literal_eval,'Nearest Cities':literal_eval,'Unemployment':literal_eval,'Common Industries':literal_eval,'Common Occupation':literal_eval,'Tornados':literal_eval,'Earthquakes':literal_eval,'Natural Disasters':literal_eval,'Comparison': literal_eval})
#schools = pd.read_csv('public_W70_CR200_Temp50_65.csv', converters={'State Ranking': literal_eval,'National Ranking':literal_eval, 'Distribution': literal_eval, 'Age':literal_eval,'Income':literal_eval,'Housing':literal_eval,'Race':literal_eval,'Crime Status':literal_eval,'Police':literal_eval,'Population Density':literal_eval,'Nearest Cities':literal_eval,'Unemployment':literal_eval,'Common Industries':literal_eval,'Common Occupation':literal_eval,'Tornados':literal_eval,'Earthquakes':literal_eval,'Natural Disasters':literal_eval,'Comparison': literal_eval})
#schools = pd.read_csv('public_W70_CR200_Temp50_65_TypeElem_Stat13.csv', converters={'State Ranking': literal_eval,'National Ranking':literal_eval, 'Distribution': literal_eval, 'Age':literal_eval,'Income':literal_eval,'Housing':literal_eval,'Race':literal_eval,'Crime Status':literal_eval,'Police':literal_eval,'Population Density':literal_eval,'Nearest Cities':literal_eval,'Unemployment':literal_eval,'Common Industries':literal_eval,'Common Occupation':literal_eval,'Tornados':literal_eval,'Earthquakes':literal_eval,'Natural Disasters':literal_eval,'Comparison': literal_eval})
#schools = pd.read_csv('pre_sel.csv', converters={'State Ranking': literal_eval,'National Ranking':literal_eval, 'Distribution': literal_eval, 'Age':literal_eval,'Income':literal_eval,'Housing':literal_eval,'Race':literal_eval,'Crime Status':literal_eval,'Police':literal_eval,'Population Density':literal_eval,'Nearest Cities':literal_eval,'Unemployment':literal_eval,'Common Industries':literal_eval,'Common Occupation':literal_eval,'Tornados':literal_eval,'Earthquakes':literal_eval,'Natural Disasters':literal_eval,'Comparison': literal_eval})
#preferred = pd.read_csv('preferred.csv')
#preferred.drop(['Unnamed: 0'], axis=1, inplace=True)
st.set_page_config(
    page_title = "Athlea's School Selection",
    layout = 'wide'
)
layout = st.sidebar.columns([2, 3])

m = st.markdown(""" <style> div.stButton > * { width: 100%; } </style>""", unsafe_allow_html=True)
#justify-content: left; 

st.sidebar.markdown(f"<h1 style='text-align: left; color: black;'>Athlea's School Selection</h1>", unsafe_allow_html=True)
st.sidebar.image("Athlea.jpeg", width=100)

tpe = st.sidebar.radio(
     "School Type",
     ('Elementary', 'All Schools'))


st.sidebar.markdown(f'<p style=" font-size: 20px; text-align: left;"><b>State Temperatures</b></p>', unsafe_allow_html=True)
temps = [25,30,35,40,45,50,55,60,65,70]
temp_min = st.sidebar.selectbox('Min', temps, 0)
idx = temps.index(temp_min)
temp_max = st.sidebar.selectbox('Max', temps[idx:],len(temps[idx:])-1) 

if temp_min == 70:
    schools = schools.query(f'Temperature >= {temp_min}')
else:
    schools = schools.query(f'Temperature > {temp_min} and Temperature < {temp_max}')


user_input = st.sidebar.selectbox('Select a State',sorted(set(schools['State'])))

rac = st.sidebar.selectbox('Percentage of caucasian', [10,20,30,40,50,60,70,80,90], 6)
sort_by = st.sidebar.selectbox('Sort by',['Select','Class Size', 'District', 'Math', 'National Ranking', 'Reading','State Ranking'],6)
#group = st.sidebar.selectbox('Select a Store',sorted(set(schools.columns)))


if tpe == 'Elementary':
    schools = schools.query('Type == "Elementary"')

schools = schools.query(f'White > {rac}')

grouped = schools.groupby('State')


selected = grouped.get_group(user_input)


if sort_by == 'Class Size' or sort_by == 'National Ranking' or sort_by == 'State Ranking' or sort_by == 'District':
    selected = selected.sort_values(by=sort_by)
elif sort_by == 'Select':
    pass
else:
    selected = selected.sort_values(by=sort_by, ascending=False)

if sort_by == 'District':
    dt_choice = st.sidebar.selectbox('Select District',sorted(set(selected['District'])))
    g_district = schools.groupby(['State','District'])
    selected = g_district.get_group((user_input,dt_choice))  
      
s_name_col, choice_col = st.columns((3,3))
header_row, header_spacer = st.columns((5.9, 0.1))
school_info_row1, school_info_row2  = st.columns((3,3))
header_row2, header_spacver2 = st.columns((5.9,0.1))
town_info_row1, town_info_row2 = st.columns((3,3))
save_row_space1, save_row, save_row_spacer2 = st.columns((1.5,3,1.5))

if sort_by != 'Select':
    with s_name_col:
        st.markdown(f'<p style=" font-size: 20px; text-align: center;"><b>School Name</b></p>', unsafe_allow_html=True)
        for i,j in zip(selected['Name'], range(len(selected['Name']))):
            if st.button(i, key=j):
                
                with header_row:
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 20px; text-align: center;"><b>{i} Statistics</b></p>', unsafe_allow_html=True)
                with school_info_row1:
                    grades = (selected.loc[selected['Name'] == i, 'Grades'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Grades: </b>{grades}</p>', unsafe_allow_html=True)
                    st_ranking = (selected.loc[selected['Name'] == i, 'State Ranking'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>State Ranking: </b>{st_ranking}</p>', unsafe_allow_html=True)
                    nt_ranking = (selected.loc[selected['Name'] == i, 'National Ranking'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>National Ranking: </b>{nt_ranking}</p>', unsafe_allow_html=True)
                    cl_size = (selected.loc[selected['Name'] == i, 'Class Size'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Class Size: </b>{cl_size}</p>', unsafe_allow_html=True)
                    mat= (selected.loc[selected['Name'] == i, 'Math'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Math Proficiency: </b>{mat}</p>', unsafe_allow_html=True)
                    reading = (selected.loc[selected['Name'] == i, 'Reading'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Reading Proficiency: </b>{reading}</p>', unsafe_allow_html=True)
                    dist = (selected.loc[selected['Name'] == i, 'District'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>District: </b>{dist}</p>', unsafe_allow_html=True)
                    addrss = (selected.loc[selected['Name'] == i, 'Address'].values)[0]
                    phone = (selected.loc[selected['Name'] == i, 'Phone'].values)[0]
                    
                    webs = (selected.loc[selected['Name'] == i, 'Website'].values)[0]
                    us_news = (selected.loc[selected['Name'] == i, 'US News Link'].values)[0]
                    dt_link = (selected.loc[selected['Name'] == i, 'District Link'].values)[0]
                    realt = (selected.loc[selected['Name'] == i, 'ct_st'].values)[0]
                    realtor = f"https://www.realtor.com/realestateandhomes-search/{realt}/beds-3/baths-3/age-10?view=map"
                    land = f'https://www.realtor.com/realestateandhomes-search/{realt}/type-land?view=map'
                with school_info_row2:
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>{i} Demographics</b></p>', unsafe_allow_html=True)
                    distribution = (selected.loc[selected['Name'] == i, 'Distribution'].values)[0]
                    for z in distribution:
                        st.write(f'--{z}: {distribution[z]}')
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Address: </b>{addrss}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Phone: </b>{phone}</p>', unsafe_allow_html=True)
                    st.write(f"**Links:** [Website]({webs}),  [More info]({us_news}),  [All District Schools]({dt_link}),  [Houses]({realtor}), [Land]({land})")
                    #st.write(f"**Links:** [Website]({webs}),  [More info]({us_news}),  [All District Schools]({dt_link})")
                with header_row2:
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 20px; text-align: center;"><b>City Statistics Statistics</b></p>', unsafe_allow_html=True)
                with town_info_row1:
                    age = (selected.loc[selected['Name'] == i, 'Age'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Median Age: </b>{age[0]} - <b>State: </b>{age[1]}</p>', unsafe_allow_html=True)
                    pov = (selected.loc[selected['Name'] == i, 'Poverty'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>{pov}</b></p>', unsafe_allow_html=True)
                    police = (selected.loc[selected['Name'] == i, 'Police'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Law Enforcement Statistics: </b></p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>-- Officers: </b>{police[0]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>-- Police Officers: </b>{police[1]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>-- Police per 1000: </b>{police[2]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>-- State Average: </b>{police[3]}</p>', unsafe_allow_html=True)
                    so = (selected.loc[selected['Name'] == i, 'Sex Offender'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Sex Offender: </b>{so}</p>', unsafe_allow_html=True)
                    crime = (selected.loc[selected['Name'] == i, 'Crime Status'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Crime Statistics: </b></p>', unsafe_allow_html=True)
                    for c in crime[:-1]:
                        st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>{c[0]}: </b>{c[1]} - <b>Per 1000: </b>{c[2]}</p>', unsafe_allow_html=True)
                    crime_rate = (selected.loc[selected['Name'] == i, 'Crime Rate'].values)[0]
                    if len(crime_rate) > 10:
                        st.write(f"**Crime Rate:** [Link]({crime_rate})")
                    else:
                        st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Crime Rate: </b>{crime_rate} - <b>National Average: </b>270.6</p>', unsafe_allow_html=True)
                    air = (selected.loc[selected['Name'] == i, 'Air'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Air Quality: </b>{air}</p>', unsafe_allow_html=True)
                    temp = (selected.loc[selected['Name'] == i, 'Temperature'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Average Yearly Temperature: </b>{temp}</p>', unsafe_allow_html=True)
                    near = (selected.loc[selected['Name'] == i, 'Nearest Cities'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Nearest Cities: </b></p>', unsafe_allow_html=True)
                    for nc in near:
                        st.write(f'--{nc}')
                    com_in = (selected.loc[selected['Name'] == i, 'Common Industries'].values)[0]
                    com_oc = (selected.loc[selected['Name'] == i, 'Common Occupation'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Common Industries: </b></p>', unsafe_allow_html=True)
                    for ci in com_in:
                        st.write(f"--{ci}")
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Common Occupation: </b></p>', unsafe_allow_html=True)
                    for co in com_oc:
                        st.write(f"--{co}") 
                    comp = torn = (selected.loc[selected['Name'] == i, 'Comparison'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Comparison: </b></p>', unsafe_allow_html=True)
                    for com in comp:
                        st.write(f"--{com}") 
        
                with town_info_row2:
                    income = (selected.loc[selected['Name'] == i, 'Income'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Median Income: </b>{income[0][1:]} - <b>State: </b>{income[1][1:]}</p>', unsafe_allow_html=True)
                    house = (selected.loc[selected['Name'] == i, 'Housing'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Median Housing: </b>{house[0][1:]} - <b>State: </b>{house[1][1:]}</p>', unsafe_allow_html=True)
                    race = (selected.loc[selected['Name'] == i, 'Race'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Demographics: </b></p>', unsafe_allow_html=True)
                    for r in race:
                        st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>-- {r[0]}: </b>{r[1]}</p>', unsafe_allow_html=True)
                    ele =  (selected.loc[selected['Name'] == i, 'Elevation'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Elevation: </b>{ele}</p>', unsafe_allow_html=True)  
                    pop = (selected.loc[selected['Name'] == i, 'Population'].values)[0]
                    st.write(f"**Population:** [Link]({pop})")
                    pop_den = (selected.loc[selected['Name'] == i, 'Population Density'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Population Density: </b></p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>--Grade: </b>{pop_den[1]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>--Per Square Mile: </b>{pop_den[0]}</p>', unsafe_allow_html=True)
                    unem = (selected.loc[selected['Name'] == i, 'Unemployment'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Unemployment: </b>{unem[0]} - <b>State: </b>{unem[1]}</p>', unsafe_allow_html=True)
                    torn = (selected.loc[selected['Name'] == i, 'Tornados'].values)[0]
                    eart = (selected.loc[selected['Name'] == i, 'Earthquakes'].values)[0]
                    natu = (selected.loc[selected['Name'] == i, 'Natural Disasters'].values)[0]
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Tornados: </b></p>', unsafe_allow_html=True)
                    for to in torn:
                        st.write(f"--{to}") 
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Earthquakes: </b></p>', unsafe_allow_html=True)
                    for ea in eart:
                        st.write(f"--{ea}") 
                    st.markdown(f'<p style=" font-size: 17px; text-align: left;"><b>Natural Disasters: </b></p>', unsafe_allow_html=True)
                    for nat in natu:
                        st.write(f"--{nat}") 
                    #stt =  dist = (selected.loc[selected['Name'] == i, 'State'].values)[0]
                    #lst = [i, stt]
                    #preferred.loc[len(preferred)] = lst
                         
                    st.sidebar.write(f"Curret: {i}")            

    
    with choice_col:
        st.markdown(f'<p style=" font-size: 20px; text-align: center;"><b>{sort_by}</b></p>', unsafe_allow_html=True)
        for i,j in zip(selected[sort_by], range(1000, 1000+len(selected[sort_by]))):
            if i == 0 or i == '0':
                i = 'No info'
                st.button(str(i), key=j, disabled=True)
            else:
                st.button(str(i), key=j, disabled=True)

else:
    with s_name_col:
        st.markdown('School Name')
        for i,j in zip(selected['Name'], range(len(selected['Name']))):
            st.button(i, key=j)

#st.sidebar.write(f"Last Save: {(preferred['School Name'].values)[-2]}")
def convert_df(df):
     return df.to_csv().encode('utf-8')

#csv = convert_df(preferred)

#st.sidebar.download_button( label="Save", data=csv, file_name='preferred.csv', mime='text/csv',)



    