from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.backends import django
from django.urls import reverse
from django.db.models import Q
from django.template.defaultfilters import date as django_date_filter
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractWeekDay

from datetime import datetime, timedelta

from app_contacts.forms import ContactForm, AddressForm
from app_contacts.models import Contact, Address


def main(request, page=1):
    contacts = Contact.objects.all().order_by('name')
    total_contacts = contacts.count()

    if not contacts:
        error_message = "You have no contacts"
    else:
        error_message = None
    query = request.GET.get('q')

    if query:
        contacts = Contact.objects.filter(
            Q(address__in=Address.objects.filter(
                Q(country__icontains=query.strip()) |
                Q(city__icontains=query.strip()) |
                Q(address__icontains=query.strip())
            ))
            | Q(name__icontains=query.strip())
            | Q(surname__icontains=query.strip())
            | Q(email__icontains=query.strip())
            | Q(mobile_phone__icontains=query.strip())
            | Q(home_phone__icontains=query.strip())
            | Q(work_phone__icontains=query.strip())
            | Q(birthdate__icontains=query.strip())
        ).distinct()

        if not contacts:
            error_message = "No contacts found"
        else:
            error_message = None

    per_page = 10
    paginator = Paginator(contacts, per_page)
    page = request.GET.get('page', 1)
    try:
        contacts_on_page = paginator.page(page)
    except PageNotAnInteger:
        contacts_on_page = paginator.page(1)
    except EmptyPage:
        contacts_on_page = paginator.page(paginator.num_pages)

    return render(request, "app_contacts/contacts.html",
                  context={'contacts': contacts_on_page, 'error_message': error_message,
                           'total_contacts': total_contacts})


@login_required
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        form2 = AddressForm(request.POST)

        if form.is_valid() and form2.is_valid():
            contact = form.save()

            address = form2.save(commit=False)
            address.contact = contact
            address.save()
            messages.success(request, f"Contact '{form.cleaned_data['name']}' {form.cleaned_data['surname']}' added")
            return redirect(to="app_contacts:contacts")
        else:
            return render(request, "app_contacts/add_contact.html", context={'form': form, 'form2': form2})
    return render(request, "app_contacts/add_contact.html", context={'form': ContactForm(), 'form2': AddressForm()})


@login_required
def contact_details(request, contact_id):
    a = get_object_or_404(Contact, id=contact_id)
    b = get_object_or_404(Address, contact_id=contact_id)
    return render(request, "app_contacts/contact_details.html",
                  context={'Title': 'Contact details', 'contact': a, 'address': b})


@login_required
def delete_contact(request, contact_id):
    try:
        a = get_object_or_404(Contact, id=contact_id)
        a.delete()
        messages.success(request, f"Contact '{a.name} {a.surname}' deleted")
        return redirect(to="app_contacts:contacts")
    except Contact.DoesNotExist:
        raise Http404("Contact not found")


@login_required
def contact_update(request, contact_id=None):
    a = None

    if contact_id:
        a = get_object_or_404(Contact, id=contact_id)
        b = get_object_or_404(Address, contact_id=contact_id)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=a)
        form2 = AddressForm(request.POST, instance=b)
        if form.is_valid() and form2.is_valid():
            contact = form.save()

            address = form2.save(commit=False)
            address.contact = contact
            address.save()
            if a:
                messages.success(request,
                                 f"Contact '{form.cleaned_data['name']} {form.cleaned_data['surname']}' updated")
            else:
                messages.success(request, f"Contact '{form.cleaned_data['name']} {form.cleaned_data['surname']}' added")
            # return redirect(reverse('app_contacts:contact_update', args=[contact_id]))
            return redirect(to="app_contacts:contact_details", contact_id=contact_id)
    else:
        form = ContactForm(instance=a, initial={'mobile_phone': a.mobile_phone,
                                                'birthdate': a.birthdate})
    return render(request, "app_contacts/contact_update.html", context={'form': form, 'contact': a, 'address': b})


@login_required
def contact_birthday(request):
    period = request.GET.get('period')

    today = datetime.now()
    current_month = today.month
    current_day = today.day
    passed_this_year = []
    today_birthdays = []
    upcoming_this_month = []

    if period == 'today':
        contacts = Contact.objects.filter(birthdate__month=current_month, birthdate__day=current_day)
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        contacts = Contact.objects.filter(birthdate__range=[start_date, end_date])
        print("Query week:", contacts.query)
    elif period == 'month':
        passed_this_year = Contact.objects.filter(birthdate__month=current_month, birthdate__day__lt=current_day)
        today_birthdays = Contact.objects.filter(birthdate__month=current_month, birthdate__day=current_day)
        upcoming_this_month = Contact.objects.filter(birthdate__month=current_month, birthdate__day__gt=current_day)
        contacts = []
    else:
        contacts = []

    context = {
        'passed_this_year': passed_this_year,
        'today_birthdays': today_birthdays,
        'upcoming_this_month': upcoming_this_month,
        'period': period,
        'birthday_contacts': contacts,
    }
    return render(request, "app_contacts/contact_birthday.html", context=context)