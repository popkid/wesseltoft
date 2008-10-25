from django.db import models

class Category(models.Model):
    title = models.CharField('title', max_length=300, help_text='No longer than 300 characters.')
    slug = models.SlugField('slug', unique=True, help_text="Unique 'slug' for use in URL etc.")
    description = models.TextField()
    
    class Meta:
        ordering = ['title']
        verbose_name =('category')
        verbose_name_plural = ('categories')
    
    class Admin:
        pass
        
    def __unicode__(self):
        return u'%s' % self.title
        
    def get_absolute_url(self):
        return "/categories/%s/" % self.slug


