import json
import random

data = {}

product_id = 10000
product_description = "This is test data generated for gemift.com. The product id is "
product_title = "This is product title"

category = ["A121","A122","A123","A124","A125","A126","A127","A128","A129","A130","A131"]
subcategory = ["A1","A2","A3","A4","A5", "A51","A52","A53","A54","A55","A41","A42","A43","A44","A401","A411","A421","A31","A41"]
cat_name = {"A121": "Electronics","A122":"Home","A123":"Software","A124":"Test2","A125":"Travel","A126":"Hobby","A127":"Running","A128":"Utensils","A129":"Sports","A130":"Outdoors","A131":"Entertainment"}
subcat_name = {"A1":"Subcat1","A2":"Subcat2","A3":"Subcat3","A4":"Subcat4","A5":"Subcat5", "A51":"Subcat6","A52":"Subcat7","A53":"Subcat8","A54":"Subcat9","A55":"Subcat10",
               "A41":"Subcat11","A42":"Subcat12","A43":"Subcat13","A44":"Subcat14","A401":"Subcat15","A411":"Subcat16","A421":"Subcat17","A31":"Subcat18","A41":"Subcat19"}
price = [10.02,20.02,30.03,40.03,50.09,60.09,80.90, 120.20, 140.08, 200.00]
age_range_list = [[0,5],[6,10,],[11,15], [15,19], [20,30], [31,39], [40,49], [50,60], [60,100],[101,150]]
gender_list = ["male","female","both"]
website_url = ["http://www.amazon.com","http://www.flipkart.com","http:///www.ebay.com","http:///www.dealshare.in"]
occasion = [["Birthday","GEM-OCC-999999"], ["Valentines Day","2"],["Wedding Anniversary","GEM-OCC-000124"],["Met my girlfriend","GEM-OCC-000125"],["Mothers day","5"],["Fathers Day","6"]]
season_product = ["Y","N"]
country = ["India","Europe","USA","Singapore","Hong Kong","Malaysia","Thailand", "All"]

file_handle = open("/home/krissrinivasan/Downloads/product_gemift.json","w")

for cat in category:
    for subcat in subcategory:
        for i in range(1,50):
            data = {}
            product_id = product_id + 1
            data["product_id"] = product_id
            data["product_title"] = product_title + " " + str(product_id)
            data["product_description"] = product_description + str(product_id)
            data["category"] = cat
            data["subcategory"] = subcat
            data["category_name"] = cat_name[cat]
            data["subcategory_name"] = subcat_name[subcat]
            data["price"] = random.choice(price)
            data["gender"] = random.choice(gender_list)
            age_range = random.choice(age_range_list)
            data["age_lo"] = age_range[0]
            data["age_hi"] = age_range[1]
            data["website_url"] = random.choice(website_url)
            data["seasonal_product"] = random.choice(season_product)
            l_occasion = random.choice(occasion)
            data["occasion_name"] = l_occasion[0]
            data["occasion_id"] = l_occasion[1]
            data["country"] = random.choice(country)

            json_data = json.dumps(data)

            file_handle.write(json_data + "\n")

            print ("Json data ", json_data)

