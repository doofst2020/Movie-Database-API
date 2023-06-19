
from tqdm import tqdm
from flask import Flask, request, render_template, abort
import csv, json
import traceback

app = Flask('app')

app.route('/calculator')
def calculator():
  return render_template('calculator.html')

@app.route('/docs')
@app.route('/')
def docs():
  return render_template('docs.html')

@app.route('/square', methods = ['GET'])
def square():
  # This is how we get a parameter from the url submission. This is how we will handle get requests in the assignment for this week.
	num = request.args.get('num')
	# return str(int(num) ** 2)
  # If we are not given a 'num' parameter.
	if num is None:
    # We will abort the request with the 400 error code and a message.
		abort(400, 'ERR_PARAMETER_MISSING: Please include num parameter.')
  # We will attempt to give them a response of an integer.
	try:
    # You can return a string, integer, list or dictionary.
		return {'num': num, 'resp': int(num) ** 2}
  # If it doesn't work.
	except:
    # We will abort the request with the 400 error code and a message.
		abort(400,  "ERR_BAD_PARAMETER: Please use a INT for num parameter")

@app.route('/single-movie', methods = ['GET'])
def get_movie():
	with open ('output.json', 'r') as file:
		jsonreader = json.load(file)
		return jsonreader[0]

@app.route('/all', methods = ['GET'])
def get_all():
	with open('output.json', 'r') as file:
		jsonreader = json.load(file)
		return jsonreader

@app.route('/get-movie', methods = ['GET'])
def moviesearch():
	name = request.args.get('name')
	with open('output.json', 'r') as jsonfile:
		jsonreader = json.load(jsonfile)
		# return jsonreader[0]
		lst=sorted([cur['original_title'] for cur in jsonreader])
		# print(lst)
		return thesearching(name,lst)
		
def thesearching(name,lst): #[!Recursive Function AND Binary Search, Finds the specific movie prompted!]
	# print(lst)
	if len(lst)<1: return ['BAD JOB! Movie Not Found']
	elif len(lst) ==  2: return lst
	middle = lst[round(len(lst)/2)]
	# print(f'Middle: {middle} -- Checking {name} in {lst[0:round(len(lst)/2)] if name < middle else lst[round(len(lst)/2)+1:-1]}')
  # If the middle is equal to our 
	if middle.lower() == name.lower(): 
		with open('output.json', 'r') as jsonfile:
			jsonreader = json.load(jsonfile)
			for cur in jsonreader:
				if cur['title'] == name: return cur
				
	if name >= middle: return thesearching(name, lst[round(len(lst)/2)+1:-1])
	else: return thesearching(name, lst[0:round(len(lst)/2)+1])

@app.route('/newmovie', methods = ['POST']) #[5]
def new_country():
	body = request.json
	try: #[!Exception Handling!]
		with open('new.json','w') as file:
			json.dump(body, file)
		return "Successful"
	except:
		print(traceback.format_exc())
		abort(400, "uhoh")

@app.route('/changehomepage', methods = ['POST']) #[6]
def changewebsite():
	name = request.args.get('name')
	body = request.json
	print(name, body)
	with open('output.json') as file:
		jsonreader = json.load(file)
		# for cur in jsonreader[0:5]:
			# if cur[19] == name: print(cur)
		bigfile = jsonreader
		movie = [cur for cur in jsonreader if cur['title'] == name]
		for cur in movie:
			print(body['homepage'])
			# movie['homepage'] = body['homepage']
			cur.update(body)
			fixed = cur
		for cur in bigfile:
			if cur['title'] == name: cur = fixed
	with open('output.json', 'w',) as file:
		json.dump(bigfile, file)
	return ['ITSA Success']

@app.route('/kill-movie', methods = ['DELETE']) #[Delete Function :) ]
def delete_movie():
	title = request.args.get('title')
	with open('output.json') as file:
		jsonreader = json.load(file)
		newfile = [cur for cur in jsonreader if cur['title'] != title]
	with open('output.json', 'w') as file:
		json.dump(newfile, file)
	return ['ITSA Success']


@app.route('/lamestmovies', methods = ['GET'])
def sort():
	with open('output.json', 'r') as jsonfile:
		jsonreader = json.load(jsonfile)
		# return jsonreader[0]

		lst=[((cur['original_title'],cur['popularity'])) for cur in jsonreader] #[!Comprehension in order to go through entire data set]
	
	for last_ind in range(len(lst) -1, 0, -1): #[1 !Bubble Sort Algorithm to reverse sort movies]
  
		for nested_ind in range(last_ind):

			if float(lst[nested_ind][1]) > float(lst[nested_ind+1][1]):

				lst[nested_ind], lst[nested_ind + 1] = lst[nested_ind + 1], lst[nested_ind]

	return lst


@app.route('/find-directors', methods = ['GET'])
def find_director():
	lst = []
	# Find directors from classes
	# For movie in json create object
	with open('output.json', 'r') as jsonfile:
		jsonreader = json.load(jsonfile)
		for cur in jsonreader:
			lst.append(Movies(cur))
	return [(x.title, x.director) for x in lst]
	pass
		
class Movies:
	def __init__(self, dictionary):
		self.title = dictionary['title']
		self.popularity = dictionary['popularity']
		self.keywords = dictionary['keywords']
		self.homepage = dictionary['homepage']
		self.director = dictionary['director']


	def __repr__(self): #[!Dunder Function][2] 
		return self.title

	def __str__(self): #[2]
		return f'{self.title} has a popularity of {self.popularity}, great.'
	# def __len__
		# return len([self.title for cur ])
	
	# def find_director(self):
	# 	with open('output.json', 'r') as jsonfile:
	# 		jsonreader = json.load(jsonfile)
	# 		for cur in jsonreader:
	# 			print(self.title)



# launch app
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)






# garbage from setting up db
	# 	for row in csv_reader:
	# 		row['crew'] = eval(row['crew'])
	# 		row['spoken_languages'] = eval(row['spoken_languages'])
	# 		row["production_companies"] = eval(row["production_companies"])
	# 		row["production_countries"] = eval(row["production_countries"])
	# 		row['keywords'] = row['keywords'].split()
	# 		row['genres'] = row['genres'].split()
			
	# 		lst.append(row)

	# with open('output.json', 'w') as file:
 #    # Dump your dictionary in the output file
	# 	json.dump(lst, file)
 #    # Close the file
	# 	file.close()
	# return lst[0]


# i don't have the heart to delete this it's my soul
# , fieldnames=['index','budget','genres','homepage','id', 'keywords','original_language', 'original_title','overview','popularity','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','title','vote_average','vote_count','cast','crew','original_language','original_title','overview','popularity','production_companies','status','tagline','title','vote_average','vote_count'])
