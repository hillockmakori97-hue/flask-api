import cloudinary
import cloudinary.uploader
Cloud_name='cveyuvm6'
Api_key='922563693918987'
Secret_key='U7Odcx8EBGqS8A4fSKhYASZw5sE'
# connecting to cloudinary
cloudinary.config(
    cloud_name=Cloud_name,
    api_key=Api_key,
    api_secret=Secret_key
)
def upload_pdf(pdf_file):
    try:
        file_path=f'receipts/{pdf_file}.pdf'
        # upload pdf
        upload= cloudinary.uploader.upload(file_path,resource_type='raw')
        
        receipt_url=upload['secure_url']

        print(receipt_url)
        print("Successfull file upload")
        return 'success'
    except Exception as e:
        print(f'upload failed: {e}')
        return 'failed'