from re import search
from sys import exception
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import code
import bd #arquivo .py com os parametros do banco de dados

def busca(product_name):
    produto = product_name
    bd.pesquisa(produto)

    browser = webdriver.Firefox()

    # acessar ML
    def busca_ml(produto):
        Site = 'Mercado Livre'
        browser.get('https://www.mercadolivre.com.br/')
        assert 'Mercado Livre' in browser.title

        SearchCamp = browser.find_element(By.XPATH,"""//*[@id="cb1-edit"]""")
        SearchCamp.send_keys(produto)
        SearchCamp.send_keys(Keys.RETURN)
        time.sleep(5)

        #--- Criar um while antes desse para mudar de pagina
        pag = 0
        while True:
            if pag <=3:
                cont = 1
                
                while True:
                    try:
                        # Tente encontrar a variável (e.g., um elemento com um texto específico)
                        Nome = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]/div/div/div[2]/h2/a""").text
                        Link = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]/div/div/div[2]/h2/a""").get_attribute('href')
                        # Se o elemento for encontrado, incremente o contador
                        
                    except Exception as e:
                        # Se o elemento não for encontrado, interrompa o loop
                        try:
                            Nome = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]//a [@class="ui-search-link__title-card ui-search-link"]""").text
                            Link = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]//a [@class="ui-search-link__title-card ui-search-link"]""").get_attribute('href')
                        except Exception as e:
                            print(f"Variável não encontrada. Contador parou em {cont}.")
                            break
                        '''---------Copiar preço------------'''
                    centValor = 0
                    try:
                        Preco = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]/div/div/div[2]/div[2]/div/span[1]/span[2]""").text
                        centValor = 1
                        
                    except Exception as e:
                        try:
                            Preco = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]/div/div/div[2]/div[1]/div/span[1]/span[2]""").text
                            centValor = 2
                            
                        except Exception as e:
                            try:
                                Preco = browser.find_element(By.XPATH,f"""//div[3]/section/ol/li[{cont}]//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]/span[2]""").text
                                centValor = 3
                                
                            except Exception as e:
                                try:
                                    Preco = browser.find_element(By.XPATH,f"""//div[3]/section/ol/li[{cont}]//div[@class="poly-component__price"]/div/span[1]/span[2]""").text
                                    centValor = 4
                                    
                                except Exception as e:
                                    print("Erro no valor")
                                    break

                        #-------Case para saber o valor de centavos(se tiver)
                    def valor_cent(centValor):
                        match centValor:
                            case 1:
                                try:

                                    Centavos = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]/div/div/div[2]/div[2]/div/span[1]/span[4]""").text
                                    print(f'Valor centavos - {Centavos}')
                                    return Centavos
                                except Exception as e:
                                    Centavos = '0'
                                    return Centavos
                            case 2:
                                try:
                                    Centavos = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/ol/li[{cont}]/div/div/div[2]/div[1]/div/span[1]/span[4]""").text
                                    print(f'Valor centavos - {Centavos}')
                                    return Centavos
                                except Exception as e:
                                    Centavos = '0'
                                    return Centavos
                            case 3:
                                try:
                                    Centavos = browser.find_element(By.XPATH,f"""//div[3]/section/ol/li[{cont}]//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]/span[4]""").text
                                    print(f'Valor centavos - {Centavos}')
                                    return Centavos
                                except Exception as e:
                                    Centavos = '0'
                                    return Centavos
                            case 4:
                                try:
                                    Centavos = browser.find_element(By.XPATH,f"""//div[3]/section/ol/li[{cont}]//div[@class="poly-component__price"]/div/span[1]/span[4]""").text
                                    print(f'Valor centavos - {Centavos}')
                                    return Centavos
                                except Exception as e:
                                    Centavos = '0'
                                    return Centavos
                            case _:
                                return
                        return Centavos
                    Centavos = valor_cent(centValor)
                    Preco = Preco.replace('.','')
                    Preco = f"{Preco}.{Centavos}"
                
                    
                    bd.include_data(Site,produto,Nome,Preco,Link)
                    '''-----------------------------------------------------------------------'''
                    cont += 1
                print(f"---------- Pagina {pag} ---------")


                time.sleep(2)
                prox = browser.find_element(By.XPATH,f"""/html/body/main/div/div[3]/section/nav/ul/li[12]""")
                browser.execute_script("arguments[0].scrollIntoView();", prox)
                prox.click()
                pag +=1
            else:
                break
        print(f'''Busca pelo {Site} finalizado''')


    def busca_amazon(produto):
        Site = 'Amazon'
        browser.get('https://www.amazon.com.br/')
        assert 'Amazon' in browser.title

        try:
            SearchCamp = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"""//*[@id="twotabsearchtextbox"]""")))

        except Exception as e:
            SearchCamp = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"""//* [@class = "nav-bb-search-wrapper"]""")))

        SearchCamp.send_keys(produto)
        SearchCamp.send_keys(Keys.RETURN)
        time.sleep(5)

        #--- Criar um while antes desse para mudar de pagina
        pag = 0
        while True:
            if pag <=3:
                cont = 2
                time.sleep(10)
                
                while True:
                    try:
                        # Tente encontrar a variável (e.g., um elemento com um texto específico)
                        Nome = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,f"""/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{cont}]//h2/a"""))).text
                        Link = browser.find_element(By.XPATH,f"""/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{cont}]//h2/a""").get_attribute('href')
                        # Se o elemento for encontrado, incremente o contador
                        
                    except Exception as e:
                        if cont ==2:
                            cont +=1
                            Nome = browser.find_element(By.XPATH,f"""/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{cont}]//h2/a""").text
                            Link = browser.find_element(By.XPATH,f"""/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{cont}]//h2/a""").get_attribute('href')
                        
                        else:
                            print(f"Variável não encontrada. Contador parou em {cont}.")
                            break
                    '''---------Copiar preço------------'''

                    try:
                        Preco = browser.find_element(By.XPATH,f"""/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{cont}]//span [@class="a-price"]""").text
                        Preco = Preco.replace('R$','').replace('.','').replace('\n','.')

                        bd.include_data(Site,produto,Nome,Preco,Link)
                        
                    except Exception as e:

                        '''Caso o preço esteja indisponivel, o produto pode aparecer no site mas sem o valor.
                        Caso o preço não seja encontrado, o mesmo não será salvo no BD'''

                        print(f"-----------Produto numero {cont} - Erro no valor ou valor Indisponivel no site---------")


                    
                    cont += 1
                print(f"---------- Pagina {pag+1} ---------")


                time.sleep(2)
                prox = browser.find_element(By.XPATH,f"""//*[text() = 'Próximo']""")
                browser.execute_script("arguments[0].scrollIntoView();", prox)
                time.sleep(5)
                prox.click()
                pag +=1
            else:
                break
        print(f'''Busca pelo {Site} - Finalizado''')


    busca_amazon(produto)
    busca_ml(produto)

    print(f'''Finalizando o processo''')
    browser.close()