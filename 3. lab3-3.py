#!/usr/bin/python3
import pandas as pd

url1 = "http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217419&type=222"

def get_tik_data(url):

    page = pd.read_html(url, encoding = 'CP1251')
    part1 = page[6].fillna(method = 'ffill').T
    part2 = page[7].fillna(method = 'ffill').T
    part1[0] = '№ УИК'
    data = part1.append(part2)
    data.index = range(data.shape[0])
    for i in range(16):
        data = data.rename(columns={i:data.loc[1,i]})
    data = data.drop(data.index[[0,1]])
    data.index = range(data.shape[0])
    data.iloc[0, 0] = 'all'
    data.iloc[:, 0] = data.iloc[:, 0].str.replace('УИК №', '')

    for j in range(13,16):
        num=[]
        pr=[]
        for s in data.iloc[:,j]:
            s = s.split()
            num.append(s[0])
            pr.append(float(s[1][:-1]))
        data.iloc[:,j] = num
        data["% " + str(data.columns.values[j]).split()[0]] = pr

    for i in range(1,16):
        data.iloc[:,i]=pd.to_numeric(data.iloc[:,i])

    data.columns.values[12]='лишний'
    del data['лишний']

    return data

tik1 = get_tik_data(url1)

tik1

####
#getting UIK numbers for each MO

colomna = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
cennoy = [15,16,17,18,19,20,21,22]
admiral = [23,24,25,26,27,28,29,30,31,32]
semen = [33.34,35,36,37,38,39,40,41,42]
imzal = [43,44,45,46,47,48,49,50,51,52]
ekateringof = [53,54,55,56,57,58,59,60,61]

#plotting
####
import matplotlib.pyplot as plt

def get_atd(tik):
    l=tik.shape[0]
    atd=[]
    for i in range(1,l):
        atd.append(round(((tik.iloc[i, 3] + tik.iloc[i, 4]) * 100 / tik.iloc[i, 1]), 1))
    return atd

def kolvo_uik_ot_atd(tik):
    l=tik.shape[0]
    uik = [0]*101
    atd=get_atd(tik)
    for i in range(101):
        for j in range(l-1):
            if i<=atd[j]<i+1:
                uik[i]+=1
    return uik

uik = kolvo_uik_ot_atd(tik1)
plt.figure(figsize=(7, 7))
plt.plot(uik,color='b', linewidth=0.5, label = 'ТИК №1')
plt.axis([0, 100, 0, max(uik)+2])
plt.ylabel('Количество УИКов в 1% интервале')
plt.xlabel('Явка, %')
plt.legend()
plt.show()
####

#vizualization
import geopandas as gpd
my_district = gpd.read_file('/home/egor/lab2/izbirkom_parser/mygeodata/border_level8_polygon.shp', encoding='utf-8')

#print(my_district)

my_district = my_district.drop(my_district.index[[0,2,4,7,8,9,11]])

#print(my_district)

my_district=my_district.drop(['url', 'old_name', 'oktmo_user', 'addr_count', 'addr_regio','boundary'],axis=1)
my_district=my_district.drop(['website', 'official_s', 'wikidata', 'wikipedia', 'admin_leve'],axis=1)
my_district=my_district.drop(['name_ru', 'alt_name', 'ref', 'name_de', 'name_en','place'],axis=1)

print(my_district)

my_district.plot(column = 'name', linewidth=0.5, cmap='plasma', legend=True, figsize=[15,15])
my_district = pd.DataFrame(my_district)
my_district.index = [0,1,2,3,4,5]

print(my_district)

mo_list = []
def mo_data(name):
    stat = [0]*5
    for i in range(len(name)):
        if str(name[i]) in tik1['№ УИК'].values:
            row = tik1[tik1['№ УИК'] == str(name[i])].index[0]
            stat[0] += tik1.iloc[row, 1]
            stat[1] += tik1.iloc[row, 3] + tik1.iloc[row, 4]
            stat[2] += tik1.iloc[row, 12]
            stat[3] += tik1.iloc[row, 13]
            stat[4] += tik1.iloc[row, 14]

    mo_list.append(stat)

mo_data(colomna)
mo_data(cennoy)
mo_data(admiral)
mo_data(semen)
mo_data(imzal)
mo_data(ekateringof)

mo_frame = pd.DataFrame(mo_list)

print(mo_frame)

mo_frame.columns = ['kol-vo vsego', 'prishlo', 'Amosov', 'Beglov', 'Tihonova']
mo_frame['Amosov,%'] = mo_frame['Amosov'] / mo_frame['prishlo'] * 100
mo_frame['Beglov,%'] = mo_frame['Beglov'] / mo_frame['prishlo'] * 100
mo_frame['Tihonova,%'] = mo_frame['Tihonova'] / mo_frame['prishlo'] * 100
mo_frame['yavka'] = mo_frame['prishlo'] / mo_frame['kol-vo vsego'] * 100
mo_frame['winner'] = mo_frame.iloc[:,3:5].idxmax(axis=1)


mo_frame['name'] = my_district['name']
mo_frame['geometry'] = my_district['geometry']
mo_frame = gpd.GeoDataFrame(mo_frame)

print(mo_frame)

mo_frame.plot(column = 'winner', linewidth=2, cmap='plasma', legend=True, figsize=[10,10])
mo_frame.plot(column = 'yavka', linewidth=2, cmap='BuPu', legend=True, figsize=[20,20])
mo_frame.plot(column = 'Beglov,%', linewidth=2, cmap='YlOrRd', legend=True, figsize=[20,20])
plt.show()
