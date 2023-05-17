# coding=utf-8
import os
import shutil
import tempfile
import unittest
import transcode


class TestGetSuffix(unittest.TestCase):
    def test_flac(self):
        self.assertEqual(transcode.get_suffix('FLAC'), '[FLAC]')

    def test_320(self):
        self.assertEqual(transcode.get_suffix('320'), '[320]')

    def test_v0(self):
        self.assertEqual(transcode.get_suffix('V0'), '[V0]')


class TestGetBasename(unittest.TestCase):
    def test_all(self):
        b = {
            'artist': 'artist',
            'album': 'album',
            'year': '2000',
            'media': 'CD',
            'remaster': 'remaster'
        }
        self.assertEqual(transcode.get_basename(b), 'artist - album (remaster)(2000)[CD]')

    def test_no_remaster(self):
        b = {
            'artist': 'artist',
            'album': 'album',
            'year': '2000',
            'media': 'CD',
        }
        self.assertEqual(transcode.get_basename(b), 'artist - album(2000)[CD]')

    def test_no_remaster_no_media(self):
        b = {
            'artist': 'artist',
            'album': 'album',
            'year': '2000',
        }
        self.assertEqual(transcode.get_basename(b), 'artist - album(2000)')

    def test_no_remaster_no_media_no_year(self):
        b = {
            'artist': 'artist',
            'album': 'album',
        }
        self.assertEqual(transcode.get_basename(b), 'artist - album')

    def test_album(self):
        b = {
            'album': 'album',
        }
        self.assertEqual(transcode.get_basename(b), 'album')


class TestGetTranscodeDir(unittest.TestCase):
    def test_no_prompt_smart_shorten_all(self):
        dir = tempfile.mkdtemp('flacdir')
        flac = open(os.path.join(dir, '1.flac'), 'w')
        b = {
            'artist': 'my artist is long enough to get the name reduced to just the album',
            'album': 'an album just long enough so that everything else is dropped to make an acceptable basename. filling filling filling filling filling filling filling filling filling',
            'year': '2000',
            'media': 'CD',
            'remaster': 'remaster'
        }
        expected = b['album'] + '[V0]'
        actual = transcode.get_transcode_dir(dir, '', 'ignored', 'V0', True, b)
        self.assertEqual(expected, actual)
        shutil.rmtree(dir)

    def test_va_shortened(self):
        dir = tempfile.mkdtemp('flacdir')
        flac = open(os.path.join(dir, '1.flac'), 'w')
        b = {
            'artist': 'Various Artists',
            'album': 'Album',
            'year': '2000',
            'media': 'CD',
        }
        expected = 'VA - Album(2000)[CD][V0]'
        actual = transcode.get_transcode_dir(dir, '', 'ignored', 'V0', True, b)
        self.assertEqual(expected, actual)
        shutil.rmtree(dir)


class TestGetSuitableBasename(unittest.TestCase):
    def test_ascii(self):
        name = 'Artist - Album (2000) [FLAC]'
        expected = name
        actual = transcode.get_suitable_basename(name)
        self.assertEqual(expected, actual)

    def test_japanese(self):
        name = u'Nihon Kogakuin College (日本工学院専門学校) - (1985) Pink Papaia {NKS MD8503A 24-96 Vinyl} [FLAC]'
        expected = name
        actual = unicode(transcode.get_suitable_basename(name),"utf-8")
        self.assertEqual(expected, actual)

    def test_illegal_characters(self):
        name = 'fi:l*e/p\"a?t>h|.t<xt \0_abc<d>e%f/(g)h+i_0.txt'
        expected = 'fi,lepath.txt _abcde%f(g)h+i_0.txt'
        actual = transcode.get_suitable_basename(name)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
