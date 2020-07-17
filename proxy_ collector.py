from selenium import webdriver
import csv,os,sys,time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def printf (text):
    print(text, end="")

def install():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') # This option this option slows down the execution speed, however it does not disturb you as the browser opens in every execution.
    return webdriver.Chrome(chrome_options=chrome_options, executable_path=resource_path('./driver/chromedriver.exe'))

ip = []
port = []
protocol = []
anonymity = []
country = []

print('*** Proxy Collector ***             by Gustavo Felici\n')
x = str(input('File name: '))

browser = install()

browser.get('http://www.freeproxylists.net')
i=2 #Start table position
printf('\nStarting...\n')

number_pages = 20 # check the website how many pages he has (normally he has 19~20)
for page in range(1,number_pages):
    printf('\nPage ('+str(page)+')...')
    while i < 60:
        try:
            ipc = browser.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr['+str(i)+']/td[1]')
            portc = browser.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr['+str(i)+']/td[2]')
            protoc = browser.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr['+str(i)+']/td[3]')
            anonyc = browser.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr['+str(i)+']/td[4]')
            countryc = browser.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr['+str(i)+']/td[5]')

            ip.append(ipc.text)
            port.append(portc.text)
            protocol.append(protoc.text)
            anonymity.append(anonyc.text)
            country.append(countryc.text)
        except:
            pass #this is an empty line
        i += 1
    printf('Done! Collected proxies: '+str(len(ip))+'\n')
    browser.get('http://www.freeproxylists.net/?page=' + str(page+1))
    time.sleep(2)
    i = 2 #Reset table position

browser.quit()
print('\nResult...\n','\nip =',ip,'\nport =',port)

printf('\nStoring results...')

with open(resource_path('./GeneratedFiles/'+x+'.csv'), 'w') as arq_csv:
    column = ['id','ip','port','protocol','anonymity','country']
    write = csv.DictWriter(arq_csv, fieldnames=column, delimiter=',', lineterminator='\n')
    write.writeheader()
    for i in range(0,len(ip)):
        write.writerow({'id': i,'ip': ip[i],'port': port[i],'protocol': protocol[i],'anonymity': anonymity[i],'country': country[i]})
printf('Complete!')
