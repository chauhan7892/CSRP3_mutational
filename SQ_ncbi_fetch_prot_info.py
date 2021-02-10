import re
from os import listdir
import entrezpy.conduit
from collections import OrderedDict
import argparse
import entrezpy.base.result 
import entrezpy.base.analyzer


# class Prot_Result(entrezpy.base.result.EutilsResult):
# 	def __init__(self, response, request):
# 		super().__init__(request.eutil, request.query_id, request.db)
# 		self.prot_records = {}

# 		def size(self):
# 		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.size`
# 		returning the number of stored data records."""
# 		return len(self.prot_records)

# 		def isEmpty(self):
# 		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.isEmpty`
# 		to query if any records have been stored at all."""
# 		if not self.prot_records:
# 		  return True
# 		return False


# 		def dump(self):
# 		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.dump`.

# 		:return: instance attributes
# 		:rtype: dict
# 		"""
# 		return {self:{'dump':{'prot_records':[x for x in self.prot_records],
# 		                          'query_id': self.query_id, 'db':self.db,
# 		                          'eutil':self.function}}}

# class ProtAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
#   """Derived class of :class:`entrezpy.base.analyzer.EutilsAnalyzer` to analyze and
#   parse PubMed responses and requests."""

#   def __init__(self):
#     super().__init__()

#   def init_result(self, response, request):
#     """Implemented virtual method :meth:`entrezpy.base.analyzer.init_result`.
#     This method initiate a result instance when analyzing the first response"""
#     if self.result is None:
#       self.result = PubmedResult(response, request)

#   def analyze_error(self, response, request):
#     """Implement virtual method :meth:`entrezpy.base.analyzer.analyze_error`. Since
#     we expect XML errors, just print the error to STDOUT for
#     logging/debugging."""
#     print(json.dumps({__name__:{'Response': {'dump' : request.dump(),
#                                              'error' : response.getvalue()}}}))

#   def analyze_result(self, response, request):
#     """Implement virtual method :meth:`entrezpy.base.analyzer.analyze_result`.
#     Parse PubMed  XML line by line to extract authors and citations.
#     xml.etree.ElementTree.iterparse
#     (https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.iterparse)
#     reads the XML file incrementally. Each  <PubmedArticle> is cleared after processing.

#     ..note::  Adjust this method to include more/different tags to extract.
#               Remember to adjust :class:`.PubmedRecord` as well."""
#     self.init_result(response, request)



def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	with open(input_file[0],'r') as f_in_seq_id:
		for line in f_in_seq_id:
			if line[0] == '\n':
				continue
			if line[0]=='>':
				line_attrs = line.split(' ')
				protein_id = line_attrs[0][1:]
				w = entrezpy.conduit.Conduit('pankajchauhan@itadmin-lab25')
				fetch_prot_info = w.new_pipeline()	
				fetch_prot_info.add_fetch({'db' : 'protein', 'id' : protein_id, 'retmode' : 'xml'}, analyzer=entrezpy.efetch.efetch_analyzer.EfetchAnalyzer())
				tmp = w.run(fetch_prot_info)
				xml_txt = tmp.analyze_result(response,request) #.uids
				f_out_path = output_file[0]+'/'+protein_id+'.xml'
				with open(f_out_path,'wb') as f_out:
					f_out.write(xml_txt)

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="A script to extract Disease Gene Data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="OM_.txt", help="Check Mesh file and Morbid file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="OM_.txt", help="Check OMIM file")
	args_ = parser.parse_args()

	main(  )
	#print distance('Myasthenic syndrome, congenital, 10, 254300 (3)', 'Myasthenic Syndrome')
	print( 'done' )


