# encoding: utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg,CityDict,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
import json
from django.db.models import Q
from operation.models import UserFavorite
from courses.models import Course
# Create your views here.
# 课程机构列表页，筛选页


class OrgView(View):
    #课程机构列表
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_citys = CityDict.objects.all()
        #机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords) )

        #对城市进行筛选
        city_id = request.GET.get('city',"")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #对类别进行筛选
        category = request.GET.get('ct',"")
        if category:
            all_orgs = all_orgs.filter(catgory=category)

        #排序设计
        sort = request.GET.get("sort","")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort =="courses":
                all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
       #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs,5, request=request)#第2个参数 为每页的个数
        orgs = p.page(page)

        return render(request,"org-list.html", {
            "all_orgs":orgs,
            "all_citys":all_citys,
            'org_nums':org_nums,
            "city_id":city_id,
            "category": category,
            "hot_orgs":hot_orgs,
            "sort":sort
        }
                      )

# 用户添加咨询课程表单提交
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        res = dict()
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)#保存都数据库
            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            res['msg'] = '添加出错'
        return HttpResponse(json.dumps(res), content_type='application/json')#返回json格式

# 课程机构详情页的首页
class OrgHomeView(View):
    def get(self, request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums +=1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav =True
        # 取出某个指定课程机构下所有的课程(course)# 语法 course + _set
        all_courses = course_org.course_set.all()[:3]
        # 取出某个指定课程机构下所有的老师(course)
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
             'course_org': course_org,
             'org_id': org_id,
            'current_page':current_page,
            'has_fav':has_fav
        })


# 课程机构详情页讲师页面
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav =True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'org_id': org_id,
            'all_courses': all_courses,
            'current_page':current_page,
            'has_fav':has_fav
        })

    # 课程机构介绍页
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav =True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'org_id':org_id,
            'has_fav': has_fav
        })


# 课程机构详情页     讲师页面
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav =True
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'current_page': current_page,
            'course_org': course_org,
            'org_id': org_id,
            'has_fav':has_fav
        })

# 用户收藏、取消收藏 课程机构
class AddFavView(View):

    '''
    def set_fav_nums(self, fav_type, fav_id, num=1):
        if fav_type == 1:
            course = Course.objects.get(id=fav_id)
            course.fav_nums += num
            course.save()
        elif fav_type == 2:
            course_org = CourseOrg.objects.get(id=fav_id)
            course_org.fav_nums += num
            course_org.save()
        elif fav_type == 3:
            teacher = Teacher.objects.get(id=fav_id)
            teacher.fav_nums += num
            teacher.save()
    '''
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))
        res = dict()
        if not request.user.is_authenticated():#先判断用户是否登录
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')
        # 查询收藏记录
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            # self.set_fav_nums(fav_type, fav_id, -1)
            if int(fav_type) ==1:
                course =  Course.objects.get(id=int(fav_id))
                course.fav_nums -=1
                if course.fav_nums <0:
                    course.fav_nums =0
                course.save()
            elif int(fav_type)==2:
                course_org =  CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -=1
                if course_org.fav_nums < 0:
                    course_org.fav_nums =0
                course_org.save()
            elif int(fav_type)==3:
                teacher =  Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -=1
                if teacher.fav_nums<0:
                    teacher.fav_nums = 0
                teacher.save()
            res['status'] = 'success'
            res['msg'] = '收藏'
        else:
            user_fav = UserFavorite()
            if int(fav_id) >0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                #self.set_fav_nums(fav_type, fav_id, 1)
                res['status'] = 'success'
                res['msg'] = '已收藏'
            else:
                res['status'] = 'fail'
                res['msg'] = '收藏出错'
        return HttpResponse(json.dumps(res), content_type='application/json')



# 讲师列表页
class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        #机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords) |
                Q(work_position__icontains=search_keywords)
            )

        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]


        # 最新  人气排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
             'sort': sort,
        })


# 讲师详情
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)
        #讲师排行
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        #收藏功能
        has_teacher_faved = False
        # 注意这里有个坑就是 teacher_id 是字符串，teacher.id 是数字
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,
        })