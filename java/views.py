import subprocess
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

class CalculatorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'calculator.html')

    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')

        # Run the Java program as a subprocess
        result = subprocess.run(
            ['java', 'Calculator'],
            input=f"{operation} {num1} {num2}",
            capture_output=True,
            text=True,
            cwd='static/java'  # Specify the working directory
        )
        output = result.stdout.strip()  # Capture and strip the output
        return render(request, 'calculator.html', {'result': output})