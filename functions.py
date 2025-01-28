import logging
import datetime
from botcity.web import WebBot, Browser, By
from botcity.web.browsers.chrome import default_options
from botcity.maestro import *
import os

def setup_logging():
    log_path = "C:/Users/ricar/Desktop/-/Compass/atividades-praticas-compass/Sprint-4/ativ-pratica-1-python-aa/resources/logfiles"
    # Verifica se a pasta "logfiles" existe, se não, cria-a
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo_log = f"{log_path}/logfile-{data_atual}.txt"

    logging.basicConfig(
        filename=nome_arquivo_log,
        level=logging.INFO,
        format="(%(asctime)s) - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )


def bot_driver_setup():
    bot = WebBot()
    def_options = default_options(
        headless = bot.headless,
        user_data_dir = r"C:\Users\ricar\AppData\Local\Google\Chrome\User Data"
    )

    bot.options = def_options
    bot.browser = Browser.CHROME
    bot.driver_path = r"C:\Users\ricar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    return bot


def login_aa_community(bot):
    aa_username = "email"  # COLOCAR EMAIL AQUI
    aa_password = "senha"  # COLOCAR SENHA AQUI
    logging.info('Inicio - login_aa_community function')
    logging.info("Login necessario no Automation Anywhere Community")

    email_field = bot.find_element("input[id='43:2;a']", By.CSS_SELECTOR)
    submit_btn = bot.find_element("button[type='button']", By.CSS_SELECTOR)
    email_field.send_keys(aa_username)             
    submit_btn.click()
    bot.wait(500)
    password_field = bot.find_element("input[id='10:159;a']", By.CSS_SELECTOR)
    password_field.send_keys(aa_password)
    bot.enter()
    return
    

def login_try(username, password, email_field, password_field, submit_btn, bot, maestro, execution):
    for counter in range(1, 4):
        email_field.clear()
        password_field.clear()
        result = login(username, password, email_field, password_field, submit_btn, bot, maestro, execution, counter)

        logging.info(f"Resultado da tentativa {counter}: {'Login feito com sucesso' if result else 'Login falhou'}")
        if maestro:
            maestro.alert(
                task_id=execution.task_id,
                title=f"Attempt {counter}",
                message=f"Started attempt {counter}.",
                alert_type=AlertType.INFO
            )
        if result:
            if maestro:
                maestro.post_artifact(
                    task_id=execution.task_id,
                    artifact_name=f"Successful Login.",
                    filepath="resultados.png"
                )
                maestro.finish_task(
                    task_id=execution.task_id,
                    status=AutomationTaskFinishStatus.SUCCESS,
                    message="Task Finished OK."
                )
            ok_btn = bot.find_element("#btn-modal", By.CSS_SELECTOR)
            ok_btn.click()
            break
        else:
            error = bot.find_element("#success-title", By.CSS_SELECTOR).text
            # Verifica se a mensagem é a mensagem de erro de login
            if error == "Check your code again. Either your username or password is incorrect. Note: Both are case sensitive":
                logging.info("Elemento de erro do login capturado.")
                ok_btn = bot.find_element("#btn-modal", By.CSS_SELECTOR)
                ok_btn.click()
                if maestro:
                    maestro.alert(
                        task_id=execution.task_id,
                        title=f"Invalid Login",
                        message=f"{error.text}",
                        alert_type=AlertType.WARN
                    )
        if counter == 3:
            logging.warning("Todas as tentativas de login falharam.")
            if maestro:
                maestro.finish_task(
                    task_id=execution.task_id,
                    status=AutomationTaskFinishStatus.SUCCESS,
                    message="All login attempts failed."
                )
            bot.stop_browser()


def login(username, password, email_field, password_field, submit_btn, bot, maestro, execution, counter):
    logging.info('Inicio - login function')
    logging.info(f"{counter}a tentativa de login.")
    try:
        while (email_field.text != username) and (password_field.get_attribute("value") != password):
            email_field.clear()
            password_field.clear()
            email_field.send_keys(username)
            password_field.send_keys(password)
            
        submit_btn.click()
        bot.wait(500)

        successful_login = bot.find_element("#success-title", By.CSS_SELECTOR).text
        time_success = bot.find_element("#processing-time", By.CSS_SELECTOR).text
        accuracy_success = bot.find_element("#accuracy", By.CSS_SELECTOR).text
        if successful_login == "Awesome, you got it right!":
            bot.save_screenshot("resultados.png")
            logging.info(f"Login feito com sucesso. Tempo de execucao: {time_success}, Precisao: {accuracy_success}.")
            print(f"Login feito com sucesso. Tempo de execucao: {time_success}, Precisão: {accuracy_success}.")
            return True
        else:
            counter += 1
            logging.error(f"Erro ao tentar realizar o login. Username: {username}, Password: {password}")
            return False
        
    except Exception as e:
        logging.error(f"Erro fatal na execucao do login: {e}")
        if maestro:
            maestro.error(task_id=execution.task_id, exception=e)
        return False

