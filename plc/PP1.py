import time

if __name__=="__main__":
    while(True):
        # выгрузка команды из kafka
        command = {
            
        } #TODO
        if command["type"]=="protection": # команда защиты
            pass
        elif command["type"]=="sensor": # отправка показаний с датчиков
            pass
        elif command["type"]=="control": # выдача управляющего воздействия на устройство
            pass
        elif command["type"]=="stop": # остановка данного ПП
            pass
        else:
            time.sleep(0.1)