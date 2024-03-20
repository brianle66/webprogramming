# context_processors.py

def watchlist_quantity(request):
    if request.user.is_authenticated:
        currentuser = request.user
        currentuser_watchlist_items = currentuser.userwatchlist.all()
        watchlist_quantity = currentuser_watchlist_items.count()
    else:
        watchlist_quantity = 0  # If the user is not authenticated, set the quantity to 0
    return {'watchlist_quantity': watchlist_quantity}
