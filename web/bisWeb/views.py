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

#Utilities

def obtener_boss_item_por_nombre(nombre_item):
    try:
        nombre_item = nombre_item.lower()
        boss_item = BossItem.objects.get(name__iexact=nombre_item)
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

def getAllBossesDataInJSON():
    bosses = RaidBoss.objects.filter().all()
    serializer = RaidBossSerializer(bosses,many=True)
    jsonData = json.dumps(serializer.data)    
    
    return jsonData

def getAllItemsPickedUpDataInJSON():
    items = ItemPicked.objects.filter().all()
    serializer = ItemPickedSerializer(items,many=True)
    jsonData = json.dumps(serializer.data)    
    
    return jsonData

# Create your views here.
def bisListView(request):	
    context = {}
    if request.user.is_authenticated:
        context["logged"] = True
        context["username"] = request.user.username
    else:
        context["logged"] = False        

    context["inAdminPanel"] = False       
    context["bosses"] = getAllBossesDataInJSON()
    context["itemsPicked"] = getAllItemsPickedUpDataInJSON()
    
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
                context["bosses"] = getAllBossesDataInJSON()
                context["itemsPicked"] = getAllItemsPickedUpDataInJSON() 

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
            
            #Leemos la priemra hoja con la informacion de los jugadores
            hoja = xls.parse(xls.sheet_names[0])			

            # Leer cada columna que representa un player
            for nombreColumna in hoja.columns:
                #obtenemos o creamos el player
                nombrePlayer,correct = validataString(nombreColumna)
                if correct:                    
                    player, created = Player.objects.get_or_create(name=nombrePlayer)
                    #Clear previous items
                    player.bisItems.clear()
                    #Add new items
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
          
       
@login_required(login_url='bisListView')
def addOrUpdateItemPicked(request):	
    if request.method == 'POST':
        try:	
            playerId = request.POST.get('playerId')
            itemId = request.POST.get('itemId')
            itemLevel = request.POST.get('itemLevel')

            player = Player.objects.get(id=playerId)
            item = BossItem.objects.get(id=itemId)

            # Crear o actualizar el modelo ItemPicked
            item_picked, created = ItemPicked.objects.get_or_create(
                player=player,
                bossItem=item,
                defaults={'itemLevel': itemLevel}
            )

            # Si ya existía, actualiza el nivel del ítem
            if not created:
                item_picked.itemLevel = itemLevel
                item_picked.save()

            return HttpResponse(
                    json.dumps({"success": True,"itemsPickedJson":getAllItemsPickedUpDataInJSON()}),
                    content_type="application/json")
        except:
            return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json") 
        

@login_required(login_url='bisListView')
def removeItemPicked(request):	
    if request.method == 'POST':
        try:	
            playerId = request.POST.get('playerId')
            itemId = request.POST.get('itemId')             
            print(playerId)
            print(itemId)
            item_picked = ItemPicked.objects.get(player__id=playerId, bossItem__id=itemId)            
            # Eliminar el objeto de la base de datos
            item_picked.delete()          

            return HttpResponse(
                    json.dumps({"success": True,"itemsPickedJson":getAllItemsPickedUpDataInJSON()}),
                    content_type="application/json")
        except:
            return HttpResponse(
                json.dumps({"success": False}),
                content_type="application/json") 