from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from .models import Artist, Product
from Authentication.models import User
# Create your views here.

def is_artist(user):
    return user.is_authenticated and user.role == 'artist'




@login_required(login_url='/')
@user_passes_test(is_artist)
@never_cache
def artist_dashboard(request):
    my_products = Product.objects.filter(artist__user=request.user)
    my_products_count = my_products.count()
    active_products = my_products.filter(quantity__gt=0)
    sales_count = my_products.filter(quantity__iexact=0).count()
    total_earnings = sum((float(product.price) * (1 if product.quantity == 0 else 0)) for product in my_products)   
    user = request.user
    try:
        name = Artist.objects.get(user=user)
    except Artist.DoesNotExist:
        return redirect('artist:create_artist_profile')

    # print(name)

    return render(request, "art_dashboard.html", {"artist": name, "my_products": my_products, "my_products_count": my_products_count, "active_products": active_products, "sales_count": sales_count, "total_earnings": total_earnings})

@login_required(login_url='/')
@never_cache
def artist_profile(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    user = request.user
    # print(user.role)
    # print(artist.user.id)
    # print(user.id)
    my_products = Product.objects.filter(artist=artist)
    sold_count = my_products.filter(quantity__iexact=0).count()
    my_products_count = my_products.count()
    return render(request, "artist_profile.html", {"user": user, "artist": artist, "my_products": my_products, "my_products_count": my_products_count, "sold_count": sold_count})


@login_required(login_url='/')
@user_passes_test(is_artist)
@never_cache
def create_artist_profile(request):
    # Check if artist profile already exists to prevent duplicates
    if Artist.objects.filter(user=request.user).exists():
        return redirect('artist:artist_dashboard')

    if request.method == "POST":
        user = request.user
        profile_picture = request.FILES.get('profile_picture')
        name = request.POST.get('name')
        specialty = request.POST.get('specialty')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        languages = request.POST.get('languages')
        bio = request.POST.get('bio')
        insta = request.POST.get('insta')
        twitter = request.POST.get('twitter')
        facebook = request.POST.get('facebook')
        linkedin = request.POST.get('linkedin')

        artist = Artist(
            user=user,
            profile_picture=profile_picture,
            name=name,
            specialty=specialty,
            email=email,
            phone=phone,
            location=location,
            languages=languages,
            bio=bio,
            insta=insta,
            twitter=twitter,
            facebook=facebook,
            linkedin=linkedin
        )
        artist.save()
        # Update user profile_created flag
        # We need to fetch the user again or ensure we are updating the instance
        u = User.objects.get(id=user.id)
        u.profile_created = True
        u.save()
        
        return redirect('artist:artist_dashboard')

    return render(request, "profile_edit.html")

@login_required(login_url='/')
@user_passes_test(is_artist)
@never_cache
def edit_profile(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    if artist.user != request.user:
        return redirect('artist:artist_dashboard')  # Prevent unauthorized access

    if request.method == "POST":
        # Handle profile picture update/removal
        remove_flag = request.POST.get('remove_profile_picture') == '1'
        new_picture = request.FILES.get('profile_picture')

        if remove_flag:
            # Delete the existing profile picture if it exists
            if artist.profile_picture:
                artist.profile_picture.delete(save=False)
            artist.profile_picture = None
        elif new_picture:
            # Update with new picture if provided
            artist.profile_picture = new_picture
        artist.name = request.POST.get('name', artist.name)
        artist.specialty = request.POST.get('specialty', artist.specialty)
        artist.email = request.POST.get('email', artist.email)
        artist.phone = request.POST.get('phone', artist.phone)
        artist.location = request.POST.get('location', artist.location)
        artist.languages = request.POST.get('languages', artist.languages)
        artist.bio = request.POST.get('bio', artist.bio)
        artist.insta = request.POST.get('insta', artist.insta)
        artist.twitter = request.POST.get('twitter', artist.twitter)
        artist.facebook = request.POST.get('facebook', artist.facebook)
        artist.linkedin = request.POST.get('linkedin', artist.linkedin)

        artist.save()
        return redirect('artist:artist_dashboard')  # Redirect to artist dashboard

    return render(request, "profile_edit.html", {"artist": artist})

@login_required(login_url='/')
@user_passes_test(is_artist)
def add_product(request):
    try:
        artist = Artist.objects.get(user=request.user)
    except Artist.DoesNotExist:
        return redirect('artist:create_artist_profile')

    if request.method == "POST":
        image = request.FILES.get('image')
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        medium = request.POST.get('medium')
        description = request.POST.get('description')
        year_created = request.POST.get('year_created')
        width = request.POST.get('width')
        height = request.POST.get('height')
        depth = request.POST.get('depth')
        quantity = 1
        tags_keywords = request.POST.get('tags_keywords')
        framed = bool(request.POST.get('framed'))
        signed = bool(request.POST.get('signed'))
        certificate_of_authenticity = bool(request.POST.get('certificate_of_authenticity'))
        featured = bool(request.POST.get('featured'))

        product = Product(
            artist=artist,
            image=image,
            title=title,
            price=price,
            category=category,
            medium=medium,
            description=description,
            year_created=year_created,
            width=width,
            height=height,
            depth=depth,
            quantity=quantity,
            tags_keywords=tags_keywords,
            framed=framed,
            signed=signed,
            certificate_of_authenticity=certificate_of_authenticity,
            featured=featured
        )
        product.save()
        return redirect('artist:artist_dashboard')  # Redirect to artist dashboard or another appropriate page after adding product

    return render(request, "add_pro.html")


@login_required(login_url='/')
@user_passes_test(is_artist)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.artist.user != request.user:
        return redirect('artist:artist_dashboard')  # Prevent unauthorized access

    if request.method == "POST":
        # Handle image replacement/removal:
        # - If a new file was uploaded, use it.
        # - Else if remove_image flag set, clear the image.
        # - Otherwise keep existing image.
        new_file = request.FILES.get('image')
        remove_flag = request.POST.get('remove_image') == '1'
        if new_file:
            product.image = new_file
        elif remove_flag:
            # clear the image field
            product.image.delete(save=False)
            product.image = None
        product.title = request.POST.get('title', product.title)
        product.price = request.POST.get('price', product.price)
        product.category = request.POST.get('category', product.category)
        product.medium = request.POST.get('medium', product.medium)
        product.year_created = request.POST.get('year_created', product.year_created)
        product.description = request.POST.get('description', product.description)
        product.width = request.POST.get('width', product.width)
        product.height = request.POST.get('height', product.height)
        product.depth = request.POST.get('depth', product.depth)
        product.quantity = request.POST.get('quantity', product.quantity)
        product.tags_keywords = request.POST.get('tags_keywords', product.tags_keywords)
        product.framed = bool(request.POST.get('framed', product.framed))
        product.signed = bool(request.POST.get('signed', product.signed))
        product.certificate_of_authenticity = bool(request.POST.get('certificate_of_authenticity', product.certificate_of_authenticity))
        product.featured = bool(request.POST.get('featured', product.featured))

        product.save()
        return redirect('artist:artist_dashboard')  # Redirect to artist dashboard or another appropriate page after updating product

    return render(request, "add_pro.html", {"artwork": product})

@login_required(login_url='/')
@user_passes_test(is_artist)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.artist.user != request.user:
        return redirect('artist:artist_dashboard')  # Prevent another artist to edit or delete access
    product.delete()
    return redirect('artist:artist_dashboard')  # artist daashboard