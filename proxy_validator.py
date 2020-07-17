from selenium import webdriver
import time,os,sys
import pandas as pd
import csv
from statistics import mean
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def printf (text):
    print(text, end="")

def multiples(x):
    n=0
    print('\n* Possible Multiples *')
    for i in range(1, 150):
        if x % i == 0:
            print('\nNumber of threads:', i, 'Each thread will execute', x / i)
            n+=1
    if n==1:
        print('There are no perfect multiples choose an imperfect (Some threads will have more executions)')
        for i in range(1, 150):
            if x % i == 1:
                print('\nNumber of threads:', i, 'Each thread will execute', x / i)

def change_proxy(i):
    PROXY = str(df['ip'][i]) + ':' + str(df['port'][i])  # IP:PORT or HOST:PORT
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    return webdriver.Chrome(chrome_options=chrome_options, executable_path=resource_path('./driver/chromedriver.exe'))



print('*** Proxy Validator ***             by Gustavo Felici\n')
x = str(input('\nFile name: '))
arq = pd.read_csv(resource_path('./GeneratedFiles/'+x+'.csv'),encoding='cp1252')
df = pd.DataFrame(arq)
global attempts

ip = []
port = []
protocol = []
anonymity = []
country = []

runtimes = []
runtimef = []

def Test(id,start,end): # Threads function

    ini = time.time()
    not_detected = 0
    retry = 0

    xip = []
    xport = []
    xprotocol = []
    xanonymity = []
    xcountry = []

    i = start - 1
    while i < end:

        i += 1
        try:
            l = time.time()
            print('\n['+str(id)+'] '+'Testing... ('+str(i)+'/'+str(end)+')')
            complet_ip = str(df['ip'][i]) + ':' + str(df['port'][i])

            browser = change_proxy(i)

            browser.get('https://whatismyipaddress.com/')

            time.sleep(5)
            ipv4 = browser.find_element_by_id('ipv4')

            s = str(ipv4.text)

            if s == str(df['ip'][i]):
                print('\n['+str(id)+'] '+'*** Sucess ***')
                #print('My IP Address Is \nIPv6 = ', ipv6.text, 'IPv4 = ', ipv4.text)
                ip.append(df['ip'][i])
                port.append(df['port'][i])
                protocol.append(df['protocol'][i])
                anonymity.append(df['anonymity'][i])
                country.append(df['country'][i])
                runtimes.append(time.time() - l)

            elif s == 'Not detected':
                print('\n['+str(id)+'] '+'*** Not detected ***')
                #print('\nMy IP Address Is \nIPv6 = ', ipv6.text, 'IPv4 = ', ipv4.text)
                not_detected+=1

            else:
                print('\n['+str(id)+'] '+'*** FAIL ***')
                runtimef.append(time.time() - l)

        except:
            i -= 1
            if retry == attempts:
                i += 1
                retry = 0
                print('\n[' + str(id) + '] Failed Registered (i = ', str(i+1) + ')')
            else:
                retry += 1
                print('\n[' + str(id) + '] Failed Registered (i = ', str(i+1) + ')','Retrying...' + ' (' + str(retry) + '/' + str(attempts) + ')')

            runtimef.append(time.time() - l)

        print('\nRuntime:', str(round(time.time() - ini, 2)) + 's')
        browser.quit()

    print('\nEnd of Thread' + ' [' + str(id) + ']')
    ip.extend(xip)
    port.extend(xport)
    protocol.extend(xprotocol)
    anonymity.extend(xanonymity)
    country.extend(xcountry)


def startThreading(n):
    threads = []
    ant = 0
    v = df['id'].count()/n

    for i in range(1,n+1): #Create and start threading
        c = i*v
        #print('i:',i,'ant:',ant,'c:',c-1,'v:',v) #To test a split of threads
        t = threading.Thread(target=Test, args=(i, int(ant), int(c-1)))
        t.start()
        threads.append(t)
        ant = c
    for t in threads: #Wait until the end of all threads
        t.join()

printf('\n*** Warnings ***\nNot closing the program can cause many errors.\nMany threads can result in a lower success rate')
time.sleep(3)

print('\nStarting...')
p = time.time()
multiples(len(df['id']))
n = int(input('\nChoose multiple active threads simultaneously (warning: your machine may crash): '))
attempts = int(input('Choose how many attempts to check: '))
startThreading(n)

print('\nResults...\nip =',ip,'\nport =',port,'\n\nSucess:',len(runtimes),'\nFailed:',len(runtimef))

printf('\nStoring results...')

with open(resource_path('./GeneratedFiles/'+x+'_correct'+'.csv'), 'w') as arq_csv:
    column = ['id','ip','port','protocol','anonymity','country']
    write = csv.DictWriter(arq_csv, fieldnames=column, delimiter=',', lineterminator='\n')
    write.writeheader()
    for i in range(0,len(ip)):
        write.writerow({'id': i,'ip': ip[i],'port': port[i],'protocol': protocol[i],'anonymity': anonymity[i],'country': country[i]})
printf('Complete!\n')

uni = runtimes+runtimef
total = df['id'].count()

print('\n*** Statistical Results ***')
print('\nSucess =',len(runtimes))
print('Tax of Sucess =',str(round((len(runtimes)/total)*100,2))+'%')
print("Medium Time per execution =",round(mean(uni),2))
print("[Sucess] Medium Time per execution =",round(mean(runtimes),2))
if len(runtimef) != 0:
    print("[Fail] Medium Time per execution =",round(mean(runtimef),2))
else:
    print("No have Fail's")
print('\nTotal Testing Runtime:', str(round(time.time() - p, 2)) + 's','or',str(round((time.time() - p)/60, 2)) + ' minutes')


