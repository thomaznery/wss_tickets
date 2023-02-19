import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import date,datetime
import time
import csv
from collections import OrderedDict
import re
import logging




urls = {'IBOV':"https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br",
     'IBXX': "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBXX?language=pt-br",
     'IBXL': "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBXL?language=pt-br",
     'IBRA': "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBRA?language=pt-br"}

today = date.today()
today_str= today.strftime("%d-%m-%y")
SAVE_PATH = f"{os.getcwd()}/download"
X_PATH_DOWNLOAD = "//*[@id='divContainerIframeB3']/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a"

def get_download_files():
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
    return arquivos,diretorio

def all_equitys() -> list:  
     logging.info("servico solicitado..")   
     today_files = []
     for url in urls.keys():          
          string = url + "Dia_"+ today_str + ".csv"
          today_files.append(string)
     #lista atual de arquivos
     arquivos, diretorio = get_download_files()          
     if len(arquivos) > 0:                                
          urls_to_download = []
          for arquivo in arquivos:
               arquivo = arquivo.replace("'", "")
               if arquivo:
                    if re.findall("\\([0-9]{1,2}\\)", arquivo).__len__() > 0:
                         os.remove(diretorio+"/"+arquivo)
                         continue
                    date_pattern = "-".join([arquivo[8:10],arquivo[11:13],arquivo[14:16]])
                    date_file = datetime.strptime(date_pattern, '%d-%m-%y').date()
                    if today == date_file: continue
                    if date_file<today:                           
                         os.remove(diretorio+"/"+arquivo)                           
                         urls_to_download.append(urls[str(arquivo[0:4])])                                                                       
          
          arquivos, diretorio = get_download_files() 
          indice_file = []
          
          for arquivo in arquivos: indice_file.append(str(arquivo[0:4]))          
          for key in urls.keys():               
               if key not in indice_file:
                    urls_to_download.append(urls[key])          
                                                                      
          urls_to_download = list(set(urls_to_download))
     else:
          logging.info("atualizando todos arquivos")
          urls_to_download = urls.values()

     if urls_to_download:
          logging.info(f"atualizando {len(urls_to_download)} arquivos..")
          proxy = Proxy(dict(proxyType=ProxyType.AUTODETECT))
          
          options = Options()
          options.headless = True
          options.set_preference("browser.download.folderList",2)
          options.set_preference('browser.startup.homepage_override.mstone', '')
          options.set_preference('startup.homepage_welcome_url', 'about:')
          options.set_preference("browser.download.dir", SAVE_PATH)
          browser = webdriver.Firefox(options=options, proxy=proxy)     

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
