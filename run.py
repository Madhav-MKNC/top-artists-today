from os import system


with open('requirements.txt', 'r', encoding='utf-8') as file:
    reqs = file.read().strip().split('\n')


for i in reqs:
    system(f'pip uninstall {i.split('==')[0]}')
    system(f'pip install {i}')

from main import main_entry_point
main_entry_point()
