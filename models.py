from django.db import models
import datetime
from django.contrib.auth.models import User
from tagging.fields import TagField
from markdown import markdown
from textile import textile


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

class Entry (models.Model):
    PUBLISH_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    
    MARKDOWN_MARKUP = 1
    #BBCODE_MARKUP = 2
    TEXTILE_MARKUP = 3
    
    MARKUP_CHOICES = (
                (MARKDOWN_MARKUP, 'Markdown'),
                #(BBCODE_MARKUP, 'BBCode'),
                (TEXTILE_MARKUP, 'Tetxtile'),
    )
    
    STATUS_CHOICES = (
                (PUBLISH_STATUS, 'Publish'),
                (DRAFT_STATUS, 'Draft'),
                (HIDDEN_STATUS, 'Hidden'),
    )
    author = models.ForeignKey(User)
    title = models.CharField('title', max_length=300, help_text='Descriptive title')
    slug = models.SlugField('slug', unique_for_date='pub_date', 
                                                        help_text='For use in generating url. One slug per date.')
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLISH_STATUS)
    categories = models.ManyToManyField(Category)
    tags = TagField()
    markup = models.IntegerField(choices=MARKUP_CHOICES, default=MARKDOWN_MARKUP)
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)
    
    def save(self):
        if self.MARKUP_CHOICES == self.MARKDOWN_MARKUP:            
            self.body_html = markdown(self.body)
            if self.excerpt:
                self.excerpt_html = markdown(self.excerpt)
            super(Entry, self).save()
        elif self.MARKUP_CHOICES == self.TEXTILE_MARKUP:            
            self.body_html = textile(self.body)
            if self.excerpt:
                self.excerpt_html = textile(self.excerpt)
        super(Entry, self).save()
        
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
        
    class Admin:
        pass
        
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return "/weblog/%s/%s/" % \
                      (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


