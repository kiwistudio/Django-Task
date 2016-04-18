import datetime, random, csv


from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse

from .models import UserProfile
from .forms import UserUpdateForm


def user_list(request):
	u = UserProfile.objects.all()

	# Eligible
	now_date = datetime.date.today()
	delta = datetime.timedelta(days=4745)
	eligible = now_date - delta

	return render(request, 'index.html', {'user': u, 'eligible': eligible})


def export_excel(request):
    user = UserProfile.objects.all()
    response = HttpResponse(content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="UserProfile.xls"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Birthday', 'Random Number'])
    for u in user:
        writer.writerow([u.username, u.birthday, u.random_number])

    return response


def user_add(request):

	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			# errors collection
			errors = {}
			# validate data collection
			data = {'username': 'username'+str(random.randint(1, 100)),
					'password': 'password'+str(random.randint(1, 100)),
					'random_number': random.randint(1, 100)}		
			# validate user input
			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = "field is required"
			else:
				try:
					datetime.datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = "enter correct format (e.g. 1985-08-07)"
				else:
					data['birthday'] = birthday

			# save 
			if not errors:
				u = UserProfile(**data)
				u.save()	
				messages.success(request, u'User has been added!')
				return HttpResponseRedirect(reverse('home'))
			else:
				# render form with errors and previous user input
				return render(request, 'user_add.html',
					{'user': UserProfile.objects.all(), 'errors': errors})

		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			messages.info(request, 'Add cancel!')
			return HttpResponseRedirect('%s' % reverse('home'))
	else:
		# initial form render
		return render(request, 'user_add.html',
			{'user': UserProfile.objects.all()})


class UserUpdate(UpdateView):
	model = UserProfile
	template_name = 'user_edit.html'
	form_class = UserUpdateForm
	def get_success_url(self):
		return '%s?status_message=User Saved!' % reverse('home')
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect('%s?status_message=Edit canceled!' % reverse('home'))
		else:
			return super(UserUpdate, self).post(request, *args, **kwargs)


class UserDelete(DeleteView):
	model = UserProfile
	template_name = 'user_delete.html'
	def get_success_url(self):
		return '%s?status_message=User deleted!' % reverse('home')
