from django.shortcuts import render, HttpResponse
import pandas as pd, buscarf, io, datetime, hashlib

# Create your views here.
def home(request):
    if request.method == 'POST' and request.FILES['fileUpload']:
        uploaded_file = request.FILES['fileUpload']

        # Read the uploaded file into memory
        file_data = uploaded_file.read()

        # Determine the file format (assuming you can extract it from the file name)
        file_format = '.' + uploaded_file.name.split('.')[-1].lower()  # Extract extension

        # Create an in-memory file-like object from the uploaded data
        in_memory_file = io.BytesIO(file_data)

        # Process the file using your module
        processed_df = buscarf.exportar(in_memory_file, file_format)  # Pass the in-memory file

        # Create an in-memory output stream for the Excel file
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        processed_df.to_excel(writer, index=False)  # Write DataFrame to Excel
        writer.save()

        # Create the download response
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="rf_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_{hashlib.md5(processed_df.to_string().encode()).hexdigest()[:8]}.xlsx"'
        return response
    
    return render(request, "base.html")