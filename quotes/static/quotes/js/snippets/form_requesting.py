# Old verbose method of discerning form request methods
'''
if request.method == 'POST':
    form = forms.AuthorSubmissionAdminForm(request.POST, files=request.FILES, instance=subm)
else:
    form = forms.AuthorSubmissionAdminForm(instance=subm)
'''
# Concise  method of discerning form request methods
'''
form = forms.AuthorSubmissionAdminForm(
    request.POST or None,
    request.FILES or None,
    instance=subm)
'''

# Custom filter logic
'''
class PendingStatusFilter(SimpleListFilter):
    title = 'Submission Status'
    parameter_name = 'submission_status'

    def lookups(self, request, model_admin):
        return [
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ]
    
    def choices(self, changelist):
        for lookup, label in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': label,
            }

    def queryset(self, request, queryset):
        value = self.value()
        if self.value():
            return queryset.filter(status__iexact=value)
        return queryset
'''