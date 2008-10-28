import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
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
    
    title = models.CharField('title', max_length=300, help_text='Descriptive title')
    excerpt = models.TextField(blank=True, help_text='A optional summary of the contents')
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)
    
    author = models.ForeignKey(User)
    slug = models.SlugField('slug', unique_for_date='pub_date', 
                                                        help_text='For use in generating url. One slug per date.')
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLISH_STATUS)
    markup = models.IntegerField(choices=MARKUP_CHOICES, default=MARKDOWN_MARKUP)
    
    categories = models.ManyToManyField(Category)
    tags = TagField(help_text='Descriptive comma separated tag(s)')
        
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
        
    class Admin:
        pass
        
    def __unicode__(self):
        return self.title
    
    def save(self):
        #Needs refactoring
        #if self.markup == self.MARKDOWN_MARKUP:            
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save()
        #elif self.markup == self.TEXTILE_MARKUP:            
           # self.body_html = textile(self.body)
           # if self.excerpt:
          #      self.excerpt_html = textile(self.excerpt)
       # super(Entry, self).save()
    
    
    def get_absolute_url(self):
            return ('wesseltoft_entry_detail', (), { 
                                           'year': self.pub_date.strftime("%Y"),
                                           'month': self.pub_date.strftime("%b").lower(),
                                           'day': self.pub_date.strftime("%d"),
                                           'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
class Link (models.Model):
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to del.icio.us', default=True,
                                                                            help_text='If checked, link will be posted to \
                                                                            del.icio.us.')
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField('title',max_length=300)
    slug = models.SlugField('slug', unique_for_date='pub_date', 
                                                        help_text='For use in generating url. One slug per date.')
    # Link                                                        
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)
    via_name = models.CharField('Via', max_length=300, blank=True,
                                                           help_text='The name of the person who refered you \
                                                           to the link. Optional.')
    via_url = models.URLField('Via Url', blank=True,
                                                  help_text='The URL where you found the link. Optional.')
    url = models.URLField(unique=True)
    tags = TagField()
                                                  
    class Meta:
        ordering = ['-pub_date']
        
    class Admin:
        pass
        
    def __unicode__(self):
        return self.title
        
    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        if not self.id and self.post_elsewhere:
            import pydelicious
            from django.utils.encoding import smart_str
            pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD,
                                         smart_str(self.url), smart_str(self.title), smart_str(self.tags))
        super(Link, self).save()
        
    def get_absolute_url(self):
        return ('wesseltoft_link_detail', (), { 
                                            'year': self.pub_date.strftime('%Y'),
                                            'month': self.pub_date.strftime('%b').lower(),
                                            'dat': self.pub_date.strftime('%d'),
                                            'slug': self.slug }),
    get_absolute_url = models.permalink(get_absolute_url)
                                            
    
    
    
    
    
    
    
    
    
    
    
    
    
    


