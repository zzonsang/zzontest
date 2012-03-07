# -*- encoding: UTF-8 -*-

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django_bookmarks.bookmarks.forms import RegistrationForm, BookmarkSaveForm,\
    SearchForm, FriendInviteForm
from django_bookmarks.bookmarks.models import Link, Bookmark, Tag,\
    SharedBookmark, Friendship, Invitation
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.db.models.query_utils import Q
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 10


def main_page(request):
#    request.session['django_language']='en'
    
    shared_bookmarks = SharedBookmark.objects.order_by('-date')[:10]
    variables = RequestContext(request, {
                                        'shared_bookmarks' : shared_bookmarks
                                        })
    # RequestContext 을 이용하면 기본적으로 User 정보를 넘겨주며, 추가로 다른 변수도 보낼 수 있다.
    return render_to_response('main_page.html', variables)

def user_page(request, username):
    # get_object_or_404는 첫번째 인자인 'User' 모델에서 'username'을 가져오도록 하고 없으면 '404 Page Not Found'를 출력해준다.
    user = get_object_or_404(User, username=username)
    query_set = user.bookmark_set.order_by('-id')
    paginator = Paginator(query_set, ITEMS_PER_PAGE)
    is_friend = Friendship.objects.filter(from_friend=request.user, to_friend=user)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    try:
        bookmarks = paginator.page(page)
    except:
        raise Http404
    
    variables = RequestContext(request, { 
                                         'bookmarks': bookmarks.object_list, 
                                         'username': username, 
                                         'show_tags': True,
                                         'show_edit': username == request.user.username,
                                         'show_paginator' : paginator.num_pages > 1,
                                         'has_prev' : bookmarks.has_previous(),
                                         'has_next' : bookmarks.has_next(),
                                         'page' : page,
                                         'pages' : paginator.num_pages,
                                         'next_page' : bookmarks.next_page_number(),
                                         'prev_page' : bookmarks.previous_page_number(), 
                                         'is_friend' : is_friend,
                                         })
    
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
            user = User.objects.create_user(
                                     username=form.cleaned_data['username'], 
                                     email=form.cleaned_data['email'], 
                                     password=form.cleaned_data['password1'])
            # invitation
            if 'invitation' in request.session:
                # Retrieve the invitation object.
                invitation = Invitation.objects.get(id=request.session['invitation'])
                
                # Create friendship from user to sender
                friendship = Friendship( from_friend = user, to_friend = invitation.sender )
                friendship.save()
                
                # Create friendship from sender to user
                friendship = Friendship( from_friend = invitation.sender, to_friend = user )
                friendship.save()
                
                # Delete the invitation from the database and session
                invitation.delete()
                del request.session['invitation']
            
            return HttpResponseRedirect('/register/success')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form} )
    
    return render_to_response('registration/register.html', RequestContext(request, variables ) )

'''
ajax 로 POST 요청시 403 에러가 발생하고 이는 @csrf_exempt 을 이용하여 1차적으로 회피할 수는 있다.
하지만, 올바른 방법은 아닌 것으로 보고 있다.
bookmar_edit.js 에서 해결해야 할 이슈로 보인다.
이번 이슈는 http://jessoclarence.blogspot.com/2011/12/django-post-csrf.html 로 처리 했음
'''
# 북마크 입력 페이지
# 로그인한 사용자만 접근할 수 있도록 제한한다.
@login_required(login_url='/login/')
#@permission_required('bookmarks.add_bookmark', login_url="/login/")
def bookmark_save_page(request):
    ajax = request.GET.has_key('ajax')
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
            if ajax:
                variables = RequestContext(request, {
                                                     'bookmarks' : [bookmark],
                                                     'show_edit' : True,
                                                     'show_tags' : True
                                                     
                })
                return render_to_response('bookmark_list.html', variables)
            else:
                return HttpResponseRedirect('/user/%s/' % request.user.username)
        else:
            if ajax:
                return HttpResponse('failure')
    elif request.GET.has_key('url'):
        url = request.GET['url']
        title = ''
        tags = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(link=link, user=request.user)
            title = bookmark.title
            tags = ' '.join( tag.name for tag in bookmark.tag_set.all() )
            
        except ObjectDoesNotExist:
            pass
        form = BookmarkSaveForm( {
                                  'url':url,
                                  'title':title,
                                  'tags':tags
                                  })
    else:
        form = BookmarkSaveForm()
        
    variables = RequestContext(request, { 'form': form } )
    if ajax:
        return render_to_response('bookmark_save_form.html', variables)
    else:
        return render_to_response('bookmark_save.html', variables)

'''
_ 로 시작하는 함수는 import 하는 다른 모듈에서는 사용할 수 없다.
'''     
def _bookmark_save(request, form):     
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
            
    # 첫 페이지에서 공유하도록 설정합니다.
    if form.cleaned_data['share']:
        shared_bookmark, created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
        if created:
            shared_bookmark.users_voted.add(request.user)
            shared_bookmark.save()
            
    # 북마크를 저장합니다.
    bookmark.save()
    
    return bookmark
            
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
#            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]

            # ver2. 9.2.3 검색 기능 개선
            # 검색어를 분리한다.
            keywords = query.split()
            q = Q()
            for keyword in keywords:
                q = q & Q(title__icontains=keyword)
            bookmarks = Bookmark.objects.filter(q)[:10]
            
    variables = RequestContext(request, {'form': form, 
                                         'bookmarks': bookmarks, 
                                         'show_results': show_results, 
                                         'show_tags': True, 
                                         'show_user': True
                                         })
    
    # AJAX 요청인지 확인한다.
    if request.is_ajax():
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)

@login_required(login_url='/login/')
def bookmark_vote_page(request):
    if request.GET.has_key('id'):
        try:
            id = request.GET['id']
            shared_bookmark = SharedBookmark.objects.get(id=id)
            user_voted = shared_bookmark.users_voted.filter(username=request.user.username)
            
            if not user_voted:
                shared_bookmark.votes += 1
                shared_bookmark.users_voted.add(request.user)
                shared_bookmark.save()
        except ObjectDoesNotExist:
            raise Http404('Not find the bookmark.')
        
    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    return HttpResponseRedirect('/')

def popular_page(request):
    today = datetime.today()
    yesterday = today - timedelta(1)
    shared_bookmarks = SharedBookmark.objects.filter(date__gt=yesterday)
    shared_bookmarks = shared_bookmarks.order_by('-votes')[:10]
    variables = RequestContext(request, {
                                         'shared_bookmarks' : shared_bookmarks
                                         })
    return render_to_response('popular_page.html', variables)
    
def bookmark_page(request, bookmark_id):
    shared_bookmark = get_object_or_404(SharedBookmark, id=bookmark_id)
    varialbes = RequestContext(request, {
                                        'shared_bookmark' : shared_bookmark
                                         })
    return render_to_response('bookmark_page.html', varialbes)

def ajax_tag_autocomplete(request):
    if request.GET.has_key('q'):
        tags = Tag.objects.filter(name__istartswith=request.GET['q'])[:10]
        return HttpResponse('\n'.join(tag.name for tag in tags))
    return HttpResponse()

def friends_page(request, username):
    user = get_object_or_404(User, username=username)
    friends = [friendship.to_friend for friendship in user.friend_set.all()]
    friend_bookmarks = Bookmark.objects.filter(user__in=friends).order_by('-id')
    variables = RequestContext(request, {
                                         'username' : username,
                                         'friends' : friends,
                                         'bookmarks' : friend_bookmarks[:10],
                                         'show_tags' : True,
                                         'show_user' : True
                                         })
    return render_to_response('friends_page.html', variables)

@login_required(login_url='/login/')
def friend_add(request):
    if request.GET.has_key('username'):
        friend = get_object_or_404(User, username=request.GET['username'])
        friendship = Friendship( from_friend = request.user, to_friend = friend )
        try:
            friendship.save()
            request.user.message_set.create(message='%s has been added as friend.' % friend.username)
        except:
            request.user.message_set.create(message='%s is already a friend.' % friend.username)
        return HttpResponseRedirect('/friends/%s/' % (request.user.username) )
    else:
        raise Http404

@login_required(login_url='/login/')
def friend_invite(request):
    if request.method == 'POST':
        form = FriendInviteForm(request.POST)
        if form.is_valid():
            invitation = Invitation(
                                    name = form.cleaned_data['name'],
                                    email = form.cleaned_data['email'],
                                    code = User.objects.make_random_password(20),
                                    sender = request.user
                                    )
            invitation.save()
            try:
                invitation.send()
                request.user.message_set.create( message=u'%s has sent an invitation message.' % invitation.email)
            except:
                request.user.message_set.create( message=u'There was an error in the invite.')
            
            return HttpResponseRedirect('/friend/invite/')
    else:
        form = FriendInviteForm()
    
        variables = RequestContext(request, { 'form' : form })
        return render_to_response('friend_invite.html', variables)

def friend_accept(request, code):    
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    
    return HttpResponseRedirect('/register/')
    
    
def highchart_page(request):
    return render_to_response('highchart.html', None)

def datatables_page(request):
    return render_to_response('datatables.html', None)
    
    