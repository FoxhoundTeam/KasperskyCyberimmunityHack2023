from hashlib import sha256
# from multiprocessing import Pool, Process
import hashlib
import queue
import time
import subprocess


import requests
from flask import Flask, request, jsonify

port = "6090"
host_name = "0.0.0.0"
app = Flask(__name__)  # create an app instance

class PP_Triplet:
    """
    Класс, представляющий тройку экземпляров ПП одной версии
    Осуществляет запуск и остановку процессов, проверку подписи
    """

    pp_exemplars = []

    def __init__(self, filenames):
        
        return

    def check_process_integrity(self, pid, hex_checksum):
        """
        Проверка целостности в виртуальной памяти
        для противодействия патчингу "на лету",
        запускается регулярно
        """

        #TODO встроить прототип из check_process_integrity.py
        return True
    
    def check_file_integrity(self, filename, hex_checksum):
        """
        Проверка целостности файла ПП перед запуском
        """
        file_hash = hashlib.sha256()
        BLOCK_SIZE = 65536
        f = open(f"./storage/{filename}", 'rb')
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE)
        f.close()
        result = (file_hash.hexdigest() == hex_checksum)
        return True

    def start_pool(self, filenames):
        # https://stackoverflow.com/questions/25120363/multiprocessing-execute-external-command-and-wait-before-proceeding
        
        # for fname in filenames:
        #     proc = subprocess.Popen(fname)
        #     self.pp_exemplars.append(proc)

        tempFilenames = ["PP1.py", "PP2.py", "PP3.py"]
        for fname in tempFilenames:
            hex_checksum = ""
            if(self.check_file_integrity(fname, hex_checksum)):
                proc = subprocess.Popen(f"python3 {fname}")
                self.pp_exemplars.append(proc)
            else:
                #TODO сообщение об ошибке
                pass
            #TODO сообщение о корректном запуске
        return

    def stop_pool_by_kafka(self):
        for proc in self.pp_exemplars:
            # TODO сигнал уведомления для pp1, pp2 и pp3 через кафку
            pass
        return

    def stop_pool_by_sigterm(self):
        for proc in self.pp_exemplars:
            try:
                proc.terminate(self)
            except Exception as e:
                print(e)
        return

    def stop_pool_by_sigkill(self):
        for proc in self.pp_exemplars:
            try:
                proc.kill()
            except Exception as e:
                print(e)
        return

    def __del__(self):
        print("!!! Triplet removed")
        return


class VersionPool:
    """
    Класс, осуществляющий управление очередью
    из триплетов (PP_Triplet) ПП разных версий
    """

    queue_of_versions = queue.Queue() # очередь тройных пулов версий ПП

    def __init__(self):
        
        return

    def start_new_version(self, filenames):
        triplet = PP_Triplet(filenames)
        triplet.start_pool(filenames)
        self.queue_of_versions.put(triplet)

        if(self.queue_of_versions.qsize()>2):
            self.queue_of_versions.get()
        return
    
    def __del__(self):
        pass

    #TODO процесс подписывается, получает сигналы от кафки,
    # или он должен в цикле её опрашивать сам?

versionPool = VersionPool()

@app.route("/upload_update", methods=['POST'])
def upload_update():
    """Обновление ПП
    """
    content = request.json
    # содержимое типа
    # { "update_files" : [update_file1, update_file2, update_file3 ] }
    try:
        
        for itm_name in request.json["update_files"]:
            # запрос новых версий ПП
            response = requests.post(
                f"http://update_server:6067/upload_update/{itm_name}",
                headers=CONTENT_HEADER,
            )

            # TODO response = json.loads(response.content.decode('utf8'))
            if response['status'] is True:
                f = open(f"/storage/{itm_name}", "w")
                f.write(test_response.text)
                # TODOjson.dump(content, f)
                f.close()

                response_data = {"status": 'ok'}
                return jsonify(response_data)
            else:
                response_data = {"status": 'error',
                                 "details": "Не удалось получить обновления"}
                return jsonify(response_data)
        versionPool.start_new_version(request.json["update_files"])
        # TODO ответ
    except Exception as e:
        error_message = f"malformed request {request.data}"
        return error_message, 400
    return jsonify({"status": 'error', "details": "Неизвестная ошибка"})


@app.route("/upload_settings", methods=['POST'])
def upload_settings():
    """
    Обновление настроек
    """
    content = request.json
    # содержимое типа
    # {
    #     "max_power_rpm" :
    #     "max_speed_rpm" :
    #     "max_temperature_deg" :
    #     "min_power_mwt":
    #     "min_speed_rpm":
    #     "min_temperature_deg":
    # }

    try:
        f = open("./storage/settings_plc.json", "w")
        # TODO проверка целостности и авторизации

        json.dump(content, f)
        f.close()

        # TODO синхронный запрос через кафку на обновление настроек

        response_data = {"status": 'ok', }
        return jsonify(response_data)
    except Exception as _:
        error_message = f"malformed request {request.data}"
        return error_message, 400
    return jsonify({"operation": "stopped"})


if __name__=="__main__":
    filenames = []
    versionPool.start_new_version(filenames) # запуск первой версии типлета ПП
    versionPool.start_new_version(filenames) # запуск второй версии типлета ПП
    # тест смены версий versionPool.start_new_version(filenames)
    # тест смены версий versionPool.start_new_version(filenames)
    app.run(port=port, host=host_name)


