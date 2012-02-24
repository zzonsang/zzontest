# -*- encoding: utf-8 -*-

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django_bookmarks.bookmarks.forms import RegistrationForm, BookmarkSaveForm,\
    SearchForm
from django_bookmarks.bookmarks.models import Link, Bookmark, Tag

def main_page(request):
#    return render_to_response('main_page.html', { 'user': request.user })

    # RequestContext 을 이용하면 기본적으로 User 정보를 넘겨주며, 추가로 다른 변수도 보낼 수 있다.
    return render_to_response('main_page.html', RequestContext(request))
    
#def user_page(request, username):
#    try:
#        user = User.objects.get(username=username)
#    except:
#        raise Http404('사용자를 찾을 수 없습니다.')
#    
#    bookmarks = user.bookmark_set.all()
#    
##    template = get_template('user_page.html')
##    variables = Context( {'username': username, 'bookmarks': bookmarks } )
##    output = template.render(variables)
##    return HttpResponse(output)
#    variables = RequestContext(request, { 'username': username, 
#                                         'bookmarks': bookmarks})
#    return render_to_response('user_page.html', variables)

def user_page(request, username):
    # get_object_or_404는 첫번째 인자인 'User' 모델에서 'username'을 가져오도록 하고 없으면 '404 Page Not Found'를 출력해준다.
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')
    
    variables = RequestContext(request, { 'bookmarks': bookmarks, 'username': username, 'show_tags': True})
    
    return render_to_response('user_page.html', variables)

def logout_page(request):
    # session logout
    logout(request)
    
    # Redirect 을 '/'로 지정함
    return HttpResponseRedirect('/')

# 등록 페이지 
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                                     username=form.cleaned_data['username'], 
                                     email=form.cleaned_data['email'], 
                                     password=form.cleaned_data['password1'])
            return HttpResponseRedirect('/register/success')
    else:
        form = RegistrationForm()
        
    return render_to_response('registration/register.html', RequestContext(request, {'form': form} ))

# 북마크 입력 페이지
# 로그인한 사용자만 접근할 수 있도록 제한한다.
@login_required(login_url='/login/')
def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            
            # URL이 있으면 가져오고 없으면 새로 저장합니다.
            link, dummy = Link.objects.get_or_create( url=form.cleaned_data['url'] )
            
            # 북마크가 있으면 가져오고 없으면 새로 저장합니다.
            bookmark, created = Bookmark.objects.get_or_create( user=request.user, link=link )
            
            # 북마크 제목을 수정합니다.
            bookmark.title = form.cleaned_data['title']
            
            # 북마크를 수정한 경우에는 이전에 입력된 모든 태그를 지웁니다.
            if not created:
                bookmark.tag_set.clear()
            
            # 태그 목록을 새로 만듭니다.
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                    tag, dummy = Tag.objects.get_or_create(name=tag_name)
                    bookmark.tag_set.add(tag)
                    
            # 북마크를 저장합니다.
            bookmark.save()
            
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
            form = BookmarkSaveForm()
        
    return render_to_response('bookmark_save.html', RequestContext(request, {'form': form}))
            
def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    variables = RequestContext(request, {'bookmarks': bookmarks, 'tag_name': tag_name, 'show_tags': True, 'show_user': True})
    
    return render_to_response('tag_page.html', variables)
   
def tag_cloud_page(request): 
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
    
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
            
    # Calculate count range. Avoid dividing by zero
    range = float(max_count - min_count)        
    if range == 0.0:
        range = 1.0
        
    # Calculate tag weights.
    for tag in tags:
        tag.weight = int(MAX_WEIGHT * (tag.count - min_count) / range)
        
    variables = RequestContext(request, {'tags': tags})
    
    return render_to_response('tag_cloud_page.html', variables)
    
def search_page(request):
    form = SearchForm()
    bookmarks = []
    show_results = False
    
    # request.GET은 사전형 데이터(dict)이기 때문에 has_key 메서드로 검색어 'query'가 있는지 확인할 수 있다.
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            # filter 메서드는 검색 조건을 전달받아서 검색 결과를 반환
            # 필드이름__조건 으로 사용한다.
            # exact: 검색어가 필드의 값과 정확하게 일치
            # contains: 검색어가 필드의 값에 포함되는 경우
            # startwith: 필드의 값이 검색어로 시작될 경우
            # lt: 필드의 값이 검색어보다 작은 경우
            # gt: 필드의 값이 검색어보다 큰 경우
            # 앞에 'i'가 붙으면 '대소문자' 구분하지 않음
            # 추가로 아래 문법은 [:10] 을 사용하여 첫 번째 10개만 가져온다는 것을 의미한다.
            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]
    
    variables = RequestContext(request, { 'form': form, 'bookmarks': bookmarks, 'show_results': show_results, 'show_tags': True, 'show_user': True})
    
    # AJAX 요청인지 확인한다.
    if request.is_ajax():
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)



