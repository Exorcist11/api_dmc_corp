from Services.Middleware import *

from config import app
from flask import jsonify, render_template, request, redirect
from vn_pay.vnpay import *
from vn_pay.settings import *
from datetime import *
from Models.Orders import *
from Models.Carts import *
from Models.Products import *


@app.route('/create_payment', methods=['POST'])
def create_payment():
    request_json = request.json
    bank_code = request_json.get('bank_code')
    order_id = request_json.get('order_id')
    total = request_json.get('total')
    account_id = request_json.get('account_id')
    cart_id = request_json.get('cart_id')
    address_id = request_json.get('address_id')

    vnp = vnpay()
    vnp.requestData['vnp_Version'] = '2.1.0'
    vnp.requestData['vnp_Command'] = 'pay'
    vnp.requestData['vnp_TmnCode'] = VNPAY_TMN_CODE
    vnp.requestData['vnp_Amount'] = total * 100 if total > 700000 else (total + 30000) * 100
    vnp.requestData['vnp_CurrCode'] = 'VND'
    vnp.requestData['vnp_TxnRef'] = order_id
    vnp.requestData['vnp_OrderInfo'] = f'{account_id}_{cart_id}_{address_id}'
    vnp.requestData['vnp_OrderType'] = 'other'
    vnp.requestData['vnp_Locale'] = 'vn'
    if bank_code and bank_code != "":
        vnp.requestData['vnp_BankCode'] = bank_code
    vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
    vnp.requestData['vnp_IpAddr'] = '127.0.0.1'
    vnp.requestData['vnp_ReturnUrl'] = VNPAY_RETURN_URL
    vnpay_payment_url = vnp.get_payment_url(VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY)
    return jsonify({'payment_url': vnpay_payment_url})


@app.route('/payment_return', methods=['GET'])
def payment_return():
    inputData = request.args.to_dict()

    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        order_detail = order_desc.split('_')
        cart_product = CartProducts.query.filter_by(cart_id=order_detail[1]).all()

        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
            firstTimeUpdate = True
            totalAmount = True
            if totalAmount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = jsonify({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = jsonify({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = jsonify({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = jsonify({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = jsonify({'RspCode': '99', 'Message': 'Invalid request'})

    return result


