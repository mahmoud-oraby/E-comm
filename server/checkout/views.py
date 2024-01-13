from django.http import JsonResponse
import stripe
from django.conf import settings
from shipping.models import ShippingAddress
from rest_framework.decorators import api_view
from order.models import Order, ProductOrder
from cart.models import Cart, CartItem
from django.db.models import F, Sum
from order.utils import generate_random
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
import os
import decimal
from store.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["GET"])
def create_checkout_session(request):
    user = request.user

    cart = Cart.objects.get(user=user)
    apply_discount = False
    coupon = None
    try:
        shipping = ShippingAddress.objects.get(
            user=user, default_address=True)

        total = CartItem.objects.filter(cart=cart).aggregate(
            total_price=Sum(F('product__price') * F('quantity')))['total_price']
        if cart.coupon:
            coupon = stripe.Coupon.retrieve(cart.coupon)

            if coupon.metadata.type == 'percentage' and int(coupon.metadata.min_total) <= total:
                total -= (float(total) * (coupon.percent_off / 100) / 100)
                apply_discount = True
            elif coupon.metadata.type == 'fixed' and int(coupon.metadata.min_total) <= total:
                total -= decimal.Decimal(str(float(coupon.amount_off) / 100))
                apply_discount = True


        if total:
            try:
                order = Order.objects.get(
                    customer_name=user, status='unpaid')
            except:
                products = CartItem.objects.filter(cart=cart)
                order = Order.objects.create(
                    customer_name=user, cart=cart, order_id=generate_random(), total_price=total, shipping=shipping)
                for product in products:
                    product_order, created = ProductOrder.objects.get_or_create(
                        product_name=product.product, price=product.product.price, quantity=product.quantity, image=product.product.image)
                    order.product.add(product_order)
        else:
            return {'error': 'Cart item is empty.'}

    except ShippingAddress.DoesNotExist:
        return Response({'error': 'Select default address.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    cart_items = CartItem.objects.filter(cart_id__user_id=user).all()

    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.title,
                    'images': [f'{settings.BACKEND_DOMAIN}/{item.product.image}'],
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,


        })
    

    if not line_items:
        # Handle the case where line_items is empty
        return JsonResponse({'message': 'No items in the cart'})
    
    # Create the checkout session
    discount = []
    if coupon and int(coupon.metadata.min_total) <= total:
        discount.append({"coupon":coupon.id})
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            discounts=discount,
            mode="payment",
            success_url=os.environ.get("SUCCESS_URL"),
            cancel_url=os.environ.get("CANCEL_URL"),
            metadata={
                'user_id': item.cart.user.id,
                'order_id': order.order_id
            },
        )
    except stripe._error.InvalidRequestError:
        return Response({"message":"This coupon is no longer available!"},status=status.HTTP_400_BAD_REQUEST)


    return JsonResponse({'checkout_url': session.url})


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
def create_checkout_session_webhook(request):
    payload = request.body.decode('utf-8')
    sig_header = request.headers.get('Stripe-Signature')

    endpoint_secret = settings.WEB_HOOK_SECRET

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.metadata.user_id
        order_id = session.metadata.order_id

        order = Order.objects.get(order_id=order_id)
        order.status = 'pending'
        order.save()

        cart_items = CartItem.objects.filter(cart_id__user_id=user_id)
        cart = Cart.objects.get(user_id=user_id)

        for cart_item in cart_items:
            product  = cart_item.product
            product.selled += cart_item.quantity
            product.save()

        cart_items.delete()
        if not cart.coupon == None:
            cart.coupon = None
            cart.save()

    return Response(status=200)
