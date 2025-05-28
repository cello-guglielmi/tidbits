from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    full_name = models.CharField(max_length=30)
    COUNTRIES= {
        'GER': 'Germany',
        'GBR': 'United Kingdom',
        'USA': 'United States',
        'BRA': 'Brazil',
        'MDE': 'Middle Earth',
        'NAR': 'Narnia',
    }
    nationality = models.CharField(max_length=50, choices=COUNTRIES)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
        return self.full_name

class Quote(models.Model):
    sentence = models.TextField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    MOODS = {
        'love': 'Love',
        'motivational': 'Motivational',
        'analytical': 'Analytical',
        'humble': 'Humble',
        'silly': 'Silly',
    }
    mood = models.CharField(max_length=50, choices=MOODS)
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
    def __str__(self):
        return self.sentence
