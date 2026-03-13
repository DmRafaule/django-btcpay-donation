# Django BTCPay Donation

**django-btcpay-donation** is a Django application designed to help you easily track and manage generated links on a BTCPay Server for use via invoices. It allows you to centrally store links, group them by location, and switch between different configurations through the Django admin panel, automatically injecting active links into your template context.

## Features:

* **URL Management**: Save and automatically format BTCPay URLs by overriding the domain and Store ID via Django settings.
* **Location Grouping**: Map specific donation links to physical locations on your site (e.g., "Sidebar", "Footer").
* **Flexible Configurations**: Create sets of link locations and switch the "Active" set globally with a single click.
* **Automatic Context Injection**: A custom middleware provides your templates with active donation links without manual view updates.

## Installation

Install the package via pip:
``` Bash
pip install django-btcpay-donation
```
Requirements:

* Python >= 3.10
* Django >= 5.2

## Configuration
1. Update settings.py

    Add the app label to your INSTALLED_APPS list to enable app:
    ```Python
    INSTALLED_APPS = [
        ...,
        'django_btcpay_donation.apps.BtcpaydonationConfig',
        ...,
    ]
    ```

    Add the middleware to your MIDDLEWARE list to enable template context injection:
    ```Python
    MIDDLEWARE = [
        ...,
        'django_btcpay_donation.middleware.BTCPayDonationMiddleware', 
        ...,
    ]
    ```

2. (Optional) Global BTCPay Settings

    You can define global parameters for your BTCPay Server. If these are set, the application will automatically replace the domain and Store ID in any saved links to match these values:
    ```Python
    # The domain of your BTCPay Server
    BTCPAY_DOMAIN = "https://btc-node.of.by"
    # Your specific Store ID
    BTCPAY_STORE_ID = "YourStoreID"
    ```

3. Database Migrations

    Run migrations to create the necessary database tables:
    ```Bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Usage

1. In Admin Interface

    Use the Django Admin to manage your setup:

    * BTCPay Donation Links: Add your raw BTCPay invoice URLs.
    * BTCPay Donation Link Locations: Assign links to specific named locations (e.g., top_banner).
    * BTCPay Donation Configurations: Create a named group of locations.
    * BTCPay Donation Current Configuration: Select which configuration is currently "Live" on the site.

    2. Templates

    The middleware automatically adds donation_link_locations to your template context. You can loop through them like this:
    ```HTML
    {% if isBTCPayDonationMiddlewareConnected %}
        {% for location in donation_link_locations %}
            <a href="{{location.link}}">
                Donate
            </a>
        {% endfor %}
    {% endif %}
    ```
    Or select the spefic one:
    ```HTML
    {% if isBTCPayDonationMiddlewareConnected %}
        {% for location in donation_link_locations %}
            {% if location.linklocation_name == "FOOTER" %}
                <a href="{{location.link}}">
                    Donate
                </a>
            {% endif %}
        {% endfor %}
    {% endif %}
    ```
    Where is the FOOTER is a name of a location assigned in admin while creating *BTCPay Donation Link Locations*.


## URL Logic

When a BTCPayDonationLink is saved, the application parses the URL:

* It replaces the host with BTCPAY_DOMAIN if configured.
* It updates the storeId query parameter with BTCPAY_STORE_ID if configured.
* This ensures that even if you migrate your BTCPay Server or change stores, you only need to update your settings.py.

## License

This project is licensed under the MIT License.
Author: [Tim The Webmaster](https://timthewebmaster.com) - timachuduk@gmail.com

Project Links

* Repository: [GitHub](https://github.com/DmRafaule/django-btcpay-donation)
* [Full Guide(EN)](https://timthewebmaster.com/en/tools/django-btcpay-donation)
* [Full Guide(RU)](https://timthewebmaster.com/ru/tools/django-btcpay-donation)