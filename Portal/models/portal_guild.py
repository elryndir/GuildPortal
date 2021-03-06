from django.db.models.signals import pre_save
from django.dispatch import receiver

__author__ = 'Alexandre Cloquet'


from django.utils.translation import ugettext as _
from django.db.models import Count
from django.db import models
from .enrollment import Game
from SuperPortal.models.superportal import SuperPortal


class Portal(models.Model):
    portal = models.ForeignKey(SuperPortal, blank=True, null=True)
    game = models.ForeignKey(Game, blank=True, null=True)
    active = models.BooleanField(_('Active ?'), default=True)
    name = models.CharField(_("Portal name"), max_length=100)
    slug = models.CharField(_('Slug'), max_length=100, db_index=True, default="", blank=True,
                            help_text=_('You don\'t need to fill it'))
    guild_name = models.CharField(_("Portal guild name"), max_length=100, help_text="Can be blank. If blank, we will take guild name from SuperPortal")
    image = models.ImageField(_('Icon'), upload_to='portal/logo/', help_text=_("Please select an squared image"))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('Portal.views.index', args=[str(self.slug)])

    def __str__(self):
        return u"%s - %s" % (self.guild_name, self.name)

    def get_last_news(self):
        return self.news_set.all().order_by('-published_date')

    def get_most_viewed_news(self):
        return self.news_set.all().order_by('view')

    def get_most_commented_news(self):
        return self.news_set.all().annotate(num_comments=Count('commentnews')).order_by('-num_comments')


from django.template.defaultfilters import slugify

@receiver(pre_save, sender=Portal)
def my_callback(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)
