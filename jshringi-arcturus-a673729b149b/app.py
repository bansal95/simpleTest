from __future__ import print_function
from flask import Flask, render_template,request,redirect,url_for # For flask implementation
import pdb
import pysolr
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json

#import pysolr
import difflib
import collections
from flask_cors import CORS
application =   Flask(__name__)
FlaskJSON(application)
CORS(application)
taxons = ["silver earrings" , "mens organizers",
 "lapel pins", "artifacts",
	"kids chains", "ties",
	 "tie pins", "mens pens",
		"rakhi thalis", "religious decor",
		 "mens sherwani buttons",
			"mens wallets", "maang tika combos", "panna", "vouchers", "combos", "clutches combos",
				"lahsuniya", "manik", "mens wallets combos",
					"armlets combos", "bags and wallets", "kids necklaces",
					 "gift vouchers", "kids accessories", "combos", "anklets combos",
						"kids bangles & bracelets combos", "artifacts", "mens bags and wallets",
						 "wallets", "kids necklace sets", "healing stones", "kids pendant sets",
							"pouches combos", "women", "mens belts combos", "pendants sets combos",
							 "mens lapel pins", "moti", "nose pins combos", "wallets combos",
								"mens tie-pins combos", "kids anklets", "mens ties", 
								"moonga", "mens tie-pins", "gomed","gold jewellery", "ratnas", "pukhraj",
								 "neelam", "buttons", "mens kada combos", "mens chains combos", "mens cufflinks combos", 
								 "mangalsutras combos", "mens earrings", "nose rings & pins", "brooches combos",
									"accessories", "brooches", "mens rings combos", "silver coins", "coins",
									 "handbags", "handbags combos", "kids pendants combos", "hath phool combos",
										"kamarband combos", "pooja thalis", "kids rakhis", "gold coins", "juda pins",
										 "hath phool", "mens rings", "mens pendants", "mens chains",
											"mens bracelets", "mens pendants combos", "necklaces combos",
											 "mens earrings combos", "nose pins", "mens rakhis combos",
												"rakhis combos", "mens jewellery", "clutches", "necklaces",
												 "toe rings combos", "kamarband", "watches", "maang tika",
													"pendant sets", "armlets", "mens cufflinks", "anklets", "pendants combos",
													 "toe rings", "kids earrings combos", "combos", "mixed combos", "bags & wallets", 
													 "pouches", "mens belts", "mens mixed combos", "saree clips", "kids jewellery", 
													 "necklace sets combos", "earrings combos", "gifts", "mens brooches"
													 , "bridal sets", "mens bracelets combos", "saree pins",
														"bracelets combos", "kids bangles and bracelets", "mens accessories",
														 "belts", "rakhis", "mens rakhis", "mens necklaces", "hair accessories",
															"mens buttons", "body chains", "kids pendants", "kids earrings",
															 "maang tika sets", "chains", "rings combos", "mens kada",
										"jewellery", "rings", "bracelets", "necklace sets", "pendants", "mangalsutras", "earrings"] 

title = "Arcturus"
#solr = pysolr.Solr('http://localhost:8983/solr/voylla/', timeout=10) 

@application.route("/arcturus-search",methods=['POST','GET'])
def action ():

	query = request.values.to_dict(flat=True)
	# results = solr.search(query['q'])
	data =[]

	if 'q' in query and len(query['q'])>2:
		data = difflib.get_close_matches(query['q'].lower(),taxons,len(query['q']),0.5)
		if len(data)==1 :
			data=difflib.get_close_matches(data[0].lower(),taxons,len(data[0]),0.5)
		elif len(data)==0:
			data=difflib.get_close_matches(query['q'].lower(),taxons,len(query['q']),0)

		counter = collections.Counter(data)
		newdata = [key for key, _ in counter.most_common()]
		newdata.sort(key=len, reverse=False)
		finaldata = sorted(newdata,key=lambda x: (not x.startswith(query['q']), x))
		return json_response(data=finaldata,success=True)
	else:
		return json_response(data=[],success=True)


@application.route("/get_server_status",methods=['POST','GET'])
def get_server_status():
	return json_response(success=True)


@application.route("/get_solr_data",methods=['POST','GET'])
def get_solr_data():
	# if(request.method == 'POST'):

	pdb.set_trace()

	solr_url = 'http://localhost:8983/solr/voylla'
	solr = pysolr.Solr(solr_url, timeout=100)
	filter_queries = ['bracelets','productPopularity: 5','product_gender: men']
	val_docs = solr.search('*',fq = filter_queries,rows=10)
	
	finaldata = []

	for val in val_docs.__dict__['docs']:
		element = {}

		product_permalink = val['product_permalink']
		productURL = 'https://www.voylla.com/products/' + product_permalink

		variant_sku = val['variant_sku'][0]
		pid = val['product_asset_detail_json'][0].split(':')[1].split(',')[0]
		img = val['product_asset_detail_json'][0].split('swatch-image')[1].split('",')[0]
		imagesURL = 'https://images.voylla.com/i/' + pid + '/original/' + product_permalink + '-' + variant_sku + '-' + img
		imagesURL = imagesURL.lower()

		prodDesc = val['product_description']
		prodName = val['productName']

		element['id'] = len(finaldata) + 1
		element['productName'] = prodName
		element['imagesURL'] = imagesURL
		element['productURL'] = productURL
		element['productDesc'] = prodDesc

		finaldata.append(element)

	return json_response(data=finaldata,success=True)



@application.route("/api/get_chatbot_data",methods=['POST','GET'])
def dialogue_webhook():
	# if(request.method == 'POST'):

	solr_url = 'http://localhost:8983/solr/voylla'
	solr = pysolr.Solr(solr_url, timeout=100)
	#filter_queries = ['Jaipur','productPopularity: 5','product_gender: men']
	filter_queries = ['Jaipur']
	val_docs = solr.search('*',fq = filter_queries,rows=10)

	facebook = {}
	attachment={}
	attachment['type']='template'
	payload = {}
	payload['template_type']='generic'
	elements = []
	for val in val_docs.__dict__['docs']:
		element = {}

		product_permalink = val['product_permalink']
		productURL = 'https://www.voylla.com/products/' + product_permalink

		variant_sku = val['variant_sku'][0]
		pid = val['product_asset_detail_json'][0].split(':')[1].split(',')[0]
		img = val['product_asset_detail_json'][0]

		imagesURL = 'https://i2.wp.com/www.indiaretailing.com/wp-content/uploads/2016/06/voylla.png?fit=681%2C400'
		if('swatch-image' in img):
			img = img.split('swatch-image')[1].split('",')[0]
			imagesURL = 'https://images.voylla.com/i/' + pid + '/original/' + product_permalink + '-' + variant_sku + '-' + img
		elif('swatch-ms' in img):
			# https://images.voylla.com/i/524390/original/flutter-bracelet-with-dual-tone-snjai41672-ms-20170814-28735-1uxvdjq.jpg?1502722802
			img = img.split('swatch-ms')[1].split('",')[0]
			imagesURL = 'https://images.voylla.com/i/' + pid + '/original/' + product_permalink + '-' + variant_sku + '-ms-' + img
		imagesURL = imagesURL.lower()

		prodDesc = val['product_description']
		prodName = val['productName']
		price = val['Price'][0]
		
		element['image_url'] = imagesURL
		element['subtitle'] = "Rs. " + str(price)
		element['title']=prodName

		default_action={}
		default_action['type']='web_url'
		default_action['url']=productURL
		default_action["webview_height_ratio"] = "tall"
		#default_action["fallback_url"] = "https://www.voylla.com/"
		element['default_action']=default_action

		buttons = []
		button_buy_now = {}
		button_buy_now['type'] = 'web_url'
		button_buy_now['url'] = productURL
		button_buy_now['title'] = 'Buy Now'
		buttons.append(button_buy_now)
		button_show_details = {}
		button_show_details['type'] = 'web_url'
		button_show_details['url'] = productURL
		button_show_details['title'] = 'Show Details'
		buttons.append(button_show_details)
		element['buttons'] = buttons

		elements.append(element)
	
	payload['elements']=elements
	attachment['payload']=payload
	facebook['attachment']=attachment
	#print(facebook)

	#pdb.set_trace()
	return json_response(data=facebook,success=True)



# "message":{
# 	"attachment":{
# 		"type":"template",
# 		"payload":{
# 			"template_type":"generic",
# 			"elements":[
# 				{
# 					"title":"Welcome!",
# 					"image_url":"https://petersfancybrownhats.com/company_image.png",
# 					"subtitle":"We have the right hat for everyone.",
# 					"default_action": {
# 						"type": "web_url",
# 						"url": "https://petersfancybrownhats.com/view?item=103",
# 						"messenger_extensions": false,
# 						"webview_height_ratio": "tall",
# 						"fallback_url": "https://petersfancybrownhats.com/"
# 					},
# 					"buttons":[
# 						{
# 							"type":"web_url",
# 							"url":"https://petersfancybrownhats.com",
# 							"title":"View Website"
# 						},{
# 							"type":"postback",
# 							"title":"Start Chatting",
# 							"payload":"DEVELOPER_DEFINED_PAYLOAD"
# 						}
# 					]
# 				}
# 			]
# 		}
# 	}
# }






# @application.route("/mlt",methods=['POST','GET'])
# def get_mlt_product():
# 	query = request.values.to_dict(flat=True)
# 	query_data = "product_id:"+query['product_id']
# 	res = solr.more_like_this(q=query_data, mltfl='product_taxonomy_name')
# 	return json_response(data=list(res),success=True)


if __name__ == "__main__":
		application.run(host='0.0.0.0',debug=True)