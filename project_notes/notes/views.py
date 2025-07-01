from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth, messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .models import *
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.timezone import now
import markdown
from django.utils.safestring import mark_safe
import re
import json
from django.utils.html import strip_tags


# Configure Gemini API
import google.generativeai as genai
import os
from dotenv import load_dotenv


# Configure OpenAI API
# import openai

# =================================================================



# Create your views here.


# Register Page
def register(request):
    context = {}
    return render(request,'notes/register.html',context)


# Login Page
def login(request):
    context = {}
    return render(request,'notes/login.html',context)


# Display all notes with search functionality
@login_required
def index(request):
    query = request.GET.get('query', '')
    user_id = request.user.id

    if query:
        notes = Note.objects.filter(user_id=user_id).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        notes = Note.objects.filter(user_id=user_id)

    context = {'notes': notes, 'query': query}
    return render(request, 'notes/index.html', context)


# Store Register Data
def store(request):
    # auth_user
    myfname     = request.POST['fname']
    mylname     = request.POST['lname']
    myemail     = request.POST['email']
    myusername  = request.POST['username']
    mypassword  = request.POST['password']
    mycpassword = request.POST['cpassword']

    #profile
    mycontact   = request.POST['contact']

    if mypassword == mycpassword:
        result = User.objects.create_user(first_name=myfname,
            last_name=mylname,
            email=myemail,
            username=myusername,
            password=mypassword)
        Profile.objects.create(contact=mycontact,user_id=result.id)
        return redirect('/notes/login')
    else:
        messages.success(request, "Missmatch Password")
        return redirect('/notes/register')

# Update Profile
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        fname    = request.POST.get("fname").strip()
        lname    = request.POST.get("lname").strip()
        email    = request.POST.get("email").strip()
        username = request.POST.get("username").strip()
        contact  = request.POST.get("contact").strip()
        new_password = request.POST.get("new_password", "").strip()

        # Validate Input
        if not fname or not lname or not email or not username or not contact:
            messages.error(request, " All fields except password are required!")
            return redirect("update_profile")

        # Check if email or username already exists (excluding current user)
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, " This email is already in use!")
            return redirect("update_profile")

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, " This username is already taken!")
            return redirect("update_profile")

        # Update user details
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.username = username
        if new_password:
            user.set_password(new_password)  # Hash password before saving

        user.save()

        # Update Profile
        profile.contact = contact
        profile.save()

        messages.success(request, " Profile updated successfully!")
        return redirect("index")

    return render(request, "notes/edit_profile.html", {"user": user, "profile": profile})

# def index(request):
#     user_id = request.user.id
#     profile = Profile.objects.get(user_id=user_id)
#     context = {'profile':profile}
#     return render(request,'notes/index.html',context)


def login_check(request):
    myusername = request.POST['username']
    mypassword = request.POST['password']

    result = auth.authenticate(username=myusername,password=mypassword)
    if result is None:
        messages.success(request, "Invalid Username or Password")
        return redirect('/notes/login')
    else:
        auth.login(request,result)
        return redirect('/notes/index')


# Feedback
@login_required
def feedback(request):
    return render(request, 'notes/feedback.html')

@login_required
def feedback_store(request):
    if request.method == "POST":
        rating = request.POST.get("rating", "").strip()
        comment = request.POST.get("comment", "").strip()

        if not rating or not comment:
            messages.error(request, " Please provide both a rating and a comment!")
            return redirect("feedback")

        try:
            Feedback.objects.create(
                rating=rating,
                comment=comment,
                user=request.user
            )
            messages.success(request, " Thank you for your feedback! ")
        except Exception as e:
            messages.error(request, f" Error submitting feedback: {str(e)}")

    return redirect("feedback")

# def update_password(request):
#     context = {}
#     return render(request,'notes/update_password.html',context)


@login_required
def update_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password     = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, " Current password is incorrect!")
            return redirect("update_password")

        if new_password != confirm_password:
            messages.error(request, " New passwords do not match!")
            return redirect("update_password")

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, " Password updated successfully!")
        return redirect("update_password")

    return render(request, "notes/update_password.html")




def logout(request):
    auth.logout(request)
    return redirect('/notes/login')

# ==================================================================================

# def filter_notes(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         filter_type = data.get("filter_type")
#         filter_value = data.get("filter_value")

#         # Start filtering
#         received_notes = SentNote.objects.filter(receiver=request.user)

#         if filter_type == "tags":
#             received_notes = received_notes.filter(note__tags__icontains=filter_value)
#         elif filter_type == "date":
#             received_notes = received_notes.filter(sent_at__date=filter_value)
#         elif filter_type == "type":
#             received_notes = received_notes.filter(note__note_type__icontains=filter_value)
#         elif filter_type == "sort":
#             if filter_value.lower() == "newest":
#                 received_notes = received_notes.order_by("-sent_at")
#             elif filter_value.lower() == "oldest":
#                 received_notes = received_notes.order_by("sent_at")

#         # Render filtered notes as HTML
#         html = render(request, "notes/partials/note_list.html", {"received_notes": received_notes}).content.decode("utf-8")
        
#         return JsonResponse({"success": True, "html": html})

#     return JsonResponse({"success": False})

# ==================================================================================

# Create a new note
@login_required
def create_note(request):
    if request.method == 'POST':
        title   = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user=request.user)
        messages.success(request, "Note created successfully!")
        return redirect('index')
    
    return render(request, 'notes/create_note.html')


# View a specific note
@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    context = {'note': note}
    return render(request, 'notes/note_detail.html', context)


# Update an existing note
# @login_required
# def update_note(request, pk):
#     note = get_object_or_404(Note, pk=pk, user=request.user)

#     if request.method == 'POST':
#         note.title   = request.POST['title']
#         note.content = request.POST['content']
#         note.save()
#         messages.success(request, "Note updated successfully!")
#         return redirect('note_detail', pk=note.pk)
    
#     context = {'note': note}
#     return render(request, 'notes/update_note.html', context)


@login_required
def update_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title or not content:
            messages.error(request, "Title and content cannot be empty!")
            return redirect('update_note', pk=pk)

        note.title = title
        note.content = content  # Store as HTML (Quill.js gives HTML)
        note.save()

        messages.success(request, "Note updated successfully! ")
        return redirect('note_detail', pk=note.pk)

    #  Fixed Markdown conversion issue
    note.content = mark_safe(markdown.markdown(note.content))  

    return render(request, 'notes/update_note.html', {'note': note})




@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    plain_text_content = markdown_to_plain_text(note.content)  # Convert to clean text

    if request.method == 'POST':
        note.delete()
        messages.success(request, "Note deleted successfully!")
        return redirect('index')

    context = {'note': note, 'plain_text_content': plain_text_content}
    return render(request, 'notes/delete_confirm.html', context)



# Markdown
def markdown_to_plain_text(md_text):
    md_text = markdown.markdown(md_text)
    plain_text = strip_tags(md_text)
    plain_text = re.sub(r"\n\s*\n", "\n", plain_text)
    return plain_text.strip()


# Download note
def download_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    plain_text_content = markdown_to_plain_text(note.content)
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename=\"{note.title}.txt\"'
    response.write(f"Title: {note.title}\n\n{plain_text_content}")
    return response


# AJAX search for notes
@login_required
def search_notes(request):
    query   = request.GET.get('query', '')  # Get search term
    user_id = request.user.id

    # Filter notes based on query (title or content)
    notes = Note.objects.filter(user_id=user_id).filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )

    # Convert queryset to JSON response
    results = [
        {
            'id': note.id,
            'title': note.title,
            'updated_at': note.updated_at.strftime('%b %d, %Y')
        }
        for note in notes
    ]

    return JsonResponse({'notes': results})




# ========================================================================================



# Load OpenAI API Key from .env
# openai.api_key = os.getenv("OPENAI_API_KEY")

# @login_required
# def generate_note(request):
#     if request.method == "POST":
#         topic = request.POST.get("topic", "").strip()
#         prompt = request.POST.get("prompt", "").strip()

#         if not topic or not prompt:
#             messages.error(request, "Both topic and prompt are required!")
#             return redirect("generate_note")

#         try:
#             client = openai.OpenAI()  # Correct way to initialize OpenAI in v1.0+
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful AI assistant that generates structured notes."},
#                     {"role": "user", "content": f"Write a detailed and structured note about {topic}. {prompt}"}
#                 ]
#             )

#             content = response.choices[0].message.content  # Correct way to access response text

#         except Exception as e:
#             content = f"Error: {str(e)}"

#         # Save AI-generated note
#         note = Note.objects.create(
#             title=topic,
#             content=content,
#             user=request.user,
#             created_at=now(),
#             updated_at=now()
#         )

#         messages.success(request, "AI-generated note successfully created!")
#         return redirect("note_detail", pk=note.pk)

#     return render(request, "notes/generate_note.html")


# ========================================================================================

# GEMINI
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@login_required
def generate_note(request):
    if request.method == "POST":
        topic = request.POST.get("topic", "").strip()
        prompt = request.POST.get("prompt", "").strip()

        if not topic or not prompt:
            messages.error(request, "Both topic and prompt are required!")
            return redirect("generate_note")

        try:
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(f"Write a structured note about {topic}. {prompt}")

            if response and hasattr(response, "text"):
                content = response.text
            else:
                content = " AI couldn't generate content. Please try again with a different topic."

        except Exception as e:
            content = f" Error: {str(e)}"

        # Save AI-generated note
        note = Note.objects.create(
            title=topic,
            content=content,
            user=request.user,
            created_at=now(),
            updated_at=now()
        )

        messages.success(request, " AI-generated note successfully created!")
        return redirect("note_detail", pk=note.pk)

    return render(request, "notes/generate_note.html")


# ============================

@login_required
def send_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "POST":
        receiver_username = request.POST.get("receiver").strip()
        try:
            receiver = User.objects.get(username=receiver_username)
            SentNote.objects.create(sender=request.user, receiver=receiver, note=note)
            messages.success(request, f" Note sent to {receiver.username}!")
        except User.DoesNotExist:
            messages.error(request, "User not found!")

    return redirect("note_detail", pk=pk)

@login_required
def inbox(request):
    received_notes = SentNote.objects.filter(receiver=request.user).order_by("-sent_at")
    return render(request, "notes/inbox.html", {"received_notes": received_notes})

@login_required
def sent_notes(request):
    sent_notes = SentNote.objects.filter(sender=request.user).order_by("-sent_at")
    return render(request, "notes/sent_notes.html", {"sent_notes": sent_notes})

@login_required
def view_received_note(request, pk):
    sent_note = get_object_or_404(SentNote, pk=pk, receiver=request.user)
    return render(request, "notes/view_received_note.html", {"sent_note": sent_note})

@login_required
def delete_received_note(request, pk):
    sent_note = get_object_or_404(SentNote, pk=pk, receiver=request.user)

    if request.method == "POST":
        sent_note.delete()
        messages.success(request, " Note deleted successfully!")
        return redirect("inbox")

    return render(request, "notes/delete_received_note.html", {"sent_note": sent_note})

# =========

def send_note_page(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, "notes/send_note.html", {"note": note})

# Handles note to another user
@login_required
def send_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "POST":
        receiver_username = request.POST.get("receiver").strip()

        try:
            receiver = User.objects.get(username=receiver_username)
            SentNote.objects.create(sender=request.user, receiver=receiver, note=note)
            messages.success(request, f" Note successfully sent to {receiver.username}!")
            return redirect("note_detail", pk=pk)
        except User.DoesNotExist:
            messages.error(request, " User not found!")

    return redirect("send_note_page", pk=pk)