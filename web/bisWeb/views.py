from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .serializers import *
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def bisListView(request):	
    context = {}
    if request.user.is_authenticated:
        context["logged"] = True
        context["username"] = request.user.username
    else:
        context["logged"] = False        

    context["inAdminPanel"] = False    
    bosses = RaidBoss.objects.filter().all()
    serializer = RaidBossSerializer(bosses,many=True)
    jsonData = json.dumps(serializer.data)
    context["bosses"] = jsonData
    
    return render(request, "bisViewTemplate.html", context)

def loginView(request):	
    print("login")
    if request.user.is_authenticated:
        return redirect("adminView")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("adminView")
            else:
                context = {}
                context["errorLogin"] = True
                context["logged"] = False  
                context["inAdminPanel"] = False
                bosses = RaidBoss.objects.filter().all()
                serializer = RaidBossSerializer(bosses,many=True)
                jsonData = json.dumps(serializer.data)
                context["bosses"] = jsonData             
                return render(request, "bisViewTemplate.html", context)        

def logoutUser(request):	
    logout(request)
    return redirect("bisListView")

@login_required(login_url='bisListView')
def adminView(request):	
    context = {}
    context["logged"] = True
    context["username"] = request.user.username
    context["inAdminPanel"] = True 
    return render (request, "adminViewTemplate.html",context)

def obtener_boss_item_por_nombre(nombre_item):
    try:
        boss_item = BossItem.objects.get(name=nombre_item)
        existe_item = True
    except BossItem.DoesNotExist:
        boss_item = None
        existe_item = False

    return boss_item, existe_item


def validataString(value):
    try:
        if isinstance(value,str):
            cleanValue = value.strip()
            if len(cleanValue) > 0:
                return cleanValue,True
            else:
                return value,False
        else:
            return value,False
    except:
        return value,False
    

@login_required(login_url='bisListView')
def initializeDatabase(request):
    if request.method == 'POST' and request.FILES['excelFile']:
        try:
            excelFile = request.FILES['excelFile']

            # Leer el archivo Excel utilizando pandas
            xls = pd.ExcelFile(excelFile)
            #Recorrer cada hoja que representa una raid
            for hoja_nombre in xls.sheet_names:
                hoja = xls.parse(hoja_nombre)			

                # Leer cada columna que representa un boss
                for nombreColumna in hoja.columns:
                    #obtenemos o creamos el boss
                    nombreBoss,correct = validataString(nombreColumna)
                    if correct:                    
                        boss, created = RaidBoss.objects.get_or_create(name=nombreBoss)
                        columna = hoja[nombreColumna]
                        itemList = columna.tolist()

                        for item in itemList:
                            nombreItem,correct = validataString(item)
                            if correct:                                
                                item, created = BossItem.objects.get_or_create(name=nombreItem,boss=boss)		
            
            return HttpResponse(
                json.dumps({"success": True}),
                content_type="application/json") 
        except:
            return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json") 
    else:
        return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json")

 


@login_required(login_url='bisListView')
def initializePlayerItems(request):
    if request.method == 'POST' and request.FILES['excelFile']:
        try:
            excelFile = request.FILES['excelFile']

            # Leer el archivo Excel utilizando pandas
            xls = pd.ExcelFile(excelFile)
            #Recorrer cada hoja 
            for hoja_nombre in xls.sheet_names:
                hoja = xls.parse(hoja_nombre)			

                # Leer cada columna que representa un player
                for nombreColumna in hoja.columns:
                    #obtenemos o creamos el player
                    nombrePlayer,correct = validataString(nombreColumna)
                    if correct:                    
                        player, created = Player.objects.get_or_create(name=nombrePlayer)
                        columna = hoja[nombreColumna]
                        itemList = columna.tolist()

                        for item in itemList:
                            nombreItem,correct = validataString(item)
                            if correct:                               
                                boss_item, existe_item = obtener_boss_item_por_nombre(nombreItem)	
                                if existe_item:
                                    player.bisItems.add(boss_item)
            
            return HttpResponse(
                json.dumps({"success": True}),
                content_type="application/json") 
        except:
            return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json")
    else:
        return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json")




@login_required(login_url='bisListView')
def cleanDatabase(request):	
    if request.method == 'POST':	
        try:
            Player.objects.all().delete()
            RaidBoss.objects.all().delete()

            return HttpResponse(
                json.dumps({"success": True}),
                content_type="application/json") 
        except:
            return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json") 
          
       
