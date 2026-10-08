from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .forms import DonationForm,RegisterForm,LoginForm
from .models import Donation,Profile,DonationRequest
from django.contrib import messages
from django.views.decorators.cache import never_cache
# Create your views here.

def register(request):
    if request.method == 'POST':
        obj = RegisterForm(request.POST)

        if obj.is_valid():
            user = obj.save()

            Profile.objects.create(
                user=user,
                role=obj.cleaned_data['role']
            )

            login(request, user)
            return redirect('login')

           
    else:
        obj = RegisterForm()

    return render(request, 'register.html', {'x': obj})


@never_cache
def user_login(request):

    obj = LoginForm()

    if request.method == 'POST':
        obj = LoginForm(data=request.POST)

        if obj.is_valid():

            user = obj.get_user()
            selected_role = obj.cleaned_data['role']

            print("SELECTED ROLE:", selected_role)
            print("USER ROLE:", user.profile.role)

            if user.profile.role == selected_role:

                login(request, user)

                if selected_role == 'Donor':
                    return redirect('donor_dashboard')
                else:
                    return redirect('recipient_dashboard')

            else:
                obj.add_error('role', 'Wrong role selected.')

    return render(request, 'login.html', {'x': obj})

@login_required
def add_donation(request):
    if request.method == 'POST':
        obj = DonationForm(request.POST, request.FILES)

        if obj.is_valid():
            print("USER:", request.user)
            print("AUTH:", request.user.is_authenticated)
            print("ID:", request.user.id)

            donation = obj.save(commit=False)
            donation.donor_id = request.user.id
            donation.save()

            return redirect('donation_list')

    else:
        obj = DonationForm()

    return render(request, 'add_donation.html', {'x': obj})

@login_required
def donation_list(request):

    if request.user.profile.role == 'Donor':
        donations = Donation.objects.filter(donor=request.user)

    else:
        donations = Donation.objects.filter(status='Available')

    return render(request, 'donation_list.html', {'donations': donations})

@login_required
def edit_donation(request, id):
    donation = Donation.objects.get(id=id)

    if request.method == 'POST':
        obj = DonationForm(request.POST, request.FILES, instance=donation)

        if obj.is_valid():
            obj.save()
            return redirect('donation_list')
    else:
        obj = DonationForm(instance=donation)

    return render(request, 'edit_donation.html', {'x': obj})


@login_required
def delete_donation(request, pk):
    donation = Donation.objects.get(id=pk)

    if request.method == 'POST':
        donation.delete()
        return redirect('donation_list')

    return render(request, 'delete_donation.html', {'donation': donation})

@login_required
def donor_dashboard(request):
    return render(request,'donor_dashboard.html')

@login_required
def recipient_dashboard(request):
    return render(request,'recipient_dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def request_donation(request, donation_id):

    donation = Donation.objects.get(id=donation_id)

    if request.user.profile.role != 'Recipient':
        return redirect('donation_list')

    # Already requested check
    if DonationRequest.objects.filter(
        donation=donation,
        recipient=request.user
    ).exists():

        messages.warning(request, 'You have already requested this donation.')
        return redirect('donation_list')

    # Create new request
    DonationRequest.objects.create(
        donation=donation,
        recipient=request.user
    )

    messages.success(request, 'Donation Request Sent Successfully!')

    return redirect('donation_list')

@login_required
def donation_requests(request):

    requests = DonationRequest.objects.filter(
        donation__donor=request.user
    )

    return render(
        request,
        'donation_requests.html',
        {'requests': requests}
    )

@login_required
def accept_request(request, request_id):
    donation_request = DonationRequest.objects.get(id=request_id)

    # Only the donor who owns the donation can accept
    if donation_request.donation.donor != request.user:
        return redirect('donor_dashboard')

    donation_request.status = 'Accepted'
    donation_request.save()

    return redirect('donation_requests')

@login_required
def reject_request(request, request_id):
    req = DonationRequest.objects.get(id=request_id)
    req.status = "Rejected"
    req.save()
    return redirect('donation_requests')

@login_required
def my_requests(request):
    requests = DonationRequest.objects.filter(recipient=request.user)

    return render(
        request,
        'my_requests.html',
        {'requests': requests}
    )

def index(request):
    return render(request, 'index.html')