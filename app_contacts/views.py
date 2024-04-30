from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from app_contacts.forms import ContactForm, AddressForm
from app_contacts.models import Contact, Address


def main(request, page=1):
    contacts = Contact.objects.all()

    # per_page = 10
    # paginator = Paginator(contacts, per_page)
    # contacts_on_page = paginator.page(per_page)

    return render(request, "app_contacts/contacts.html", context={'contacts': contacts})


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
            form.save()

            address = form2.save(commit=False)
            address.contact = form.instance
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
        # form = ContactForm(instance=a)
    return render(request, "app_contacts/contact_update.html", context={'form': form, 'contact': a, 'address': b})

# def contact_update(request, contact_id):
#     a = get_object_or_404(Contact, id=contact_id)
#
#     if request.method == "POST":
#         form = ContactUpdateForm(request.POST, instance=a)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Contact '{form.cleaned_data['name']}' {form.cleaned_data['surname']}' updated")
#             return redirect(reverse('contact_update', args=[contact_id]))
#         else:
#             form = ContactUpdateForm(instance=a)
#     return render(request, "app_contacts/contact_update.html", context={'form': ContactUpdateForm()})
