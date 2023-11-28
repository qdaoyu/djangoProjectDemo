from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
import pandas as pd
from .models import Question,Choice,TEST_VARIANT
from asgiref.sync import sync_to_async
from django.template import loader
from django.urls import reverse

# Create your views here.
@sync_to_async
def get_latest_questions():
    return list(Question.objects.order_by('pub_date')[:5])

async def showHowtoUseAsync(request):
#     Question.objects.order_by('pub_date')[:5]。在异步上下文中调用同步的数据库查询是不允许的，因为这可能会导致事件循环的阻塞。
# 为了在异步视图中执行数据库查询，你可以使用 asgiref 库中的 database_sync_to_async 装饰器将同步的数据库查询操作转换为异步操作 
# from asgiref.sync import sync_to_async
    latest_question_list = await get_latest_questions()
    output = ', '.join([q.question_text for q in latest_question_list]) + TEST_VARIANT
    print(output)
    return HttpResponse(output)

# 下述代码的作用是，载入 polls/index.html 模板文件，并且向它传递一个上下文(context)。这个上下文是一个字典，它将模板内的变量映射为 Python 对象。
def indexOld(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

# 一个快捷函数： render()¶
# 「载入模板，填充上下文，再返回由它生成的 HttpResponse 对象」是一个非常常用的操作流程。于是 Django 提供了一个快捷函数，我们用它来重写 index() 视图：
# 注意到，我们不再需要导入 loader 和 HttpResponse 
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # print(111)
    return render(request, 'polls/index.html', context)




async def excelRead(request):
    excel_path = r'/Users/mac/cleverPig/tempdownload/门店对应信息.xlsx'
    df = pd.read_excel(excel_path)
    print(df.head(10))
    return HttpResponse("|".join(list(df.columns)))

def setTestValue(request, change_value):
    global TEST_VARIANT
    TEST_VARIANT = change_value
    return HttpResponse("You're changing a value %s." % change_value)

def detailNotAdvise(request, question_id):
    try:
        question = Question.objects.get(pk= question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,"polls/detail.html",{"question":question})

# 一个快捷函数： get_object_or_404()¶
# 尝试用 get() 函数获取一个对象，如果不存在就抛出 Http404 错误也是一个普遍的流程。Django 也提供了一个快捷函数
# 为什么我们使用辅助函数 get_object_or_404() 而不是自己捕获 ObjectDoesNotExist 异常呢？还有，为什么模型 API 不直接抛出 ObjectDoesNotExist 而是抛出 Http404 呢？
# 因为这样做会增加模型层和视图层的耦合性。指导 Django 设计的最重要的思想之一就是要保证松散耦合。一些受控的耦合将会被包含在 django.shortcuts 模块中。
# 也有 get_list_or_404() 函数，工作原理和 get_object_or_404() 一样，除了 get() 函数被换成了 filter() 函数。如果列表为空的话会抛出 Http404 异常。
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,"polls/detail.html",{"question":question,"error_message":"you did not select a choice"})
    else:
        select_choice.votes += 1
        select_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))