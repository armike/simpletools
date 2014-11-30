#!/usr/local/bin/python

def _getSubLists(paths, maxCount=3000, joiner=' '):
    """
    :Parameters:
        paths : `str list`
            Paths.
    :Returns:
        Result of joiner.join(paths), broken up into separate strings that
        are all less than maxCount length.  The full list is divided by
        two repeatedly in order to keep reasonably balanced lists.
    :Rtype:
        `str list`
    """
    results = []
    joined = joiner.join(paths)
    if len(joined) > maxCount:
        return _getSubLists(paths[0:len(paths)/2], maxCount, joiner) + \
            _getSubLists(paths[len(paths)/2:], maxCount, joiner)
    else:
        return [joined]
    return results

def main():
    print _getSubLists('a b c d e f g h i j k l m n o p q r s t u v w y x z'.split(),
    maxCount=5, joiner=' ')

if __name__ == '__main__':
    main()
