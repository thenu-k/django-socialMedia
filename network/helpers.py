from .models import * 

# Function that takes the request, and the query set and gives out the like counts and whether the user has like it
def likeExtrapolator(request, postObjects):
    if request.user.is_authenticated:
        for postObject in postObjects:
            postObject.likeCount = len(Like.objects.filter(postKey = postObject.id))
            