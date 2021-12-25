import os


def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('디렉토리 생성 실패 ' + directory)
