from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from Business.models import Business
from django.db.models import Count

class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    # Step-based questions - linked to a specific step in a HowTo guide
    howto_step = models.ForeignKey('HowTo.HowToStep', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def answer_count(self):
        return self.answers.count()

    @property
    def has_accepted_answer(self):
        return self.answers.filter(is_accepted=True).exists()

    @property
    def context_type(self):
        """Returns the context type of the question: step, product, business, or general"""
        if self.howto_step:
            return 'step'
        elif self.product:
            return 'product'
        elif self.business:
            return 'business'
        return 'general'

    @property
    def howto(self):
        """Returns the parent HowTo if this is a step-based question"""
        if self.howto_step:
            return self.howto_step.how_to
        return None

    @property
    def vote_score(self):
        """Calculates the vote score based on answer likes for sorting"""
        return sum(answer.like_count for answer in self.answers.all())

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    is_accepted = models.BooleanField(default=False) # Marked by OP
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    class Meta:
        ordering = ['-is_accepted', '-created_at']
    
    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"
        
    @property
    def like_count(self):
        return self.likes.count()

from Comment.models import Comment

class AnswerComment(Comment):
    """Comments on specific answers for clarification"""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        ordering = ['created_at'] # Comments usually sorted chronologically

    def __str__(self):
        return f"Comment on answer by {self.user.username}"
