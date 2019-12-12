from resources import wpl
import json
from datetime import datetime, timedelta
import sys
import requests

def tts(data,dt):
    readings_per_day = 8
    if data is None:
        response = requests.get(
            "https://community-open-weather-map.p.rapidapi.com/forecast", 
            params= {
                "q": "herndon,us",
                "units": "imperial"
            },
            headers={
                "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",        
                "X-RapidAPI-Key": "4735041723mshbe34feaa59fd91fp10c60djsn2eb915b4a3c1"
            }
        )

        data = {"forecast": response.json()}

    # data = json.loads(json.loads(data))

    # with open('forecast.json') as file:
    #     data = json.loads(file.read())

    # lets get the forecast for saturday

    today = dt
    fore = wpl.FiveDayForecast(data).forecast_on(today)
    average_temp = int(fore.average_apparent_temp())
    highest_temp = fore.highest_apparent_temp()
    rain_times = fore.rain_times()

    # initialize text to speech string
    tts = ""

    ###################
    #   TEMPERATURE   #
    ###################
    # get temperature trend
    temp_trend = ""
    trendict = {
        80: "a pretty hot",
        60: "a pretty nice",
        40: "a pretty cool",
        20: "a pretty cold",
        float("-inf"): "an extremely cold"
    }

    for temp,name in trendict.items():
        if average_temp > temp:
            temp_trend = trendict[min(average_temp,temp)]
            break

    # get temperature range 
    temp_class = {
        6 : "high",
        3 : "mid",
        -1 : "low"
    }

    str_temp = ""
    average_temp = [average_temp - average_temp%10, average_temp%10]
    for deg,name in temp_class.items():
        if average_temp[1] > deg:
            str_temp = name
            break


    str_temp = f"{str_temp} {(average_temp[0])}'s" if average_temp[0] >= 20 \
        else f"{str_temp} teens"

    tts += f"It'll be {temp_trend} day today, with temperatures hovering in the {str_temp}. "


    ###################
    #   CLOUD COVER   #
    ###################
    cloud_classes = {
        89: "overcast",
        69: "mostly cloudy",
        59: "relatively cloudy", # this one is made up
        34: "partly cloudy",
        -1: "minimal"
    }

    clouds = fore.average_clouds()
    cloud_class = ""
    for val,name in cloud_classes.items():
        if clouds > val:
            cloud_class = name
            break

    tts += f"Additionally, cloud cover will be {cloud_class}" if cloud_class == "minimal" \
        else f"Additionally it will be {cloud_class}"


    ##################
    #      RAIN      #
    ##################
    if fore.will_rain():
        tts += ", and you can expect "
                
        rain_classes = {
            7.5: "heavy",
            2.4: "moderate",
            0  : "light"
        }

        rain_class = ""
        if len(rain_times) >= readings_per_day/2:
            avg_rain = fore.average_rain()
            for val,name in rain_classes.items():
                if avg_rain > val:
                    rain_class = name
                    break

            tts += f"{rain_class} rain showers for the better half of the day."

        else:
            if len(rain_times) == 1:
                rain_time = datetime.fromtimestamp(rain_times[0]['time'])
                st = rain_time.strftime("%I:%M %p")
                en = (rain_time + timedelta(hours=3)).strftime("%I:%M %p")

                rain_amnt = rain_times[0]['val']
                rain_class = \
                    "light scattered showers" if rain_amnt < 2.5 else    \
                    "moderate scattered showers" if rain_amnt < 7.6 else \
                    "heavy scattered showers"

                if en == "12:00 AM":
                    tts += f"{rain_class} to start at {st} and continue into tomorrow."
                else:
                    tts += f"{rain_class} to hit from {st} to {en}."
            else:
                avg_rain_amnt = sum([r['val'] for r in rain_times])/len(rain_times)
                rain_class = \
                    "light" if avg_rain_amnt < 2.5 else    \
                    "moderate" if avg_rain_amnt < 7.6 else \
                    "heavy"

                # check for concurrent rain times
                # e.g: 6:00-9:00 and 9:00-12:00
                tts += f"{rain_class} rain showers to hit from "

                start = (
                    datetime.fromtimestamp(rain_times[0]['time'])
                ).strftime("%I:%M %p")
                end = (
                    datetime.fromtimestamp(rain_times[0]['time'])+timedelta(hours=3)
                ).strftime("%I:%M %p")

                rts = {  }
                for rain_time in rain_times[1:]:            
                    cur_start = datetime.fromtimestamp(rain_time['time']).strftime("%I:%M %p")
                    cur_end = (
                        datetime.fromtimestamp(rain_time['time']) + timedelta(hours=3)
                    ).strftime("%I:%M %p")

                    if cur_start == end:
                        end = cur_end
                    else:
                        rts[start] = end
                        start = cur_start
                        end = cur_end

                rts[start] = end

                for st,en in rts.items():
                    tts += f"{st} and will continue into tomorrow" if en == '12:00 AM' \
                        else f"{st} to {en}"

                    if len(rts.items()) > 1:
                        tts += ", "
                tts += "."

    ##############
    #    SNOW    # 
    ##############

    print(tts)
    return tts
