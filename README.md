# Online ticket sales

The application is used to sell tickets for events. It is based on **Django 3**. **Bootstrap 4** was used for the appearance of the application. 
Admin has the ability to add and edit events and tickets. The user who is not logged in can watch the events, but have to register to buy tickets.
The app can be improved by adding a user who can register as an event organizer who will be add and edit events.
After selecting specific tickets, the customer goes to the payment made with **Braintree**.
After proceeding to payment, an e-mail is sent with the order confirmation using the async task completed by **Celery** with **Redis** as backend.
If the payment is successful, an e-mail with the ticket is sent using the async task. **Redis** was also used to count views of events, which made it possible to display the most viewed events on the main page.
If the payment has not been made, the asyc task adds the tickets from that order back to the pool.
The customer can also download his tickets by going to his profile tab. Searching by event name is handled with **Elasticsearch**.
Admin can generate **csv report** of selected orders.


## How to run:
- you must have installed docker and docker-compose,
- clone this repo,
- make a file named "web-variables.env" in main folder and then setup variables:
BRAINTREE_PRIVETE_KEY=??
BRAINTREE_PUBLIC_KEY=??
BRAINTREE_MERCHANT_ID=??
EMAIL_HOST=??
EMAIL_HOST_USER=??
EMAIL_HOST_PASSWORD=??
EMAIL_PORT=??
- run -> make build,
- get data from fixtures, run -> make loaddata ,
- run the app -> make run,
- superuser is already created, you can log in by username: admin | password: admin.
