from xmlrpc.client import getparser
from plugin import plugin, require

from colorama import Fore
import requests
#from ryanair import Ryanair
from FlightRadar24.api import FlightRadar24API

@require(network=True)
@plugin('flights')
class Flights():
    def __call__ (self,jarvis,s):
        self.flights(jarvis,s)
    def flights(self,jarvis, s):
        fr_api = FlightRadar24API()
        jarvis.say("Welcome to Flight module."+ "\n")
        self.newRadarApp(jarvis,s)


    def newRadarApp(self,jarvis, s):
        url='https://app.goflightlabs.com/advanced-real-time-flights?access_key='
        #jarvis.say('Please input your api key from :https://app.goflightlabs.com/')
        #api_key= jarvis.input()
        api_key=  'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiMjI2NzBiMGU5ZjM1MjQ0NTM0NTZkMGFmMWNhMTRjMjU5NGUxY2M2MzYyMjMwNjc3NGY1NmRiOTBlNzQ3ZDFiNjczYThlYzJlNjU3OWI0MDciLCJpYXQiOjE2NzAzNDY2NTksIm5iZiI6MTY3MDM0NjY1OSwiZXhwIjoxNzAxODgyNjU5LCJzdWIiOiIxOTEyNSIsInNjb3BlcyI6W119.utABbQBy23WneF4n8doTyWZzX1RqxtYiClMMRS0lkdaNuRMhVQpkST0fUwJ19SXKHyu2kp6VkWeRvpe8OYNnwg'
        query = self.getParams(jarvis)
        if query == 'q':
            return-1
        jarvis.say(query)
        jarvis.say('Getting results ...')
        try:
            req = requests.get(url+ api_key+query)
        except:
            jarvis.say('Something went wrong, please try again')
        try:
            flight = req.json()
        except:
            jarvis.say('Something went wrong during parsing JSON')
            return -1
        print(flight['data'][1]['arrival']['iataCode'])
        jarvis.say('Filter results, select how many results to display')
        
        display= jarvis.input()
        print(display)
        while display.isnumeric()==False:
            jarvis.say('Please input number:')
            display= input()
        self.print_results(jarvis, flight,display)
        

    def getParams(self,jarvis):
        jarvis.say('select params: 1-status 2-dep 3-arr 4-airline 5-flight number 6-flight code q to quit')
        user=jarvis.input()
        userState=['1','2','3','4','5','6','q']
        query=''
        while user not in userState:
            jarvis.say('insert valid option')
            user=jarvis.input()
        if '1' in user:
            status_state=['en-route', 'started', 'landed', 'unknown']
            jarvis.say('Enter flight status: en-route, started, landed, unknown')
            status=jarvis.input()
            while status not in status_state:
                jarvis.say('Please input valid state')
                status=jarvis.input()

            query= query+'&status='+status
        elif '2' in user:
            jarvis.say('Enter departure airport iata code: LHR')
            dep=jarvis.input()
            query= query+'&depIata='+dep.upper()
        elif '3' in user:
            jarvis.say('Enter arrival airport iata code: LHR')
            arr=jarvis.input()
            query= query+'&arrIata='+arr.upper()
        elif '4' in user:
            jarvis.say('Enter airline name: AA (American airlines')
            dep=jarvis.input()
            query= query+'&airlineIata='+dep
        elif '5' in user:
            jarvis.say('Enter flight iata:')
            num=jarvis.input()
            query= query+'&flightIata='+num.upper()
        elif '6' in user:
            jarvis.say('Enter flight number:')
            dep=jarvis.input()
            query= query+'&flightNum='+dep.upper()
        elif user == 'q':
            return 'q'
        return query
        
    def check_value(self,value):
        if value == None:
            
            value='None'
            return 'None'
        else:
            return value

    def print_live_flights(self,jarvis,flight):
        jarvis.say('latitude: ' + str(flight['live']['latitude']))
        jarvis.say('longitude: ' +str(flight['live']['longitude']))
        jarvis.say('altitude: ' +str(flight['live']['altitude']))
        jarvis.say('direction: ' +str(flight['live']['direction']))
        jarvis.say('speed horizontal: ' +str(flight['live']['speed_horizontal']))


    def print_results(self,jarvis, flights, number_of_prints):
        #print(flights)
        if 'success' in flights and flights['success'] == False:
            jarvis.say('No data found, please try again')
            print(flights)
            return -1
        i=0
        while i<int(number_of_prints):
            text = Fore.RED + \
                'FLIGHT' + Fore.RESET
            jarvis.say(text)
            
            dep_airport1=flights['data'][i]['departure']['iataCode']
            arr_airport1=flights['data'][i]['arrival']['iataCode']
            flight1=flights['data'][i]['flight']['iataNumber']
            aircraft=flights['data'][i]['aircraft']['iataCode']
            speed=flights['data'][i]['speed']['horizontal']
            longitude=flights['data'][i]['geography']['longitude']
            latitude=flights['data'][i]['geography']['latitude']
            altitude=flights['data'][i]['geography']['altitude']
            jarvis.say('Flight status: ' + flights['data'][i]['status'])

            text = Fore.BLUE + \
                'DEPARTURE' + Fore.RESET
            jarvis.say(text)
            jarvis.say('Departure airport: ' +dep_airport1)
            text1 = Fore.BLUE + \
                'ARRIVAL' + Fore.RESET
            jarvis.say(text1)
            jarvis.say('Arrival airport: ' + arr_airport1)
            jarvis.say('Flight: ' + flight1)
            jarvis.say('Aircraft: ' + aircraft)
            jarvis.say('Speed:' + str(speed))
            jarvis.say('Longitude: ' + str(longitude))
            jarvis.say('Latitude: ' +str(latitude))
            jarvis.say('Altitude: ' +str(altitude))
            i=i+1
            
            
            
            """""
            dep_airport1=flights['data'][i]['departure']['iataCode']
            dep_airport=self.check_value(dep_airport1) 
            flight1=flights['data'][i]['flight']['iataNumber']
            flight_info1=self.check_value(flight1)
            dep_country1= flights['data'][i]['departure']['timezone']
            dep_country= self.check_value(dep_country1)
            dep_gate1=flights['data'][i]['departure']['gate']
            dep_gate=self.check_value(dep_gate1)
            dep_scheduled1=flights['data'][i]['departure']['scheduled']
            dep_scheduled=self.check_value(dep_scheduled1)

            arr_airport1=flights['data'][i]['arrival']['airport']
            arr_country1= flights['data'][i]['arrival']['timezone']
            arr_terminal1=flights['data'][i]['arrival']['terminal']
            arr_gate1=flights['data'][i]['arrival']['gate']
            arr_airport=self.check_value(arr_airport1)
            arr_country=self.check_value(arr_country1)
            arr_terminal=self.check_value(arr_terminal1)
            arr_gate=self.check_value(arr_gate1)
            arr_delay1=flights[i]['arrival']['scheduled']
            arr_scheduled=self.check_value(arr_delay1)
            
            jarvis.say('Flight status: ' + flights['data'][i]['status'])

            text = Fore.BLUE + \
                'DEPARTURE' + Fore.RESET
            jarvis.say(text)
            jarvis.say('Departure airport: ' +dep_airport)
            #jarvis.say('Departure country: ' + dep_country)
            
            #jarvis.say(flights[0]['departure']['airport'])
            #jarvis.say('Flight: ' + flight_info1)
            #jarvis.say('Departure gate: ' + dep_gate)
            #jarvis.say('Departure scheduled: '+dep_scheduled) 
            #jarvis.say(str(dep_delay))
            
            text1 = Fore.BLUE + \
                'ARRIVAL' + Fore.RESET
            jarvis.say(text1)
            
        """
            #jarvis.say('Arrival airport: ' + arr_airport)
            #jarvis.say('Arrival country: ' + arr_country)
            #jarvis.say('Arrival terminal: ' + arr_terminal)
            #jarvis.say('Arrival gate: ' + arr_gate)
            #jarvis.say('Arrival scheduled: ') 
            ##jarvis.say(flights[0]['arrival']['delay'])
            """
            if flights[i]['live']!=None:
                jarvis.say('live:')
                print( flights[i]['live'])
                self.print_live_flights(jarvis,flights[i])
            i=i+1
            """