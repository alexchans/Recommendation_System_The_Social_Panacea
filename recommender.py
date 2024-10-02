import firebase_admin
from firebase_admin import credentials, db

# get access to the realtime database, store in data as dict
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesocialpanacea-default-rtdb.firebaseio.com/'  # Replace with your database URL
})
ref = db.reference('users')  
data = ref.get()

for user, user_info in data.items():
    user_info['age'] /= 100 #1
    user_info['sportsPreferences'] = len( user_info['sportsPreferences'])/10 #3
    user_info['pickUpGamesPreferences'] = len( user_info['pickUpGamesPreferences'])/10 #4
    user_info['foodPreferences'] = len( user_info['foodPreferences'])/10 #5
    user_info['eatingWithFriends'] = 1 if user_info['eatingWithFriends'] == True else 0 #6
    user_info['cookingWithFriends'] = 1 if user_info['cookingWithFriends'] == True else 0 #7
    user_info['popCulturePreferences'] = len( user_info['popCulturePreferences'])/10 #8
    user_info['popCultureFriendPreferences'] = len( user_info['popCultureFriendPreferences'])/10 #9
    user_info['travelWithFriends'] = 1 if user_info['travelWithFriends'] == True else 0 #10
    user_info['meetingNewPeopleComfortLevel'] /= 5 #13
print(data)
    
    


