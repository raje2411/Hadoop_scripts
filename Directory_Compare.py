from filecmp import dircmp
def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print "diff_file %s found in %s and %s" % (name, dcmp.left,
              dcmp.right)
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

dcmp = dircmp('/Users/rraman/Desktop/temp/dir1/', '/Users/rraman/Desktop/temp/dir2/')
dcmp
# print_diff_files(dcmp)
