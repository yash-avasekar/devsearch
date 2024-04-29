from django.db import models
import uuid

from users.models import Profile


# Create your models here.


# Product
class Project(models.Model):
    # one-many (one user can have many projects)
    # dont delete the user data when user is deleted
    owner = models.ForeignKey(Profile ,null=True ,blank=True ,on_delete=models.SET_NULL)
    title  = models.CharField(max_length=200)
    description = models.TextField(null=True ,blank=True)
    featured_image = models.ImageField(null=True ,blank=True ,default='default.jpg')
    demo_link = models.CharField(max_length=2000 ,null=True ,blank=True)
    source_link = models.CharField(max_length=2000 ,null=True ,blank=True)
    # Create many to many relation with tag (one project can have many tag) and
    # visa vera
    tags = models.ManyToManyField('Tag' ,blank=True)
    # total votes on a project
    vote_total = models.IntegerField(default=0 ,null=True ,blank=True)
    # vote ratio (+ve and -ve votes) 
    vote_ratio = models.IntegerField(default=0 ,null=True ,blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 ,unique=True ,primary_key=True ,editable=False)

    
    class Meta:
        ordering = ['-vote_total' ,'-vote_ratio' ,'title']

    def __str__(self):
        return self.title
    
    
    @property
    def reviewers(self):
        # get only the list of owner id (flat makes it pure list)
        queryset = self.review_set.all().value_list('owner__id' ,flat=True)
        return queryset
    
    # propert works as an attribute
    @property
    def getVoteCount(self):
        '''calculate votes'''
        review = self.review_set.all() # child model
        upVotes = review.filter(value='Up').count()
        totalVotes = review.count()

        '''calculate ratio'''
        ratio = ((upVotes / totalVotes) *100)
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

# Review
class Review(models.Model):
    VOTE_TYPE = (
        ('up' , 'Up Vote'),
        ('down' , 'Down Vote')
    )
    # relationship
    # bind owner and review for having only 1 review per project
    owner = models.ForeignKey(Profile ,on_delete=models.CASCADE ,null=True ,blank=True)
    project = models.ForeignKey(Project ,on_delete=models.CASCADE)
    body = models.TextField(null=True ,blank=False)
    value = models.CharField(max_length=200 ,choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 ,unique=True ,primary_key=True 
                          ,editable=False)
    
    class Meta:
        unique_together = [['owner' ,'project']]

    def __str__(self):
        return self.value
    

# Tag (python ,java ,etc)
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 ,unique=True ,primary_key=True 
                          ,editable=False)

    def __str__(self):
        return self.name