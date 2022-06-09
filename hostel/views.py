from email.policy import default
from django.forms import NullBooleanField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from hostel.models import Cust_details, activity_log, Hostel_detail
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import F


# Create your views here.


def index(request):
    
    
    hstl = Hostel_detail.objects.all()
    if request.method=='POST':
        hs_id = request.POST.get('hs_id')
        
        
        return redirect('booking')

    if request.method == 'GET':
        adrs = request.GET.get('place')
        price = request.GET.get('price')
        if  adrs is not None and price is not None: 
            hstl = Hostel_detail.objects.filter(street__icontains=adrs, ppm__lte = price)
            pass
        else:
            params ={'hstl' : hstl} 
  
   
    
    params = {'hstl': hstl}
    return render(request, 'index.html', params)
   

def about(request):
    """send_mail(
        'Hello',
        "comment tu vas?", 
        "domitory.8055@gmail.com",
        ['devrajdora445@gmail.com'],
        fail_silently=False,
        )"""
    return render(request, 'about.html')







# Registration Start from here
# first one is for Owner
# second one is for user


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username already Exist')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email already Exist')
                return redirect('register')

            else:
                user = User.objects.create_user(username = username, password = password1,  email = email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'Created')
                return redirect('register')
        else:
            messages.info(request, 'Password is not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')

def cust_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        dob = request.POST['dob']
        address = request.POST['address']
        city = request.POST['city']
        pin_code = request.POST['pin_code']
        if len(request.FILES) != 0:
            id_proof = request.FILES['id_proof']
        profile_pic = request.FILES['profile_pic']

        if password1 == password2:
            if Cust_details.objects.filter(username = username).exists():
                messages.info(request, 'Username already Exist')
                return redirect('cust_register')
            elif Cust_details.objects.filter(email = email).exists():
                messages.info(request, 'Email already Exist')
                return redirect('cust_register')
            else:
                
                cust = Cust_details(first_name=first_name, last_name=last_name, email=email, username=username, password = password1, phone = phone, gender = gender,dob = dob, address = address, city=city, pin_code = pin_code, id_proof=id_proof, profile_pic=profile_pic)
                cust.password = make_password(cust.password)
                
                cust.save()
                messages.info(request, 'Successfully Registerd')
                return redirect('cust_register')
        else:
            messages.info(request, 'Password is not matching')
            return redirect('cust_register')

    else:
        return render(request,'cust_register.html' )



# Login section Start from here
# first one is for Owner
# second one is for user



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['owner_id'] = user.id
            request.session['owner_usname'] = user.username
            return redirect('details/dashboard')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

    return render(request, 'login.html')



def cust_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            cust = Cust_details.objects.get(email=email)
        except:
            messages.info(request, "Password  Invalid")
            return redirect('cust_login')
        if cust:
            flag = check_password(password, cust.password)
            
            if flag:
                messages.info(request, 'Successful')

                request.session['cust'] = cust.id
                request.session['cust_fname'] = cust.first_name
                print('You are: ', request.session['cust_fname'])
                return redirect('/')
            else:
                messages.info(request, "Password  Invalid")
                return redirect('cust_login')
        else:
            messages.info(request, "Email or Password Invalid")
            return redirect('cust_login')

        

    return render(request, 'cust_login.html')


def cust_booking(request):
    if request.session.has_key('cust'):
        id = request.session['cust']
        c = Cust_details.objects.get(id =  id)
        
        a_log = activity_log.objects.filter(cust_email = c.email)
        print(a_log)
        return render(request, 'cust_booking.html', {'log': a_log})
    else:
        return render(request, 'index.html')

def cust_logout(request):
    request.session.clear()
    return redirect('cust_login')


def cust_profile(request):
    if request.session.has_key('cust'):
        id = request.session['cust']
        c = Cust_details.objects.get(id =  id)
        
        count = activity_log.objects.filter(cust_email = c.email).count()
        
        print(count)
        return render(request, 'cust_profile.html',{'cus': c, 'count': count})
    else:
        return redirect('cust_login')


def booking(request):
    if request.session.has_key('cust'):
        if request.method == 'POST':
            hs_id = request.POST.get('hs_id')
            
            hstl = Hostel_detail.objects.get(user_id=hs_id)
            id = request.session['cust']
            c = Cust_details.objects.get(id=id)
            return render(request, 'booking.html', {'hstl': hstl, 'cus': c})

    else:
        return redirect('cust_login')


def confirm(request):
    if request.session.has_key('cust'):
        if request.method == 'POST':
            cust_name = request.POST.get('cust_name')
            password = request.POST.get('password')
            cust_email = request.POST.get('cust_email')
            cust_phone = request.POST.get('cust_phone')
            check_in = request.POST.get('check_in')
            cust_id_proof = request.FILES.get('cust_id_proof')
            pos = request.POST.get('pos')

            price = request.POST.get('price')
            bed = request.POST.get('bed')
            guest = request.POST.get('guest')

            owner_name = request.POST.get('owner_uname')
            hstl_name = request.POST.get('hstl_name')
            try:
                cust = Cust_details.objects.get(email=cust_email)
            except:
                messages.info(request, "Password  Invalid")
                return redirect('booking')
            if cust:
                flag = check_password(password, cust.password)
            
                if flag:
                    messages.info(request, 'Successful')
                    a_log = activity_log(cust_name = cust_name, cust_email = cust_email, cust_phone = cust_phone, check_in = check_in, cust_id_proof = cust_id_proof, pos = pos, price = price, bed = bed, guest = guest, owner_uname = owner_name, hstl_name= hstl_name, date= datetime.today())
                    a_log.save()
                    Hostel_detail.objects.filter(username=owner_name).update(rooms_avail = F("rooms_avail") - 1  )
                    return render(request, 'confirm.html') 
                else:
                    messages.info(request, " Email or Password  Invalid")
                    return redirect('/')
        else:
            messages.info(request, " Email or Password  Invalid")
            return redirect('/')
    else:
        messages.info(request, " Email or Password  Invalid")
        return redirect('/')


# Dashboard of Owner 
# and other section 
# start form here



def dashboard(request):
    if request.session.has_key('owner_id'):
        id = request.session['owner_id']
        try:
            hstl = Hostel_detail.objects.get(user_id =  id)
            print(hstl)
            count = activity_log.objects.filter(owner_uname = hstl.username).count()
            if request.method ==  'POST':
                
                beds = request.POST['beds']
                Hostel_detail.objects.filter(user_id = id ).update(rooms_avail = beds)
                messages.info(request, 'Updated Successfully, Refresh page to see the Updated Value')
                return render(request, 'details/dashboard.html', {'hstl': hstl, 'count': count} )
            else:
            
                return render(request, 'details/dashboard.html', {'hstl': hstl, 'count': count} )

        except:
            messages.info(request, "Fill this form before procedding")
            return redirect('hstl_details')
        
        
    else:
        return redirect('login')

def logout(request):
    auth.logout(request)
    print('User log out')
    return redirect('/')

def prof_detail(request):
    if request.session.has_key('owner_id'):
        id = request.session['owner_id']
        hstl = Hostel_detail.objects.get(user_id = id)
        user = User.objects.get(id = id)
        count = activity_log.objects.filter(owner_uname = hstl.username).count()


        return render(request, 'details/prof_detail.html', {'hstl': hstl, 'user': user,'count': count })
    else:
        return redirect('login')

    


def hstl_details(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        hstl_name = request.POST['hstl_name']
        street = request.POST['street']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        city = request.POST['city']
        hstl_type = request.POST['hstl_type']
        zip = request.POST['zip']
        rooms = request.POST['rooms']
        beds = request.POST['beds']
        ppw = request.POST['ppw']
        ppm = request.POST['ppm']
        rooms_avail = request.POST['rooms_avail']
        aadhar = request.POST['aadhar']
        if len(request.FILES) != 0:
            id_proof = request.FILES['id_proof']
            image = request.FILES['image']


        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            hstl = Hostel_detail(user_id = user_id, username=username,phone = phone, hstl_name = hstl_name, street = street, latitude = latitude,longitude = longitude, city = city, hstl_type=hstl_type, zip = zip, rooms = rooms, beds=beds, ppw=ppw, ppm=ppm, rooms_avail = rooms_avail, aadhar = aadhar, id_proof = id_proof, image = image)
            hstl.save()
            return render(request, 'details/dashboard.html')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('details/hstl_details')
        
    else:

        return render(request, 'details/hstl_details.html')
   
def std_detail(request):
    if request.session.has_key('owner_id'):
        owner_id =request.session['owner_id']
        user = User.objects.get(id=owner_id)
        a_log = activity_log.objects.filter(owner_uname = user.username)

        
        return render(request, 'details/std_detail.html',{'log': a_log})
    else:
        return redirect('login')


def hstl_activity(request):
    if request.session.has_key('owner_id'):
        id = request.session['owner_id']
        user = User.objects.get(id = id)
        #hstl = Hostel_detail.objects.get(username = user.username)
        
        return render(request, 'details/hstl_activity.html')
    else:
        return render(request, 'login.html')

def update_hstl(request):
    if request.session.has_key('owner_id'):
        if request.method == 'POST':
            id = request.session['owner_id']
            
            user = User.objects.get(id = id)
            hstl = Hostel_detail.objects.get(username= user.username)
            idd = hstl.id
            print(idd)

            username = request.POST['username']
            phone = request.POST['phone']
            hstl_name = request.POST['hstl_name']
            street = request.POST['street']
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            city = request.POST['city']
            hstl_type = request.POST['hstl_type']
            zip = request.POST['zip']
            rooms = request.POST['rooms']
            beds = request.POST['beds']
            ppw = request.POST['ppw']
            ppm = request.POST['ppm']
            rooms_avail = request.POST['rooms_avail']
            aadhar = request.POST['aadhar']
            
            
            
            h = Hostel_detail(id = idd, username = username, phone = phone, hstl_name = hstl_name, street = street, latitude = latitude,longitude = longitude, city = city, hstl_type=hstl_type, zip = zip, rooms = rooms, beds=beds, ppw=ppw, ppm=ppm, rooms_avail = rooms_avail, aadhar = aadhar)
            h.save()
            messages.info(request, 'Updated Successfully')
            return render(request, 'details/hstl_activity.html')
        else:
            id = request.session['owner_id']
            user = User.objects.get(id = id)
            hstl = Hostel_detail.objects.get(username = user.username)
            
            return render(request, 'details/update_hstl.html',{'hstl':hstl})
    else:
        return redirect('login')
    