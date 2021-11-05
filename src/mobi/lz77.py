# https://en.wikibooks.org/wiki/Data_Compression/Dictionary_compression#PalmDoc
# https://github.com/woshifyz/mobi_reader/blob/fdd4536c6b42b181342cf248a2b71051b474f7ca/mobi.js#L99

def decompress(data: bytes) -> bytearray:
	length = len(data)
	offset = 0

	result = bytearray()

	while offset < length:
		char = data[offset]

		offset += 1

		if char == 0:
			result.append(char)
			
		elif char <= 0x08:
			for i in range(0, char):
				if offset + i < length:
					result.append(data[offset + i])
			offset += char

		elif char <= 0x7f:
			result.append(char)

		elif char <= 0xbf:
			next = data[offset]

			distance = (((char << 8) | next) & 0x3ff8) >> 3
			lz_length = (next & 0x07) + 3

			result_length = len(result)
			for i in range(0, lz_length):
				result.append(result[result_length - distance])
				result_length += 1

			offset += 1

		else:
			result.append(32)
			result.append(char ^ 0x80)

	return result
