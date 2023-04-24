1. Создать корректные .env-файлы (шаблон .env.example) в корневой папке:
  1.1 .env:
заменить в .env.example следующие переменные:

KAFKA_SERVER=su-broker:9092
OPENSEARCH_HOST=opensearch
KAFKA_TOPIC=monitor
SOURCE_KEY_MAP={"machine1": "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJ8OHYXkZona3129rXCuKIywoLWn8frp\nx5qj/Gxm85xFLXAB5LvMWgPnN5jQrptEJ2w1Rt8UpPBIo0XCapQo6BUCAwEAAQ==\n-----END PUBLIC KEY-----", "machine2": "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKFw6CCujgYp65RreMP7nBfGrUDGTJ0m\ns2cgPZOxBpOAQ4BbbzCZEAwZbCKp3lPAWl7XXBM6MJ/OGipcmNzCcEUCAwEAAQ==\n-----END PUBLIC KEY-----", "rest": "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMT/+1cpyOqarfJwSrYkrIZOiHVxfDVQ\noQIA0dx9cRt8AR1PM8iZTC2PnNvVOW8Oq3yrS68rbO0xpwP/9N0ZSVMCAwEAAQ==\n-----END PUBLIC KEY-----"}
BROKER_USER="test"
BROKER_PASS="test"
BROKER_SERVER="broker"
POLICIES=[["rest", "machine2"], ["machine2", "rest"], ["rest", "machine1"], ["machine1", "rest"]]


  1.2 .env.machine1:
заменить в .env.example следующие переменные:

KAFKA_SERVER=su-broker:9092
KAFKA_TOPIC=machine1
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nMIIBOwIBAAJBAJ8OHYXkZona3129rXCuKIywoLWn8frpx5qj/Gxm85xFLXAB5LvM\nWgPnN5jQrptEJ2w1Rt8UpPBIo0XCapQo6BUCAwEAAQJAZTQyDNO7etPNdHQQO7ZV\nDtAEMhHeomzGGNtm7gLD1xYcT0tbMKpqdsECGQ2xySNr2MXMo5l3HdVd5UccR+d8\ngQIhANFt6IkTWP8XF+RoVK0Bj6K2U9/zxBm0DB44dxEsipH5AiEAwmyT1HNZk4t4\nwjIuGJeij8jBE8NGXGLWBe6XvAd1Df0CIQC7JK6thvd5A2bbOQupiYKT0L/EmOy8\nVzKY8rYbR6UP6QIgMfnS7hNQfTqmqdRYQP4JTUhfSQMy/OBy/0dbPXv1PMkCIQDP\n7XLbvxXbzCZnIIHH4YY3aca0dCquY9XlIKRZEKgqYw==\n-----END RSA PRIVATE KEY-----"

  1.3 .env.machine2:
заменить в .env.example следующие переменные:

KAFKA_SERVER=su-broker:9092
KAFKA_TOPIC=machine2
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nMIIBPAIBAAJBAKFw6CCujgYp65RreMP7nBfGrUDGTJ0ms2cgPZOxBpOAQ4BbbzCZ\nEAwZbCKp3lPAWl7XXBM6MJ/OGipcmNzCcEUCAwEAAQJAMM+5b4A3csej8ckYx3DA\nvjOU2JvcODumTIzj8U655UiMi/onUN/qV60JboqpiSBGXYhsa7y6uBWxmX9YBN0d\n1QIhANVsV/KodNl7bc0VW6AJRMNcXKopkukBM9ONZeZxpF+fAiEAwaXNGr5jMWPB\n3gbvYyctHEbgu9vQkIolToR0wkFLlZsCIQDEysg1uls0hnlyl3ULFkDPmwTe6sLK\nEw/EzCbf3H3ipQIhAIvkKvdW8nGLj1HF0MngU0ZKLa+IbHL+WVUPewmaAfBhAiEA\nrozRcJEUHl+Bxe8WgvsSiPBVYNUKb//DR0yPR7FsPFw=\n-----END RSA PRIVATE KEY-----"


2. Поднять все контейнеры, запустив docker-compose-kafka.yml
3. Тестирование:

Тестирование взаимодействия с монитором:

Установить poetry (https://python-poetry.org/docs/)
перейти в sample_processes
создать виртуальное окружение python -m venv .venv
активировать его . .venv/bin/activate
установить зависимости poetry install --no-root
в файл .env в директории  sample_processes записать 
KAFKA_SERVER=localhost:9092
KAFKA_TOPIC=rest
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nMIIBOwIBAAJBAMT/+1cpyOqarfJwSrYkrIZOiHVxfDVQoQIA0dx9cRt8AR1PM8iZ\nTC2PnNvVOW8Oq3yrS68rbO0xpwP/9N0ZSVMCAwEAAQJBAL9xJAeoi5+xgalAhtpK\n+X3rg6DeEB6fpFgWA9uJ7AkP26nj7/LCD8e6IHchNMlYwUfkQunSrBXH0bZk1DX0\nh0ECIQDuLy0vVW9wom1eX9M/KRF1iZ1Zk41yniQ8ghrv0s4LPwIhANO8Me12iCnG\nEcdvXQej7cwN+sTe+ql3AfAoePZlzyDtAiApgvNfEobPnJ9vGUhZ87BlScywtfSr\nC0DJgutq7NSYRQIhAIYxgHM/7IyNPDdqHUv6WXw6X/TmXXeKNXBANmnznJMBAiB0\nRLQ2EgGhyWavLLXMATc6+GCO9pMTbR6kOhOVolA6bQ==\n-----END RSA PRIVATE KEY-----"
запустить ipython в двух терминалах
в первом терминале делаем импорт
from message_helpers import MessageSender
во втором
from message_helpers import MessageGetter
MessageGetter().consume()

все остальные действия выполняются в первом терминале. Например, отправить сообщение 
MessageSender().send_message("machine1", "request_sensor", {"sensor_id": 2})