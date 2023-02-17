import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import date
import time
import csv
from collections import OrderedDict
import re

urls = {'IBOV':"https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br",
     'IBXX': "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBXX?language=pt-br",
     'IBXL': "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBXL?language=pt-br",
     'IBRA': "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBRA?language=pt-br"}

today = date.today().strftime("%d-%m-%y")

SAVE_PATH = f"{os.getcwd()}/download"
X_PATH_DOWNLOAD = "//*[@id='divContainerIframeB3']/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a"

def all_equitys() -> list:
     #arquivos de hoje
     today_files = []
     for url in urls.keys():
          string = url + "Dia_"+ today + ".csv"
          today_files.append(string)


     arquivos = []
     #todos arquivos da pasta
     for diretorio, subpastas, arquivo in os.walk(SAVE_PATH):           
          if arquivo != None:          
               val = str(arquivo).replace("'", "")
               val = val.replace(" ","")                         
               arquivos.append(val)          


     if len(arquivos) > 0:
          arquivos = str(arquivos).split(",")     
          arquivos[0] = arquivos[0].replace("'", "")
          arquivos[0] = arquivos[0].replace("[", "")
          arquivos[len(arquivos)-1] = arquivos[len(arquivos)-1].replace("'", "")
          arquivos[len(arquivos)-1] = arquivos[len(arquivos)-1].replace("]", "")
                         
          #remover arquivos duplicados
          for arquivo in arquivos:
               duplicate_extract = "\\([0-9]{1,2}\\)"
               if re.findall(duplicate_extract, arquivo).__len__() > 0:
                    os.remove(diretorio+"/"+arquivo)     
          urls_to_download = []
     
          for index,arquivo in enumerate(arquivos): 
               arquivo = arquivo.replace("'", "")          
               if None != arquivo and today not in arquivo[0:16]:
                    os.remove(diretorio+"/"+arquivo)     
                    if (str(arquivo[:8])+today+".csv") not in arquivos:
                         urls_to_download.append(urls[str(arquivo)[0:4]])              
                         
          for tf in today_files:     
               tf = tf.replace("'", "")   
               if str(tf) not in arquivos:               
                    urls_to_download.append(urls[str(tf)[0:4]])      
                    
          urls_to_download = list(set(urls_to_download))
     else:
          print("atualizando todos os arquivos..")
          urls_to_download = urls.values()

     if urls_to_download:
          proxy = Proxy(dict(proxyType=ProxyType.AUTODETECT))
          # To prevent download dialog
          profile = webdriver.FirefoxProfile()
          profile.set_preference('browser.download.folderList', 2) # custom location
          profile.set_preference('browser.download.manager.showWhenStarting', True)
          profile.set_preference('browser.download.dir', SAVE_PATH)
          profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
          
          options = Options()
          options.headless = True
    
          browser = webdriver.Firefox(firefox_profile=profile, options=options, proxy=proxy)     

          for url in urls_to_download:
               browser.get(url)
               time.sleep(3)
               browser.find_element(By.XPATH, X_PATH_DOWNLOAD).click()
          browser.close()
         
     all_equitys = []
     for file in arquivos:
          path = SAVE_PATH+"/"+file     
          try:
               with open(path, newline='', encoding="latin-1") as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                    patter_equity = "[A-Z]{4}[0-9]{1}"               
                    patter_equity2 = "[A-Z]{4}[0-9]{2}"                              
                    for row in spamreader:                    
                         values = str(row).split(";")[0]                   
                         equity = (re.findall(patter_equity2, values))                    
                         if len(equity) == 0:
                              equity = (re.findall(patter_equity, values))
                         
                         if len(equity)==1:
                              all_equitys.append(str(equity))                                                       
          except FileNotFoundError:
               pass
                    
     all_equitys = list(OrderedDict.fromkeys(all_equitys))
     final_list = []
     for ativo in all_equitys:          
          if len(ativo) == 9:
               final_list.append(ativo[2:7])
          if len(ativo) == 10:
               final_list.append(ativo[2:8])          
     return final_list
