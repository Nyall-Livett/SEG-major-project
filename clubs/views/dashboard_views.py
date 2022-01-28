from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')



# class ClubPageView(LoginRequiredMixin, View):
#     """ View that handles club page. """

#     """Render log in template with blank log in form."""
#     def render(self):
#         self.request.
        
#         return render(self.request, 'log_in.html', {'form': form, 'next': self.next})