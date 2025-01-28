"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.
"""
from botcity.web import WebBot, Browser, By
from botcity.maestro import *
from functions import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    setup_logging()

    logging.info('Iniciando a Atividade 1 - Python & Automation Anywhere')

    if execution.task_id == 0:
        logging.info("Maestro desativado -> Executando localmente")
        maestro = None

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = bot_driver_setup()

    url = "https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-Login.html?_gl=1*8sosof*_gcl_au*MTY2MDI2MTU3NS4xNzM0MzYxMzYzLjg3NDI4MjM4OS4xNzM0MzYxNzY4LjE3MzQzNjE3Njg.*_ga*MTcxMjEwMDAyNy4xNzI1MDM5NTgx*_ga_DG1BTLENXK*MTczNzk3Mjg3MS4zOS4xLjE3Mzc5NzMyNzcuNTUuMC4xNzAxMDAwNTM0&_fsi=MZ1nc3Vl"
    bot.browse(url)
    
    try:
        email_field = bot.find_element("#inputEmail", By.CSS_SELECTOR)

        # Verifica se está logado no Automation Anywhere Community, se não estiver, é feito o login
        if not email_field:
            try:
                aa_login = bot.find_element("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/a[1]/button[1]", By.XPATH)
                if aa_login:
                    aa_login.click()
                    login_aa_community(bot)  # Alterar email e senha na função login_aa_community
                    bot.wait(1000)
            except Exception:
                pass
    except Exception as e:
        logging.error(e)
        if maestro:
            maestro.error(task_id=execution.task_id, exception=e)

    username = "user@automationanywhere.com"
    password = "Automation123"
    
    email_field = bot.find_element("#inputEmail", By.CSS_SELECTOR)
    password_field = bot.find_element("#inputPassword", By.CSS_SELECTOR)
    submit_btn = bot.find_element("button[type='button']", By.CSS_SELECTOR)
    login_try(username, password, email_field, password_field, submit_btn, bot, maestro, execution)

    logging.info('Fim.')
    bot.wait(3000)
    bot.stop_browser()

    if maestro:
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Task Finished OK.",
            total_items=0,
            processed_items=0,
            failed_items=0
        )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
