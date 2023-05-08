from django.shortcuts import render, redirect
from users.models import User, UserVerificationRecord
from django.db.models import Count

def verify_users(request, message=None):
    if request.method == 'GET':
        print(request.__dict__)
        context = {'users': User.objects.annotate(num_records=Count('userverificationrecord')).filter(num_records__gte=1)}
        if message == 'verified':
            context['message'] = 'User has been verified successfully'
        elif message == 'deleted':
            context['message'] = 'Record has been deleted successfully'
        return render(request, 'panel/verify_users.html', context)
    
def user_verification_record_view(request, pk):
    if request.method == 'GET':
        context = {'records': UserVerificationRecord.objects.filter(user=pk)}
        return render(request, 'panel/user_verification_records.html', context)
    
def verification_record_view(request, pk):
    if request.method == 'GET':
        context = {'record': UserVerificationRecord.objects.filter(id=pk).first()}
        return render(request, 'panel/verification_record.html', context)

def verify_user_confirm(request, pk):
    if request.method == 'POST':
        user = User.objects.filter(id=pk).first()
        user.profile.isVerified = True
        user.profile.save()
        records =  UserVerificationRecord.objects.filter(user=pk)
        for record in records:
            record.delete()
        return redirect(verify_users, message='verified')

def verify_user_delete(request, pk):
    record =  UserVerificationRecord.objects.filter(id=pk).first()
    record.delete()
    return redirect(verify_users, message='deleted')