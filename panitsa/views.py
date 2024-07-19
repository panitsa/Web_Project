from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import *
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
import os
import io
from reportlab.lib.pagesizes import  A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import datetime
from babel.dates import format_date 
import locale

locale.setlocale(locale.LC_TIME, 'th_TH.UTF-8')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
            
    return render(request, 'panitsa/signup.html',{"form":form})


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            form = AuthenticationForm()
    return render(request, 'panitsa/login_user.html', {'form': form})

    
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login_user')
def home(request):
    print(request.user.is_authenticated) 
    return render(request, 'panitsa/home.html')


def representative(request):
    representatives = Representative.objects.all().order_by('id')[:3]
    asom_representatives = Villagepublic.objects.all()[:10]
    print("Representatives:", representatives)
    print("Asom Representatives:", asom_representatives)
    return render(request, 'panitsa/representative.html', {'representatives': representatives, 'asom_representatives': asom_representatives})


def activity_news(request):
    activity_news = Activity_news.objects.all()
    return render(request, 'panitsa/activity_news.html',{'activity_news':activity_news})


def income_expenses(request):
    income_expenses = Income_expenses.objects.all()
    donations = Donation.objects.filter(approved=True) 
    return render(request, 'panitsa/income_expenses.html',{'income_expenses':income_expenses, 'donations': donations})


#admin

@login_required(login_url='admin_login')
def admin_edit(request):
    representative = Representative.objects.first()  
    villagepublic = Villagepublic.objects.first()
    activity_news = Activity_news.objects.first()
    income_expenses = Income_expenses.objects.first()
    users = User.objects.all()
    messages = ChatMessage.objects.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.is_admin = True
            new_message.save()
            return redirect('admin_edit')
    else:
        form = MessageForm()

    return render(request, 'admin/admin_edit.html', {
        'representative': representative,
        'villagepublic': villagepublic,
        'activity_news': activity_news,
        'income_expenses': income_expenses,
        'users': users,
        'messages': messages,
        'form': form
    })


# admin ของ ผู้แทนในหมู่บ้าน
#เพิ่มผู้แทนในหมู่บ้าน
def add_representative(request):
    if request.method == 'POST':
        form = RepresentativeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_edit')  
    else:
        form = RepresentativeForm()

    return render(request, 'admin/add_representative.html', {'form': form})
#แก้ไขผู้แทนในหมู่บ้าน
def edit_representative(request, representative_id=None):
    representative = get_object_or_404(Representative, id=representative_id)

    if request.method == 'POST':
        form = RepresentativeForm(request.POST, request.FILES, instance=representative)
        if form.is_valid():
            form.save()
            return redirect('admin_representatives')
    else:
        form = RepresentativeForm(instance=representative)

    return render(request, 'admin/edit_representative.html', {'representative': representative, 'form': form})
##เลือกข้อมูลที่ต้องการแก้ไขผู้แทนในหมู่บ้าน
def admin_representatives(request):
    representatives = Representative.objects.all()
    return render(request, 'admin/admin_representatives.html', {'representatives': representatives})
#ลบผู้แทนในหมู่บ้าน
def delete_representative(request, representative_id):
    representative = get_object_or_404(Representative, id=representative_id)
    representative.delete()
    return redirect('admin_representatives')


#admin ของ (อสม.)
#เพิ่ม(อสม.)
def add_villagepublic(request):
    if request.method == 'POST':
        form = VillagepublicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_edit') 
    else:
        form = VillagepublicForm()

    return render(request, 'admin/add_villagepublic.html', {'form': form})
#แก้ไข(อสม.)
def edit_villagepublic(request, villagepublic_id=None):
    villagepublic = get_object_or_404(Villagepublic, id=villagepublic_id)

    if request.method == 'POST':
        form = VillagepublicForm(request.POST, request.FILES, instance=villagepublic)
        if form.is_valid():
            form.save()
            return redirect('admin_villagepublic')
    else:
        form = VillagepublicForm(instance=villagepublic)

    return render(request, 'admin/edit_villagepublic.html', {'villagepublic': villagepublic, 'form': form})
#เลือกข้อมูลที่ต้องการแก้ไข(อสม.)
def admin_villagepublic(request):
    villagepublic = Villagepublic.objects.all()
    return render(request, 'admin/admin_villagepublic.html', {'villagepublic':villagepublic})
#ลบ(อสม.)
def delete_villagepublic(request, villagepublic_id):
    villagepublic = get_object_or_404(Villagepublic, id=villagepublic_id)
    villagepublic.delete()
    return redirect('admin_villagepublic')

#admin ของ ข่าวสารกิจกรรม
#เพิ่ม
def add_activity_news(request):
    if request.method == 'POST':
        form = Activity_newsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_edit')
    else:
        form = Activity_newsForm()

    return render(request, 'admin/add_activity_news.html',  {'form': form})
# แก้ไข
def edit_activity_news(request, activity_news_id=None):
    activity_news = get_object_or_404(Activity_news, id=activity_news_id)

    if request.method == 'POST':
        form = Activity_newsForm(request.POST, request.FILES, instance=activity_news)
        if form.is_valid():
            form.save()
            return redirect('admin_edit')  
    else:
        form = Activity_newsForm(instance=activity_news)

    return render(request, 'admin/edit_activity_news.html', {'activity_news': activity_news, 'form': form})
# เลือกหัวข้อข่าวสาร
def admin_activity_news(request):
    activity_news = Activity_news.objects.all()
    return render(request, 'admin/admin_activity_news.html', {'activity_news':activity_news})
# ลบ 
def delete_activity_news(request, activity_news_id):
    activity_news = get_object_or_404(Activity_news, id=activity_news_id)
    activity_news.delete()
    return redirect('admin_activity_news')

#admin ของ รายรับรายจ่าย
# เพิ่ม
def add_income_expenses(request):
    if request.method == 'POST':
        form = Income_expensesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_edit')  
    else:
        form = Income_expensesForm()

    return render(request, 'admin/add_income_expenses.html',{'form': form})
#แก้ไข
def edit_income_expenses(request, income_expenses_id=None):
    income_expenses_ = get_object_or_404(Income_expenses, id=income_expenses_id)
    
    if request.method == 'POST':
        form = Income_expensesForm(request.POST, request.FILES, instance=income_expenses_)
        if form.is_valid():
            form.save()
            return redirect('admin_edit')
    else:
        form = Income_expensesForm(instance=income_expenses_)

    return render(request, 'admin/edit_income_expenses.html', {'income_expenses': income_expenses_,'form': form})
# เลือกรายรับรายจ่าย
def admin_income_expenses(request):
    income_expenses = Income_expenses.objects.all()
    return render(request, 'admin/admin_income_expenses.html', {'income_expenses':income_expenses})
# ลบ
def delete_income_expenses(request, income_expenses_id):
    income_expenses = get_object_or_404(Income_expenses, id=income_expenses_id)
    income_expenses.delete()
    return redirect('admin_income_expenses')



@login_required(login_url='login_user')
def chat_report(request): 
    if request.method == 'POST':
        category = request.POST.get('category')
        
        if category == 'road':
            return redirect('road_chat')
        elif category == 'water':
            return redirect('water_chat')
        elif category == 'electricity':
            return redirect('electricity_chat')
        elif category == 'general':
            return redirect('general_chat')
        
    return render(request, 'panitsa/chat_report.html')


@login_required(login_url='login_user')
def road_chat(request):
    user = request.user
    messages = ChatMessage.objects.filter(category='road', user=user).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.admin_message = False
            new_message.category = 'road'
            new_message.save()
            return redirect('road_chat')
    else:
        form = MessageForm()
    
    return render(request, 'panitsa/road_chat.html', {'form': form, 'messages': messages})


@login_required(login_url='login_user')
def water_chat(request):
    user = request.user
    messages = ChatMessage.objects.filter(category='water', user=user).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.admin_message = False
            new_message.category = 'water'  
            new_message.save()
            return redirect('water_chat')
    else:
        form = MessageForm()

    return render(request, 'panitsa/water_chat.html', {'form': form, 'messages':messages})


@login_required(login_url='login_user')
def electricity_chat(request):
    user = request.user
    messages = ChatMessage.objects.filter(category='electricity', user=user).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.admin_message = False
            new_message.category = 'electricity' 
            new_message.save()
            return redirect('electricity_chat')
    else:
        form = MessageForm()

    return render(request, 'panitsa/electricity_chat.html', {'form': form, 'messages': messages})


@login_required(login_url='login_user')
def general_chat(request):
    user = request.user
    messages = ChatMessage.objects.filter( category='general', user=user).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.admin_message = False
            new_message.category = 'general'  
            new_message.save()
            return redirect('general_chat')
    else:
        form = MessageForm()

    return render(request, 'panitsa/general_chat.html', {'form': form, 'messages': messages})



@login_required(login_url='admin_login')
def admin_user_list(request):
    # ดึงข้อมูลผู้ใช้ที่มีการแชท
    active_users = User.objects.filter(chatmessage__isnull=False).distinct()
    

    return render(request, 'admin/user_list.html', {'users': active_users})

@login_required(login_url='admin_login')
def admin_road_chat(request, user_id):
    user = User.objects.get(id=user_id)
    messages = ChatMessage.objects.filter(user=user, category='road').order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = user
            new_message.admin_message = True
            new_message.category = 'road'
            new_message.save()
            return redirect('admin_road_chat', user_id=user.id)
    else:
        form = MessageForm()

    return render(request, 'admin/admin_road_chat.html', {
        'messages': messages,
        'form': form,
        'user': user
    })

@login_required(login_url='admin_login')
def admin_water_chat(request, user_id):
    user = User.objects.get(id=user_id)
    messages = ChatMessage.objects.filter(user=user, category='water').order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = user  
            new_message.admin_message = True
            new_message.category = 'water'
            new_message.save()
            return redirect('admin_water_chat', user_id=user.id)
    else:
        form = MessageForm()

    return render(request, 'admin/admin_water_chat.html', {
        'messages': messages,
        'form': form,
        'user': user  
    })



@login_required(login_url='admin_login')
def admin_electricity_chat(request, user_id):
    user = User.objects.get(id=user_id)
    messages = ChatMessage.objects.filter(user=user, category='electricity').order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = user  
            new_message.admin_message = True
            new_message.category = 'electricity'
            new_message.save()
            return redirect('admin_electricity_chat', user_id=user.id)
    else:
        form = MessageForm()

    return render(request, 'admin/admin_electricity_chat.html', {
        'messages': messages,
        'form': form,
        'user': user  
    })

@login_required(login_url='admin_login')
def admin_general_chat(request, user_id):
    user = User.objects.get(id=user_id)
    messages = ChatMessage.objects.filter(user=user, category='general').order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = user  
            new_message.admin_message = True
            new_message.category = 'general'
            new_message.save()
            return redirect('admin_general_chat', user_id=user.id)
    else:
        form = MessageForm()

    return render(request, 'admin/admin_general_chat.html', {
        'messages': messages,
        'form': form,
        'user': user  
    })



def donation_form(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.save()
            return redirect('thank_you_page', donation_id=donation.id)
    else:
        form = DonationForm()
    
    return render(request, 'panitsa/donation_form.html', {'form': form})

def admin_dashboard(request):
    donations = Donation.objects.filter(approved=False, rejected=False)
    return render(request, 'admin/donation_approval.html', {'donations': donations})

def approve_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.approved = True
    donation.rejected = False
    donation.save()
    return redirect('admin_dashboard')

def reject_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.approved = False
    donation.rejected = True
    donation.save()
    return redirect('admin_dashboard')

def generate_donation_pdf(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="donation_{donation_id}.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    font_path = os.path.join(settings.STATIC_ROOT, "fonts", "Sarabun-Bold.ttf")
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Sarabun', font_path))
        p.setFont("Sarabun", 16)
    else:
        p.setFont("Helvetica", 16)

    p.drawString(100, 800, "แบบฟอร์มการรับเงินบริจาค")
    p.drawString(100, 780, f"วันที่: {donation.date.strftime('%d/%m/%Y')}")
    p.drawString(100, 760, f"เรื่อง: {donation.subject}")
    p.drawString(100, 740, f"ชื่อ-สกุล: {donation.name}")
    p.drawString(100, 720, f"ที่อยู่: {donation.address}")
    p.drawString(100, 700, f"เบอร์โทร: {donation.phone}")
    p.drawString(100, 680, f"จำนวน: {donation.amount}")
    p.drawString(100, 660, f"จำนวนเงิน (ตัวอักษร): {donation.amount_text}")
    p.drawString(100, 640, f"ประเภทการบริจาค: โอนผ่านธนาคาร")

    bank_name = "ธนาคารกรุงไทย"
    bank_account_number = "123-456-7890"
    p.drawString(100, 620, f"ชื่อธนาคาร: {bank_name}")
    p.drawString(100, 600, f"เลขบัญชี: {bank_account_number}")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def thank_you_page(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    
    return render(request, 'panitsa/thank_you_page.html', {'donation': donation})

def admin_monthly_summary(request):
    income_expenses_summary = Income_expenses.objects.all().order_by('date')
    donation_summary = Donation.objects.filter(approved=True).order_by('date')

    for entry in income_expenses_summary:
        entry.formatted_date = format_date(entry.date, format='d MMMM yyyy', locale='th')
    for donation in donation_summary:
        donation.formatted_date = format_date(donation.date, format='d MMMM yyyy', locale='th')

    return render(request, 'admin/monthly_summary.html', {
        'income_expenses_summary': income_expenses_summary,
        'donation_summary': donation_summary
    })
    
def user_monthly_summary(request):
    income_expenses_summary = Income_expenses.objects.all().order_by('date')
    donation_summary = Donation.objects.filter(approved=True).order_by('date')

    for entry in income_expenses_summary:
        entry.formatted_date = format_date(entry.date, format='d MMMM yyyy', locale='th')
    for donation in donation_summary:
        donation.formatted_date = format_date(donation.date, format='d MMMM yyyy', locale='th')

    return render(request, 'panitsa/monthly_summary.html', {
        'income_expenses_summary': income_expenses_summary,
        'donation_summary': donation_summary
    })