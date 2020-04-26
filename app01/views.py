import os
import xlwt
import json
import re
import datetime
import base64
from io import BytesIO
from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from app01 import models
# Create your views here.

def check_login(func):
    def wrapper(req,*args,**kwargs):
        if 'usertype' not in req.session:
            return redirect('/logintimeout')
        else:
            re = func(req,*args,**kwargs)
            return re
    return wrapper

def logintimeout(request):
    return render(request,'logintimeout.html')


def index(request):
    if request.method == 'GET':
        username = request.COOKIES.get('username')
        userid = request.COOKIES.get('userid')
        if username == None:
            username = ''
            userid = ''
        else:
            username = json.loads(username)
        return render(request,'index2.html',{'c_username':username,'c_userid':userid})
    else:
        # print(request.POST)
        user_id = request.POST.get('userid')
        music_link = request.POST.get('musicLink')
        try:
            regular = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            music_link = re.findall(regular,music_link)[0]
        except Exception as e:
            return HttpResponse('请检查链接是否填写错误')
        system_labe = request.POST.get('systemLabel')
        if system_labe == '其他':
            system_labe = request.POST.get('systemLabel2')
        user_label = request.POST.get('userLabel')
        if user_label == '其他':
            user_label = request.POST.get('userLabel2')
        check_label = request.POST.get('check_label')
        username = request.POST.get('username')
        # imgfile = request.FILES.get('imgfile')
        base64_data = request.POST.get('pic')
        data = base64_data.split(';base64,')[1]
        # if imgfile.size > 2097152:  #文件大小判断
        #     return HttpResponse('文件过大')
        tempobj = models.info.objects.all().last()
        if tempobj:
            tempid = tempobj.id + 1
        else:
            tempid = 1

        filename = 'img' + str(tempid) + '.png'
        file_path = os.path.join(r'statics',filename)
        data = base64.b64decode(data)
        with open(file_path,'wb') as f:
            f.write(data)
        if check_label == '1':
            checkinfo = '是'
            user_label = system_labe
        else:
            checkinfo = '否'
        newobj = models.info.objects.create(
            userid = user_id,
            username = username,
            musiclink = music_link,
            system_label=system_labe,
            user_label= user_label,
            imgfile=filename,
            checklabel= checkinfo,
        )
        res = render(request,'submitsucess.html')
        username = json.dumps(username)
        res.set_cookie("username",username)
        res.set_cookie("userid",user_id)
        return res
@check_login
def showall(request):
    if request.method == 'GET':
        allobjs = models.info.objects.filter(status='申诉提交')[:20]
        return render(request,'showall.html',{'allobjs':allobjs})

@check_login
def showimg(request,filename):
    if request.method == 'GET':
        return render(request,'showimg.html',{'filename':filename})
@check_login
def check_sucess(request,id):
    obj = models.info.objects.filter(id=id)
    obj.update(
        status = '申诉通过',
    )
    return redirect('/all')
@check_login
def check_false(request,id):
    if request.method == 'GET':
        return render(request,'return_false_info.html')
    else:
        correctlabel = request.POST.get('correct_label')
        obj = models.info.objects.filter(id=id)
        obj.update(
        status = '申诉驳回',
        correct = correctlabel,
    )
    return redirect('/all')
def mypull(request):
    if request.method == 'GET':
        userid = request.COOKIES.get('userid')
        if userid == None:
            userid = ''
        return render(request,'usercheck.html',{'c_userid':userid})
    else:
        userid = request.POST.get('userid')
        allobjs = models.info.objects.filter(userid=userid)
        res = render(request,'mypull.html',{'allobjs':allobjs})
        res.set_cookie("userid",userid)
        return res
def admin(request):
    if request.method == 'GET':
        return render(request,'admin.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            obj = models.admins.objects.get(username=username,password=password)
        except Exception as e:
            return HttpResponse('输入有误，请重试')
        if obj:
            request.session['usertype'] = 'admin'
            return redirect('/all')
        else:
            return HttpResponse('输入有误 请重试')
@check_login
def history(request):
    if request.method == 'GET':
        # allobjs = models.info.objects.all()
        return render(request,'history.html')
    else:
        # print(request.POST)
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        user_id = request.POST.get('userid')
        if not startdate:
            startdate = '2020-01-01'
        if not enddate:
            enddate = datetime.datetime.now().strftime('%Y-%m-%d')
        if user_id:
            allobjs = models.info.objects.filter(submit_time__range=(startdate,enddate),status__in=['申诉通过','申诉驳回'],userid=user_id)
        else:
            allobjs = models.info.objects.filter(submit_time__range=(startdate,enddate),status__in=['申诉通过','申诉驳回'])
        res = render(request,'history.html',{'allobjs':allobjs})
        res.set_cookie('startdate',startdate)
        res.set_cookie('enddate',enddate)
        res.set_cookie('userid',user_id)
        return res

@check_login
def export_excel(request):
    user_id = request.COOKIES.get('userid')
    startdate = request.COOKIES.get('startdate')
    enddate = request.COOKIES.get('enddate')
    if not startdate or not enddate:
        return redirect('/history')
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    # 写入文件标题
    sheet.write(0,0,'网易云ID',style_heading)
    sheet.write(0,0,'网易云昵称',style_heading)
    sheet.write(0,1,'歌曲链接',style_heading)
    sheet.write(0,2,'系统标签',style_heading)
    sheet.write(0,3,'用户给出标签',style_heading)
    # sheet.write(0,4,'申诉截图',style_heading)
    sheet.write(0,4,'申诉时间',style_heading)
    sheet.write(0,5,'申诉状态',style_heading)
    sheet.write(0,6,'正确标签',style_heading)

    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    if user_id:
        allobjs = models.info.objects.filter(submit_time__range=(startdate, enddate), status__in=['申诉通过', '申诉驳回'],userid=user_id)
    else:
        allobjs = models.info.objects.filter(submit_time__range=(startdate, enddate), status__in=['申诉通过', '申诉驳回'])
    for i in allobjs:
        # 格式化datetime
        pri_time = i.submit_time.strftime('%Y-%m-%d')
        # oper_time = i.operating_time.strftime('%Y-%m-%d')
        sheet.write(data_row,0,i.userid)
        sheet.write(data_row,1,i.username)
        sheet.write(data_row,2,i.musiclink)
        sheet.write(data_row,3,i.system_label)
        sheet.write(data_row,4,i.user_label)
        sheet.write(data_row,5,pri_time)
        sheet.write(data_row,6,i.status)
        sheet.write(data_row,7,i.correct)
        # sheet.write(data_row,6,i.statu.statu_name)
        # sheet.write(data_row,7,oper_time)
        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response
