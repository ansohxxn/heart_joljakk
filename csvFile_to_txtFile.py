import csv


#read csv file
csv_f = open('시.csv', 'r', encoding='utf-8')
read = csv.reader(csv_f)

#create new text file
txt_f = open('Poem.txt', 'w', encoding='utf-8')

#skip the first row
firstline = True                                                                  #['index', '시 제목', '시인', 시 본문']

#readline csv file 
for line in read:
    if firstline:
        firstline = False
        continue
    txt_f.write(line[0]+"\n\n")
    if line[1] == '':
        line[1] = line[1].replace('','제목 미상')
    txt_f.write(line[1]+"\n\n")
    if line[2] == '':
        line[2] = line[2].replace('','작자 미상')
    txt_f.write(line[2])
    if line[3] == '':
        line[3] = line[3].replace('', '본문 없음')
    txt_f.write(line[3]+"\n\n\n\n\n")
    txt_f.write("-------------------------------------------------------\n\n")    #구분선
    
csv_f.close()
txt_f.close()



