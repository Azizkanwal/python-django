from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account import views
from django.db.models import Q
import json
from django.http import JsonResponse
from hashids import Hashids
from hashid_field import HashidField
from .models import PrivacyType, PrivacyOn, UserPrivacy, BlockedUser, UserSpecificContacts
from .models import NotificationEventTypes, NotificationType, Notification
from django.shortcuts import render

"""
Method:             settingStat
Developer:          Aziz
Created Date:       06-03-2018
Purpose:            Setting data
Params:             []
Return:             []
"""
@login_required
def __settingStat(request):
    hashids = Hashids(min_length=16)
    try:
        userPrivacyOn = PrivacyOn.objects.all()
    except PrivacyOn.DoesNotExist:
        userPrivacyOn = None

    try:
        userPrivacyType = PrivacyType.objects.all()
    except PrivacyType.DoesNotExist:
        userPrivacyType = None

    try:
        privacyData = UserPrivacy.objects.filter(user_id = request.user.id)
    except UserPrivacy.DoesNotExist:
        privacyData = None

    context = {
        "privacyOn" : userPrivacyOn,
        "privacyType" : userPrivacyType,
        "userPrivacy" : privacyData,
        "notificationType" : notificationType
    }
    return context
"""end function __settingStat"""

"""
Method:             userPrivacySetting
Developer:          Aziz
Created Date:       17-04-2018
Purpose:            Getting User privacy
Params:             null
Return:             []
"""
@login_required
def userPrivacySetting(request):
    if request.method == 'GET':
        templateName = 'user_privacy_setting.html'
        currentUser = request.user
        userInfo = views.__userStats(request) #defined in accounts views.py
        settingData = __settingStat(request)

        try:
            userDetails = User.objects.filter(~Q(id = 1),~Q(id = currentUser.id))
        except User.DoesNotExist:
            userDetails = None

        userData = []
        for user in userDetails:
            listdata = (user.id,user.username)
            userData.append(listdata)
       
        userData = json.dumps(userData)
       
        context = {
            "userData": userData,
            "profile" : userInfo['profile'],
            "privacyOn" : settingData['privacyOn'],
            "privacyType" : settingData['privacyType'],
            "userPrivacy" : settingData['userPrivacy'],
            "blockUserData" : settingData['blockUserData'],
            "notificationType" : settingData['notificationType'],
            "eventType" : settingData['eventType']
        }

        return render(request, templateName, context)
    else:
        messages.warning(request, 'Please Try again')
        redirect('/')
"""end function userPrivacySetting"""

"""
Method:             addUserPrivacy
Developer:          Aziz
Created Date:       06-03-2018
Purpose:            Add user Privacy
Params:             []
Return:             []
"""

@login_required
def addUserPrivacy(request):
    if request.user.is_authenticated():
        template_name = 'user_privacy_setting.html'
        currentUser = request.user
        if request.method == 'POST':
            try:
                userPrivacyData = UserPrivacy.objects.all().filter(user_id = currentUser.id)
            except UserPrivacy.DoesNotExist:
                userPrivacyData = None
        
            if userPrivacyData is not None:
                userPrivacyData.delete()
                privacyContent = None
            else:
                privacyContent = None

            if not privacyContent :
              
                userprivacy1 = UserPrivacy()
                userprivacy1.privacyon_id = request.POST['privacy_event_type_1']
                userprivacy1.privacytype_id = request.POST['privacy_type_id_1']
                userprivacy1.user_id = currentUser.id
                userprivacy1.save()

                userprivacy2 = UserPrivacy()
                userprivacy2.privacyon_id = request.POST['privacy_event_type_2']
                userprivacy2.privacytype_id = request.POST['privacy_type_id_2']
                userprivacy2.user_id = currentUser.id
                userprivacy2.save()

                userprivacy3 = UserPrivacy()
                userprivacy3.privacyon_id = request.POST['privacy_event_type_3']
                userprivacy3.privacytype_id = request.POST['privacy_type_id_3']
                userprivacy3.user_id = currentUser.id
                userprivacy3.save()

                userprivacy4 = UserPrivacy()
                userprivacy4.privacyon_id = request.POST['privacy_event_type_4']
                userprivacy4.privacytype_id = request.POST['privacy_type_id_4']
                userprivacy4.user_id = currentUser.id
                userprivacy4.save()

                userprivacy5 = UserPrivacy()
                userprivacy5.privacyon_id = request.POST['privacy_event_type_5']
                userprivacy5.privacytype_id = request.POST['privacy_type_id_5']
                userprivacy5.user_id = currentUser.id
                userprivacy5.save()

                userprivacy6 = UserPrivacy()
                userprivacy6.privacyon_id = request.POST['privacy_event_type_6']
                userprivacy6.privacytype_id = request.POST['privacy_type_id_6']
                userprivacy6.user_id = currentUser.id
                userprivacy6.save()

            messages.success(request, 'Information has been saved successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Please try again')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')
"""end function addUserPrivacy"""


"""
Method:             addSpecificUsers
Developer:          Aziz
Created Date:       19-04-2018
Purpose:            Adding Specific user list
Params:             [request]
Return:             user data[]
"""
@login_required
def addSpecificUsers(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            userList = request.POST.getlist('user_list[]')
            for user in userList:
                if UserSpecificContacts.objects.filter(specific_user_id = user, user_id = request.user.id).exist():
                    specificUserObj = UserSpecificContacts.objects.get(specific_user_id = user)
                    specificUserObj.specific_user_id = user
                    specificUserObj.user_id = request.user.id
                    specificUserObj.save()
                else:
                    specificUser = UserSpecificContacts()
                    specificUser.specific_user_id = user
                    specificUser.user_id = request.user.id
                    specificUser.save()
            response = HttpResponse(json.dumps({'success': 'Added successfully'}),content_type='application/json')
            response.status_code = 200
            return response
"""end function addSpecificUsers"""


"""
Method:             deleteSpecificUser
Developer:          Aziz
Created Date:       19-03-2018
Purpose:            delete specific user
Params:             [id]
Return:             []
"""
@login_required
def deleteSpecificUser(request):
    if request.user.is_authenticated():
        hashids = Hashids(min_length=16)
         if request.is_ajax():
            userId = request.POST.get('user_id')
            currentUser = hashids.decode(userId)
            try:
                userData = UserSpecificContacts.objects.filter(specific_user_id = currentUser[0], user_id = request.user.id)
            except UserSpecificContacts.DoesNotExist:
                userData = None
            if userData:
                userData.delete()
            response = HttpResponse(json.dumps({'success': 'Added successfully'}),content_type='application/json')
            response.status_code = 200
            return response
        else:
            response = HttpResponse(json.dumps({'error': 'Please try Again'}),content_type='application/json')
            response.status_code = 400
            return response
"""end function deleteSpecificUser"""
