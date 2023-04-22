from hashlib import sha256
from multiprocessing import Pool, Process
import hashlib
import queue
import time
import subprocess

def check_process_integrity(pid, hex_checksum):
    """
    Проверка целостности в виртуальной памяти для противодействия патчингу "на лету"
    """

    return True

def check_file_integrity(filename, hex_checksum):
    """
    Проверка целостности файла
    """
    f = open(filename, 'rb', buffering=0)
    result = (hashlib.file_digest(f, 'sha256').hexdigest() == hex_checksum)
    f.close()
    return True

class PP_Triplet:
    """
    Класс, представляющий тройку экземпляров ПП одной версии
    Осуществляет запуск и остановку процессов, проверку подписи
    """

    pp_exemplars = []

    def __init__(self, filenames):
        
        return

    def start_pool(self, filenames):
        # https://stackoverflow.com/questions/25120363/multiprocessing-execute-external-command-and-wait-before-proceeding
        
        # for fname in filenames:
        #     proc = subprocess.Popen(fname)
        #     self.pp_exemplars.append(proc)

        tempFilenames = ["python3 PP1.py", "python3 PP2.py", "python3 PP3.py"]
        for fname in tempFilenames:
            proc = subprocess.Popen(fname)
            self.pp_exemplars.append(proc)
        return

    def stop_pool_by_kafka(self):
        for proc in self.pp_exemplars:
            # TODO сигнал уведомления через кафку
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

    def exec(self):
        """Цикличная работа менеджера версий
        """
        while(True):
            # выгрузка команд из шины

            # выполнение регулярных действий по функционалу класса
            if(False):#TODO
                self.start_new_version(filenames)
            elif(False):
                pass
            else:
                pass

            # ожидание
            time.sleep(0.5)
        return
    
    def __del__(self):
        pass

    #TODO процесс подписывается, получает сигналы от кафки,
    # или он должен в цикле её опрашивать сам?


if __name__=="__main__":
    versionPool = VersionPool()
    filenames = []
    versionPool.start_new_version(filenames)
    versionPool.start_new_version(filenames)
    versionPool.start_new_version(filenames)
    versionPool.start_new_version(filenames)
    versionPool.exec()


