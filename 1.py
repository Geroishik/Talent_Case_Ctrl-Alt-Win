import pymorphy2
import json
import time

udaleno = 0

start = time.time()

#Подключение словаря
morph = pymorphy2.MorphAnalyzer()

#Коэффициен совпадения слов (0.8 = предложения совпадают на 80%)
coef = 0.8

#Функция нахождения слов одной части речи
def findwords(types, pred): #NPRO, NOUN, VERB, INFN
    words = []
    for i in pred:
        if str(morph.parse(i)[0][1].POS) in types:
            words.append(i)
    return words

f = [] #Итоговый список
f1 = [] #Список слов в каждом предложении

chars_to_remove = ['.', '!', '?', ','] #Знаки препинания

#Чтение файла(txt)
file = open("case_text.txt", encoding='utf-8-sig')
while (a:=file.readline()) != "":
    f.append(a)
file.close()

"""#Чтение файла(json)
with open('sample.json', encoding='utf-8') as json_file:
    d = json.load(json_file)
for i in d:
    f.append(i['text']+"\n")
"""

#Удаление знаков препинания
for j in f:
    b = []
    for i in j.split():
        if i[-1] in chars_to_remove:
            i = i[:-1]
        b.append(i)
    f1.append(b)

#Алгоритм поиска совпадений
for indi, i in enumerate(f1):
    f2 = f1[:]
    f2.remove(i)

    for indj, j in enumerate(f2):
        res = sum(ele in i for ele in j) #Поиск количества совпадений слов

        if res > ((len(i)+len(j))//2)*coef and not "-\n" in i: #Поиск количества совпадений слов в предложениях
            if findwords(("NPRO", "NOUN"), i) == findwords(("NPRO", "NOUN"), j): #Сравнение существительных и местоимений в предложениях
                # Удаление лишних предложений
                f[indj+1] = "-\n"
                f1[indj+1] = "-\n"
                udaleno+=1

                # Вывод на экран удаленных предложений
                print(f"{indi+1}) {' '.join(i)} \n{indj+1}) {' '.join(j)} \n{res} повторений\n\n")

stop = time.time()

#Запись получившегося списка в файл
with open("itog.txt", "w") as output:
    for i in f:
        output.write(i)

print(f"Всего строк удалено:{udaleno}\nВремя выполнения: {round(stop-start,2)}c")