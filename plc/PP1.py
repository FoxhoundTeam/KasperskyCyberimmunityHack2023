import time

if __name__=="__main__":
    while(True):
        # выгрузка команды из kafka
        command = {
            
        } #TODO

        # 

        if command["type"]=="protection": # команда защиты
            send_command()
        elif command["type"]=="sensor": # отправка показаний с датчиков
            read_pin()
        elif command["type"]=="control": # выдача управляющего воздействия на устройство
            send_command()
        elif command["type"]=="stop": # остановка данного ПП
            break
        else:
            time.sleep(0.05)

