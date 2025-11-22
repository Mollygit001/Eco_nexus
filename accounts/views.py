from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, StudentProfileForm


def signup(request):
	if request.method == 'POST':
		form = StudentSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			# Update first/last/email if provided
			user.first_name = form.cleaned_data.get('first_name', '')
			user.last_name = form.cleaned_data.get('last_name', '')
			user.email = form.cleaned_data.get('email', '')
			user.save()

			# Authenticate and login the user
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			if user is not None:
				login(request, user)
				return redirect('accounts:profile')
			return redirect('home')
	else:
		form = StudentSignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
	profile = getattr(request.user, 'student_profile', None)
	if profile is None:
		# In case profile wasn't created by signal
		from .models import StudentProfile
		profile = StudentProfile.objects.create(user=request.user, student_id=f"S{request.user.id:06d}")

	if request.method == 'POST':
		form = StudentProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return render(request, 'accounts/profile.html', {'form': form, 'saved': True})
	else:
		form = StudentProfileForm(instance=profile)
	return render(request, 'accounts/profile.html', {'form': form})
