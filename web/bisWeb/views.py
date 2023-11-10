from django.shortcuts import render

# Create your views here.

def test(request):
    context = {}
    context['errorLogin'] = False
    return render(request, "test.html", context)
	
"""
class SaveWristGameData(APIView):
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, format=None):        
		username = request.data.get('username')		
		questionsAskedBlock1 = request.data.get('questionsAskedBlock1')
		questionsAskedBlock2 =request.data.get('questionsAskedBlock2')
		correctEvaluationSentence = request.data.get('correctEvaluationSentence')
		wrongEvaluationSentence = request.data.get('wrongEvaluationSentence')
		finalScore = request.data.get('finalScore')

		try:           
			newData = WristGameUserData()
			newData.questionsAskedBlock1 = questionsAskedBlock1
			newData.questionsAskedBlock2 = questionsAskedBlock2
			newData.correctEvaluationSentence = correctEvaluationSentence
			newData.wrongEvaluationSentence = wrongEvaluationSentence
			newData.finalScore = finalScore
			userData = HealthtekGameUser.objects.get(username=username)  
			newData.user = userData

			newData.save()
			
			response = HttpResponse(json.dumps({"saved": True}),content_type="application/json")  
		 
		except:
			response = HttpResponse(json.dumps({"saved": False}),content_type="application/json")         
		   
		return response    


def loginDoctorGameView(request):	
	if request.method == "GET":	
		context = {}
		context['errorLogin'] = False
		return render(request, "doctorGameLogin.html", context)
	else:
		username = request.POST.get('username')
		password = request.POST.get('password')
		hashPassword =  sha256(password.encode('utf-8')).hexdigest()
		user = HealthtekGameUser.objects.filter(username=username,password=hashPassword).first()
		if user is not None:	
			print("correct login")
			return redirect('statisticsDoctorGame',username=username)
		else:
			print("error login")		
			context = {}
			context['errorLogin'] = True
			return render(request, "doctorGameLogin.html", context)	 


"""