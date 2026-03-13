from django.contrib import admin
from .models import BTCPayDonationLink, BTCPayDonationLinkLocation, BTCPayDonationConfiguration, BTCPayDonationCurrentConfiguration

# Register your models here.

admin.site.register(BTCPayDonationLink, admin.ModelAdmin)
admin.site.register(BTCPayDonationLinkLocation, admin.ModelAdmin)
admin.site.register(BTCPayDonationConfiguration, admin.ModelAdmin)
admin.site.register(BTCPayDonationCurrentConfiguration, admin.ModelAdmin)