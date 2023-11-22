import string
import time


arr = list()
arrWrd = list()
arrNRW = list()
arrPrist = list()
arrSuf = list()
arrEnd = list()

#Считывания файла с данными
file = open('case_text.txt', 'r', encoding = 'utf8')
content = file.read()  
content = content.splitlines()

#Считывания файла со словами, что можно выкинуть
file2 = open('sort.txt', 'r', encoding = 'utf8') 
content2 = file2.read()  
content2 = content2.splitlines()

#Открытие файла с приставками и запись в массив
filePrist = open('prist.txt', 'r', encoding = 'utf8')
content3 = filePrist.read()
content3 = content3.splitlines()
for i in range(0, 48):
    strinPrist = content3[i] 
    arrPrist.append(strinPrist)
filePrist.close()

#Открытие файла с суффиксами и запись в массив
fileSuf= open('suf.txt', 'r', encoding = 'utf8')
content4 = fileSuf.read()
content4 = content4.splitlines()
for i in range(0, 83):
    strinSuf = content4[i] 
    arrSuf.append(strinSuf)
fileSuf.close()

#Открытие файла с окончаниями и запись в массив
fileEnd = open('end.txt', 'r', encoding = 'utf8')
content5 = fileEnd.read()
content5 = content5.splitlines()
for i in range(0, 75):
    strinEnd = content5[i] 
    arrEnd.append(strinEnd)
fileEnd.close()

#Открытие выходного файла
file3 = open('rewrite_check_end.txt', 'w', encoding='utf8')

#Запись файла с данными в массив
for i in range(0, 412):
    strin = content[i]
    arr.append(strin)
    res = [word.strip(string.punctuation) for word in strin.split() if word.strip(string.punctuation).isalnum()] #извлечение слов из строки
    #делаем все в нижнем регистре
    for j in range(0, len(res)):
        res[j] = res[j].lower()
    arrWrd.append(res)
file.close()

#Запись файла со словами, что можно выкинуть в массив
for i in range(0, 110): 
    strin2 = content2[i]
    arrNRW.append(strin2)
file2.close()

#Удаление не значимых слов
for i in range(0, 412):
    str2 = arrWrd[i]
    for x in str2:
        if x in arrNRW:
            str2.remove(x)
            arrWrd[i] = str2

def get_root(word):
    find: bool
    find = True
    #удаление окончаний
    word = ''.join(reversed(word))
    while find and len(word) >= 2:
        find = False
        max = ''
        for i in arrEnd:
            if word.find(''.join(reversed(i))) == 0 and len(i) > len(max):
                find = False
                max = i
        if len(word) - len(max) >= 2:
            word = word.replace(''.join(reversed(max)), '', 1)
    word = ''.join(reversed(word))

    find = True
    max = ''
    #удаление приставок
    while find and len(word) >= 2:      
        find = False
        max = ''
        for i in arrPrist:
            if word.find(i) == 0 and len(i) > len(max):
                find = False
                max = i
        if len(word) - len(max)>=2:
            word = word.replace(max, '', 1)    
     
    find = True
    max = ''
    #удаление суффиксов
    word = ''.join(reversed(word))
    while find and len(word) >= 2:
        find = False
        max = ''
        for i in arrSuf:
            if word.find(''.join(reversed(i))) == 0 and len(i) > len(max):
                find = False
                max = i
        if len(word) - len(max) >= 2:
            word = word.replace(''.join(reversed(max)), '', 1)
    word = ''.join(reversed(word))

    return word
      

#Сортирка массива слов по длине и добавление в конце номер строки
j = -1
strin3 = ''
for i in arrWrd:
    j = j + 1
    for k in i:
        k = get_root(k)
    i.sort(key=len)
    for k in i:      
        for n in k:
            strin3 = strin3 + str(n)
    i.append(str(j))
    i.append(strin3)
    strin3 = ''


#Сортировка массива по массивам слов
arrWrd.sort()

#проверка на равенство строк при условии одной опечатки
def check_opet(wrd1, wrd2):
    opet = False
    check = True
    for i in range(0, min(len(wrd1), len(wrd2))):
        if check:
            if wrd1[i] != wrd2[i] and not opet:
                opet = True
            elif wrd1[i] != wrd2[i] and opet:
                check = False
                return False
    if check:
        return True
    else:
        return False
   
      
#Запись в файл

#перенос рерайтов ближе друг к другу
sut1 = arrWrd[0][len(arrWrd[0])-1]
for i in range(1, len(arrWrd)):
    sut2 = arrWrd[i][len(arrWrd[i])-1]
    if not check_opet(sut1, sut2):
        for j in range(i, len(arrWrd)):
            sut3 = arrWrd[j][len(arrWrd[j])-1]
            if check_opet(sut1, sut3):
                a = arrWrd[j]
                arrWrd.pop(j)
                arrWrd.insert(i, a)
    sut1 = sut2
  

l = 0
#группировка рерайтов
j = int(arrWrd[0][len(arrWrd[0])-2])
file3.write(arr[j])
file3.write('\n')
sut1 = arrWrd[0][len(arrWrd[0])-1]
for i in range(1, len(arrWrd)):
    j = int(arrWrd[i][len(arrWrd[i])-2])
    sut2 = arrWrd[i][len(arrWrd[i])-1]
    #print(i)
    if not check_opet(sut1, sut2):
        file3.write('\n')
    file3.write(arr[j])

    sut1 = sut2
    file3.write('\n')

file3.close()

