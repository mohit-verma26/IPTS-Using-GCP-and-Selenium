import json
import requests

def get_prediction(lat, lng, speed, vehicle_type):
    endpoint = "https://us-central1-aiplatform.googleapis.com/v1/projects/transportation-app-450511/locations/us-central1/endpoints/YOUR_ENDPOINT_ID:predict"
    
    headers = {
        "Authorization": f"Bearer ya29.c.c0ASRK0GbYJZGJ4fUCuNXBO9V387tVEgP82gkqhM_nVX5BkxYqtM5z-Oul17xOtF4F5iJ8k5qOtsfR-VinUOshDeIR-PsAVgK8yOjuPgCjXniPDvXMW4WVj2I8hcAkb94dDbnOdJZa7EKZqMc6IK4lUl2oSKjA9a6_qZidgMX7kwyY7tXmCwqOzT8sUjgC3kKb29KVqRM6t9ylQIzJ1IaB-YE2S6-ZZPnxxeNVbGUvUIHpxwGSwjEsNg8qUmmlcIprHbGdZDwZncT23jJIxdtErn2FMirR9om2_pJIrpowjdm8mkA7bfMxn0Yxiee_Ys0VlJ69Nac5Zi5H9L26nQchbHMxqfVSrxzj8i5qGDWAsZCAll5g2Y01tXATE385PMUuglz7Y90_s9UZBxlxeRtgbxYyj-cwnRmsRik8i-QiOuvkhrsYmv-tmzqOOZbZyU267JxW5JszehBxnjhnld_0M6bdUrvzaqjUlZbmuZIUt6q2od_OrpZ7f_apcu8JBxkO36rwcayn7O8iidiRfaijZzFSoIkQIQVQnzc5RBepkffQ5Wz7rfB0pmpvmVnd2-iOO0yrIFq5ayqk0x31hnadoJZtv9x7_28_5ldMqX6einphVuqWzWuq31pRgSUj8IkRstXYaX1X6fb8JveZ9jd_lO7wBdS-0VtOFlleZ-wV29oW8SwjU60qgxBi07szqMnlfk9incja_3MdYo3ZjbWvylFkqSh0b4vd96zrFfoUXfqMYO7BqtImetsBiyhBzYQymmZd94rUp90xpf20kMzhUz4beUwYfoh8yv9wQM7xqV2tYuJfWUOFM99ImYIgSVJ_RdrBZd3VcirpnzQ9FrrzQ6WbuM_yxB3n8xibbYn7jQJmXshmk7rzp3SMIuXniYUU46_bmFSSj4w1l1I6JO1V0sQoy72V94vyumlVmq1_Vmx71atQY4ulpllmVbXIoba4hfsrBphVI6WMzxFm_zctW323_hXYaopwWbU26b9dFlXlV6Or1kI8-dr",  # Replace with your actual token
        "Content-Type": "application/json"
    }

    data = {
        "instances": [
            {
                "lat": lat,
                "lng": lng,
                "speed": speed,
                "type": vehicle_type
            }
        ]
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.json())
        return None
