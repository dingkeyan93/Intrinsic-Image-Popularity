import logging
from django.contrib import admin
from .models import ImageRating
from django.contrib import messages
from django.utils.translation import ngettext

logger = logging.getLogger(__file__)

# Register your models here.


class ImageRatingAdmin(admin.ModelAdmin):
    list_display = ["rated_img_name","uuid", "updated_at", "rated_value"]
    ordering = ["updated_at"]
    actions = ["get_avg_rating"]

    @admin.action(description="Get Average Rating")
    def get_avg_rating(self, request, queryset):
        avg = 0
        sum = 0
        imageRatings = ImageRating.objects.filter()
        for imageRatingObj in imageRatings:
            sum += imageRatingObj.rated_value
        avg = sum / len(imageRatings)
        logger.debug({sum, avg})
        self.message_user(
            request,
            ngettext(
                "The average rating is %f ",
                "The average rating is %f ",
                avg,
            )
            % avg,
            messages.SUCCESS,
        )
        return


admin.site.register(ImageRating, ImageRatingAdmin)
