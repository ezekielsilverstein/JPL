#Numerical Python
import numpy as np

#Pylab Plotting
import pylab
import matplotlib.pyplot as plt


#INTERNET
#Selenium Internet Browsing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


import os
from decimal import *

import time

import csv

#Internet
import urllib2

print "Start up complete"

#call time upon starting
start_time=time.time()

#open Atlas
#Atlas=webdriver.Firefox()
#Atlas.get('http://isc.astro.cornell.edu/~sloan/library/swsatlas/aot1.html')

#Import Greg Sloan data
Sloan_List=np.genfromtxt('Sloan_List_RA_DEC.txt',delimiter='	',\
skip_header=1,dtype=[('source',object),('TDT',object),('RA',object),\
('DEC',object),('classification',object)])

for name in Sloan_List.dtype.names:
	if name=='source':
		source=Sloan_List[name]
	if name=='TDT':
		TDT=Sloan_List[name]
	if name=='RA':
		RA=Sloan_List[name]
	if name=='DEC':
		DEC=Sloan_List[name]
	if name=='classification':
		classification=Sloan_List[name]

#Make each TDT entry 8 digits
for i in range(len(TDT)):
	if len(TDT[i])<8:
		TDT[i]='0'+TDT[i]


#remove spaces at end of source names
for i in range(len(source)):
	if source[i][-1]==' ':
		source[i]=source[i][:-1]

#MAKE DICTIONARIES

#create lists for the meanings of the classifications, subsets, and suffixes
level1_meanings=['naked star','star associated with dust',\
'warm dusty object with little or no stellar contribution',\
'cool dusty object','red spectrum rising to 45um','no continuum',\
'flawed spectrum']

level2_meanings=['carbon-rich dust emission, dominated by SiC at 11.5um',\
'carbon-rich proto planetary nebula',\
'reddened continuum from amorphous carbon',\
'carbon-rich spectrum showing the 21um feature',\
'emission lines are the only significatn spectral feature',\
'featureless (Groups 4 and 5)','miscellaneous',\
'naked star, no molecular bands (Group 1 only)',\
'naked star with oxygen-rich molecular bands (Group 1 only)',\
'naked star with carbon-rich molecular bands (Group 1 only)',\
'naked star with emission lines (Group 1 only)',\
'a miscellaneous group of naked stars (Group 1 only)',\
'planetary nebula, many emission lines',\
'as PN, but with UIR features',\
'oxygen-rich dust, 10um silicate absorption',\
'oxygen-rich dust, self-absorbed silicate emission at 10um',\
'crystalline silicate emission, especially at longer wavelengths',\
'oxgyen-rich dust emission at 10-12 um',\
'broad low-contrast dust feature from alumina',\
'structured silicate emission',\
'classic narrow silicate emission',\
'crystalline silicate emission at 10-11um and to the red',\
'UIR emission features dominate the spectrum',\
'UIR emission features dominate the spectrum as only significant spectral feature',\
'spectrum peaks 5-8um, drops to red, many are WR stars',\
'silicate/carbon stars',\
'mixture of carbon-rich and crystalline silicate features',\
'mixture of UIR and crystalline silicate features',\
'not applicable']

suffix_meanings=['emission lines','peculiar','UIR features present',\
'uncertain classification','very uncertain classification']


#create lists of the classifications, subsets, and suffixes
classification_subset_names=['level1','level2','suffix']
classification_subsets=[]
level1=['1','2','3','4','5','6','7']
level2=['CE','CN','CR','CT','E','F','M','N','NO','NC','NE','NM',\
'PN','PU','SA','SB','SC','SE','SEa','SEb','SEc','SEC','U','UE','W','C/SE',\
'C/SC','U/SC','N/A']
suffix=['e','p','u',':','::']
classification_subsets.append(level1)
classification_subsets.append(level2)
classification_subsets.append(suffix)

#create dictionaries for the meanings
level1_meanings_dict={}
for i in range(len(level1)):
	level1_meanings_dict[level1[i]]=level1_meanings[i]

level2_meanings_dict={}
for i in range(len(level2)):
	level2_meanings_dict[level2[i]]=level2_meanings[i]

suffix_meanings_dict={}
for i in range(len(suffix)):
	suffix_meanings_dict[suffix[i]]=suffix_meanings[i]

#MAKE MASTER DICTIONARY for classification meanings
Sloan_meanings={}
Sloan_meanings[classification_subset_names[0]]=level1_meanings_dict
Sloan_meanings[classification_subset_names[1]]=level2_meanings_dict
Sloan_meanings[classification_subset_names[2]]=suffix_meanings_dict

#Rawlist of objects and their classifications
Sloan_objects_list=[]

for i in range(len(source)):
	Sloan_objects_list+=[[source[i]]+[TDT[i]]+[classification[i]]+[RA[i]]+[DEC[i]]]

Sloan_objects=np.array(Sloan_objects_list)

#How to search
#for i in range(len(Sloan_objects)):
#	if Sloan_objects[i][0]=='NGC 1386':
#		print i

#outputs instance where object name is 'NGC 1386'

######
#Create folders
#execfile('/Users/esilverstein1992/Desktop/Scripts/JPL/color mag plot/Object Spectra/SLOAN LIST/create_folders.py')

#create base folder location
# base='/Users/esilverstein1992/Desktop/Scripts/JPL/color mag plot/Object Spectra/SLOAN LIST/'

#create Master folder
# os.mkdir(base+'MASTER')
os.mkdir('MASTER')

#enter Master folder
# os.chdir(base+'MASTER')
os.chdir('MASTER')

#create level1 folders
# for i in level1:
# 	os.mkdir(base+'MASTER/'+str(i))
for i in level1:
	os.mkdir(str(i))

#alter names of level2 dictionaries with '/' to create folders
for j in range(len(level2)):
	for k in range(len(level2[j])):
		if level2[j][k]=='/':
			level2[j]=level2[j][0:k]+'|'+level2[j][k+1:]

#alter names of 2.SE dictionaries so SEc and SEC aren't the same
for j in range(len(level2)):
	if len(level2[j])==3:
		if level2[j][2].islower():
			level2[j]=level2[j][0]+level2[j][1]+'_'+level2[j][2]

#enter each level1 folder and create all level2 folders
for i in level1:
	os.chdir(str(i))
	for j in level2:
		os.mkdir(j)
	os.chdir('..')

#remove suffixes from classification list
for j in range(len(classification)):
	while classification[j][-1]=='e' or classification[j][-1]=='p' or \
	classification[j][-1]=='u' or classification[j][-1]==':':
		if classification[j][-1]==':' and classification[j][-2]==':':
			classification[j]=classification[j][0:-2]
		elif classification[j][-1]=='e' or classification[j][-1]=='p' or \
		classification[j][-1]=='u' or classification[j][-1]==':':
			classification[j]=classification[j][0:-1]

#add underscore to 2.SEa,b,c
for j in range(len(classification)):
	if classification[j][-1].islower()==True:
		classification[j]=classification[j][0:-1]+'_'+classification[j][-1]

#add N|A to the classification if there isn't one
#to be able to place into a folder
for j in range(len(classification)):
	if len(classification[j])==1:
		classification[j]=classification[j]+'.'+'N|A'

#change '/' to '|' in the source classifications
for j in range(len(classification)):
	for k in range(len(classification[j])):
		if classification[j][k]=='/':
			classification[j]=classification[j][:k]+'|'+classification[j][k+1:]

#create folder for each source
for i in range(len(classification)):
        os.mkdir(classification[i][0]+'/'+classification[i][2:]+'/'+source[i]+' '+TDT[i])

print 'Folders Created'

#END RESULT::
#1 MASTER folder
#7 level 1 folders with the MASTER folder
#29 level2 folders within EACH level1 folder
#within the level2 folders are folders for each individual source of the 1239
#each of these source folders contains the name and TDT number
#many level2 folders won't have ANY source folders within
#####







#create list of objects with negative fluxes
neg_flux_number=[]
neg_flux_source=[]
neg_flux_TDT=[]

#Open browser to SWS Atlas
driver=webdriver.Firefox()
driver.get('http://irsa.ipac.caltech.edu/data/SWS/')

#wait for page to load
time.sleep(3)

#Create MASSIVE 'FOR' LOOP

for a in range(1239):
	#create wvlen, flux, error lists as a failsafe
	wvlen=[]
	flux=[]
	flux_error=[]
	norm_error=[]
	#if they remain empty at the end, then skip to the next source

	#Search for the object in SWS Atlas
	#click on 'Single Object' to input name
	object_input=driver.find_element_by_name('locstr')

	#clear the box
	object_input.clear()
	#input RA-DEC of object
	object_input.send_keys(RA[a])
	object_input.send_keys(', ')
	object_input.send_keys(DEC[a])

	#limit search size
	#radnumber=driver.find_element_by_name('radius')
	#radnumber.clear()
	#radnumber.send_keys('1')
	#select 'arcseconds'
	#radunits=driver.find_element_by_xpath("//select/option[3]").click()

	#click on 'Submit'
	object_input.send_keys(Keys.RETURN)
	#EXAMPLE: driver.find_element_by_xpath("//input[@name='username']")
		
	#switch to this window:
	driver.switch_to_window(str(driver.window_handles[1]))
	#driver.switch_to_window(str(handle))
		
	#wait for page to load
	time.sleep(3)

	#click to open the source table
	#try to click on the source table
	#if it can't, wait 20 seconds to load, then try again
	try:
		time.sleep(5)
		element=driver.find_element_by_xpath\
		("html/body/div[2]/form/center/center/table/tbody/tr[2]/td/a")
		element.click()
	except:
		time.sleep(10)
		element=driver.find_element_by_xpath\
		("html/body/div[2]/form/center/center/table/tbody/tr[2]/td/a")
		element.click()
		

	#wait for page to load
	time.sleep(1)

	#switch to this new window
	driver.switch_to_window(str(driver.window_handles[2]))

	#select the desired IPAC_FORMAT_ASCII_Data Set

	#find the desired row number based on name,TDT and 'filenum'
	match=False
	i=2
	while match==False:
		xpathfilenum='''//tr['''+str(i)+''']/td[3]'''
		objectfilenum=driver.find_element_by_xpath(xpathfilenum)
		if str(objectfilenum.text)!=TDT[a]:
			i+=1
		elif str(objectfilenum.text)==TDT[a]:
			match=True

	rownumber=i	

	#create xpath codes and define the desired link's row, name, filenum and hyperlink
	table=driver.find_element_by_xpath("//tbody")
	xpathrow='''//tbody/tr['''+str(rownumber)+''']'''
	objectrow=driver.find_element_by_xpath(xpathrow)
	xpathname='''//tbody/tr['''+str(rownumber)+''']/td[2]'''
	objectname=driver.find_element_by_xpath(xpathname)
	xpathnumber='''//tbody/tr['''+str(rownumber)+''']/td[3]'''
	objectnumber=driver.find_element_by_xpath(xpathnumber)
	xpathhyperlink='''//tbody/tr['''+str(rownumber)+''']/td[6]/a'''
	objecthyperlink=driver.find_element_by_xpath(xpathhyperlink)


	#click on the link
	objecthyperlink.click()

	#switch to new window with the data
	driver.switch_to_window(str(driver.window_handles[3]))

	#wait to load
	time.sleep(1)

	#make sure this is a data table
	if driver.title=='':
		pass

	#if driver.title!='':
	#	break

	######
	#import directly into python
	url=str(driver.current_url)
	downloaded_data=urllib2.urlopen(url)
	csv_data=csv.reader(downloaded_data)

	#create raw datatable
	datatable=[]
	for row in csv_data:
		datatable.append(''.join(row))

	#delete the 3 rows of headers
	del datatable[0]
	del datatable[0]
	del datatable[0]

	#split each row into individual values
	for i in range(len(datatable)):
		datatable[i]=datatable[i].split(' ')
		j=0
		while j<len(datatable[i]):
			if datatable[i][j]=='':
				del datatable[i][j]
			else:
				j=j+1

	wvlen=[]
	flux=[]
	flux_error=[]
	norm_error=[]

	#append to wavelength, flux, flux_error, and norm_error lists
	for i in range(len(datatable)):
		wvlen.append(datatable[i][0])
		flux.append(datatable[i][1])
		flux_error.append(datatable[i][2])
		norm_error.append(datatable[i][3])

	#if an error occurred and wvlen, flux, errors, haven't been filled,
	#continue to next source
	if wvlen==[]:
		continue

	#change strings into numeric values
	for i in range(len(wvlen)):
		wvlen[i]=float(wvlen[i])
		flux[i]=float(flux[i])
		flux_error[i]=float(flux_error[i])
		norm_error[i]=float(norm_error[i])

	#change lists into arrays
	wvlen=np.array(wvlen)
	flux=np.array(flux)
	flux_error=np.array(flux_error)
	norm_error=np.array(norm_error)

	#Create unsmoothed
	pylab.plot(wvlen,flux)
	pylab.xlabel('wavelength (microns)')
	pylab.ylabel('flux (Janksys)')
	pylab.title(source[a]+' '+TDT[a]+' '+classification[a]+' '+'Wavelength vs. Flux 2.36-45um undegraded')
	plt.savefig(\
	classification[a][0]+'/'+classification[a][2:]+'/'+source[a]+' '+TDT[a]+'/'\
	+source[a]+' '+TDT[a]+' 2-45 undegraded.pdf')
	plt.close()

	#Create 2-5 unsmoothed
	shortlist=np.where(wvlen<5)[0]
	pylab.plot(wvlen[shortlist],flux[shortlist])
	pylab.xlabel('wavelength (microns)')
	pylab.ylabel('flux (Janksys)')
	pylab.title(source[a]+' '+TDT[a]+' '+classification[a]+' '+'Wavelength vs. Flux 2.36-5um undegraded')
	plt.savefig(\
	classification[a][0]+'/'+classification[a][2:]+'/'+source[a]+' '+TDT[a]+'/'\
	+source[a]+' '+TDT[a]+' 2-5 undegraded.pdf')
	plt.close()

	#Create 2-5 smoothed

	#Degrade flux to resolution limit
	res=150.

	#Width of wavelength prior, OLD
	old_width=np.zeros(len(wvlen[shortlist]))
	for i in range(len(wvlen[shortlist])):
		if i==0:
			pass
		elif i==(len(wvlen[shortlist])-1):
			pass
		if i!=0 and i!=(len(wvlen[shortlist])-1):
			old_width[i]=((wvlen[shortlist][i]-wvlen[shortlist][i-1])/2)+\
			((wvlen[shortlist][i+1]-wvlen[shortlist][i])/2.)

	old_width[0]=old_width[1]
	old_width[-1]=old_width[-2]

	#Determine the width at each wavelength
	width=np.array([])
	for i in wvlen[shortlist]:
		width=np.append(width,i/res)

	#Sum fluxes
	sum_flux=np.array([])
	for i in wvlen[shortlist]:
		item=np.where(wvlen[shortlist]==i)[0][0]
		band_size=\
		np.where(\
		(wvlen[shortlist]>(i-(width[item])/2.))*(wvlen[shortlist]<(i+(width[item])/2.)))[0]
		fluxes=flux[shortlist][band_size]
		band_sum_fluxes=np.sum(fluxes)
		sum_flux=np.append(sum_flux,band_sum_fluxes)

	#find out how many datapoints are going into each wavelength width
	bin_number=np.array([])
	for i in range(len(shortlist)):
		length=len(np.where((wvlen>(wvlen[shortlist][i]-width[i]/2))*(wvlen<(wvlen[shortlist][i]+width[i]/2)))[0])
		bin_number=np.append(bin_number,length)

	new_flux=sum_flux/bin_number

	pylab.plot(wvlen[shortlist],new_flux)
	pylab.xlabel('wavelength (microns)')
	pylab.ylabel('Flux (Janskys)')
	pylab.title(source[a]+' '+TDT[a]+' '+classification[a]+' '+'Wavelength vs. Flux 2.36-5um degraded')
	plt.savefig(\
	classification[a][0]+'/'+classification[a][2:]+'/'+source[a]+' '+TDT[a]+'/'\
	+source[a]+' '+TDT[a]+' 2-5 degraded.pdf')
	plt.close()

	#create 2-5 both
	pylab.plot(wvlen[shortlist],new_flux,label='degraded')
	pylab.plot(wvlen[shortlist],flux[shortlist],label='undegraded')
	pylab.xlabel('wavelength (microns)')
	pylab.ylabel('Flux (Janskys)')
	pylab.title(source[a]+' '+TDT[a]+' '+classification[a]+' '+'Wavelength vs. Flux 2.36-5um')
	plt.legend(loc=4)
	plt.savefig(\
	classification[a][0]+'/'+classification[a][2:]+'/'+source[a]+' '+TDT[a]+'/'\
	+source[a]+' '+TDT[a]+' 2-5.pdf')
	plt.close()

	#swtich to and close data table window
	driver.switch_to_window(str(driver.window_handles[3]))
	driver.close()

	#switch to window #2 and close
	driver.switch_to_window(str(driver.window_handles[2]))
	driver.close()

	#switch to window #1 and close
	driver.switch_to_window(str(driver.window_handles[1]))
	driver.close()

	#switch back to SWS Atlas page
	driver.switch_to_window(str(driver.window_handles[0]))

	#print progress
	print a

	#append to negative flux list if >5% of fluxes are negative
	neg_instances=np.array([])
	for i in range(len(flux)):
		if flux[i]<0:
			neg_instances=np.append(neg_instances,i)

	if len(neg_instances)>=616:
		neg_flux_number.append(str(a))
		neg_flux_source.append(source[a])
		neg_flux_TDT.append(TDT[a])


#close original window and quit driver
driver.quit()

#call time upon finishing
end_time=time.time()

#total run time in seconds, minutes, and hours
run_time_s=end_time-start_time
run_time_m=run_time_s/60.
run_time_h=run_time_m/60.

#create composite time
run_time_h_comp=int(np.floor(run_time_h))
run_time_m_comp=int(np.floor(run_time_m-run_time_h_comp*60))
run_time_s_comp=int(np.floor(run_time_s-run_time_h_comp*60*60-run_time_m_comp*60))

run_time=str(run_time_h_comp)+':'+str(run_time_m_comp)+':'+str(run_time_s_comp)

print run_time
