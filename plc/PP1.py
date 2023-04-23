import time
import json

"""
Имитатор прикладного ПО (ПП) ПЛК 
получает запросы на 
- остановку (kafka)
- 
"""

class Settings:
    max_power_mwt = 1000
    max_speed_rpm = 10000
    max_temperature_deg = 500
    min_temperature_deg = -50
    min_power_mwt = 0
    min_speed_rpm = -1

    def __init__(self):
        self.update_settings()

    def update_settings(self):
        f = open("./storage/settings_plc.json", "r")
        data = json.load(f)
        f.close()
        max_power = data['max_power']
        max_speed = data['max_speed']
        max_temperature = data['max_temperature']
        min_power = data['min_power']
        min_speed = data['min_speed']
        min_temperature = data['min_temperature']
        return


class PP:
    settins = Settings()

    def send_command():
        """
        Отправка команды исполнительному устройству
        через модуль мажоритарной логики
        """

        return

    def read_sensor():
        """
        Выгрузка показаний датчиков из очереди сообщений
        от компонента "Интерфейс датчиков"
        """

        return

    def exec(self):
        while(True):
            # TODO выгрузка команды из kafka

            # { команда вида 
            #     "source": "text",
            #     "signature": "base64encoded",
            #     "body": {
            #         "destination": "text",
            #         "timestamp": "ISO datetime",
            #         "message_type": "text",
            #         "message_id": "integer"
            #     // остальные поля сообщения (полезная нагрузка)
            #     }
            # }

            command = {
                
            }
            message_type = command["body"]["message_type"]

            if(message_type=="protection") or (message_type=="device"):
                # ОТПРАВКА КОМАНД НА ИСП. УСТРОЙСТВО

                # обработка данных и сборка нового сообщения
                # отправка в мажоритарную логику
                command2 = command
                self.send_command(command2)

            elif message_type=="sensor":
                # ПОЛУЧЕНИЕ ПОКАЗАНИЙ С ДАТЧИКА И ОБРАБОТКА

                # чтение готовой очереди показаний датчиков
                self.read_sensor()

            elif command["type"]=="control": # выдача управляющего воздействия на устройство
                send_command()

            elif command["type"]=="stop": # остановка данного ПП
                break

            else:
                time.sleep(0.05)

    
    def apply_settings(self):
        self.settins.update_settings()
        pass

    def apply_license(self):
        pass

# if __name__ == "__main__":
#     app.run(port=port, host=host_name)

# if __name__=="__main__":
#     pp = PP()
#     pp.exec()

