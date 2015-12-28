# coding=utf-8
from django import forms

class PollForm(forms.Form):
    question_text = forms.CharField(label='Question',max_length=200)
    choice_text1 = forms.CharField(label='choice1',max_length=200)
    choice_text2 = forms.CharField(label='choice2',max_length=200)
    choice_text3 = forms.CharField(label='choice3',max_length=200)



