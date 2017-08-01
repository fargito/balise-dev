

def generate_ordering_links(ordering, attributes, links_base, default_order=0):
	"""generates a list of links to order a list with the attributes and the current choice
	of order"""
	

	ordering_links = []

	if ordering:
		current_order = ordering.split('.')
		for i in range(len(attributes)):
			if '-'+str(i) in current_order:
				j = current_order.index('-'+str(i))
				current_order_filtered = current_order[:j] + current_order [j+1:]
				parsed = '.'.join(current_order_filtered)
				if parsed:
					link = links_base + str(i) + '.' + parsed
				else:
					link = links_base + str(i)
				ordering_links.append(link)
			elif str(i) in current_order:
				j = current_order.index(str(i))
				current_order_filtered = current_order[:j] + current_order [j+1:]
				parsed = '.'.join(current_order_filtered)
				if parsed:
					link = links_base + '-' + str(i) + '.' + parsed
				else:
					link = links_base + '-' + str(i)
				ordering_links.append(link)
			else:
				parsed = '.'.join(current_order)
				if parsed:
					link = links_base + str(i) + '.' + parsed
				else:
					link = links_base + str(i)
				ordering_links.append(link)

	else:
		for i in range(len(attributes)):
			if i == default_order:
				ordering_links.append(links_base+'-'+str(i))
			else:
				ordering_links.append(links_base+str(i))



	return ordering_links




def generate_ordering_arguments(ordering, attributes):
	"""generates the arguments used to filter a list of objects. Return None if no arg"""
	arguments = None

	if ordering:		
		arguments = []
		# on met tous les paramètres dans une liste pour faire l'ordonnance d'un seul coup (sinon ça
		# fait de la merde)
		for index in ordering.split('.'):
			try:
				if '-' in index:
					arguments.append('-'+attributes[abs(int(index))])
				else:
					arguments.append(attributes[int(index)])
			except:
				pass

	return arguments