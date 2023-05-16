# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from .forms import RegisterForm , LoginForm
from argon2.exceptions import InvalidHash

# {
#     "user_id": "aaaa",
#     "user_pw": "aaaaaaaa",
#     "user_pw_confirm": "aaaaaaaa",
#     "user_name": "aa",
#     "user_email": "aaaa@example.com"
# }


@api_view(['POST'])
def user_signup(request):
    form = RegisterForm(data=request.data)
    if form.is_valid():
        user = User(
                user_id = form.user_id,
                user_pw = form.user_pw,
                user_name = form.user_name,
                user_email = form.user_email,
            ) 
        user.save()
        return Response({'message': '회원가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
    else:
        error_message = {}
        for field, errors in form.errors.items():
            error_message[field] = [error for error in errors]
        return Response({'message': '회원가입에 실패하였습니다.', 'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    form = LoginForm(data=request.data)
    if form.is_valid():
        try:
            # login(request, user)
            return Response({'message': '로그인 되었습니다.'}, status=status.HTTP_200_OK)
        except InvalidHash:
            return Response({'message': '잘못된 비밀번호 형식입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def user_login(request):
#     form = LoginForm(data=request.data)
#     if form.is_valid():
#         user = authenticate(request, username=form.cleaned_data['user_id'], password=form.cleaned_data['user_pw'])
#         if user is not None:
#             try:
#                 login(request, user)
#                 return Response({'message': '로그인 되었습니다.'}, status=status.HTTP_200_OK)
#             except InvalidHash:
#                 return Response({'message': '잘못된 비밀번호 형식입니다.'}, status=status.HTTP_400_BAD_REQUEST)
#     return Response({'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def user_login(request):
#     form = LoginForm(data=request.data)
#     if form.is_valid():
#         user = authenticate(request, username=form.cleaned_data['user_id'], password=form.cleaned_data['user_pw'])
#         if user is not None:
#             login(request, user)
#             return Response({'message': '로그인 되었습니다.'}, status=status.HTTP_200_OK)
#     return Response({'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)





# 장고
from django.shortcuts import redirect, render
from django.db import transaction
from .models import User
from argon2 import PasswordHasher
from .forms import RegisterForm , LoginForm

def register(request):
    register_form = RegisterForm()
    context = {'forms' : register_form}
    
    if request.method == 'GET' :
        return render(request, 'user/register.html',context)
    
    elif request.method == 'POST' :
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = User(
                user_id = register_form.user_id,
                user_pw = register_form.user_pw,
                user_name = register_form.user_name,
                user_email = register_form.user_email,
            ) 
            user.save()
            return redirect('/')
        else:
            context['forms'] = register_form
            if register_form.errors :
                for value in register_form.errors.values():
                    context['error'] = value
        return render(request, 'user/register.html',context)


def login(request):
    loginform = LoginForm()
    context = {'forms' : loginform}
    
    if request.method == 'GET' :
        return render(request, 'user/login.html',context)
    
    elif request.method == 'POST' :
        loginform = LoginForm(request.POST)
        if loginform.is_valid() :
            return redirect('/')
        else:
            context['forms'] = loginform
            if loginform.errors :
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'user/login.html',context)
