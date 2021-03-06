from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
from Portal.models import Game, CharacterAttribute


class CharacterModel(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=50)
    server = models.ForeignKey('Realm')
    iLvl = models.IntegerField(_('iLvl'), default=0, null=True)
    url = models.URLField(null=True, blank=True)
    classCharacter = models.ManyToManyField(CharacterAttribute, verbose_name=_("Class for your character"))

    def __str__(self):
        return "%s: %s - %s : %s" % (self.user.username, self.name, self.game.name, self.server.name)

    class Meta:
        ordering = ('user',)
        verbose_name = _('Character')
        verbose_name_plural = _('Characters')


class Realm(models.Model):
    #TODO Faire une update admin pour remplir automatiquement
    game = models.ForeignKey(Game, blank=True, null=True)
    name = models.CharField(_('Realm name'), max_length=50)

    def __str__(self):
        return "%s - %s" %(self.game, self.name)

    class Meta:
        ordering = ('game',)
        verbose_name = _('Realm')
        verbose_name_plural = _('Realms')


class Raid(models.Model):
    name = models.CharField(_('Raid name'), max_length=64)
    game = models.ForeignKey(Game)
    lvl = models.ForeignKey('RaidLvl', null=True)
    number_of_boss = models.SmallIntegerField(_('Number of boss'))
    boss_successful = models.SmallIntegerField(_('Boss Successful'))
    image = models.ImageField(_('Image'), upload_to='portalraid/image/')

    def class_formatted_level(self):
        return self.lvl.name.replace(' ', '-')

    def get_progression_boss(self):
        return self.boss_successful * 100 / self.number_of_boss

    def get_out_raid(self):
        return self.outraid_set.all()

    def __str__(self):
        return "%s, %s - %s" % (self.name, self.game.name, self.lvl.name)

class Boss(models.Model):
    name = models.CharField(_('Boss name'), max_length=64)
    raid = models.ManyToManyField(Raid)
    position_in_raid = models.SmallIntegerField(_('Position in raid'), default=1)
    story = models.TextField(_('Story about this boss'))
    image = models.ImageField(_('Image'), upload_to='portalraid/boss/')

    def __str__(self):
        return "%s - %s" % (self.name, self.raid.name)

class RaidLvl(models.Model):
    name = models.CharField(_('Level name'), max_length=64, help_text=_("Normal mode, Heroic mode, Mythic mode"))

    def __str__(self):
        return "%s" % self.name

class GroupForRaid(models.Model):
    name = models.CharField(_('Name'), max_length=64)
    users = models.ManyToManyField(CharacterModel)


class ClassForOutRaid(models.Model):
    number = models.SmallIntegerField()
    classCharacter = models.ForeignKey(CharacterAttribute)

    def __str__(self):
        return "%d %s" % (self.number, self.classCharacter.attribute_value)

from datetime import datetime

class OutRaid(models.Model):
    name = models.CharField(_('Out name'), max_length=64)
    raid = models.ForeignKey(Raid)
    raid_lvl = models.ForeignKey(RaidLvl)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(User)
    class_needed = models.ManyToManyField(ClassForOutRaid)
    lvl = models.SmallIntegerField(_('Level'))

    def __str__(self):
        return "%s - %s => %s for %s" % (self.start_date, self.end_date, self.name, self.raid.name)

    def check_character_in(self, character):
        for character_out in self.characterforoutraid_set.all():
            if character == character_out.character:
                return True
        return False

    def get_characters(self):
        return self.characterforoutraid_set.all()

    def can_be_register(self):
        if self.start_date < datetime.now():
            return False
        return True

class CharacterForOutRaid(models.Model):
    out_raid = models.ForeignKey(OutRaid, blank=True, null=True)
    character = models.ForeignKey(CharacterModel)
    classCharacter = models.ForeignKey(CharacterAttribute)
    present = models.BooleanField(default=False)
