
import sys
import itertools

from fabulous import image


class DebugImage(image.Image):
    def reduce(self, colors):
        need_reset = False
        line = ''
        for color, items in itertools.groupby(colors):
            if color is None:
                if need_reset:
                    line = line[:-1] + ">"
                    need_reset = False
                line += 'T' + (self.pad * len(list(items)))[1:]
            elif color == "EOL":
                if need_reset:
                    line = line[:-1] + ">"
                    need_reset = False
                    yield line.rstrip(' T')
                else:
                    yield line.rstrip(' T')
                line = ''
            else:
                need_reset = True
                line += '<' + (self.pad * len(list(items)))[1:]


if __name__ == '__main__':
    for imgpath in sys.argv[1:]:
        for line in DebugImage(imgpath):
            print line
