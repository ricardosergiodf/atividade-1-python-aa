"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.
"""
from botcity.web import WebBot, Browser, By
from botcity.maestro import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.headless = False

    bot.browser = Browser.CHROME

    bot.driver_path = r"C:\Users\ricar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    bot.browse("https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-Login.html?_gl=1*8sosof*_gcl_au*MTY2MDI2MTU3NS4xNzM0MzYxMzYzLjg3NDI4MjM4OS4xNzM0MzYxNzY4LjE3MzQzNjE3Njg.*_ga*MTcxMjEwMDAyNy4xNzI1MDM5NTgx*_ga_DG1BTLENXK*MTczNzk3Mjg3MS4zOS4xLjE3Mzc5NzMyNzcuNTUuMC4xNzAxMDAwNTM0&_fsi=MZ1nc3Vl")

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
