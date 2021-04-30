from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail

def contact(request):
    if request.method=="POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Remove inquiry duplicacy
        if request.user.is_authenticated:
            user_id=request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'Enquiry for this particular listing is already made, please wait for our realtor to get back at you')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        #Send Mail
        send_mail(
            'Subject: Property Listing Inquiry',
            'There has been an Inquiry for ' + listing + '. Sign into the admin area for more info',
            'barui1080p@gmail.com',
            [realtor_email,'barui504@gmail.com'],
            fail_silently=False
        )
        
        messages.success(request, 'Your request has processed successfully, our realtor will get back to you')
        return redirect('/listings/'+listing_id)