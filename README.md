### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeyVolkoff/switches.git
```

```
cd switches
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
На данный момент делает: Проверяет доступность пингом хостов в тестовой лабе GNS3 перед тестом, версию ПО и платформы на DUT, наличие настройки тоннеля(ip, статус), проверяет, что трассировка до хопа за тоннелем идет через тоннель.
