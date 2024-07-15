import os
from django.shortcuts import render
from openai import OpenAI
from django.contrib import messages

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_image_url(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url


def generate_image(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt')

        # Validate the prompt
        if not prompt or len(prompt) < 3:
            messages.error(
                request, 'Prompt is too short. Please enter at least 3 characters.')
            return render(request, 'generate_image/generate_image.html', {'header': "Enter your prompt below to generate an image"})

        try:
            image_url = get_image_url(prompt)
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'generate_image/generate_image.html', {'header': "Enter your prompt below to generate an image"})

        if image_url:
            return render(request, 'generate_image/generate_image.html', {'image_url': image_url, 'image_description': prompt, 'header': "Enter your prompt below to generate an image"})
        else:
            messages.error(request, 'Try again...')

    return render(request, 'generate_image/generate_image.html', {'header': "Enter your prompt below to generate an image"})


def first_page(request):
    return render(request, 'first_page.html')
