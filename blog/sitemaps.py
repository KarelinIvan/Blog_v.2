from django.contrib.sitemaps import Sitemap
from blog.models import Post


class PostSitemap(Sitemap):
    """ Определяет конкретно-прикладную карту сайта """
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
