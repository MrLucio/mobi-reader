from mobi import Mobi

# Test the reader with Alice In Wonderland's mobi file
# Available at: https://www.gutenberg.org/ebooks/11
def test_reader():
  reader = Mobi('./alice_in_wonderland.mobi')
  output = reader.read()  # bytearray containing the decoded mobi file
  reader.close()
