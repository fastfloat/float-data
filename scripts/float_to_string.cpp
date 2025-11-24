#include <charconv>
#include <vector>
#include <fstream>

int main(int argc, char** argv) {
  if (argc != 2) {
    std::fprintf(stderr, "Usage: %s <input_float_bin_file>\n", argv[0]);
    return 1;
  }

  std::ifstream in(argv[1], std::ios::binary);
  std::vector<char> buf(sizeof(float));

  float f;
  while (in.read((char*)&f, sizeof(f))) {
    char out[64];
    auto result = std::to_chars(out, out + sizeof(out), f);
    *result.ptr = '\n';
    std::fwrite(out, 1, result.ptr - out + 1, stdout);
  }
}
