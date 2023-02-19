

def log(tag='', message=''):
    with open('logs/log.txt', 'w+') as log:
        log.write(f'{tag}: {message}\n')
