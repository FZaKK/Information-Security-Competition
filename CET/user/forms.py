from django import forms
from .models import Student
from django.contrib.auth.forms import PasswordChangeForm


class ModifyInfoForm(forms.Form):
    name = forms.CharField(label='姓名', max_length=100, required=False)
    school = forms.CharField(label='学校', max_length=100, required=False)
    phone = forms.CharField(label='电话', max_length=100, required=False)
    email = forms.EmailField(label='邮箱', max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        school = cleaned_data.get('school')
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')

        # 如果字段都为空，则返回原始数据
        if not name and not school and not phone and not email:
            raise forms.ValidationError("请至少填写一个字段")

        return cleaned_data


class ModifyInfoForm_tea(forms.Form):
    name = forms.CharField(label='姓名', max_length=100, required=False)
    phone = forms.CharField(label='电话', max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')
        # 如果字段都为空，则返回原始数据
        if not name and  not phone :
            raise forms.ValidationError("请至少填写一个字段")

        return cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='新密码', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)




