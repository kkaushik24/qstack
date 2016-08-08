from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
        Base model for generic functionality
    """

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Query(BaseModel):
    """
        Model for query logging
    """

    query = models.CharField(max_length=500, null=False, blank=True)

    def __unicodeO__(self):
        return u'%s' % (self.query)


class QueryQuestion(BaseModel):
    """
        Model to keep info of stackoverflow questions
        that matched the query
    """
    query = models.ForeignKey('Query')
    title = models.CharField(max_length=500, db_index=True)
    tags = models.ManyToManyField('Tag')
    accepted_answer_id = models.PositiveIntegerField()
    answer_html = models.TextField()
    stackoverflow_link = models.URLField(max_length=1000)
    stackoverflow_view_count = models.PositiveIntegerField(default=0)
    stackoverflow_answer_count = models.PositiveIntegerField(default=0)
    stackoverflow_score_count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % (self.title)


class QueryAnswer(BaseModel):
    """
        This is the model for keeping answer information.
    """

    query_question = models.ForeignKey('QueryAnswer')
    stackoverflow_answer_id = models.PositiveIntegerField()
    answer_html = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.query_question.title)


class Tag(BaseModel):
    """
        Tag Model
    """

    name = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)
