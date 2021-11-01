from mobi import Mobi


# Test the reader with Alice In Wonderland's mobi file
# Available at: https://www.gutenberg.org/ebooks/11
def test_book_1():
  reader = Mobi('./alice_in_wonderland.mobi')
  output = reader.read()  # bytearray containing the decoded mobi file
  reader.close()


# Test the reader with Divine Comedy's mobi file
# Available at: https://www.gutenberg.org/ebooks/8799
def test_book_2():
  reader = Mobi('./divine_comedy.mobi')
  output = reader.read()  # bytearray containing the decoded mobi file
  reader.close()
