import re
import csv

def task1():
    with open('task1-en.txt', 'r') as f:
        text = f.read()
    
    words_c = re.findall(r'\bc\w*\b', text, re.I)
    
    words_after = []
    for match in re.finditer(r'\b(and|the)\s+(\w+)', text, re.I):
        words_after.append(match.group(2))
    
    print("Task 1:")
    print(f"Words starting with 'c': {words_c}")
    print(f"Words after 'and'/'the': {words_after}")
    return words_c, words_after

def task2():
    with open('task2.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    print("Successfully read HTML file with cp1251 (Windows Cyrillic) encoding")
    
    fonts = re.findall(r'font-family:\s*[\'"]?([^;\'"]+)', html, re.I)
    
    cleaned = []
    for font in fonts:
        font_names = font.split(',')
        for font_name in font_names:
            font_name = font_name.strip()
            font_name = font_name.strip(' "\'')
            if font_name:
                cleaned.append(font_name)
    
    font_type = []
    seen = set()
    for font in cleaned:
        if font not in seen:
            seen.add(font)
            font_type.append(font)
    
    print("\nTask 2:")
    print(f"Found {len(font_type)} font-type: {font_type}")
    
    return font_type


def task3():
    s = open('task3.txt', encoding='utf-8').read().split()

    ids = [st for st in s if re.fullmatch(r'\d+', st)]
    fam = [st for st in s if re.fullmatch(r'[A-Z][a-zA-Z]+', st)]
    emails = [st for st in s if re.fullmatch(r'\S+@\S+', st)]
    date = [st for st in s if re.fullmatch(r'\d{4}-\d{2}-\d{2}', st)]
    web = [st for st in s if re.fullmatch(r'https?://\S+|www\.\S+', st)]

    rows = [[ids[i], fam[i], emails[i], date[i], web[i]] for i in range(len(ids))]

    with open('task3_output.csv','w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['ID','Фамилия','Email','Дата','Сайт'])
        w.writerows(rows)

    print('\nTask 3:')
    print('Total=', len(rows))
    return rows

def additional_task():
    with open('task_add.txt', 'r') as f:
        content = f.read()
    
    dates = re.findall(r'\b\d+[./-]\d+[./-]\d+\b', content)[:5]
    emails = re.findall(r'\b\w+@\w+\.\w+\b', content)[:5]
    websites = re.findall(r'\b(?:https?://)?(?:www\.)?\w+\.\w+\b', content)[:5]
    
    print("\nAdditional task:")
    print(f"Dates: {dates}")
    print(f"Emails: {emails}")
    print(f"Websites: {websites}")
    return dates, emails, websites

if __name__ == "__main__":
    task1()
    task2()
    task3()
    additional_task()