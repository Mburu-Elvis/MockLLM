from gradio_client import Client

client = Client("https://751948b0baf06556fe.gradio.live/")
result = client.predict(
		phoneNumber="792897412",
		userQuery="when is my next appointment",
		api_name="/predict"
)
print(result)
