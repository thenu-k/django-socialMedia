from .models import * 

# Function that takes the request, and the query set and gives out the like counts and whether the user has like it
def likeExtrapolator(request, postObjects):
    for postObject in postObjects:
        postObject.likeCount = len(Like.objects.filter(postKey = postObject))
        if request.user.is_authenticated:
            if Like.objects.filter(userKey=User.objects.get(id=request.user.id), postKey = postObject).exists():
                postObject.userLikedThis = True
            else: 
                postObject.userLikedThis = False
            