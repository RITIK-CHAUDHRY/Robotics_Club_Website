from django.shortcuts import render,HttpResponse,redirect
from .models import Component,Request
from .forms import ComponenentForm,UpdateComponentForm,RequestForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
# Create your views here.
def test(request,id):
    context={}
    component = Request.objects.filter(component_id=id).filter(status=0)
    othcomp = Request.objects.filter(component_id=id).filter(status=1)
    context['request'] = component
    context['approved']= othcomp
    return render(request,'component/test.html',context)

def componentlist(request):
    context = {}
    context['components'] = Component.objects.all()
    context['form'] = RequestForm()
    return render(request, 'component/component_list.html', context)

def addcomponent(request):
    context = {}
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ComponenentForm(request.POST)
            form.save()
            return redirect('component_list')
        else:
            form = ComponenentForm()
            context['form'] = form
        return render(request, 'component/component_form.html', context)
    else:
        return HttpResponse("Sorry You don't have permission :)")

def deletecomponent(request,pk):
    component=Component.objects.get(pk=pk)
    component.delete()
    return redirect('component_list')

def updatecomponent(request,pk):
    component=Component.objects.get(pk=pk)
    context = {}
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UpdateComponentForm(request.POST,instance=component)
            form.save()
            return redirect('component_list')
        else:
            form = UpdateComponentForm(instance=component)
            context['form'] = form
        return render(request, 'component/component_form.html', context)
    else:
        return HttpResponse("Sorry You don't have permission :)")

def handlerequest(request):
    context={}
    cid=request.GET.get('id')
    user=request.GET.get('user')
    type=request.GET.get('r_type')
    comp = Component.objects.get(pk=cid)
    user = User.objects.get(username__exact=user)
    req = Request.objects.get(request_user=user, component=comp)

    if type=='0': #approve
        req.status = 1
        add=req.request_num
        if add>comp.available():
            messages.success(request, "Not enough component!")
        else:
            req.save()
            comp.issued_num=comp.issued_num+add
            comp.save()
            messages.success(request, "request accepted successfully")
    elif type=='1': #reject
        req.delete()
    elif type=='2':
        add = req.request_num
        if (req.status == 1):
            comp.issued_num = comp.issued_num - add
        req.delete()
        comp.save()
    else:
        print("this should not be happening")
    context['request'] = Request.objects.filter(component=comp).filter(status=0)
    context['approved'] = Request.objects.filter(component=comp).filter(status=1)
    if request.is_ajax():
        html = render_to_string('Component/test_part.html', context, request=request)
        return JsonResponse({'html':html},status=200)
    else:
        return HttpResponse("This is unexpected :(")

def createrequest(request):
    context={}
    if request.is_ajax():
        cid=request.POST.get('cid')
        component=Component.objects.get(pk=cid)
        req_num=request.POST.get('req_num')
        if int(req_num) < 0:
            return JsonResponse({'request':'2'})
        if Request.objects.filter(request_user=request.user,component=component).exists():
            req = Request.objects.get(request_user=request.user, component=component)
            if req.status==0:
                if int(req_num) > component.available():
                    messages.success(request, "Not Enough components!")
                else:
                    req.request_num=req_num
                    req.save()
                    messages.success(request, "Request Updated Successfully!")
            else:
                messages.success(request, "Request Already Accepted!")
        elif int(req_num) > component.available():
            messages.success(request, "Not Enough Components!")
        else:
            req = Request(request_num=req_num, request_user=request.user, component=component)
            req.save()
            messages.success(request, "Request Sent Successfully!")
        html = render_to_string('spinnets/message.html', context, request=request)
        return JsonResponse({'html': html}, status=200)
    else:
        return HttpResponse("woops")