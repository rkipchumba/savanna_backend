from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from utils.notifications import send_sms
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@receiver(post_save, sender=OrderItem)
def notify_order(sender, instance, created, **kwargs):
    order = instance.order
    customer = order.customer

    # Skip if order has no items yet? Actually at this point, at least one exists
    items = order.items.all()
    if not items:
        return

    # Total
    total_price = sum([i.product.price * i.quantity for i in items])

    # SMS
    if customer.phone:
        message = (
            f"Hi {customer.user.get_full_name() or customer.user.username}, "
            f"your order #{order.id} has been placed successfully. Total: {total_price}."
        )
        send_sms(customer.phone, message)

    # Email
    items_text = "\n".join([f"- {i.product.name} x {i.quantity} @ {i.product.price}" for i in items])
    rows = "".join(
        [f"<tr><td>{i.product.name}</td><td>{i.quantity}</td><td>{i.product.price}</td></tr>" for i in items]
    )

    text_content = (
        f"A new order has been placed.\n\n"
        f"Customer: {customer.user.get_full_name() or customer.user.username}\n"
        f"Phone: {customer.phone}\n"
        f"Order ID: {order.id}\n"
        f"Total: {total_price}\n\n"
        f"Items:\n{items_text}"
    )

    html_content = f"""
    <h2>New Order #{order.id} Placed</h2>
    <p><strong>Customer:</strong> {customer.user.get_full_name() or customer.user.username}<br>
    <strong>Phone:</strong> {customer.phone}<br>
    <strong>Total:</strong> {total_price}</p>
    <h3>Items:</h3>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
      <tr>
        <th>Product</th><th>Quantity</th><th>Price</th>
      </tr>
      {rows}
    </table>
    """

    subject = f"New Order #{order.id} placed"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = ["kipchumbarodgers@gmail.com"]

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
