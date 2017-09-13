http://www.eventbrite.com/myaccount/apps/

https://www.eventbrite.com/developer/v3/quickstart/

https://www.eventbrite.com/developer/v3/endpoints/organizers/

https://www.eventbrite.com/o/vietstartuplondon-14646693153

https://vietstartuplondon.eventbrite.com

https://www.eventbrite.co.uk/o/london-vietstartup-8609317297

https://www.eventbriteapi.com/v3/organizers/14646693153/events/?token=${EVBRITE_ANON_TOKEN}

https://www.eventbriteapi.com/v3/organizers/14646693153/events/?status=live%2Cended%2Cstarted&order_by=start_desc&token=${EVBRITE_ANON_TOKEN}

https://www.eventbrite.com/developer/v3/response_formats/event/

https://docs.python.org/2/library/datetime.html

https://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime

http://docs.python-requests.org/en/master/user/quickstart/#make-a-request

```
{
    "pagination": {
        "object_count": 1,
        "page_number": 1,
        "page_size": 50,
        "page_count": 1,
        "has_more_items": false
    },
    "events": [
        {
            "name": {
                "text": "InfiBot Launch",
                "html": "InfiBot Launch"
            },
            "description": {
                "text": "With advent of technology and the rise of bots, you can now join communities and get assistance from the bots.",
                "html": "<P>With advent of technology and the rise of bots, you can now join communities and get assistance from the bots.<\/P>"
            },
            "id": "36456262663",
            "url": "https://www.eventbrite.com/e/vslbot-launch-tickets-36456262663",
            "vanity_url": "https://vslbot-launch.eventbrite.com",
            "start": {
                "timezone": "Europe/London",
                "local": "2017-08-11T09:00:00",
                "utc": "2017-08-11T08:00:00Z"
            },
            "end": {
                "timezone": "Europe/London",
                "local": "2017-08-11T12:00:00",
                "utc": "2017-08-11T11:00:00Z"
            },
            "created": "2017-07-22T05:43:37Z",
            "changed": "2017-07-22T05:56:09Z",
            "capacity": 100,
            "capacity_is_custom": false,
            "status": "live",
            "currency": "USD",
            "listed": true,
            "shareable": true,
            "online_event": false,
            "tx_time_limit": 480,
            "hide_start_date": false,
            "hide_end_date": false,
            "locale": "en_US",
            "is_locked": false,
            "privacy_setting": "unlocked",
            "is_series": false,
            "is_series_parent": false,
            "is_reserved_seating": false,
            "source": "create_2.0",
            "is_free": true,
            "version": "3.0.0",
            "logo_id": null,
            "organizer_id": "14646693153",
            "venue_id": "20440548",
            "category_id": "102",
            "subcategory_id": "2004",
            "format_id": "11",
            "resource_uri": "https://www.eventbriteapi.com/v3/events/36456262663/",
            "logo": null
        }
    ]
}
```