from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Debate

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'join_debate_code', 'signup']

    def location(self, item):
        return reverse(item)

class DebateSitemap(Sitemap):
    priority = 0.6
    changefreq = 'hourly'

    def items(self):
        return Debate.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('join_debate', kwargs={'debate_id': obj.id})
