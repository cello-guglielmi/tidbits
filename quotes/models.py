from django.db import models
from django.conf import settings

'''
def truncate(self):
    words = self.sentence.split()
    chat_limit = 30
    output = []
    for word in words:
        if len(' '.join(output + [word])) > chat_limit:
            break
        output.append(word)
    truncated = ' '.join(output)
    if len(truncated) < len(words):
        truncated += '...'
    return truncated
'''

class Nationality(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=3, unique=True)
    class Meta:
        verbose_name_plural = "nationalities"

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True, related_name='authors')
    portrait = models.ImageField(upload_to='authors', null=True, blank=True)
    def __str__(self):
        return self.name

class Quote(models.Model):
    sentence = models.TextField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_quotes', blank=True)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_quotes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    MOODS = {
        'love': 'Love',
        'motivational': 'Motivational',
        'analytical': 'Analytical',
        'humble': 'Humble',
        'silly': 'Silly',
    }
    mood = models.CharField(max_length=50, choices=MOODS)

    def __str__(self):
        return self.sentence[:40] + '...' if len(self.sentence) > 40 else self.sentence
    
#========================================================
# === Submission Models =================================
#========================================================

class AuthorSubmission(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='author_submissions')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    status = models.CharField(max_length=20, choices=(('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')), default='pending')
    author_obj = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, default=None)
    def __str__(self):
        return self.name

class QuoteSubmission(models.Model):
    sentence = models.TextField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    new_author_submission = models.ForeignKey(AuthorSubmission, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quote_submissions')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    status = models.CharField(max_length=20, choices=(('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')), default='pending')
    MOODS = {
        'love': 'Love',
        'motivational': 'Motivational',
        'analytical': 'Analytical',
        'humble': 'Humble',
        'silly': 'Silly',
    }
    mood = models.CharField(max_length=50, choices=MOODS)

    def __str__(self):
        return self.sentence[:40] + '...' if len(self.sentence) > 40 else self.sentence
    
