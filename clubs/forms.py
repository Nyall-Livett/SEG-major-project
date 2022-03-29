"""Forms for the clubs app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Club, Meeting, Post, Book, Moment, BooksRead
from dal import autocomplete

class BookAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated:
        #    return Book.objects.none()

        qs = Book.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'favourite_book', 'favourite_character', 'favourite_genre', 'favourite_author', 'want_to_read_next', 'using_gravatar']
        widgets = { 'bio': forms.Textarea(), 'favourite_book': autocomplete.ModelSelect2(url='book-autocomplete'), 'want_to_read_next': autocomplete.ModelSelect2(url='book-autocomplete') }

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            bio=self.cleaned_data.get('bio'),
            password=self.cleaned_data.get('new_password'),
            favourite_book=self.cleaned_data.get('favourite_book'),
            favourite_character=self.cleaned_data.get('favourite_character'),
            favourite_genre=self.cleaned_data.get('favourite_genre'),
            favourite_author=self.cleaned_data.get('favourite_author'),
            want_to_read_next=self.cleaned_data.get('want_to_read_next'),
        )
        return user


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        keys = list(self.fields)
        keys.remove('using_gravatar')
        for key in keys:
            self.fields[key].widget.attrs['class'] = 'form-control'


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'favourite_book', 'favourite_character', 'favourite_genre', 'favourite_author', 'want_to_read_next', 'using_gravatar']
        widgets = { 'bio': forms.Textarea(), 'favourite_book': autocomplete.ModelSelect2(url='book-autocomplete'), 'want_to_read_next': autocomplete.ModelSelect2(url='book-autocomplete') }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        keys = list(self.fields)
        keys.remove('using_gravatar')
        for key in keys:
            self.fields[key].widget.attrs['class'] = 'form-control'

class ClubForm(forms.ModelForm):
    class Meta:
        """Form options."""

        model = Club
        fields = ['name', 'description', 'theme', 'maximum_members', 'image']
        widgets = {
            'description': forms.Textarea(),
            'maximum_members': forms.NumberInput(attrs={'min': 2, 'max': 64})
        }


    def __init__(self, *args, **kwargs):
        super(ClubForm, self).__init__(*args, **kwargs)
        keys = list(self.fields)
        for key in keys:
            self.fields[key].widget.attrs['class'] = 'form-control'
        # self.fields['image'].required = False



class MeetingForm(forms.ModelForm):
    class Meta:
        "Form options"

        model = Meeting
        fields = ['start', 'finish', 'location', 'book', 'notes']
        widgets = { 'notes': forms.Textarea(), 'book': autocomplete.ModelSelect2(url='book-autocomplete') }
    location = forms.CharField(initial='Online')

class CompleteMeetingForm(forms.ModelForm):
    class Meta:
        "Form options"
        model = Meeting
        fields = ['start', 'finish', 'location', 'URL', 'passcode', 'book', 'chosen_member', 'next_book', 'notes']
        widgets = { 'notes': forms.Textarea(), 'book': forms.Select(attrs={'disabled':'disabled'}), 'next_book': autocomplete.ModelSelect2(url='book-autocomplete') , 'chosen_member': forms.Select(attrs={'disabled':'disabled'}) }
    start = forms.CharField(disabled=True, required=False)
    finish = forms.CharField(disabled=True, required=False)
    location = forms.CharField(disabled=True, required=False)
    URL = forms.CharField(disabled=True, required=False)
    passcode = forms.CharField(disabled=True, required=False)


class EditMeetingForm(forms.ModelForm):
    class Meta:
        "Form options"
        model = Meeting
        fields = ['start', 'finish', 'location', 'URL', 'book', 'notes']
        widgets = { 'notes': forms.Textarea(), 'book': autocomplete.ModelSelect2(url='book-autocomplete') }


class BookReviewForm(forms.ModelForm):
    class Meta:
        "Form options"
        model = BooksRead
        fields = ['book', 'rating']
        widgets = { 'book': autocomplete.ModelSelect2(url='book-autocomplete') }


class BookForm(forms.ModelForm):
    class Meta:

        model = Book
        fields = ['name', 'description', 'isbn', 'author', 'publisher', 'publication_year', 'image_url_s', 'image_url_m', 'image_url_l']

class PostForm(forms.ModelForm):
    class Meta:
        """Form options."""

        model = Post
        fields = ['title','body']
        widgets = {
            'body': forms.Textarea()
        }

class MomentForm(forms.ModelForm):
    """docstring for MomentForm."""
    class Meta:

        model = Moment
        fields = {'body'}


class UploadBooksForm(forms.Form):
    file = forms.FileField()
