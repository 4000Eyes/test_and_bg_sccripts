import json
import requests
import datetime
import re

# These are the timezones to use when you submit request with date as parameters.
#['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', 'Africa/Algiers', 'Africa/Asmara', 'Africa/Asmera', 'Africa/Bamako', 'Africa/Bangui', 'Africa/Banjul', 'Africa/Bissau', 'Africa/Blantyre', 'Africa/Brazzaville', 'Africa/Bujumbura', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/Conakry', 'Africa/Dakar', 'Africa/Dar_es_Salaam', 'Africa/Djibouti', 'Africa/Douala', 'Africa/El_Aaiun', 'Africa/Freetown', 'Africa/Gaborone', 'Africa/Harare', 'Africa/Johannesburg', 'Africa/Juba', 'Africa/Kampala', 'Africa/Khartoum', 'Africa/Kigali', 'Africa/Kinshasa', 'Africa/Lagos', 'Africa/Libreville', 'Africa/Lome', 'Africa/Luanda', 'Africa/Lubumbashi', 'Africa/Lusaka', 'Africa/Malabo', 'Africa/Maputo', 'Africa/Maseru', 'Africa/Mbabane', 'Africa/Mogadishu', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Niamey', 'Africa/Nouakchott', 'Africa/Ouagadougou', 'Africa/Porto-Novo', 'Africa/Sao_Tome', 'Africa/Timbuktu', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Anguilla', 'America/Antigua', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/ComodRivadavia', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Aruba', 'America/Asuncion', 'America/Atikokan', 'America/Atka', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Buenos_Aires', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Catamarca', 'America/Cayenne', 'America/Cayman', 'America/Chicago', 'America/Chihuahua', 'America/Coral_Harbour', 'America/Cordoba', 'America/Costa_Rica', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Dominica', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Ensenada', 'America/Fort_Nelson', 'America/Fort_Wayne', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Grenada', 'America/Guadeloupe', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Indianapolis', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Jujuy', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Knox_IN', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Mendoza', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Rosario', 'America/Santa_Isabel', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Shiprock', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Virgin', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/South_Pole', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Ashkhabad', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Calcutta', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Chongqing', 'Asia/Chungking', 'Asia/Colombo', 'Asia/Dacca', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Harbin', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kashgar', 'Asia/Kathmandu', 'Asia/Katmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macao', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Rangoon', 'Asia/Riyadh', 'Asia/Saigon', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Tel_Aviv', 'Asia/Thimbu', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ujung_Pandang', 'Asia/Ulaanbaatar', 'Asia/Ulan_Bator', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faeroe', 'Atlantic/Faroe', 'Atlantic/Jan_Mayen', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/ACT', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Canberra', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/LHI', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/NSW', 'Australia/North', 'Australia/Perth', 'Australia/Queensland', 'Australia/South', 'Australia/Sydney', 'Australia/Tasmania', 'Australia/Victoria', 'Australia/West', 'Australia/Yancowinna', 'Brazil/Acre', 'Brazil/DeNoronha', 'Brazil/East', 'Brazil/West', 'CET', 'CST6CDT', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Canada/Saskatchewan', 'Canada/Yukon', 'Chile/Continental', 'Chile/EasterIsland', 'Cuba', 'EET', 'EST', 'EST5EDT', 'Egypt', 'Eire', 'Etc/GMT', 'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7', 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-0', 'Etc/GMT-1', 'Etc/GMT-10', 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13', 'Etc/GMT-14', 'Etc/GMT-2', 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9', 'Etc/GMT0', 'Etc/Greenwich', 'Etc/UCT', 'Etc/UTC', 'Etc/Universal', 'Etc/Zulu', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belfast', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Nicosia', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Tiraspol', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GB', 'GB-Eire', 'GMT', 'GMT+0', 'GMT-0', 'GMT0', 'Greenwich', 'HST', 'Hongkong', 'Iceland', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Iran', 'Israel', 'Jamaica', 'Japan', 'Kwajalein', 'Libya', 'MET', 'MST', 'MST7MDT', 'Mexico/BajaNorte', 'Mexico/BajaSur', 'Mexico/General', 'NZ', 'NZ-CHAT', 'Navajo', 'PRC', 'PST8PDT', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Johnston', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Ponape', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Samoa', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Truk', 'Pacific/Wake', 'Pacific/Wallis', 'Pacific/Yap', 'Poland', 'Portugal', 'ROC', 'ROK', 'Singapore', 'Turkey', 'UCT', 'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US/East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Samoa', 'UTC', 'Universal', 'W-SU', 'WET', 'Zulu']


def user_search():
    try:
        parameters = {
                "text" : "sri"
        }
        # res = test_login()
        # headers = {}
        # headers["Authorization"] = "Bearer " + res["token"]
        # print ("The token is ", res["token"])
        #response = requests.get("https://gemift.uw.r.appspot.com/api/prod/search", params=parameters)
        #response = requests.get("http://0.0.0.0:8081/api/user/search",params=parameters, headers=headers)
        response = requests.get("http://0.0.0.0:8081/api/user/search", params=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400


def search_product():
    """
       #following parameters are optional, but send to improve the selection.
       friend_circle_id : You may have to send it most of the time as the search will be done for specific secret friend.
       category: send it in the format used for occasion_list (as shown below). In other words, an array. You send this when the user wants to filter.
       subcategory: send it in the format as shown for occasion_list. You send this array when the user wants to filter.

       In the future I will add the following
       brand: same format as occasion_list
       colot: same forat as occasion_list.

       When the friend circle id is sent. The API will look for all the category and subcategory for the secret friend.
       I am actively implementing this funcitonality.

    :return:
    """


    try:
        parameters = {
            "request_id": 1,
            "sort_order": "ASC",
            "occasion_list": ("Birthday","Marriage")
        }
        #response = requests.get("https://gemift.uw.r.appspot.com/api/prod/search", params=parameters)
        response = requests.get("http://0.0.0.0:8081/api/prod/search",params=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400


def search_product_detail():
    try:
        parameters = {
            "request_id": 7,
            "product_id" : (2,3)
        }
        #response = requests.get("https://gemift.uw.r.appspot.com/api/prod/search",params=parameters)
        response = requests.get("http://0.0.0.0:8081/api/prod/search",params=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def vote_product():
    try:
        parameters = {
            "request_id": 8,
            "product_id" : 2,
            "friend_circle_id":'95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "user_id" : '55e77082-d4c2-4bfa-8032-57f461765591',
            "friend_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "vote" : 1,
            "comment": "He will love this product",
            "occasion_name" : "birthday",
            "occasion_year": 2021
        }
        response = requests.get("http://localhost:5000/api/prod/search", json=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def get_product_votes():
    try:
        parameters = {
            "request_id": 5,
            "product_id" : 2,
            "friend_circle_id":'95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "occasion_name" : "birthday",
            "occasion_year": 2021
        }
        response = requests.get("http://localhost:5000/api/prod/search", json=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def test_get_web_category(request_id, age_lo, age_hi, gender):
    try:
        output_list = []
        parameters = {
            "request_id" : request_id,
            "age_lo" : age_lo,
            "age_hi" : age_hi,
            "gender" : gender
        }
        response = requests.get("http://localhost:5000/api/category", json=parameters)
        print ("The response is ", response.json())
        return 200
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def test_signup():
    try:
        output_list = []
        parameters = {
           # "email" : "Vidya1232@gmail.com",
            "email": "Kraken@gmail.com",
            "user_type" : 0,
            "password" : "Krishna123@",
            "phone_number" : "335-111-2322",
            "gender": "F",
            "first_name" : "Kraken",
            "last_name" : "Raj",
            "location" : "India",
            "external_referrer_id": "Google",
            "external_referrer_param": "abc123-123jsh",
            "image_url": "http://ww.roo.com"
        }
        response = requests.post("http://0.0.0.0:8081/api/auth/signup", json=parameters)
        #response = requests.post("https://gemift.uw.r.appspot.com/api/auth/signup", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def test_login():
    try:
        output_list = []
        parameters = {
           # "email" : "Vidya1232@gmail.com",
            "email": "kokki@gmail.com",
            "password" : "Krishna123@"
        }
        response = requests.post("http://0.0.0.0:8081/api/login", json=parameters)
        #response = requests.post("https://gemift.uw.r.appspot.com/api/auth/signup", json=parameters)
        print ("The response is ", response.json())
        return response.json()
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def test_login_phone():
    try:
        output_list = []
        parameters = {
           # "email" : "Vidya1232@gmail.com",
            "phone_number": "14252815459",
            "password" : "Krishna123@"
        }
        response = requests.post("http://0.0.0.0:8081/api/phone/login", json=parameters)
        #response = requests.post("https://gemift.uw.r.appspot.com/api/auth/signup", json=parameters)
        print ("The response is ", response.json())
        return response.json()
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def friend_circle_request_1():
    try:
        output_list = []

        parameters =         {"request_id": 1,
         "friend_circle_id": "054c1679-daa4-4793-88b4-3790995b6b6d",
         "referrer_user_id": "14503f22-731c-4876-88bf-9ef5d8e8d7b3",
         "referred_user_id": "53cb6fd2-c1b8-4c48-b963-fc3a150c33a6"
         }


        response = requests.post("http://0.0.0.0:8081/api/friend/circle", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def friend_circle_request_2():
    try:
        output_list = []
        parameters = {
            "request_id" : 2,
            "friend_circle_id":"054c1679-daa4-4793-88b4-3790995b6b6d",
            "referrer_user_id": "14503f22-731c-4876-88bf-9ef5d8e8d7b3",
            "email_address":"kuku1254@gmail.com",
            "phone_number": "425-111-2312",
            "first_name":"x",
            "last_name":"y",
            "gender": "M",
            "location": "India"
        }

        parameters = {"request_id": 2,
         "friend_circle_id": "054c1679-daa4-4793-88b4-3790995b6b6d",
             "referrer_user_id": "14503f22-731c-4876-88bf-9ef5d8e8d7b3",
         "email_address": "krishnanIyengar@gmail.com",
         "phone_number": "14252343342",
         "first_name": "Krishnan",
        "last_name": "Iyengar",
        "gender": "M",
        "location": "India"
        }


        response = requests.post("http://0.0.0.0.:8081/api/friend/circle", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def friend_circle_request_3(): #Image url is optional. If there is no image, dont send the parameter.
    try:
        output_list = []
        parameters = { "request_id": 3,
            "referrer_user_id": '7d09a56f-99fd-40a2-b694-4a8a8982c47a',
            "referred_user_id": 'ae61c5ff-5437-4504-b60b-9f61337e1d4d',
            "group_name" : "Lovely 2022",
            "image_url" : "http://www.roo.com",
            "age" : 7,
            "gender": "M"}


        response = requests.post("http://0.0.0.0:8081/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


def friend_circle_request_4():
    try:
        output_list = []
        parameters = {"request_id": 4,
            "referrer_user_id": '80cdb839-46ff-4523-be09-422ba6476c7a',
            "email_address": "mkmknbn@gmail.com",
            "phone_number": "918768768563",
            "first_name": "Jaddusachin",
            "last_name": "mmm",
            "gender": "M",
            "location" : "India",
            "group_name" : "Test2",
            "image_url" : "http://www.roo.com",
            "age" : 45
            }

        parameters = {"request_id": 4,
        "referrer_user_id": "14503f22-731c-4876-88bf-9ef5d8e8d7b3",
        "email_address": "mkIyengar@gmail.com",
        "phone_number": "918768768500",
        "first_name": "Jaddusachin",
        "last_name": "Narayanan",
        "gender": "M",
        "location": "India",
        "group_name": "Only Iyengars",
        "image_url": "http://www.roo.com",
        "age": 45}


        response = requests.post("http://0.0.0.0:8081/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def friend_circle_request_6():
    try:
        output_list = []
        parameters = {
            "request_id": 6,
            "list_friend_circle_id": ["b5b9d6f4-6ce4-435c-80f4-ebb28e6e3872"],
            "referrer_user_id": "e2174acb-dc1e-4ee2-85b9-9be84d3e250a",
            "referred_user_id": "2dfe5543-877e-42d9-95a6-650befd9946d"
        }

        response = requests.post("http://0.0.0.0:8081/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

# call this API when you want to get data for a specific friend circle
def get_friend_circle():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": 'b4870446-6647-436c-af07-8037fa06146a'
        }
        response = requests.get("http://0.0.0.0:8081/api/friend/circle", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

# Call this API when you want to get the friend circle data for a given user.
def get_friend_circle_summary():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "user_id":  "8eefa6e5-0b37-48cd-8757-be6041a421ca",
        }
        response = requests.get("http://0.0.0.0:8081/api/friend/circle", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def add_interest():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "creator_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "user_id": 'fd28bcef-ff38-453a-9258-41e00d6fe6b1',
            "list_category_id": [{"web_category_id":"c3e3805c-8d4a-4bb1-9cb4-7d1d4f05b682", "vote":1}, {"web_category_id":"067da0e1-dc08-4ecf-a6c9-a403611c1886", "vote":1}],
            "list_subcategory_id" :[{"web_subcategory_id":"6a0f5478-b1b0-48b0-9e86-3f5bf44682c0", "vote":1}]
        }
        response = requests.post("http://localhost:5000/api/interest", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

# def get_interest():
#     try:
#         output_list = []
#         parameters = {
#             "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86'
#         }
#         response = requests.get("http://localhost:5000/api/interest", params=parameters)
#         print("The response is ", response.json())
#         return response.status_code
#     except Exception as e:
#         return False

def create_occasion():
    try:
        output_list = []


        parameters = {"request_id": 1,
                      "friend_circle_id": "e28c1f45-164d-4ebd-b677-87a7a48b27c3",
                      "creator_user_id": "3d6c38b3-1873-428f-9196-688f6970b8c2",
                      "occasion_id": 1,
                      "occasion_date": "01/02/2000",
                      "occasion_timezone": "America/New_York"}
        response = requests.post("http://0.0.0.0:8081/api/user/occasion", json=parameters)

        response = requests.post("http://0.0.0.0:8081/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def vote_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "creator_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "occasion_id" : 1,
            "flag": 1,
            "value": "10/12/1979",
            "value_timezone":"America/New_York"
        }

        parameters = {
        "request_id":2,
      "friend_circle_id":"ae48a387-fdc2-456c-b4cd-d7f204406fa0",
        "creator_user_id":"f7d403d9-ceb4-4e47-b074-db8c70427f7c",
        "occasion_id":1,
        "flag":1,
        "value":"10/12/1979",
        "value_timezone": "America/New_York"
        }
        response = requests.post("http://0.0.0.0:8081/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def approve_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 3,
            "friend_circle_id": 'ae48a387-fdc2-456c-b4cd-d7f204406fa0',
            "creator_user_id": 	"8eefa6e5-0b37-48cd-8757-be6041a421ca",
            "occasion_id":"014819e4-7931-4b27-9456-8a31ea351efc",
            "flag": 1
        }
        response = requests.post("http://0.0.0.0:8081/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_occasion_details():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": "04e04f28-272b-4ef7-b424-73116ce4c93f",
            "user_id": "160ece24-24ce-4496-8a1a-10d1b8fad80b"
        }
        response = requests.get("http://0.0.0.0:8081/api/user/occasion", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_occasions_by_user():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "user_id": "160ece24-24ce-4496-8a1a-10d1b8fad80b"
        }
        response = requests.get("http://0.0.0.0:8081/api/user/occasion", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def test_whatsapp():
    try:
        output_list = []
        parameters = {
            "admin_friend_id" : 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "request_id" : 5,
            "user_list" : [
                    {"email_address":"k1@gmail.com", "phone_number": "425-111-1111", "first_name":"x", "last_name":"y", "gender": "M", "secret_friend" : "Y", "contributor": [id1, id2]},
                {"email_address": "k2@gmail.com", "phone_number": "425-111-1112", "first_name": "a", "last_name": "b",
                 "gender": "M", "secret_friend" : "N", "contributor": [id1, id2]},
                {"email_address": "k3@gmail.com", "phone_number": "425-111-1113", "first_name": "a", "last_name": "d",
                 "gender": "M", "secret_friend":"Y", "contributor": [id1, id2]},
                           ]
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

# get all the categories. Call this method for new users

def get_category():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id" : "97ba580f-9055-4199-95a2-22487c20eeb0"
        }
        response = requests.get("http://0.0.0.0:8081/api/category", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

# to store the categories chosen by the user
def add_category_to_user():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "referred_user_id" : "3d6c38b3-1873-428f-9196-688f6970b8c2",
            "friend_circle_id": "659e4af3-e48c-4fc7-9c82-dc1c7c5624eb",
            "list_category_id": [{"web_category_id":"A123", "vote":1}, {"web_category_id":"A124", "vote":1}]

        }

        response = requests.post("http://0.0.0.0:8081/api/interest", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

#to store the subcategories chosen by the user

def add_subcategory_to_user():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "referred_user_id" : '7d09a56f-99fd-40a2-b694-4a8a8982c47',
            "friend_circle_id": "7936eda4-3c75-4091-b55c-fca6f03addb6",
            "list_subcategory_id": [{"web_subcategory_id":"A123", "vote":1}, {"web_subcategory_id":"A124", "vote":1}]
        }

        #response = requests.post("http://0.0.0.0:8081/api/interest", json=parameters)
        response = requests.post("http://gemift.uw.r.appspot.com/api/interest", json=parameters)

        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


#You can repeatedly call this method to get subcategories to show for the user.
def get_user_subcategory():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "friend_circle_id":"ae48a387-fdc2-456c-b4cd-d7f204406fa0",
            "age" : 20
        }
        response = requests.get("http://0.0.0.0:8081/api/interest", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


# to show the categories and subcategories chosen by the user and friends
def get_user_selection_category_and_subcategory():
     try:
         output_list = []
         parameters = {
             "request_id": 3,
             "friend_circle_id":"659e4af3-e48c-4fc7-9c82-dc1c7c5624eb"
         }
         response = requests.get("http://0.0.0.0:8081/api/interest", params=parameters)
         print("The response is ", response.json())
         return response.status_code
     except Exception as e:
         return False

# to upload image
def upload_image():
    try:
        output_list = []
        parameters = {
            "request_id": 3,
            "entity_id":"659e4af3-e48c-4fc7-9c82-dc1c7c5624eb",
            "image_url" : "http://ww.oo.com",
            "image_type": "friend_circle"
        }
        # parameters = {
        #     "request_id": 3,
        #     "entity_id":"659e4af3-e48c-4fc7-9c82-dc1c7c5624eb",
        #     "image_url" : "http://ww.oo.com",
        #     "image_type": "user"
        # }
        response = requests.post("http://0.0.0.0:8081/api/attr", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def notify_landing_page():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "user_id": "8eefa6e5-0b37-48cd-8757-be6041a421ca",
            "phone_number": "919500153858"
        }

        response = requests.get("http://0.0.0.0:8081/api/notify", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False



def creat_custom_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 4,
            "occasion_name" : "Birthday",
                "friend_circle_id":"92fef2d0-14fa-4f4f-b42d-7e91469eccc9",
            "creator_user_id": "9da4bad8-51e9-45a1-833c-3f5bfba5eb59",
            "occasion_date" : "05/04/2022",
            "value_timezone" : "US/Pacific",
            "frequency" : "Every Week"
        }

        response = requests.post("http://0.0.0.0:8081/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def deactivate_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 5,
            "occasion_id" : '33408a1e-249e-4053-b9bd-64e4a2f73492',
            "friend_circle_id":"659e4af3-e48c-4fc7-9c82-dc1c7c5624eb"
        }

        response = requests.post("http://0.0.0.0:8081/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_occasion_names(): # Note: friend circle id is optional. You send friend circle id if the context requires it.
    try:
        output_list = []
        parameters = {
            "request_id": 3,
            "friend_circle_id":"ae48a387-fdc2-456c-b4cd-d7f204406fa0"
        }
        response = requests.get("http://0.0.0.0:8081/api/user/occasion", params=parameters)
        response = requests.get("https://gemift.uw.r.appspot.com/api/user/occasion", params=parameters)

        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def contributor_approval():  # Note: friend circle id is optional. You send friend circle id if the context requires it.
    try:
        output_list = []
        parameters = {
            "request_id": 7,
            "friend_circle_id": "42ab88ce-ab48-4e93-a308-8a550abb491e",
            "phone_number" : "919551027363",
            "signal" : 1
        }
        response = requests.post("http://0.0.0.0:8081/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


def contributor_open_invites():  # Note: friend circle id is optional. You send friend circle id if the context requires it.
    try:
        output_list = []
        parameters = {
            "request_id": 4,
            "phone_number": "14252815459"
        }
        response = requests.get("http://0.0.0.0:8081/api/friend/circle", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_recently_added_interest():
    try:
        output_list = []
        parameters = {
            "request_id": 4,
            "friend_circle_id": "4397b80a-0ec6-42a0-b827-47033dd10b25"
        }
        response = requests.get("http://0.0.0.0:8081/api/interest", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_secret_friend_age_gender():
    try:
        output_list = []
        parameters = {
            "request_id" :1,
            "friend_circle_id": "4397b80a-0ec6-42a0-b827-47033dd10b25"
        }
        response = requests.get("http://0.0.0.0:8081/api/attr", params=parameters)


        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def update_secret_friend_age_gender():
    try:
        output_list = []
        parameters = {
            "request_id" :1,
            "user_id": "3d6c38b3-1873-428f-9196-688f6970b8c2",
            "friend_circle_id": "4397b80a-0ec6-42a0-b827-47033dd10b25",
            "age" : 45,
            "gender" : "M"
        }
        response = requests.post("http://0.0.0.0:8081/api/attr", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_unapproved_occasions():
    try:
        output_list = []
        parameters = {
            "request_id": 6,
            "user_id": "9da4bad8-51e9-45a1-833c-3f5bfba5eb59"
        }

        response = requests.get("http://0.0.0.0:8081/api/notify", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def app_notification():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "user_id": "9da4bad8-51e9-45a1-833c-3f5bfba5eb59",
            "phone_number": "9500153858"
        }

        response = requests.get("http://0.0.0.0:8081/api/notify", params=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


def gmm_initiate_team_buy():
    try:
        output_list = []
        parameters = {
            "request_type": "initiate_team_buy"
        }

        response = requests.post("http://localhost:8081/api/gmm/txn", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def gmm_adjusted_user_share():
    try:
        output_list = []
        parameters = {
            "request_type": "adjusted_user_share"
        }

        response = requests.post("http://localhost:8081/api/gmm/txn", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def opt_out():
    try:
        output_list = []
        parameters = {
            "request_type": "opt_out"
        }

        response = requests.post("http://localhost:8081/api/gmm/txn", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def pay_amount():
    try:
        output_list = []
        parameters = {
            "request_type": "pay_amount"
        }

        response = requests.post("http://localhost:5000/api/gmm/txn", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


def st_friend_circle_request_4():
    try:
        for x in range(4,50):
            email_address = "XXmkIyengar" + str(x) + "@gmail.com"
            phone_number = 918768768500 + x
            first_name = "Avatar" + str(x)
            last_name = 'God' + str(x)
            group_name = "stress test" + str(x)
            parameters = {"request_id": 4,
            "referrer_user_id": '80cdb839-46ff-4523-be09-422ba6476c7a',
            "email_address": email_address,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "gender": "M",
            "location": "India",
            "group_name": group_name,
            "image_url": "http://www.roo.com",
            "age": 45}

            response = requests.post("http://0.0.0.0:8081/api/friend/circle", json=parameters)
            print("The response is ", response.json(), response.status_code)
    except Exception as e:
        print ("The error is ", e)
        return False

def st_friend_circle_request_2():
    try:
        for x in range(101,150):
            email_address = "XXmkIyengar" + str(x) + "@gmail.com"
            phone_number = 918768768300 + x
            first_name = "Rama" + str(x)
            last_name = 'Krishna' + str(x)
            parameters = {"request_id": 2,
             "friend_circle_id": '8abaf99c-8dc5-4cfc-9d8d-3dbe72492f9f',
                 "referrer_user_id": '80cdb839-46ff-4523-be09-422ba6476c7a',
             "email_address": email_address,
             "phone_number": phone_number,
             "first_name": first_name,
            "last_name": last_name,
            "gender": "M",
            "age": 32,
            "location": "India"
            }
            response = requests.post("http://0.0.0.0.:8081/api/friend/circle", json=parameters)
            print ("The response is ", response.json(),response.status_code)
    except Exception as e:
        print ("The error is", e)
        return False


try:
    output_hash = []
    status_code = 0
    #status_code = search_product()
    #status_code = test_get_web_category(3, 10, 20, "F")
    #status_code = test_signup()
    #status_code = test_login_phone()
    #status_code = test_login()
    #status_code = user_search()
    #status_code = test_whatsapp()

    """
    # request_id : 1 --> referring an existing member to an existing friend circle - This will require referrer_user_id, friend_circle_id, friend_user_id
    # request_id : 2 --> referring a non-existing user friend to an existing friend circle - This will require referrer_user_id, friend_circle_id, email_address, name.
    # requests_id : 3 --> creating a friend circle for an existing member as the secret friend - This will require creator_user_id, friend_id, circle name
    # request_id : 4 --> creating a friend circle for a non-existing member as the secret friend - This will require creator_user_id, email_address, name, circle_name
    # request_id : 5 --> a list of friends or contacts from whatsapp to create friend circles.
    
    """
    #status_code = friend_circle_request_1()
    #status_code = friend_circle_request_2()
    #status_code = friend_circle_request_3()
    #status_code = friend_circle_request_4()
    #status_code = friend_circle_request_6()
    #status_code = create_occasion()
    #status_code = vote_occasion()
    #status_code = approve_occasion()
    #status_code = get_occasion_details()
    #status_code = get_occasions_by_user()
    #status_code = get_friend_circle()
    #status_code = get_friend_circle_summary()
    #status_code = add_interest()
    #status_code = get_interest()
    status_code = search_product()
    #status_code = search_product_detail()
    #status_code = vote_product()
    #status_code = get_product_votes()
    #status_code = get_category()
    #status_code = add_category_to_user()
    #status_code = add_subcategory_to_user()
    #status_code = get_category()
    #status_code = get_user_subcategory()
    #status_code = upload_image()
    #status_code = get_user_selection_category_and_subcategory()
    #status_code = notify_landing_page()
    #status_code = contributor_approval()
    #status_code = creat_custom_occasion()
    #status_code = deactivate_occasion()
    #status_code = get_occasion_names()
    #status_code = get_secret_friend_age_gender()
    #status_code = update_secret_friend_age_gender()
    #status_code = get_unapproved_occasions()
    #status_code = app_notification()
    #status_code = st_friend_circle_request_4()
    #status_code = st_friend_circle_request_2()
    #status_code = gmm_initiate_team_buy()
    #status_code = pay_amount()
    #status_code = gmm_adjusted_user_share()
    #status_code = opt_out()

    print ("The status code is", status_code)

except Exception as e:
    print ("The error is ", e)