from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import User, Problem, Example, Submission, Contest, ContestRegistration, ContestSubmission


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    pfp = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["full_name", "university_id", "email", "password", "pfp"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@uap-bd.edu"):
            raise forms.ValidationError("Invalid email address")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.endswith("@uap-bd.edu"):
            raise forms.ValidationError("Invalid email address")
        return username

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'pfp']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'pfp': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("Invalid email address")
        return email

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'difficulty', 'time_limit', 'statement', 'input_specification', 'output_specification']

ExampleFormSet = inlineformset_factory(
    Problem, Example,
    fields=['input', 'output', 'note'],
    extra=1,
    can_delete=True,
    widgets={
        'input': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        'output': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        'note': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
    }
)

class SubmissionForm(forms.ModelForm):
    code_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['py', 'c', 'cpp', 'cc', 'cxx', 'java', 'js'])]
    )

    class Meta:
        model = Submission
        fields = ['language', 'code_file']


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['name', 'description', 'start_time', 'end_time', 'problems']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'problems': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time.")

        return cleaned_data

class ContestRegistrationForm(forms.ModelForm):
    class Meta:
        model = ContestRegistration
        fields = ['name', 'email', 'student_id']

class ContestSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContestSubmission
        fields = ['language', 'code_file']
        widgets = {
            'code': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
        }