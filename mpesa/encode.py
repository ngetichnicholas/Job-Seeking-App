import base64
import keys



def create_password(formatted_time):

    

    data_to_encode = (
        keys.business_shortCode + keys.mpesa_payment_passkey + formatted_time
    )

    encoded_string = base64.b64encode(data_to_encode.encode())

    decoded_password = encoded_string.decode("utf-8")

    return decoded_password
