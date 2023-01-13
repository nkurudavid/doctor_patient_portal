from django.contrib import admin
from .models import (
        Speciality,
        Patient,
        Illness,
        Doctor,
        TreatmentSuggestion,
        Treatment,
        requestTimer,
    )


class SpecialityAdmin(admin.ModelAdmin):

    list_display = ('speciality_name', 'description',)
    list_filter = ('speciality_name',)
    fieldsets = (
        ('SPECIALITY DETAILS', {'fields': ('speciality_name', 'description',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('speciality_name', 'description',),
        }),
    )
    search_fields = ('speciality_name', 'description',)
    ordering = ('speciality_name', )
    filter_horizontal = ()




class PatientAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'gender', 'birthdate', 'phone', 'address', 'reg_date', )
    list_filter = ('gender', 'reg_date',)
    fieldsets = (
        ('PATIENT', {'fields': ('user',)}),
        ('PATIENT DETAILS', {'fields': ('gender', 'birthdate', 'phone', 'address',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'gender', 'birthdate', 'phone', 'address',),
        }),
    )
    search_fields = ('user', 'phone',)
    ordering = ('reg_date',)
    filter_horizontal = ()




class IllnessAdmin(admin.ModelAdmin):
    
    list_display = ('patient','description', 'status','date_created',)
    list_filter = ('status', 'date_created',)
    fieldsets = (
        ('TREATMENT REQUEST DETAILS', {'fields': ('patient','description', 'status',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('patient', 'description', 'status',),
        }),
    )
    search_fields = ('patient', 'description',)
    ordering = ('date_created',)
    filter_horizontal = ()



class DoctorAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'speciality', 'employ_id', 'phone', 'gender', 'image',)
    list_filter = ('speciality', 'gender', 'reg_date',)
    fieldsets = (
        ('DOCTOR', {'fields': ('user',)}),
        ('DOCTOR DETAILS', {'fields': ('speciality', 'employ_id', 'phone', 'gender', )}),
        ('IMAGE', {'fields': ('doc_image',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'speciality', 'employ_id', 'phone', 'gender', 'doc_image',),
        }),
    )
    search_fields = ('user','employ_id', 'phone',)
    ordering = ('reg_date',)
    filter_horizontal = ()



class TreatmentSuggestionAdmin(admin.ModelAdmin):
    
    list_display = ('illness', 'doctor', 'suggestion', 'suggestionDescription', 'sugg_dated',)
    list_filter = ('doctor','sugg_dated',)
    fieldsets = (
        ('DOCTOR INFORMATION', {'fields': ('doctor',)}),
        ('TREATMENT REQUEST', {'fields': ('illness',)}),
        ('SUGGESTION DETAILS', {'fields': ('suggestion', 'suggestionDescription',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('illness', 'doctor', 'suggestion', 'suggestionDescription',),
        }),
    )
    search_fields = ('illness', 'doctor', 'sugg_dated',)
    ordering = ('sugg_dated',)
    filter_horizontal = ()




class TreatmentAdmin(admin.ModelAdmin):
    
    list_display = ('illness', 'description', 'date_confirmed',)
    list_filter = ('date_confirmed',)
    fieldsets = (
        ('TREATMENT REQUEST', {'fields': ('illness',)}),
        ('TREATMENT DETAILS', {'fields': ('description', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('illness', 'description',),
        }),
    )
    search_fields = ('illness', 'description', 'date_confirmed',)
    ordering = ('date_confirmed',)
    filter_horizontal = ()




class requestTimerAdmin(admin.ModelAdmin):
    
    list_display = ('request', 'start_period', 'end_period',)
    list_filter = ('start_period', 'end_period',)
    fieldsets = (
        ('TREATMENT REQUEST', {'fields': ('request',)}),
        ('COUNTER DETAILS', {'fields': ('start_period', 'end_period',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('request', 'start_period', 'end_period',),
        }),
    )
    search_fields = ('request',)
    ordering = ('start_period',)
    filter_horizontal = ()




admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Illness, IllnessAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(TreatmentSuggestion, TreatmentSuggestionAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(requestTimer, requestTimerAdmin)