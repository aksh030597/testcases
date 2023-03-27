from django.http import  JsonResponse
from rest_framework.views import APIView
from .models import Student
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class StudentView(APIView):
    def get(self, request):
        try:
          queryset = Student.objects.all()
          return JsonResponse(list(queryset.values()), safe=False, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            data = {'status':'error','error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            data = {'status':'error','error_code': 101, 'message': "error: {0}".format(e)}      
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
    

       
    def post(self, request): 
        try:       
            data = {}
            data['name'] =request.POST.get('name')
            data['div'] =request.POST.get('div')
            data['mail'] =request.POST.get('mail')
            data['mobile'] =request.POST.get('mobile')
            validate_email(data['mail'])                         # Validate email field
            student = Student.objects.create(**data)
            return JsonResponse({'data':data},status=status.HTTP_201_CREATED) 
        
        except ValidationError as e:
            data = {'status':'error','error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)        

        except Exception as e:
            data = {'status':'error','error_code': 101, 'message': "error: {0}".format(e)}      
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
       
    def put(self, request, format=None):
      try:   
           data={}
           data['id'] =request.POST.get('id')
           data['name'] =request.POST.get('name')
           data['div'] =request.POST.get('div')
           data['mobile'] =request.POST.get('mobile')
           data['mail'] =request.POST.get('mail')
           validate_email(data['mail'])                             # Validate email field
           stud= Student.objects.get(id=data['id'])
           for key, value in data.items():
               setattr(stud, key, value)
           stud.save()
           #print(data['id'])
           return JsonResponse({'data':data}, status=status.HTTP_200_OK)
      
      except ValidationError as e:
            data = {'status':'error','error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)      

      except Exception as e:
            data = {'status':'error','error_code': 101, 'message': "error: {0}".format(e)}      
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:   
            data={}
            data['id'] =request.POST.get('id')
            stud= Student.objects.get(id=data['id'])
            for key in request.POST:
                if key == 'mail':
                    # validate email field
                    email = request.POST[key]
                    try:
                        validate_email(email)
                    except ValidationError as e:
                        data = {'status': 'error', 'error_code': 103, 'message': "error: {0}".format(e)}
                        return JsonResponse(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)                
                setattr(stud, key, request.POST[key])
            stud.save()
            return JsonResponse({'data':data, 'updates':key, 'status':'patched successfully'}, status=status.HTTP_200_OK)   

        except Exception as e:
            data = {'status':'error','error_code': 101, 'message': "error: {0}".format(e)}      
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,format=None):
        try:
            data={}
            data['id'] =request.POST.get('id')
            stud= Student.objects.get(id=data['id'])
            stud.delete()
            return JsonResponse({'data':'Deleted Successsfully!!'}, status=status.HTTP_204_NO_CONTENT) 
        
        except ValidationError as e:
            data = {'status':'error','error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)       

        except Exception as e:
            data = {'status':'error','error_code': 101, 'message': "error: {0}".format(e)}      
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)