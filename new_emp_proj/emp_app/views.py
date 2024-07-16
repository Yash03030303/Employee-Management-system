from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index (request):
    return render(request, "index.html")

def all_emp (request):
    emps= Employee.objects.all()
    context={
        "emps" : emps
    }
    print(context)
    return render(request, "view_all_emp.html", context)

def add_emp(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        role_id = int(request.POST["role"])
        phone = int(request.POST["phone"])
        dept_id = int(request.POST["dept"])
        salary = int(request.POST["salary"])
        bonus = int(request.POST["bonus"])

        # Retrieve the department and role objects
        try:
            dept = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
        except Department.DoesNotExist:
            return HttpResponse("Invalid Department ID")
        except Role.DoesNotExist:
            return HttpResponse("Invalid Role ID")

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=dept,
            role=role,
            join_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse("Employee is successfully added")

    elif request.method == "GET":
        roles = Role.objects.all()
        departments = Department.objects.all()
        return render(request, "add_emp.html", {'roles': roles, 'departments': departments})
    
    else:
        return HttpResponse("Exception Occurred! Employee is not added")


def remove_emp (request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id = emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee is removed Successfully")
            
        except:
            return HttpResponse("Please Enter valid employee id")
    emps = Employee.objects.all()
    context = {
        "emps" : emps
    }
    return render(request, "remove_emp.html", context)

def filter_emp (request):
    if request.method == "POST":
        name = request.POST["name"]
        dept = request.POST["dept"]
        role = request.POST["role"]
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            "emps" : emps
        }
        return render(request, "view_all_emp.html", context)
    
    elif request.method == "GET":
        return render(request, "filter_emp.html")
    
    else:
        return HttpResponse("Exception Occured")
    
def login (request):
    return render(request, "login.html")