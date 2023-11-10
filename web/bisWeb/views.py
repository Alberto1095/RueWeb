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
# Create your views here.
def test(request):
	context = {}
	context['errorLogin'] = False
	return render(request, "test.html", context)
	

def loginView(request):	
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
				return render(request, "login.html", context)
		context = {}
		context["errorLogin"] = False
		return render(request, "login.html", context)

def logoutUser(request):	
	logout(request)
	return redirect("bisListView")

@login_required(login_url='login')
def adminView(request):		
	return render (request, "adminViewTemplate.html")

def obtener_boss_item_por_nombre(nombre_item):
	try:
		boss_item = BossItem.objects.get(name=nombre_item)
		existe_item = True
	except BossItem.DoesNotExist:
		boss_item = None
		existe_item = False

	return boss_item, existe_item

@login_required(login_url='login')
def addItemsToPlayer(request):	
	if request.method == 'POST':  
		added = True
	
		playerName = request.POST.get('playerName')    
		cleanPlayerName = playerName.strip()

		player, created = Player.objects.get_or_create(name=cleanPlayerName)

		listItemsString = request.POST.get('listItems')     
		listItems = listItemsString.splitlines()
		player.bisItems.clear()

		for item in listItems:
			boss_item, existe_item = obtener_boss_item_por_nombre(item)
			if existe_item:
				player.bisItems.add(boss_item)
			else:
				added = False

		player.save()

		context = {
			'addedItemsCorrectly': added,            
		}
		return render(request, "adminViewTemplate.html", context)

	return render (request, "adminViewTemplate.html")



@csrf_exempt
def initializeDatabase(request):
	if request.method == 'POST' and request.FILES['excelFile']:
		excelFile = request.FILES['excelFile']

		# Leer el archivo Excel utilizando pandas
		xls = pd.ExcelFile(excelFile)
		#Recorrer cada hoja que representa una raid
		for hoja_nombre in xls.sheet_names:
			hoja = xls.parse(hoja_nombre)		
			#Crear u obtener la raid si ya existe
			nombreRaid = hoja_nombre.strip()
			print(nombreRaid)
			raid, created = Raid.objects.get_or_create(name=nombreRaid)

			# Leer cada columna que representa un boss
			for nombreColumna in hoja.columns:
				#obtenemos o creamos el boss
				nombreBoss = nombreColumna.strip()
				print(nombreBoss)
				boss, created = RaidBoss.objects.get_or_create(name=nombreBoss,raid=raid)
				columna = hoja[nombreColumna]
				itemList = columna.tolist()

				for item in itemList:
					if isinstance(item,str):
						itemName = item.strip()
						item, created = BossItem.objects.get_or_create(name=itemName,boss=boss)		
		
		return HttpResponse("Initialized")
 

def raidListView(request):	
	context = {}	
	raid = Raid.objects.all()	
	serializer = RaidSerializer(raid,many=True)
	context["raid"] = serializer.data

	return JsonResponse(serializer.data, safe=False)
	#return render (request, "raidListViewTemplate.html",context)

def bisListView(request,raidID):	
	context = {}	
	raid = Raid.objects.filter(pk=raidID).first()
	bosses = RaidBoss.objects.filter(raid=raid).all()
	serializer = RaidBossSerializer(bosses,many=True)
	context["bosses"] = serializer.data

	return JsonResponse(serializer.data, safe=False)
	#return render (request, "bisListViewTemplate.html",context)

