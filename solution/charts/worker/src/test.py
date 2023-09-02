import logging
from evfinder import EVFinder
import utils
import unittest
from tabulate import tabulate

# DEBUG | INFO | WARNING | ERROR | CRITICAL
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

class TestWorker(unittest.TestCase):
  #@unittest.skip("")
  def test_connector_types(self):
    connectors1 = ['NEMA1450', 'NEMA515', 'NEMA520', 'J1772', 'J1772COMBO', 'CHADEMO', 'TESLA']
    connectors2 = ['NEMA1450', 'NEMA515', 'NEMA520', 'J1772COMBO', 'J1772', 'CHADEMO', 'TESLA']
    
    result1 = utils.get_connector_types(connectors1)
    self.assertEqual(result1, 'Ⓝ⑭-㊿  Ⓝ⑤-⑮  Ⓝ⑤-⑳  Ⓙ  ⒸⒸⓈ  ⒸⒽⒶ  Ⓣ')

    result2 = utils.get_connector_types(connectors2)
    self.assertEqual(result2, 'Ⓝ⑭-㊿  Ⓝ⑤-⑮  Ⓝ⑤-⑳  ⒸⒸⓈ  Ⓙ  ⒸⒽⒶ  Ⓣ')

  #@unittest.skip("")
  def test_get_stations_nearest_neighboorhood(self):
    finder = EVFinder()
    station_list = utils.form_list_of_stations(finder.get_stations_nearest('wrigleyville, chicago', limit=5).get('fuel_stations'))
    full_list = tabulate(station_list, tablefmt='plain') # plain | simple

    chunks = utils.split_text_into_chunks(finder.title + '\n' + full_list)
    for idx, chunk in enumerate(chunks, start=1):
      logging.debug(f"Chunk {idx}:\n{chunk}\n")
    
    self.assertEqual(len(station_list), 5)
    self.assertEqual(len(chunks), 2)

  #@unittest.skip("")
  def test_get_stations_nearest_city(self):
    finder = EVFinder()
    station_list = utils.form_list_of_stations(finder.get_stations_nearest('Chicago', limit=7).get('fuel_stations'))
    full_list = tabulate(station_list, tablefmt='plain') # plain | simple

    chunks = utils.split_text_into_chunks(finder.title + '\n' + full_list)
    for idx, chunk in enumerate(chunks, start=1):
      logging.debug(f"Chunk {idx}:\n{chunk}\n")
    
    self.assertEqual(len(station_list), 7)
    self.assertEqual(len(chunks), 2)

  #@unittest.skip("")
  def test_get_stations_nearest_empty(self):
    finder = EVFinder()
    station_list = utils.form_list_of_stations(finder.get_stations_nearest('', limit=7).get('fuel_stations'))
    full_list = tabulate(station_list, tablefmt='plain') # plain | simple

    chunks = utils.split_text_into_chunks(finder.title + '\n' + full_list)
    for idx, chunk in enumerate(chunks, start=1):
      logging.debug(f"Chunk {idx}:\n{chunk}\n")
    
    self.assertEqual(len(station_list), 0)
    self.assertEqual(len(chunks), 0)

  #@unittest.skip("")
  def test_get_stations_nearest_nonsense(self):
    finder = EVFinder()
    station_list = utils.form_list_of_stations(finder.get_stations_nearest(r'^%^$ calweiu%crwefr nf fwpi%20uefb fr', 
                                                                           limit=7).get('fuel_stations'))
    logging.debug(station_list)
    full_list = tabulate(station_list, tablefmt='plain') # plain | simple
    logging.debug(full_list == '')
    
    self.assertEqual(len(station_list), 0)

  @unittest.skip("")
  def test_set_location(self):
    finder = EVFinder()
    finder.set_location('west loop, chicago')
    self.assertEqual(finder.zip, '60602')

  @unittest.skip("")
  def test_set_location_query_too_broad(self):
    finder = EVFinder()
    finder.set_location('chicago')
    self.assertTrue(hasattr(finder, 'zip'))
    self.assertEqual(finder.zip, '')

  @unittest.skip("")
  def test_set_location_query_empty(self):
    finder = EVFinder()
    finder.set_location('')
    self.assertFalse(hasattr(finder, 'zip'))

  @unittest.skip("")
  def test_set_location_query_nonsense(self):
    finder = EVFinder()
    finder.set_location(r'^%^$ calweiu%crwefr nf fwpi%20uefb fr')
    self.assertFalse(hasattr(finder, 'zip'))

  @unittest.skip("")
  def test_get_stations(self):
    finder = EVFinder() 
    finder.set_location('wrigleyville, chicago')
    station_list = utils.form_list_of_stations(finder.get_stations().get('fuel_stations'))
    
    full_list = tabulate(station_list, tablefmt='plain') # plain | simple
    chunks = utils.split_text_into_chunks(finder.title + '\n' + full_list)

    for idx, chunk in enumerate(chunks, start=1):
      logging.debug(f"Chunk {idx}:\n{chunk}\n")
    
    self.assertEqual(len(station_list), 5)
    self.assertEqual(len(chunks), 2)
  
  @unittest.skip("")
  def test_get_stations_no_zip(self):
    finder = EVFinder() 
    finder.set_location('chicago')
    self.assertIsNone(finder.get_stations())

  @unittest.skip("")
  def test_get_stations_empty(self):
    finder = EVFinder() 
    finder.set_location('')
    self.assertIsNone(finder.get_stations())

  @unittest.skip("")
  def test_get_stations_nonsense(self):
    finder = EVFinder() 
    finder.set_location(r'^%^$ calweiu%crwefr nf fwpi%20uefb fr')
    self.assertIsNone(finder.get_stations())

suite = unittest.TestLoader().loadTestsFromTestCase(TestWorker)
unittest.TextTestRunner(verbosity=2).run(suite)
