from django.db.models import Q
from django.template.response import TemplateResponse
from django.conf import settings

from .models import BTCPayDonationCurrentConfiguration


class BTCPayDonationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)            
        return response
    
    def process_template_response(self, request, response: TemplateResponse):
        self.donationlink_handler(request, response)
        return response
    
    def donationlink_handler(self, request, response):
        if response.context_data:
            response.context_data.update({'isBTCPayDonationMiddlewareConnected': True})
            current_ad_network = BTCPayDonationCurrentConfiguration.get_current()
            if current_ad_network:
                response.context_data.update({f'donation_link_locations': current_ad_network.current.donation_link_locations.all()})