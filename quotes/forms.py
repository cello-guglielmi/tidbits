from django import forms
from . import models

class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = ['name']



class QuoteSubmissionForm(forms.ModelForm):

    author_name = forms.CharField(label='Author:', max_length=30, required=True, help_text="You can select an existing author or submit a new one.")
    sentence = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your quote…'}))
    MOOD_CHOICES_WITH_BLANK = [('', '-----')] + list(models.QuoteSubmission.MOODS.items())
    mood = forms.ChoiceField(label='Mood (help us categorize this quote)', choices=MOOD_CHOICES_WITH_BLANK, help_text="Choose the tone you feel best fits this quote. We'll review and adjust if needed.")


    class Meta:
        model = models.QuoteSubmission
        fields = ['author_name', 'sentence', 'mood']

    def clean_author_name(self):
        return self.cleaned_data['author_name'].strip().title()
    
    def save(self, user, commit=True):
        instance = super().save(commit=False)
        
        name = self.cleaned_data['author_name']
        existing_author = models.Author.objects.filter(name__iexact=name).first()
        if existing_author:
            instance.author = existing_author
        else:
            new_author_inst = models.AuthorSubmission.objects.create(name=name, submitted_by=user)
            instance.new_author_submission = new_author_inst
    
        instance.submitted_by = user
        if commit:
            instance.save()
        return instance