from bs4 import BeautifulSoup
import json
import xlwt

with open('index.html','r') as f:
    html = f.read()

soup = BeautifulSoup(html,'html.parser')
trs = soup.find_all("tr")
questions = []
for tr in trs:
    if 'align' in tr.attrs:
        tds = tr.find_all('td')

        if len(tds) == 0:
            continue

        id = tds[0].text
        picid = tds[8].text.replace('.jpg','')
        answer = tds[-2].text

        questions.append({
            'id' : id,
            'picid' : picid,
            'answer' : answer
        })

class ExcelOperator():
    def __init__(self):
        self.book = xlwt.Workbook(encoding="utf-8")
        self.sheet = self.book.add_sheet("sheet1")
        self.current_line = 1

    def write_head(self, header_list):
        for index in range(len(header_list)):
            self.sheet.write(0, index, header_list[index])

    def append_line(self, list):
        for index in range(len(list)):
            value = list[index]
            self.sheet.write(self.current_line, index, value)
        self.current_line += 1

    def save(self, filename):
        self.book.save(filename)

with open('物理网考题库.json','w',encoding='utf-8') as f:
    json.dump(questions,f,indent=4,ensure_ascii=False)



excel = ExcelOperator()
excel.write_head(['ID','图片ID','答案'])
for question in questions:
    excel.append_line([
        question['id'],
        question['picid'],
        question['answer']
    ])
excel.save("物理网考题库.xlsx")
