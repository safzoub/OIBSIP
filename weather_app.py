import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import io
import geocoder

API_KEY = "824b43820d140234262377f41dc588a6"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city, unit):
    try:
        units = "metric" if unit == "Celsius" else "imperial"
        params = {"q": city, "appid": API_KEY, "units": units}
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if data.get("cod") != 200:
            raise ValueError(data.get("message", "City not found"))

        return {
            "name": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "condition": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def update_weather():
    city = city_entry.get().strip()
    unit = unit_var.get()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city.")
        return

    weather = fetch_weather(city, unit)
    if weather:
        temp_label.config(text=f"Temp: {weather['temp']}° {'C' if unit == 'Celsius' else 'F'}")
        humidity_label.config(text=f"Humidity: {weather['humidity']}%")
        wind_label.config(text=f"Wind: {weather['wind']} {'m/s' if unit == 'Celsius' else 'mph'}")
        condition_label.config(text=f"Condition: {weather['condition'].capitalize()}")
        city_label.config(text=f"{weather['name']}")

        try:
            icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
            icon_response = requests.get(icon_url, timeout=5)
            icon_img = Image.open(io.BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
        except:
            icon_label.config(image='', text="")

def autofill_location():
    try:
        g = geocoder.ip('me')
        city_entry.delete(0, tk.END)
        city_entry.insert(0, g.city or "")
    except:
        messagebox.showwarning("Location Error", "Could not auto-detect location.")

root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("360x440")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

tk.Label(root, text="Enter City:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))
city_entry = tk.Entry(root, font=("Arial", 14), width=25)
city_entry.pack(pady=5)

tk.Button(root, text="Use My Location", command=autofill_location, bg="#1976d2", fg="white").pack(pady=(0, 8))

unit_var = tk.StringVar(value="Celsius")
unit_frame = tk.Frame(root, bg="#f0f0f0")
tk.Radiobutton(unit_frame, text="Celsius", variable=unit_var, value="Celsius", bg="#f0f0f0").pack(side="left", padx=10)
tk.Radiobutton(unit_frame, text="Fahrenheit", variable=unit_var, value="Fahrenheit", bg="#f0f0f0").pack(side="left", padx=10)
unit_frame.pack(pady=5)

tk.Button(root, text="Get Weather", command=update_weather, bg="#4caf50", fg="white", font=("Arial", 12)).pack(pady=10)

city_label = tk.Label(root, font=("Arial", 16, "bold"), bg="#f0f0f0")
city_label.pack(pady=5)

icon_label = tk.Label(root, bg="#f0f0f0")
icon_label.pack()

temp_label = tk.Label(root, font=("Arial", 12), bg="#f0f0f0")
humidity_label = tk.Label(root, font=("Arial", 12), bg="#f0f0f0")
wind_label = tk.Label(root, font=("Arial", 12), bg="#f0f0f0")
condition_label = tk.Label(root, font=("Arial", 12), bg="#f0f0f0")

for lbl in [temp_label, humidity_label, wind_label, condition_label]:
    lbl.pack(pady=2)

root.mainloop()
