from django.urls import path

from . import views
# 为 URL 名称添加命名空间¶
# 教程项目只有一个应用，polls 。在一个真实的 Django 项目中，可能会有五个，十个，二十个，甚至更多应用。Django 如何分辨重名的 URL 呢？举个例子，
# polls 应用有 detail 视图，可能另一个博客应用也有同名的视图。Django 如何知道 {% url %} 标签到底对应哪一个应用的 URL 呢？
# 答案是：在根 URLconf 中添加命名空间。在 polls/urls.py 文件中稍作修改，加上 app_name 设置命名空间：
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.excelRead, name='excelRead'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /polls/test01/vote/
    path('<str:change_value>/', views.setTestValue, name='setTestValue'),
]