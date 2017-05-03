from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup as BS

def cal(xh):
    posturl = 'http://210.44.176.116/cjcx/zcjcx_list.php'

    postdata = {
    'post_xuehao':xh,
    'Submit':'提交'
    }

    s = requests.session()
    r = s.post(posturl,postdata)

    bsObj = BS(r.text)
    #提取带有课程成绩的标签内容
    list1 = bsObj.findAll('td',{'scope':'col'})
    #去掉标签
    list2 = []
    for i in range(len(list1)):
        list2.append(list1[i].text)
    #去掉没用的内容
    list3 = []
    for i in list2:
        j = i.replace('\xa0','')
        if j != '':
            list3.append(j)
    i = 0        
    while i < len(list3):
        if list3[i]=='2012-2013'or list3[i]=='2013-2014'or list3[i]=='2014-2015'or list3[i]=='2015-2016'or list3[i]=='2016-2017'or list3[i]=='2017-2018':
            del list3[i]
            del list3[i]
        i += 1

    #提取需要的信息
    name = list3[1]
    i = 0
    #重修
    while i < len(list3)-1:
        if list3[i]=='必修课'or list3[i]=='选修课'or list3[i]=='实践'or list3[i]=='实践环节':
            j = 0
            while j < len(list3)-1:
                if (list3[i+1]==list3[j+1])and(j > i):
                    del list3[i]
                    break
                j += 1
        i += 1
    for i in range(len(list3)):
        if list3[i] == '优秀':
            list3[i] = '95'
        if list3[i] == '良好'or list3[i] == '免修':
            list3[i] = '84'
        if list3[i] == '中等':
            list3[i] = '73'
        if list3[i] == '及格':
            list3[i] = '62'
        if list3[i] == '不及格'or list3[i] == '不合格'or list3[i] == '缺考'or list3[i] == '缓考'or list3[i] == '休学'or list3[i] == '作弊':
            list3[i] = '0'
        if list3[i] == '合格':
            list3[i] = '70'
    list4 = []
    sumtotal = 0.0
    sumcent = 0.0
    for i in range(len(list3)):
        if list3[i]=='必修课'or list3[i]=='选修课'or list3[i]=='实践'or list3[i]=='实践环节':
            if float(list3[i+3])>=60:
                sumcent += float(list3[i+2])
                sumtotal += float(list3[i+2])*float(list3[i+3])
            elif float(list3[i+4])==60:
                sumcent += float(list3[i+2])
                sumtotal += float(list3[i+2])*float(list3[i+4])
            else:
                sumcent += float(list3[i+2])
                sumtotal += float(list3[i+2])*0
    score = sumtotal/sumcent
    return name,score


app = Flask(__name__)

@app.route('/', methods=['GET'])
def score_form():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score_get():
    a = cal(request.form['xh'])
    name = '姓名：{}'.format(a[0])
    score = '绩点：{}'.format(a[1])
    return render_template('score.html',name=name,score=score)

if __name__ == '__main__':
    app.run()

