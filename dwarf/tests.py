# -*- coding: UTF-8-*
import os
import application
import unittest
import tempfile,operator

class DwarfTestCase(unittest.TestCase):
    def setUp(self):
	application.app.config.from_object('config.TestingConfig')
	self.app = application.app.test_client()
	self.basedir = os.path.abspath(os.path.dirname(__file__))

    def tearDown(self):
	pass

    def test_initialize(self):
	assert os.path.exists(os.path.join(self.basedir + '/content/')) == 1
	assert os.listdir(os.path.join(self.basedir + '/content/')) != []

    def test_home(self):
	rv = self.app.get('/')
	assert rv.mimetype == 'text/html'
	assert rv.status_code == 200
	assert rv.charset == 'utf-8'
	assert 'DWARF' in rv.data


    def test_pagination(self):
	""" test pagination , fixe pagination to 5 to  allow testing
	-- set pagination.PEER_PAGE =5
	"""

	l= application.content_list('blog')
	l_sorted =sorted(
		l,
		key	= operator.itemgetter("date"),
		reverse = True)
	index = l_sorted[6]
	expected = index["title"].encode("utf-8")
	print expected
	# --out Petit bilan des seances de prise en main Ubuntu--
	# as title , depend of the content of your blog (Markdown
	# files
	rv = self.app.get('/')
	assert expected not in rv.data
	rv = self.app.get('page/2')
	assert expected in rv.data


if __name__ == '__main__':
   unittest.main()
