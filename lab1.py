import csv
import os
import time

def esc(code):
    return f'\u001b[{code}m'

RED = esc(41)
BLUE = esc(44)
WHITE = esc(47)
GREEN = esc(42)
BLACK = esc(40)
END = esc(0)

#1. Флаг Японии
def create_flag_japan(size):
    """ Функция, которая создает флаг Японии"""
    flag = ''
    center = size // 2
    radius = size // 4
    for i in range(size):
        for j in range(size):
            distance = ((i - center)**2 + (j - center)**2)**0.5
            if distance <= radius:
                flag += RED
            else:
                flag += WHITE
            flag += '  '
        flag += f'{END}\n'
    return flag

print(f'1. Флаг Японии\n{create_flag_japan(12)}')



#2. Сгенерированный узор, № g
def create_pattern_g(x, a):
    """генерирует узор g (шахматная доска), x - высота, a - количество циклов"""
    pattern = ''
    y = a * x
    for i in range(x):
        for j in range(y):
            if j > x-1 and j % x == 0:
                continue
            if j > x-1:
                times = j // x
                j = j - (times * x)
            if (i + j) % 2 == 0:
                pattern += f'{WHITE}   {END}'
            else:
                pattern += f'{BLACK}   {END}'
        pattern += '\n'
    print(pattern)

print('2. Сгенерированный Узор, № g (шахматная доска)')
create_pattern_g(8, 1)


#3. Создает график функции, f(x) = 3x
def create_graph(y, x):
    """ это создает график функции f(x) = 3x, где y = f(x)"""
    graph = ''
    for i in range(y, -3, -1):
        for j in range(-1, x+1, 1):
            if j == -1 and i > -1:
                graph += f' {i}|'
            elif i == -2 and j != -1:
                graph += f' {j} '
            elif i == -1 and j == -1:
                graph += '   '
            elif i == -1:
                graph += '---'
            elif i == 3*j and i >= 0 and j >= 0:
                graph += GREEN
                graph += ' * '
                graph += END
            else:
                graph += f'   '
        graph += '\n'
    print(graph)

print('3. График функции, f(x) = 3x')
create_graph(9, 3)


#4. Создает гистограмму на основе условия № 7
def get_percent():
    """Вычисляет процент чисел по условию варианта 7 и создает список"""
    greater_minus5 = 0
    less_minus5 = 0
    
    file_path=r'C:\Users\SPRADOH\Desktop\SPRADOH\PythonProjectRepo\sequence.txt'
    # Создаем тестовую последовательность, если файла нет
    try:
        with open(file_path, 'r') as file:
            content=file.read().strip()
            numbers = [float(x.strip()) for x in content.split()]
    except FileNotFoundError:
        print("файл не найден, используется тестовая последовательность")
        # Тестовая последовательность для варианта 7
        numbers = [-2, -6, -1, -8, -3, -7, -4, -9, -2, -10, -1, -11, 
                  -3, -4, -6, -7, -2, -8, -1, -9, -3, -10, -4, -11]
    
    print(f"Всего чисел в последовательности: {len(numbers)}")
    print(f"Положительные числа (отброшены): {len([x for x in numbers if x > 0])}")
    print(f"Нули (отброшены): {len([x for x in numbers if x == 0])}")


    for num in numbers:
        if num > -5 and num < 0:
            greater_minus5 += 1
        elif num < -5:
            less_minus5 += 1
    
    total_relevant = greater_minus5 + less_minus5
    if total_relevant == 0:
        return [['> -5 и < 0', 0], ['< -5', 0]]
    
    greater_percent = round(100 * greater_minus5 / total_relevant, 2)
    less_percent = round(100 * less_minus5 / total_relevant, 2)
    
    data = [['> -5 и < 0', greater_percent], ['< -5', less_percent]]
    return data

def create_histogram(entries):
    """строит гистограмму на основе результатов"""
    graph = ''
    #histogram construction
    for i in range(len(entries)-1, -3, -1):
        line = ''
        if i >= 0:
            # Label and bar
            label = entries[i][0]
            percent = entries[i][1]
            bar_length = int(percent // 5)  # Scale for better visibility
            line += f'{label:>12} |{BLUE}'
            line += '█' * bar_length
            line += f'{END} {percent}%'
        elif i == -1:
            # X-axis line
            line += ' ' * 13 + '└' + '─' * 20
        elif i == -2:
            # X-axis labels
            line += ' ' * 13 + '0%   ' + '20%   ' + '40%   ' + '60%   ' + '80%   ' + '100%'
        print(line)
    print()

percents = get_percent()
print('4. Гистограмма процентного количества чисел по условию варианта 7')
print('Условие: Числа больше -5 и меньше -5, положительные числа отбрасываются')
create_histogram(percents)


#5. Анимация с использованием os.system('cls')
def animate(x):
    """функция, которая создает анимацию, где x - размер"""
    # Фрейм 1: Прямоугольник
    for i in range(x):
        line = ''
        for j in range(x):
            if i == 0 or j == 0 or j == x - 1 or i == x - 1:
                line += f'{RED}   {END}'
            else:
                line += '   '
        print(line)
    time.sleep(1)  #Wait after drawing complete frame
    os.system('cls')
    
    # Фрейм 2: Крест
    for i in range(x):
        line = ''
        for j in range(x):
            if i == x // 2 or j == x // 2:
                line += f'{GREEN}   {END}'
            else:
                line += '   '
        print(line)
    time.sleep(1)  # Wait after drawing complete frame
    os.system('cls')
    
    # Фрейм 3: Диагонали
    for i in range(x):
        line = ''
        for j in range(x):
            if i == j or i + j == x - 1:
                line += f'{BLUE}   {END}'
            else:
                line += '   '
        print(line)
    time.sleep(1)  # Wait after drawing complete frame
    os.system('cls')

print('5. Анимация')
input("Нажмите Enter чтобы начать анимацию...")
animate(12)
print("Анимация завершена!")