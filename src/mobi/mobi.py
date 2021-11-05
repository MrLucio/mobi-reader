from datetime import date, datetime
from typing import Dict, List, Tuple, Union
from mobi.type import Type
from mobi.lz77 import decompress

class Mobi:

  pdb_header_fields = [
    {
      "name": "name",
      "size": 32,
      "type": Type.STRING
    },
    {
      "name": "file_attributes",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "version",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "creation_time",
      "size": 4,
      "type": Type.PDB_DATETIME
    },
    {
      "name": "modification_time",
      "size": 4,
      "type": Type.PDB_DATETIME
    },
    {
      "name": "backup_time",
      "size": 4,
      "type": Type.PDB_DATETIME
    },
    {
      "name": "modification_number",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "app_info",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "sort_info",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "type",
      "size": 4,
      "type": Type.STRING
    },
    {
      "name": "creator",
      "size": 4,
      "type": Type.STRING
    },
    {
      "name": "unique_id_seed",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "next_record_list",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "num_records",
      "size": 2,
      "type": Type.INT
    }
  ]

  palm_header_fields = [
    {
      "name": "compression",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "unused",
      "size": 2,
      "type": Type.UNUSED
    },
    {
      "name": "text_length",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "record_count",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "record_size",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "encryption_type",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "unknown",
      "size": 2,
      "type": Type.UNUSED
    },
  ]

  mobi_header_fields = [
    {
      "name": "identifier",
      "size": 4,
      "type": Type.STRING
    },
    {
      "name": "header_length",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "mobi_type",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "text_encoding",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "uid",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "generator_version",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "unusued",
      "size": 40,
      "type": Type.UNUSED
    },
    {
      "name": "first_nonbook_index",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "full_name_offset",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "full_name_length",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "locale",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "input_language",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "output_language",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "minimum_version",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "first_image_index",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "huffman_record_offset",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "huffman_record_count",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "huffman_table_offset",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "huffman_table_length",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "exth_flags",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "unused",
      "size": 36,
      "type": Type.UNUSED
    },
    {
      "name": "drm_offset",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "drm_count",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "drm_size",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "drm_flags",
      "size": 4,
      "type": Type.INT
    },
    {
      "name": "unused",
      "size": 8,
      "type": Type.UNUSED
    },
    {
      "name": "first_content_number",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "last_content_number",
      "size": 2,
      "type": Type.INT
    },
    {
      "name": "unused",
      "size": 44,
      "type": Type.NULL
    },
    {
      "name": "extra_flags",
      "size": 4,
      "type": Type.INT
    },
  ]


  def __init__(self, path: str):
    self.file = open(path, 'rb')

    self.record_list = []

    self.pdb_header = {}
    self.palm_header = {}
    self.mobi_header = {}


  def close(self) -> None:
    self.file.close()


  def read(self) -> bytearray:
    self.load_pdb_headers()
    self.load_record_list()
    self.load_record0()
    self.load_mobi_headers()

    output = bytearray()

    record_count = self.palm_header["record_count"]

    for i in range(1, record_count + 1):
      output += self.read_text_record(i)

    return output


  def decode_raw_data(self, raw_data: bytes, type: Type) -> Union[int, str, datetime, None]:
    value = None

    if type == Type.INT:
      value = int.from_bytes(raw_data, "big")
    elif type == Type.STRING:
      value = raw_data.decode("UTF-8")
    elif type == Type.PDB_DATETIME:
      value = int.from_bytes(raw_data, "big")
      value = datetime.fromtimestamp(value)

    return value


  def load_by_fields(self, fields: List[Dict[str]], target: dict) -> None:
    for field in fields:
      name, size, type = field.values()

      raw_data = self.file.read(size)
      value = self.decode_raw_data(raw_data, type)

      if value == None:
        continue

      target[name] = value


  # https://en.wikipedia.org/wiki/PDB_(Palm_OS)
  def load_pdb_headers(self) -> None:
    self.load_by_fields(self.pdb_header_fields, self.pdb_header)


  def load_record_list(self) -> None:
    for i in range(0, self.pdb_header["num_records"]):
      record = {}

      record["offset"] = self.decode_raw_data(self.file.read(4), Type.INT)
      record["attributes"] = self.decode_raw_data(self.file.read(1), Type.INT)
      
      self.file.read(3)

      self.record_list.append(record)


  def load_record0(self) -> None:
    self.file.seek(self.record_list[0]["offset"]) # move to first record's offset

    self.load_by_fields(self.palm_header_fields, self.palm_header)


  def load_mobi_headers(self) -> None:
    self.load_by_fields(self.mobi_header_fields, self.mobi_header)


  # VLQ = Variable-Length Quantity
  @staticmethod
  def get_vlq(data: bytes) -> Tuple[int, int, int]:
    pos = len(data) - 1
    length = 0
    result = 0

    mask = 0x7F
    end = 0x80

    while True:
      byte = data[pos]
      result |= (byte & mask) << (7 * length)
      pos -= 1
      length += 1

      if byte & end or length >= 4:
        break

    return (result, length, pos)


  def get_record_extra_size(self, data: bytes) -> int:
    pos = len(data) - 1
    extra_flags = self.mobi_header["extra_flags"]

    extra_size = 0

    for i in range(15, 0, -1):
      if extra_flags & (1 << i):
        [result, length, pos] = self.get_vlq(data)
        pos -= result - length
        extra_size += result

    if extra_flags & 1:
      extra_size += (data[pos] & 0x3) + 1

    return extra_size


  def read_image(self, recindex):
    first_image_index = self.mobi_header["first_image_index"]
    start = self.record_list[first_image_index + recindex - 1]["offset"]
    end = self.record_list[first_image_index + recindex]["offset"]

    self.file.seek(start)
    image = self.file.read(end - start)

    return image


  def read_text_record(self, index: int) -> bytearray:
    start = self.record_list[index]["offset"]
    end =  self.record_list[index + 1]["offset"]

    self.file.seek(start) # move cursor to record's start
    data = self.file.read(end - start)  # read whole record

    extra_size = self.get_record_extra_size(data)
    
    return decompress(data[:-extra_size])
