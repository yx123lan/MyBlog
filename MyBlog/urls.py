from django.conf.urls import include, url
from django.contrib import admin
from main_view import main, write, submit_blog, save_blog, preview_blog, edit_blog, login, logout
from main_view import blog_favor, delete_blog, all_blog_list, read_blog
from main_view import generate_204
urlpatterns = {
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main),
    url(r'^main/$', main),
    url(r'^main/(\d+)/$', read_blog),
    url(r'^write/$', write),
    url(r'^save-blog/$', save_blog),
    url(r'^submit-blog/$', submit_blog),
    url(r'^preview-blog/$', preview_blog),
    url(r'^edit-blog/(\d+)/$', edit_blog),
    url(r'^delete-blog/(\d+)/$', delete_blog),
    url(r'^list/(\d+)/$', all_blog_list),
    url(r'^main/login/$', login),
    url(r'^main/logout/$', logout),
    url(r'^main/favor/$', blog_favor),
    url(r'^generate_204', generate_204),
}