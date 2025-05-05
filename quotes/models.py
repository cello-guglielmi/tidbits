from django.db import models

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
    def __str__(self):
        return self.full_name

class Quote(models.Model):
    sentence = models.TextField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    MOODS = {
        'Love': 'Love',
        'Motivational': 'Motivational',
        'Analytical': 'Analytical',
        'Humble': 'Humble',
        'Goofy': 'Goofy',
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
        string = self.sentence if len(self.sentence) <= 30 else self.sentence[:30] + '...'
        return string
