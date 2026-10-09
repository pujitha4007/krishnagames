from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import random


# ==============================
# HOME
# ==============================

def home(request):
    if request.method == "POST":
        username = request.POST.get("username")

        request.session["username"] = username

        return redirect("transition")

    return render(request, "home.html")


# ==============================
# TRANSITION
# ==============================

def transition(request):
    return render(request, "transition.html")


# ==============================
# WELCOME
# ==============================

def welcome(request):
    username = request.session.get("username")

    return render(request, "welcome.html", {
        "username": username
    })


# ==============================
# GAME MENU
# ==============================

def game(request):
    return render(request, "game.html")


# ==============================
# MAKHAN HUNT
# ==============================

def makhan(request):

    if "makhan_pot" not in request.session:
        request.session["makhan_pot"] = random.randint(1, 3)
        request.session["makhan_score"] = 0

    message = ""
    game_over = False

    if request.method == "POST":

        if request.POST.get("play_again"):

            request.session["makhan_pot"] = random.randint(1, 3)

            game_over = False

        else:

            clicked_pot = int(request.POST.get("pot"))

            makhan_pot = request.session["makhan_pot"]

            if clicked_pot == makhan_pot:

                message = "🎉 Correct! You found the Makhan! 🧈"

                request.session["makhan_score"] += 1

            else:

                message = "❌ Wrong! The Makhan was in the other pot! 🧈"

                request.session["makhan_score"] = 0

            game_over = True

    score = request.session.get("makhan_score", 0)

    return render(request, "makhan.html", {
        "message": message,
        "makhan_pot": request.session["makhan_pot"],
        "game_over": game_over,
        "score": score
    })


# ==============================
# MEMORY MATCH
# ==============================

def memory(request):
    return render(request, "memory.html")


# ==============================
# EXPLORE PAGE
# ==============================

def explore(request):
    return render(request, "explore.html")


# ==============================
# UNSPLASH API
# ==============================

def explore_api(request):

    category = request.GET.get("category", "krishna")

    page = int(request.GET.get("page", 1))


    # PUT YOUR UNSPLASH ACCESS KEY HERE
    ACCESS_KEY = "B-dXLnGuE6Nenh2qiIXFZk1IOxS2DQTK8YbBuD7EMXU"


    # More specific searches for each category
    search_queries = {

        "krishna":
            "Lord Krishna Hindu deity",

        "krishna flute":
            "Lord Krishna playing flute Hindu deity",

        "bal krishna":
            "Bal Krishna Hindu deity",

        "radha krishna":
            "Radha Krishna Hindu deity",

        "krishna cows":
            "Lord Krishna with cows Hindu deity",

        "krishna crown":
            "Lord Krishna crown peacock feather Hindu deity",

        "krishna lotus":
            "Lord Krishna with lotus Hindu deity",

        "krishna peacock":
            "Lord Krishna peacock feather Hindu deity"
    }


    # Select the correct search phrase
    search_text = search_queries.get(
        category,
        "Lord Krishna Hindu deity"
    )


    # Unsplash API URL
    url = "https://api.unsplash.com/search/photos"


    # API parameters
    params = {

        "query": search_text,

        "page": page,

        "per_page": 30,

        "content_filter": "high"
    }


    # API headers
    headers = {

        "Authorization": "Client-ID " + ACCESS_KEY,

        "Accept-Version": "v1"
    }


    # Send request to Unsplash
    response = requests.get(

        url,

        params=params,

        headers=headers,

        timeout=15
    )


    # If Unsplash gives an error
    if response.status_code != 200:

        return JsonResponse({

            "status": response.status_code,

            "unsplash_error": response.text

        }, status=response.status_code)


    # Convert response to JSON
    data = response.json()


    # Store pictures
    photos = []


    # Go through every picture
    for photo in data.get("results", []):

        photos.append({

            "id": photo["id"],

            "image": photo["urls"]["regular"],

            "full_image": photo["urls"]["full"],

            "download_location":
                photo["links"].get("download_location"),

            "photographer":
                photo["user"]["name"],

            "photographer_url":
                photo["user"]["links"]["html"],

            "unsplash_url":
                photo["links"]["html"]
        })


    # Get Krishna fact
    fact = get_krishna_fact(category)


    # Send everything to Explore page
    return JsonResponse({

        "photos": photos,

        "fact": fact,

        "page": page,

        "total_pages":
            data.get("total_pages", 1)
    })


# ==============================
# KRISHNA FACTS
# ==============================

def get_krishna_fact(category):

    facts = {

        "krishna":
            "Krishna is a central figure in Hindu tradition and is known for the teachings of the Bhagavad Gita.",

        "krishna flute":
            "Krishna is traditionally depicted playing the flute, which is closely associated with his divine and joyful nature.",

        "bal krishna":
            "Bal Krishna refers to Krishna's childhood form, remembered through many playful stories from his early life.",

        "radha krishna":
            "Radha and Krishna are traditionally associated with devotion, divine love and bhakti.",

        "krishna cows":
            "Krishna is traditionally known as Govinda and Gopala, names associated with his relationship with cows and cowherds.",

        "krishna crown":
            "Krishna is often depicted wearing a crown decorated with a peacock feather.",

        "krishna lotus":
            "The lotus is an important symbol in Indian spiritual traditions and frequently appears in depictions associated with Krishna.",

        "krishna peacock":
            "The peacock feather is one of the most recognizable symbols associated with artistic depictions of Krishna."
    }


    return facts.get(
        category,
        facts["krishna"]
    )


# ==============================
# DOWNLOAD PHOTO
# ==============================

def download_photo(request):

    download_location = request.GET.get(
        "download_location"
    )


    if not download_location:

        return JsonResponse({

            "error": "Missing download location"

        }, status=400)


    # PUT THE SAME UNSPLASH ACCESS KEY HERE
    ACCESS_KEY = "B-dXLnGuE6Nenh2qiIXFZk1IOxS2DQTK8YbBuD7EMXU"


    response = requests.get(

        download_location,

        headers={

            "Authorization":
                "Client-ID " + ACCESS_KEY
        },

        timeout=15
    )


    return JsonResponse({

        "success":
            response.status_code == 200
    })