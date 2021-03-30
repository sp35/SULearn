from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf.urls import url
from django.urls import path, include
from user.views import (
    Home,
    ViewerProfile,
    CreatorProfile,
    )
from course.views import (
    CourseCreate,
    CourseDetail,
    AddModule,
    enroll,
    complete,
    CourseRate,
    CourseDetailNU,
    ProfileViewerDetail,
    ProfileCreatorDetail,
    creatorprofile_edit,
    viewerprofile_edit,
    search,
    creator_following,
    CreatorProfilenu,
    SubjectList,
    ModuleDetail,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(),name='logout'),
    path('', Home.as_view(), name='home'),
    path('viewerform/',ViewerProfile.as_view(),name='viewerform'),
    path('creatorform/',CreatorProfile.as_view(),name='creatorform'),
    path('createcourse/',CourseCreate.as_view(),name='create-course'),
    path('coursedetail/<pk>/',CourseDetail.as_view(),name='course-detail'),
    path('coursedetail/<pk>/addmodule/', AddModule.as_view(),name='add-module'),
    path('coursedetail/<pk>/enroll/', enroll,name='enroll'),
    path('module/<pk>/complete',complete,name='complete'),
    path('course/<pk>/rate',CourseRate.as_view(),name='course-rate'),
    path('coursedetailnu/<pk>/',CourseDetailNU.as_view(),name='coursenu'),
    path('<str:username>/detail',ProfileViewerDetail.as_view(),name='profileviewer'),
    path('<str:username>/creator/detail/',ProfileCreatorDetail.as_view(),name='profilecreator'),
    path('creatoredit/',creatorprofile_edit,name='creatorprofile_edit'),
    path('vieweredit/',viewerprofile_edit,name='viewerprofile_edit'),
    path('results/',search,name='search'),
    path('follow/<pk>/',creator_following,name='creator_following'),
    path('creatorprofile/<pk>/',CreatorProfilenu.as_view(),name='creatorprofilenu'),
    path('subject/<pk>/',SubjectList.as_view(),name='subjectlist'),
    path('moduledetail/<pk>/',ModuleDetail.as_view(),name='moduledetail')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

