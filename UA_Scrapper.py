import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----- Configuration de Selenium pour utiliser Chrome -----
# Chemin vers le profil Chrome
chrome_profile_path = '/Users/charles-albert/Library/Application Support/Google/Chrome/Default'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
driver = webdriver.Chrome(options=options,executable_path='/Users/charles-albert/Desktop/chromedriver_mac_arm64/chromedriver') #Chemin vers l'exécutable chromedriver
# -----------------------------------------------------------

def scrappe(list,navigator_name,N_useragents):
    list = []
    
    # Attendre que l'iframe devienne invisible
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.ID, 'aswift_3')))
    
     # Cliquer sur l'élément correspondant au 'navigator_name'
    element = str(f'a[href="/pages/{navigator_name}/ "]')
    navigator_link = driver.find_element(By.CSS_SELECTOR, element)
    navigator_link.click()
    # scrapper les N_useragents vers la liste 'list'
    for i in range(1, N_useragents+1):
        xpath = '//*[@id="liste"]/ul[{}]/li/a'.format(i)
        elements = driver.find_element_by_xpath(xpath).text
        list.append(elements)
    # retourner à la page précédente
    driver.back()
    return list

def save_yml(datas,Navigators_names):
    data = {}
    for i in range(0,len(datas)):
        data[Navigators_names[i]] = datas[i]
    # Enregistrer les User_agents dans un fichier YAML
    with open('User_Agents.yml', 'w') as file:
        yaml.dump(data, file)

# Accès à la page contenant les user_agents avec Selenium
reponse = driver.get("https://www.useragentstring.com/pages/useragentstring.php")

#**************************************************************************************
Navigators_names = ['Firefox','Chrome','Safari'] # Spécifier les noms des navigateurs à explorer
N_DATAS = 20 # Nombre de User_agents à récupérer
# Créer les listes vides correspondantes
Firefox_list = []
Chrome_list = []
Safari_list = []

datas = [Firefox_list,Chrome_list,Safari_list]
#**************************************************************************************

# scrapper les données des navigateurs spécifiés 
for i in range(len(datas)):
    datas[i] = scrappe(datas[i],Navigators_names[i],N_DATAS)

# Sauvegarder les données sous format yml
save_yml(datas,Navigators_names)

# Fermer le navigateur
driver.quit()

# Afficher un message de confirmation
print("\nFichier User_Agents.yml enregistré.")
