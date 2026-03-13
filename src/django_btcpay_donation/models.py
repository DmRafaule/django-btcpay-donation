from urllib.parse import urlparse, urlunparse, urlencode, parse_qs, unquote


from django.db import models
from django.conf import settings

class BTCPayDonationLink(models.Model):
    url = models.URLField(max_length=1028)

    def __str__(self):
        return f"{unquote(self.url)}"

    def save(self, *args, **kwargs):
        if self.url:
            parsed_url = urlparse(self.url)
            # Если действительно разработчики указал Домен магазина в настройках меняем на указанный, 
            # иначе останется тот, что был указан в ссылке
            raw_domain = getattr(settings, 'BTCPAY_DOMAIN', parsed_url.netloc)
            # Проверяем, есть ли протокол в строке из настроек
            if "://" not in raw_domain:
                # Если протокола нет, считаем, что это чистый домен и добавляем https
                domain_parts = urlparse(f"https://{raw_domain}")
            else:
                domain_parts = urlparse(raw_domain)
            
            new_domain = domain_parts.netloc
            # Если в настройках указан свой протокол (например, http для локалки), берем его
            new_scheme = domain_parts.scheme or parsed_url.scheme or 'https'

            new_store_id = getattr(settings, 'BTCPAY_STORE_ID', None)
            query_params = parse_qs(parsed_url.query)
            # Если действительно разработчики указал ID магазина в настройках меняем на указанный, 
            # иначе останется тот, что был указан в ссылке
            if new_store_id:
                query_params['storeId'] = [new_store_id]
            new_query = urlencode(query_params, doseq=True)

            self.url = urlunparse((
                new_scheme,
                new_domain,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment
            ))

        super().save(*args, **kwargs)

class BTCPayDonationLinkLocation(models.Model):
    linklocation_name = models.CharField(max_length=100, unique=True)
    link = models.ForeignKey(BTCPayDonationLink, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.linklocation_name} | {self.link}"

class BTCPayDonationConfiguration(models.Model):
    configuration_name = models.CharField(max_length=100, blank=False, null=True, unique=True)
    donation_link_locations = models.ManyToManyField(BTCPayDonationLinkLocation)

    def __str__(self):
        return self.configuration_name

class BTCPayDonationCurrentConfiguration(models.Model):
    current = models.OneToOneField(
        BTCPayDonationConfiguration,
        on_delete=models.CASCADE,
        null=True,  # Allow no item to be selected initially
        blank=True,
        related_name='current_donation_link_config' # Optional: for reverse access
    )

    def __str__(self):
        return f"Current selection: { self.current.configuration_name if self.current else 'None'}"

    def save(self, *args, **kwargs):
        # Ensure only one CurrentSelection object exists
        if not self.pk and BTCPayDonationCurrentConfiguration.objects.exists():
            raise Exception("Only one BTCPayDonationCurrentConfiguration object can exist.")
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        # Helper method to get the single CurrentSelection instance
        try:
            obj = cls.objects.all().first() # Use a fixed PK for single instance
            return obj
        except:
            return None 

    @classmethod
    def set_current_item(cls, item_instance):
        current_selection = cls.get_current()
        current_selection.current = item_instance
        current_selection.save()