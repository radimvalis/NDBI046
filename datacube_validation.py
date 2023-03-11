import rdflib, sys, os

def run_validation(dataset: rdflib.Graph):
  
	with open("validation_queries.sparql") as stream:
	 
		query_prefixes = stream.readline()

		query_number = 1

		for query in stream:

			print(f"IC-{query_number}: ", end="")

			try:
				result = dataset.query(query_prefixes + query)
				for row in result:
					if not row:
						print("OK")
					else:
						print("NOT OK")
		
			except:
				print("Query evaluation skipped")

			query_number += 1

def main():

	if len(sys.argv) == 1:
		print(f"{sys.argv[0]}: No data file provided", file=sys.stderr)
		return
	
	if not os.path.isfile(sys.argv[1]):
		print(f"File '{sys.argv[1]}' not found", file=sys.stderr)
		return

	datacube_as_turtle = sys.argv[1]
	graph = rdflib.Graph()
	graph.parse(datacube_as_turtle, format="turtle")

	run_validation(graph)

if __name__ == "__main__":
	main()