from mobi import Mobi


# Test the reader with Alice In Wonderland's mobi file
# Available at: https://www.gutenberg.org/ebooks/11
def test_book_1():
  reader = Mobi('./alice_in_wonderland.mobi')
  reader.to_html(with_images=True)  # will generate a folder with images and HTML output
  reader.close()


# Test the reader with Divine Comedy's mobi file
# Available at: https://www.gutenberg.org/ebooks/8799
def test_book_2():
  reader = Mobi('./divine_comedy.mobi')
  reader.to_html(with_images=True)  # will generate a folder with images and HTML output
  reader.close()
