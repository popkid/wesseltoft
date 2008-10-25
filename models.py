from django.db import models

class Category(models.Model):
    title = models.CharField('title', max_length=300, help_text='No longer than 300 characters.')
    slug = models.SlugField('slug', unique=True)
    description = models.TextField()
    
    class Meta:
        verbose_name =('category')
        verbose_name_plural = ('categories')
    
    class Admin:
        pass
        
    def __unicode__(self):
        return u'%s' % self.title

