import os
import pickle
import shutil

'''
user_names list에 있는 유저 이름과 디렉토리 삭제
'''

delete_name = input("Delete user name: ")

if os.path.isdir(f'./{delete_name}'):
    with open('./user_names.pickle', 'rb') as f:
        user_names = pickle.load(f)
    
    user_names.remove(delete_name)
    shutil.rmtree(f'./{delete_name}')

    with open('./user_names.pickle', 'wb') as f:
        pickle.dump(user_names, f)

    print('delete complete')

else:
    print('not exist user')
