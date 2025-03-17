from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from debate import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from debate.sitemaps import StaticViewSitemap, DebateSitemap

# Define sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'debates': DebateSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('debate.urls')),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='debate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Serve robots.txt statically
    path('robots.txt', serve, {'document_root': settings.BASE_DIR, 'path': 'robots.txt'}),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
