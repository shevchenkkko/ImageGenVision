import os
import requests
from django.shortcuts import render
import base64
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

api_key = os.environ.get("OPENAI_API_KEY")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_image_desc(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    json_data = response.json()

    return json_data.get("choices", [])[0].get("message", {}).get("content", [])


def describe_image(request):
    description = None
    image_path = None
    image_url = None
    if request.method == 'POST':
        if 'image' not in request.FILES or not request.FILES['image']:
            messages.error(request, 'You have not selected a file')
        else:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)

            image_path = fs.path(filename)

            image_url = fs.url(filename)
            base64_image = encode_image(image_path)
            try:
                description = get_image_desc(base64_image)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'describe_image/describe_image.html', {
        'description': description,
        'image_url': image_url,
        'header': "What's in this image?"
    })
