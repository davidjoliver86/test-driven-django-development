from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
import hashlib


class Entry(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey('auth.User')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name_plural = "entries"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'year': self.created_at.year,
                  'month': self.created_at.month,
                  'day': self.created_at.day,
                  'slug': self.slug,
                  'pk': self.pk}
        return reverse('blog.views.entry_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.body

    def gravatar_url(self):
        # Get the md5 hash of the email address
        md5 = hashlib.new('md5')
        md5.update(unicode(self.email))
        digest = md5.hexdigest()

        url = 'https://www.gravatar.com/avatar/{}'.format(digest)
        return url
