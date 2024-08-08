from do_connect import do_connect
from run_blynk_server import ConnectToBlynk
from secrets import secrets

def main():
    print('Starting main...')
    ip = do_connect()
    blynk = ConnectToBlynk(secrets['BLYNK_AUTH'])
    blynk.run()

main()
