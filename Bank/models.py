from django.db import models
from django.db.models import Max
from django.conf import settings
import uuid
import os

class User(models.Model):

    def uidgen(*args):
        while True:
            new_id = str(uuid.uuid1())[:8].upper()
            if User.objects.filter(pk=new_id).count() == 0:
                break
        return new_id

    user_id = models.CharField(max_length=8, primary_key=True, default=uidgen, help_text="This is auto-generated")
    screen_name = models.CharField(max_length=20, blank=True, default='')
    unlocked_levels = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
       return self.screen_name if self.screen_name else 'User-'+self.user_id

    def __str__(self):
        return self.screen_name if self.screen_name else 'Use-'+self.user_id

class Level(models.Model):

    def nextLevel(*args):
        max_level = Level.objects.all().aggregate(Max('level'))
        return max_level['level__max']+1 if max_level['level__max'] else 1

    def strLevel(self):
        return 'Level %d' % self.level
    strLevel.short_description = 'Level'
    strLevel.admin_order_field = 'level'

    level = models.IntegerField(primary_key=True, default=nextLevel)
    enabled = models.BooleanField(default=False)

    def __unicode__(self):
       return '(%s) Level %d'% ('Enabled' if self.enabled else 'Disabled', self.level)

    def __str__(self):
        return '(%s) Level %d'% ('Enabled' if self.enabled else 'Disabled', self.level)

    class Meta:
        ordering = ['level']


class Question(models.Model):

    def uidgen(*args):
        while True:
            new_id = str(uuid.uuid1())[:8].upper()
            if Question.objects.filter(pk=new_id).count() == 0:
                break
        print('New q id'+new_id)
        return new_id

    def thumbnail(self):
        return '<img style="width:75px; height:75px;" src="%s%s"/>' % (settings.MEDIA_URL, self.image)
    thumbnail.allow_tags = True

    def setDirectory(self, filename):
         return 'Level{levelIndex}/{name}'.format(levelIndex=str(self.level.level),name=filename)

    level = models.ForeignKey(Level)
    image = models.ImageField("Image", upload_to=setDirectory, default='')
    question_id = models.CharField(max_length=8, primary_key=True, default=uidgen, help_text="This is auto-generated")
    answer = models.CharField(max_length=20, blank=True)
    jumbled_answer = models.CharField(max_length=20, blank=True)
    enabled = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.image:
            name = self.image.name
            print('Modifying name '+name)
            if '/' in name:
                name = name[name.rindex('/')+1:]
            if '.' in name:
                name = name[:name.rindex('.')]

            self.answer = name.upper().replace('_', ' ').strip()
            # self.image.upload_to = self.level
        super(Question, self).save(*args, **kwargs)

    def __unicode__(self):
        return "(%s) Question for %s" % ('Enabled' if self.enabled else 'Disabled', self.answer)

    def __str__(self):
        return "(%s) Question for %s" % ('Enabled' if self.enabled else 'Disabled', self.answer)

    class Meta:
        ordering = ['level']

class Hint(models.Model):
    question_id = models.ForeignKey(Question)
    hint = models.TextField()

    def __unicode__(self):
        return 'Hint'

    def __str__(self):
        return 'Hint'