from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                            widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'请输入用户名'})) 
                            #required提示  不关键
    password = forms.CharField(label='密码',
                            widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请输入密码'})) 
#widget：密文
    def clean(self):
        username = self.cleaned_data['username']#从POST中用cleaned_data['username']干净取得username数据
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)#验证
        if user is None:
            raise forms.ValidationError('用户名或密码不正确') #直接抛出错误
        self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                            max_length=30,
                            min_length=3,
                            widget=forms.TextInput(
                                        attrs={'class':'form-control','placeholder':'请输入用户名'}))
    email = forms.EmailField(label='邮箱',
                            max_length=30,
                            min_length=3,
                            widget=forms.EmailInput(
                                        attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码',
                            min_length=6,
                            widget=forms.PasswordInput(
                                        attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again = forms.CharField(label='密码',
                            min_length=6,
                            widget=forms.PasswordInput(
                                        attrs={'class':'form-control','placeholder':'再输入一次密码'})) 

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('密码已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return password_again    


    
