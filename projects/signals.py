from django.db.models.signals import post_save, post_delete,pre_delete
from django.conf import settings

from .models import Review, Project


def updateVotesInProjects(sender,instance,created=False,**kwargs):
    if created:
        review = instance
        project = review.project
        project.vote_total += 1
        project.getVoteCount
        project.save()
        review.save() 
    review = instance
    project = review.project
    project.vote_total = review.project.vote_total - 1
    project.save()
    project.getVoteCount
    
post_delete.connect(updateVotesInProjects,sender=Review)
post_save.connect(updateVotesInProjects,sender=Review)
